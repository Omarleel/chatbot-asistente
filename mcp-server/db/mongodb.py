from pymongo import MongoClient
from core.config import settings

client = MongoClient(settings.mongodb_uri)
db = client["chatbot_db"]
