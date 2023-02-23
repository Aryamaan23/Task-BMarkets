from django.urls import path, include
from rest_framework import routers
from app.views import UserViewSet,CustomAuthToken
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', CustomAuthToken.as_view())
    
]
