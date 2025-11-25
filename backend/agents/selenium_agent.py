import json
import os
from bs4 import BeautifulSoup
from backend.rag.retriever import get_context
import requests
from dotenv import load_dotenv

load_dotenv()

LLM_API = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv("OPENAI_API_KEY")


# Load previously generated test case from JSON file
def load_test_case(test_case_id):
    with open("generated_test_cases.json", "r") as f:
        test_cases = json.load(f)
    for tc in test_cases:
        if tc["test_id"] == test_case_id:
            return tc
    return None


# Read HTML UI mockup for element grounding
def read_checkout_html():
    with open("html/checkout.html", "r", encoding="utf-8") as f:
        return f.read()


def generate_selenium_script(test_case_id):

    test_case = load_test_case(test_case_id)
    if not test_case:
        return "❌ Test case not found."

    html = read_checkout_html()
    soup = BeautifulSoup(html, "html.parser")

    # extract HTML structure
    html_structure = []
    for tag in soup.find_all(True):
        html_structure.append({
            "tag": tag.name,
            "id": tag.get("id"),
            "class": tag.get("class"),
            "name": tag.get("name"),
            "text": tag.text.strip()
        })

    # get context grounded in documents
    retrieved_text = get_context(test_case["feature"])

    prompt = f"""
You are an expert in Selenium Python automation.

Generate a FULL EXECUTABLE Selenium script for the test case below.

### TEST CASE
{json.dumps(test_case, indent=2)}

### HTML STRUCTURE
{json.dumps(html_structure, indent=2)}

### PRODUCT / DOCUMENT CONTEXT
{retrieved_text}

### RULES
- Only select elements that exist in HTML structure.
- Prefer: id → name → class → XPath (only if necessary).
- Avoid made-up locators — no hallucination.
- Use ChromeDriver + waits.
- Produce a runnable `.py` script with imports.

### OUTPUT
Only send Selenium Python script — no explanations.
"""

    response = requests.post(
        LLM_API,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    script = response.json()["choices"][0]["message"]["content"]
    return script
