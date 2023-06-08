from datetime import datetime
from handoffmls import db
from sqlalchemy import CheckConstraint


class Handoff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.Text, nullable=False)
    actions = db.Column(db.Text, nullable=False)
    changes = db.Column(db.Text, nullable=False)
    evaluation = db.Column(db.Text, nullable=False)
    persons = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="in progress")
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    created_by = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    assign_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)
    created_by_user = db.relationship("User", foreign_keys=[created_by])
    assign_to_user = db.relationship("User", foreign_keys=[assign_to])
    lab_info = db.relationship("Lab", foreign_keys=[lab_id])
    tasks = db.relationship('Task', backref='handoff', lazy=True)
    __table_args__ = (
        CheckConstraint(status.in_(
            ["in progress", "completed"]), name="check_status"),
    )

    def __repr__(self):
        return f"Post('{self.summary}', '{self.created_at}', '{self.tasks}')"
