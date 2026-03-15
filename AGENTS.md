# AGENTS.md

## Project Overview
This repository is a Python-based reference implementation for the NIH/NIAID \"Blueprint to Connect Data Across the NIAID Data Ecosystem\". It includes:
- Flask server example (`code/server/main.py`)
- API client examples (`code/clients/*`)
- Jupyter notebooks
- Documentation and JSON-LD examples
- No frontend, tests, or complex build process

**Tech Stack**:
- Python 3.13+
- Package manager: `uv` (`pyproject.toml`, `uv.lock`)
- Key deps: Flask, requests-cache, pandas, pyarrow, pyld, pyshacl, networkx
- Linting/Formatting: Ruff (default config)
- No testing framework configured
- No TypeScript/ESLint/Prettier

**Key Directories**:
- `code/server/`: Flask API server
- `code/clients/`: Example clients (CTG, ImmPort, simple1)
- `docs/`: Documentation, OpenAPI specs, JSON-LD examples
- `code/NIAID_API_homeEdition.ipynb`: Jupyter notebook

## Commands

### Installation
```bash
uv sync  # Installs deps from pyproject.toml into .venv
source .venv/bin/activate  # Or use `uv run`
```

### Linting & Formatting
```bash
# Check linting (errors, warnings)
ruff check .

# Fix linting issues automatically
ruff check --fix .

# Format code
ruff format .

# Check formatting
ruff format --check .
```
- Run these **after every code change**.
- No `.ruff.toml` or `[tool.ruff]` in `pyproject.toml`; uses defaults.
- Targets Python files (`**/*.py`).

### Testing
**No tests configured currently** (no `pytest`, `unittest`, `tests/` dir).

To run a single test (once added):
```bash
# If using pytest (install: uv add --dev pytest)
pytest tests/test_example.py::test_function_name -v
pytest path/to/test_file.py -k \"test_name\"  # Filter by name
```

**Verification Steps** (manual for now):
- Run server: `uv run python code/server/main.py`
- Test endpoints: `curl http://127.0.0.1:8080/id/index/datasets`
- Client: `uv run python code/clients/simple1/client.py <id>`

### Running the Project
```bash
# Server (port 8080)
uv run python code/server/main.py

# Clients
uv run python code/clients/simple1/client.py dataset_id
uv run python code/clients/CTG/cli.py --help

# Jupyter
uv run jupyter notebook code/NIAID_API_homeEdition.ipynb
```

### CI/CD
- `.github/workflows/ci.yml`: Deploys MkDocs (outdated, no `mkdocs/` dir).
- No lint/test in CI currently.

### Git Workflow
- Stage: `git add .`
- Commit: `git commit -m \"feat: add feature (why)\"`
- **NEVER commit `.venv/`, `.ruff_cache/`, `.idea/`, `secret/`, `uv.lock` changes unless intentional.**
- No pre-commit hooks.

## Code Style Guidelines

Follow **PEP 8** strictly. Mimic existing patterns.

### Naming Conventions
- **Functions/Variables/Files**: `snake_case` (e.g., `dataset_handler`, `get_dataset`, `main.py`)
- **Classes**: `CamelCase` (rarely used)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `BASE_URL`)
- **Args**: Descriptive `snake_case` (e.g., `dataset_id`)

Examples:
```python
def get_dataset(dataset_id: str) -> dict | None:
    pass
```

### Imports
- Stdlib first, then third-party, then local.
- Group `from X import Y` together.
- No unused imports.
- Prefer absolute imports.

Existing pattern:
```python
from flask import Flask, send_file, abort, jsonify, request
import os

import requests
import json
```

### Type Hints
- Use `typing` extensively (e.g., `Optional[str]`, `Dict[str, Any]`).
- Function signatures: `def func(arg: type) -> return_type:`
- Not always used; add consistently.

### Docstrings
Google/Numpy style:
```python
def get_dataset(dataset_id):
    \"\"\"
    Retrieves a dataset from the Provisium API.

    Args:
        dataset_id: The ID of the dataset to retrieve.

    Returns:
        The dataset as a JSON object, or None if an error occurs.
    \"\"\"
```

### Error Handling
- Use `try/except` for specific exceptions.
- HTTP: `response.raise_for_status()`
- Flask: `abort(400)` / `abort(404)`
- Path security: Check `os.path.abspath()` prefixes.
- CLI: `sys.exit(1)` on errors.
- Log/print errors to `sys.stderr`.

Examples:
```python
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f\"Error: {e}\", file=sys.stderr)
    return None

if not id or not id.isalnum():
    abort(400)

abs_data = os.path.abspath(\"data\")
if not abs_file.startswith(abs_data):
    abort(404)
```

### Flask Patterns
- Resource-oriented routes: `/id/dataset/<id>`
- JSON-LD responses: `mimetype=\"application/ld+json\"`
- Index endpoints: `/id/index/datasets`
- No verbs in paths.

### Security Best Practices
- Path traversal prevention (as in `main.py`).
- Validate/sanitize inputs (e.g., `isalnum()`).
- Never log secrets.
- Use `requests-cache` for caching.
- Env vars for API keys: `os.getenv(\"KEY\")`.

### JSON-LD / RDF Focus
- Responses in JSON-LD.
- Use `pyld`, `pyshacl` for validation.
- IRIs as `@id`.

### General Rules
- **No comments** unless requested.
- Max line length: 88 (Ruff default).
- Black-compatible formatting.
- If adding features, check `pyproject.toml` deps first; use `uv add <pkg>`.
- Jupyter: Use existing notebook patterns.
- Pandas/Parquet: For data export (ImmPort example).

## Cursor / Copilot Rules
None present (no `.cursor/rules/`, no `.github/copilot-instructions.md`).

## Verification Checklist for Agents
1. Run `ruff check . --fix` after edits.
2. Test manually: Run server/clients.
3. No new files unless necessary.
4. Mimic existing simplicity (short functions, direct execution).

**Length: ~150 lines** (this file is reference for agents; update as project evolves).