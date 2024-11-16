from flask import Flask, flash
from .class_files import auth_class
from .class_files import cookie_class
from .class_files import session_class
import secrets


app = Flask(__name__)  # Create an instance of your app


def signup_func(f_name, auth_key, pass_key):
    auth = auth_class.authentication()
    result = auth.signup_func(f_name, auth_key, pass_key)
    return result


def signin_func(auth_key, pass_key=None):
    auth = auth_class.authentication()
    result = auth.signin_func(auth_key, pass_key)
    return result


def google_oauth(user_info):
    oauth = auth_class.authentication()
    result = oauth.google_oauth_func(user_info)
    return result


def is_cookie_exists(cookie_id):
    cookie = cookie_class.cookie_class()
    user_id = cookie.is_cookie_present(cookie_id)
    if user_id:
        session = session_class.session_class()
        cookie_id = secrets.token_hex(nbytes=16)
        if session.update_the_session(user_id[0], cookie_id):
            if cookie.update_cookie(cookie_id):
                return cookie.update_cookie(cookie_id)
        else:
            return False
    else:
        return False
