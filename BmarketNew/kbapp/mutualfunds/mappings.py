from kbapp.mutualfunds.utils import get_cutoff_time,get_response_from_api,get_status_flag,convert_date_format
import datetime
def fund_mappings(fund):
    fund_payload={
                "fund_type":fund['category'],
                "fund_sub_type":fund['subcategory'],
                "risk_factor":fund['risktype'],
                "rta_fund_code":fund['scheme'],
                "fund_category":fund['category'],
                "modified_by":"Aryamaan",
                "modified":datetime.datetime.now()
            } 
    return fund_payload


def scheme_mappings(scheme,amcfund,fund):
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
                        "rta_scheme_type": fund["category"],
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
                    return scheme_payload