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


import requests

url = "https://clientwebsitesuat3.kfintech.com/bajaj/api/v1/masterData/getSchemes"
response = requests.get(url)

if response.status_code == 200:
    json_response = response.json()
    print(json_response)
else:
    print("Error:", response.status_code)