from photo_gallery.dao.user import UserDAO
from photo_gallery.utils.security import (hash_password, check_password)


class UserModel():
    def __init__(self):
        self.user_dao = UserDAO()

    def login(self, email, password):
        err = self.validate_email(email)
        if not err:
            hashed_password = self.get_password_from_email(email)
            if not(
                hashed_password and
                check_password(password, hashed_password)
            ):
                err['invalid_user'] = True
        return err

    def validate_email(self, email):
        err = {}
        if not email:
            err['invalid_email'] = True

        return err

    def get_password_from_email(self, email):
        user = self.user_dao.get_user_from_email(email)
        if user:
            return user.password
        return None

    def get_user_id_from_email(self, email):
        return self.user_dao.get_user_id_from_email(email)

    def get_user_from_email(self, email):
        if email:
            return self.user_dao.get_user_from_email(email)

    def register(self, user, pass_conf):
        err = self.validate(user, pass_conf)
        if not err:
            user.password = hash_password(user.password)
            inserted_id = self.user_dao.insert(user)
            if not inserted_id:
                err['db_error'] = True
                return err
            # Add id to object
            user.id = inserted_id
        return err

    def validate(self, user, pass_conf):
        err = {}
        if not user.name:
            err['empty_name'] = True
        if not user.email:
            err['empty_email'] = True
        elif self.get_user_id_from_email(user.email) is not None:
            err['duplicate_email'] = True
        if not user.password:
            err['empty_password'] = True
        if user.password != pass_conf:
            print(user.password, pass_conf)
            err['passwords_dont_match'] = True

        return err
