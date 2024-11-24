from flask import Blueprint, render_template, request
from functools import wraps
import random
import string
from flask import (
    request,
    flash,
    redirect,
    url_for,
    current_app,
    jsonify,
    session,
    abort,
)
from ..models.seller import (
    add_product,
    get_all_products,
    get_individual_product,
    delete_individual_product,
    get_pending_orders,
    get_single_pending_order,
    get_completed_orders,
    get_single_completed_order,
    get_canceled_orders,
    get_single_canceled_order
)
from ..models.seller import edit_individual_product

# from app import app


# from app import csrf


seller = Blueprint("seller", __name__)


""" LOGICAL FUNCTIONS """

""" LOGIN CHECK """


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "seller_key" not in session:
            # return redrender_template("home.html", login=True)
            return redirect(url_for("home.index", login=True))
        return f(*args, **kwargs)

    return decorated_function


def generate_random_text(length):
    letters_and_digits = string.ascii_letters + string.digits
    random_text = "".join(random.choice(letters_and_digits) for i in range(length))
    return random_text


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


""" GET ROUTES """


@seller.route("", methods=["GET"])
@login_required
def home():
    return render_template("themes/seller/home.html")


@seller.route("/payments")
@login_required
def payments():
    return render_template("themes/seller/payments.html")


@seller.route("/products", methods=["GET"])
@login_required
def products():
    return render_template("themes/seller/products/products.html")


@seller.route("/accounts", methods=["GET"])
@login_required
def accounts():
    return render_template("themes/seller/accounts.html")


@seller.route("/notifications", methods=["GET"])
@login_required
def notifications():
    return render_template("themes/seller/notifications.html")


@seller.route("/orders", methods=["GET"])
@login_required
def orders():
    return render_template("themes/seller/orders/orders.html")

# Pending orders
@seller.route("/orders/show/p", methods=["GET"])
@login_required
def show_pending_orders():
    current_order_id = request.args.get("id_")  # Get the order ID from the URL
    pending_orders = get_pending_orders()
    no_orders_found = 0
    if not pending_orders:
        no_orders_found = 1
        
    return render_template(
        "themes/seller/orders/pending_orders/show_all_pending_orders.html",
        orders=pending_orders,
        current_order_id=current_order_id,
        no_orders_found = no_orders_found
    )
    



@seller.route("/orders/show/p/<o_id>", methods=["GET"])
@login_required
def show_single_pending_orders(o_id):
    pending_orders = get_single_pending_order(o_id=o_id)
    user_details = pending_orders[0]["user_details"]
    specific_order = None
    for order in pending_orders[0]["orders"]:
        if order["order_id"] == o_id:
            specific_order = order
            break
    if specific_order:
        order_id = specific_order["order_id"]
        total_amount = specific_order["total_amount"]
        order_date = specific_order["order_date"]
        products = specific_order["products"]
        prices = specific_order["prices"]
        product_info = {}
        for product_id in products.keys():
            product_info[product_id] = get_individual_product(product_id)
        return render_template(
            "themes/seller/orders/pending_orders/show_individual_pending_orders.html",
            order_id=order_id,
            total_amount=total_amount,
            order_date=order_date,
            products=products,
            prices=prices,
            user_details=user_details,
            product_info=product_info,
        )
    else:
        pass
    
# Completed orders
@seller.route("/orders/show/d", methods=["GET"])
@login_required
def show_completed_orders():
    current_order_id = request.args.get("id_")  # Get the order ID from the URL
    completed_orders = get_completed_orders()
    no_orders_found = 0
    if not completed_orders:
        no_orders_found = 1
    return render_template(
        "themes/seller/orders/pending_orders/show_all_completed_orders.html",
        orders=completed_orders,
        current_order_id=current_order_id,
        no_orders_found = no_orders_found
    )
    
    
# Canceled orders
@seller.route("/orders/show/c", methods=["GET"])
@login_required
def show_canceled_orders():
    current_order_id = request.args.get("id_")  # Get the order ID from the URL
    canceled_orders = get_canceled_orders()
    no_orders_found = 0
    if not canceled_orders:
        no_orders_found = 1
    return render_template(
        "themes/seller/orders/pending_orders/show_all_completed_orders.html",
        orders=canceled_orders,
        current_order_id=current_order_id,
        no_orders_found = no_orders_found
    )


