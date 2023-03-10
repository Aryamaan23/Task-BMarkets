from django.core.management.base import BaseCommand
from datetime import datetime
from kbapp.models import AMCFundScheme
import json

path='/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/amcfundscheme.json'

class Command(BaseCommand):
     help = 'Stores fund data in the amcfund model'

     def handle(self,*args,**options):
         logic_file(path)
         self.stdout.write("Successfully created bank records")




def logic_file(path):
     with open(path,'r') as f:
            data=json.load(f)
            for i in range(0,len(data["data"]["funds"])):
                scheme_payload = {
                        "name": data["data"]["funds"][i]["schemes"][0]['plandesc']
                }
                    #     "amfi_scheme_code": data["data"]["funds"]["schme['amficode'] if scheme['amficode'] else 0,
                    #     "is_active": True if scheme['active'] == "Y" else False,
                        
                    #     "is_being_sold": True if scheme['purallow'] == "Y" else False,
                    #     "is_direct_fund": is_direct_fund,
                    #     "is_regular_fund": is_regular_fund,
                    #     "is_growth_fund": is_growth_fund,
                    #     "is_div_payout_fund": is_div_payout_fund,
                    #     "is_div_reinvestment_fund": is_div_reinvestment_fund,
                    #     "rta_scheme_planoptiondesc": planoptiondesc.get(True, ""),
                    #     "rta_scheme_option": scheme.get("optiondesc"),
                        
                    #     "rta_sip_flag": scheme['sipallow'],
                    #     "rta_stp_flag": scheme['stpoallow'],
                    #     "rta_swp_flag": scheme['stpiallow'],
                    #     "rta_switch_flag": "Y" if scheme['swiallow'] == 'Y' and scheme['swoallow'] == 'Y' else "N",
                    #     "rta_stp_reg_in": scheme['stpiallow'],
                    #     "rta_stp_reg_out": scheme['stpoallow'],
                    #     "rta_swi_allowed": scheme['swiallow'],
                    #     "rta_swo_allowed": scheme['swoallow'],
                        
                    #     "rta_scheme_code": scheme['schemeid'],
                    #     "rta_rta_scheme_code": scheme['schemeid'],
                    #     "rta_amc_scheme_code": scheme['schemeid'],
                    #     "rta_isin": scheme['isin'],
                    #     "rta_amc_code": scheme['fundname'],
                    #     "rta_scheme_type": fund_category,
                    #     "rta_scheme_plan": scheme['plandesc'],
                    #     "rta_scheme_name": scheme['desc'],
                    #     "rta_scheme_active_flag": scheme['active'],
                    #     "rta_lock_in_period_flag": "N",
                    #     "rta_lock_in_period": 0,
                    #     "rta_plan_code": scheme['plan'],
                    #     "rta_option_code": scheme['option'],
                        
                    #     "is_nfo": scheme['nfoidentifier'],
                    #     "nfo_face_value": scheme['facevalue'],
                    #     "nfo_start_date": convert_date_format(scheme['opendate']),
                    #     "nfo_end_date": convert_date_format(scheme['closedate']),
                    #     "nfo_reopening_date": convert_date_format(scheme['reopendate']),
                        
                    #     "rta_purchase_allowed": scheme['purallow'],
                    #     "rta_minimum_purchase_amount": scheme['new_minamt'],
                    #     "rta_additional_purchase_amount_multiple": scheme['add_minamt'],
                    #     "rta_purchase_cutoff_time": get_cutoff_time(scheme['purcuttime']),
                        
                    #     "rta_redemption_allowed": scheme['redallow'],
                    #     "rta_redemption_amount_minimum": scheme['red_minamt'],
                    #     "rta_redemption_cutoff_time": get_cutoff_time(scheme['redcuttime']),
                        
                    #     "modified_by": BATCH_USER,
                    #     "modified": datetime.datetime.now()
                    # }

                 # Check if an object with the same rta_fund_code already exists
                obj, created = AMCFundScheme.objects.get_or_create(
                name=scheme_payload['name'],
                defaults=scheme_payload
                )
     