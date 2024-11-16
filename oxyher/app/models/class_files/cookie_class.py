from flask import make_response, redirect, url_for, session
from app import mysql as conn

class cookie_class:
    def __init__(self) :
        self.connection = conn.connection  
        self.cursor = self.connection.cursor()
        
    def set_cookie_(self, cookie_value):
        if 'auth_key' in session:
            response = make_response(redirect(url_for("home.index")))
            response.set_cookie("sess_id", cookie_value, max_age=60*24*60*60, path="/")
            return response
        elif 'seller_key' in session:
            response = make_response(redirect(url_for("seller.home")))
            response.set_cookie("sess_id", cookie_value, max_age=60*24*60*60, path="/")
            return response
        else :
            pass
        
        
    def delete_cookie(self):
        pass
    def update_cookie(self, cookie_value):
        if 'auth_key' in session:
            response = make_response(redirect(url_for("home.index")))
            response.set_cookie("sess_id", cookie_value, max_age=60*24*60*60, path="/")
            return response
        elif 'seller_key' in session:
            response = make_response(redirect(url_for("seller.home")))
            response.set_cookie("sess_id", cookie_value, max_age=60*24*60*60, path="/")
            return response
        else :
            pass
    
    def is_cookie_present(self, cookie_id):
        try:
            self.cursor.execute("SELECT username FROM user_session WHERE session_id = %s", (cookie_id,))
            user_id = self.cursor.fetchone()  
            if user_id:
                return user_id
            else:
                return False
        except Exception as e:
            print(e)
            print(f"COOKIE_ID_NOT_FOUND")
            return False
        
    def __del__(self):
        self.cursor.close()
        