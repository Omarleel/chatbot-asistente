
from pydantic import BaseModel
from typing import Optional

class SlackTokens(BaseModel):
    access_token: str
    bot_user_id: Optional[str] = None
    team_id: Optional[str] = None