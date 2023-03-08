from django.contrib import admin

# Register your models here.
# Register your models here.
#from django.contrib.auth.admin import UserAdmin

from kbapp.models import Amc
from django.core.exceptions import ValidationError


class AmcAdmin(admin.ModelAdmin):

    model = Amc
    list_display = ('name','created','modified','is_active','modified_by','created_by','name','amfi_nav_download_dropdown_code',
                   'amc_assets_under_management','description','is_being_sold','f_amc_code','amc_logo','amc_website_url','scheme_information_document_url','nominee_url'
                   )

admin.site.register(Amc, AmcAdmin)


