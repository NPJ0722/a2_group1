from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

from . import db
from .models import User, Event, Booking, Comment
from .forms import LoginForm, RegisterForm, EventForm, BookingForm, CommentForm


mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)


@mainbp.route('/seed-events')
def seed_events():
    Booking.query.delete()
    Event.query.delete()

    events = [
        Event(name='The Swell Sessions 2026', category='Beach / Music Festival', date='2026-04-11',
              start_time='15:00', end_time='22:00', description='A coastal live music event featuring beachside energy, relaxed vibes, and Australian artists.',
              venue='Coastal Outdoor Stage', location='Victoria', artist_lineup='Australian live artists',
              ticket_type='General Admission', tickets_available=100, price=99, status='Open',
              image='The Swell Sessions.png', acknowledgement_type='Generic Acknowledgement',
              traditional_custodians='Traditional Custodians of Victoria', acknowledgement_statement='FestivalHub acknowledges the Traditional Custodians of the land.'),

        Event(name='Gather Sounds', category='Indie / Rock', date='2026-04-10',
              start_time='17:00', end_time='23:00', description='A two-night live music festival featuring multiple artists and a vibrant atmosphere for music lovers.',
              venue='Adelaide Uni Cloisters & Unibar', location='Adelaide', artist_lineup='Bad//Dreams, West Thebarton, The Empty Threats',
              ticket_type='General Admission', tickets_available=120, price=129, status='Open',
              image='Gather Sounds.png', acknowledgement_type='Generic Acknowledgement',
              traditional_custodians='Kaurna People', acknowledgement_statement='FestivalHub acknowledges the Kaurna People of the Adelaide Plains.'),

        Event(name='Melbourne Popfest 2026', category='Indie / Pop', date='2026-04-20',
              start_time='14:00', end_time='21:00', description='An energetic pop-focused event showcasing emerging artists and a fun city festival atmosphere.',
              venue='Melbourne Music Hall', location='Melbourne', artist_lineup='Emerging pop artists',
              ticket_type='General Admission', tickets_available=80, price=89, status='Inactive',
              image='Melbourne Popfest.png', acknowledgement_type='Generic Acknowledgement',
              traditional_custodians='Wurundjeri People', acknowledgement_statement='FestivalHub acknowledges the Traditional Custodians of Melbourne.'),

        Event(name='Ability Fest 2026', category='Accessible Festival', date='2026-06-15',
              start_time='12:00', end_time='20:00', description='Australia’s leading accessible music festival, focused on inclusion and a strong live experience.',
              venue='Accessible Outdoor Venue', location='Melbourne', artist_lineup='Inclusive live performers',
              ticket_type='General Admission', tickets_available=90, price=75, status='Inactive',
              image='Ability Fest.png', acknowledgement_type='Generic Acknowledgement',
              traditional_custodians='Wurundjeri People', acknowledgement_statement='FestivalHub acknowledges the Traditional Custodians of the land.'),

        Event(name='South Summit Tour', category='Tour', date='2026-07-01',
              start_time='18:00', end_time='22:00', description='A national tour bringing live alternative music to major Australian cities.',
              venue='National Tour Venues', location='Australia', artist_lineup='South Summit',
              ticket_type='General Admission', tickets_available=110, price=110, status='Open',
              image='South Summit.png', acknowledgement_type='Generic Acknowledgement',
              traditional_custodians='Traditional Custodians of Australia', acknowledgement_statement='FestivalHub acknowledges Traditional Custodians across Australia.'),

        Event(name='Riebl Tedsco Mcgill', category='Live Tour', date='2026-07-10',
              start_time='19:00', end_time='22:00', description='A live performance tour featuring a contemporary line-up and intimate concert venues.',
              venue='Melbourne Live Venue', location='Melbourne', artist_lineup='Riebl Tedsco Mcgill',
              ticket_type='General Admission', tickets_available=0, price=95, status='Sold out',
              image='Riebl Tedsco Mcgill.png', acknowledgement_type='Generic Acknowledgement',
              traditional_custodians='Wurundjeri People', acknowledgement_statement='FestivalHub acknowledges the Traditional Custodians of Melbourne.'),

        Event(name='ILLY Tour', category='Hip Hop / Tour', date='2026-06-20',
              start_time='19:30', end_time='22:30', description='A multi-city anniversary tour celebrating iconic hip hop releases and live fan favourites.',
              venue='Australian Tour Venues', location='Australia', artist_lineup='ILLY',
              ticket_type='General Admission', tickets_available=100, price=120, status='Inactive',
              image='ILLY.png', acknowledgement_type='Generic Acknowledgement',
              traditional_custodians='Traditional Custodians of Australia', acknowledgement_statement='FestivalHub acknowledges Traditional Custodians across Australia.'),

        Event(name='Thundamentals Tour', category='Hip Hop / Tour', date='2026-08-01',
              start_time='19:00', end_time='22:00', description='A national tour bringing energetic hip hop performances to audiences across Australia.',
              venue='Australian Tour Venues', location='Australia', artist_lineup='Thundamentals',
              ticket_type='General Admission', tickets_available=60, price=115, status='Cancelled',
              image='Thundamentals.png', acknowledgement_type='Generic Acknowledgement',
              traditional_custodians='Traditional Custodians of Australia', acknowledgement_statement='FestivalHub acknowledges Traditional Custodians across Australia.')
    ]

    db.session.add_all(events)
    db.session.commit()

    return redirect(url_for('main.booking_select'))


