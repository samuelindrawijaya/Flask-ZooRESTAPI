from app import db

class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False )
    species = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    specialRequirement = db.Column(db.String(200), nullable=True)
    
    def to_dict(self, include_id=True):
        Animal_dict = {
            'name': self.name,
            'species': self.species,
            'age': self.age,
            'specialRequirement' : self.specialRequirement
        }
        if include_id:
            Animal_dict['id'] = self.id
        return Animal_dict
