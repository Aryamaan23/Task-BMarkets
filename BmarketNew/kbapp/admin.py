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



"""
 expense_ratio_url = models.CharField(max_length=200, null=True, blank=True)
    expense_ratio_url_remarks = models.CharField(max_length=200, null=True, blank=True)
    last_nav_pull_date_from_amfi = models.DateField(null=True, blank=True)
    rta_amc_code = models.CharField(max_length=64, null=True, blank=True)
    is_isip_available = models.BooleanField(default=True)
    cio = models.CharField(max_length=150, null=True, blank=True)
    ceo = models.CharField(max_length=150, null=True, blank=True)
    management_trustee = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    owner_type = models.CharField(max_length=50, null=True, blank=True)
    address1 = models.CharField(max_length=200, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    address3 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pin = models.IntegerField(null=True, blank=True)
    amc_aum_date = models.DateTimeField(null=True, blank=True)

"""
