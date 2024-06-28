"""
This module exports a Repository that persists data in a JSON file
"""

from datetime import datetime
import json
from src.models.base import Base
from src.persistence.repository import Repository
from utils.constants import FILE_STORAGE_FILENAME


class FileRepository(Repository):
    """File Repository"""

    __filename = FILE_STORAGE_FILENAME
    __data: dict[str, list] = {
        "country": [],
        "user": [],
        "amenity": [],
        "city": [],
        "review": [],
        "place": [],
        "placeamenity": [],
    }

    def __init__(self) -> None:
        """Calls reload method"""
        self.reload()

    def _save_to_file(self):
        """Helper method to save the current object data to the file"""
        serialized = {
            k: [v.to_dict() for v in l if type(v) is not dict]
            for k, l in self.__data.items()
        }

        with open(self.__filename, "w") as file:
            json.dump(serialized, file, indent=4)

    def get_all(self, model_name: str):
        """Get all objects of a given model"""
        return self.__data.get(model_name, [])

    def get(self, model_name: str, obj_id: str):
        """Get an object by its ID"""
        for obj in self.get_all(model_name):
            if obj.id == obj_id:
                return obj
        return None

    def reload(self):
        """Reloads the data from the file"""
        file_data = {}
        try:
            with open(self.__filename, "r") as file:
                file_data = json.load(file)
        except FileNotFoundError:
            from src.models.country import Country

            self.__data["country"] = [Country("Uruguay", "UY")]

            self._save_to_file()

        from src.models.amenity import Amenity, PlaceAmenity
        from src.models.city import City
        from src.models.country import Country
        from src.models.place import Place
        from src.models.review import Review
        from src.models.user import User

        models = {
            "amenity": Amenity,
            "city": City,
            "country": Country,
            "place": Place,
            "placeamenity": PlaceAmenity,
            "review": Review,
            "user": User,
        }

        for model, data in file_data.items():
            for item in data:
                instance: Base = models[model](**item)

                if "created_at" in item:
                    instance.created_at = datetime.fromisoformat(
                        item["created_at"]
                    )
                if "updated_at" in item:
                    instance.updated_at = datetime.fromisoformat(
                        item["updated_at"]
                    )

                self.save(data=instance, save_to_file=False)

    def save(self, data: Base, save_to_file=True):
        """Save an object to the repository"""
        model: str = data.__class__.__name__.lower()

        if model not in self.__data:
            self.__data[model] = []

        self.__data[model].append(data)

        if save_to_file:
            self._save_to_file()

    def update(self, obj: Base):
        """Update an object in the repository"""
        cls = obj.__class__.__name__.lower()

        for i, o in enumerate(self.__data[cls]):
            if o.id == obj.id:
                obj.updated_at = datetime.now()
                self.__data[cls][i] = obj
                self._save_to_file()
                return obj

        return None

    def delete(self, obj: Base):
        """Delete an object from the repository"""
        class_name = obj.__class__.__name__.lower()

        if obj not in self.__data[class_name]:
            return False

        self.__data[class_name].remove(obj)

        self._save_to_file()

        return True
