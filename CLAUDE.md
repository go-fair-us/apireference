# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a reference implementation for the NIH/NIAID "Blueprint to Connect Data Across the NIAID Data Ecosystem". The project demonstrates how to expose metadata through standardized APIs following JSON-LD patterns and RESTful conventions.

**Core Purpose**: Provide working examples of API servers and clients that align with the Blueprint's recommendations for connecting data across the NIAID ecosystem.

**Tech Stack**:
- Python 3.13+
- Package manager: `uv` (pyproject.toml, uv.lock)
- Key dependencies: Flask, requests-cache, pandas, pyarrow, pyld, pyshacl, networkx, folium
- Linting/Formatting: Ruff (default configuration)
- No test framework currently configured

## Repository Setup

Install dependencies using uv:

```bash
# Install/sync dependencies from pyproject.toml
uv sync

# Activate virtual environment
source .venv/bin/activate

# Or run commands directly with uv
uv run python <script>
```

## Common Commands

### Running the Server

The Flask server exposes JSON-LD documents from the `code/server/data/` directory:

```bash
# Start server on http://127.0.0.1:8080
uv run python code/server/main.py

# Test endpoints
curl http://127.0.0.1:8080/id/index/datasets
curl http://127.0.0.1:8080/id/dataset/<id>
```

### Running Clients

```bash
# Simple client (connects to local server)
uv run python code/clients/simple1/client.py <dataset_id>

# ClinicalTrials.gov CLI client
uv run python code/clients/CTG/cli.py list --query-cond "diabetes" --page-size 5
uv run python code/clients/CTG/cli.py get NCT12345678
```

### Linting and Formatting

```bash
# Check for linting issues
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Format code
ruff format .

# Check formatting without applying
ruff format --check .
```

Run linting and formatting after every code change. No custom Ruff configuration exists; uses defaults.

### Jupyter Notebooks

```bash
# Launch Jupyter
uv run jupyter notebook

# Specific notebooks
uv run jupyter notebook code/NIAID_API_homeEdition.ipynb
uv run jupyter notebook code/niaid_network.ipynb
uv run jupyter notebook code/nominatim.ipynb
```

## Architecture

### Directory Structure

- **`code/server/`**: Flask-based reference server
  - `main.py`: Server implementation with two endpoints
  - `data/`: JSON-LD documents served by the API

- **`code/clients/`**: Example API clients
  - `simple1/`: Basic client demonstrating simple API consumption
  - `CTG/`: ClinicalTrials.gov API v2 client with OpenAPI spec
  - `Immport/`: ImmPort API documentation and examples
  - `Violin/`: Additional client examples
  - `NDE/`: NIAID Data Ecosystem client (placeholder)

- **`docs/`**: Documentation and reference materials
  - `resources_data/`: JSON-LD examples (example1.json, example2.json)
  - `niaidAPILinksTable.md`: Overview of NIAID API resources
  - `mcp/`: Model Context Protocol documentation and examples
  - `FHIR.md`: FHIR-related documentation
  - Various analysis and presentation materials

- **`secret/`**: Local credentials and secrets (gitignored)

### Key Architectural Patterns

**Server Design (code/server/main.py)**:
- Two endpoints following JSON-LD/RESTful patterns:
  - `/id/dataset/<id>` - Serves individual JSON-LD documents with `application/ld+json` mimetype
  - `/id/index/datasets` - Returns JSON array of dataset URLs
- Path traversal protection using `os.path.abspath()` checks
- Validates IDs using `isalnum()` before processing
- Minimal implementation (~50 lines) to demonstrate core concepts

**Client Design**:
- Clients use `requests` library for HTTP calls
- Error handling via `try/except` with specific exception types
- CLI clients use `argparse` for command-line interfaces
- Some clients include OpenAPI/Swagger specifications (e.g., CTG)

**JSON-LD Focus**:
- All API responses should use JSON-LD encoding
- IRIs (URLs) serve as persistent identifiers (@id field)
- Examples in `docs/resources_data/example1.json` and `example2.json`
- Use `pyld` and `pyshacl` for JSON-LD operations and validation

