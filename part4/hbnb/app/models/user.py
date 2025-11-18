from sqlalchemy.orm import validates, relationship
from .base_model import BaseModel
from app.extensions import bcrypt, db
import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
# correct format to verify user email against


class User(BaseModel):
    """Instantiates or updates User information.

    Defines the following user attributes:
    first_name (str), last_name (str), email (str)
    is_admin (bool), places (list)

    Creation and update times, as well as UUID,
    are set via the call to BaseModel's init method.

    """
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = relationship("Place", back_populates="owner", lazy=True, cascade="all, delete-orphan")
    reviews = relationship("Review", backref="author", lazy=True, cascade="all, delete-orphan")


    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.hash_password(password)
        self.is_admin = is_admin

    @validates("first_name")
    def validate_first_name(self, key, value):
        if not 0 < len(value) <= 50:
            raise ValueError("First name must be between 1 and 50 characters")
        return value

    @validates("last_name")
    def validate_last_name(self, key, value):
        if not 0 < len(value) <= 50:
            raise ValueError("Last name must be between 1 and 50 characters")
        return value

    @validates("email")
    def validate_email(self, key, value):
        if not value:
            raise ValueError("Email cant be empty")
        if not re.fullmatch(regex, value):
            raise ValueError("Invalid email format")
        return value
    
    @validates("is_admin")
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("Must be True or False")
        return value

    def hash_password(self, password):
        # Hashes the password before storing it
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        return self.password

    def verify_password(self, password):
        # Verifies if the provided password matches the hashed password
        return bcrypt.check_password_hash(self.password, password)

    def owned_places(self, place):
        # Adds an owned place to the user
        self.places.append(place)
