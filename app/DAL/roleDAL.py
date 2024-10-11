# app/dal/role_dal.py
from app import db
from app.models.role import Role

class RoleDAL:
    @staticmethod
    def get_all_roles():
        return Role.query.all()

    @staticmethod
    def get_role_by_id(role_id):
        role = db.session.get(Role, role_id)
        return role

    @staticmethod
    def add_role(name):
        new_role = Role(name=name)
        db.session.add(new_role)
        db.session.commit()
        return new_role

    @staticmethod
    def update_role(role_id, name):
        role = db.session.get(Role, role_id)
        if role:
            role.name = name
            db.session.commit()
        return role

    @staticmethod
    def delete_role(role_id):
        role = db.session.get(Role, role_id)
        if role:
            db.session.delete(role)
            db.session.commit()
        return role