@seller.route("/marketing", methods=["GET"])
@login_required
def marketing():
    return render_template("themes/seller/marketing.html")


@seller.route("/products/add_products", methods=["GET"])
@login_required
def add_products():
    product_id = generate_random_text(12)
    return render_template(
        "themes/seller/products/add_product.html", product_id=product_id
    )


@seller.route("/products/edit_product", methods=["GET"])
@login_required
def edit_products():
    products = get_all_products()
    img_url = current_app.config["IMG_URL"]
    # for product in products:
    #     for p in product:
    #         print(p["_id"])
    #         print("---------------------------------------------------------")
    # return str(type(products))
    return render_template(
        "themes/seller/products/edit_product.html", products=products, img_url=img_url
    )


@seller.route("/products/edit_product/<p_id>", methods=["GET"])
@login_required
def edit_products_individual(p_id):
    product = get_individual_product(p_id)
    img_url = current_app.config["IMG_URL"]
    return render_template(
        "themes/seller/products/edit_individual_product.html",
        product=product,
        img_url=img_url,
    )


@seller.route("/products/view_product", methods=["GET"])
@login_required
def view_products():
    return render_template("themes/seller/products/view_product.html")


""" POST METHODS """


@seller.route("/products/add_products", methods=["POST"])
@login_required
def post_products():
    dynamic_attributes = {}
    required_fields = [
        "product_title",
        "product_description",
        "product_id",
        "product_price",
        "product_quantity",
        "product_category",
        "return_policy",
        "sub_category" "images",
        "brand_name",
        "display_name",
    ]

    # for field in required_fields:
    #     if field not in request.form:
    #         abort(400, f"{request.form}")

    if request.form["product_category"] == "intimate_care":
        if request.form["sub_category"] == "sanitary_pads":
            dynamic_attributes = {
                "padType": request.form["padType"],
                "absorbency": request.form["absorbency"],
                "length": request.form["length"],
                "fragrance": request.form["fragrance"],
                "wings": request.form["wings"],
                "material": request.form["material"],
            }
        elif request.form["sub_category"] == "menstrual_cups":
            dynamic_attributes = {
                "cup_capacity": request.form["cup_capacity"],
                "absorbency": request.form["cup_size"],
                "cup_shape": request.form["cup_shape"],
            }
        elif request.form["sub_category"] == "menstrual_cup_wash":
            dynamic_attributes = {
                "self_time": request.form["self_time"],
                "ml": request.form["ml"],
            }

    elif request.form["product_category"] == "medicines":
        if request.form["sub_category"] == "spray":
            dynamic_attributes = {
                "type": request.form["type"],
                "ml": request.form["ml"],
            }
        elif request.form["sub_category"] == "roll_on":
            pass

    elif request.form["product_category"] == "kids_section":
        if (
            request.form["sub_category"] == "girls_shorts"
            or request.form["sub_category"] == "girls_panties"
            or request.form["sub_category"] == "camisole"
        ):
            dynamic_attributes = {
                "type": request.form["type"],
                "pack": request.form["pack"],
            }

    elif request.form["product_category"] == "inner_wears":
        if request.form["sub_category"] == "daily_essentials_panties":
            dynamic_attributes = {
                "panty_style": request.form["panty-style"],
                "size": request.form["size"],
                "color": request.form["color"],
            }

        elif request.form["sub_category"] == "period_panties":
            dynamic_attributes = {
                "absorbency_level": request.form["absorbency-level"],
                "style": request.form["style"],
                "color": request.form["color"],
                "size": request.form["size"],
            }
        elif request.form["sub_category"] == "undershorts":
            dynamic_attributes = {
                "fabric": request.form["fabric"],
                "length": request.form["length"],
                "color": request.form["color"],
                "size": request.form["size"],
            }
        elif request.form["sub_category"] == "bras_camis":
            dynamic_attributes = {
                "fabric": request.form["fabric"],
                "length": request.form["length"],
                "color": request.form["color"],
                "size": request.form["size"],
            }
    elif request.form["product_category"] == "medicines":
        if request.form["sub_category"] == "daily_essentials_panties":
            dynamic_attributes = {
                "panty_style": request.form["panty-style"],
                "size": request.form["size"],
                "color": request.form["color"],
            }
    else:
        dynamic_attributes = {}

    product_data = {
        "title": request.form["product_title"],
        "description": request.form["product_description"],
        "product_id": request.form["product_id"],
        "price": request.form["product_price"],
        "sub_category": request.form["sub_category"],
        "quantity": request.form["product_quantity"],
        "brand": request.form["brand_name"],
        "category": request.form["product_category"],
        "return_policy": request.form["return_policy"],
        "image_files": request.files.getlist("images"),
        "display_name": request.form["display_name"],
        "attributes": dynamic_attributes,
    }

    response = add_product(product_data)
    if response == "SUCCESS":
        flash("Products added successfully")
        return redirect(url_for("seller.add_products"))
    else:
        flash("Products added failed")
        return redirect(url_for("seller.add_products"))


