from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from dotenv import load_dotenv
load_dotenv()



os.makedirs("documents", exist_ok=True)
os.makedirs("html", exist_ok=True)



from backend.parsers.text_parser import parse_text, parse_pdf
from backend.parsers.json_parser import parse_json
from backend.parsers.html_parser import parse_html

from backend.utils.chunker import chunk_text
from backend.rag.vector_store import add_to_vector_db
from backend.agents.test_case_agent import generate_test_cases
from backend.agents.selenium_agent import generate_selenium_script

app = FastAPI()

# Allow Streamlit to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create folders if not exist
os.makedirs("documents", exist_ok=True)
os.makedirs("html", exist_ok=True)


# ------------------ ROUTES ------------------ #

@app.post("/upload_document")
async def upload_document(file: UploadFile):
    file_path = f"documents/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"status": "uploaded", "file": file.filename}


@app.post("/upload_html")
async def upload_html(file: UploadFile):
    file_path = f"html/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"status": "html uploaded", "file": file.filename}


@app.post("/build_kb")
async def build_kb():
    for filename in os.listdir("documents"):
        file_path = f"documents/{filename}"
        text = ""

        if filename.endswith(".txt") or filename.endswith(".md"):
            text = parse_text(file_path)

        elif filename.endswith(".pdf"):
            text = parse_pdf(file_path)

        elif filename.endswith(".json"):
            text = parse_json(file_path)

        # chunk text
        chunks = chunk_text(text, filename)

        # add to vector DB
        add_to_vector_db(chunks)

    # Also parse HTML for text + element structure
    for filename in os.listdir("html"):
        path = f"html/{filename}"
        html_text, elements = parse_html(path)

        html_chunks = chunk_text(html_text, filename)
        add_to_vector_db(html_chunks)

    return {"status": "Knowledge Base Built"}


@app.post("/generate_test_cases")
async def get_test_cases(query: str):
    test_cases = generate_test_cases(query)

    # Save test cases to local file for selenium agent
    with open("generated_test_cases.json", "w") as f:
        f.write(test_cases)

    return {"test_cases": test_cases}


@app.post("/generate_selenium")
async def get_selenium(test_case_id: str):
    script = generate_selenium_script(test_case_id)
    return {"script": script}
