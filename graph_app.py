from langgraph.graph import StateGraph, END
from groq import Groq
import os
from rag_store import retrieve
from tools import web_search
from typing import TypedDict

# Initialize Groq Client
# Ensure you add GROQ_API_KEY to your Streamlit Cloud Secrets!
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

class State(TypedDict):
    query: str
    plan: str
    research: str
    final: str

def planner(state: State):
    print("--- 1. PLANNING ---")
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": f"Break into steps: {state['query']}"}]
    )
    return {"plan": response.choices[0].message.content}

def researcher(state: State):
    print("--- 2. RESEARCHING ---")
    query = state["query"]
    rag_data = retrieve(query)
    web_data = web_search(query)
    combined = f"{rag_data}\n{web_data}"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": f"Data:\n{combined}\n\nQuestion:{query}"}]
    )
    return {"research": response.choices[0].message.content}

def analyst(state: State):
    print("--- 3. ANALYZING ---")
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": f"Plan: {state['plan']}\nResearch: {state['research']}\nFinal structured answer (Summary, Comparison, Recommendation, Reason):"}]
    )
    return {"final": response.choices[0].message.content}

# Graph Construction remains the same
graph = StateGraph(State)
graph.add_node("planner", planner)
graph.add_node("researcher", researcher)
graph.add_node("analyst", analyst)
graph.set_entry_point("planner")
graph.add_edge("planner", "researcher")
graph.add_edge("researcher", "analyst")
graph.add_edge("analyst", END)

app = graph.compile()
