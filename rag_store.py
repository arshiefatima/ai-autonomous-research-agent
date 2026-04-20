import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# This model is tiny (under 100MB) and runs natively in the cloud
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    "Tesla is profitable and leads EV market globally",
    "Rivian is early stage, not profitable, focused on EV trucks"
]

def embed(text):
    # Generates embeddings directly in Python without Ollama
    return embed_model.encode(text).astype('float32')

# Initialize FAISS index
dimension = embed("test").shape[0]
index = faiss.IndexFlatL2(dimension)

# Add documents to index
vectors = np.array([embed(d) for d in documents])
index.add(vectors)

def retrieve(query):
    q = embed(query).reshape(1, -1)
    _, I = index.search(q, k=2)
    return "\n".join([documents[i] for i in I[0]])
