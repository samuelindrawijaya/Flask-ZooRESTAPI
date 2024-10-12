from sqlalchemy.exc import IntegrityError # use this one to catch if there is any problem in database
from app.models.user import User
from app import db

class userDAL:
    @staticmethod
    def create_user(data):
        new_user = User(username=data['username'],role_id=data['role_id'])
        new_user.set_password(data['password'])  # Set the hashed password
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return True
        
        except IntegrityError: 
            db.session.rollback()
            return 'User with this username already exists'