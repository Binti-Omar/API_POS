import time
import math
import base64
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

consumer_key = "viIyvBpjwSWBxkshg0ze7CFxLyFU0wGnveseYeUHdiTsm2X2"
consumer_secret = "RJKWLU71hCjBzXbAfoitKTFLpYAT09yO2B9jFFMmuEO4SJ9tj4pXupxjloZg1Yyz" 
saf_short_code = "174379"
saf_stk_push_url="https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
saf_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
saf_passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
my_call_url = "https://shelter-verbose-compress.ngrok-free.dev"

# time will be sent to the stk push
# request is for sending http like axios
# math is for converting into an integer
# base64 is used for hashing for security
# httpbasicauth is for getting token for authentication

def get_mpesa_access_token():
    try:
        res = requests.get(
            saf_token_url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
        )
        token = res.json()['access_token']

    except Exception as e:
        print(str(e), "error getting access token")
        raise e

    return token

mytoken=get_mpesa_access_token()
print(mytoken)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

headers = {
            "Authorization": f"Bearer {mytoken}",
            "Content-Type": "application/json"
        }

def generate_password():
        password_str =saf_short_code + saf_passkey +timestamp
        password_bytes = password_str.encode()

        return base64.b64encode(password_bytes).decode("utf-8")

password = generate_password()
print(password)

def make_stk_push(payload):
        amount = payload['amount']
        phone_number = payload['phone_number']
        push_data = {
            "BusinessShortCode": saf_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(float(amount)),
            "PartyA": phone_number,
            "PartyB": saf_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": my_call_url,
            "AccountReference": "Whatever you call your app",
            "TransactionDesc": "description of the transaction",
        }

        response = requests.post(
            saf_token_url,
            json=push_data,
            headers=headers)

        response_data = response.json()

        return response_data

c = make_stk_push({"amount":"1","phone_number":"254717824020"})
print(c)