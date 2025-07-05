from pydantic import BaseModel
from typing import Optional, Dict

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    data: Optional[Dict[str, str]] = None 
