from pymongo import MongoClient

zConn = "mongodb+srv://zR00t:zRoot1.khthxcc.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(zConn)
database = {"usr": "users", "account": "account"}
# not sure if line 8 works if now just pass instring or dot notation
# ie client["users"] or client.users
db = client[database["usr"]]
