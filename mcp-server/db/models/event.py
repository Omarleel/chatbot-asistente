from db.mongodb import db
from bson import ObjectId

events = db["events"]

def create_event(user_id: str, title: str, start: str, end: str, google_event_id: str = ""):
    event = {
        "user_id": ObjectId(user_id),
        "title": title,
        "start": start,
        "end": end,
        "google_event_id": google_event_id,
    }
    return events.insert_one(event).inserted_id
