import json

from app.models.employee import Employee

def test_create_employee(client, auth_token, generate_fake_roles):
    response = client.post("/employees/", 
                            headers={"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"},
                            data=json.dumps({
                                "name": "Fiony",
                                "email": "fiony@example.com",
                                "phone_number": "1231231234",
                                "role_id": 1,  
                                "schedule": "9 AM - 5 PM",
                                "join_date": "2024-10-01"  
                            }))
    
    assert response.status_code == 201
    json_response = response.get_json()
    expected_message = "Employee with name Fiony has been added successfully!."
    assert json_response["message"] == expected_message
    
    employee_data = json_response["employee"]
    assert employee_data["name"] == "Fiony"
    assert employee_data["email"] == "fiony@example.com"
    assert employee_data["phone_number"] == "1231231234"
    assert employee_data["schedule"] == "9 AM - 5 PM"

def test_get_all_employees(client, auth_token):    
    response = client.get("/employees/", headers={"Authorization": f"Bearer {auth_token}"})
    
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0  # Ensure there's at least one employee
    
    
def test_get_employee_by_id(client, auth_token, generate_fake_employees):
    employee = Employee.query.first()
    response = client.get(f"/employees/{employee.id}", headers={"Authorization": f"Bearer {auth_token}"})
    print(response)
    assert response.status_code == 200
    assert response.json['name'] == employee.name
    assert response.json["email"] == employee.email
    assert response.json["phone_number"] == employee.phone_number
    assert response.json["schedule"] == employee.schedule
    
def test_update_employee(client, auth_token, generate_fake_employees):
    employee = generate_fake_employees[0]  # Get the first employee for testing
    update_data = {
        "name": "Christy",
        "email": "Christy@example.com",
        "phone_number": "3213213210",
        "role_id": 1,
        "schedule": "10 AM - 6 PM",
        "join_date": "2024-10-02"
    }
    
    response = client.put(f"/employees/{employee.id}", 
                          headers={"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"},
                          data=json.dumps(update_data))
    
    assert response.status_code == 200
    json_response = response.get_json()
    expected_message = f"Employee with name {update_data['name']} has been updated successfully!."
    assert json_response["message"] == expected_message

    response = client.get(f"/employees/{employee.id}", headers={"Authorization": f"Bearer {auth_token}"})
    updated_employee = response.get_json()

    assert updated_employee["name"] == update_data["name"]
    assert updated_employee["email"] == update_data["email"]
    assert updated_employee["phone_number"] == update_data["phone_number"]
    assert updated_employee["schedule"] == update_data["schedule"]

def test_delete_employee(client, auth_token, generate_fake_employees):
    employee = generate_fake_employees[0]  # Get the first employee for testing

    # Send DELETE request to delete the employee
    response = client.delete(f"/employees/{employee.id}", 
                             headers={"Authorization": f"Bearer {auth_token}"})
    
    assert response.status_code == 200  # Check if deletion was successful
    json_response = response.get_json()
    expected_message = "employee have been terminated"
    assert json_response["message"] == expected_message

    # Verify the employee is deleted by trying to get it
    response = client.delete(f"/employees/{employee.id}", headers={"Authorization": f"Bearer {auth_token}"})
    
    deleted_employee = Employee.query.get(employee.id)
    assert deleted_employee is not None  # Employee should still exist in the DB
    assert deleted_employee.join_date is None  # Check that join_date is None

