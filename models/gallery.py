from datetime import datetime
from models import db


class Gallery(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), default='Campus', index=True)
    alt_text = db.Column(db.String(255))
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Gallery {self.title}>'
