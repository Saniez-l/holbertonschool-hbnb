from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates, relationship
from .base_model import BaseModel
from app.extensions import db

# Association table for many-to-many relationship between place & amenity
place_amenity = db.Table('place_amenity',
                         Column('place_id', String, ForeignKey('places.id'), primary_key=True),
                         Column('amenity_id', String, ForeignKey('amenities.id'), primary_key=True)
                         )

class Place(BaseModel):
    """Instantiates or updates Place information.

    Defines the following attributes:
    title (str), description (str), owner_id (str)
    price (float), latitude (float), longitude (float)
    amenities (list), reviews (list)

    Creation and update times, as well as UUID,
    are set via the call to BaseModel's init method.

    """
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)

    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    amenities = relationship(
    "Amenity",
    secondary="place_amenity",
    back_populates="places",
    lazy='subquery'
)
    owner = relationship("User", back_populates="places")

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

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

    @validates("owner_id")
    def validate_owner_id(self, key, value):
        from app.services import facade
        all_users = facade.all_users()
        if not any(user.id == value for user in all_users):
            raise ValueError("Invalid user ID")
        return value

"""
    @validates("reviews")
    def validate_add_review(self, key, review):
        from app.services import facade
        if (review not in all.id for all in facade.get_all_reviews()):
            raise ValueError("Invalid review ID")
        self.reviews.append(review)
        return self.reviews

    @validates("amenities")
    def validate_add_amenitiy(self, key, amenity):
        from app.services import facade
        if (amenity not in all.id for all in facade.get_all_amenities()):
            raise ValueError("Invalid amenity ID")
        self.amenities.append(amenity)
        return self.amenities
"""
