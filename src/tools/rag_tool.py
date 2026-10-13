import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
 
def get_rag_tool():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    persist_dir = os.path.join(base_dir, "data", "vectorstore")
    
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
    vectorstore = FAISS.load_local(persist_dir, embeddings, allow_dangerous_deserialization=True)
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    rag_tool = create_retriever_tool(
        retriever,
        "search_enterprise_policies",
        "Searches and returns excerpts from the Enterprise Support FAQ."
    )
    return rag_tool
 