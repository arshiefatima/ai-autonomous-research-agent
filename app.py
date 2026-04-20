import ollama

def load_data():
    with open("data.txt", "r") as f:
        return f.read()


# 1️⃣ PLANNER AGENT
def planner_agent(query):
    prompt = f"""
You are a planner agent.

Break this task into steps:
{query}

Return steps like:
1.
2.
3.
"""
    response = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


# 2️⃣ RESEARCH AGENT
def research_agent(query, context):
    prompt = f"""
You are a research agent.

Extract ONLY factual information from the context.

Context:
{context}

Question:
{query}

Return clean facts only.
"""
    response = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


# 3️⃣ ANALYST AGENT
def analyst_agent(query, research_data):
    prompt = f"""
You are a senior business analyst.

Based on the facts below, give final analysis:

Facts:
{research_data}

Task:
{query}

Return:
- Summary
- Comparison
- Recommendation
- Reason
"""
    response = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


# 🔁 PIPELINE CONTROLLER
def run_system(query):
    print("\n🔵 Planning...\n")
    plan = planner_agent(query)
    print(plan)

    print("\n🟡 Researching...\n")
    context = load_data()
    research = research_agent(query, context)
    print(research)

    print("\n🟢 Analyzing...\n")
    final = analyst_agent(query, research)

    return final


if __name__ == "__main__":
    user_query = input("Enter query: ")
    result = run_system(user_query)
    print("\n\n🔥 FINAL RESULT 🔥\n")
    print(result)