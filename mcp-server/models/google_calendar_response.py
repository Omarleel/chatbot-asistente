from pydantic import BaseModel
from typing import Optional

class CalendarResponse(BaseModel):
    success: bool
    message: str
    url: Optional[str] = None
