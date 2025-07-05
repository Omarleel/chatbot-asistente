from pydantic import BaseModel
from typing import Optional

class GoogleTokens(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expiry: Optional[str] = None