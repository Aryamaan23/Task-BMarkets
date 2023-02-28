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
from .permissions import CustomerAccessPermission
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate,get_user_model

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


    

class CustomerBankAccountModellViewSets(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = CustomerBankAccount.objects.all()
    serializer_class =CustomerBankAccountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    # def perform_create(self, serializer):
    #     token_key = self.request.headers.get('Authorization').split(' ')[1]
    #     token = Token.objects.get(key=token_key)
    #     user = token.user
    #     #bank_account=CustomerBankAccount.account_number
    #     serializer.validated_data['id'] = self.request.data['customer']
    #     user_bank_accounts = CustomerBankAccount.objects.get(account_number=CustomerBankAccount.account_number)
    #     self.request.data['account_number']=user_bank_accounts.account_number
    #     for bank_account in user_bank_accounts:
    #         bank_account.is_active = False
    #         bank_account.save()
    #     serializer.save(is_active=True)
    #     return super().perform_create(serializer)

    
    """
    def perform_create(self, serializer):
        serializer.validated_data['account_number'] = self.request.account_number
        user_bank_accounts = CustomerBankAccount.objects.filter(account_number=self.request.user)
        for bank_account in user_bank_accounts:
            bank_account.is_active = False
            bank_account.save()
        serializer.save(is_active=True)
    """

   
   
    def get_queryset(self):
        # Get the user object
        token_key = self.request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(key=token_key)
        user=token.user
        customer=CustomUser.objects.get(email=user.email)
        self.request.data['customer']=customer.id
        active_banks = CustomerBankAccount.objects.filter(customer=self.request.data['customer'],is_active=True)
        return active_banks

   

    def create(self, request, *args, **kwargs):
        token_key = self.request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(key=token_key)
        user=token.user
        customer=CustomUser.objects.get(email=user.email)
        request.data['customer']=customer.id
        user_bank_accounts = CustomerBankAccount.objects.filter(customer=self.request.data['customer'])
        for bank_account in user_bank_accounts:
            bank_account.is_active = False
            bank_account.save()
        #self.serializer.save(is_active=True)
        print(request.data['customer'])
        return super().create(request, *args, **kwargs)




"""
    def perform_create(self, serializer):
        # Get the token from the request header
        token_key = self.request.headers.get('Authorization').split(' ')[1]
        # Get the token object from the database
        print('token_key:---------------------------',token_key)
        token = Token.objects.get(key=token_key)
        # Get the user associated with the token
        user = token.user
 
        # Get the customer associated with the user's email
        try:
            customer = CustomUser.objects.get(email=user.email)
            print('email--------------------------',customer)
        except CustomUser.DoesNotExist:
            return Response({"error":"Customer not found"})
 
        account_count = CustomerBankAccount.objects.filter(customer=customer).count()
        if account_count >= 4:
            return Response({"error":"You cannot create more than 4 accounts for this user"})
 
        # Set the customer in the serializer and save the object
        serializer.validated_data['customer'] = customer
        serializer.save()

"""

  
"""
    def create_bank_account(request):
    if request.method == 'POST':
        # Retrieve the logged-in user's email
        user_email = request.user.email
        # Create a new bank account object and associate it with the user
        new_account = BankAccount(user_email=user_email, account_number=request.POST['account_number'])
        new_account.save()
        return render(request, 'bank_account_created.html', {'account_number': new_account.account_number})
    else:
        return render(request, 'create_bank_account.html')

"""


"""
    def get_queryset(self):
        queryset =super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(id=self.request.user.id)

        return queryset

    
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomerAccessPermission]

    def list(self, request):
        logger.debug(str(self.queryset.query))
        return super().list(request)

    def get_queryset(self):
        queryset =super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(id=self.request.user.id)

        return queryset

    def create(self,request, *args, **kwargs):
        serilaizer = CustomerBankAccountSerializer(data=request.data)
        if serilaizer.is_valid():
            customer = serilaizer.save()
            token = Token.objects.get(user=customer)
            return Response({'customer': serilaizer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

"""


class BankModellViewSets(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Bank.objects.all()
    serializer_class =BankSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """"
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomerAccessPermission]

    def list(self, request):
        logger.debug(str(self.queryset.query))
        return super().list(request)

    def get_queryset(self):
        queryset =super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(id=self.request.user.id)

        return queryset

    def create(self,request, *args, **kwargs):
        serilaizer = CustomerBankAccountSerializer(data=request.data)
        if serilaizer.is_valid():
            customer = serilaizer.save()
            token = Token.objects.get(user=customer)
            return Response({'customer': serilaizer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

"""

