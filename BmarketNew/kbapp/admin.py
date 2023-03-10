from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
# Register your models here.
#from django.contrib.auth.admin import UserAdmin

from kbapp.models import Amc,AMCFund,AMCFundScheme
from django.core.exceptions import ValidationError



class AmcAdmin(admin.ModelAdmin):

    model = Amc
    list_display = [field.name for field in Amc._meta.fields]



class AmcFundAdmin(admin.ModelAdmin):

    model = AMCFund
    list_display = [field.name for field in AMCFund._meta.fields]




class AmcFundSchemesAdmin(admin.ModelAdmin):

    model = AMCFundScheme
    list_display = [field.name for field in AMCFundScheme._meta.fields]

admin.site.register(Amc, AmcAdmin)
admin.site.register(AMCFund, AmcFundAdmin)
admin.site.register(AMCFundScheme,AmcFundSchemesAdmin)
