"""
This is the configuration file of the flask.
some of the configuration such as Mysql connection, CSRF Initialization are done in this file.
"""

from flask import Flask
from flask_mysqldb import MySQL
import sys
# from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_cors import CORS
from flask_session import Session
import json
import os
from authlib.integrations.flask_client import OAuth
from pymongo import MongoClient
from werkzeug.middleware.proxy_fix import ProxyFix




mysql = MySQL()
# csrf = CSRFProtect()
oauth = OAuth()

mysql_json = open("/var/www/oxyher/app/config/database/sql/mysql.json")
google_oauth_json = open("/var/www/oxyher/app/config/server/oauth/google_oauth.json")
mongodb_json = open("/var/www/oxyher/app/config/database/nosql/mongodb.json")  
image_json = open("/var/www/oxyher/app/config/server/seller_image/seller_img.json")  

mysql_data = json.load(mysql_json)
google_oauth_data = json.load(google_oauth_json)
mongodb_data = json.load(mongodb_json)  
image = json.load(image_json)  

sys.path.append("/var/www/oxyher/app")




def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SESSION_COOKIE_DOMAIN'] = '.oxyher.com'

    # Session configuration
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    
    # CROS init
    CORS(app)

    # CSRF token initialization
    # app.config['WTF_CSRF_TIME_LIMIT'] = None 
    # csrf.init_app(app)

    # Database initialization
    app.config["MYSQL_USER"] = mysql_data["USERNAME"]
    app.config["MYSQL_HOST"] = mysql_data["MYSQL_HOST"]
    app.config["MYSQL_PASSWORD"] = mysql_data["PASSWORD"]
    app.config["MYSQL_DB"] = mysql_data["DATABASE"]
    mysql.init_app(app)

    # Google OAuth initialization
    app.config["GOOGLE_CLIENT_ID"] = google_oauth_data["GOOGLE_CLIENT_ID"]
    app.config["GOOGLE_CLIENT_SECRET"] = google_oauth_data["GOOGLE_CLIENT_SECRET"]
    app.google = oauth.register(
        name='google',
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        access_token_url="https://accounts.google.com/o/oauth2/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        redirect_uri="https://oxyher.com/auth/oauth",  # Ensure this matches your Google Console redirect URI
        client_kwargs={"scope": "openid email profile"},  # change it to collect more details from oauth
        jwks_uri = "https://www.googleapis.com/oauth2/v3/certs",
        
    )
    oauth.init_app(app)
    
    # get real ip of the client configuration
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)




    # Initialize MongoDB connection
    client = MongoClient(mongodb_data['MONGO_URI'],  maxPoolSize=20)  
    app.client = client

    # image uploads routes
    UPLOAD_FOLDER = image['PATH']
    IMG_URL = image['IMG_URL']
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['IMG_URL'] = IMG_URL
    
   
    
    



    # Initialize the routes
    from .routes.auth import auth  # this is authentication routes
    from .routes.home import home
    from .routes.shop import shop
    from .routes.profile import profile
    from .routes.products import products  # this is for product view routes
    from .routes.seller import seller
    from .routes.agreement import agreement
    from .routes.payments import payments

    # Register blueprints
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(shop, url_prefix="/shop")
    app.register_blueprint(seller, url_prefix="/seller")
    app.register_blueprint(products, url_prefix="/products")
    app.register_blueprint(profile, url_prefix="/profile")
    app.register_blueprint(agreement, url_prefix="/agreements")
    app.register_blueprint(payments, url_prefix="/payments")
    

    
    
    return app
