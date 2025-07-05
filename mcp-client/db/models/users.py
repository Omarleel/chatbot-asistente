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

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

