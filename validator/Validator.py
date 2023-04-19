@staticmethod
def validateLogin(username, password):
    if username is None or password is None:
        return {'isValid': False, 'message': 'Username and password required'}
    elif len(username) > 20:
        return {'isValid': False, 'message': 'Username must be less than 20 characters'}
    elif len(password) > 25 or len(password) < 8:
        return {'isValid': False, 'message': 'Password must be 8 to 25 characters'}
    # can add regex for specific characters in pwd
    else:
        return {'isValid': True, 'message': None}
