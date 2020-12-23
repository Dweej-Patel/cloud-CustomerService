from app import db
from datetime import datetime
import enum

class Email_Enum(enum.Enum):
    inactive = 0
    pending = 1
    active = 2

class Service_Types(enum.Enum):
    repair = 0
    exterminator = 1
    fire = 2
    other = 3


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    landlord_id = db.Column(db.Integer, db.ForeignKey("landlords.id"))
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))
    email_verification = db.Column(db.Enum(Email_Enum), nullable=False, default=Email_Enum.inactive)

    def __repr__(self):
        return f"User: '{self.id}', '{self.first_name}', '{self.last_name}', '{self.email}', '{self.created_date}'"

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "landlord_id": self.landlord_id,
            "email_verification": self.email_verification,
            "addressId": self.address_id
        }



class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(Service_Types), nullable=False, default=Service_Types.other)
    message = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"Request: '{self.id}', '{self.type}', '{self.subject}'"



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
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    email_verification = db.Column(db.Enum(Email_Enum), nullable=False, default=Email_Enum.inactive)

    def __repr__(self):
        return f"Landlord: '{self.id}', '{self.first_name}', '{self.last_name}'"