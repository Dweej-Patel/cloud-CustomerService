from app import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    landlord_id = db.Column(db.Integer, db.ForeignKey("landlords.id"))
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))
    email_verification = db.Column(db.Enum, nullable=False, default=False)

    def __repr__(self):
        return f"User: '{self.id}', '{self.first_name}', '{self.last_name}', '{self.email}', '{self.created_date}'"

class Addresses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    streetAddress = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    country = db.Column(db.String(30), nullable=True)
    postalCode = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f"Address: '{self.id}', '{self.streetAddress}', '{self.city}', '{self.state}', '{self.country}', '{self.postalCode}'"

class Landlords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Landlord: '{self.id}', '{self.first_name}', '{self.last_name}'"