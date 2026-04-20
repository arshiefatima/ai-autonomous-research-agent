import ollama

def research_agent(query):
    # Pass the actual query to the model
    response = ollama.chat(
        model="llama3.2:1b", 
        messages=[{"role": "user", "content": f"Research this topic: {query}"}]
    )
    return response["message"]["content"]