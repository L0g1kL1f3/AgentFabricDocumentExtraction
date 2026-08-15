"""Validation helpers for extracted document metadata."""


def find_empty_fields(data, path=""):
    """
    Recursively find values that are None, empty strings, empty lists, or empty dicts.

    Parameters
    ----------
    data : Any
        Nested dictionaries, lists, and scalar values to inspect.
    path : str
        Internal recursion path. Leave empty when calling the function.

    Returns
    -------
    list[str]
        Dotted field paths. List indexes are represented as [index].
    """
    empties = []

    if isinstance(data, dict):
        if not data and path:
            empties.append(path)
            return empties

        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            empties.extend(find_empty_fields(value, new_path))

    elif isinstance(data, list):
        if not data and path:
            empties.append(path)
            return empties

        for index, item in enumerate(data):
            new_path = f"{path}[{index}]"
            empties.extend(find_empty_fields(item, new_path))

    elif data is None or (isinstance(data, str) and data.strip() == ""):
        empties.append(path)

    return empties
