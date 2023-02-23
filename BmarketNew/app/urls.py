from django.urls import path,include
from app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user',views.CustomUserModalViewSets,basename='user' )

urlpatterns = [
    
    path('',include(router.urls)),
    path('auth/',include('rest_framework.urls'),name='restframework'),
    path('api-auth-token/',views.CustomAuthToken.as_view(),name='api-auth-token'),
    
]