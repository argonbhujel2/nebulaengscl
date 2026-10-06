from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from models import db
from models.admin import AdminUser
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
from forms.admin_forms import (NoticeForm, NewsForm, EventForm, GalleryForm,
                               FacilityForm, TeacherForm, TestimonialForm, SettingsForm)
from routes.auth import login_required, get_current_admin
from utils.helpers import slugify, unique_slug, save_upload
from datetime import date

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.context_processor
def inject_admin():
    from models.settings import SiteSettings
    try:
        site_settings = SiteSettings.get_settings()
    except Exception:
        site_settings = None
    return {
        'current_admin': get_current_admin(),
        'site_settings': site_settings,
    }


@admin_bp.route('/')
@login_required
def dashboard():
    stats = {
        'admissions': Admission.query.count(),
        'pending_admissions': Admission.query.filter_by(status='Pending').count(),
        'news': News.query.filter_by(published=True).count(),
        'events': Event.query.filter(Event.event_date >= date.today(), Event.published == True).count(),
        'gallery': Gallery.query.filter_by(published=True).count(),
        'messages': ContactMessage.query.filter_by(is_read=False).count(),
        'notices': Notice.query.filter_by(published=True).count(),
        'teachers': Teacher.query.filter_by(published=True).count(),
        'facilities': Facility.query.filter_by(published=True).count(),
        'testimonials': Testimonial.query.filter_by(published=True).count(),
    }
    recent_admissions = Admission.query.order_by(Admission.created_at.desc()).limit(5).all()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats,
                           recent_admissions=recent_admissions,
                           recent_messages=recent_messages)


