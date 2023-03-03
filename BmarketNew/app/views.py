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
            return Response(serializer.data,status=status.HTTP_201_CREATED)
   
    def perform_create(self, serializer):
        user = self.request.user
        CustomerBankAccount.set_user_is_active(user)
        serializer.save(customer=user,is_active = True)


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

   


