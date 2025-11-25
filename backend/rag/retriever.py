from backend.rag.embeddings import embed
from backend.rag.vector_store import search

def get_context(query):
    q_emb = embed([query])[0]
    result = search(q_emb)
    if result["documents"]:
        return "\n\n".join(result["documents"][0])
    return ""

