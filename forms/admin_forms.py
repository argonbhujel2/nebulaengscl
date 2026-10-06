from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, PasswordField, SelectField
from wtforms import DateField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, NumberRange


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class NoticeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = StringField('Category', validators=[Optional(), Length(max=100)], default='General')
    attachment = FileField('Attachment', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'zip', 'jpg', 'jpeg', 'png', 'webp', 'gif'], 'Documents and images only!')
    ])
    published = BooleanField('Published', default=True)


class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    excerpt = TextAreaField('Excerpt', validators=[Optional(), Length(max=500)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = StringField('Category', validators=[Optional(), Length(max=100)], default='General')
    author = StringField('Author', validators=[Optional(), Length(max=100)], default='Admin')
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')
    ])
    attachment = FileField('Attachment (PDF, DOC, etc.)', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'zip', 'jpg', 'jpeg', 'png', 'webp'], 'Documents and images only!')
    ])
    published = BooleanField('Published', default=True)


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    event_date = DateField('Event Date', validators=[DataRequired()], format='%Y-%m-%d')
    event_time = StringField('Event Time', validators=[Optional(), Length(max=50)])
    location = StringField('Location', validators=[Optional(), Length(max=200)])
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')
    ])
    attachment = FileField('Attachment (PDF, DOC, etc.)', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'zip', 'jpg', 'jpeg', 'png', 'webp'], 'Documents and images only!')
    ])
    published = BooleanField('Published', default=True)


class GalleryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    category = SelectField('Category', choices=[
        ('Campus', 'Campus'),
        ('Classroom', 'Classroom'),
        ('Sports', 'Sports'),
        ('Events', 'Events'),
        ('Activities', 'Activities'),
        ('Laboratory', 'Laboratory'),
    ], validators=[DataRequired()])
    alt_text = StringField('Alt Text', validators=[Optional(), Length(max=255)])
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')
    ])
    published = BooleanField('Published', default=True)


class FacilityForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description', validators=[Optional()])
    icon = StringField('Icon Class', validators=[Optional(), Length(max=100)], default='fas fa-building')
    image = FileField('Image')
    published = BooleanField('Published', default=True)


class TeacherForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    designation = StringField('Designation', validators=[Optional(), Length(max=100)])
    qualification = StringField('Qualification', validators=[Optional(), Length(max=200)])
    bio = TextAreaField('Bio', validators=[Optional()])
    subject = StringField('Subject', validators=[Optional(), Length(max=100)])
    image = FileField('Image')
    published = BooleanField('Published', default=True)


class TestimonialForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    role = StringField('Role', validators=[Optional(), Length(max=100)])
    message = TextAreaField('Message', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[Optional(), NumberRange(min=1, max=5)], default=5)
    image = FileField('Image')
    published = BooleanField('Published', default=True)


class SettingsForm(FlaskForm):
    school_name = StringField('School Name', validators=[DataRequired(), Length(max=200)])
    tagline = StringField('Tagline', validators=[Optional(), Length(max=200)])
    phone = StringField('Phone', validators=[Optional(), Length(max=50)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    address = StringField('Address', validators=[Optional(), Length(max=300)])
    facebook_url = StringField('Facebook URL', validators=[Optional(), Length(max=255)])
    instagram_url = StringField('Instagram URL', validators=[Optional(), Length(max=255)])
    youtube_url = StringField('YouTube URL', validators=[Optional(), Length(max=255)])
    hero_title = StringField('Hero Title', validators=[Optional(), Length(max=300)])
    hero_description = TextAreaField('Hero Description', validators=[Optional()])
    principal_name = StringField('Principal Name', validators=[Optional(), Length(max=100)])
    principal_message = TextAreaField('Principal Message', validators=[Optional()])
    about_description = TextAreaField('About Description', validators=[Optional()])
    mission = TextAreaField('Mission', validators=[Optional()])
    vision = TextAreaField('Vision', validators=[Optional()])
    announcement = StringField('Announcement Bar', validators=[Optional(), Length(max=300)])
    footer_text = StringField('Footer Text', validators=[Optional(), Length(max=300)])
    years = StringField('Years of Excellence', validators=[Optional(), Length(max=20)])
    students = StringField('Students Count', validators=[Optional(), Length(max=20)])
    teachers = StringField('Teachers Count', validators=[Optional(), Length(max=20)])
    board_result = StringField('Board Results', validators=[Optional(), Length(max=20)])
    office_hours = StringField('Office Hours', validators=[Optional(), Length(max=100)])
    map_embed = TextAreaField('Google Maps Embed (iframe HTML or embed URL)', validators=[Optional()])
    logo = FileField('Logo')
    favicon = FileField('Favicon')
    principal_image = FileField('Principal Image')
    hero_image = FileField('Hero Image')
    about_image = FileField('About Image')
