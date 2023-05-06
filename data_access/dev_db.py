import certifi
from pymongo import MongoClient


def get_database():
    connection_string = "mongodb+srv://zR00t:zR00t123@zdev.khthxcc.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_string, tlsCAFile=certifi.where())
    return client['zdev']


if __name__ == '__main__':
    dbname = get_database()