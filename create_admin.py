#!/usr/bin/env python3
"""Secure CLI to create the first admin user."""
import sys
import os
import getpass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from models.admin import AdminUser


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        print('=' * 50)
        print('  Shree Nebula English School - Create Admin')
        print('=' * 50)

        existing = AdminUser.query.count()
        if existing > 0:
            print(f'\nWarning: {existing} admin user(s) already exist.')
            confirm = input('Create another admin? (y/N): ').strip().lower()
            if confirm != 'y':
                print('Aborted.')
                sys.exit(0)

        name = input('Admin Name: ').strip()
        if not name:
            print('Name is required.')
            sys.exit(1)

        email = input('Admin Email: ').strip().lower()
        if not email or '@' not in email:
            print('Valid email is required.')
            sys.exit(1)

        if AdminUser.query.filter_by(email=email).first():
            print(f'Admin with email {email} already exists.')
            sys.exit(1)

        password = getpass.getpass('Admin Password: ')
        if len(password) < 8:
            print('Password must be at least 8 characters.')
            sys.exit(1)

        password2 = getpass.getpass('Confirm Password: ')
        if password != password2:
            print('Passwords do not match.')
            sys.exit(1)

        admin = AdminUser(name=name, email=email, role='admin', is_active=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()

        print(f'\nAdmin user "{name}" ({email}) created successfully!')
        print('You can now log in at /admin/login')


if __name__ == '__main__':
    main()
