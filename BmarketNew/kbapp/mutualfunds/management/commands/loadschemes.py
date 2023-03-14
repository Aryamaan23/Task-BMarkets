from django.core.management.base import BaseCommand
from datetime import datetime
from kbapp.models import AMCFundScheme,AMCFund
import json
import datetime

path='/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/amcfundscheme.json'



"""
The function first checks whether the input param is an integer or not using the isinstance function. If param is not an integer, the function returns an empty string.If param is an integer, the function converts it to a string and checks if the length of the string is 4. If the length is 4, the function extracts the first two characters as the hour and the last two characters as the minute of the cutoff time. It then creates a datetime.time object with these values and returns it.
If the length of the string is not 4, the function returns an empty string
"""

def get_cutoff_time(param: int):
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


"""
This Python function converts a date string in ISO format to a date object in UTC timezone.
"""
def convert_date_format(param_date: str):
    return datetime.datetime.fromisoformat(param_date[:-1] + '+00:00').date()



"""
This Python function checks if a given string "param1" is contained within another string "param2" (ignoring case sensitivity) and returns a boolean value indicating the result.
If "param1" is found in "param2", the function returns True. Otherwise, it returns False.
"""
def get_status_flag(param1, param2):
    return True if param1 in param2.lower() else False



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




