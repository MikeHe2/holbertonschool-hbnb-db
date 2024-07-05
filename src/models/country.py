from src.models import db
from sqlalchemy import Column, String
import os

"""
Country related functionality
"""


class Country(db.Model):
    """
    Country representation

    This class does NOT inherit from Base, you can't delete or update a country

    This class is used to get and list countries
    """

    __tablename__ = 'countries'


    code = db.Column(db.String(3), unique=True, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    cities = db.relationship('City', back_populates='country')


    def __init__(self, name: str, code: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the country"""
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        from src.persistence import repo

        if os.getenv("REPOSITORY") == "file":
            countries: list["Country"] = repo.get_all("country")
        else:
            countries: list["Country"] = repo.get_all(Country)

        return countries

    @staticmethod
    def get(code: str) -> "Country | None":
        """Get a country by its code"""
        for country in Country.get_all():
            if country.code == code:
                return country
        return None

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        from src.persistence import repo

        country = Country(name, code)

        repo.save(country)

        return country
