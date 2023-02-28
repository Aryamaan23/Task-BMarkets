from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _
from .managers import CustomUserManager
from rest_framework.authtoken.models import Token    
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver



class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    pan_number = models.CharField(max_length=10)
    phone_number = models.IntegerField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username','first_name','last_name','phone_number','pan_number')

    objects = CustomUserManager()

    def __str__(self):
        return self.email


'''
automatically creates token once the user is created
'''

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)





"""
account_number
ifsc_code
customer
bank
cheque_image
branch_name
is_cheque_verified
name_as_per_bank_record
verification_mode
verification_status
account_type
"""

class Bank(models.Model):
    bank_id=models.CharField(max_length=30)
    bank_name=models.CharField(max_length=30)
    bank_website=models.URLField()
    bank_number=models.CharField(max_length=30)
    bank_logo=models.ImageField()

    def __str__(self):
        return self.bank_name


class CustomerBankAccount(models.Model):
    ACCOUNT_CHOICES = [
        ('savings', 'Savings'),
        ('current', 'Current')
    ]
    account_number = models.CharField(max_length=50)
    ifsc_code=models.CharField(max_length=50)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE)
    cheque_image=models.ImageField(null=True,blank=True)
    branch_name=models.CharField(max_length=30)
    is_cheque_verified=models.BooleanField()
    name_as_per_bank_record=models.CharField(max_length=30)
    verification_mode=models.CharField(max_length=30)
    verification_status=models.BooleanField()
    account_type = models.CharField(max_length=50,choices=ACCOUNT_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    is_active=models.BooleanField(default=True)


    class Meta:
        unique_together=('account_number','ifsc_code')


"""
@receiver(pre_save, sender=CustomerBankAccount)
def limit_banks_per_pan(sender, instance, **kwargs):
    # Get the user's PAN from the bank account
        pan = instance.user.pan

    # Count the number of active and inactive bank accounts for the user
        num_active_banks = CustomerBankAccount.objects.filter(user__pan=pan, is_active=True).count()
        num_inactive_banks = CustomerBankAccount.objects.filter(user__pan=pan, is_active=False).count()

    # Check if adding the current bank account would exceed the maximum limit
        if num_active_banks >= 1 or num_inactive_banks >= 3:
            raise ValidationError('Cannot add another bank account for this PAN.')

"""
    
"""
    def save(self, *args, **kwargs):
        self.pk = f"{self.account_number}-{self.ifsc_code}"
        super(CustomerBankAccount, self).save(*args, **kwargs)

"""


