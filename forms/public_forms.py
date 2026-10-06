from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TelField, EmailField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp


class AdmissionForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired(), Length(min=2, max=150)])
    date_of_birth = DateField('Date of Birth', validators=[Optional()], format='%Y-%m-%d')
    gender = SelectField('Gender', choices=[
        ('', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    grade = SelectField('Grade Applying For', choices=[
        ('', 'Select Grade'),
        ('ECD', 'ECD'),
        ('Nursery', 'Nursery'),
        ('KG', 'KG'),
        ('Grade 1', 'Grade 1'),
        ('Grade 2', 'Grade 2'),
        ('Grade 3', 'Grade 3'),
        ('Grade 4', 'Grade 4'),
        ('Grade 5', 'Grade 5'),
        ('Grade 6', 'Grade 6'),
        ('Grade 7', 'Grade 7'),
        ('Grade 8', 'Grade 8'),
        ('Grade 9', 'Grade 9'),
        ('Grade 10', 'Grade 10'),
    ], validators=[DataRequired()])
    guardian_name = StringField('Parent/Guardian Name', validators=[DataRequired(), Length(min=2, max=150)])
    phone = TelField('Phone', validators=[DataRequired(), Length(min=7, max=30)])
    email = EmailField('Email', validators=[Optional(), Email(), Length(max=120)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=500)])
    previous_school = StringField('Previous School', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Message', validators=[Optional(), Length(max=1000)])


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = TelField('Phone', validators=[Optional(), Length(max=30)])
    subject = StringField('Subject', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)])
