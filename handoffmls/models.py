from datetime import datetime
from handoffmls import db


class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    employees = db.relationship('User', backref='lab', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    other_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    password = db.Column(db.String(60), nullable=False, default="password")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.first_name}', '{self.created_at}')"