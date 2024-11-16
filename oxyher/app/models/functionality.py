from flask import Flask,  jsonify
from app import mysql as conn


def search_products(query):
    try:
        if query:
            mycur = conn.connection.cursor()
            mycur.execute('SELECT product_name FROM products WHERE product_name LIKE %s', ('%' + query + '%',))
            results = mycur.fetchall()
            mycur.close()
            # Convert results to a list of dictionaries

            results = [{'name': row[0]} for row in results]
        else:
            results = []

        
        return jsonify(results)
    except Exception as e:
        return jsonify({"status":"None"})