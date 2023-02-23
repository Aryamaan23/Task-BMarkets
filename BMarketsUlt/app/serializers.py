from rest_framework import serializers
from . models import CustomUser
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = CustomUser
        fields = ('id', 'username', 'password', 'email', 'first_name', 'middle_name', 'last_name','pan_number')