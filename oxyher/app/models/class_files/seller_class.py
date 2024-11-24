""" This is a seller class this class contains the function about the seller side logics"""

"""
REFERENCE

p_id -> Product Id (Unique id that diffrentiates products)
"""
from flask import current_app, jsonify
import os
import uuid


class seller:
    def add_products(self, product_data):
        database = current_app.client[product_data["category"]]
        files = product_data["image_files"]
        collection = product_data["sub_category"]
        url = []
        for file in files:
            if file.filename == "":
                continue

            if file:
                random_filename = (
                    f"{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}"
                )
                file.save(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"]
                        + product_data["category"]
                        + "/"
                        + product_data["sub_category"]
                        + "/",
                        random_filename,
                    )
                )
                url.append(
                    product_data["category"]
                    + "/"
                    + product_data["sub_category"]
                    + "/"
                    + random_filename
                )

        product_data = {
            "title": product_data["title"],
            "description": product_data["description"],
            "product_id": product_data["product_id"],
            "price": float(product_data["price"]),
            "quantity": int(product_data["quantity"]),
            "category": product_data["category"],
            "sub_category": product_data["sub_category"],
            "return_policy": product_data["return_policy"],
            "attributes": product_data["attributes"],
            "img_url": url,
        }

        # Insert into MongoDB
        result = database[collection].insert_one(product_data)
        return f"SUCCESS"

    def get_all_products_func(self):
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

                        data = list(collection.find({}))
                        products.append(data)

            return products
        except Exception as e:
            error = {"CODE": 500, "ERROR": "UNABLE_TO_GET_PRODUCT_LIST"}
            return jsonify(error)

    def get_individul_products_func(self, p_id):
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
                        data = list(collection.find({"product_id": p_id}))
                        if data:
                            return data

        except Exception as e:
            error = {"CODE": 500, "ERROR": "UNABLE_TO_GET_PRODUCT_LIST"}
            return jsonify(error)

    def delete_individual_product_func(self, p_id):
        # try:

        #     database.intimate_wash.delete_one({"product_id":p_id})
        #     return "SUCCESS"
        # except Exception as e:

        #     return "FAILED"
        pass

    def delete_all_products_func(self):
        # try:
        #     database.intimate_wash.remove({})
        #     status = {"CODE" : 201, "STATUS" : "PRODUCT_DELETED_SUCCESS"}
        #     return jsonify(status)
        # except Exception as e:
        #     error = {"CODE" : 500, "ERROR" : "UNABLE_TO_DELETE_PRODUCT_LIST"}
        #     return jsonify(error)
        pass

    def edit_individual_product_func(self, p_id, updated_data):
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
                        data = list(collection.find({"product_id": p_id}))
                        if data:
                            collection.update_one(
                                {"product_id": p_id}, {"$set": updated_data}
                            )
                            # status = {"CODE" : 200, "STATUS" : "PRODUCT_EDITED_SUCCESS"}
                            # return jsonify(status)
                            return True

        except Exception as e:
            error = {"CODE": 500, "ERROR": "UNABLE_TO_DELETE_PRODUCT_LIST"}
            return jsonify(error)

    def get_pending_orders_func(self, seller_id):
        database = current_app.client["user"]
        collection = database["orders"]
        data = list(collection.find({"orders": {"$elemMatch": {"status": 1}}}))
        if data:
            return data
        else:
            return list("NO_DATA_FOUND")

    def get_single_pending_orders_func(self, o_id, seller_id):
        database = current_app.client["user"]
        collection = database["orders"]
        data = list(collection.find({"orders": {"$elemMatch": {"order_id": o_id, "status": 1}}}))
        
        if data:
            return data
        else:
            return list("NO_DATA_FOUND")
        
    def get_completed_orders_func(self, seller_id):
        database = current_app.client["user"]
        collection = database["orders"]
        data = list(collection.find({"orders": {"$elemMatch": {"status": 2}}}))
        if data:
            return data
        else:
            return list("NO_DATA_FOUND")

    def get_single_completed_orders_func(self, o_id, seller_id):
        database = current_app.client["user"]
        collection = database["orders"]
        data = list(collection.find({"orders": {"$elemMatch": {"order_id": o_id,"status": 2 }}}))
        
        if data:
            return data
        else:
            return False
        
    def get_canceled_orders_func(self, seller_id):
        database = current_app.client["user"]
        collection = database["orders"]
        data = list(collection.find({"orders": {"$elemMatch": {"status": 0}}}))
        if data:
            return data
        else:
            return False

    def get_single_canceled_orders_func(self, o_id, seller_id):
        database = current_app.client["user"]
        collection = database["orders"]
        data = list(collection.find({"orders": {"$elemMatch": {"order_id": o_id, "status": 0}}}))
        
        if data:
            return data
        else:
            return False
        
    
