from rest_framework import serializers
from .models import CustomUser,CustomerBankAccount,Bank
from django.contrib.auth import authenticate,get_user_model
from rest_framework.authtoken.models import Token
#from django.utils.encoding import force_text


CustomUser = get_user_model()
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        #fields='__all__'
        fields = ['id','first_name','middle_name','last_name','email','pan_number','phone_number','password','username']
        
    
    def create(self,validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password,**validated_data)
        return user


    


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bank
        fields='__all__'


class CustomerBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerBankAccount
        #fields='__all__'
        exclude=['is_active','verification_status']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['bank_logo']=instance.bank.bank_logo
        data['bank_name']=instance.bank.bank_name
        data['bank_logo'] = self.context['request'].build_absolute_uri(data['bank_logo'].url)
        return data
    

    def validate_customer(self, customer):
        
        account_number=CustomerBankAccount.objects.filter(customer=customer).count()
        # Check if the user already has 4 accounts in the bank
        if account_number >= 4:
            raise serializers.ValidationError("You cannot create more than 4 accounts in this bank.")

        return customer
    




    def update(self, instance, validated_data):
        if instance.verification_status==True:
             raise serializers.ValidationError("You can't update the account as verification status is true")
        else:
            instance.account_number = validated_data.get('account_number', instance.account_number)
            instance.ifsc_code = validated_data.get('ifsc_code', instance.ifsc_code)
            instance.branch_name = validated_data.get('branch_name', instance.branch_name)
            instance.name_as_per_bank_record = validated_data.get('name_as_per_bank_record', instance.name_as_per_bank_record)
            instance.verification_mode = validated_data.get('verification_mode', instance.verification_mode)
            instance.account_type = validated_data.get('account_type', instance.account_type)
            return instance
        
        return super().update(instance, validated_data)

   



# class CustomUserTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id','first_name','middle_name','last_name','email','pan_number','phone_number','password','username']
        
#     def create(self,validated_data):
#         password = validated_data.pop('password')
#         user = CustomUser.objects.create_user(password=password,**validated_data)
#         return user

# class CustomAuthSerializer(serializers.Serializer):
#     email = serializers.CharField(
#         label=("email"),
#         write_only=True
#     )
#     password = serializers.CharField(
#         label=_("Password"),
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         write_only=True
#     )
#     token = serializers.CharField(
#         label=_("Token"),
#         read_only=True
#     )

#     def validate(self, attrs):
#         email = attrs.get(_('email'))
#         password = attrs.get('password')

#         if email and password:
#             user = authenticate(request=self.context.get('request'),
#                                 email=email, password=password)

#             # The authenticate call simply returns None for is_active=False
#             # users. (Assuming the default ModelBackend authentication
#             # backend.)
#             if not user:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = _('Must include "username" and "password".')
#             raise serializers.ValidationError(msg, code='authorization')

#         attrs['user'] = user
#         return attrs


"""
    def validate(self, attrs):
        user = self.context['request'].user
        instance = CustomerBankAccount(**attrs)
        #print(instance)

        if user.is_superuser:
            # Count the number of accounts created by all users
             num_accounts = CustomerBankAccount.objects.filter(customer=instance.customer).count()
        else:
            # Count the number of accounts created by this user
             num_accounts = CustomerBankAccount.objects.filter(customer=instance.customer).count()
       
        if num_accounts >= 4:
            raise serializers.ValidationError("You cannot create more than 4 accounts in this bank.")
        return super().validate(attrs)
"""