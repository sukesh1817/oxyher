from flask import Blueprint, render_template, request, session, abort
from ..models.auth import is_cookie_exists
from cryptography.hazmat.backends import default_backend
from ..models.shop import get_random_products


home = Blueprint("home", __name__)

@home.route("/")
def index():
    data = request.args.get('login')
    # Get random products for section_1 and section_2
    sec_1 = get_random_products()
    sec_2 = get_random_products()        
    return render_template("themes/customer/home.html", login=data,sec_1=sec_1,sec_2=sec_2)
    
@home.before_request
def check_session_and_cookie():    
    
    if 'sess_id' in request.cookies:
        if 'auth_key' not in session:
            cookie_id = request.cookies['sess_id']
            result = is_cookie_exists(cookie_id)

            
@home.route("/contact-us")
def contact_us():
    return render_template("themes/customer/contact.html")
    # return session.get("auth_key")


# def calculate_sha256_string(input_string):
#     sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
#     sha256.update(input_string.encode('utf-8'))
#     return sha256.finalize().hex()

# def base64_encode(input_dict):
#     json_data = json.dumps(input_dict)
#     data_bytes = json_data.encode('utf-8')
#     return base64.b64encode(data_bytes).decode('utf-8')

# @home.route("/")
# def index():
#     MAINPAYLOAD = {
#         "merchantId": "M226I0MHQCBFO",
#         "merchantTransactionId": str(uuid.uuid4()),  # Ensure UUID is a string
#         "merchantUserId": "MUID123",
#         "amount": 1000,
#         "redirectUrl": "https://oxyher.com",
#         "redirectMode": "POST",
#         "callbackUrl": "https://oxyher.com",
#         "mobileNumber": "9999999999",
#         "paymentInstrument": {
#             "type": "PAY_PAGE"
#         }
#     }
    
#     INDEX = "1"
#     ENDPOINT = "/pg/v1/pay"
#     SALTKEY = "742a5cdb-62f9-4ba3-af92-05fbae758cc8"
#     base64String = base64_encode(MAINPAYLOAD)
#     mainString = base64String + ENDPOINT + SALTKEY
#     sha256Val = calculate_sha256_string(mainString)
#     checkSum = sha256Val + '###' + INDEX
    
#     headers = {
#         'Content-Type': 'application/json',
#         'X-VERIFY': checkSum,
#         'accept': 'application/json',
#     }
#     json_data = {'request': base64String}
    
#     try:
#         response = requests.post('https://api.phonepe.com/apis/hermes/pg/v1/pay', headers=headers, json=json_data)
#         response.raise_for_status()
#         responseData = response.json()
#         # Redirect to payment URL if success
        
#         return redirect(responseData['data']['instrumentResponse']['redirectInfo']['url'])
#     except requests.exceptions.RequestException as e:
#         return f"Payment initiation failed: {e}", 500
        
