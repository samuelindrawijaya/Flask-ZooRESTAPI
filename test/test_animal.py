from app.models.animal import Animal


def test_get_animal(client, appjson, generate_fake_animals):
    response = client.get("/animals/", headers=appjson)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    
def test_get_animal_by_id(client, appjson, generate_fake_animals):
    """
    Test retrieving an animal by its ID.
    """
    animal_id = Animal.query.first().id  # Get the ID of the first animal
    response = client.get(f"/animals/{animal_id}", headers=appjson)
    assert response.status_code == 200
    assert response.json["name"] == "Gajah"
    assert response.json["species"] == "tulus"
    assert response.json["age"] == 1
    assert response.json["specialRequirement"] == "nyanyi bareng"
    
def test_create_animal(client, appjson):
    # New animal data to be sent in the request
    new_animal_data = {
        "name": "Kuda",
        "species": "Kudanus raurus",
        "age": 5,
        "specialRequirement": "Needs space to run"
    }
    
    # POST request to create the animal
    response = client.post("/animals/", json=new_animal_data, headers=appjson)
    
    assert response.status_code == 201  # Expecting 201 Created
    json_response = response.get_json()
    
    expected_message = "New animal with name Kuda successfully added!"
    assert json_response["message"] == expected_message
    

    animal_data = json_response["animal"]
    assert animal_data["name"] == "Kuda"
    assert animal_data["species"] == "Kudanus raurus"
    assert animal_data["age"] == 5
    assert animal_data["specialRequirement"] == "Needs space to run"
    
def test_update_animal(client, appjson,generate_fake_animals):
    """
    Test updating an existing animal.
    """
    animal = Animal.query.first()
    assert animal is not None, "No animals found in the database."
    
    animal_id = animal.id
    updated_data = {
        "name": "Gajah Besar",
        "species": "Elephantidae",
        "age": 10,
        "specialRequirement": "Extra large habitat"
    }
    response = client.put(f"/animals/{animal_id}", json=updated_data, headers=appjson)
        
    json_response = response.get_json()
    
    expected_message = "Animal with name Gajah Besar succesfully updated !."
    assert json_response["message"] == expected_message
    

    animal_data = json_response["animal"]
    assert animal_data["name"] == "Gajah Besar"
    assert animal_data["species"] == "Elephantidae"
    assert animal_data["age"] == 10
    assert animal_data["specialRequirement"] == "Extra large habitat"
    
    
def test_delete_animal(client, appjson,generate_fake_animals):
    """
    Test delete an existing animal.
    """
    animal = Animal.query.first()
    assert animal is not None, "No animals found in the database."
    
    animal_id = animal.id
    response = client.delete(f'/animals/{animal_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Animal deleted successfully'

    response_check = client.get(f"/animals/{animal_id}", headers=appjson)
    assert response_check.status_code == 404
 
    