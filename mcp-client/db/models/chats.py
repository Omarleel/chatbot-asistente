from pydantic import BaseModel
from typing import Optional, Dict

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    oauth: Optional[Dict[str, str]] = None 
    data: Optional[Dict[str, str]] = None 
