from bs4 import BeautifulSoup

def parse_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    text_content = soup.get_text(separator="\n", strip=True)

    elements = []
    for tag in soup.find_all(True):
        elements.append({
            "tag": tag.name,
            "id": tag.get("id"),
            "class": tag.get("class"),
            "name": tag.get("name"),
            "text": tag.text.strip() if tag.text else ""
        })

    return text_content, elements

