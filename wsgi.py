"""WSGI entry point for Vercel / Gunicorn / production servers."""
from app import app

# Vercel looks for `app` or handler
application = app
