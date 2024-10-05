from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.DAL.AuthDAL import userDAL
from app.models.user import User
from app import db

class AuthController:

    @staticmethod
    def login():
        """
        Login a user
        ---
        tags:
          - Authentication
        summary: User login
        description: Login user and returns a JWT access token.
        parameters:
          - in: body
            name: user
            description: The username and password for login.
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                  example: "testuser"
                password:
                  type: string
                  example: "password123"
        responses:
          200:
            description: Successful login, returns an access token.
            schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
          401:
            description: Invalid credentials
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Invalid credentials"
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            role_name = user.role.name
            access_token = create_access_token(identity={'id' : user.id, 'role' : role_name})
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
        
        
    @staticmethod
    def create_user():
        """
        Register a new user
        ---
        tags:
          - Authentication
        description: Creates a new user with a username, password, and role.
        parameters:
          - in: body
            name: user
            description: The user information for registration.
            schema:
              type: object
              required:
                - username
                - password
                - role_id
              properties:
                username:
                  type: string
                  example: "newuser"
                password:
                  type: string
                  example: "password123"
                role_id:
                  type: integer
                  example: 2
        responses:
          201:
            description: User successfully created.
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User with name newuser created!"
          400:
            description: Missing or invalid parameters.
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "username, password, role_id are required."
          409:
            description: Conflict - User already exists.
            schema:
              type: object
              properties:
                status:
                  type: integer
                  example: 409
                message:
                  type: string
                  example: "User with this name or email already exists."
        """
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data or 'role_id' not in data:
            return jsonify({'message': 'username , password, role_id , are required'}), 400

        new_user = userDAL.create_user(data)

        if new_user:
            return jsonify({'message': f'User with name {data['username']} created !.'}), 201
        else:
            return jsonify({
                'status': 409,
                'message': 'User with this name or email already exists.'
            }), 409  # The second 400 is the actual HTTP status code.
