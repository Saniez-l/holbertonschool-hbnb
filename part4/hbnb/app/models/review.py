from sqlalchemy.orm import validates, relationship
from .base_model import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # ID identique à Place.id (String(36))
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    place = relationship("Place", back_populates="reviews")
    author = relationship("User", back_populates="reviews", overlaps="user")

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @validates("text")
    def validate_text(self, key, value):
        if not value:
            raise ValueError("Text cannot be empty")
        return value

    @validates("rating")
    def validate_rating(self, key, value):
        if not (0 < value < 6):
            raise ValueError("Rating must be between 1 and 5")
        return value
