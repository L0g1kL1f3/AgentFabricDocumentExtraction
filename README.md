# Agent Fabric Document Extraction

A small installable Python package for validation helpers used by Microsoft Fabric document-extraction notebooks.

## Repository layout

```text
AgentFabricDocumentExtraction/
├── src/
│   └── fabricagent/
│       ├── __init__.py
│       └── VerifyAgent.py
├── tests/
│   └── test_verify_agent.py
├── pyproject.toml
├── README.md
└── .gitignore
```

## Local installation test

From the repository root:

```bash
python -m pip install .
python -c "from fabricagent import find_empty_fields; print(find_empty_fields({'InvoiceID': None}))"
```

Expected output:

```text
['InvoiceID']
```

## Install from GitHub

After pushing this repository to GitHub:

```bash
python -m pip install "git+https://github.com/L0g1kL1f3/AgentFabricDocumentExtraction.git@main"
```

In a Microsoft Fabric Environment YAML definition:

```yaml
dependencies:
  - pip:
      - "git+https://github.com/L0g1kL1f3/AgentFabricDocumentExtraction.git@main"
```

After publishing the Environment, attach it to the notebook and start a fresh session.

## Import in a Fabric notebook

```python
from fabricagent import find_empty_fields

record = {
    "InvoiceID": None,
    "TotalAmount": 100.0,
    "Items": []
}

missing = find_empty_fields(record)
print(missing)
```

Expected output:

```text
['InvoiceID', 'Items']
```

## Add more Python files later

Add new modules under `src/fabricagent/` and re-export their public functions or classes from `src/fabricagent/__init__.py`.

Example:

```python
# src/fabricagent/ExtractionAgent.py
def extract_document():
    return "ok"
```

Then update `src/fabricagent/__init__.py`:

```python
from .VerifyAgent import find_empty_fields
from .ExtractionAgent import extract_document

__all__ = ["find_empty_fields", "extract_document"]
```

Bump the version in both `pyproject.toml` and `src/fabricagent/__init__.py` before republishing.
