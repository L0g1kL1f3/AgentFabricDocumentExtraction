# Agent Fabric Document Extraction

Installable Python package for Microsoft Fabric notebook validation helpers.

## Install from GitHub

```bash
python -m pip install "git+https://github.com/L0g1kL1f3/AgentFabricDocumentExtraction.git@main"
```

## Import

```python
from fabricagent import find_empty_fields

missing = find_empty_fields({
    "InvoiceID": None,
    "TotalAmount": 0,
    "Items": []
})

print(missing)
# ['InvoiceID', 'Items']
```

## Fabric recommendation

For a stable Fabric Environment, build the wheel and upload it under **Custom libraries** in Full mode.

```bash
python -m pip install --upgrade build
python -m build
```

Upload the generated file from `dist/`.

## Add more modules

Place additional Python files under `src/fabricagent/`, then re-export public functions or classes from `src/fabricagent/__init__.py`. Increment the version in both `pyproject.toml` and `src/fabricagent/__init__.py` before rebuilding.
