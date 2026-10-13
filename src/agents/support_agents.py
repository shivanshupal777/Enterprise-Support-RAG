from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.graph.state import SupportState
from src.tools.rag_tool import get_rag_tool

load_dotenv()
 
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
rag_tool_instance = get_rag_tool()
llm_with_tools = llm.bind_tools([rag_tool_instance])
 
async def query_understanding_node(state: SupportState):
    messages = state.get("messages", [])
    user_query = messages[0].content
    prompt = f"Identify the intent of this query: '{user_query}'. Return only a 1-3 word category."
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"intent": response.content.strip()}
 
async def agent_node(state: SupportState):
    messages = state.get("messages", [])
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}
 
async def sentiment_analysis_node(state: SupportState):
    messages = state.get("messages", [])
    user_query = messages[0].content
    prompt = f"Evaluate the sentiment of this query: '{user_query}'. Return 'Positive', 'Neutral', or 'Negative'."
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"sentiment": response.content.strip()}
 
def escalation_node(state: SupportState):
    sentiment = state.get("sentiment", "")
    escalate = "Negative" in sentiment
    return {"escalate": escalate}