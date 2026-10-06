from datetime import datetime
from models import db


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    excerpt = db.Column(db.String(500))
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    attachment = db.Column(db.String(255))
    category = db.Column(db.String(100), default='General')
    author = db.Column(db.String(100), default='Admin')
    published = db.Column(db.Boolean, default=True)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<News {self.title}>'
