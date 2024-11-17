from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    current_app,
    request,
    jsonify
)
from ..models.shop import (
    add_cart,
    get_products,
    get_my_cart,
    get_user_details,
    get_user_addr,
    get_my_final_items,
    get_item_suggestion,
    make_new_order,
    get_encrypted_dbs,
    get_decrypted_dbs
)
from modules.is_valid import is_login
import datetime, jwt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import os, requests

shop = Blueprint("shop", __name__)


""" LOGIN CHECK """


""" GET """


@shop.route("")
def home():
    search_query = request.args.get('q', '')  # Product search query
    category = request.args.get('c_', False)
    # enc_database = get_encrypted_dbs()
    if category:
        decrypted_category = get_decrypted_dbs(category)
        print(decrypted_category)
        products = get_products("CATEGORY",category=decrypted_category)

    else:
        products = get_products("ALL")
        
    try :
        for temp in products:
            if temp['product_id']:
                return render_template("themes/customer/shop/shop.html", products=products, error=0)
            else:
                return render_template("themes/customer/shop/shop.html", error=1,products=0)
    except Exception as e:
        return render_template("themes/customer/shop/shop.html", error=1,products=0)
                
    
        


    """ TODO: Pagination """
    # page = int(request.args.get('page', 1))  # Current page
    # per_page = int(request.args.get('per_page', PER_PAGE))  # Items per page
    # # Filter based on the search query (modify as needed)
    # filter_criteria = {"title": {"$regex": search_query, "$options": "i"}}
    # # Calculate the total count and pages
    # total_count = products_collection.count_documents(filter_criteria)
    # total_pages = (total_count + per_page - 1) // per_page
    # # Find products with skip and limit for pagination
    # products = list(products_collection.find(filter_criteria)
    #                 .skip((page - 1) * per_page)
    #                 .limit(per_page))
    # return render_template('search.html',
    #                        products=products,
    #                        page=page,
    #                        per_page=per_page,
    #                        total_pages=total_pages,
    #                        search_query=search_query)
    # page = int(request.args.get('page', 1)) 
    

@shop.route("/cart", methods=["GET"])
@is_login.login_required
def cart():
    img_url = current_app.config["IMG_URL"]
    cart = get_my_cart(session["auth_key"])
    products = get_products("CART", None, cart)
    return render_template(
        "themes/customer/shop/cart.html", products=products, img_url=img_url
    )
    # return "sample"


@shop.route("/p/<p_id>")
def show_individual_product(p_id):
    try:
        product_details = get_products("SINGLE", p_id)
        recommend_products = get_products("RECCOMEND", p_id)
        return render_template(
            "themes/customer/shop/detail.html",
            product=product_details,
            recommend_products=recommend_products,
        )
    except Exception as e:
        return redirect(url_for("shop.home"))


@shop.route("/shipping")
@is_login.login_required
def shipping():
    user_addr = get_user_addr(session["auth_key"])[0]
    user_data = get_user_details(session["auth_key"])
    user_items = get_my_final_items(session["auth_key"])
    if is_valid_pincode(user_data[5]): # check the pincode is valid for delivery
        return render_template(
            "themes/customer/shop/checkout.html",
            user_addr=user_addr,
            user_data=user_data,
            products=user_items,
            pincode_error=0
            
        )
    else :
        return render_template(
            "themes/customer/shop/checkout.html",
            user_addr=user_addr,
            user_data=user_data,
            products=user_items,
            pincode_error=1
        )
        



@shop.route("/shipping/confirm")
def redirect_to_payment():
    # Load the private key
    user_data = get_user_details(session["auth_key"])
    user_items = get_my_final_items(session["auth_key"])
    mobile_number = user_data[3]
    amount = 0
    for item in user_items:
        amount += item["final_price"]

    with open("/var/www/oxyher/sec_keys/private_key.pem", "r") as key_file:
        private_key = key_file.read()

    # URL for the PHP subdomain
    php_subdomain_url = "https://payments.oxyher.com/v1/pay/"

    # Prepare the payload with an expiry time (e.g., 5 minutes from now)
    payload = {
        "origin": "https://oxyher.com",
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(seconds=300),  # Expiration time
        "mob_num": mobile_number,
        "amt": amount,
        "kid": "my-key-id",  # Adding a Key ID (kid)
    }

    # Sign the payload with the private key using RS256 algorithm
    signature = jwt.encode(payload, private_key, algorithm="RS256")

    # Add the signature as a query parameter in the redirect URL
    redirect_url = f"{php_subdomain_url}?_sign={signature}"

    return redirect(redirect_url)


