from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "auth_key" not in session:
            # return redrender_template("home.html", login=True)
            return redirect(url_for("home.index", login=True))
        return f(*args, **kwargs)
    return decorated_function
