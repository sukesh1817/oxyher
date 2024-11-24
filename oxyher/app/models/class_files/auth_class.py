from app.modules.is_valid import is_valid_email
from flask import Flask
from flask_bcrypt import Bcrypt
from MySQLdb import OperationalError
from app import mysql as conn
import secrets
from datetime import datetime
from .cookie_class import cookie_class
from .session_class import session_class

app = Flask(__name__)  # Create an instance of your app
bcrypt = Bcrypt(app)


class authentication:
    def __init__(self):
        self.connection = conn.connection  # Use the existing MySQL connection
        self.cursor = self.connection.cursor()
        
    def username_found(self, auth_key):
        try:
            self.cursor.execute(
                "SELECT password FROM `user_auth` WHERE username = '{}';".format(
                    auth_key
                )
            )
            data = self.cursor.fetchall()
            if data and data[0][0]:
                return data[0][0], True
            return "ACCOUNT_NOT_FOUND", False
        except OperationalError as e:
            print(f"Database error: {e}")
            return "DB_ERROR", False

    def google_email_found(self, email):
        try:
            self.cursor.execute(
                "SELECT username FROM user_auth WHERE google_email_auth = %s", (email,)
            )

            data = self.cursor.fetchall()
            if data and data[0][0]:
                return data[0][0], True
            return "ACCOUNT_NOT_FOUND", False
        except OperationalError as e:
            print(f"Database error: {e}")
            return "DB_ERROR", False

    def signin_func(self, auth_key, pass_key):
        try:
            hashed_password = self.username_found(auth_key)
            if hashed_password[1]:
                # Validate the password
                is_valid = bcrypt.check_password_hash(hashed_password[0], pass_key)
                if is_valid:
                    session = session_class()
                    token_id = secrets.token_hex(nbytes=16)
                    if session.is_session_exists(auth_key):
                        session.update_the_session(auth_key, token_id)
                    else:
                        session.create_new_session(auth_key, token_id)
                    
                    cookie = cookie_class()
                    response = cookie.set_cookie_(token_id)
                    return "SUCCESS",response
                else:
                    return "PASSWORD_IS_WRONG", False
            else:
                return "USERNAME_NOT_FOUND",False
        except Exception as e:
            print(f"Error during sign-in: {e} ")
            return "UNEXPECTED_ERROR",False
        

    def signup_func(self, f_name, auth_key, pass_key):
        # register the user
        who_is = "USER"
        if self.username_found(auth_key)[1]:
            return "USERNAME_ALREADY_FOUND",False
        pass_key = bcrypt.generate_password_hash(pass_key).decode("utf-8")

        try:
            self.cursor.execute(
                "INSERT INTO `user_auth` (username, password, who_is) VALUES (%s, %s, %s)",
                (auth_key, pass_key, who_is),
            )

            conn.connection.commit()

            if is_valid_email.check_email(auth_key):
                self.cursor.execute(
                    "INSERT INTO `user_details` (username, full_name, email) VALUES (%s, %s, %s)",
                    (auth_key, f_name, auth_key),
                )

            else:
                self.cursor.execute(
                    "INSERT INTO `user_details` (username, full_name, phone_no) VALUES (%s, %s, %s)",
                    (auth_key, f_name, auth_key),
                )

            conn.connection.commit()

            self.cursor.execute(
                "SELECT username FROM `user_details` WHERE username=%s;", (auth_key,)
            )

            data = self.cursor.fetchall()
            if auth_key in data[0]:
                return "SUCCESS",True
            else:
                return "UNEXPECTED_ERROR",False
        except OperationalError as e:
            print(f"Database error during signup: {e}")
            return "UNEXPECTED_ERROR",False

    def google_oauth_func(self, user_info):
        
        try:
            if user_info["email_verified"] == True:
                email = user_info["email"]
                token_id = secrets.token_hex(nbytes=16)
                acc_details = self.google_email_found(email)
                if acc_details[1]:
                    session = session_class()
                    if session.is_session_exists(acc_details[0]):
                        
                        session.update_the_session(email, token_id)
                    else:
                        session.create_new_session(email, token_id)
                    cookie = cookie_class()
                    response = cookie.set_cookie_(token_id)
                    return response
                else:
                    f_name = user_info["name"]
    
                    self.cursor.execute(
                        "INSERT INTO `user_auth` (username, password, google_email_auth, account_verified, who_is) VALUES (%s, %s, %s, %s, %s)",
                        (email, "NULL", email, 1, "USER"),
                    )
                    self.cursor.execute(
                        "INSERT INTO `user_details` (username, full_name, email) VALUES (%s, %s, %s)",
                        (email, f_name, email),
                    )
                    self.cursor.execute(
                        "SELECT username FROM `user_details` WHERE username=%s;",
                        (email,),
                    )

                data = self.cursor.fetchall()
                if email in data[0]:
                    session = session_class()
                    if session.is_session_exists(user_info["email"]):
                        session.update_the_session(email, token_id)
                    else:
                        session.create_new_session(email, token_id)
                    cookie = cookie_class()
                    response = cookie.set_cookie_(token_id)
                    return response
                else:
                    return False

        except Exception as exe:
            print(f"SERVER ERROR : {exe}")
            
            return False
    def __del__(self):
        self.cursor.close()
    
