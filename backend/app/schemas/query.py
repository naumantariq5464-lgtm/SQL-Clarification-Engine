from pydantic import BaseModel
from typing import Optional, List

class ChatMessage(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    question: str
    history: Optional[List[ChatMessage]] = []

class QueryResponse(BaseModel):
    intent: Optional[str] = "DATABASE"
    casual_response: Optional[str] = None
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
    sql: Optional[str] = None
    accuracy_score: Optional[int] = None
