from flask import jsonify, request
from app.DAL.roleDAL import RoleDAL

class RoleController:
    @staticmethod
    def get_all_roles():
        """
        Get all roles
        ---
        tags:
          - Roles
        security:
          - bearerAuth: []
        responses:
          200:
            description: A list of roles
            schema:
              type: array
              items:
                $ref: '#/definitions/Role'
          401:
            description: Unauthorized
          403:
            description: Forbidden
        """
        roles = RoleDAL.get_all_roles()
        return jsonify([role.to_dict() for role in roles]), 200

    @staticmethod
    def get_role_by_id(id):
        """
        Get role by ID
        ---
        tags:
          - Roles
        security:
          - bearerAuth: []
        parameters:
          - name: id
            in: path
            required: true
            type: integer
        responses:
          200:
            description: Role details
            schema:
              $ref: '#/definitions/Role'
          404:
            description: Role not found
        """
        role = RoleDAL.get_role_by_id(id)
        if role:
            return jsonify(role.to_dict()), 200
        return jsonify({'message': 'Role not found'}), 404

    @staticmethod
    def add_role():
        """
        Add a new role
        ---
        tags:
          - Roles
        security:
          - bearerAuth: []
        parameters:
          - name: role
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
        responses:
          201:
            description: Role created
            schema:
              $ref: '#/definitions/Role'
          400:
            description: Role name is required
        """
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'message': 'Role name is required'}), 400

        new_role = RoleDAL.add_role(data['name'])
        return jsonify({
        'message': f'Role with name {data['name']} succesfully added !.',
        'animal': new_role.to_dict()
        }), 201

    @staticmethod
    def update_role(id):
        """
        Update a role
        ---
        tags:
          - Roles
        security:
          - bearerAuth: []
        parameters:
          - name: id
            in: path
            required: true
            type: integer
          - name: role
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
        responses:
          200:
            description: Role updated
            schema:
              $ref: '#/definitions/Role'
          404:
            description: Role not found
          400:
            description: Role name is required
        """
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'message': 'Role name is required'}), 400

        updated_role = RoleDAL.update_role(id, data['name'])
        if updated_role:
            return jsonify({
            'message': f'Role with name {data['name']} succesfully updated !.',
            'animal': updated_role.to_dict()
            }), 201
        return jsonify({'message': 'Role not found'}), 404

    @staticmethod
    def delete_role(id):
        """
        Delete a role
        ---
        tags:
          - Roles
        security:
          - bearerAuth: []
        parameters:
          - name: id
            in: path
            required: true
            type: integer
        responses:
          200:
            description: Role deleted
          404:
            description: Role not found
        """
        deleted_role = RoleDAL.delete_role(id)
        if deleted_role:
            return jsonify({'message': 'Role deleted'}), 200
        return jsonify({'message': 'Role not found'}), 404
