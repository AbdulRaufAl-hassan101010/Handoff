from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# store your mysql database connection credentials in the environment variable and get them for security reasons
from os import environ
db_user = environ.get("db_user")
db_password = environ.get("db_password")
db_name = environ.get("db_name")
db_host = environ.get("db_host")


# init flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab95dd6cf1628f866d9b4e6f27b7ecce'
# app.secret_key = environ.get('handoff_secret')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
db = SQLAlchemy(app)

from handoffmls.landingpage import landingpage
from handoffmls.dashboard import dashboard
app.register_blueprint(landingpage, url_prefix="")
app.register_blueprint(dashboard, url_prefix="/dashboard")
    


def create_app():
    """returns the flask app variable
    """
    return app
