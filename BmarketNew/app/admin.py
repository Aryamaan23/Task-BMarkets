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



from django.contrib import messages
class BankAdmin(admin.ModelAdmin):
    list_display = ('id','bank_id','bank_name','bank_website','bank_number','bank_logo')


class CustomerBankaccountAdmin(admin.ModelAdmin):
    #form=CustomerBankForm
    list_display=('id','account_number','ifsc_code','is_active','customer','bank','cheque_image','branch_name','is_cheque_verified','name_as_per_bank_record','verification_mode','verification_status','account_type')
    list_editable = ('verification_status',)



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Bank,BankAdmin)
admin.site.register(CustomerBankAccount,CustomerBankaccountAdmin)