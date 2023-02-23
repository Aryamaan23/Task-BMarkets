from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from app.serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

CustomUser=get_user_model()

class CustomUserViewSet(ViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer
    
    def create(self, request):
        # handle user registration
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response(serializer.errors, status=400)
        
    def retrieve(self, request):
        # handle user login
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({'token': token.key, 'user': serializer.data})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
    
    """
    def list(self, request):
        # handle user login
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({'token': token.key, 'users': {'user': serializer.data})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

    """



    def get_queryset(self):
        if self.request.user.is_superuser:
            # superuser can see all user data
            return CustomUser.objects.all()
        else:
            # regular user can only see their own data
            return CustomUser.objects.filter(id=self.request.user.id)

