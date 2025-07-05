from db.mongodb import db
from bson import ObjectId

users = db["users"]

def get_user_by_id(user_id: str):
    return users.find_one({"_id": ObjectId(user_id)})

def get_user_by_username(username: str):
    return users.find_one({"username": username})


def delete_user_by_username(username: str):
    return users.delete_one({"username": username})
