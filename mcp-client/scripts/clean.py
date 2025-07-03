from db.mongodb import db

db["users"].delete_many({})
db["chats"].delete_many({})