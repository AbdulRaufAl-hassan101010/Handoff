from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# store your mysql database connection credentials in the environment variable and get them for security reasons
import os
db_user = os.environ.get("db_user")
db_password = os.environ.get("db_password")
db_name = os.environ.get("db_name")
db_host = os.environ.get("db_host")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab95dd6cf1628f866d9b4e6f27b7ecce'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
db = SQLAlchemy(app)


from handoffmls import routes

