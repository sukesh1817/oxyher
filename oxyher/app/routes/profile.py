from flask import (
    Blueprint,
    render_template,
    session,
    request,
    flash,
    redirect,
    url_for,
    jsonify,
)

from ..models.profile import (
    get_user_details,
    edit_user_details,
    get_my_orders,
    get_my_individual_orders,
)
from ..models.shop import get_products
from ..modules.is_valid import is_valid_email, is_valid_mobile_no, is_login

profile = Blueprint("profile", __name__)


@profile.route("")
@is_login.login_required
def home():
    user = get_user_details(session["auth_key"])
    return render_template("themes/customer/profile/profile.html", user=user)


@profile.route("/edit")
@is_login.login_required
def edit():
    user = get_user_details(session["auth_key"])
    return render_template("themes/customer/profile/edit_profile.html", user=user)


@profile.route("/orders")
@is_login.login_required
def orders():
    result = get_my_orders(session["auth_key"])
    return render_template("themes/customer/profile/orders/main.html", orders=result)


@profile.route("/orders/<o_id>")
@is_login.login_required
def individual_order(o_id):  # order-id
    result = get_my_individual_orders(session["auth_key"], o_id)
    details = {}
    user = get_user_details(session["auth_key"])
    products = result["orders"][0]["products"]
    prices = result["orders"][0]["prices"]
    for (p_id1,qty),(p_id2,price) in zip(products.items(), prices.items()):
        details[p_id1] = get_products("SINGLE", p_id1)
        details[p_id1]['qty'] = qty
        details[p_id1]['price'] = price
    for detail in details.items():
        print((detail[1]['qty']))
        
    # return "s"
    return render_template(
        "themes/customer/profile/orders/individual.html",
        details=details,
        order_details = result,
        name = user[1]
    )


@profile.route("/payments/history")
@is_login.login_required
def history():
    return render_template("themes/profile.html")


@profile.route("/periods")
@is_login.login_required
def periods():
    return render_template("themes/customer/periods.html")


""" POST """


@profile.route("/edit", methods=["POST"])
@is_login.login_required
def edit_profile():
    if request.method == "POST":
        # Extract data from form
        full_name = request.form.get("full_name") or None
        email = request.form.get("email") or None
        phone_no = request.form.get("phone_no") or None  # Set to None if empty
        address = request.form.get("address") or None  # Default value if not given
        pincode = request.form.get("pin_code") or None

        # Validation
        if not full_name or not email or not phone_no or not address or not pincode:
            flash("Please fill all the field", "danger")
            return redirect(url_for("profile.edit"))
        if not is_valid_mobile_no.check_mobile_no(
            phone_no
        ) or not is_valid_email.check_email(email):
            flash("Please fill mobile number or email correctly", "danger")
            return redirect(url_for("profile.edit"))
        if (
            not isinstance(pincode, str)
            or not len(pincode) == 6
            or not pincode.isdigit()
        ):
            flash("Please fill the pincode correctly", "danger")
            return redirect(url_for("profile.edit"))

        user_data = {
            "auth_key": session["auth_key"],
            "full_name": full_name,
            "email": email,
            "phone_no": phone_no,
            "address": address,
            "pin_code": pincode,
        }

        result = edit_user_details(user_data)

        if result:
            flash("Profile updated successfully!", "success")
            return redirect(url_for("profile.edit_profile"))
        else:
            flash("Something went wrong", "danger")
            return redirect(url_for("profile.edit"))
