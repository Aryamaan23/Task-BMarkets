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
import logging
import json
import http

logger = logging.getLogger(__name__)

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

    """
    CustomerViewset for handling all the CRUD operations related to the customer
    """


    def get_queryset(self)-> CustomUser:
        """
        Fetch data of all the users if the user is a superuser and fetch only the data of that user if he/she is a normal user
        """
        queryset =super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(id=self.request.user.id)

        return queryset


    def create(self,request, *args, **kwargs) -> Response:
        """
        For creating the customer
        """
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

    """
    CustomerBankAccount Model Viewset is consumed to perform CRUD on bank account details.
    Only authorized user with the token can update his/her information
    """

    def get_queryset(self):
         """
         Filter based on the active_status of the bank accounts and fetch it
         """
         user = self.request.user
         active_banks=CustomerBankAccount.get_active_in_response(user)
         return active_banks
   
    
    # def get_queryset(self):
        
    #     user = self.request.user
    #     #active_banks=CustomerBankAccount.get_active_in_response(user)
    #     #return active_banks
    #     cookies = self.request.COOKIES
    #     print(type(cookies))
    #     print(cookies['account_data'])
        #print(type(cookies['account_data']))
        #print(cookies['account_data'])
        # set_cookie_header=cookies['account_data']
        # cookie = http.cookies.SimpleCookie(set_cookie_header)
        #print(cookie.value)
        #account_data = cookie['account_data'].value
        #account_data_dict = json.loads(account_data.replace("'", "\""))
        #return account_data_dict


        #print(cookies['account_data'])
        #return json.loads(cookies['account_data'])
        #data_dict=json.loads(cookies['account_data'])
        #return data_dict
        #string=cookies['account_data']
        #x=json.loads(string)
        #return x
        # Access the cookie value by key, e.g. cookies['account_data']
        # Return the queryset
        #queryset = super().get_queryset()
        #return queryset

    
    
    

    
    
    def create(self, request, *args, **kwargs) ->Response:
        """
        Override the create method to set the customer and set is_active=False for any existing bank accounts of the current user.
        Returns:
            Response: A response object containing the serialized customer bank account.
        """
        user = self.request.user
        request.data['customer']=user.id
        user_query = CustomerBankAccount.check_exsisting_account(user,request)
        if user_query:
            serializer = self.get_serializer(user_query)
            if CustomerBankAccount.fetch_exsisting_account_query(user,user_query) is False:
                return Response({'error':'Account is already in use'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception = True)
            self.perform_create(serializer)
            data_new=serializer.data
            bank_name,first_name,last_name,email = self.append_bank_data_in_cookie(data_new)
            # response=Response(serializer.data)
            # data_new2=self.append_bank_data_in_cookie(data_new)
            # response.set_cookie('account_data',json.dumps(data_new2))
            response=Response(serializer.data)
            response.set_cookie('name_as_per_bank_record',serializer.validated_data.get('name_as_per_bank_record'))
            response.set_cookie('branch_name',serializer.validated_data.get('branch_name'))
            response.set_cookie('bank_name',bank_name)
            response.set_cookie('first_name',first_name)
            response.set_cookie('last_name',last_name)
            response.set_cookie('email',email)
            return response
            

    def append_bank_data_in_cookie(self,data):
        bank_id=data['bank']
        bank=Bank.objects.get(bank_id=bank_id)
        bank_name=bank.bank_name
        first_name=self.request.user.first_name
        last_name=last_name=self.request.user.last_name
        email=self.request.user.email

        return bank_name,first_name,last_name,email
        #return data
   
    def perform_create(self, serializer):
        user = self.request.user
        CustomerBankAccount.set_user_is_active(user)
        serializer.save(customer=user,is_active = True)
        #account=serializer.save(customer=user,is_active = True)
        #account_data=CustomerBankAccountSerializer(account).data

        #response=Response({'status':'Account created successfully'})
        #response.set_cookie('account_data',account_data)
        #print(type(response.cookies['account_data']))
        #print(response.set_cookie)


    def update(self, request, *args, **kwargs):
    # Get the user and the instance being updated
        user = self.request.user
        instance = self.get_object()

        # Check if the instance belongs to the current user
        if instance.customer.id != user.id:
            return Response({'error': 'You are not authorized to update this account'}, status=status.HTTP_401_UNAUTHORIZED)

        # Remove the customer field from the request data in order to overcome the 
        if instance.is_active is True:
            request_data = request.data.copy()
            request_data.pop('customer', None)
            # Update the instance
            serializer = self.get_serializer(instance, data=request_data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        else:
            return Response("You can't update the account")
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        data={}
        data["bank_name"]=request.COOKIES.get('bank_name')
        data['first_name']=request.COOKIES.get('first_name')
        data['last_name']=request.COOKIES.get('last_name')
        data['email']=request.COOKIES.get('email')
        data["branch_name"] = request.COOKIES.get('branch_name')
        data["name_as_per_bank_record"] = request.COOKIES.get('name_as_per_bank_record')
        if data:
            return Response(data,status=status.HTTP_200_OK)
        # data=json.loads(request.COOKIES.get('account_data'))
        # return Response(data)
    

    # def retrieve(self, request, *args, **kwargs):
    #      user = self.request.user
    #      cookies = self.request.COOKIES
    #      cookie_data = cookies['account_data']
    #      print(cookie_data)
    #      if cookie_data:
    #          data = json.loads(cookie_data)
    #          serializer = self.get_serializer(data=data)
    #          serializer.is_valid(raise_exception=True)
    #          return Response(data)
    #      else:
    #          return Response({'error': 'Account data not found in cookie'}, status=status.HTTP_400_BAD_REQUEST)

    """
    # Set the user's other accounts as inactive if necessary
    if request.data.get('is_active') == False:
        CustomerBankAccount.set_user_is_active(user, except_account_id=instance.id)
    """

        



class BankModellViewSets(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    """
    BankViewset for doing the CRUD operations on the Master Bank Model.
    Custom Permission has been given only superuser has the access to perform CRUD on the Bank model.
    Normal User can't do any CRUD operations on the Bank Model.
    """
    queryset = Bank.objects.all()
    serializer_class =BankSerializer
    #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly & IsSuperUser]

   