@shop.route("/payment")
@is_login.login_required
def payment():
    return render_template("themes/customer/shop/payment.html")


@shop.route("/review")
@is_login.login_required
def review():
    return render_template("themes/customer/shop/review.html")


@shop.route("/order/make", methods=["GET"])
def make_order():
    # Load the public key
    with open("/var/www/oxyher/sec_keys/public_key.pem", "r") as key_file:
        public_key = key_file.read()

    # Get the JWT signature from the query parameter
    signature = request.args.get("_sign")

    if signature:
        try:
            # Decode and verify the JWT using the public key and the RS256 algorithm
            decoded = jwt.decode(signature, public_key, algorithms=["RS256"], options={"verify_exp": True})

            # Check if the token has already been used
            if session.get('used_token') == signature:
                return "This token has already been used."

            # Check the origin and other claims
            if decoded.get("origin") == "https://payments.oxyher.com":
                result = make_new_order(session['auth_key'])
                if result:
                    # Mark the token as used in the session to expire it
                    session['used_token'] = signature
                    return str("amount")
            else:
                return "Invalid origin."

        except jwt.ExpiredSignatureError:
            return "Signature has expired."
        except jwt.InvalidTokenError as e:
            return f"Invalid token: {e}"

    return "No signature found in the URL."

@shop.route("/pincode/<pincode>")

def is_valid_pincode(pincode):
    url = f"https://track.delhivery.com/c/api/pin-codes/json/?filter_codes={pincode}"
    
    # Replace with your actual token
    token = "c9a21fcbe340c942cc29f49af37e58b4d3eb5771"
    
    # Define the headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {token}"
    }
    
    try:
        # Make the GET request using requests library
        response = requests.get(url, headers=headers)

   
        # Check if the response was successful
        if response.status_code == 200:
            if response.json()["delivery_codes"]:
                return response.json()["delivery_codes"]
                # return True
            else:
                return False
        else:
            return False

    except requests.exceptions.RequestException as e:
        # Handle any errors during the request
        return False
    
    
@shop.route("/waybill/fetch/<count>", methods=["GET"])
def fetch_way_bill(count):
    url = f"https://staging-express.delhivery.com/waybill/api/bulk/json/?count={count}"
    
    # Replace with your actual token
    token = "c9a21fcbe340c942cc29f49af37e58b4d3eb5771"
    
    # Define the headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {token}"
    }
    
    try:
        # Make the GET request using requests library
        response = requests.get(url, headers=headers)
        print(response)
        # Check if the response was successful
        if response.status_code == 200:
            return str(response)
        else:
            return str(response)

    except requests.exceptions.RequestException as e:
        # Handle any errors during the request
        return e

def encrypt_data(data):
    key = os.urandom(32)

    # Generate a random IV
    iv = os.urandom(16)

    # Pad the data to a multiple of 16 bytes
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    # Encrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(iv + encrypted_data).decode("utf-8")


""" API """


@shop.route("/cart/add_cart/<p_id>")
@is_login.login_required
def add_to_cart(p_id):
    if add_cart(p_id, 1):
        return redirect(url_for("shop.cart"))
    else:
        pass


@shop.route("/search", methods=["GET"])
def search():
    return render_template("themes/customer/shop/search.html")


@shop.route("/suggestion", methods=["GET"])
def suggest_item():
    query = request.args.get("query")
    not_found = """  <div class="container">
        <div class="error-container">
            <div class="error-icon">
                <i class="bi bi-exclamation-circle fs-1"></i>
            </div>
            <div class="error-title">Product Not Found</div>
            <div class="error-message">We're sorry, but the product you are looking for does not exist.</div>
            <a href="/" class="btn btn-danger mt-3 rounded-5">Go Back to Homepage</a>
        </div>
    </div>"""
    if query:
        products = list(get_item_suggestion(query))
        if products:
            return products
        else:
            return [None, None, not_found]
    else:
        return [None, None, not_found]
