from app import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  
    email = db.Column(db.String(100), nullable=False, unique=True) 
    phone_number = db.Column(db.String(20), nullable=False)
    schedule = db.Column(db.String(100), nullable=True)
    # add foreign key to the role_id
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)  
    role = db.relationship('Role', backref='employees')  

    # UPDATED TO NULL ABLE join_date field
    join_date = db.Column(db.DateTime, nullable=True, default=datetime.now)

    def to_dict(self, include_id=True):
        employee_dict = {
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'role': self.role.name, 
            'schedule': self.schedule,
            'join_date': self.join_date.strftime('%Y-%m-%d') if self.join_date else None
        }
        if include_id:
            employee_dict['id'] = self.id
        return employee_dict
