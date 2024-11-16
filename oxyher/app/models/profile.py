from flask import Flask, flash
from .class_files import user_class



app = Flask(__name__)  # Create an instance of your app

def get_user_details(username):
    user = user_class.User()
    result = user.get_user_details_func(username)
    return result

def edit_user_details(user_data):
    user = user_class.User()
    result = user.edit_user_details_func(user_data)
    return result


def get_my_orders(auth_key):
    user = user_class.User()
    result = user.get_my_orders_func(auth_key)
    return result
    
def get_my_individual_orders(auth_key, o_id):
    user = user_class.User()
    result = user.get_my_individual_orders_func(auth_key, o_id)
    return result
    
