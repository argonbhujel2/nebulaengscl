from datetime import datetime
from models import db


class SiteSettings(db.Model):
    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(200), default='Shree Nebula English School')
    tagline = db.Column(db.String(200), default='Inspiring Minds. Building Futures.')
    logo = db.Column(db.String(255))
    favicon = db.Column(db.String(255))
    phone = db.Column(db.String(50), default='+977 984-2055059')
    email = db.Column(db.String(120), default='nebula2053@gmail.com')
    address = db.Column(db.String(300), default='Urlabari-8, Rajghat, Morang, Koshi Province, Nepal')
    facebook_url = db.Column(db.String(255), default='https://www.facebook.com')
    instagram_url = db.Column(db.String(255))
    youtube_url = db.Column(db.String(255))
    hero_title = db.Column(db.String(300), default='Inspiring Minds. Building Futures.')
    hero_description = db.Column(db.Text, default='A co-educational institution in Urlabari offering quality education from Early Childhood Development (ECD) to Grade 10, where students discover their potential and prepare for a better future.')
    hero_image = db.Column(db.String(255))
    about_image = db.Column(db.String(255))
    principal_name = db.Column(db.String(100), default='Principal')
    principal_message = db.Column(db.Text, default='Dear Parents and Students,\n\nEducation is not only about academic achievement. It is about developing responsible, confident and compassionate individuals who can contribute positively to society.\n\nAt Shree Nebula English School, we strive to create an environment where every student is encouraged to learn, explore and grow from ECD through Grade 10.')
    principal_image = db.Column(db.String(255))
    about_description = db.Column(db.Text, default='Shree Nebula English School is a private co-educational institution located in Urlabari-8, Rajghat, Morang district, Koshi Province, Nepal. We provide academic programs spanning from Early Childhood Development (ECD) up to Grade 10, with modern learning amenities including a dedicated computer lab, standard classrooms, and space for extracurricular activities.')
    mission = db.Column(db.Text, default='To provide quality education and equal opportunities for all students from ECD to Grade 10.')
    vision = db.Column(db.Text, default='To be a center of excellence in education serving the Urlabari and Morang community.')
    announcement = db.Column(db.String(300), default='📢 Admissions Open — ECD to Grade 10')
    footer_text = db.Column(db.String(300), default='© 2026 Shree Nebula English School. All Rights Reserved.')
    years = db.Column(db.String(20), default='25+')
    students = db.Column(db.String(20), default='605+')
    teachers = db.Column(db.String(20), default='40+')
    board_result = db.Column(db.String(20), default='90%+')
    office_hours = db.Column(db.String(100), default='Sun - Fri: 9:00 AM - 4:00 PM')
    map_embed = db.Column(db.Text, default='')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def get_settings():
        settings = SiteSettings.query.first()
        if not settings:
            settings = SiteSettings()
            db.session.add(settings)
            db.session.commit()
        return settings

    def __repr__(self):
        return f'<SiteSettings {self.school_name}>'
