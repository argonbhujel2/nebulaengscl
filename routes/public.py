from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, make_response
from models import db
from models.notice import Notice
from models.news import News
from models.event import Event
from models.gallery import Gallery
from models.facility import Facility
from models.teacher import Teacher
from models.admission import Admission
from models.testimonial import Testimonial
from models.contact import ContactMessage
from models.settings import SiteSettings
from forms.public_forms import AdmissionForm, ContactForm
from utils.helpers import generate_application_id
from datetime import datetime, date

public_bp = Blueprint('public', __name__)


def get_settings():
    try:
        return SiteSettings.get_settings()
    except Exception as e:
        print(f'get_settings error: {e}')
        try:
            from models import db
            db.session.rollback()
        except Exception:
            pass
        # Minimal fallback so templates never crash
        return SiteSettings(
            school_name='Shree Nebula English School',
            tagline='Inspiring Minds. Building Futures.',
        )




@public_bp.route('/')
def index():
    settings = get_settings()
    notices = Notice.query.filter_by(published=True).order_by(Notice.created_at.desc()).limit(3).all()
    news_list = News.query.filter_by(published=True).order_by(News.published_at.desc()).limit(3).all()
    events = Event.query.filter_by(published=True).filter(Event.event_date >= date.today()).order_by(Event.event_date.asc()).limit(3).all()
    gallery = Gallery.query.filter_by(published=True).order_by(Gallery.created_at.desc()).limit(8).all()
    facilities = Facility.query.filter_by(published=True).order_by(Facility.id).limit(8).all()
    testimonials = Testimonial.query.filter_by(published=True).order_by(Testimonial.created_at.desc()).limit(6).all()
    teachers = Teacher.query.filter_by(published=True).limit(4).all()
    return render_template('public/index.html',
                           notices=notices,
                           news_list=news_list,
                           events=events,
                           gallery=gallery,
                           facilities=facilities,
                           testimonials=testimonials,
                           teachers=teachers)


@public_bp.route('/about')
def about():
    teachers = Teacher.query.filter_by(published=True).all()
    return render_template('public/about.html', teachers=teachers)


@public_bp.route('/academics')
def academics():
    return render_template('public/academics.html')


@public_bp.route('/admissions', methods=['GET', 'POST'])
def admissions():
    form = AdmissionForm()
    if form.validate_on_submit():
        app_id = generate_application_id()
        admission = Admission(
            application_id=app_id,
            student_name=form.student_name.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            grade=form.grade.data,
            guardian_name=form.guardian_name.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data,
            previous_school=form.previous_school.data,
            message=form.message.data,
            status='Pending'
        )
        db.session.add(admission)
        db.session.commit()
        flash(f'Application submitted successfully! Your Application ID is {app_id}. We will contact you soon.', 'success')
        return redirect(url_for('public.admissions'))
    return render_template('public/admissions.html', form=form)


@public_bp.route('/facilities')
def facilities():
    facilities_list = Facility.query.filter_by(published=True).order_by(Facility.id).all()
    return render_template('public/facilities.html', facilities=facilities_list)


@public_bp.route('/gallery')
def gallery():
    category = request.args.get('category', 'All')
    query = Gallery.query.filter_by(published=True)
    if category and category != 'All':
        query = query.filter_by(category=category)
    images = query.order_by(Gallery.created_at.desc()).all()
    categories = ['All', 'Campus', 'Classroom', 'Sports', 'Events', 'Activities', 'Laboratory']
    return render_template('public/gallery.html', images=images, categories=categories, active_category=category)


@public_bp.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    pagination = News.query.filter_by(published=True).order_by(News.published_at.desc()).paginate(page=page, per_page=9, error_out=False)
    return render_template('public/news.html', news_list=pagination.items, pagination=pagination)


@public_bp.route('/news/<slug>')
def news_detail(slug):
    item = News.query.filter_by(slug=slug, published=True).first_or_404()
    related = News.query.filter(News.published == True, News.id != item.id).order_by(News.published_at.desc()).limit(3).all()
    return render_template('public/news_detail.html', news=item, related=related)


@public_bp.route('/events')
def events():
    page = request.args.get('page', 1, type=int)
    pagination = Event.query.filter_by(published=True).order_by(Event.event_date.desc()).paginate(page=page, per_page=9, error_out=False)
    return render_template('public/events.html', events=pagination.items, pagination=pagination)


@public_bp.route('/events/<int:event_id>')
def event_detail(event_id):
    event = Event.query.filter_by(id=event_id, published=True).first_or_404()
    return render_template('public/event_detail.html', event=event)


@public_bp.route('/notices')
def notices():
    page = request.args.get('page', 1, type=int)
    pagination = Notice.query.filter_by(published=True).order_by(Notice.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('public/notices.html', notices=pagination.items, pagination=pagination)


@public_bp.route('/notices/<slug>')
def notice_detail(slug):
    notice = Notice.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template('public/notice_detail.html', notice=notice)


@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(msg)
        db.session.commit()
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('public.contact'))
    return render_template('public/contact.html', form=form)


@public_bp.route('/sitemap.xml')
def sitemap():
    pages = [
        url_for('public.index', _external=True),
        url_for('public.about', _external=True),
        url_for('public.academics', _external=True),
        url_for('public.admissions', _external=True),
        url_for('public.facilities', _external=True),
        url_for('public.gallery', _external=True),
        url_for('public.news', _external=True),
        url_for('public.events', _external=True),
        url_for('public.contact', _external=True),
        url_for('public.notices', _external=True),
    ]
    news_items = News.query.filter_by(published=True).all()
    for n in news_items:
        pages.append(url_for('public.news_detail', slug=n.slug, _external=True))
    events_items = Event.query.filter_by(published=True).all()
    for e in events_items:
        pages.append(url_for('public.event_detail', event_id=e.id, _external=True))

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for page in pages:
        xml.append(f'  <url><loc>{page}</loc></url>')
    xml.append('</urlset>')
    response = make_response('\n'.join(xml))
    response.headers['Content-Type'] = 'application/xml'
    return response


@public_bp.route('/robots.txt')
def robots():
    content = """User-agent: *
Allow: /
Disallow: /admin/
Sitemap: /sitemap.xml
"""
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain'
    return response
