import os


@staticmethod
def get_secret():
    return os.urandom(64)


def get_salt():
    return 'BananananananananananaSalte'
