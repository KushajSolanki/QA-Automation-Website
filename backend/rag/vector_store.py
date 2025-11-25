import chromadb
from backend.rag.embeddings import embed

client = chromadb.Client()
db = client.get_or_create_collection(
    name="qa_kb",
    embedding_function=None
)

def add_to_vector_db(chunks):
    docs = [c["content"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [str(i) for i in range(len(docs))]

    vectors = embed(docs)

    db.add(
        documents=docs,
        metadatas=metadatas,
        ids=ids,
        embeddings=vectors
    )

def search(query_embedding, k=5):
    return db.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
