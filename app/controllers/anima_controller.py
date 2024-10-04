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
        """
        animals = AnimalDAL.get_all_animals()
        return jsonify([animal.to_dict() for animal in animals])

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
              description: Search Animal ID 
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
                            description: The name of the animal
                            example: "Lion"
            404:
                description: Animal not found
        """
        animal = AnimalDAL.get_animal_by_id(id)
        if animal: 
            return jsonify(animal.to_dict()) 
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
            400:
                description: Invalid input
        """
        data = request.get_json()
        new_animal = AnimalDAL.create_animal(data)
        return jsonify(new_animal.to_dict()), 201

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
            404:
                description: Animal not found
        """
        data = request.get_json()
        updated_animal = AnimalDAL.update_animal(id, data)
        if not updated_animal: 
            return jsonify({'message': 'Animal not found'}), 404
        return jsonify(updated_animal.to_dict())

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
            return jsonify({'message': 'Animal deleted successfully'}), 204
        return jsonify({'message': 'Animal not found'}), 404
