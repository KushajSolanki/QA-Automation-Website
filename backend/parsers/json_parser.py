import json

def parse_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return json.dumps(data, indent=2)

