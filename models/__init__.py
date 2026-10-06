from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    from models import admin, notice, news, event, gallery, facility, teacher, admission, testimonial, contact, settings  # noqa: F401
