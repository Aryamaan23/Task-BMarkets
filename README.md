# Task-BMarkets

## Bank-APIs-Documentation and Usecases

## Authorization

For authentication, we are using Django-based token authentication so that only the user with Auth-Token can access the APIs

## Requests

| Parameter | Type 
| :--- | :--- |
| `account_details` | `json` | 

#### Request Body
```json
{
"account_number": "000018",
    "ifsc_code": "34343",
    "cheque_image": null,
    "branch_name": "xyz",
    "is_cheque_verified": true,
    "name_as_per_bank_record": "Aryamaan",
    "verification_mode": "EKYC",
    "account_type": "savings",
    "balance": "42342.00",
    "bank":1
}
```

#### Response

Many API endpoints return the JSON representation of the resources created or edited. BankAPis returns a JSON response in the following format:

```json
{
        "id": 33,
        "account_number": "8989898998",
        "ifsc_code": "242342342342",
        "cheque_image": null,
        "branch_name": "xyz",
        "is_cheque_verified": true,
        "name_as_per_bank_record": "Aryamaan",
        "verification_mode": "EKYC",
        "account_type": "savings",
        "balance": "42342.00",
        "customer": 3,
        "bank": 1,
        "bank_logo": "http://127.0.0.1:8000/download.png",
        "bank_name": "HDFC"
    }
```


## Status Codes

The following status codes in this API has been incorporated:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `BAD REQUEST` |
| 422 | `VALIDATION ERROR` |
