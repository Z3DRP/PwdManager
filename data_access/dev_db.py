from pymongo import MongoClient


def get_database():
    connection_string = MongoClient("mongodb+srv://awillow1:awillow1@zdev.khthxcc.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(connection_string)
    return client['zdev']


if __name__ == '__main__':
    dbname = get_database()