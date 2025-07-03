from pydantic import BaseModel, EmailStr
from typing import Optional
from db.models.google_tokens import GoogleTokens
from db.models.slack_tokens import SlackTokens

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    google: Optional[GoogleTokens] = None
    slack: Optional[SlackTokens] = None
