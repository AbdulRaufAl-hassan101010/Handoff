from handoffmls import db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handoff_id = db.Column(db.Integer, db.ForeignKey(
        'handoff.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task('{self.description}', '{self.created_at}', '{self.completed}')"
