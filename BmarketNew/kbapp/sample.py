
import json
with open('/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/amcfundscheme.json','r') as f:
             data=json.load(f)
            #  print(data["statusCode"])
            #  print('-------------------')
            #  print(data["message"])
            #  print('---------------')
            #  print(data["data"]["fund"])
            #  print(data["data"]["fundname"])
            #  print(type(data["data"]["funds"]))
            #  c=0
             #for i in range(0,len(data["data"]["funds"])):
                 #  print(data["data"]["funds"][i]["scheme"])
                 #  print(data["data"]["funds"][i]["schdesc"])
                 #  print(data["data"]["funds"][i]["schemes"])
                #  print(data["data"]["funds"][i]["scheme"])
                #  print(data["data"]["funds"][i]["schdesc"])
                #  print(data["data"]["funds"][i]["category"])
                #  print(data["data"]["funds"][i]["subcategory"])
                #  print(data["data"]["funds"][i]["risktype"])

            #  print(data["data"]["funds"][1]["schemes"][1]['plandesc'])
            #  c+=1
            #  print(c)

            #  for i in range(0,len(data["data"]["funds"])):
            #      print(data["data"]["funds"][i]["schemes"][0]['plandesc'])

             for fund in data["data"]["funds"]:
                     print(fund["schdesc"])
            #     print('----------'*100)






"""
scheme_payload = {    # Scheme Name and amfi_scheme_code    "name": scheme['desc'],    "amfi_scheme_code": scheme['amficode'] if scheme['amficode'] else 0,    "is_active": True if scheme['active'] == "Y" else False,    # Scheme Plan type and Option type Fields. Do not change this logic.    "is_being_sold": True if scheme['purallow'] == "Y" else False,    "is_direct_fund": is_direct_fund,    "is_regular_fund": is_regular_fund,    "is_growth_fund": is_growth_fund,    "is_div_payout_fund": is_div_payout_fund,    "is_div_reinvestment_fund": is_div_reinvestment_fund,    "rta_scheme_planoptiondesc": planoptiondesc.get(True, ""),    "rta_scheme_option": scheme.get("optiondesc"),    # Scheme is allowed fields    "rta_sip_flag": scheme['sipallow'],    "rta_stp_flag": scheme['stpoallow'],    "rta_swp_flag": scheme['stpiallow'],    "rta_switch_flag": "Y" if scheme['swiallow'] == 'Y' and scheme['swoallow'] == 'Y' else "N",    "rta_stp_reg_in": scheme['stpiallow'],    "rta_stp_reg_out": scheme['stpoallow'],    "rta_swi_allowed": scheme['swiallow'],    "rta_swo_allowed": scheme['swoallow'],    # Kfin Scheme info Fields    "rta_scheme_code": scheme['schemeid'],    "rta_rta_scheme_code": scheme['schemeid'],    "rta_amc_scheme_code": scheme['schemeid'],    "rta_isin": scheme['isin'],    "rta_amc_code": scheme['fundname'],    "rta_scheme_type": fund_category,    "rta_scheme_plan": scheme['plandesc'],    "rta_scheme_name": scheme['desc'],    "rta_scheme_active_flag": scheme['active'],    "rta_lock_in_period_flag": "N",    "rta_lock_in_period": 0,    "rta_plan_code": scheme['plan'],    "rta_option_code": scheme['option'],    # Scheme NFO Fields    "is_nfo": scheme['nfoidentifier'],    "nfo_face_value": scheme['facevalue'],    "nfo_start_date": convert_date_format(scheme['opendate']),  # convert to datetime.date    "nfo_end_date": convert_date_format(scheme['closedate']),  # convert to datetime.date    "nfo_reopening_date": convert_date_format(scheme['reopendate']),  # convert to datetime.date    # Scheme Purchase Fields    "rta_purchase_allowed": scheme['purallow'],    "rta_minimum_purchase_amount": scheme['new_minamt'],    "rta_additional_purchase_amount_multiple": scheme['add_minamt'],    "rta_purchase_cutoff_time": get_cutoff_time(scheme['purcuttime']),  # Convert to datetime.time    # Scheme Redeem Fields    "rta_redemption_allowed": scheme['redallow'],    "rta_redemption_amount_minimum": scheme['red_minamt'],    "rta_redemption_cutoff_time": get_cutoff_time(scheme['redcuttime']),  # Convert to datetime.time    "modified_by": BATCH_USER,    "modified": datetime.datetime.now()}

"""


















# import json
# with open('/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/amcfundscheme.json','r') as f:
#             data=json.load(f)
#             print(data["statusCode"])
#             print('-------------------')
#             print(data["message"])
#             print('---------------')
#             print(data["data"]["fund"])
#             print(data["data"]["fundname"])
#             print(type(data["data"]["funds"]))
#             c=0
#             for i in range(0,len(data["data"]["funds"])):
#                 #  print(data["data"]["funds"][i]["scheme"])
#                 #  print(data["data"]["funds"][i]["schdesc"])
#                 #  print(data["data"]["funds"][i]["schemes"])
#                 print(data["data"]["funds"][i]["scheme"])
#                 print(data["data"]["funds"][i]["schdesc"])
#                 print(data["data"]["funds"][i]["category"])
#                 print(data["data"]["funds"][i]["subcategory"])
#                 print(data["data"]["funds"][i]["risktype"])
#                 c+=1
#             print(c)


# import requests

# url = "https://clientwebsitesuat3.kfintech.com/bajaj/api/v1/masterData/getSchemes"
# response = requests.get(url)

# if response.status_code == 200:
#     json_response = response.json()
#     print(json_response)
# else:
#     print("Error:", response.status_code)