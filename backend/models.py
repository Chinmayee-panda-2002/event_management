from db import db
from datetime import datetime

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # New email field
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # New created_at field

    def __repr__(self):
        return f"<User {self.username}>"

# Define EventOrganizer model
class EventOrganizer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<EventOrganizer {self.name}>"

# Define Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time, nullable=False)  # Add time field
    location = db.Column(db.String(200), nullable=False)  # Add location field
    price = db.Column(db.Float, nullable=False)  # Add price field

    def __repr__(self):
        return f"<Event {self.title}>"

# Define Ticket model
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # e.g., 'booked', 'canceled'

    event = db.relationship('Event', backref=db.backref('tickets', lazy=True))
    user = db.relationship('User', backref=db.backref('tickets', lazy=True))

    def __repr__(self):
        return f"<Ticket {self.id} for Event {self.event_id}>"
