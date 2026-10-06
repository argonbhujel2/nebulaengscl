#!/usr/bin/env python3
"""Seed database with sample content for Shree Nebula English School."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date, timedelta
from app import create_app
from models import db
from models.settings import SiteSettings
from models.notice import Notice
from models.news import News
from models.event import Event
from models.facility import Facility
from models.testimonial import Testimonial
from models.teacher import Teacher
from utils.helpers import slugify, unique_slug


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        settings = SiteSettings.get_settings()
        settings.school_name = 'Shree Nebula English School'
        settings.tagline = 'Inspiring Minds. Building Futures.'
        settings.phone = '+977 984-2055059'
        settings.email = 'nebula2053@gmail.com'
        settings.address = 'Urlabari-8, Rajghat, Morang, Koshi Province, Nepal'
        settings.facebook_url = 'https://www.facebook.com'
        settings.announcement = '📢 Admissions Open — ECD to Grade 10'
        settings.hero_title = 'Inspiring Minds. Building Futures.'
        settings.hero_description = 'A co-educational institution in Urlabari offering quality education from Early Childhood Development (ECD) to Grade 10, where students discover their potential and prepare for a better future.'
        settings.about_description = 'Shree Nebula English School is a private co-educational institution located in Urlabari-8, Rajghat, Morang district, Koshi Province, Nepal. We provide academic programs spanning from Early Childhood Development (ECD) up to Grade 10, with modern learning amenities including a dedicated computer lab, standard classrooms, and space for extracurricular activities. According to CEHRD IEMIS records, the school serves over 605 enrolled students.'
        settings.mission = 'To provide quality education and equal opportunities for all students from ECD to Grade 10.'
        settings.vision = 'To be a center of excellence in education serving the Urlabari and Morang community.'
        settings.principal_name = 'Principal'
        settings.principal_message = 'Dear Parents and Students,\n\nEducation is not only about academic achievement. It is about developing responsible, confident and compassionate individuals who can contribute positively to society.\n\nAt Shree Nebula English School, we strive to create an environment where every student is encouraged to learn, explore and grow from ECD through Grade 10.'
        settings.years = '25+'
        settings.students = '605+'
        settings.teachers = '40+'
        settings.board_result = '90%+'
        settings.footer_text = '© 2026 Shree Nebula English School. All Rights Reserved.'
        settings.office_hours = 'Sun - Fri: 9:00 AM - 4:00 PM'
        settings.map_embed = '<iframe src="https://www.google.com/maps?q=Urlabari+8+Rajghat+Morang+Nepal&output=embed" width="600" height="280" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>' 
        db.session.commit()
        print('Settings seeded (Shree Nebula English School).')

        if Facility.query.count() == 0:
            facilities = [
                ('Computer Lab', 'Dedicated computer lab for practical technical education and digital learning.', 'fas fa-desktop'),
                ('Science Lab', 'Science laboratory for hands-on experiments and practical learning.', 'fas fa-flask'),
                ('Library', 'Library with books and resources supporting students from ECD to Grade 10.', 'fas fa-book'),
                ('Classrooms', 'Standard classrooms designed for effective teaching and learning.', 'fas fa-chalkboard'),
                ('Playground', 'Outdoor space for sports, physical education and extracurricular activities.', 'fas fa-futbol'),
                ('Event Space', 'Space for extracurricular celebrations, programs and school events.', 'fas fa-theater-masks'),
                ('Smart Learning', 'Technology-supported teaching and learning environment.', 'fas fa-laptop'),
                ('First Aid', 'On-campus support for student health and safety.', 'fas fa-first-aid'),
            ]
            for title, desc, icon in facilities:
                db.session.add(Facility(title=title, description=desc, icon=icon, published=True))
            db.session.commit()
            print('Facilities seeded.')

        if Notice.query.count() == 0:
            notices = [
                ('Admission Open — ECD to Grade 10', 'Admissions are open for Early Childhood Development (ECD) through Grade 10. Contact +977 984-2055059 or visit the school office at Urlabari-8, Rajghat.', 'Admissions'),
                ('Annual Sports Meet', 'Annual sports meet will be held at the school ground. All students are encouraged to participate.', 'Events'),
                ('Examination Schedule', 'Examination schedules for secondary and higher secondary levels will be published on the notice board and website.', 'Exams'),
            ]
            for title, content, cat in notices:
                slug = unique_slug(Notice, slugify(title))
                db.session.add(Notice(title=title, slug=slug, content=content, category=cat, published=True))
            db.session.commit()
            print('Notices seeded.')

        if News.query.count() == 0:
            news_items = [
                ('Welcome to Shree Nebula English School', 'Shree Nebula English School in Urlabari-8, Rajghat, Morang continues to serve the community with quality education from ECD to Grade 10 for over 605 students.', 'Campus'),
                ('Computer Lab for Technical Education', 'Our dedicated computer lab supports practical technical education and helps students build digital skills for the future.', 'Facilities'),
                ('Extracurricular Activities & Celebrations', 'Students actively take part in dance performances, cultural programs and school activities shared with the community.', 'Activities'),
            ]
            for title, content, cat in news_items:
                slug = unique_slug(News, slugify(title))
                db.session.add(News(
                    title=title, slug=slug, excerpt=content[:150],
                    content=content, category=cat, author='Admin', published=True
                ))
            db.session.commit()
            print('News seeded.')

        if Event.query.count() == 0:
            today = date.today()
            events = [
                ('Annual Sports Meet', 'Join us for the annual sports meet featuring various sports and games for students.', today + timedelta(days=20), '9:00 AM', 'School Ground, Urlabari'),
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

        print('\nSeed data completed for Shree Nebula English School!')


if __name__ == '__main__':
    seed()
