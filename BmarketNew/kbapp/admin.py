from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
# Register your models here.
#from django.contrib.auth.admin import UserAdmin

from kbapp.models import Amc
from django.core.exceptions import ValidationError



class AmcAdmin(admin.ModelAdmin):

    model = Amc
    list_display = [field.name for field in Amc._meta.fields]

admin.site.register(Amc, AmcAdmin)
