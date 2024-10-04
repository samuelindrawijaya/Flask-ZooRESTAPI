from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.DAL.AuthDAL import userDAL
from app.models.user import User
from app import db

class AuthController:

    @staticmethod
    def login():
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