@seller.route("/products/delete_product/", methods=["POST"])
@login_required
def delete_products():
    try:
        product_id = request.form.get("p_id")  # Get the product ID from the request
        if not product_id:
            return jsonify({"error": "No product ID provided"}), 400
        status = delete_individual_product(product_id)
        if status == "SUCCESS":
            return jsonify({"message": "Product deleted successfully"}), 201
        else:
            return jsonify({"error": "Product not found or unable to delete"}), 400
    except Exception as e:
        return jsonify({"error": "UNEXPECTED_ERROR"}), 500


@seller.route("/product/edit_product/<product_id>", methods=["POST"])
@login_required
def edit_product(product_id):
    print(request.form)
    try:
        updated_data = {
            "title": request.form["product_title"],
            "description": request.form["product_description"],
            "brand": request.form["brand_name"],
            "price": float(request.form["product_price"]),
            "quantity": int(request.form["product_quantity"]),
            "return_policy": request.form["return_policy"],
            "display_name": request.form["display_name"],
        }
        result = edit_individual_product(product_id, updated_data)
        if result:
            flash("Product edited success")
            return redirect(url_for("seller.edit_products_individual", p_id=product_id))
        else:
            flash("Product edited failed")
            return redirect(url_for("seller.edit_products_individual", p_id=product_id))

    except Exception as e:
        flash("Product edited failed")
        return redirect(url_for("seller.edit_products_individual", p_id=product_id))


""" THIS ROUTE PAGE IS FOR DOCUMENTS """


@seller.route("/docx")
def home_docx():
    return render_template("themes/seller/docx/home.html")


@seller.route("/docx/typo")
def typo_docx():
    return render_template("themes/seller/docx/typography.html")


@seller.route("/docx/icon")
def icon_docx():
    return render_template("themes/seller/docx/icons.html")


@seller.route("/docx/noti")
def noti_docx():
    return render_template("themes/seller/docx/notifications.html")


@seller.route("/docx/table")
def tables_docx():
    return render_template("themes/seller/docx/tables.html")


@seller.route("/docx/forms")
def forms_docx():
    return render_template("themes/seller/docx/forms.html")


# @seller.route("/view_orders")
# @login_required
# def view_orders():
#     # Query orders from the database that belong to the logged-in seller
#     orders = Order.query.filter_by(seller_id=current_user.id).all()
#     return render_template("themes/seller/view_orders.html", orders=orders)

# # Route to update order status
# @seller.route("/update_order/<int:order_id>", methods=['GET', 'POST'])
# @login_required
# def update_order(order_id):
#     order = Order.query.get_or_404(order_id)

#     # Ensure the seller owns the order
#     if order.seller_id != current_user.id:
#         flash("You do not have permission to update this order.", "danger")
#         return redirect(url_for('seller.view_orders'))

#     if request.method == 'POST':
#         # Get the updated status from the form
#         new_status = request.form.get('status')

#         # Update the order status
#         order.status = new_status
#         db.session.commit()

#         flash("Order status updated successfully!", "success")
#         return redirect(url_for('seller.view_orders'))

#     return render_template("themes/seller/update_order.html", order=order)


# @seller.route("/products/add_product", methods=['POST'])
# def add_product():
#     pass
