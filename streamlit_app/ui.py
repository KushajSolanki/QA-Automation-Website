import streamlit as st
import requests

BACKEND_URL = "http://localhost:9000"


st.title("🧠 Autonomous QA Agent")


# -------- Upload Product Documents --------
st.header("📄 Upload Support Documents")
uploaded_docs = st.file_uploader("Upload documents (PDF / MD / JSON / TXT)", accept_multiple_files=True)

if st.button("Upload Documents"):
    if not uploaded_docs:
        st.error("Please upload documents.")
    else:
        for doc in uploaded_docs:
            files = {"file": (doc.name, doc.getvalue())}
            requests.post(f"{BACKEND_URL}/upload_document", files=files)
        st.success("Documents uploaded successfully! 👍")


# -------- Upload HTML --------
st.header("🧩 Upload checkout.html")
html_file = st.file_uploader("Upload checkout.html", type=["html"])

if st.button("Upload HTML"):
    if not html_file:
        st.error("Please upload checkout.html")
    else:
        files = {"file": (html_file.name, html_file.getvalue())}
        requests.post(f"{BACKEND_URL}/upload_html", files=files)
        st.success("HTML uploaded successfully! 🎉")


# -------- Build Knowledge Base --------
st.header("🧠 Build Knowledge Base")
if st.button("Build KB"):
    response = requests.post(f"{BACKEND_URL}/build_kb")
    try:
        msg = response.json().get("status", response.text)
        st.success(msg)
    except:
        st.success(response.text)


# -------- Generate Test Cases --------
st.header("🧪 Generate Test Cases")
query = st.text_input("Enter feature (example: discount code)")

if st.button("Get Test Cases"):
    response = requests.post(f"{BACKEND_URL}/generate_test_cases", params={"query": query})
    try:
        data = response.json()
        st.json(data)
        with open("generated_test_cases.json", "w") as f:
            f.write(response.text)
    except:
        st.error("Invalid response from backend")
        st.write(response.text)


# -------- Generate Selenium Script --------
st.header("🤖 Generate Selenium Script")
test_case_id = st.text_input("Enter Test Case ID (e.g., TC-001)")

if st.button("Generate Script"):
    response = requests.post(f"{BACKEND_URL}/generate_selenium", params={"test_case_id": test_case_id})
    if response.status_code == 200:
        try:
            st.code(response.text, language="python")
        except:
            st.write(response.text)
    else:
        st.error("Backend error generating script")
        st.write(response.text)
