from flask import Blueprint, render_template
from datetime import datetime

agreement = Blueprint("agreements", __name__)

@agreement.route("/privacy-policy")
def privacy_policy():
    current_year = datetime.now().year
    return render_template("policies/privacy_policy.html", year=current_year)

@agreement.route("/terms-and-conditions")
def terms_and_condition():
    current_year = datetime.now().year
    return render_template("policies/terms_and_condition.html", year=current_year)


@agreement.route("/return-policy")
def return_policy():
    current_year = datetime.now().year
    return render_template("policies/return_policy.html", year=current_year)



