from flask import current_app, request, jsonify
from functools import wraps
import jwt
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if the token is in the headers
        if 'Authorization' in request.headers:
            print(request.headers['Authorization'])
            token = request.headers['Authorization'].split(" ")[1]  # Assuming "Bearer <token>"

        # If no token, return a 403 response
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            secret_key = current_app.config['JWT_SECRET_KEY']
            # Decode the token
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401 # Unathorized
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()  # Verify the JWT token
        identity = get_jwt_identity()
        if identity['role'] != 'Admin':  # Check if role from JWT is 'admin'
            return jsonify({'message': 'Admins only!'}), 403  # Forbidden
        return fn(*args, **kwargs)
    return wrapper