# ─── Notices ───────────────────────────────────────────────
@admin_bp.route('/notices')
@login_required
def notices_list():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    query = Notice.query
    if q:
        query = query.filter(Notice.title.ilike(f'%{q}%'))
    pagination = query.order_by(Notice.created_at.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('admin/notices/list.html', notices=pagination.items, pagination=pagination, q=q)


@admin_bp.route('/notices/create', methods=['GET', 'POST'])
@login_required
def notices_create():
    form = NoticeForm()
    if form.validate_on_submit():
        slug = unique_slug(Notice, slugify(form.title.data))
        notice = Notice(
            title=form.title.data,
            slug=slug,
            content=form.content.data,
            category=form.category.data or 'General',
            published=form.published.data
        )
        if form.attachment.data:
            path = save_upload(form.attachment.data, 'notices', allow_attachments=True)
            if path:
                notice.attachment = path
        db.session.add(notice)
        db.session.commit()
        flash('Notice created successfully.', 'success')
        return redirect(url_for('admin.notices_list'))
    return render_template('admin/notices/form.html', form=form, title='Create Notice')


@admin_bp.route('/notices/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def notices_edit(id):
    notice = Notice.query.get_or_404(id)
    form = NoticeForm(obj=notice)
    if form.validate_on_submit():
        notice.title = form.title.data
        notice.slug = unique_slug(Notice, slugify(form.title.data), exclude_id=notice.id)
        notice.content = form.content.data
        notice.category = form.category.data or 'General'
        notice.published = form.published.data
        if form.attachment.data:
            path = save_upload(form.attachment.data, 'notices', allow_attachments=True)
            if path:
                notice.attachment = path
        db.session.commit()
        flash('Notice updated successfully.', 'success')
        return redirect(url_for('admin.notices_list'))
    return render_template('admin/notices/form.html', form=form, title='Edit Notice', notice=notice)


@admin_bp.route('/notices/<int:id>/delete', methods=['POST'])
@login_required
def notices_delete(id):
    notice = Notice.query.get_or_404(id)
    db.session.delete(notice)
    db.session.commit()
    flash('Notice deleted successfully.', 'success')
    return redirect(url_for('admin.notices_list'))


# ─── News ──────────────────────────────────────────────────
@admin_bp.route('/news')
@login_required
def news_list():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    query = News.query
    if q:
        query = query.filter(News.title.ilike(f'%{q}%'))
    pagination = query.order_by(News.created_at.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('admin/news/list.html', news_list=pagination.items, pagination=pagination, q=q)


@admin_bp.route('/news/create', methods=['GET', 'POST'])
@login_required
def news_create():
    form = NewsForm()
    if form.validate_on_submit():
        slug = unique_slug(News, slugify(form.title.data))
        item = News(
            title=form.title.data,
            slug=slug,
            excerpt=form.excerpt.data,
            content=form.content.data,
            category=form.category.data or 'General',
            author=form.author.data or 'Admin',
            published=form.published.data
        )
        if form.image.data:
            path = save_upload(form.image.data, 'news')
            if path:
                item.image = path
        if form.attachment.data:
            path = save_upload(form.attachment.data, 'news', allow_attachments=True)
            if path:
                item.attachment = path
        db.session.add(item)
        db.session.commit()
        flash('News created successfully.', 'success')
        return redirect(url_for('admin.news_list'))
    return render_template('admin/news/form.html', form=form, title='Create News')


@admin_bp.route('/news/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def news_edit(id):
    item = News.query.get_or_404(id)
    form = NewsForm(obj=item)
    if form.validate_on_submit():
        item.title = form.title.data
        item.slug = unique_slug(News, slugify(form.title.data), exclude_id=item.id)
        item.excerpt = form.excerpt.data
        item.content = form.content.data
        item.category = form.category.data or 'General'
        item.author = form.author.data or 'Admin'
        item.published = form.published.data
        if form.image.data:
            path = save_upload(form.image.data, 'news')
            if path:
                item.image = path
        if form.attachment.data:
            path = save_upload(form.attachment.data, 'news', allow_attachments=True)
            if path:
                item.attachment = path
        db.session.commit()
        flash('News updated successfully.', 'success')
        return redirect(url_for('admin.news_list'))
    return render_template('admin/news/form.html', form=form, title='Edit News', item=item)


@admin_bp.route('/news/<int:id>/delete', methods=['POST'])
@login_required
def news_delete(id):
    item = News.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('News deleted successfully.', 'success')
    return redirect(url_for('admin.news_list'))


# ─── Events ────────────────────────────────────────────────
@admin_bp.route('/events')
@login_required
def events_list():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    query = Event.query
    if q:
        query = query.filter(Event.title.ilike(f'%{q}%'))
    pagination = query.order_by(Event.event_date.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('admin/events/list.html', events=pagination.items, pagination=pagination, q=q)


@admin_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def events_create():
    form = EventForm()
    if form.validate_on_submit():
        slug = unique_slug(Event, slugify(form.title.data))
        event = Event(
            title=form.title.data,
            slug=slug,
            description=form.description.data,
            event_date=form.event_date.data,
            event_time=form.event_time.data,
            location=form.location.data,
            published=form.published.data
        )
        if form.image.data:
            path = save_upload(form.image.data, 'events')
            if path:
                event.image = path
        if form.attachment.data:
            path = save_upload(form.attachment.data, 'events', allow_attachments=True)
            if path:
                event.attachment = path
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully.', 'success')
        return redirect(url_for('admin.events_list'))
    return render_template('admin/events/form.html', form=form, title='Create Event')


@admin_bp.route('/events/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def events_edit(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.slug = unique_slug(Event, slugify(form.title.data), exclude_id=event.id)
        event.description = form.description.data
        event.event_date = form.event_date.data
        event.event_time = form.event_time.data
        event.location = form.location.data
        event.published = form.published.data
        if form.image.data:
            path = save_upload(form.image.data, 'events')
            if path:
                event.image = path
        if form.attachment.data:
            path = save_upload(form.attachment.data, 'events', allow_attachments=True)
            if path:
                event.attachment = path
        db.session.commit()
        flash('Event updated successfully.', 'success')
        return redirect(url_for('admin.events_list'))
    return render_template('admin/events/form.html', form=form, title='Edit Event', event=event)


@admin_bp.route('/events/<int:id>/delete', methods=['POST'])
@login_required
def events_delete(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully.', 'success')
    return redirect(url_for('admin.events_list'))


# ─── Gallery ───────────────────────────────────────────────
@admin_bp.route('/gallery')
@login_required
def gallery_list():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    query = Gallery.query
    if q:
        query = query.filter(Gallery.title.ilike(f'%{q}%'))
    pagination = query.order_by(Gallery.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/gallery/list.html', images=pagination.items, pagination=pagination, q=q)


@admin_bp.route('/gallery/create', methods=['GET', 'POST'])
@login_required
def gallery_create():
    form = GalleryForm()
    if form.validate_on_submit():
        if not form.image.data:
            flash('Image is required.', 'error')
            return render_template('admin/gallery/form.html', form=form, title='Add Image')
        path = save_upload(form.image.data, 'gallery')
        if not path:
            flash('Invalid image file.', 'error')
            return render_template('admin/gallery/form.html', form=form, title='Add Image')
        item = Gallery(
            title=form.title.data,
            image=path,
            category=form.category.data,
            alt_text=form.alt_text.data or form.title.data,
            published=form.published.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Image added successfully.', 'success')
        return redirect(url_for('admin.gallery_list'))
    return render_template('admin/gallery/form.html', form=form, title='Add Image')


@admin_bp.route('/gallery/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def gallery_edit(id):
    item = Gallery.query.get_or_404(id)
    form = GalleryForm(obj=item)
    if form.validate_on_submit():
        item.title = form.title.data
        item.category = form.category.data
        item.alt_text = form.alt_text.data or form.title.data
        item.published = form.published.data
        if form.image.data:
            path = save_upload(form.image.data, 'gallery')
            if path:
                item.image = path
        db.session.commit()
        flash('Image updated successfully.', 'success')
        return redirect(url_for('admin.gallery_list'))
    return render_template('admin/gallery/form.html', form=form, title='Edit Image', item=item)


@admin_bp.route('/gallery/<int:id>/delete', methods=['POST'])
@login_required
def gallery_delete(id):
    item = Gallery.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Image deleted successfully.', 'success')
    return redirect(url_for('admin.gallery_list'))


# ─── Facilities ────────────────────────────────────────────
@admin_bp.route('/facilities')
@login_required
def facilities_list():
    items = Facility.query.order_by(Facility.id).all()
    return render_template('admin/facilities/list.html', facilities=items)


@admin_bp.route('/facilities/create', methods=['GET', 'POST'])
@login_required
def facilities_create():
    form = FacilityForm()
    if form.validate_on_submit():
        item = Facility(
            title=form.title.data,
            description=form.description.data,
            icon=form.icon.data or 'fas fa-building',
            published=form.published.data
        )
        f = request.files.get('image')
        if f and getattr(f, 'filename', None):
            path = save_upload(f, 'facilities')
            if path:
                item.image = path
        db.session.add(item)
        db.session.commit()
        flash('Facility created successfully.', 'success')
        return redirect(url_for('admin.facilities_list'))
    return render_template('admin/facilities/form.html', form=form, title='Create Facility')


@admin_bp.route('/facilities/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def facilities_edit(id):
    item = Facility.query.get_or_404(id)
    form = FacilityForm(obj=item)
    form.image.data = None
    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        item.icon = form.icon.data or 'fas fa-building'
        item.published = form.published.data
        f = request.files.get('image')
        if f and getattr(f, 'filename', None):
            path = save_upload(f, 'facilities')
            if path:
                item.image = path
        db.session.commit()
        flash('Facility updated successfully.', 'success')
        return redirect(url_for('admin.facilities_list'))
    return render_template('admin/facilities/form.html', form=form, title='Edit Facility', item=item)


@admin_bp.route('/facilities/<int:id>/delete', methods=['POST'])
@login_required
def facilities_delete(id):
    item = Facility.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Facility deleted successfully.', 'success')
    return redirect(url_for('admin.facilities_list'))


# ─── Teachers ──────────────────────────────────────────────
@admin_bp.route('/teachers')
@login_required
def teachers_list():
    items = Teacher.query.order_by(Teacher.name).all()
    return render_template('admin/teachers/list.html', teachers=items)


@admin_bp.route('/teachers/create', methods=['GET', 'POST'])
@login_required
def teachers_create():
    form = TeacherForm()
    if form.validate_on_submit():
        item = Teacher(
            name=form.name.data,
            designation=form.designation.data,
            qualification=form.qualification.data,
            bio=form.bio.data,
            subject=form.subject.data,
            published=form.published.data
        )
        f = request.files.get('image')
        if f and getattr(f, 'filename', None):
            path = save_upload(f, 'teachers')
            if path:
                item.image = path
        db.session.add(item)
        db.session.commit()
        flash('Teacher added successfully.', 'success')
        return redirect(url_for('admin.teachers_list'))
    return render_template('admin/teachers/form.html', form=form, title='Add Teacher')


@admin_bp.route('/teachers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def teachers_edit(id):
    item = Teacher.query.get_or_404(id)
    form = TeacherForm(obj=item)
    form.image.data = None
    if form.validate_on_submit():
        item.name = form.name.data
        item.designation = form.designation.data
        item.qualification = form.qualification.data
        item.bio = form.bio.data
        item.subject = form.subject.data
        item.published = form.published.data
        f = request.files.get('image')
        if f and getattr(f, 'filename', None):
            path = save_upload(f, 'teachers')
            if path:
                item.image = path
        db.session.commit()
        flash('Teacher updated successfully.', 'success')
        return redirect(url_for('admin.teachers_list'))
    return render_template('admin/teachers/form.html', form=form, title='Edit Teacher', item=item)


@admin_bp.route('/teachers/<int:id>/delete', methods=['POST'])
@login_required
def teachers_delete(id):
    item = Teacher.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Teacher deleted successfully.', 'success')
    return redirect(url_for('admin.teachers_list'))


# ─── Testimonials ──────────────────────────────────────────
@admin_bp.route('/testimonials')
@login_required
def testimonials_list():
    items = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials/list.html', testimonials=items)


@admin_bp.route('/testimonials/create', methods=['GET', 'POST'])
@login_required
def testimonials_create():
    form = TestimonialForm()
    if form.validate_on_submit():
        item = Testimonial(
            name=form.name.data,
            role=form.role.data,
            message=form.message.data,
            rating=form.rating.data or 5,
            published=form.published.data
        )
        f = request.files.get('image')
        if f and getattr(f, 'filename', None):
            path = save_upload(f, 'testimonials')
            if path:
                item.image = path
        db.session.add(item)
        db.session.commit()
        flash('Testimonial created successfully.', 'success')
        return redirect(url_for('admin.testimonials_list'))
    return render_template('admin/testimonials/form.html', form=form, title='Add Testimonial')


@admin_bp.route('/testimonials/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def testimonials_edit(id):
    item = Testimonial.query.get_or_404(id)
    form = TestimonialForm(obj=item)
    form.image.data = None
    if form.validate_on_submit():
        item.name = form.name.data
        item.role = form.role.data
        item.message = form.message.data
        item.rating = form.rating.data or 5
        item.published = form.published.data
        f = request.files.get('image')
        if f and getattr(f, 'filename', None):
            path = save_upload(f, 'testimonials')
            if path:
                item.image = path
        db.session.commit()
        flash('Testimonial updated successfully.', 'success')
        return redirect(url_for('admin.testimonials_list'))
    return render_template('admin/testimonials/form.html', form=form, title='Edit Testimonial', item=item)


@admin_bp.route('/testimonials/<int:id>/delete', methods=['POST'])
@login_required
def testimonials_delete(id):
    item = Testimonial.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Testimonial deleted successfully.', 'success')
    return redirect(url_for('admin.testimonials_list'))


# ─── Admissions ────────────────────────────────────────────
@admin_bp.route('/admissions')
@login_required
def admissions_list():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    q = request.args.get('q', '')
    query = Admission.query
    if status:
        query = query.filter_by(status=status)
    if q:
        query = query.filter(
            db.or_(
                Admission.student_name.ilike(f'%{q}%'),
                Admission.application_id.ilike(f'%{q}%'),
                Admission.guardian_name.ilike(f'%{q}%')
            )
        )
    pagination = query.order_by(Admission.created_at.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('admin/admissions/list.html', admissions=pagination.items,
                           pagination=pagination, status=status, q=q)


@admin_bp.route('/admissions/<int:id>')
@login_required
def admissions_view(id):
    item = Admission.query.get_or_404(id)
    return render_template('admin/admissions/view.html', admission=item)


@admin_bp.route('/admissions/<int:id>/status', methods=['POST'])
@login_required
def admissions_status(id):
    item = Admission.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ('Pending', 'Reviewed', 'Approved', 'Rejected'):
        item.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}.', 'success')
    return redirect(url_for('admin.admissions_view', id=id))


@admin_bp.route('/admissions/<int:id>/delete', methods=['POST'])
@login_required
def admissions_delete(id):
    item = Admission.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Application deleted successfully.', 'success')
    return redirect(url_for('admin.admissions_list'))


# ─── Messages ──────────────────────────────────────────────
@admin_bp.route('/messages')
@login_required
def messages_list():
    page = request.args.get('page', 1, type=int)
    pagination = ContactMessage.query.order_by(ContactMessage.created_at.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('admin/messages/list.html', messages=pagination.items, pagination=pagination)


@admin_bp.route('/messages/<int:id>')
@login_required
def messages_view(id):
    msg = ContactMessage.query.get_or_404(id)
    if not msg.is_read:
        msg.is_read = True
        db.session.commit()
    return render_template('admin/messages/view.html', message=msg)


@admin_bp.route('/messages/<int:id>/delete', methods=['POST'])
@login_required
def messages_delete(id):
    msg = ContactMessage.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message deleted successfully.', 'success')
    return redirect(url_for('admin.messages_list'))


# ─── Settings ──────────────────────────────────────────────
@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    from utils.helpers import is_file_upload
    settings_obj = SiteSettings.get_settings()
    form = SettingsForm(obj=settings_obj)
    # Clear FileFields so existing path strings are not treated as uploads
    form.logo.data = None
    form.favicon.data = None
    form.principal_image.data = None
    form.hero_image.data = None
    form.about_image.data = None

    if request.method == 'POST' and form.validate_on_submit():
        for field in ['school_name', 'tagline', 'phone', 'email', 'address',
                      'facebook_url', 'instagram_url', 'youtube_url',
                      'hero_title', 'hero_description', 'principal_name',
                      'principal_message', 'about_description', 'mission',
                      'vision', 'announcement', 'footer_text',
                      'years', 'students', 'teachers', 'board_result', 'office_hours', 'map_embed']:
            setattr(settings_obj, field, getattr(form, field).data)

        for form_name, attr in [
            ('logo', 'logo'),
            ('favicon', 'favicon'),
            ('principal_image', 'principal_image'),
            ('hero_image', 'hero_image'),
            ('about_image', 'about_image'),
        ]:
            f = request.files.get(form_name)
            if is_file_upload(f):
                path = save_upload(f, 'settings')
                if path:
                    setattr(settings_obj, attr, path)

        db.session.commit()
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('admin.settings'))
    elif request.method == 'POST':
        for err in form.errors.values():
            for e in err:
                flash(e, 'error')

    return render_template('admin/settings/form.html', form=form, settings=settings_obj)


# ─── Profile ───────────────────────────────────────────────
@admin_bp.route('/profile')
@login_required
def profile():
    from flask import redirect, url_for, flash
    admin = get_current_admin()
    if not admin:
        flash('Session expired. Please log in again.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('admin/profile.html', admin=admin)
