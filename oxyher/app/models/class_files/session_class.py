from flask import request, session
from app import mysql as conn
from datetime import datetime


class session_class:
    def __init__(self):
        self.connection = conn.connection  # Use the existing MySQL connection
        self.cursor = self.connection.cursor()
        
    def create_new_session(self, auth_key, token):
        try:
    
            ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            user_agent = dict(request.headers)
            self.cursor.execute(
                "INSERT INTO `user_session` VALUES (%s, %s, %s, %s, %s)",
                (auth_key, token, formatted_datetime, ip,user_agent['User-Agent']),
            )
            conn.connection.commit()
            self.cursor.execute(
                "SELECT who_is FROM `user_auth`WHERE username = %s ", (auth_key,)
            )
            data = self.cursor.fetchall()
            
            if data[0][0] == "SELLER":
                session["seller_key"] = auth_key
            elif data[0][0] == "USER":
                session["auth_key"] = auth_key               
            return True
        except Exception as e:
            return False

    def is_session_exists(self, auth_key):

        try:
            self.cursor.execute(
                "SELECT username FROM `user_session`WHERE username = %s ", (auth_key,)
            )
            data = self.cursor.fetchall()
            
            if auth_key in data[0]:
                return True
            else:
                
                return False
        except Exception as e:
            return False

    def update_the_session(self, auth_key, token):

        ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")
        user_agent = dict(request.headers)
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute(
            "UPDATE `user_session` SET session_id = %s, last_login_ip = %s, last_login_time = %s, user_agent = %s WHERE username = %s",
            (token, ip[0], formatted_datetime,user_agent['User-Agent'], auth_key ),
        )

        conn.connection.commit()
        self.cursor.execute(
                "SELECT who_is FROM `user_auth` WHERE username = %s ", (auth_key,)
            )
        data = self.cursor.fetchall()
        if data[0][0] == "SELLER":
            session["seller_key"] = auth_key
        elif data[0][0] == "USER":
            session["auth_key"] = auth_key   
        return True
    def __del__(self):
        self.cursor.close()
