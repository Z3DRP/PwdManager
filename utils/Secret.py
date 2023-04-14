import os


@staticmethod
def get_secret():
    return os.urandom(64)

