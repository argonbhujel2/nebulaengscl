import os
import re
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import current_app

IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
ATTACHMENT_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'webp', 'gif',
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'txt', 'zip', 'rar', 'csv'
}


def allowed_file(filename, extensions=None):
    if extensions is None:
        extensions = current_app.config.get('ALLOWED_EXTENSIONS', IMAGE_EXTENSIONS)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


def is_file_upload(file):
    if file is None:
        return False
    if isinstance(file, str):
        return False
    if not isinstance(file, FileStorage):
        return False
    if not getattr(file, 'filename', None):
        return False
    if not str(file.filename).strip():
        return False
    return True


def is_image_filename(filename):
    if not filename or '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS


def save_upload(file, subfolder='general', allow_attachments=False):
    """Save upload. Images use Cloudinary when configured; otherwise local static/uploads."""
    if not is_file_upload(file):
        return None

    exts = ATTACHMENT_EXTENSIONS if allow_attachments else IMAGE_EXTENSIONS
    if not allowed_file(file.filename, exts):
        return None

    # Cloudinary for images (and optional for all if CLOUDINARY_ALL=1)
    use_cloudinary = is_image_filename(file.filename) or os.environ.get('CLOUDINARY_ALL') == '1'
    if use_cloudinary:
        try:
            from utils.cloudinary_upload import cloudinary_enabled, upload_to_cloudinary
            if cloudinary_enabled():
                # Need to reset stream for local fallback
                url = upload_to_cloudinary(file, folder=subfolder)
                if url:
                    return url  # full https URL
                # rewind if possible for local save
                try:
                    file.stream.seek(0)
                except Exception:
                    pass
        except Exception:
            try:
                file.stream.seek(0)
            except Exception:
                pass

    # Local filesystem
    original = secure_filename(file.filename)
    ext = original.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"

    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    try:
        os.makedirs(upload_dir, exist_ok=True)
    except OSError:
        # Read-only filesystem (e.g. Vercel without Cloudinary configured)
        raise RuntimeError(
            'Cannot save uploads on this host. Configure CLOUDINARY_URL '
            '(or CLOUDINARY_CLOUD_NAME / API_KEY / API_SECRET) for production.'
        ) from None

    filepath = os.path.join(upload_dir, unique_name)
    file.save(filepath)
    # If UPLOAD_FOLDER is under /tmp, still return a path relative to static expectation
    # so media_url / templates work when possible; Cloudinary is preferred in production.
    return f"uploads/{subfolder}/{unique_name}"


def media_url(path):
    """Return URL for a stored path (Cloudinary full URL or local static path)."""
    if not path:
        return ''
    path = str(path)
    if path.startswith('http://') or path.startswith('https://'):
        return path
    try:
        from flask import url_for
        return url_for('static', filename=path)
    except Exception:
        return f'/static/{path.lstrip("/")}' 


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text[:200]


def generate_application_id():
    now = datetime.utcnow()
    return f"APP-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"


def unique_slug(model, base_slug, exclude_id=None):
    slug = base_slug
    counter = 1
    while True:
        query = model.query.filter_by(slug=slug)
        if exclude_id:
            query = query.filter(model.id != exclude_id)
        if not query.first():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


def is_image_file(path):
    if not path:
        return False
    if path.startswith('http'):
        return any(path.lower().endswith(f'.{e}') or f'.{e}?' in path.lower() for e in IMAGE_EXTENSIONS)
    ext = path.rsplit('.', 1)[-1].lower() if '.' in path else ''
    return ext in IMAGE_EXTENSIONS
