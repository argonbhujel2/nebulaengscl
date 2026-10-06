from datetime import datetime
from models import db


class Admission(db.Model):
    __tablename__ = 'admissions'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    student_name = db.Column(db.String(150), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    grade = db.Column(db.String(50), nullable=False)
    guardian_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    previous_school = db.Column(db.String(200))
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Admission {self.application_id}>'
