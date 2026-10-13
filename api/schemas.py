from pydantic import BaseModel
from typing import Optional
 
class QueryRequest(BaseModel):
    session_id: Optional[str] = None
    query: str
 
class QueryResponse(BaseModel):
    answer: str
    intent: str
    sentiment: str
    escalate: bool
 