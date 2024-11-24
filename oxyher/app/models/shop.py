from flask import session, render_template
from datetime import datetime, timezone
from .class_files import shop_class
from .class_files import user_class
import random, string
import smtplib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json


def add_cart(product_id, qty):
    shop = shop_class.shop()
    response = shop.add_cart_func(product_id, qty, session["auth_key"])
    if response:
        return response


def get_products(method, p_id=None, cart=None, category=None):
    shop = shop_class.shop()
    if method == "ALL":
        products = shop.get_products_func()
        return products
    elif method == "SINGLE":
        product = shop.get_individual_product_func(p_id)
        return product
    elif method == "CATEGORY":
        product = shop.get_products_using_db_func(category)
        return product

    elif method == "CART":
        try:
            product = []
            shop_obj = shop_class.shop()
            for p_id, qty in cart["products"].items():
                p = shop_obj.get_individual_product_func(p_id)
                p["qty"] = qty
                product.append(p)
            return product
        except Exception as e:
            return product
    elif method == "RECCOMEND":
        try:
            shop_obj = shop_class.shop()
            recommend_products = shop_obj.get_recommend_products_func(p_id)
            return recommend_products
        except Exception as e:
            return product


def get_my_cart(u_id):  # u_id => user_id
    shop = shop_class.shop()
    products = shop.get_my_cart_func(u_id)
    return products


def get_my_final_items(auth_key):
    user = user_class.User()
    shop = shop_class.shop()
    products = []
    result = user.get_my_final_items_func(auth_key)
    for (p_id, q), (p_id, price) in zip(
        result["products"].items(), result["prices"].items()
    ):
        p = shop.get_individual_product_func(p_id)
        p["qty"] = q
        p["final_price"] = price
        products.append(p)
    return products


def get_user_details(auth_key):
    user = user_class.User()
    result = user.get_user_details_func(auth_key)
    return result


def get_user_addr(auth_key):
    user = user_class.User()
    result = user.get_user_addr_func(auth_key)
    return result


def get_item_suggestion(query):
    shop = shop_class.shop()
    result = shop.get_item_suggestion_func(query)
    return result


def generate_order_id(size=10, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def delete_products(method, u_id):
    if method == "CART":
        shop = shop_class.shop()
        shop.delete_my_cart_func(u_id)
    else:
        pass


def make_new_order(auth_key):
    shop = shop_class.shop()
    cart = get_my_cart(session["auth_key"])
    products = get_products("CART", None, cart)
    amount = 0
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
    for product in products:
        amount += product["qty"] * product["price"]
    order_data = {
        "order_id": generate_order_id(),
        "products": cart[
            "products"
        ],  # Example: {"product_id1": quantity, "product_id2": quantity}
        "payment_type": "PRE_PAID",
        "prices": cart[
            "prices"
        ],  # Example: {"product_id1": amount, "product_id2": amount}
        "total_amount": amount,  # Calculate total order amount
        "status": 1,  # 0 -> order_failed( may be canceled), 1 -> order_pending(order processing) 2 -> order_success(succesfully delivered),
        "order_date": formatted_datetime,  # Timestamp for order
    }
    result = shop.make_order(auth_key, order_data)
    if result["status"]:
        user_details = get_user_details(auth_key)
        send_order_notification()
        delete_products("CART", u_id=auth_key)
    return result


def get_random_products():
    shop = shop_class.shop()

    # Get the random products from ddifferent databases.
    random_products_1 = shop.get_random_products_func("medicines")
    random_products_2 = shop.get_random_products_func("inner_wears")
    random_products_3 = shop.get_random_products_func("intimate_care")
    random_products_4 = shop.get_random_products_func("intimate_care")
    if (
        random_products_1
        and random_products_2
        and random_products_3
        and random_products_4
    ):
        # Successfully get the random products.
        return [
            random_products_1,
            random_products_2,
            random_products_3,
            random_products_4,
        ]
    else:
        # Unable to get the random products from database.
        return "ERROR"


def get_encrypted_dbs():
    shop = shop_class.shop()
    return shop.get_encrypted_dbs_func()


def get_decrypted_dbs(key):
    shop = shop_class.shop()
    return shop.get_decrypted_dbs_func(key)


def send_order_notification(recipient_email, order_details):

    # Load mail config from json.
    current_year = datetime.datetime.now().year
    mail_config = open("/var/www/oxyher/app/config/server/mail_server/mail.json")
    mail = json.load(mail_config)

    # SMTP server configuration
    smtp_server = mail["MAIL_SERVER"]
    smtp_port = mail["MAIL_PORT"]
    sender_email = mail["MAIL_FROM"]["PRIMARY"]
    sender_password = mail["MAIL_PASSWORD"]
    sender_alias = mail["MAIL_FROM"]["NOTIFICATION"]
    seller_name = "Oxyher"
    customer_name = "Sukesh"
    customer_email = "sukesh.1814@gmail.com"
    customer_phone = "+91 9600944093"

    subject = "Order Booking Confirmation"

    # HTML template
    html_template = render_template(
        "themes/seller/orders/send_mail/order_email_template.html",
        current_year=current_year,
        seller_name=seller_name,
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone
    )
    message = MIMEMultipart("alternative")
    message["From"] = sender_alias
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(html_template, "html"))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        return {"status": True, "message": "Mail send successfully"}
    except Exception as e:
        print(f"Failed to send email: {e}")
        return {"status": False, "message": "Mail send Failed"}
