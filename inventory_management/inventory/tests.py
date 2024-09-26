from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Item
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationTests(APITestCase):
    def test_user_registration_success(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully')

    def test_user_registration_invalid_data(self):
        url = reverse('register')
        data = {
            'username': '',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword123')

    def test_user_login_success(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ItemTests(APITestCase):
    def setUp(self):
        # Create a user and get their tokens
        self.user = User.objects.create_user(
            username='testuser', password='testpassword123')
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Create an initial item for testing
        self.item = Item.objects.create(
            name='Test Item', description='Test Description')

    def test_create_item(self):
        url = reverse('create_item')
        data = {
            'name': 'New Item',
            'description': 'New Item Description'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Item')

    def test_create_item_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        url = reverse('create_item')
        data = {
            'name': 'New Item',
            'description': 'New Item Description'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        url = reverse('item_detail', kwargs={'item_id': self.item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_get_item_not_found(self):
        url = reverse('item_detail', kwargs={'item_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item(self):
        url = reverse('item_detail', kwargs={'item_id': self.item.id})
        data = {
            'name': 'Updated Item',
            'description': 'Updated Description'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item')

    def test_update_item_not_found(self):
        url = reverse('item_detail', kwargs={'item_id': 999})
        data = {
            'name': 'Updated Item',
            'description': 'Updated Description'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item(self):
        url = reverse('item_detail', kwargs={'item_id': self.item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())

    def test_delete_item_not_found(self):
        url = reverse('item_detail', kwargs={'item_id': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
