from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.messages import HumanMessage

from api.schemas import QueryRequest, QueryResponse
from src.graph.workflow import build_graph

load_dotenv()
 
app = FastAPI(title="Enterprise Support RAG API")
graph = build_graph()
 
@app.get("/health")
def health_check():
    return {"status": "ok"}
 
@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest): # CHANGED: Made function async
    inputs = {"messages": [HumanMessage(content=request.query)]}
    
    final_state = await graph.ainvoke(inputs) # CHANGED: Used await and ainvoke
    
    answer = final_state["messages"][-1].content if final_state.get("messages") else "No response generated."
    intent = final_state.get("intent", "Unknown")
    sentiment = final_state.get("sentiment", "Unknown")
    escalate = final_state.get("escalate", False)
    
    return QueryResponse(
        answer=answer,
        intent=intent,
        sentiment=sentiment,
        escalate=escalate
    )
 