import requests


def get_pdfs(Url,path):
    output = []
    fullPath = f"{Url}{path}"

    response = requests.get(fullPath)
    response.raise_for_status()

    items = response.json()

    for item in items:
        if item["type"] == "dir":
            output.extend(get_pdfs(Url,item["path"]))

        elif item["type"] == "file" and item["name"].lower().endswith(".pdf"):
            output.append({
                "DocumentUrl": item["download_url"],
                "SourceFolder": f"Files/{path.split('/')[-1]}",
                "FileName": item["name"]
            })

    return output