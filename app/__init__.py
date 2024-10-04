from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_jwt_extended import JWTManager
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)  # Initialize JWT
    swagger = Swagger(app, 
    template={
            "swagger": "2.0",
            "info": {
                "title": "ZOO API",
                "description": "ZOO Restfull API made by Flask and postgree @supabase",
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
                }
            }
        }
    )
    
    @app.route('/')
    def index():
        return redirect('/apidocs/#/')

    from app.routes.api import animal_bp,employee_bp,role_bp,auth_bp  
    
    
    app.register_blueprint(animal_bp, url_prefix='/animals')
    app.register_blueprint(employee_bp, url_prefix='/employees')
    app.register_blueprint(role_bp, url_prefix='/roles')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
