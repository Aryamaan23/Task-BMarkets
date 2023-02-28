from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *

from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        #fields = ('email',)
        fields='__all__'

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)



class CustomerBankForm(forms.ModelForm):

    class Meta:
        model=CustomerBankAccount
        fields='__all__'


    def clean(self):
        customer = self.cleaned_data['customer']
        if self.customer.count()>=4:
            raise forms.ValidationError({'customer': "Can't create more than 4 accounts"})


