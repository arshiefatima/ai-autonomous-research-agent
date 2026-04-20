import faiss
import numpy as np
import ollama

documents = [
    "Tesla is profitable and leads EV market globally",
    "Rivian is early stage, not profitable, focused on EV trucks"
]

def embed(text):
    response = ollama.embeddings(
        # CHANGE 'llama3' to 'all-minilm'
        model="all-minilm", 
        prompt=text
    )
    return np.array(response["embedding"])

# This will now be much faster and won't crash your RAM
dimension = len(embed("test"))
index = faiss.IndexFlatL2(dimension)

vectors = [embed(d) for d in documents]
index.add(np.array(vectors))

def retrieve(query):
    q = embed(query)
    _, I = index.search(np.array([q]), k=2)
    return "\n".join([documents[i] for i in I[0]])