from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)
class Connection():
    def __init__(self, app):
        # Replace with your database configuration.
        self.app = app
        self.app.config["MYSQL_USER"] = "sukesh"
        self.app.config["MYSQL_HOST"] = "192.168.210.239"
        self.app.config["MYSQL_PASSWORD"] = "sukesh@123"
        self.app.config["MYSQL_DB"] = "oxyher"
        
    def return_connection(self):
        return MySQL(self.app)
    
    def __del__(self):
        self.return_connection.connection.close()


