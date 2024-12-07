# automation/mpesa_utils.py
import base64
import requests
from django.conf import settings


# 1. Function to get the access token
def get_mpesa_access_token():
    """
    Get the OAuth token to authenticate requests to the M-Pesa API.
    """
    url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    credentials = f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}"
    headers = {
        'Authorization': f'Basic {base64.b64encode(credentials.encode()).decode()}',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None


# 2. Function to initiate an STK push
def initiate_stk_push(phone_number, amount, account_reference, transaction_desc, callback_url):
    """
    Initiate an STK Push to prompt the user to pay via M-Pesa.
    """
    access_token = get_mpesa_access_token()
    if not access_token:
        return None

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

    payload = {
        "BusinessShortcode": settings.MPESA_SHORTCODE,
        "LipaNaMpesaOnlineShortcode": settings.MPESA_SHORTCODE,
        "LipaNaMpesaOnlineShortcodeType": settings.MPESA_SHORTCODE_TYPE,
        "Amount": amount,
        "PartyA": phone_number,  # User's phone number
        "PartyB": settings.MPESA_SHORTCODE,  # Your shortcode
        "PhoneNumber": phone_number,  # User's phone number
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc,
        "Passkey": settings.MPESA_PASSKEY,
        "CallbackURL": callback_url,
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None
