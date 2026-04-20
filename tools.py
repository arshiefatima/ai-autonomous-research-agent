from duckduckgo_search import DDGS

def web_search(query):
    results = DDGS().text(query, max_results=3)

    text = ""
    for r in results:
        text += r["title"] + " - " + r["body"] + "\n"

    return text