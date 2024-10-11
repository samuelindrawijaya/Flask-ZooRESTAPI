from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()
def create_app(settings_conf=None):
    app = Flask(__name__)

    # Default to development configuration if none is provided
    os.environ.setdefault("FLASK_SETTINGS_MODULE", "app.Config.dev")
    conf = settings_conf or os.getenv("FLASK_SETTINGS_MODULE")
    
    app.config.from_object(conf)
    
    # Check if testing environment, set specific database for testing
    if app.config.get('TESTING'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_POSTGRES_CONNECTION_STRING_TEST')
    else:
        # For non-test environments, ensure the JWT_SECRET_KEY is set
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)  # Initialize JWT
    Swagger(app, 
    template={
            "swagger": "2.0",
            "info": {
                "title": "ZOO API",
                "description": "ZOO Restful API made by Flask and PostgreSQL @supabase",
                "contact": {
                "responsibleOrganization": "ME",
                "responsibleDeveloper": "Me",
                "email": "me@me.com",
                "url": "www.me.com",
                }
            },
            "securityDefinitions": {
                "bearerAuth": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
                }
            },
            "security": [
                {"bearerAuth": []}
            ],
            "definitions": {
                "Role": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "example": 1
                        },
                        "name": {
                            "type": "string",
                            "example": "Admin"
                        }
                    }
                },
                "Employee": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "example": 1
                        },
                        "name": {
                            "type": "string",
                            "example": "Admin"
                        },
                        "email": {
                            "type": "string",
                            "example": "Admin@gmail.com"
                        },
                        "phone_number": {
                            "type": "string",
                            "example": "03444433434"
                        },
                        "role_id": {
                            "type": "string",
                            "example": "1"
                        },
                        "schedule": {
                            "type": "string",
                            "example": "Mon - Sun"
                        }
                    }
                }
            }
        }
    )
    
    @app.route('/')
    def index():
        return redirect('/apidocs/#/')

    from app.routes.api import animal_bp, employee_bp, role_bp, auth_bp  
    
    app.register_blueprint(animal_bp, url_prefix='/animals')
    app.register_blueprint(employee_bp, url_prefix='/employees')
    app.register_blueprint(role_bp, url_prefix='/roles')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

