from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm,CustomerBankForm
from .models import CustomUser,CustomerBankAccount,Bank
from django.core.exceptions import ValidationError

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser

    list_display = ('id','username', 'email','password','first_name','middle_name','last_name','phone_number','pan_number' ,'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


"""
 account_number = models.CharField(max_length=50)
    ifsc_code=models.CharField(max_length=50)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE)
    cheque_image=models.ImageField()
    branch_name=models.CharField(max_length=30)
    is_cheque_verified=models.BooleanField()
    name_as_per_bank_record=models.CharField(max_length=30)
    verification_mode=models.CharField(max_length=30)
    verification_status=models.BooleanField()
    account_type = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

"""

"""
from django.core.exceptions import ValidationError

class Lecture(models.Model):
    topic = models.CharField(max_length=100)
    speaker = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date > self.end_date::
            raise ValidationError("Dates are incorrect")

"""


from django.contrib import messages
class BankAdmin(admin.ModelAdmin):
    list_display = ('id','bank_id','bank_name','bank_website','bank_number','bank_logo')


class CustomerBankaccountAdmin(admin.ModelAdmin):
    #form=CustomerBankForm
    list_display=('id','account_number','ifsc_code','is_active','customer','bank','cheque_image','branch_name','is_cheque_verified','name_as_per_bank_record','verification_mode','verification_status','account_type')
    
    
    def save_model(self, request, obj, form, change):
        existing_count = CustomerBankAccount.objects.filter(customer=obj.customer).count()
        condition=True
        if existing_count >=4:
                messages.add_message(request, messages.ERROR, 'You cannot add more than 4 accounts')
            #raise ValidationError("You can't add more than 4 accounts.")
                condition=False
        if condition==True:
            super().save_model(request, obj, form, change)

    """
    def clean(self):
        if  CustomerBankAccount.objects.filter(customer=self.customer).count()>=4:
            raise ValidationError("You cannot create more than 4 accounts in this bank.")
    """


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Bank,BankAdmin)
admin.site.register(CustomerBankAccount,CustomerBankaccountAdmin)