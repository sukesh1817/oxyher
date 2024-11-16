from app import mysql as conn
from flask import current_app


class User:
    def __init__(self):
        self.connection = conn.connection  # Use the existing MySQL connection
        self.cursor = self.connection.cursor()  # Create a cursor

    def get_user_details_func(self, username):
        try:
            self.cursor.execute(
                "SELECT username, full_name, email, phone_no, address, pincode FROM user_details WHERE username = %s",
                (username,),
            )
            user_data = self.cursor.fetchone()
            return user_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def edit_user_details_func(self, user_data):
        try:
            self.cursor.execute(
                "UPDATE user_details SET full_name = %s, email = %s, phone_no = %s, address = %s, gender = %s, pincode = %s WHERE username = %s;",
                (
                    user_data["full_name"],
                    user_data["email"],
                    user_data["phone_no"],
                    user_data["address"],
                    "NOT_GIVEN",
                    str(user_data["pin_code"]),
                    user_data["auth_key"],
                ),
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def get_user_addr_func(self, auth_key):
        try:
            self.cursor.execute(
                "SELECT address FROM user_details WHERE username = %s", (auth_key,)
            )
            user_data = self.cursor.fetchone()
            return user_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_my_final_items_func(self, auth_key):
        database = current_app.client["user"]
        cart = database.cart.find_one({"_id": auth_key})
        return cart

    def get_my_orders_func(self, auth_key):
        database = current_app.client["user"]
        orders = database.orders.find_one({"_id": auth_key})
        return orders

    def get_my_individual_orders_func(self, auth_key, o_id):
        database = current_app.client["user"]
        orders = database.orders.find_one(
            {"_id": auth_key, "orders.order_id": o_id}, {"orders.$": 1}
        )
        return orders

    def __del__(self):
        self.cursor.close()
