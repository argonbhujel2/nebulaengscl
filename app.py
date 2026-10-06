import sys
import os
from datetime import datetime
from types import SimpleNamespace

_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ROOT)

from flask import Flask, render_template
from config import Config
from models import init_db, db
from routes import register_blueprints


def _fallback_settings():
    return SimpleNamespace(
        school_name='Shree Nebula English School',
        tagline='Inspiring Minds. Building Futures.',
        logo=None, favicon=None, phone='+977 984-2055059',
        email='nebula2053@gmail.com',
        address='Urlabari-8, Rajghat, Morang, Koshi Province, Nepal',
        facebook_url='', instagram_url='', youtube_url='',
        announcement='', footer_text='© 2026 Shree Nebula English School. All Rights Reserved.',
        years='25+', students='605+', teachers='40+', board_result='90%+',
        office_hours='Sun - Fri: 9:00 AM - 4:00 PM',
        hero_title='Inspiring Minds. Building Futures.',
        hero_description='', hero_image=None, about_image=None,
        principal_name='Principal', principal_message='', principal_image=None,
        about_description='', mission='', vision='', map_embed='',
    )


def _bootstrap_defaults(app):
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f'db.create_all warning: {e}')

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
            elif os.environ.get('RESET_ADMIN_PASSWORD') == '1':
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

        # Seed sample content once when tables are empty
        try:
            from models.notice import Notice
            from models.news import News
            if Notice.query.count() == 0 and News.query.count() == 0:
                from seed_data import seed_content
                seed_content()
                print('Sample content seeded')
        except Exception as e:
            print(f'content seed warning: {e}')
            try:
                db.session.rollback()
            except Exception:
                pass


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=os.path.join(_ROOT, 'templates'),
        static_folder=os.path.join(_ROOT, 'static'),
        static_url_path='/static',
    )
    app.config.from_object(config_class)

    if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        app.config['UPLOAD_FOLDER'] = os.path.join('/tmp', 'uploads')

    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError:
        pass

    init_db(app)
    register_blueprints(app)

    @app.template_filter('media')
    def media_filter(path):
        from utils.helpers import media_url
        try:
            return media_url(path)
        except Exception:
            return path or ''

    @app.context_processor
    def inject_globals():
        try:
            from models.settings import SiteSettings
            try:
                settings = SiteSettings.get_settings()
            except Exception as e:
                print(f'get_settings error: {e}')
                try:
                    db.session.rollback()
                except Exception:
                    pass
                settings = _fallback_settings()
        except Exception:
            settings = _fallback_settings()
        return {
            'settings': settings,
            'current_year': datetime.utcnow().year,
        }

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
