from django.core.management.base import BaseCommand
from datetime import datetime
from kbapp.models import AMCFundScheme,AMCFund
import json
import datetime
import json
import requests


url = "https://clientwebsitesuat3.kfintech.com/bajaj/api/v1/masterData/getSchemes"


def get_cutoff_time(param: int):
    """
    If the length is 4, the function extracts the first two characters as the hour
    and the last two characters as the minute of the cutoff time. 
    It then creates a datetime.time object with these values and returns it.
    If the length of the string is not 4, the function returns an empty string
    """
    if isinstance(param, int):
        str_time = str(param)
        if len(str_time) == 4:
            cutoff_time_hour = int(str_time[:2])
            cutoff_time_min = int(str_time[2:])
            cut_off_time = datetime.time(cutoff_time_hour, cutoff_time_min)
        else:
            cut_off_time = ''
    else:
        cut_off_time = ''
    return cut_off_time


def convert_date_format(param_date: str):
    """
    This Python function converts a date string in ISO format to a date object in UTC timezone.
    """
    return datetime.datetime.fromisoformat(param_date[:-1] + '+00:00').date()


def get_status_flag(param1, param2):
    """
    If "param1" is found in "param2", the function returns True. Otherwise, it returns False.
    """
    return True if param1 in param2.lower() else False



def get_response_from_api(url : str):
    """
    This method is to fetch the response from KFin API using GET method
    """
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        #print(json_response)
        return json_response
    else:
        return response.status_code

def logic_api_funds(url : str):
     data = get_response_from_api(url)
     for fund in data["data"]["funds"]:
            fund_payload={
                "fund_type":fund['category'],
                "fund_sub_type":fund['subcategory'],
                "risk_factor":fund['risktype'],
                "rta_fund_code":fund['scheme'],
                "fund_category":fund['category'],
                "modified_by":"Aryamaan",
                "modified":datetime.datetime.now()
            } 
            AMCFund.update_or_create_from_payload(fund_payload)



def logic_api_schemes(url : str):
        created_count = 0
        updated_count = 0
        data = get_response_from_api(url)
        funds_list = data["data"]["funds"]
        # for i in range(0,len(data["data"]["funds"])):
        for fund in funds_list:
                amcfund_code = fund["scheme"]
                amcfund = AMCFund.objects.get(rta_fund_code = amcfund_code)
                #amcfund=AMCFund.get_amc_fund(amcfund_code)
                schemes_list = fund["schemes"]
                for scheme in schemes_list:
                    is_direct_fund = get_status_flag('direct', scheme['plandesc'])
                    is_regular_fund = get_status_flag('regular', scheme['plandesc'])
                    is_growth_fund = get_status_flag('growth', scheme['optiondesc'])
                    is_div_payout_fund = get_status_flag('payout', scheme['optiondesc'])
                    is_div_reinvestment_fund = get_status_flag('reinvestment', scheme['optiondesc'])
    
                    planoptiondesc = {is_direct_fund and is_growth_fund: "Direct - Growth",
                      is_regular_fund and is_growth_fund: "Regular - Growth",
                      is_direct_fund and is_div_reinvestment_fund: "Direct – IDCW Reinvestment",
                      is_regular_fund and is_div_reinvestment_fund: "Regular – IDCW Reinvestment",
                      is_direct_fund and is_div_payout_fund: "Direct – IDCW Payout",
                      is_regular_fund and is_div_payout_fund: "Regular – IDCW Payout"}
                    scheme_payload={
                        "name":scheme["desc"],
                        "AMCFund": amcfund,
                        "rta_scheme_code": scheme['schemeid'],
                        "amfi_scheme_code": scheme['amficode'] if scheme['amficode'] else 0,
                        "is_active": True if scheme['active'] == "Y" else False,
                        # Scheme Plan type and Option type Fields. Do not change this logic.
                        "is_being_sold": True if scheme['purallow'] == "Y" else False,
                        "is_direct_fund": is_direct_fund,
                        "is_regular_fund": is_regular_fund,
                        "is_growth_fund": is_growth_fund,
                        "is_div_payout_fund": is_div_payout_fund,
                        "is_div_reinvestment_fund": is_div_reinvestment_fund,
                        "rta_scheme_planoptiondesc": planoptiondesc.get(True, ""),
                        "rta_scheme_option": scheme.get("optiondesc"),
                        # Scheme is allowed fields
                        "rta_sip_flag": scheme['sipallow'],
                        "rta_stp_flag": scheme['stpoallow'],
                        "rta_swp_flag": scheme['stpiallow'],
                        "rta_switch_flag": "Y" if scheme['swiallow'] == 'Y' and scheme['swoallow'] == 'Y' else "N",
                        # Kfin Scheme info Fields
                        "rta_scheme_code": scheme['schemeid'],
                        "rta_rta_scheme_code": scheme['schemeid'],
                        "rta_amc_scheme_code": scheme['schemeid'],
                        "rta_isin": scheme['isin'],
                        "rta_amc_code": scheme['fundname'],
                        "rta_scheme_type": amcfund.fund_category,
                        "rta_scheme_plan": scheme['plandesc'],
                        "rta_scheme_name": scheme['desc'],
                        "rta_scheme_active_flag": scheme['active'],
                        "rta_lock_in_period_flag": "N",
                        "rta_lock_in_period": 0,
                        "rta_plan_code": scheme['plan'],
                        "rta_option_code": scheme['option'],
                        # Scheme NFO Fields
                        "is_nfo": scheme['nfoidentifier'],
                        "nfo_face_value": scheme['facevalue'],
                        "nfo_start_date": convert_date_format(scheme['opendate']),  # convert to datetime.date
                        "nfo_end_date": convert_date_format(scheme['closedate']),  # convert to datetime.date
                        "nfo_reopening_date": convert_date_format(scheme['reopendate']),  # convert to datetime.date

                        # Scheme Purchase Fields
                        "rta_purchase_allowed": scheme['purallow'],
                        "rta_minimum_purchase_amount": scheme['new_minamt'],
                        "rta_additional_purchase_amount_multiple": scheme['add_minamt'],
                        "rta_purchase_cutoff_time": get_cutoff_time(scheme['purcuttime']),  # Convert to datetime.time

                        # Scheme Redeem Fields
                        "rta_redemption_allowed": scheme['redallow'],
                        "rta_redemption_amount_minimum": scheme['red_minamt'],
                        "rta_redemption_cutoff_time": get_cutoff_time(scheme['redcuttime']),  # Convert to datetime.time
                        "modified_by": "Aryamaan Pandey",
                        "modified": datetime.datetime.now()
                    }
                    AMCFundScheme.update_or_create_from_schemes_payload(scheme_payload)




