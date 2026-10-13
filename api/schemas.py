
from pydantic import BaseModel


class QueryRequest(BaseModel):
    session_id: str | None = None
    query: str
 
class QueryResponse(BaseModel):
    answer: str
    intent: str
    sentiment: str
    escalate: bool
 