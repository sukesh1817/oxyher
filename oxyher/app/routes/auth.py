from modules.is_valid import is_valid_email, is_valid_mobile_no
from modules.quotes import women_quotes
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect,
    session,
    make_response,
    current_app,
    jsonify
)
from ..models.auth import signup_func, signin_func, google_oauth
import json
import html


auth = Blueprint("auth", __name__)

# Load Google OAuth credentials
with open("/var/www/oxyher/app/config/server/oauth/google_oauth.json") as google_oauth_json:
    google_oauth_data = json.load(google_oauth_json)


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    quotes = women_quotes.get_women_quotes()
    for quote in quotes:
        quote["quote"] = html.unescape(quote["quote"])
        quote["author"] = html.unescape(quote["author"])
    if request.method == "POST":
        auth_key = request.form.get("auth_key")
        if not (is_valid_email.check_email(auth_key) or is_valid_mobile_no.check_mobile_no(auth_key)):
            return render_template(
                "authentication/customer/signin.html",
                auth_key=True,
                error="Please provide a valid email or mobile number.",
                quotes = quotes
            )
        elif request.form.get("auth_key") and request.form.get("pass_key"):
            pass_key = request.form.get("pass_key")
            response = signin_func(auth_key, pass_key)
            if response[0]=="SUCCESS":
                return response[1]
            elif response[0] == "USERNAME_NOT_FOUND":
                return render_template(
                    "authentication/customer/pass_key.html",
                    acc_not_found=True,
                    error="Account not found",
                    auth_key=auth_key,
                    quotes = quotes
                )
            elif response[0]=="PASSWORD_IS_WRONG":
                return render_template(
                    "authentication/customer/pass_key.html",
                    pass_key=True,
                    error="Invalid password, please try again.",
                    auth_key=auth_key,
                    quotes = quotes
                )
            else :
                print(response)
                return "error"
                
        else:
            return render_template(
                "authentication/customer/pass_key.html", 
                auth_key=auth_key,
                quotes = quotes
            )
    else:
        return render_template("authentication/customer/signin.html", quotes = quotes)


@auth.route("/login/oauth", methods=["GET", "POST"])
def google_o_auth():
    redirect_uri = "https://oxyher.com/auth/oauth"
    return current_app.google.authorize_redirect(redirect_uri)


@auth.route('/oauth')
def auth_callback():
    # raise Exception("sample")
    token = current_app.google.authorize_access_token()  # Fetch access token
    user_info = current_app.google.get("https://www.googleapis.com/oauth2/v3/userinfo").json()
    
    result = google_oauth(user_info)
    return result




@auth.route("/signup", methods=["POST", "GET"])
def signup():
    quotes = women_quotes.get_women_quotes()
    for quote in quotes:
        quote["quote"] = html.unescape(quote["quote"])
        quote["author"] = html.unescape(quote["author"])
    if request.method == "POST":
        f_name = request.form.get("full_name")
        auth_key = request.form.get("auth_key")
        pass_key = request.form.get("pass_key")
        pass_key_confirm = request.form.get("pass_key_confirm")

        if not (is_valid_email.check_email(auth_key) or is_valid_mobile_no.check_mobile_no(auth_key)):
            return render_template(
                "authentication/customer/signup.html",
                auth_key=True,
                error="Please provide a valid email or mobile number.",
                data=request.form,
                quotes = quotes
            )
        elif len(f_name) < 3:
            return render_template(
                "authentication/customer/signup.html",
                f_name=True,
                error="Name must be at least 3 characters long.",
                data=request.form,
                quotes = quotes
            )
        elif pass_key != pass_key_confirm:
            return render_template(
                "authentication/customer/signup.html",
                pass_key_not_match=True,
                error="Passwords do not match.",
                data=request.form,
                quotes = quotes
            )
        elif len(pass_key) < 5:
            return render_template(
                "authentication/customer/signup.html",
                pass_key_len=True,
                error="Password must be at least 5 characters long.",
                data=request.form,
                quotes = quotes
            )
        else:
            result = signup_func(f_name, auth_key, pass_key)
        
            if result[0] == "USERNAME_ALREADY_FOUND":
                return render_template(
                    "authentication/customer/signup.html",
                    acc_already_found=True,
                    error="An account with this email/mobile already exists.",
                    data=request.form,
                    quotes = quotes
                )
            else:
                print(type(result))
                flash(result)
                # flash("Signup successful, please sign in.")
                return redirect(url_for("auth.signin"))
    else:
        return render_template("authentication/customer/signup.html", quotes = quotes)


@auth.route("/seller/signup", methods=["POST", "GET"])
def seller_signup():
    if request.method == "POST":
        f_name = request.form.get("full_name")
        auth_key = request.form.get("auth_key")
        pass_key = request.form.get("pass_key")
        pass_key_confirm = request.form.get("pass_key_confirm")

        if not (is_valid_email.check_email(auth_key) or is_valid_mobile_no.check_mobile_no(auth_key)):
            return render_template(
                "authentication/seller/signup.html",
                auth_key=True,
                error="Please provide a valid email or mobile number.",
                data=request.form,
            )
        elif len(f_name) < 3:
            return render_template(
                "authentication/seller/signup.html",
                f_name=True,
                error="Name must be at least 3 characters long.",
                data=request.form,
            )
        elif pass_key != pass_key_confirm:
            return render_template(
                "authentication/seller/signup.html",
                pass_key_not_match=True,
                error="Passwords do not match.",
                data=request.form,
            )
        elif len(pass_key) < 5:
            return render_template(
                "authentication/seller/signup.html",
                pass_key_len=True,
                error="Password must be at least 5 characters long.",
                data=request.form,
            )
        else:
            result = signup_func(f_name, auth_key, pass_key)
            if result == "USERNAME_ALREADY_FOUND":
                return render_template(
                    "authentication/seller/signup.html",
                    acc_already_found=True,
                    error="An account with this email/mobile already exists.",
                    data=request.form,
                )
            else:
                flash("Signup successful, please sign in.")
                return redirect(url_for("auth.signin"))
    else:
        return render_template("authentication/seller/signup.html", data={})


@auth.route("/signout")
# @is_login.login_required
def signout():
    session.clear()  
    resp = make_response(redirect(url_for('auth.signin')))
    resp.set_cookie('sess_id', '', expires=0)
    return resp


@auth.route("/forget_pass")
def forget_pass():
    return "forget_pass"




""" API  """

@auth.route("/get_sess_id")
def get_session_id():
    if session.get('auth_key') is not None:
        return {'auth_id': session.get('auth_key')}
    else :
        return jsonify({"Request":"Unauthorized"})
    
    

