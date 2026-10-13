from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from src.graph.state import SupportState
from src.agents.support_agents import (
    query_understanding_node,
    agent_node,
    sentiment_analysis_node,
    escalation_node
)
from src.tools.rag_tool import get_rag_tool
 
def should_continue(state: SupportState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "sentiment_analysis"
 
def build_graph():
    workflow = StateGraph(SupportState)
    
    workflow.add_node("query_understanding", query_understanding_node)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode([get_rag_tool()]))
    workflow.add_node("sentiment_analysis", sentiment_analysis_node)
    workflow.add_node("escalation", escalation_node)
    
    workflow.set_entry_point("query_understanding")
    workflow.add_edge("query_understanding", "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {"tools": "tools", "sentiment_analysis": "sentiment_analysis"}
    )
    workflow.add_edge("tools", "agent")
    workflow.add_edge("sentiment_analysis", "escalation")
    workflow.add_edge("escalation", END)
    
    return workflow.compile()