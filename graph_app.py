from langgraph.graph import StateGraph, END
import ollama
from rag_store import retrieve
from tools import web_search
from typing import TypedDict

# Global model definition to ensure we use the lightweight version everywhere
MODEL_NAME = "llama3.2:1b"

# Define a proper TypedDict for the State
class State(TypedDict):
    query: str
    plan: str
    research: str
    final: str

# PLANNER
def planner(state: State):
    print("--- 1. PLANNING ---")
    query = state["query"]

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": f"Break into steps: {query}"}]
    )

    return {"plan": response["message"]["content"]}


# RESEARCH (RAG + WEB TOOL)
def researcher(state: State):
    print("--- 2. RESEARCHING ---")
    query = state["query"]

    # Safely calling your external files
    rag_data = retrieve(query)
    web_data = web_search(query)

    combined = f"{rag_data}\n{web_data}"

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{
            "role": "user",
            "content": f"Use this data:\n{combined}\n\nQuestion:{query}"
        }]
    )

    return {"research": response["message"]["content"]}


# ANALYST
def analyst(state: State):
    print("--- 3. ANALYZING ---")
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{
            "role": "user",
            "content": f"""
Plan: {state['plan']}
Research: {state['research']}

Give final structured answer:
- Summary
- Comparison
- Recommendation
- Reason
"""
        }]
    )

    return {"final": response["message"]["content"]}


# GRAPH CONSTRUCTION
graph = StateGraph(State)

graph.add_node("planner", planner)
graph.add_node("researcher", researcher)
graph.add_node("analyst", analyst)

graph.set_entry_point("planner")
graph.add_edge("planner", "researcher")
graph.add_edge("researcher", "analyst")
graph.add_edge("analyst", END)

app = graph.compile()