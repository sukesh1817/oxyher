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




    

if __name__ == '__main__':
    app.run(debug=True)
