from app.models.role import Role


def test_get_all_roles(client, appjson, generate_fake_roles, auth_token):
    response = client.get("/roles/", headers={**appjson, "Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert {role['name'] for role in data} == {"Admin", "user"}

def test_get_role_by_id(client, appjson, generate_fake_roles, auth_token):
    role_id = Role.query.filter_by(name="Admin").first().id #query filter_by
    response = client.get(f"/roles/{role_id}", headers={**appjson, "Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == "Admin"
    
def test_create_role(client, appjson, auth_token):
    add_role_data = {"name": "Member"}
    response = client.post("/roles/", json=add_role_data, 
                           headers={**appjson, "Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201
    json_response = response.get_json()
    
    expected_message = 'Role with name Member succesfully added !.'
    assert json_response["message"] == expected_message
    
def test_update_role(client, appjson, generate_fake_roles, auth_token):
    role_to_update = Role.query.filter_by(name="Member").first()
    updated_data = {"name": "General Member"}
    response = client.put(f"/roles/{role_to_update.id}", json=updated_data, headers={**appjson, "Authorization": f"Bearer {auth_token}"})
    
    assert response.status_code == 201
    json_response = response.get_json()
    
    expected_message = 'Role with name General Member succesfully updated !.'
    assert json_response["message"] == expected_message
    
def test_delete_role(client, appjson, generate_fake_roles, auth_token):
    role_to_delete = Role.query.filter_by(name="user").first()
    response = client.delete(f"/roles/{role_to_delete.id}", headers={**appjson, "Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    fetched_role = Role.query.get(role_to_delete.id)
    assert fetched_role is None  # Ensure the role is deleted

def test_delete_non_existing_role(client, appjson, auth_token):
    response = client.delete("/roles/99999", headers={**appjson, "Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 404  # Not Found