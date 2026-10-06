import sys
import os

# Ensure project root is on sys.path (fixes some Windows/custom Python installs)
_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ROOT)

from flask import Flask, render_template
from config import Config
from models import init_db, db
from routes import register_blueprints


def create_app(config_class=Config):
    # Explicit absolute paths — required for reliable templates/static on Vercel
    app = Flask(
        __name__,
        template_folder=os.path.join(_ROOT, 'templates'),
        static_folder=os.path.join(_ROOT, 'static'),
        static_url_path='/static',
    )
    app.config.from_object(config_class)

    # On Vercel / serverless the deploy package is read-only.
    # Use /tmp for local uploads (ephemeral) or rely on Cloudinary.
    if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        app.config['UPLOAD_FOLDER'] = os.path.join('/tmp', 'uploads')

    # Ensure upload folder exists — ignore read-only filesystem errors
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError:
        pass

    init_db(app)
    register_blueprints(app)

    @app.template_filter('media')
    def media_filter(path):
        """Jinja filter: {{ path|media }} works for local and Cloudinary URLs."""
        from utils.helpers import media_url
        return media_url(path)

    # Create tables automatically for SQLite / first run
    with app.app_context():
        db.create_all()
        # Add missing columns on existing SQLite DBs (create_all does not alter)
        try:
            from sqlalchemy import text, inspect
            insp = inspect(db.engine)
            if 'site_settings' in insp.get_table_names():
                cols = {c['name'] for c in insp.get_columns('site_settings')}
                for col in ('hero_image', 'about_image', 'principal_image', 'logo', 'favicon'):
                    if col not in cols:
                        db.session.execute(text(f'ALTER TABLE site_settings ADD COLUMN {col} VARCHAR(255)'))
                        db.session.commit()
                if 'map_embed' not in cols:
                    db.session.execute(text('ALTER TABLE site_settings ADD COLUMN map_embed TEXT'))
                    db.session.commit()
            if 'news' in insp.get_table_names():
                cols = {c['name'] for c in insp.get_columns('news')}
                if 'attachment' not in cols:
                    db.session.execute(text('ALTER TABLE news ADD COLUMN attachment VARCHAR(255)'))
                    db.session.commit()
            if 'events' in insp.get_table_names():
                cols = {c['name'] for c in insp.get_columns('events')}
                if 'attachment' not in cols:
                    db.session.execute(text('ALTER TABLE events ADD COLUMN attachment VARCHAR(255)'))
                    db.session.commit()
        except Exception:
            pass

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