class Command(BaseCommand):
     help = 'Stores fund and schemes data in the amcfund model'

     def handle(self,*args,**options):
         logic_api_funds(url)
         logic_api_schemes(url)
         self.stdout.write("Successfully created bank records")






"""
Logic for inserting funds data through json file
"""
#path='/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/amcfundscheme.json'
# def logic_file(path : str):
#          with open(path,'r') as f:
#             data=json.load(f)
#             for i in range(0,len(data["data"]["funds"])):
#                 fund_payload={
#                     "fund_type":data["data"]["funds"][i]['category'],
#                     "fund_sub_type":data["data"]["funds"][i]['subcategory'],
#                     "risk_factor":data["data"]["funds"][i]['risktype'],
#                     "rta_fund_code":data["data"]["funds"][i]['scheme'],
#                     "fund_category":data["data"]["funds"][i]['category'],
#                     "modified_by":"Aryamaan",
#                     "modified":datetime.datetime.now()
#                 } 
#                  # Check if an object with the same rta_fund_code already exists
#                 obj, created = AMCFund.objects.get_or_create(
#                 rta_fund_code=fund_payload['rta_fund_code'],
#                 defaults=fund_payload
#                 )

#                 # If the object already exists, update it with the new values
#                 if not created:
#                     obj.fund_type = fund_payload['fund_type']
#                     obj.fund_sub_type = fund_payload['fund_sub_type']
#                     obj.risk_factor = fund_payload['risk_factor']
#                     obj.fund_category = fund_payload['fund_category']
#                     obj.modified_by = fund_payload['modified_by']
#                     obj.modified = fund_payload['modified']
#                     obj.save()



"""
Logic for inserting schemes data through json file
"""
#path='/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/amcfundscheme.json'
# def logic_file_class_schemes(path : str):
#         created_count = 0
#         updated_count = 0
#         with open(path,'r') as f:
#                data=json.load(f)
#                funds_list = data["data"]["funds"]
#         # for i in range(0,len(data["data"]["funds"])):
#         for fund in funds_list:
#                 amcfund_code = fund["scheme"]
#                 amcfund = AMCFund.objects.get(rta_fund_code = amcfund_code)
#                 #amcfund=AMCFund.get_amc_fund(amcfund_code)
#                 schemes_list = fund["schemes"]
#                 for scheme in schemes_list:
#                     is_direct_fund = get_status_flag('direct', scheme['plandesc'])
#                     is_regular_fund = get_status_flag('regular', scheme['plandesc'])
#                     is_growth_fund = get_status_flag('growth', scheme['optiondesc'])
#                     is_div_payout_fund = get_status_flag('payout', scheme['optiondesc'])
#                     is_div_reinvestment_fund = get_status_flag('reinvestment', scheme['optiondesc'])
    
