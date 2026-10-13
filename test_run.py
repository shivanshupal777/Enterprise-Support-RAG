from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from src.graph.workflow import build_graph
 
load_dotenv()
 
def run_test():
    app = build_graph()
    
    query = "I requested a refund yesterday. How long does it take?"
    print(f"Testing Query: {query}\n")
    
    inputs = {"messages": [HumanMessage(content=query)]}
    
    for output in app.stream(inputs, stream_mode="updates"):
        for node_name, state_update in output.items():
            print(f"--- Output from node: {node_name} ---")
            if "intent" in state_update:
                print(f"Intent: {state_update['intent']}")
            if "sentiment" in state_update:
                print(f"Sentiment: {state_update['sentiment']}")
            if "escalate" in state_update:
                print(f"Escalate to Human: {state_update['escalate']}")
            if "messages" in state_update:
                last_msg = state_update["messages"][-1]
                if last_msg.content:
                    print(f"Response: {last_msg.content}")
            print("\n")
 
if __name__ == "__main__":
    run_test()
 