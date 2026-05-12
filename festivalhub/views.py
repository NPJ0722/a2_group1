from flask import Blueprint, render_template

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    return render_template('index.html')


@mainbp.route('/details')
def details():
    return render_template('event-details.html')


@mainbp.route('/create')
def create_event():
    return render_template('create-update-event.html')


@mainbp.route('/booking')
def booking():
    return render_template('booking.html')


@mainbp.route('/bookings')
def bookings():
    return render_template('booking-history.html')


# General Login / Register
@mainbp.route('/login')
def login():
    return render_template('login.html', next_page='/')


# Login required before booking
@mainbp.route('/login-booking')
def login_booking():
    return render_template('login.html', next_page='/booking')


@mainbp.route('/logout')
def logout():
    return render_template('logout.html')


@mainbp.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@mainbp.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500