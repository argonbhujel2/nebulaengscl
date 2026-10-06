import sys
import os

# Ensure project root is on sys.path (fixes some Windows/custom Python installs)
_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ROOT)

from flask import Flask, render_template
from config import Config
from models import init_db, db
from routes import register_blueprints


def _bootstrap_defaults(app):
    """Create tables, default site settings, and default admin if missing."""
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f'db.create_all warning: {e}')

        # Add missing columns when possible (best-effort)
        try:
            from sqlalchemy import text, inspect
            insp = inspect(db.engine)
            if 'site_settings' in insp.get_table_names():
                cols = {c['name'] for c in insp.get_columns('site_settings')}
                for col, coltype in (
                    ('hero_image', 'VARCHAR(255)'),
                    ('about_image', 'VARCHAR(255)'),
                    ('principal_image', 'VARCHAR(255)'),
                    ('logo', 'VARCHAR(255)'),
                    ('favicon', 'VARCHAR(255)'),
                    ('map_embed', 'TEXT'),
                ):
                    if col not in cols:
                        db.session.execute(text(f'ALTER TABLE site_settings ADD COLUMN {col} {coltype}'))
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
        except Exception as e:
            print(f'schema migrate warning: {e}')

        # Default site settings row
        try:
            from models.settings import SiteSettings
            if not SiteSettings.query.first():
                db.session.add(SiteSettings())
                db.session.commit()
                print('Created default SiteSettings')
        except Exception as e:
            print(f'settings bootstrap warning: {e}')
            try:
                db.session.rollback()
            except Exception:
                pass

        # Default admin: admin@nebula / admin123
        try:
            from models.admin import AdminUser
            email = 'admin@nebula'
            existing = AdminUser.query.filter_by(email=email).first()
            if not existing:
                admin = AdminUser(name='Admin', email=email, role='admin', is_active=True)
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print('Created default admin admin@nebula / admin123')
            else:
                # Ensure known password on fresh deploys if env forces reset
                if os.environ.get('RESET_ADMIN_PASSWORD') == '1':
                    existing.set_password('admin123')
                    existing.is_active = True
                    db.session.commit()
                    print('Reset admin password to admin123')
        except Exception as e:
            print(f'admin bootstrap warning: {e}')
            try:
                db.session.rollback()
            except Exception:
                pass


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
        try:
            return media_url(path)
        except Exception:
            return path or ''

    _bootstrap_defaults(app)

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
