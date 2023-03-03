from rest_framework import serializers
from .models import CustomUser,CustomerBankAccount,Bank
from django.contrib.auth import authenticate,get_user_model
from rest_framework.authtoken.models import Token


CustomUser = get_user_model()
class CustomUserSerializer(serializers.ModelSerializer):
    """
    For handling the fields in the response of the customer
    """
    class Meta:
        model = CustomUser
        #fields='__all__'
        fields = ['id','first_name','middle_name','last_name','email','pan_number','phone_number','password','username']
        
    
    def create(self,validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password,**validated_data)
        return user


class BankSerializer(serializers.ModelSerializer):
    """
    For handling the fields in the response of the bank
    """
    class Meta:
        model=Bank
        fields='__all__'


class CustomerBankAccountSerializer(serializers.ModelSerializer):
    """
    For handling the fields in the response of the customer bank account
    """
    class Meta:
        model=CustomerBankAccount
        #fields='__all__'
        exclude=['is_active','verification_status']

   
  
    def to_representation(self, instance):
        """
        For adding the bank logo in the get response
        """
        data = super().to_representation(instance)
        data['bank_logo']=instance.bank.bank_logo
        data['bank_name']=instance.bank.bank_name
        data['bank_logo'] = self.context['request'].build_absolute_uri(data['bank_logo'].url)
        return data
    


    def validate_customer(self, customer):
        """
        Validation so that the customer can't add more than 4 bank accounts
        """
        account_number=CustomerBankAccount.objects.filter(customer=customer).count()
        # Check if the user already has 4 accounts in the bank
        if account_number >= 4:
            raise serializers.ValidationError("You cannot create more than 4 accounts in this bank.")

        return customer
    


    def update(self, instance, validated_data):
        """
        If the status is active but the verification status is true then the user can't update the details of the account
        """
        if instance.is_active is True:
            if instance.verification_status is True:
                raise serializers.ValidationError("You can't update the account as verification status is true")
        else:
            """
            Only these specific fields can be edited by the customer
            """
            instance.account_number = validated_data.get('account_number', instance.account_number)
            instance.ifsc_code = validated_data.get('ifsc_code', instance.ifsc_code)
            instance.branch_name = validated_data.get('branch_name', instance.branch_name)
            instance.name_as_per_bank_record = validated_data.get('name_as_per_bank_record', instance.name_as_per_bank_record)
            instance.verification_mode = validated_data.get('verification_mode', instance.verification_mode)
            instance.account_type = validated_data.get('account_type', instance.account_type)
            #return instance
        return super().update(instance, validated_data)
        
        #return super().update(instance, validated_data)
   

   


