import uuid
from pymongo import MongoClient
from core.config import settings
from db.models.users import User
from datetime import datetime
from bson import ObjectId

# Conexión a la base de datos
client = MongoClient(settings.mongodb_uri)
db = client["chatbot_db"]
users_collection = db["users"]
chats_collection = db["chats"]

# 👉 Crear usuario
def create_user(username: str, email: str, password: str) -> str:
    user_data = User(
        username=username,
        email=email,
        password=password
    ).model_dump()
    inserted_id = users_collection.insert_one(user_data).inserted_id
    return inserted_id

# 👉 Obtener usuario por correo
def get_user_by_email(email: str) -> dict | None:
    return users_collection.find_one({"email": email})

# 👉 Guardar tokens de Google
def save_google_tokens(email: str, google_tokens: dict):
    users_collection.update_one(
        {"email": email},
        {"$set": {"google": google_tokens}}
    )

# 👉 Guardar tokens de Slack
def save_slack_tokens(correo: str, slack_tokens: dict):
    users_collection.update_one(
        {"email": correo},
        {"$set": {"slack": slack_tokens}}
    )

# 👉 Obtener usuario completo
def get_user(email: str) -> dict | None:
    return users_collection.find_one({"email": email})

# 👉 Eliminar usuario
def delete_user(email: str):
    users_collection.delete_one({"email": email})

def save_chat(user_id: str, question: str, answer: str):
    chat = {
        "user_id": ObjectId(user_id),
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().timestamp()
    }
    inserted_id = chats_collection.insert_one(chat).inserted_id

    return inserted_id

def get_recent_chats(user_id: str, limit: int = 5):
    return list(chats_collection.find({"user_id": ObjectId(user_id)}).sort("timestamp", -1).limit(limit))
