class User():
    def __init__(self, name, email, password, admin):
        self._id = None
        self._name = name
        self._email = email
        self._password = password
        self._admin = admin

    def __str__(self):
        return (self._name)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def admin(self):
        return self._admin

    @admin.setter
    def admin(self, value):
        self._admin = value
