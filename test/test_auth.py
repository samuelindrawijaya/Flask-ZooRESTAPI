import json
from jwt import PyJWTError
import pytest
from flask_jwt_extended import decode_token

from app.models.user import User

# Test for login functionality
def test_login_success(client, appjson,test_db, generate_fake_roles, generate_fake_user):
    test_user = generate_fake_user[0]
    test_user.set_password("password123")
    test_db.session.commit()
    
    
    login_data = {
        "username": test_user.username,  
        "password": "password123"
    }
    
   
    response = client.post("/auth/", data=json.dumps(login_data), headers=appjson)
    

    assert response.status_code == 200
    data = response.get_json()
    

    assert "access_token" in data
    
    # Decode the token and verify contents
    token_data = decode_token(data["access_token"])
    assert token_data['sub']['id'] == test_user.id
    assert token_data['sub']['role'] == test_user.role.name
    
    
def test_invalid_token_decoding(client, appjson, generate_fake_roles, generate_fake_user):
    test_user = generate_fake_user[0]
    test_user.set_password("password123")
    
    login_data = {
        "username": test_user.username,
        "password": "password123"
    }

    response = client.post("/auth/", data=json.dumps(login_data), headers=appjson)
    assert response.status_code == 200
    data = response.get_json()
    
    assert "access_token" in data
    
    valid_token = data["access_token"]
    invalid_token = valid_token[:-1]  # Tamper with the token (remove the last character)


    try:
        token_data = decode_token(invalid_token)
        assert False, "Expected JWTError was not raised"
    except PyJWTError as e:
        assert str(e) == "Signature verification failed"  

# Test invalid login credentials
def test_login_invalid_credentials(client,appjson):
    login_data = {
        "username": "non_existent_user",
        "password": "wrong_password"
    }
    response = client.post("/auth/", data=json.dumps(login_data), headers=appjson)
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Invalid credentials"

# Test successful user creation
def test_create_user_success(client,appjson, test_db, generate_fake_roles):
    user_data = {
        "username": "newuser",
        "password": "password123",
        "role_id": 2  
    }
    
    response = client.post("/auth/register", data=json.dumps(user_data), headers=appjson)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User with name newuser created !."

# Test user creation with missing parameters
def test_create_user_missing_parameters(client,appjson):
    user_data = {
        "username": "newuser",
       
    }
    
    response = client.post("/auth/register", data=json.dumps(user_data), headers=appjson)
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "username , password, role_id , are required"

def test_create_user_error(client,appjson):
    user_data = {
        'username': 'Kuda',
        'password': 'gajah123',
        'role_id': 1
    }

   
    response = client.post('/auth/register', json=user_data, headers=appjson)
    assert response.status_code == 201  

    # Check if the user actually exists in the database
    created_user = User.query.filter_by(username='Kuda').first()
    assert created_user is not None
    assert created_user.username == 'Kuda'