from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect,
    session,
    make_response,
)
from ..models.functionality import search_products

# from app import csrf

products = Blueprint("products", __name__)

@products.route("/p")
def cart():
    return render_template("themes/cart.html")

@products.route("/checkout")
def checkout():
    return render_template("themes/checkout.html")

@products.route("/details")
def details():
    return render_template("themes/detail.html")

@products.route("/shopping")
def shopping():
    return render_template("themes/shop.html")








""" API  """
@products.route("/search", methods=['POST'])
# @csrf.exempt 
def search():
    query = request.json.get('query', '')
    return search_products(query)





