from flask import request, jsonify
from app.DAL.AnimalDAL import AnimalDAL

class AnimalController:
    @staticmethod
    def get_all_animals():
        """
        Get all animals
        ---
        tags:
          - Animal
        responses:
            200:
                description: Return list of animals
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: Animal ID
                                example: 1
                            name:
                                type: string
                                description: Animal Name
                                example: "Lion"
                            species:
                                type: string
                                description: Animal Species
                                example: "Panthera leo"
                            age:
                                type: integer
                                description: Age of the animal
                                example: 5
                            specialRequirement:
                                type: string
                                description: Special requirements for the animal
                                example: "Requires daily sun exposure"
        """
        animals = AnimalDAL.get_all_animals()
        return jsonify([animal.to_dict(include_id=False) for animal in animals])

    @staticmethod
    def get_animal_by_id(id):
        """
        Get animal by ID
        ---
        tags:
          - Animal
        parameters:
            - name: id
              in: path
              type: integer
              required: true
              description: Animal ID
        responses:
            200:
                description: Animal Detail
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: Animal ID
                            example: 1
                        name:
                            type: string
                            description: Animal Name
                            example: "Lion"
                        species:
                            type: string
                            description: Animal Species
                            example: "Panthera leo"
                        age:
                            type: integer
                            description: Age of the animal
                            example: 5
                        specialRequirement:
                            type: string
                            description: Special requirements
                            example: "Requires daily sun exposure"
            404:
                description: Animal not found
        """
        animal = AnimalDAL.get_animal_by_id(id)
        if animal: 
            return jsonify(animal.to_dict(include_id=False)) 
        return jsonify({'message': 'Animal not found'}), 404

    @staticmethod
    def create_animal():
        """
        Create a new animal
        ---
        tags:
          - Animal
        parameters:
            - name: animal
              in: body
              required: true
              schema:
                  type: object
                  properties:
                      name:
                          type: string
                          description: Animal Name
                          example: "Lion"
                      species:
                          type: string
                          description: Animal Species
                          example: "Panthera leo"
                      age:
                          type: integer
                          description: Animal Age
                          example: 5
                      specialRequirement:
                          type: string
                          description: Special requirements for the animal
                          example: "Requires daily sun exposure"
        responses:
            201:
                description: Animal created successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: Animal ID
                            example: 1
                        name:
                            type: string
                            description: Animal Name
                            example: "Lion"
                        species:
                            type: string
                            description: Animal Species
                            example: "Panthera leo"
                        age:
                            type: integer
                            description: Animal Age
                            example: 5
                        specialRequirement:
                            type: string
                            description: Special requirements
                            example: "Requires daily sun exposure"
            400:
                description: Invalid input
        """
        data = request.get_json()
        new_animal = AnimalDAL.create_animal(data)
        return jsonify({
        'message': f'New animal with name {data['name']} successfully added!',
        'animal': new_animal.to_dict(include_id=False)
        }), 201

    @staticmethod
    def update_animal(id):
        """
        Update an animal
        ---
        tags:
          - Animal
        parameters:
            - name: id
              in: path
              type: integer
              required: true
              description: Animal ID to update
            - name: animal
              in: body
              required: true
              schema:
                  type: object
                  properties:
                      name:
                          type: string
                          description: New Animal Name
                          example: "Lion"
                      species:
                          type: string
                          description: New Animal Species
                          example: "Panthera leo"
                      age:
                          type: integer
                          description: New Animal Age
                          example: 6
                      specialRequirement:
                          type: string
                          description: New special requirements
                          example: "Needs to be kept in shade during afternoon"
        responses:
            200:
                description: Updated animal
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: Animal ID
                            example: 1
                        name:
                            type: string
                            description: Updated Animal Name
                            example: "Lion"
                        species:
                            type: string
                            description: Updated Animal Species
                            example: "Panthera leo"
                        age:
                            type: integer
                            description: Updated Animal Age
                            example: 6
                        specialRequirement:
                            type: string
                            description: Updated special requirements
                            example: "Needs to be kept in shade during afternoon"
            404:
                description: Animal not found
        """
        data = request.get_json()
        updated_animal = AnimalDAL.update_animal(id, data)
        if not updated_animal: 
            return jsonify({'message': 'Animal not found'}), 404
        return jsonify({
        'message': f'Animal with name {data['name']} succesfully updated !.',
        'animal': updated_animal.to_dict(include_id=False)
        }), 201

    @staticmethod
    def delete_animal(id):
        """
        Delete an animal
        ---
        tags:
          - Animal
        parameters:
            - name: id
              in: path
              type: integer
              required: true
              description: Animal ID to delete
        responses:
            204:
                description: Animal deleted successfully
            404:
                description: Animal not found
        """
        deleted = AnimalDAL.delete_animal(id)
        if deleted:
            return jsonify({'message': 'Animal deleted successfully'}), 200  
        return jsonify({'message': 'Animal not found'}), 404
