"""
Amenity related functionality
"""

from sqlalchemy import ForeignKey
from src.models.base import Base
from src.models import db

class Amenity(db.Model):
    """Amenity representation"""

    __tablename__ = 'amenities'

    name = db.Column(db.String(120), unique=True, nullable=False)
    places = db.relationship('PlaceAmenity', back_populates='amenity')



    def __init__(self, name: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)

        self.name = name

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        """Create a new amenity"""
        from src.persistence import repo

        amenity = Amenity(**data)

        repo.save(amenity)

        return amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        from src.persistence import repo

        amenity: Amenity | None = Amenity.get(amenity_id)

        if not amenity:
            return None

        if "name" in data:
            amenity.name = data["name"]

        repo.update(amenity)

        return amenity


class PlaceAmenity(db.Model):
    """PlaceAmenity representation"""

    __tablename__ = 'place_amenities'

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), primary_key=True)
    amenity_id = db.Column(db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    place = db.relationship('Place', back_populates='amenities')
    amenity = db.relationship('Amenity', back_populates='places')


    def __init__(self, place_id: str, amenity_id: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)

        self.place_id = place_id
        self.amenity_id = amenity_id

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<PlaceAmenity ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get(place_id: str, amenity_id: str) -> "PlaceAmenity | None":
        """Get a PlaceAmenity object by place_id and amenity_id"""
        from src.persistence import repo

        place_amenities: list[PlaceAmenity] = repo.get_all("placeamenity")

        for place_amenity in place_amenities:
            if (
                place_amenity.place_id == place_id
                and place_amenity.amenity_id == amenity_id
            ):
                return place_amenity

        return None

    @staticmethod
    def create(data: dict) -> "PlaceAmenity":
        """Create a new PlaceAmenity object"""
        from src.persistence import repo

        new_place_amenity = PlaceAmenity(**data)

        repo.save(new_place_amenity)

        return new_place_amenity

    @staticmethod
    def delete(place_id: str, amenity_id: str) -> bool:
        """Delete a PlaceAmenity object by place_id and amenity_id"""
        from src.persistence import repo

        place_amenity = PlaceAmenity.get(place_id, amenity_id)

        if not place_amenity:
            return False

        repo.delete(place_amenity)

        return True

    @staticmethod
    def update(entity_id: str, data: dict):
        """Not implemented, isn't needed"""
        raise NotImplementedError(
            "This method is defined only because of the Base class"
        )
