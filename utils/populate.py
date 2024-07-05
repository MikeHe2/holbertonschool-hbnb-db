# populate.py
from src.persistence.repository import Repository
from src.models.country import Country

def populate_db(repo: Repository) -> None:
    """Populate the database with countries and cities."""


    try:
        countries= [
            Country(name="Uruguay", code="UY"),
            Country(name="Puertp Rico", code="PR"),
            Country(name="United States", code="US"),
            Country(name="Canada", code="CA"),
        ]
        for country in countries:
            existing_country = repo.get_by_code(Country, country.code)
            if existing_country is None:
                repo.save(country)

        print("Memory DB populated")

    except Exception as e:
        print("An error occurred:", str(e))