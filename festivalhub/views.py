from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from . import db
from .models import User, Event, Booking, Comment
from .forms import LoginForm, RegisterForm, EventForm, BookingForm, CommentForm
import os
from werkzeug.utils import secure_filename
from sqlalchemy import func

mainbp = Blueprint('main', __name__)


def user_can_manage_event(event):
    if not current_user.is_authenticated:
        return False

    if event.creator_id is None:
        return True

    return event.creator_id == current_user.id


def fill_event_from_form(event, form):
    event.name = form.name.data
    event.category = form.category.data
    event.date = request.form['date']
    event.start_time = request.form['start_time']
    event.end_time = request.form['end_time']
    event.description = form.description.data
    event.venue = form.venue.data
    event.location = form.location.data
    event.artist_lineup = form.artist_lineup.data
    event.ticket_type = form.ticket_type.data
    event.tickets_available = form.tickets_available.data
    event.price = form.price.data

    # Status is controlled by the system, not by the create/update form
    if not event.status:
        event.status = 'Open'

    # Save uploaded image file into static/img and store filename in DB
    if form.image.data:
        filename = secure_filename(form.image.data.filename)

        upload_path = os.path.join(
            current_app.root_path,
            'static',
            'img',
            filename
        )

        form.image.data.save(upload_path)
        event.image = filename

    event.acknowledgement_type = form.acknowledgement_type.data
    event.traditional_custodians = form.traditional_custodians.data
    event.acknowledgement_statement = form.acknowledgement_statement.data

def populate_event_form(form, event):
    form.name.data = event.name
    form.category.data = event.category
    form.description.data = event.description
    form.venue.data = event.venue
    form.location.data = event.location
    form.artist_lineup.data = event.artist_lineup
    form.ticket_type.data = event.ticket_type
    form.tickets_available.data = event.tickets_available
    form.price.data = event.price
    form.image.data = event.image
    form.acknowledgement_type.data = event.acknowledgement_type
    form.traditional_custodians.data = event.traditional_custodians
    form.acknowledgement_statement.data = event.acknowledgement_statement

    try:
        form.date.data = datetime.datetime.strptime(event.date, '%Y-%m-%d').date()
    except Exception:
        form.date.data = None

    try:
        form.start_time.data = datetime.datetime.strptime(event.start_time, '%H:%M').time()
    except Exception:
        form.start_time.data = None

    try:
        form.end_time.data = datetime.datetime.strptime(event.end_time, '%H:%M').time()
    except Exception:
        form.end_time.data = None


@mainbp.route('/')
def index():
    selected_category = request.args.get('category', 'All')

    if selected_category == 'All':
        events = Event.query.all()
    else:
        events = Event.query.filter(
            Event.category.ilike(f'%{selected_category}%')
        ).all()

    return render_template(
        'index.html',
        events=events,
        selected_category=selected_category
    )


@mainbp.route('/details', defaults={'event_id': None}, methods=['GET', 'POST'])
@mainbp.route('/details/<int:event_id>', methods=['GET', 'POST'])
def details(event_id):
    if event_id is None:
        event = Event.query.first()
    else:
        event = Event.query.get_or_404(event_id)

    comment_form = CommentForm()

    if request.method == 'POST':

        if not current_user.is_authenticated and request.form.get('guest_confirm') != '1':
            return redirect(url_for('main.login', next=url_for('main.details', event_id=event.id)))

        new_comment = Comment(
            event_id=event.id,
            user_name=request.form['user_name'],
            comment_text=request.form['comment_text']
        )

        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('main.details', event_id=event.id))

    comments = Comment.query.filter_by(event_id=event.id).all()

    return render_template(
        'event-details.html',
        event=event,
        comment_form=comment_form,
        comments=comments,
        can_manage_event=user_can_manage_event(event)
    )


@mainbp.route('/delete-comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    event_id = comment.event_id

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('main.details', event_id=event_id))


