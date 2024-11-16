from flask import Flask, redirect, request, render_template, Blueprint
import uuid
import json
import base64
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

payments = Blueprint("payments", __name__)

def calculate_sha256_string(input_string):
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    sha256.update(input_string.encode('utf-8'))
    return sha256.finalize().hex()

def base64_encode(input_dict):
    json_data = json.dumps(input_dict)
    data_bytes = json_data.encode('utf-8')
    return base64.b64encode(data_bytes).decode('utf-8')

@payments.route("/pay", methods=['GET'])
def pay():
    MAINPAYLOAD = {
        "merchantId": "M226I0MHQCBFO",
        "merchantTransactionId": str(uuid.uuid4()),  # Ensure UUID is a string
        "merchantUserId": "MUID123",
        "amount": 1000,
        "redirectUrl": "https://oxyher.com/payments/status",
        "redirectMode": "POST",
        "callbackUrl": "https://oxyher.com/payments/status",
        "mobileNumber": "9999999999",
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }
    
    INDEX = "1"
    ENDPOINT = "/pg/v1/pay"
    SALTKEY = "742a5cdb-62f9-4ba3-af92-05fbae758cc8"
    base64String = base64_encode(MAINPAYLOAD)
    mainString = base64String + ENDPOINT + SALTKEY
    sha256Val = calculate_sha256_string(mainString)
    checkSum = sha256Val + '###' + INDEX
    
    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': checkSum,
        'accept': 'application/json',
    }
    json_data = {'request': base64String}
    
    try:
        response = requests.post('https://api.phonepe.com/apis/hermes/pg/v1/pay', headers=headers, json=json_data)
        response.raise_for_status()
        responseData = response.json()
        # Redirect to payment URL if success
        
        return redirect(responseData['data']['instrumentResponse']['redirectInfo']['url'])
    except requests.exceptions.RequestException as e:
        return f"Payment initiation failed: {e}", 500

@payments.route("/status", methods=['GET', 'POST'])
def payment_return():
    INDEX = "1"
    SALTKEY = "742a5cdb-62f9-4ba3-af92-05fbae758cc8"
    form_data = request.form
    form_data_dict = dict(form_data)

    if request.form.get('transactionId'):
        transaction_id = request.form.get('transactionId')
        request_url = f'https://api.phonepe.com/apis/hermes/pg/v1/status/M226I0MHQCBFO/{transaction_id}'
        sha256_Pay_load_String = f'/pg/v1/status/M226I0MHQCBFO/{transaction_id}{SALTKEY}'
        sha256_val = calculate_sha256_string(sha256_Pay_load_String)
        checksum = sha256_val + '###' + INDEX

        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checksum,
            'X-MERCHANT-ID': "M226I0MHQCBFO",  # Ensure correct Merchant ID
            'accept': 'application/json',
        }

        try:
            response = requests.get(request_url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            response_data = f"Status check failed: {e}"
            return response_data

    return render_template('themes/customer/payment/status.html', page_respond_data=form_data_dict, page_respond_data_varify=response_data)