@mainbp.route('/details', methods=['GET', 'POST'])
def details():
    event = Event.query.first()
    comment_form = CommentForm()

    if request.method == 'POST':
        new_comment = Comment(
            event_id=event.id,
            user_name=request.form['user_name'],
            comment_text=request.form['comment_text']
        )

        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('main.details'))

    comments = Comment.query.filter_by(event_id=event.id).all()

    return render_template(
        'event-details.html',
        event=event,
        comment_form=comment_form,
        comments=comments
    )

@mainbp.route('/create', methods=['GET', 'POST'])
def create_event():
    form = EventForm()

    if request.method == 'POST':
        new_event = Event(
            name=form.name.data,
            category=form.category.data,
            date=request.form['date'],
            start_time=request.form['start_time'],
            end_time=request.form['end_time'],
            description=form.description.data,
            venue=form.venue.data,
            location=form.location.data,
            artist_lineup=form.artist_lineup.data,
            ticket_type=form.ticket_type.data,
            tickets_available=form.tickets_available.data,
            price=form.price.data,
            status=request.form['status'],
            image=form.image.data,
            acknowledgement_type=form.acknowledgement_type.data,
            traditional_custodians=form.traditional_custodians.data,
            acknowledgement_statement=form.acknowledgement_statement.data
        )

        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('create-update-event.html', form=form)


@mainbp.route('/booking')
def booking_select():
    events = Event.query.all()
    show_login_modal = request.args.get('login_required') == '1'
    return render_template('booking-select.html', events=events, show_login_modal=show_login_modal)


@mainbp.route('/booking/<int:event_id>', methods=['GET', 'POST'])
def booking(event_id):
    form = BookingForm()
    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        ticket_quantity = int(request.form['ticket_quantity'])

        if ticket_quantity > event.tickets_available:
            return render_template('booking.html', form=form, event=event)

        ticket_price = event.price
        booking_fee = 8.00
        total_price = (ticket_price * ticket_quantity) + booking_fee

        new_booking = Booking(
            user_id=1,
            event_id=event.id,
            ticket_quantity=ticket_quantity,
            ticket_price=ticket_price,
            booking_fee=booking_fee,
            total_price=total_price
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

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()

        if user and check_password_hash(user.password, login_form.password.data):
            login_user(user)
            return redirect(next_page)
        else:
            error_message = "Incorrect email or password."

    if register_form.validate_on_submit():
        existing_user = User.query.filter_by(email=register_form.email.data).first()

        if existing_user:
            error_message = "This email is already registered."
        else:
            new_user = User(
                first_name=register_form.first_name.data,
                last_name=register_form.last_name.data,
                phone=register_form.phone.data,
                email=register_form.email.data,
                password=generate_password_hash(register_form.password.data),
                street_address=register_form.street_address.data
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