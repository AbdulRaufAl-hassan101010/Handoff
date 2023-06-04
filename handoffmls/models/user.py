from datetime import datetime
from handoffmls import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    other_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    password = db.Column(db.String(60), nullable=False, default="password")
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)
