from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import validates, relationship
from .base_model import BaseModel
from app.extensions import db

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True)  # Important : doit correspondre à Review.place_id
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    amenities = relationship(
        "Amenity",
        secondary="place_amenity",
        back_populates="places",
        lazy='subquery'
    )
    owner = relationship("User", back_populates="places")

    def __init__(self, title, description, price, latitude, longitude, owner_id, image_url=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.image_url = image_url

    @validates("title")
    def validate_title(self, key, value):
        if not value or len(value) > 100:
            raise ValueError("Title must be between 1 and 100 characters")
        return value

    @validates("price")
    def validate_price(self, key, value):
        if not isinstance(value, float) or value < 0:
            raise ValueError("Price must be a positive number")
        return value

    @validates("latitude")
    def validate_latitude(self, key, value):
        if not isinstance(value, float) or not (-90.00 <= value <= 90.00):
            raise ValueError("Latitude must be between -90.00 and 90.00")
        return value

    @validates("longitude")
    def validate_longitude(self, key, value):
        if not isinstance(value, float) or not (-180.00 <= value <= 180.00):
            raise ValueError("Longitude must be between -180.00 and 180.00")
        return value
