from flask import Flask, render_template

app = Flask(__name__)


# Home Page
@app.route('/')
def index():
    return render_template('index.html')


# Event Details Page
@app.route('/details')
def details():
    return render_template('event-details.html')


# Create / Update Event Page
@app.route('/create')
def create_event():
    return render_template('create-update-event.html')


# Booking Page
@app.route('/booking')
def booking():
    return render_template('booking.html')


# Booking History Page
@app.route('/bookings')
def bookings():
    return render_template('booking-history.html')


# Login / Register Page
@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)