@mainbp.route('/create', methods=['GET', 'POST'])
def create_event():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login', next=url_for('main.create_event')))

    form = EventForm()

    if form.validate_on_submit():
        new_event = Event(
            creator_id=current_user.id
        )

        fill_event_from_form(new_event, form)

        new_event.status = 'Open'

        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for('main.details', event_id=new_event.id))

    return render_template(
        'create-update-event.html',
        form=form,
        page_title='Create Event',
        submit_label='Create Event',
        is_update=False
    )


@mainbp.route('/update/<int:event_id>', methods=['GET', 'POST'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)

    if not user_can_manage_event(event):
        return redirect(url_for('main.details', event_id=event.id))

    form = EventForm()

    if request.method == 'POST':
        fill_event_from_form(event, form)
        db.session.commit()

        return redirect(url_for('main.details', event_id=event.id))

    populate_event_form(form, event)

    return render_template(
        'create-update-event.html',
        form=form,
        event=event,
        page_title='Update Event',
        submit_label='Update Event',
        is_update=True
    )

@mainbp.route('/inactive-event/<int:event_id>')
@login_required
def inactive_event(event_id):

    event = Event.query.get_or_404(event_id)

    event.status = 'Inactive'

    db.session.commit()

    return redirect(url_for('main.details', event_id=event.id))

@mainbp.route('/cancel-event/<int:event_id>', methods=['POST'])
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)

    if not user_can_manage_event(event):
        return redirect(url_for('main.details', event_id=event.id))

    event.status = 'Cancelled'
    db.session.commit()

    return redirect(url_for('main.details', event_id=event.id))


@mainbp.route('/booking')
def booking_select():
    events = Event.query.all()
    show_login_modal = request.args.get('login_required') == '1'
    return render_template(
        'booking-select.html',
        events=events,
        show_login_modal=show_login_modal
    )

@mainbp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    booking.status = 'Cancelled'
    db.session.commit()

    return redirect(url_for('main.bookings'))

@mainbp.route('/booking/<int:event_id>', methods=['GET', 'POST'])
def booking(event_id):

    form = BookingForm()
    event = Event.query.get_or_404(event_id)

    if event.status == 'Cancelled':
        return redirect(url_for('main.details', event_id=event.id))

    if request.method == 'POST':
        ticket_quantity = int(request.form['ticket_quantity'])

        if ticket_quantity > event.tickets_available:
            return render_template('booking.html', form=form, event=event)

        ticket_price = event.price
        booking_fee = 8.00
        total_price = (ticket_price * ticket_quantity) + booking_fee

        new_booking = Booking(
            user_id=current_user.id,
            event_id=event.id,
            ticket_quantity=ticket_quantity,
            ticket_price=ticket_price,
            booking_fee=booking_fee,
            total_price=total_price,
            status='Confirmed'
        )

        event.tickets_available -= ticket_quantity

        if event.tickets_available == 0:
            event.status = 'Sold out'

        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('main.bookings'))

    return render_template('booking.html', form=form, event=event)


@mainbp.route('/bookings')
def bookings():
    bookings = Booking.query.all()
    return render_template('booking-history.html', bookings=bookings)


@mainbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()
    next_page = request.args.get('next', '/')
    error_message = None

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'login':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(next_page)
            else:
                error_message = "Incorrect email or password."

        elif form_type == 'register':
            email = request.form.get('email')
            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                error_message = "This email is already registered."
            else:
                new_user = User(
                    first_name=request.form.get('first_name'),
                    last_name=request.form.get('last_name'),
                    phone=request.form.get('phone'),
                    email=email,
                    password=generate_password_hash(request.form.get('password')),
                    street_address=request.form.get('street_address')
                )

                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)

                return redirect(next_page)

    return render_template(
        'login.html',
        login_form=login_form,
        register_form=register_form,
        next_page=next_page,
        error_message=error_message
    )


@mainbp.route('/login-booking', methods=['GET', 'POST'])
def login_booking():
    return redirect(url_for('main.login', next=url_for('main.booking_select')))


@mainbp.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html')


@mainbp.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@mainbp.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500