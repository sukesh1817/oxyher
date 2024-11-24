from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    current_app,
    request,
    jsonify,
    flash
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
    get_decrypted_dbs,
    send_order_notification
    
)
from modules.is_valid import is_login
import datetime, jwt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import os, requests, json

shop = Blueprint("shop", __name__)


""" LOGIN CHECK """


""" GET """


@shop.route("")
def home():
    search_query = request.args.get("q", "")  # Product search query
    category = request.args.get("c_", False)
    # enc_database = get_encrypted_dbs()
    if category:
        decrypted_category = get_decrypted_dbs(category)
        print(decrypted_category)
        products = get_products("CATEGORY", category=decrypted_category)

    else:
        products = get_products("ALL")

    try:
        for temp in products:
            if temp["product_id"]:
                return render_template(
                    "themes/customer/shop/shop.html", products=products, error=0
                )
            else:
                return render_template(
                    "themes/customer/shop/shop.html", error=1, products=0
                )
    except Exception as e:
        return render_template("themes/customer/shop/shop.html", error=1, products=0)

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
    send_order_notification("sukesh.1814@gmail.com","sample")
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
    if is_valid_pincode(user_data[5]):  # check the pincode is valid for delivery
        return render_template(
            "themes/customer/shop/checkout.html",
            user_addr=user_addr,
            user_data=user_data,
            products=user_items,
            pincode_error=0,
        )
    else:
        return render_template(
            "themes/customer/shop/checkout.html",
            user_addr=user_addr,
            user_data=user_data,
            products=user_items,
            pincode_error=1,
        )


@shop.route("/shipping/confirm")
@is_login.login_required
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

    flash("pincode is not deliverable . . .")
    return redirect(url_for("shop.cart"))
    # return redirect(redirect_url)


@shop.route("/payment")
@is_login.login_required
def payment():
    return render_template("themes/customer/shop/payment.html")

@shop.route("/mail")
def mail():
    company_name = "Oxyher"
    current_year = datetime.datetime.now().year
    return render_template("themes/seller/orders/send_mail/order_email_template.html", current_year=current_year,company_name=company_name)


@shop.route("/review")
@is_login.login_required
def review():
    return render_template("themes/customer/shop/review.html")


@shop.route("/order/make", methods=["GET"])
@is_login.login_required
def make_order():
    # Load the public key
    with open("/var/www/oxyher/sec_keys/public_key.pem", "r") as key_file:
        public_key = key_file.read()

    # Get the JWT signature from the query parameter
    signature = request.args.get("_sign")

    if signature:
        try:
            # Decode and verify the JWT using the public key and the RS256 algorithm
            decoded = jwt.decode(
                signature,
                public_key,
                algorithms=["RS256"],
                options={"verify_exp": True},
            )

            # Check if the token has already been used
            if session.get("used_token") == signature:
                return "Token expried"

            # Check the origin and other claims
            if decoded.get("origin") == "https://payments.oxyher.com":
                # delivery_json = open(
                #    "/var/www/oxyher/app/config/server/delivery/config.json"
                # )  # Delivery url JSON file
                result = make_new_order(session["auth_key"])
                if result['status']:
                    # Mark the token as used in the session to expire it
                    session["used_token"] = signature
                else:
                    flash("pincode is not deliverable")
                    return redirect(url_for("shop.cart"))
            else:
                return "Invalid origin."

        except jwt.ExpiredSignatureError:
            return "Signature has expired."
        except jwt.InvalidTokenError as e:
            return f"Invalid token: {e}"

    return "No signature found in the URL."


    
    

# @shop.route("/pincode/<pincode>", methods=["GET"])
def is_valid_pincode(pincode):
    # Replace with your actual token

    delivery_json = open("/var/www/oxyher/app/config/server/delivery/config.json")
    delivery = json.load(delivery_json)
    token = delivery["CREDENTIALS"]["API_TOKEN"]
    url = (
        delivery["PIN_CODES"]["PRODUCTION_URL"]
        + f"?token={token}&filter_codes={pincode}"
    )

    # Define the headers for the request
    headers = {
        "Content-Type": "application/json",
    }

    try:
        # Make the GET request using requests library
        response = requests.get(url, headers=headers)
        pin_codes = response.json()  # Use response.json() to parse the JSON
        pincode = jsonify(pin_codes).get_json()
        # Check if the response was successful
        if response.status_code == 200:
            if not(pincode['delivery_codes']):
                return False
            else:
                return True
        else:
            return False
    

    except requests.exceptions.RequestException as e:
        # Handle any errors during the request
        print("UNEXPEDTED ERROR DURING FETCHING PINCODE AVALIABILITY : ", e)
        return False


@shop.route("/waybill/<count>", methods=["GET"])
def fetch_way_bill(count):
    delivery_json = open("/var/www/oxyher/app/config/server/delivery/config.json")
    delivery = json.load(delivery_json)
    token = delivery["CREDENTIALS"]["TEST_API_TOKEN"]
    url = delivery["WAY_BILL"]["TESTING_URL"] + f"?token={token}&count={count}"
    # Define the headers for the request
    try:
        # Make the GET request using requests library
        response = requests.get(url)
        # Check if the response was successful
        if response.status_code == 200:
            return str(response.content.decode())
        else:
            return "None"
    except requests.exceptions.RequestException as e:
        # Handle any errors during the request
        return "None"


# @shop.route("/order/create", methods=["GET"])
def create_shipment(client, pickup):
    delivery_json = open("/var/www/oxyher/app/config/server/delivery/config.json")
    delivery = json.load(delivery_json)
    data = {
        "add": client['address'],
        "address_type": client['type'],
        "phone": client['mobile_number'],
        "payment_mode": client['payment_type'],
        "name": client['name'],
        "pin": client['pincode'],
        "order": client['no_of_item'],
        "country": client['country'],
        "cod_amount": client['price'],
        "waybill": "",
        "shipping_mode": "Surface",
        "pickup_name": pickup['name'],
        "pickup_city": pickup['city'],
        "pickup_pin": pickup['pincode'],
        "pickup_country": pickup['country'],
        "pickup_phone": pickup['mobile_number'],
        "pickup_add": pickup['address'],
    }

    raw_data = """
    format=json&data={{
    "shipments": [
        {{
            "add": "{add}",
            "address_type": "{address_type}",
            "phone": "{phone}",
            "payment_mode": "{payment_mode}",
            "name": "{name}",
            "pin": "{pin}",
            "order": "{order}",
            "country": "{country}",
            "cod_amount": {cod_amount},
            "waybill": "{waybill}",
            "shipping_mode" : "{shipping_mode}"
        }}
    ],
    "pickup_location": {{
        "name": "{pickup_name}",
        "city": "{pickup_city}",
        "pin": "{pickup_pin}",
        "country": "{pickup_country}",
        "phone": "{pickup_phone}",
        "add": "{pickup_add}"
    }}
    }}
""".format(
        **data
    )

    token = delivery["CREDENTIALS"]["TEST_API_TOKEN"]
    url = delivery["SHIPMENT_CREATION"]["TESTING_URL"]

    headers = {"Content-Type": "application/json", "Authorization": f"Token {token}"}
    try:
        # Make the GET request using requests library
        response = requests.post(url, headers=headers, data=raw_data)
        # Check if the response was successful
        order_info = response.json
        print(response.status_code)
        if response.status_code == 200:
            return jsonify(order_info())
        else:
            return "None"
    except requests.exceptions.RequestException as e:
        # Handle any errors during the request
        return "None"


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


@shop.route("/bill")
def bill_download():
    return render_template("themes/customer/payments/bill.html")


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
