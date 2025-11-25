from backend.rag.retriever import get_context

from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

LLM_API = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv("OPENAI_API_KEY")

def generate_test_cases(query):
    # 1. Retrieve relevant chunks
    context = get_context(query)

    # safety check if no context found
    if not context or context.strip() == "":
        return json.dumps({"error": "No relevant context found in documents."})

    # 2. LLM prompt
    prompt = f"""
You are a QA Expert. Generate detailed software test cases based ONLY on the provided documentation.

User Query:
{query}

Context From Project Documents:
{context}

Output Format (JSON list):
[
  {{
    "test_id": "TC-XXX",
    "feature": "...",
    "scenario": "...",
    "steps": ["step1", "step2", ...],
    "expected_result": "...",
    "grounded_in": "which document the rule came from"
  }}
]

Rules:
- Do NOT hallucinate features that are not in the context.
- Every test case must reference a real document in "grounded_in".
"""

    response = requests.post(
        LLM_API,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    test_cases = response.json()["choices"][0]["message"]["content"]
    return test_cases