#                     planoptiondesc = {is_direct_fund and is_growth_fund: "Direct - Growth",
#                       is_regular_fund and is_growth_fund: "Regular - Growth",
#                       is_direct_fund and is_div_reinvestment_fund: "Direct – IDCW Reinvestment",
#                       is_regular_fund and is_div_reinvestment_fund: "Regular – IDCW Reinvestment",
#                       is_direct_fund and is_div_payout_fund: "Direct – IDCW Payout",
#                       is_regular_fund and is_div_payout_fund: "Regular – IDCW Payout"}
#                     scheme_payload={
#                         "name":scheme["desc"],
#                         "AMCFund": amcfund,
#                         "rta_scheme_code": scheme['schemeid'],
#                         "amfi_scheme_code": scheme['amficode'] if scheme['amficode'] else 0,
#                         "is_active": True if scheme['active'] == "Y" else False,
#                         # Scheme Plan type and Option type Fields. Do not change this logic.
#                         "is_being_sold": True if scheme['purallow'] == "Y" else False,
#                         "is_direct_fund": is_direct_fund,
#                         "is_regular_fund": is_regular_fund,
#                         "is_growth_fund": is_growth_fund,
#                         "is_div_payout_fund": is_div_payout_fund,
#                         "is_div_reinvestment_fund": is_div_reinvestment_fund,
#                         "rta_scheme_planoptiondesc": planoptiondesc.get(True, ""),
#                         "rta_scheme_option": scheme.get("optiondesc"),
#                         # Scheme is allowed fields
#                         "rta_sip_flag": scheme['sipallow'],
#                         "rta_stp_flag": scheme['stpoallow'],
#                         "rta_swp_flag": scheme['stpiallow'],
#                         "rta_switch_flag": "Y" if scheme['swiallow'] == 'Y' and scheme['swoallow'] == 'Y' else "N",
#                         # Kfin Scheme info Fields
#                         "rta_scheme_code": scheme['schemeid'],
#                         "rta_rta_scheme_code": scheme['schemeid'],
#                         "rta_amc_scheme_code": scheme['schemeid'],
#                         "rta_isin": scheme['isin'],
#                         "rta_amc_code": scheme['fundname'],
#                         "rta_scheme_type": amcfund.fund_category,
#                         "rta_scheme_plan": scheme['plandesc'],
#                         "rta_scheme_name": scheme['desc'],
#                         "rta_scheme_active_flag": scheme['active'],
#                         "rta_lock_in_period_flag": "N",
#                         "rta_lock_in_period": 0,
#                         "rta_plan_code": scheme['plan'],
#                         "rta_option_code": scheme['option'],
#                         # Scheme NFO Fields
#                         "is_nfo": scheme['nfoidentifier'],
#                         "nfo_face_value": scheme['facevalue'],
#                         "nfo_start_date": convert_date_format(scheme['opendate']),  # convert to datetime.date
#                         "nfo_end_date": convert_date_format(scheme['closedate']),  # convert to datetime.date
#                         "nfo_reopening_date": convert_date_format(scheme['reopendate']),  # convert to datetime.date

#                         # Scheme Purchase Fields
#                         "rta_purchase_allowed": scheme['purallow'],
#                         "rta_minimum_purchase_amount": scheme['new_minamt'],
#                         "rta_additional_purchase_amount_multiple": scheme['add_minamt'],
#                         "rta_purchase_cutoff_time": get_cutoff_time(scheme['purcuttime']),  # Convert to datetime.time

#                         # Scheme Redeem Fields
#                         "rta_redemption_allowed": scheme['redallow'],
#                         "rta_redemption_amount_minimum": scheme['red_minamt'],
#                         "rta_redemption_cutoff_time": get_cutoff_time(scheme['redcuttime']),  # Convert to datetime.time
#                         "modified_by": "Aryamaan Pandey",
#                         "modified": datetime.datetime.now()
#                     }
#                     AMCFundScheme.update_or_create_from_schemes_payload(scheme_payload)





