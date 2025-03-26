import json

def save(file_path: str, results: list):
    with open(file_path, 'w') as file:
        data = json.dumps(results, indent=4)
        file.write(data)