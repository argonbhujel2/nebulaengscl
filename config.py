import os
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    url = os.environ.get('DATABASE_URL') or 'sqlite:///school.db'
    # Heroku/Neon sometimes use postgres:// which SQLAlchemy 2 needs as postgresql://
    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    # Force psycopg2 driver (package: psycopg2-binary). Neon/Vercel Postgres
    # URLs sometimes use postgresql+psycopg:// which expects the psycopg v3 package.
    if url.startswith('postgresql+psycopg://'):
        url = url.replace('postgresql+psycopg://', 'postgresql+psycopg2://', 1)
    elif url.startswith('postgresql://'):
        url = url.replace('postgresql://', 'postgresql+psycopg2://', 1)
    # Neon / many cloud Postgres require SSL
    if url.startswith('postgresql') and 'sslmode=' not in url:
        sep = '&' if '?' in url else '?'
        url = f'{url}{sep}sslmode=require'
    return url


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024))
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    PERMANENT_SESSION_LIFETIME = 3600 * 8
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
