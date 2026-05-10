from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)

    bookings = db.relationship('Booking', backref='user', lazy=True)


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    start_time = db.Column(db.String(50))
    end_time = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)

    venue = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    artist_lineup = db.Column(db.Text)

    ticket_type = db.Column(db.String(80), default='General Admission')
    tickets_available = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(30), default='Open')
    image = db.Column(db.String(255))

    acknowledgement_type = db.Column(db.String(80), default='No Acknowledgement of Country')
    traditional_custodians = db.Column(db.String(150))
    acknowledgement_statement = db.Column(db.Text)

    bookings = db.relationship('Booking', backref='event', lazy=True)
    comments = db.relationship('Comment', backref='event', lazy=True)


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    ticket_quantity = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    booking_fee = db.Column(db.Float, default=0.0)
    total_price = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    user_name = db.Column(db.String(120), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    posted_time = db.Column(db.DateTime, default=datetime.utcnow)