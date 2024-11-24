from flask import Flask
from .class_files import seller_class

app = Flask(__name__)


def add_product(product_data):
    seller = seller_class.seller()
    result = seller.add_products(product_data)
    return result

def get_all_products():
    seller = seller_class.seller()
    result = seller.get_all_products_func()
    return result

def get_individual_product(p_id):
    seller = seller_class.seller()
    result = seller.get_individul_products_func(p_id)
    # print(result)
    return result


def edit_individual_product(p_id, data):
    seller = seller_class.seller()
    result = seller.edit_individual_product_func(p_id, data)
    if result:
        return True
    else :
        return False


def delete_individual_product(p_id):
    seller = seller_class.seller()
    result = seller.delete_individual_product_func(p_id)
    return result


# Pending orders
def get_pending_orders(seller_id=None):
    seller = seller_class.seller()
    result = seller.get_pending_orders_func(seller_id)
    return result

def get_single_pending_order(o_id,seller_id=None):
    seller = seller_class.seller()
    result = seller.get_single_pending_orders_func(o_id,seller_id)
    return result

# Completed orders
def get_completed_orders(seller_id=None):
    seller = seller_class.seller()
    result = seller.get_completed_orders_func(seller_id)
    return result

def get_single_completed_order(o_id,seller_id=None):
    seller = seller_class.seller()
    result = seller.get_single_completed_orders_func(o_id,seller_id)
    return result

# Canceled orders
def get_canceled_orders(seller_id=None):
    seller = seller_class.seller()
    result = seller.get_canceled_orders_func(seller_id)
    return result

def get_single_canceled_order(o_id,seller_id=None):
    seller = seller_class.seller()
    result = seller.get_single_canceled_orders_func(o_id,seller_id)
    return result
    

# if __name__ == '__main__':
#     app.run(debug=True)
