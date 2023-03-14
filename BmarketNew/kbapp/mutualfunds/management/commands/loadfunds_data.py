from django.core.management.base import BaseCommand
from datetime import datetime
from kbapp.models import AMCFundScheme,AMCFund
from kbapp.mutualfunds.utils import get_cutoff_time,get_response_from_api,get_status_flag,convert_date_format
from kbapp.mutualfunds.mappings import fund_mappings,scheme_mappings
import json
import datetime
import json
import requests


url = "https://clientwebsitesuat3.kfintech.com/bajaj/api/v1/masterData/getSchemes"



def logic_api_funds(fund):
    """
     In this logic, we are fetching the response from KFIN api. Then traversing through the funds list so 
     that we can save the data of each fund as per the payload mapping.
     """
    fund_payload=fund_mappings(fund)
    amc_fund=AMCFund.update_or_create_from_payload(fund_payload)
    flag_updated=True
    return amc_fund,flag_updated
     

def logic_api_schemes(schemes_list,amcfund,fund):
     for scheme in schemes_list:
                scheme_payload=scheme_mappings(scheme,amcfund,fund)
                AMCFundScheme.update_or_create_from_schemes_payload(scheme_payload)



def logic_api_fund_schemes(url : str):
        """
        In this logic, we are fetching the response from KFIN api. Then traversing through the schemes list which is inside
        the funds list in response. In that schemes we are trying to match the rta_fund_code with the scheme because it is a
        unique identifier in funds table so that we can save the schemes corresponding to the fund because they have a one to many relationship as per the payload mapping.
        """
        data = get_response_from_api(url)
        funds_list = data["data"]["funds"]
        for fund in funds_list:
                amcfund_code = fund["scheme"]
                amcfund,fund_status = logic_api_funds(fund)
                #amcfund = AMCFund.objects.get(rta_fund_code = amcfund_code)
                #amcfund=AMCFund.get_amc_fund(amcfund_code)
                if not fund_status:
                    continue
                schemes_list = fund["schemes"]
                logic_api_schemes(schemes_list,amcfund,fund)



class Command(BaseCommand):
     help = 'Stores fund and schemes data in the amcfund model'

     def handle(self,*args,**options):
         logic_api_fund_schemes(url)
         self.stdout.write("Successfully created bank records")































# from django.core.management.base import BaseCommand
# from datetime import datetime
# from kbapp.models import AMCFundScheme,AMCFund
# import json
# import datetime
# import json
# import requests
# from kbapp.mutualfunds.utils import get_cutoff_time,get_response_from_api,get_status_flag,convert_date_format
# from kbapp.mutualfunds.mappings import fund_mappings,scheme_mappings

# url = "https://clientwebsitesuat3.kfintech.com/bajaj/api/v1/masterData/getSchemes"

# def funds(fund):
#     """
#      In this logic, we are fetching the response from KFIN api. Then traversing through the funds list so 
#      that we can save the data of each fund as per the payload mapping.
#      """
#     fund_payload=fund_mappings(fund)
#     amc_fund=AMCFund.update_or_create_from_payload(fund_payload)
#     flag_updated=True
#     return amc_fund,flag_updated
     

# def schemes(schemes_list,amcfund,fund):
#                     scheme_payload=scheme_mappings(schemes_list,amcfund,fund)
#                     AMCFundScheme.update_or_create_from_schemes_payload(scheme_payload)


# def logic_api_fund_schemes(url : str):
#         """
#         In this logic, we are fetching the response from KFIN api. Then traversing through the schemes list which is inside
#         the funds list in response. In that schemes we are trying to match the rta_fund_code with the scheme because it is a
#         unique identifier in funds table so that we can save the schemes corresponding to the fund because they have a one to many relationship as per the payload mapping.
#         """
#         data = get_response_from_api(url)
#         funds_list = data["data"]["funds"]
#         for fund in funds_list:
#                 amcfund_code = fund["scheme"]
#                 amcfund,fund_status = funds(fund)
#                 if not fund_status:
#                      continue
#                 schemes_list = fund["schemes"]
#                 schemes(schemes_list,amcfund,fund)
                


# class Command(BaseCommand):
#      help = 'Stores fund and schemes data in the amcfund model'

#      def handle(self,*args,**options):
#          logic_api_fund_schemes(url)
#          self.stdout.write("Successfully created bank records")







