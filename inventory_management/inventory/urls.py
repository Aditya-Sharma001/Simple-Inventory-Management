from django.urls import path
from .views import (
    ItemView,
    UserRegistrationView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('items/', ItemView.as_view(), name='create_item'),
    path('items/<int:item_id>/', ItemView.as_view(), name='item_detail'),
]
