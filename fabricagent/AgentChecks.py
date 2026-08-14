def find_empty_fields(data, path=""):
    """
    Recursively find all keys whose value is None or an empty/whitespace string.
    Returns a list of dotted paths (with [index] for list items).
    """
    empties = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            empties.extend(find_empty_fields(value, new_path))

    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            empties.extend(find_empty_fields(item, new_path))

    else:
        # Leaf value: check if it is None or empty string
        if data is None or (isinstance(data, str) and data.strip() == ""):
            empties.append(path)

    return empties