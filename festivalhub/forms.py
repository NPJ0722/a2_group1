from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    IntegerField,
    FloatField,
    SubmitField
)
from wtforms.fields import DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, Regexp
from flask_wtf.file import FileField, FileAllowed


class LoginForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Continue')


class RegisterForm(FlaskForm):
    first_name = StringField(
        'First Name',
        validators=[DataRequired(), Length(max=80)]
    )

    last_name = StringField(
        'Last Name',
        validators=[DataRequired(), Length(max=80)]
    )

    phone = StringField(
        'Phone Number',
        validators=[
            DataRequired(),
            Regexp(r'^04\d{8}$', message='Please enter a valid Australian mobile number, e.g. 04xxxxxxxx.')
        ]
    )   

    email = StringField(
        'Email Address',
        validators=[
            DataRequired(),
            Email(),
            Regexp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', message='Please enter a valid email address, e.g. name@example.com.'),
            Length(max=120)
        ]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=255)]
    )

    street_address = StringField(
        'Street Address',
        validators=[DataRequired(), Length(max=255)]
    )

    submit = SubmitField('Create Account & Continue')


class EventForm(FlaskForm):
    name = StringField(
        'Event Name',
        validators=[DataRequired(), Length(max=150)]
    )

    category = SelectField(
        'Category',
        choices=[
            ('Music Festival', 'Music Festival'),
            ('Indie', 'Indie'),
            ('Pop', 'Pop'),
            ('Hip Hop', 'Hip Hop'),
            ('Accessible Festival', 'Accessible Festival'),
            ('Tour', 'Tour')
        ],
        validators=[DataRequired()]
    )

    date = DateField(
        'Event Date',
        validators=[DataRequired()],
        format='%Y-%m-%d'
    )

    start_time = TimeField(
        'Start Time',
        validators=[Optional()],
        format='%H:%M'
    )

    end_time = TimeField(
        'End Time',
        validators=[Optional()],
        format='%H:%M'
    )

    description = TextAreaField(
        'Description',
        validators=[DataRequired()]
    )

    venue = StringField(
        'Venue Name',
        validators=[DataRequired(), Length(max=150)]
    )

    location = StringField(
        'Location',
        validators=[DataRequired(), Length(max=150)]
    )

    artist_lineup = TextAreaField(
        'Artist / Line-up',
        validators=[Optional()]
    )

    acknowledgement_type = SelectField(
        'Acknowledgement Type',
        choices=[
            ('No Acknowledgement of Country', 'No Acknowledgement of Country'),
            ('Generic Acknowledgement', 'Generic Acknowledgement'),
            ('Enhanced Acknowledgement', 'Enhanced Acknowledgement')
        ],
        validators=[DataRequired()]
    )

    traditional_custodians = StringField(
        'Traditional Custodians',
        validators=[Optional(), Length(max=150)]
    )

    acknowledgement_statement = TextAreaField(
        'Acknowledgement Statement',
        validators=[Optional()]
    )

    ticket_type = SelectField(
        'Ticket Type',
        choices=[
            ('General Admission', 'General Admission'),
            ('VIP Pass', 'VIP Pass'),
            ('Student Ticket', 'Student Ticket')
        ],
        validators=[DataRequired()]
    )

    tickets_available = IntegerField(
        'Tickets Available',
        validators=[DataRequired(), NumberRange(min=0)]
    )

    price = FloatField(
        'Ticket Price',
        validators=[
            DataRequired(message='Please enter a valid number for ticket price.'),
            NumberRange(min=0, message='Ticket price must be 0 or above.')
        ]
    )

    image = FileField(
        'Upload Event Image',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')
        ]
    )

    submit = SubmitField('Create Event')


class BookingForm(FlaskForm):
    ticket_quantity = IntegerField(
        'Number of Tickets',
        validators=[DataRequired(), NumberRange(min=1, max=10)]
    )

    ticket_type = SelectField(
        'Ticket Type',
        choices=[
            ('General Admission', 'General Admission'),
            ('VIP Ticket', 'VIP Ticket'),
            ('Student Ticket', 'Student Ticket')
        ],
        validators=[DataRequired()]
    )

    notes = TextAreaField(
        'Additional Notes',
        validators=[Optional()]
    )

    submit = SubmitField('Confirm Booking')


class CommentForm(FlaskForm):
    user_name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=120)]
    )

    comment_text = TextAreaField(
        'Comment',
        validators=[DataRequired()]
    )

    submit = SubmitField('Post Comment')