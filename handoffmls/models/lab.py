from handoffmls import db


class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    employees = db.relationship('User', backref='lab', lazy=True)

    def __repr__(self):
        return f"Lab('{self.name}', ' {self.email}', '{self.image_file}')"
