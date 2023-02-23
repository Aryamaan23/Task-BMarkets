from django.contrib.auth import get_user_model
from rest_framework import viewsets,mixins
from app.serializers import UserSerializer
#from app.permissions import IsCreationOrIsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import CustomerAccessPermission
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from rest_framework import viewsets, mixins, exceptions, authentication
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        print(serializer.initial_data)
        serializer.is_valid(raise_exception=False)
        user = serializer.validated_data['user']
        print(serializer.validated_data)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserViewSet(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.CreateModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomerAccessPermission]

    def get_queryset(self):
        queryset=super().get_queryset()
        if not self.request.user.is_superuser:
            queryset=queryset.filter(id=self.request.user.id)
        return queryset
