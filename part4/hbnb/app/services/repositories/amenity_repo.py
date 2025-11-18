from app.persistence.repository import SQLAlchemyRepository
from app.models.amenity import Amenity


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
