from random import seed
from random import randint

class Account:

    def __init__(self, userId, name, email, password):
        self._userid = userId
        self._name = name
        self._email = email
        self._password = password
        # TODO add self.extra_field stores ['fieldName', 'value']

    def get_userid(self):
        return self._userid

    def get_account_name(self):
        return self._name

    def get_account_email(self):
        return self._email

    def get_account_password(self):
        return self._password