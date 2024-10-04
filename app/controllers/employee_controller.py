from flask import jsonify, request
from app.DAL.EmployeeDAL import EmployeeDAL

class EmployeeController:
    
    @staticmethod
    def get_all_employees():
        """
        Get all employees
        ---
        tags:
          - Employee
        security:
          - bearerAuth: []
        responses:
            200:
                description: A list of employees
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: Employee ID
                                example: 1
                            name:
                                type: string
                                description: Employee Name
                                example: "John Doe"
                            email:
                                type: string
                                description: Employee Email
                                example: "john.doe@example.com"
                            role_id:
                                type: integer
                                description: Role ID
                                example: 2
        """
        employeeData = EmployeeDAL.get_all_employees()
        return jsonify([employee.to_dict() for employee in employeeData])
    
    @staticmethod
    def get_employee_by_id(id):
        """
        Get employee by ID
        ---
        tags:
          - Employee
        security:
          - bearerAuth: []
        parameters:
            - name: id
              in: path
              type: integer
              required: true
              description: ID of the employee to retrieve
        responses:
            200:
                description: Employee detail
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: Employee ID
                            example: 1
                        name:
                            type: string
                            description: Employee Name
                            example: "John Doe"
                        email:
                            type: string
                            description: Employee Email
                            example: "john.doe@example.com"
                        role_id:
                            type: integer
                            description: Role ID
                            example: 2
            404:
                description: Employee not found
        """
        employee = EmployeeDAL.get_employee_by_id(id)
        if employee: 
            return jsonify(employee.to_dict()) 
        else: 
            return jsonify({'message': 'employee not found'}), 404
    
    @staticmethod
    def create_employee():
        """
        Create a new employee
        ---
        tags:
          - Employee
        security:
          - bearerAuth: []
        parameters:
            - name: employee
              in: body
              required: true
              schema:
                  type: object
                  properties:
                      name:
                          type: string
                          description: Employee Name
                          example: "John Doe"
                      email:
                          type: string
                          description: Employee Email
                          example: "john.doe@example.com"
                      role_id:
                          type: integer
                          description: Role ID
                          example: 2
        responses:
            201:
                description: Employee created successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: Employee ID
                            example: 1
                        name:
                            type: string
                            description: Employee Name
                            example: "John Doe"
                        email:
                            type: string
                            description: Employee Email
                            example: "john.doe@example.com"
                        role_id:
                            type: integer
                            description: Role ID
                            example: 2
            400:
                description: Invalid input
            409:
                description: Employee with this name or email already exists
        """
        data = request.get_json()
        
        if not data or 'name' not in data or 'email' not in data or 'role_id' not in data:
            return jsonify({'message': 'Name, email, and role_id are required'}), 400

        new_employee = EmployeeDAL.create_employee(data)

        if new_employee:
            return jsonify(new_employee.to_dict()), 201
        else:
            return jsonify({'message': 'Employee with this name or email already exists.'}), 409

    @staticmethod
    def update_employee(id):
        """
        Update an employee
        ---
        tags:
          - Employee
        security:
          - bearerAuth: []
        parameters:
            - name: id
              in: path
              type: integer
              required: true
              description: ID of the employee to update
            - name: employee
              in: body
              required: true
              schema:
                  type: object
                  properties:
                      name:
                          type: string
                          description: New Employee Name
                          example: "John Doe"
                      email:
                          type: string
                          description: New Employee Email
                          example: "john.doe@example.com"
                      role_id:
                          type: integer
                          description: New Role ID
                          example: 2
        responses:
            200:
                description: Updated employee
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: Employee ID
                            example: 1
                        name:
                            type: string
                            description: Updated Employee Name
                            example: "John Doe"
                        email:
                            type: string
                            description: Updated Employee Email
                            example: "john.doe@example.com"
                        role_id:
                            type: integer
                            description: Updated Role ID
                            example: 2
            400:
                description: No data provided
            404:
                description: Employee not found or duplicate name/email exists
        """
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        updated_employee = EmployeeDAL.update_employee(id, data)
        
        if updated_employee:
            return jsonify(updated_employee.to_dict()), 200
        else:
            return jsonify({'message': 'Employee not found or duplicate name/email exists.'}), 409
    
    @staticmethod
    def delete_employee(id):
        """
        Delete an employee
        ---
        tags:
          - Employee
        security:
          - bearerAuth: []
        parameters:
            - name: id
              in: path
              type: integer
              required: true
              description: ID of the employee to delete
        responses:
            204:
                description: Employee terminated successfully
            404:
                description: Employee not found
        """
        deleted = EmployeeDAL.delete_employee(id)
        if deleted:
            return jsonify({'message': 'employee have been terminated'}), 204
        else:
            return jsonify({'message': 'employee not found'}), 404
