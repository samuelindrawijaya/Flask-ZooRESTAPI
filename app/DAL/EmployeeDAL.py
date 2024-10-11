from sqlalchemy.exc import IntegrityError # use this one to catch if there is any problem in database
from app.models.employee import Employee
from app import db

class EmployeeDAL:

    @staticmethod
    def create_employee(data):
        new_employee = Employee(
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number'],
            role_id=data['role_id'],
            schedule=data.get('schedule'),
            join_date=data.get('join_date')  # we can null join date
        )
        
        try:
            db.session.add(new_employee)
            db.session.commit()
            return new_employee
        except IntegrityError: # to check if unique violation exist using sqlalchemy
            db.session.rollback()  
            return None 
        

    @staticmethod
    def update_employee(id, data):
        employee = db.session.get(Employee, id)
        if not employee:
            return None

        # using query filter if name input = name saved 
        existing_employee = Employee.query.filter(
            (Employee.name == data['name']) | 
            (Employee.email == data['email'])
        ).filter(Employee.id != id).first()  # the filtered data is not the edited data

        if existing_employee:
            return None  # if exist true means that there is already employee have name and email

        employee.name = data['name']
        employee.email = data['email']
        employee.phone_number = data['phone_number']
        employee.role_id = data['role_id']
        employee.schedule = data.get('schedule')

        if 'join_date' in data:  # because it can be null, it check if there is value 
            employee.join_date = data['join_date']

        db.session.commit()
        return employee

    @staticmethod
    def get_all_employees():
        return Employee.query.all()

    @staticmethod
    def get_employee_by_id(employee_id):
        return Employee.query.get(employee_id)
    
    @staticmethod
    def delete_employee(id):
        employee = Employee.query.get(id)
        if employee:
            employee.join_date = None
            db.session.commit()
            return True
        return False
