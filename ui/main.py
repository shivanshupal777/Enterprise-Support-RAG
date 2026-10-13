import requests
import streamlit as st

st.set_page_config(page_title="Enterprise Support Assistant", page_icon="🤖")
 
st.title("Enterprise Support Assistant")
 
if "messages" not in st.session_state:
    st.session_state.messages = []
 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
if prompt := st.chat_input("Type your support query here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/query",
                json={"query": prompt, "session_id": "streamlit_user"}
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer provided.")
                intent = data.get("intent", "Unknown")
                sentiment = data.get("sentiment", "Unknown")
                escalate = data.get("escalate", False)
                
                st.markdown(answer)
                
                st.caption(f"**Intent:** {intent} | **Sentiment:** {sentiment} | **Escalated:** {escalate}")
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"API Error: {response.status_code}")
        except requests.expections.RequestException:
            st.error("Failed to connect to the backend API. Is it running?")
 