from django.core.management.base import BaseCommand
from datetime import datetime
from kbapp.models import AMCFund
import json
import requests

path='/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/amcfundscheme.json'
url = "https://clientwebsitesuat3.kfintech.com/bajaj/api/v1/masterData/getSchemes"

class Command(BaseCommand):
     help = 'Stores fund data in the amcfund model'

     def handle(self,*args,**options):
         logic_api(url)
         self.stdout.write("Successfully created bank records")


def logic_file(path):
         with open(path,'r') as f:
            data=json.load(f)
            for i in range(0,len(data["data"]["funds"])):
                fund_payload={
                    "fund_type":data["data"]["funds"][i]['category'],
                    "fund_sub_type":data["data"]["funds"][i]['subcategory'],
                    "risk_factor":data["data"]["funds"][i]['risktype'],
                    "rta_fund_code":data["data"]["funds"][i]['scheme'],
                    "fund_category":data["data"]["funds"][i]['category'],
                    "modified_by":"Aryamaan",
                    "modified":datetime.now()
                } 
                 # Check if an object with the same rta_fund_code already exists
                obj, created = AMCFund.objects.get_or_create(
                rta_fund_code=fund_payload['rta_fund_code'],
                defaults=fund_payload
                )

                # If the object already exists, update it with the new values
                if not created:
                    obj.fund_type = fund_payload['fund_type']
                    obj.fund_sub_type = fund_payload['fund_sub_type']
                    obj.risk_factor = fund_payload['risk_factor']
                    obj.fund_category = fund_payload['fund_category']
                    obj.modified_by = fund_payload['modified_by']
                    obj.modified = fund_payload['modified']
                    obj.save()


                # # If an object was created, print a message
                # if created:
                #     print(f"Created new AMCFund object with rta_fund_code: {obj.rta_fund_code}")
         

def logic_api(url):
            data=get_response_from_api(url)
            for i in range(0,len(data["data"]["funds"])):
                fund_payload={
                    "fund_type":data["data"]["funds"][i]['category'],
                    "fund_sub_type":data["data"]["funds"][i]['subcategory'],
                    "risk_factor":data["data"]["funds"][i]['risktype'],
                    "rta_fund_code":data["data"]["funds"][i]['scheme'],
                    "fund_category":data["data"]["funds"][i]['category'],
                    "modified_by":"Aryamaan",
                    "modified":datetime.now()
                } 
                 # Check if an object with the same rta_fund_code already exists
                obj, created = AMCFund.objects.get_or_create(
                rta_fund_code=fund_payload['rta_fund_code'],
                defaults=fund_payload
                )

                 # If the object already exists, update it with the new values
                if not created:
                    obj.fund_type = fund_payload['fund_type']
                    obj.fund_sub_type = fund_payload['fund_sub_type']
                    obj.risk_factor = fund_payload['risk_factor']
                    obj.fund_category = fund_payload['fund_category']
                    obj.modified_by = fund_payload['modified_by']
                    obj.modified = fund_payload['modified']
                    obj.save()


def get_response_from_api(url):
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        #print(json_response)
        return json_response
    else:
        return response.status_code
















#  def handle(self,*args,**options):
    #     with open('/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/amcfundscheme.json','r') as f:
    #         data=json.load(f)
    #        #print(data["data"]["funds"]["category"])
    #        #amc = AMCFund.objects.get(pk=)
    #         for i in range(0,len(data["data"]["funds"])):
    #             #for payload_param in data["data"]["funds"][i]:
    #             fund_payload={
    #                 "fund_type":data["data"]["funds"][i]['category'],
    #                 "fund_sub_type":data["data"]["funds"][i]['subcategory'],
    #                 "risk_factor":data["data"]["funds"][i]['risktype'],
    #                 "rta_fund_code":data["data"]["funds"][i]['scheme'],
    #                 "fund_category":data["data"]["funds"][i]['category'],
    #                 "modified_by":"Aryamaan",
    #                 "modified":datetime.now()
    #             } 
    #              # Check if an object with the same rta_fund_code already exists
    #             obj, created = AMCFund.objects.get_or_create(
    #             rta_fund_code=fund_payload['rta_fund_code'],
    #             defaults=fund_payload
    #             )

    #             # If an object was created, print a message
    #             if created:
    #                 print(f"Created new AMCFund object with rta_fund_code: {obj.rta_fund_code}")





"""
import json
with open('/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/amcfundscheme.json','r') as f:
            data=json.load(f)
            print(data["statusCode"])
            print('-------------------')
            print(data["message"])
            print('---------------')
            print(data["data"]["fund"])
            print(data["data"]["fundname"])
            print(type(data["data"]["funds"]))
            for i in range(0,len(data["data"]["funds"])):
                #  print(data["data"]["funds"][i]["scheme"])
                #  print(data["data"]["funds"][i]["schdesc"])
                #  print(data["data"]["funds"][i]["schemes"])
                print(data["data"]["funds"][i]["scheme"])
                print(data["data"]["funds"][i]["schdesc"])
                print(data["data"]["funds"][i]["category"])
                print(data["data"]["funds"][i]["subcategory"])
                print(data["data"]["funds"][i]["risktype"])


"""