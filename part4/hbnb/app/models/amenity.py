from sqlalchemy.orm import validates, relationship
from .base_model import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    """Instantiates or updates Amenity information.

    Defines the attribute 'name' (str)

    Creation and update times, as well as UUID,
    are set via the call to BaseModel's init method.

    """
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    places = relationship("Place", secondary="place_amenity", back_populates="amenities")

    def __init__(self, name):
        super().__init__()
        self.name = name

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("Name must be between 1 and 50 characters")
        return value
