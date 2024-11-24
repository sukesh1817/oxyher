from app import mysql as conn
from flask import current_app, jsonify
import random, json, requests
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)


class shop:
    def __init__(self):
        self.connection = conn.connection  # Use the existing MySQL connection
        self.cursor = self.connection.cursor()  # Create a cursor

    def add_cart_func(self, product_id, qty, auth_key):
        try:
            # Connect to the database and collection
            database = current_app.client["user"]
            collection = database["cart"]
            product_info = self.get_individual_product_func(product_id)
            # Find if the cart for the user exists
            data = collection.find_one({"_id": auth_key})

            if data:
                # If the cart exists, update the quantity of the product
                collection.update_one(
                    {"_id": auth_key},
                    {
                        "$set": {f"products.{product_id}": qty}
                    },  # Use dot notation for nested products
                )
                collection.update_one(
                    {"_id": auth_key},
                    {
                        "$set": {f"prices.{product_id}": product_info["price"]}
                    },  # Use dot notation for nested products
                )
            else:
                # If no cart exists for this user, create a new cart with the product
                collection.insert_one(
                    {
                        "_id": auth_key,
                        "products": {product_id: qty},
                        "prices": {
                            product_id: product_info["price"]
                        },  # Initialize with the product and quantity and price
                    }
                )
            return True

        except Exception as e:
            # Return a more appropriate error message
            error = {"CODE": 500, "ERROR": str(e)}
            return jsonify(error)

    def get_products_func(self):
        products = []  # Initialize an empty list to store products
        try:
            databases = current_app.client.list_database_names()
            for database in databases:
                if database in ["config", "admin", "local", "user"]:
                    continue
                else:
                    database = current_app.client[database]
                    collections = database.list_collection_names()
                    for collection_name in collections:
                        collection = database[collection_name]
                        data = collection.find({})
                        for (
                            document
                        ) in data:  # Iterate over each document in the cursor
                            products.append(document)

            return products
        except Exception as e:
            error = {"CODE": 500, "ERROR": "UNABLE_TO_GET_PRODUCT_LIST"}
            return jsonify(error)

    def get_products_using_db_func(self, database):
        products = []  # Initialize an empty list to store products
        try:
            database = current_app.client[database]
            collections = database.list_collection_names()
            for collection_name in collections:
                collection = database[collection_name]
                data = collection.find({})
                for document in data:  # Iterate over each document in the cursor
                    products.append(document)
            return products
        except Exception as e:
            error = {"CODE": 500, "ERROR": "UNABLE_TO_GET_PRODUCT_LIST"}
            return jsonify(error)

    def get_individual_product_func(self, p_id):
        try:
            # Get a list of all databases
            databases = current_app.client.list_database_names()

            # Loop through the databases
            for db_name in databases:
                # Skip system databases
                if db_name in ["config", "admin", "local", "user"]:
                    continue

                # Access the database
                database = current_app.client[db_name]
                collections = (
                    database.list_collection_names()
                )  # Get all collections in the database

                # Loop through the collections
                for collection_name in collections:
                    collection = database[collection_name]

                    # Search for the product in the current collection by `product_id`
                    product = collection.find_one({"product_id": p_id})

                    # If the product is found, return it
                    if product:
                        return product

            # If the product is not found in any collection
            error = {"CODE": 404, "ERROR": "PRODUCT_NOT_FOUND"}
            return jsonify(error)

        except Exception as e:
            # Log the error message (optional: add proper logging)
            error = {"CODE": 500, "ERROR": "UNABLE_TO_GET_PRODUCT", "DETAIL": str(e)}
            return jsonify(error)

    def get_my_cart_func(self, u_id):
        database = current_app.client["user"]
        cart = database.cart.find_one({"_id": u_id})
        return cart

    def delete_my_cart_func(self, u_id):
        database = current_app.client["user"]
        cart = database.cart.delete_one({"_id": u_id})
        return cart

    def get_recommend_products_func(self, p_id):
        try:
            # Get a list of all databases
            databases = current_app.client.list_database_names()

            # Loop through the databases
            for db_name in databases:
                # Skip system databases
                if db_name in ["config", "admin", "local", "user"]:
                    continue

                # Access the database
                database = current_app.client[db_name]
                collections = (
                    database.list_collection_names()
                )  # Get all collections in the database

                # Loop through the collections
                for collection_name in collections:
                    collection = database[collection_name]

                    # Search for the product in the current collection by `product_id`
                    product = collection.find_one({"product_id": p_id})

                    # If the product is found, return it
                    if product:
                        return collection.find()

            # If the product is not found in any collection
            error = {"CODE": 404, "ERROR": "PRODUCT_NOT_FOUND"}
            return jsonify(error)

        except Exception as e:
            # Log the error message (optional: add proper logging)
            error = {"CODE": 500, "ERROR": "UNABLE_TO_GET_PRODUCT", "DETAIL": str(e)}
            return jsonify(error)

    def get_item_suggestion_func(self, query):
        try:
            search_term = f"%{query}%"
            self.cursor.execute(
                "SELECT database_name, document_name, product_name FROM products WHERE product_name LIKE %s;",
                (search_term,),
            )
            user_data = self.cursor.fetchall()
            return user_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def is_valid_pincode(self,pincode):
        # Load the configuration json file.
        delivery_json = open("/var/www/oxyher/app/config/server/delivery/config.json")
        delivery = json.load(delivery_json)
        token = delivery["CREDENTIALS"]["API_TOKEN"]
        url = (
            delivery["PIN_CODES"]["PRODUCTION_URL"]
            + f"?token={token}&filter_codes={pincode}"
        )

        # Define the headers for the request
        headers = {
            "Content-Type": "application/json",
        }

        try:
            # Make the GET request using requests library
            response = requests.get(url, headers=headers)
            pin_codes = response.json()  # Use response.json() to parse the JSON
            # Check if the response was successful
            if response.status_code == 200:
                # print("HEY")
                return {"status": True, "data": pin_codes}
            else:
                return {"status": False, "error": "something went wrong"}
        except requests.exceptions.RequestException as e:
            # Handle any errors during the request
            print("UNEXPEDTED ERROR DURING FETCHING PINCODE AVALIABILITY : ", e)
            return {"status": False, "error": e}

    def make_order(self, user_id, order_data):
        try:
            # Get the user_data.
            self.cursor.execute(
                "SELECT * FROM user_details WHERE username = %s;",
                (user_id,),
            )
            user_data = self.cursor.fetchall()
            pincode = self.is_valid_pincode(user_data[0][6])
            # Raise error if the pincode is not deliverable.
            if not(pincode["status"] and pincode['data']['delivery_codes']):
                raise Exception("PINCODE_NOT_DELIVERABLE")

            # Select database and collections and update or create the new orders.
            database = current_app.client["user"]
            collection = database["orders"]
            existing_user = collection.find_one({"_id": user_id})
            if existing_user:
                result = collection.update_one(
                    {"_id": user_id}, {"$push": {"orders": order_data}}
                )
                if result.modified_count > 0:
                    return {"status": True, "message": "success"}
                else:
                    return {"status": False, "error": "document not modified"}
            else:
                user_details = {
                    "name": user_data[0][1],
                    "address": user_data[0][4],
                    "mobile": user_data[0][3],
                    "email": user_data[0][0],
                    "pincode": user_data[0][6],
                }
                new_user_data = {
                    "_id": user_id,
                    "user_details": user_details,
                    "orders": [order_data],
                }
                collection.insert_one(new_user_data)
                return {"status": True, "message": "success"}

        except Exception as e:
            return {"status": False, "error": "error in order making | "+ str(e)}

    def get_random_products_func(self, db):
        # This function helps to get random products from the database.
        try:
            database = current_app.client[str(db)]
            rand = 0
            collections = database.list_collection_names()
            count = len(collections)  # Get the length of collections.
            rand = random.randrange(
                count
            )  # Generate random number, less than the collection length.
            collection = database[collections[rand]]  # Select random collection.
            data = collection.aggregate([{"$sample": {"size": 2}}])
            if data:
                return data
        except Exception as e:
            print(e)
            return False

    def get_encrypted_dbs_func(self):
        # This function helps to encrypt the database name.
        try:
            # key = Fernet.generate_key()  # Generate a key pair.
            # cipher_suite = Fernet(key)
            databases = (
                current_app.client.list_database_names()
            )  # Get the avaliable databases
            new_dbs = []
            for database in databases:
                if database in ["config", "admin", "local", "user"]:
                    continue
                old_db = database
                database = cipher_suite.encrypt(database.encode()).decode()
                new_dbs.append({old_db: database})
            if new_dbs:
                return new_dbs
        except Exception as e:
            print("ERROR OCCURED WHILE ENCRYPTING : ", e)
            return False

    def get_decrypted_dbs_func(self, value):
        # This function helps to encrypt the database name.
        try:
            if value:
                # return cipher_suite
                text = cipher_suite.decrypt(value.encode()).decode()
                return text
        except Exception as e:
            print("ERROR OCCURED WHILE DECRYPTING : ", e)
            return False

    def __del__(self):
        # Close the MySql connection.
        self.cursor.close()
