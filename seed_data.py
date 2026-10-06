#!/usr/bin/env python3
"""Seed database with sample content for Shree Nebula English School."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date, timedelta
from models import db
from models.settings import SiteSettings
from models.notice import Notice
from models.news import News
from models.event import Event
from models.facility import Facility
from models.testimonial import Testimonial
from models.teacher import Teacher
from utils.helpers import slugify, unique_slug


def seed_content():
    """Insert sample content if tables are empty. Must run inside app context."""
    settings = SiteSettings.get_settings()
    settings.school_name = 'Shree Nebula English School'
    settings.tagline = 'Inspiring Minds. Building Futures.'
    settings.phone = '+977 984-2055059'
    settings.email = 'nebula2053@gmail.com'
    settings.address = 'Urlabari-8, Rajghat, Morang, Koshi Province, Nepal'
    settings.facebook_url = 'https://www.facebook.com'
    settings.announcement = 'Admissions Open — ECD to Grade 10'
    settings.hero_title = 'Inspiring Minds. Building Futures.'
    settings.hero_description = (
        'A co-educational institution in Urlabari offering quality education from '
        'Early Childhood Development (ECD) to Grade 10, where students discover '
        'their potential and prepare for a better future.'
    )
    settings.about_description = (
        'Shree Nebula English School is a private co-educational institution located '
        'in Urlabari-8, Rajghat, Morang district, Koshi Province, Nepal. We provide '
        'academic programs spanning from Early Childhood Development (ECD) up to '
        'Grade 10, with modern learning amenities including a dedicated computer lab, '
        'standard classrooms, and space for extracurricular activities.'
    )
    settings.mission = 'To provide quality education and equal opportunities for all students from ECD to Grade 10.'
    settings.vision = 'To be a center of excellence in education serving the Urlabari and Morang community.'
    settings.principal_name = 'Principal'
    settings.principal_message = (
        'Dear Parents and Students,\n\n'
        'Education is not only about academic achievement. It is about developing '
        'responsible, confident and compassionate individuals who can contribute '
        'positively to society.\n\n'
        'At Shree Nebula English School, we strive to create an environment where '
        'every student is encouraged to learn, explore and grow from ECD through Grade 10.'
    )
    settings.years = '25+'
    settings.students = '605+'
    settings.teachers = '40+'
    settings.board_result = '90%+'
    settings.office_hours = 'Sun - Fri: 9:00 AM - 4:00 PM'
    db.session.commit()
    print('Settings seeded (Shree Nebula English School).')

    if Facility.query.count() == 0:
        facilities = [
            ('Computer Lab', 'Modern computer lab for digital literacy and IT skills.', 'fa-laptop'),
            ('Library', 'Well-stocked library with textbooks and reference materials.', 'fa-book'),
            ('Science Lab', 'Hands-on science experiments for secondary students.', 'fa-flask'),
            ('Playground', 'Open space for sports and outdoor activities.', 'fa-futbol'),
            ('Smart Classrooms', 'Standard classrooms designed for effective learning.', 'fa-chalkboard'),
            ('Transportation', 'Safe transport options for students in the Urlabari area.', 'fa-bus'),
        ]
        for title, desc, icon in facilities:
            db.session.add(Facility(title=title, description=desc, icon=icon, published=True))
        db.session.commit()
        print('Facilities seeded.')

    if Notice.query.count() == 0:
        notices = [
            ('Admissions Open for Academic Year', 'Admissions are now open for ECD to Grade 10. Visit the school office or apply online.', 'Admission'),
            ('School Reopening Notice', 'Classes will resume as per the academic calendar. Please ensure students arrive on time.', 'General'),
            ('Parent Orientation Program', 'Orientation for new parents will be held at the school hall. All new families are invited.', 'Event'),
        ]
        for title, content, cat in notices:
            slug = unique_slug(Notice, slugify(title))
            db.session.add(Notice(title=title, slug=slug, content=content, category=cat, published=True))
        db.session.commit()
        print('Notices seeded.')

    if News.query.count() == 0:
        news_items = [
            ('Welcome to the New Academic Session', 'We warmly welcome all students and parents to the new academic session at Shree Nebula English School.', 'General'),
            ('Computer Lab Upgraded', 'Our computer lab has been upgraded to support better digital learning for all grades.', 'Campus'),
            ('Annual Sports Day Highlights', 'Students participated enthusiastically in races, games and team events during Sports Day.', 'Sports'),
        ]
        for title, content, cat in news_items:
            slug = unique_slug(News, slugify(title))
            db.session.add(News(
                title=title, slug=slug, excerpt=content[:200], content=content,
                category=cat, author='Admin', published=True
            ))
        db.session.commit()
        print('News seeded.')

    if Event.query.count() == 0:
        today = date.today()
        events = [
            ('Admission Counseling Day', 'Meet teachers and learn about our programs from ECD to Grade 10.', today + timedelta(days=10), '10:00 AM', 'School Office'),
            ('Science Exhibition', 'Students present science projects and experiments.', today + timedelta(days=25), '9:00 AM', 'Science Lab'),
            ('Parent Teacher Meeting', 'Important parent-teacher meeting to discuss student progress.', today + timedelta(days=35), '10:00 AM', 'School Hall'),
            ('Cultural Program', 'Student dance performances and cultural celebrations.', today + timedelta(days=50), '11:00 AM', 'School Premises'),
        ]
        for title, desc, edate, etime, loc in events:
            slug = unique_slug(Event, slugify(title))
            db.session.add(Event(
                title=title, slug=slug, description=desc,
                event_date=edate, event_time=etime, location=loc, published=True
            ))
        db.session.commit()
        print('Events seeded.')

    if Testimonial.query.count() == 0:
        testimonials = [
            ('Parent', 'Parent of Grade 8 Student', 'Shree Nebula English School provides a supportive environment. We are happy with our child\'s progress in Urlabari.', 5),
            ('Student', 'Grade 10 Student', 'The teachers are supportive and the computer lab helps us learn practical skills.', 5),
            ('Guardian', 'Parent', 'A good co-educational school from ECD to Grade 10 in Rajghat, Morang. Highly recommended.', 5),
        ]
        for name, role, msg, rating in testimonials:
            db.session.add(Testimonial(name=name, role=role, message=msg, rating=rating, published=True))
        db.session.commit()
        print('Testimonials seeded.')

    if Teacher.query.count() == 0:
        teachers = [
            ('Principal', 'Principal', 'M.Ed.', 'Leading Shree Nebula English School with dedication to quality education.', 'Administration'),
            ('Vice Principal', 'Vice Principal', 'B.Ed.', 'Supporting academic excellence from ECD to Grade 10.', 'Administration'),
            ('Computer Teacher', 'IT Coordinator', 'B.Sc. CS', 'Guiding students in the computer lab and digital skills.', 'Computer'),
            ('Science Teacher', 'Science Teacher', 'M.Sc.', 'Hands-on science learning for secondary students.', 'Science'),
        ]
        for name, desig, qual, bio, subj in teachers:
            db.session.add(Teacher(name=name, designation=desig, qualification=qual, bio=bio, subject=subj, published=True))
        db.session.commit()
        print('Teachers seeded.')

    print('Seed data completed for Shree Nebula English School!')


def seed():
    from app import create_app
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_content()


if __name__ == '__main__':
    seed()
