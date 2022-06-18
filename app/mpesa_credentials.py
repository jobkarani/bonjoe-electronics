from decouple import config, Csv
import requests
from requests.auth import HTTPBasicAuth
import json
import base64
from datetime import datetime



# get mpesa access token
class MpesaAccessToken:
    consumer_key = config("CONSUMER_KEY")
    consumer_secret = config("CONSUMER_SECRET")
    api_url = config("GET_ACCESS_TOKEN_URL")

    the_request = requests.get(
        api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret)
    )
    mpesa_access_token = json.loads(the_request.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

print('the_request.text')


# LIPA NA M-PESA ONLINE
class LipaNaMpesaPassword:
    payment_time = datetime.now().strftime("%Y%m%d%H%M%S")
    
    BusinessShortCode = config("BusinessShortCode")
    BusinessShortCodeForCToB = config('BusinessShortCodeForCToB')
    
    passkey = config('PASSKEY')

    data_to_encode = BusinessShortCode + passkey + payment_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')