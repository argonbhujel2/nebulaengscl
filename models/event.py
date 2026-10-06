from datetime import datetime
from models import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.Date, nullable=False, index=True)
    event_time = db.Column(db.String(50))
    location = db.Column(db.String(200))
    image = db.Column(db.String(255))
    attachment = db.Column(db.String(255))
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Event {self.title}>'
