from .mongo_database import MongoDatabase
from ..domain.user import User


class UserDAO():
    def __init__(self):
        self.db = MongoDatabase().instance()

    def insert(self, user):
        user_to_insert = {
            "email": user.email,
            "name": user.name,
            "password": user.password,
            "admin": user.admin
        }
        return self.db.users.insert(user_to_insert)

    def get_user_from_email(self, email):
        user = self.db.users.find_one({"email": email})
        return self.user_from_dict(user)

    def get_user_id_from_email(self, email):
        user = self.get_user_from_email(email)
        if user:
            return user.id

    def user_from_dict(self, user):
        if user:
            user_obj = User(
                user.get('name', ''),
                user.get('email', ''),
                user.get('password', ''),
                user.get('admin', '')
            )
            user_obj.id = user.get('_id', '')
            return user_obj
