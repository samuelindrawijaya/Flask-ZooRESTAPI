from flask import Blueprint
from app.controllers.AuthController import AuthController
from app.controllers.anima_controller import AnimalController
from app.controllers.employee_controller import EmployeeController
from app.controllers.role_controller import RoleController
from app.jwtdecorator import admin_required, token_required 

# Animal Routing 
animal_bp = Blueprint('animals', __name__)

animal_bp.add_url_rule('/', view_func=AnimalController.get_all_animals, methods=['GET'])
animal_bp.add_url_rule('/<int:id>', view_func=AnimalController.get_animal_by_id, methods=['GET'])
animal_bp.add_url_rule('/', view_func=AnimalController.create_animal, methods=['POST'])
animal_bp.add_url_rule('/<int:id>', view_func=AnimalController.update_animal, methods=['PUT'])
animal_bp.add_url_rule('/<int:id>', view_func=AnimalController.delete_animal, methods=['DELETE'])


# Employee Routing Protected (token_required)
employee_bp = Blueprint('employees', __name__)

employee_bp.add_url_rule('/', view_func=token_required(EmployeeController.get_all_employees), methods=['GET'])
employee_bp.add_url_rule('/<int:id>', view_func=token_required(EmployeeController.get_employee_by_id), methods=['GET'])
employee_bp.add_url_rule('/', view_func=token_required(EmployeeController.create_employee), methods=['POST'])
employee_bp.add_url_rule('/<int:id>', view_func=token_required(EmployeeController.update_employee), methods=['PUT'])
employee_bp.add_url_rule('/<int:id>', view_func=token_required(EmployeeController.delete_employee), methods=['DELETE'])

# Role Routing 
role_bp = Blueprint('roles', __name__)

role_bp.add_url_rule('/', view_func=token_required(admin_required(RoleController.get_all_roles)), methods=['GET'])

role_bp.add_url_rule('/<int:id>', view_func=token_required(admin_required(RoleController.get_role_by_id)), methods=['GET'])

role_bp.add_url_rule('/', view_func=token_required(admin_required(RoleController.add_role)), methods=['POST'])
role_bp.add_url_rule('/<int:id>', view_func=token_required(admin_required(RoleController.update_role)), methods=['PUT'])
role_bp.add_url_rule('/<int:id>', view_func=token_required(admin_required(RoleController.delete_role)), methods=['DELETE'])

# Auth Routing 
auth_bp = Blueprint('login', __name__)
auth_bp.add_url_rule('/', view_func=AuthController.login, methods=['POST'])
auth_bp.add_url_rule('/register', view_func=AuthController.create_user, methods=['POST']) # for test creating user