### Model Context Protocol (MCP)

The project explores MCP as a next-generation integration pattern for AI systems. See `docs/mcp/README.md` for details.

**Key MCP Concepts**:
- **Tools**: Actions/functions AI can execute (e.g., search, query database)
- **Prompts**: Pre-written templates guiding AI behavior
- **Resources**: Data sources AI can read (files, APIs, databases)

**MCP Configuration**: `opencode.json` defines MCP server connections for local development.

**Bio-related MCP Examples**: BioMCP, BioThings, BioPortal, BVBRC API integrations.

## Code Style

Follow PEP 8 strictly. Mimic existing patterns in the codebase.

### Naming Conventions
- Functions/variables/files: `snake_case` (e.g., `get_dataset`, `dataset_id`, `main.py`)
- Classes: `CamelCase` (rarely used)
- Constants: `UPPER_SNAKE_CASE` (e.g., `BASE_URL`)

### Imports
- Standard library first, then third-party, then local imports
- Group `from X import Y` statements together
- No unused imports
- Prefer absolute imports over relative

### Type Hints
Use typing extensively for function signatures:
```python
from typing import Optional, Dict, Any

def get_dataset(dataset_id: str) -> Optional[Dict[str, Any]]:
    pass
```

### Error Handling
- Use specific exception types in `try/except` blocks
- HTTP requests: `response.raise_for_status()`
- Flask routes: `abort(400)` for bad requests, `abort(404)` for not found
- Path security: Always check `os.path.abspath()` prefixes to prevent traversal
- CLI scripts: `sys.exit(1)` on errors, print to `sys.stderr`

Example:
```python
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}", file=sys.stderr)
    return None
```

### Flask Patterns
- Resource-oriented routes: `/id/<resource_type>/<id>` (no verbs)
- JSON-LD responses: `mimetype="application/ld+json"`
- Index endpoints: `/id/index/<collection>`
- Input validation before processing (e.g., `if not id.isalnum(): abort(400)`)

### Security Best Practices
- Always validate and sanitize user inputs
- Check file paths to prevent directory traversal attacks
- Never commit secrets to git (use `secret/` directory for local credentials)
- Use environment variables for API keys: `os.getenv("API_KEY")`
- Use `requests-cache` for caching API responses

## NIAID API Ecosystem

This repository connects to various NIAID resources. Key APIs include:

- **IEDB**: Immune Epitope Database (OpenAPI/Swagger)
- **ImmPort**: Immunology database (OpenAPI/Swagger)
- **BV-BRC**: Bacterial and Viral Bioinformatics Resource Center (RESTful)
- **VeuPathDB**: Vector and eukaryotic pathogen database (RESTful + digital objects)
- **TB Portals**: Tuberculosis data platform (Token-based API)
- **NDE**: NIAID Data Ecosystem Discovery Portal (BioThings-based RESTful API)
- **ClinicalTrials.gov**: Clinical trials database (external, used for examples)

See `docs/niaidAPILinksTable.md` for a comprehensive table of NIAID API resources.

## Blueprint Alignment

When implementing or modifying APIs, ensure alignment with Blueprint requirements:

1. **Metadata Encoding**: Return JSON-LD, at least as an option
2. **IRI Structure**: Use resource-oriented IRIs (e.g., `/datasets/{id}`)
3. **HTTP Method**: Use GET for metadata retrieval
4. **Documentation**: Provide OpenAPI/Swagger specs where possible

## Development Notes

- **No testing framework** currently configured. Verification is manual via running servers/clients.
- **No CI/CD for linting/testing**. The existing `.github/workflows/ci.yml` is for MkDocs deployment (outdated).
- **Virtual environments** are managed by uv. The `.venv/` directory is gitignored.
- **Jupyter notebooks** are used for demonstrations and exploratory analysis.
- Keep implementations **minimal and focused**. This is a reference implementation showing patterns, not a production system.

## Adding Dependencies

Use uv to add packages:

```bash
# Add runtime dependency
uv add <package>

# Add development dependency
uv add --dev <package>
```

This updates `pyproject.toml` and `uv.lock` automatically.
