import re
import json

def find_empty_fields(data, path=""):
    """
    Recursively find all keys whose value is None or an empty/whitespace string.
    Returns:
        empties: list of empty field paths
        fullies: list of populated field paths
    """
    empties = []
    fullies = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key

            child_empties, child_fullies = find_empty_fields(value, new_path)
            empties.extend(child_empties)
            fullies.extend(child_fullies)

    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"

            child_empties, child_fullies = find_empty_fields(item, new_path)
            empties.extend(child_empties)
            fullies.extend(child_fullies)

    else:
        # Leaf value
        if data is None or (isinstance(data, str) and data.strip() == ""):
            empties.append(path)
        else:
            fullies.append(path)

    return empties, fullies

def llm_data_extraction(row,client,Schema):
        response = client.complete(
            messages=[
            {"role": "user",
            "content":
             f'''You are a document data extractor, the following document is a {DocumentType}, your response should only be
             in the following Json format <<< {Schema} >>> if no value is found keep the value None,
             if there are missing values in non required fields do not create None values for those fields, here is the document <<< {row["Markdown"]}>>>'''}
                ],temperature=0.0,seed=67
            ) 
        text=response.choices[0].message.content

        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)

        DocumentData =json.loads(match.group(1).strip())

        return DocumentData

def normalize(value):

    # Number
    if isinstance(value, (int, float)):
        return f"{float(value):.2f}"

    text = str(value).strip().lower()

    # Remove commas between digits (1,234.56 -> 1234.56)
    text = re.sub(r'(?<=\d),(?=\d)', '', text)

    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)

    return text


def find_incorrect_values(data, markdown):
    markdown_norm = normalize(markdown)
    incorrect = []

    def extract(obj, path=""):

        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                extract(value, new_path)

        elif isinstance(obj, list):

            # Flag empty lists
            if len(obj) == 0:
                incorrect.append({
                    "field": path,
                    "value": []
                })

            for i, item in enumerate(obj):
                extract(item, f"{path}[{i}]")

        else:
            value_norm = normalize(obj)

            if value_norm not in markdown_norm:
                incorrect.append({
                    "field": path,
                    "value": obj
                })

    extract(data)

    return incorrect
