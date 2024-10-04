from app.models.animal import Animal
from app import db

class AnimalDAL:
    @staticmethod
    def get_all_animals():
        return Animal.query.all()

    @staticmethod
    def get_animal_by_id(id):
        return Animal.query.get(id)

    @staticmethod
    def create_animal(data):
        new_animal = Animal(
            name=data['name'],
            species=data['species'],
            age=data['age']
        )
        db.session.add(new_animal)
        db.session.commit()
        return new_animal

    @staticmethod
    def update_animal(id, data):
        animal = Animal.query.get(id)
        if animal:
            animal.name = data.get('name', animal.name)
            animal.species = data.get('species', animal.species)
            animal.age = data.get('age', animal.age)
            db.session.commit()
        return animal

    @staticmethod
    def delete_animal(id):
        animal = Animal.query.get(id)
        if animal:
            db.session.delete(animal)
            db.session.commit()
            return True
        return False
