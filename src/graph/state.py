from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
 
class SupportState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    intent: str
    sentiment: str
    escalate: bool
 