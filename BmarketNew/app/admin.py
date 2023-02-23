from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,CustomerBankAccount,Bank

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser

    list_display = ('username', 'email','password','first_name','middle_name','last_name','phone_number','pan_number' ,'is_active',
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


class BankAdmin(admin.ModelAdmin):
    list_display = ('bank_id','bank_name','bank_website','bank_number','bank_logo')


class CustomerBankaccountAdmin(admin.ModelAdmin):
    list_display=('ifsc_code','customer','bank','cheque_image','branch_name','is_cheque_verified','name_as_per_bank_record','verification_mode','verification_status','account_type')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Bank,BankAdmin)
admin.site.register(CustomerBankAccount,CustomerBankaccountAdmin)