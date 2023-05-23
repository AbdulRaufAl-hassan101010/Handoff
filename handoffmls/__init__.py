from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab95dd6cf1628f866d9b4e6f27b7ecce'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://handoff:password@localhost/handoff_db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)