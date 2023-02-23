from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import CustomUserViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    # other URLs
]