import os
import sys
from flask_jwt_extended import create_access_token
import pytest
from unittest.mock import patch
from app import create_app, db
from app.models.animal import Animal
from app.models.employee import Employee
from app.models.role import Role
from app.models.user import User

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture(scope="module") 
def app():
    app = create_app("app.Config.testing")
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    with app.app_context():
        yield app

@pytest.fixture(scope="module")
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def test_db(app):
    # Create the database and the tables
    db.drop_all()
    db.create_all()

    yield db  # this is where the test happens

    # Teardown: drop the database and tables after the tests
    db.session.remove()
    db.drop_all()

@pytest.fixture
def generate_fake_animals(test_db):
    gajah = Animal(
        name="Gajah", 
        species="tulus", 
        age=1, 
        specialRequirement="nyanyi bareng"
    )
    merpati = Animal(
        name="merpati", 
        species="doradus", 
        age=1, 
        specialRequirement="kugeruk kwok"
    )
    test_db.session.add(gajah)
    test_db.session.add(merpati)
    test_db.session.commit()
    
    return [gajah, merpati]

@pytest.fixture(scope="module", autouse=True)
def generate_fake_roles(test_db):
    role1 = Role(name='Admin')
    role2 = Role(name='user') 
    test_db.session.add(role1)
    test_db.session.add(role2)
    test_db.session.commit()
    yield
    
    
@pytest.fixture
def generate_fake_user(test_db):
    
    test_db.session.query(User).delete()
    test_db.session.commit()
    
    user1 = User(
        username="Gajah", 
        role_id=1, 
        password_hash = 'gajah123'
    )
    user2 = User(
        username="Leo", 
        role_id=1, 
        password_hash = 'leo123'
    )
    test_db.session.add(user1)
    test_db.session.add(user2)
    test_db.session.commit()
    
    return [user1, user2]

@pytest.fixture
def generate_fake_employees(test_db):
    # Clear any existing employee records
    db.session.query(Employee).delete()
    db.session.commit()

    employees = []
    for i in range(3):  
        employee = Employee(
            name=f"Marsha_{os.urandom(4).hex()}",  
            email=f"marsha{i}@example.com",  
            phone_number="1234567890",
            role_id=1  
        )
        test_db.session.add(employee)
        employees.append(employee)  # Add to the list
    test_db.session.commit()
    return employees  # Return the list of employees

@pytest.fixture
def auth_token(app, generate_fake_employees):
    with app.app_context():
        employee = Employee.query.first()   
        token = create_access_token(identity={'id': employee.id, 'role': 'Admin'})
        return token

@pytest.fixture
def appjson() -> dict:
    return {"Content-Type": "application/json"}
