from flask import Flask
from flask_mysql_connector import MySQL
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, CLOUD_NAME, API_KEY, API_SECRET
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
import cloudinary


mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DATABASE=DB_NAME,
        MYSQL_HOST=DB_HOST,
        #BOOTSTRAP_SERVE_LOCAL=BOOTSTRAP_SERVE_LOCAL
    )

    cloudinary.config(
        CLOUD_NAME = CLOUD_NAME,
        API_KEY = API_KEY,
        API_SECRET = API_SECRET
    )

    mysql.init_app(app)
    
    CSRFProtect(app)

    from .routes import routes
    # from .auth import auth

    app.register_blueprint(routes, url_prefix='/')

    return app

