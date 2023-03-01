from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from app.serializers import CustomUserSerializer,CustomerBankAccountSerializer,BankSerializer
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from .permissions import CustomerAccessPermission,IsSuperUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate,get_user_model
from rest_framework.decorators import action

#import logging

#logger = logging.getLogger(__name__)


class CustomAuthToken(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token = Token.objects.get(user=user)
            serializer = CustomUserSerializer(user)
            return Response({
                'token': token.key,
                #'user': serializer.data
                })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomUserModalViewSets(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomerAccessPermission]

    # def list(self, request):
    #     logger.debug(str(self.queryset.query))
    #     return super().list(request)

    def get_queryset(self):
        queryset =super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(id=self.request.user.id)

        return queryset

    def create(self,request, *args, **kwargs):
        serilaizer = CustomUserSerializer(data=request.data)
        if serilaizer.is_valid():
            customer = serilaizer.save()
            token = Token.objects.get(user=customer)
            return Response({'customer': serilaizer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)


    

class CustomerBankAccountModellViewSets(viewsets.ModelViewSet):
    queryset = CustomerBankAccount.objects.all()
    serializer_class =CustomerBankAccountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

   
    def get_queryset(self):
        user = self.request.user
        customer=CustomUser.objects.get(email=user.email)
        active_banks = CustomerBankAccount.objects.filter(customer=customer.id,is_active=True)
        return active_banks


    def create(self, request, *args, **kwargs):
        user = self.request.user
        customer=CustomUser.objects.get(email=user.email)
        request.data['customer']=customer.id
        user_bank_accounts = CustomerBankAccount.objects.filter(customer=customer.id)
        for bank_account in user_bank_accounts:
            bank_account.is_active = False
            bank_account.save()
        return super().create(request, *args, **kwargs)



class BankModellViewSets(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Bank.objects.all()
    serializer_class =BankSerializer
    #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly & IsSuperUser]






