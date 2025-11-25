import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"

def embed(text_list):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = "https://api.openai.com/v1/embeddings"
    vectors = []

    for text in text_list:
        response = requests.post(url, headers=headers, json={
            "model": EMBEDDING_MODEL,
            "input": text
        })
        data = response.json()
        if "data" in data:
            vectors.append(data["data"][0]["embedding"])
        else:
            print("Embedding error:", data)
            vectors.append([0.0] * 1536)   # failsafe vector to avoid crashes

    return vectors
