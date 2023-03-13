from django.core.management.base import BaseCommand
from datetime import datetime
from kbapp.models import AMCFundScheme,AMCFund
import json

path='/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/amcfundscheme.json'

class Command(BaseCommand):
     help = 'Stores fund data in the amcfund model'

     def handle(self,*args,**options):
         logic_file_class(path)
         self.stdout.write("Successfully created bank records")




def logic_file_class(path):
        created_count = 0
        updated_count = 0
        with open(path,'r') as f:
               data=json.load(f)
               funds_list = data["data"]["funds"]
        # for i in range(0,len(data["data"]["funds"])):
        for fund in funds_list:
                amcfund_code = fund["scheme"]
                amcfund = AMCFund.objects.get(rta_fund_code = amcfund_code)
                #amcfund=AMCFund.get_amc_fund(amcfund_code)
                schemes_list = fund["schemes"]
                for scheme in schemes_list:
                    scheme_payload={
                        "name":scheme["desc"],
                        "AMCFund": amcfund,
                        "rta_scheme_code": scheme['schemeid']
                    }
                    AMCFundScheme.update_or_create_from_schemes_payload(scheme_payload)
                    










# def logic_file(path):
#         created_count = 0
#         updated_count = 0
#         with open(path,'r') as f:
#                data=json.load(f)
#                funds_list = data["data"]["funds"]
#         # for i in range(0,len(data["data"]["funds"])):
#         for fund in funds_list:
#                 amcfund_code = fund["scheme"]
#                 amcfund = AMCFund.objects.get(rta_fund_code = amcfund_code)
#                 schemes_list = fund["schemes"]
#                 for scheme in schemes_list:
#                     scheme_payload={
#                         "name":scheme["desc"],
#                         "AMCFund": amcfund,
#                         "rta_scheme_code": scheme['schemeid']
#                     }
 
#                     obj, created = AMCFundScheme.objects.update_or_create(
#                                     name = scheme_payload['name'],
#                                     defaults=scheme_payload
#                                     )
#                     if created:
#                         created_count += 1
#                     else:
#                         updated_count += 1
 
#         return [created_count, updated_count]





