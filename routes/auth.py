from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models.admin import AdminUser
from forms.admin_forms import LoginForm

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access the admin panel.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def get_current_admin():
    if 'admin_id' in session:
        return AdminUser.query.get(session['admin_id'])
    return None


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if 'admin_id' in session:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = AdminUser.query.filter_by(email=form.email.data.lower().strip()).first()
        if admin and admin.is_active and admin.check_password(form.password.data):
            session['admin_id'] = admin.id
            session['admin_name'] = admin.name
            session.permanent = True
            flash(f'Welcome back, {admin.name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        flash('Invalid email or password.', 'error')
    return render_template('admin/login.html', form=form)


@auth_bp.route('/admin/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
