import logging
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Item
from .serializers import ItemSerializer, UserSerializer
from django.core.cache import cache


logger = logging.getLogger('inventory')

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id=None):
        if item_id:
            cached_item = cache.get(f'item_{item_id}')
            if cached_item:
                logger.info(f"Cache hit for item ID {item_id}.")
                return Response(cached_item)
            
            try:
                item = Item.objects.get(id=item_id)
                serializer = ItemSerializer(item)
                cache.set(f'item_{item_id}', serializer.data, timeout=60*15)
                logger.info(f"Cache miss for item ID {item_id}. Fetched from DB and stored in cache.")
                return Response(serializer.data)
            except Item.DoesNotExist:
                logger.error(f"Item with ID {item_id} not found.")
                return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            logger.debug("Fetched all items.")
            return Response(serializer.data)

    def post(self, request):
        logger.info(f"User {request.user} attempting to create an item.")
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Item created successfully by user {request.user}.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.error(f"Error creating item: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            logger.error(f"Attempt to update non-existent item ID {item_id} by user {request.user}.")
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'item_{item_id}')
            logger.info(f"Item ID {item_id} updated by user {request.user}. Cache cleared.")
            return Response(serializer.data)

        logger.error(f"Error updating item ID {item_id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            logger.error(f"Attempt to delete non-existent item ID {item_id} by user {request.user}.")
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        cache.delete(f'item_{item_id}')
        logger.info(f"Item ID {item_id} deleted by user {request.user}. Cache cleared.")
        return Response({'message': 'Item deleted'}, status=status.HTTP_204_NO_CONTENT)