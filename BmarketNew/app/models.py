from django.db import models
from .managers import CustomUserManager

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    # add additional fields in here
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=30)
    middle_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    pan_number=models.CharField(max_length=30)

    objects=CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]


    """
    address = models.CharField(max_length=250)
    dob = models.DateField()
    mobile = models.CharField(max_length=30)
    """

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


