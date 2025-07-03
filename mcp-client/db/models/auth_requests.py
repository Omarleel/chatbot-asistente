from pydantic import BaseModel, EmailStr

class GoogleAuthRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    google_tokens: dict

class SlackAuthRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    slack_tokens: dict
