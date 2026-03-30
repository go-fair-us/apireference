# Code

## About

This directory contains the reference implementation for the NIH/NIAID "Blueprint to Connect Data Across the NIAID Data Ecosystem". It provides working examples of API servers and clients that demonstrate how to expose metadata through standardized APIs following JSON-LD patterns and RESTful conventions.

The implementation emphasizes simplicity and clarity—showing patterns rather than building production systems.

## Quick Start

```bash
# Install dependencies
uv sync

# Run the reference server
cd server
uv run python main.py

# Test the server
curl http://127.0.0.1:8080/id/index/datasets
curl http://127.0.0.1:8080/id/dataset/1

# Run a client example
uv run python clients/simple1/client.py 1
```

## Directory Structure

```
code/
├── server/           # Flask-based reference server
├── clients/          # Example API client implementations
│   ├── simple1/      # Basic reference client
│   ├── CTG/          # ClinicalTrials.gov CLI client
│   ├── Immport/      # ImmPort immunology database clients
│   ├── Violin/       # Vaccine Investigation Network client
│   └── NDE/          # NIAID Data Ecosystem (placeholder)
├── input/            # Input data and resource listings
└── *.ipynb           # Jupyter notebooks for demonstrations
```

---

## Server

**Location:** `server/`

A minimal Flask server (~50 lines) demonstrating JSON-LD exposure with two endpoints:

| Endpoint | Description |
|----------|-------------|
| `/id/dataset/<id>` | Serves individual JSON-LD documents |
| `/id/index/datasets` | Returns JSON array of available dataset URLs |

**Features:**
- Input validation (`isalnum()` check)
- Path traversal protection
- `application/ld+json` MIME type

**Data Files:**
- `server/data/1.json` - Minimal sample dataset
- `server/data/3.json` - Comprehensive example with DOIs, ORCID, ROR identifiers

---

## Clients

### simple1 - Basic Reference Client

**Location:** `clients/simple1/`

Minimal demonstration of API consumption using the `requests` library. Shows error handling patterns and basic HTTP request flow.

```bash
uv run python clients/simple1/client.py <dataset_id>
```

### CTG - ClinicalTrials.gov CLI

**Location:** `clients/CTG/`

Full-featured CLI for the ClinicalTrials.gov API v2 with support for:
- Study listing with condition filtering
- Multiple output formats (JSON, CSV)
- Pagination
- Optional LLM integration for analysis

```bash
# List diabetes studies
uv run python clients/CTG/cli.py list --query-cond "diabetes" --page-size 5

# Get specific study
uv run python clients/CTG/cli.py get NCT12345678
```

**Files:**
- `cli.py` - Main CLI implementation
- `ctg-oas-v2.yaml` - OpenAPI v2 specification (80 KB)

### Immport - ImmPort Database Clients

**Location:** `clients/Immport/`

Two client implementations for the ImmPort immunology database:

| File | Description |
|------|-------------|
| `immportSeronetClient.py` | SeroNet study search with age filtering |
| `immportStudies.py` | Full-featured studies search with Parquet export |

```bash
# Run ImmPort client
uv run python clients/Immport/immportStudies.py --search "COVID" --page-size 10
```

### Violin - Vaccine Investigation Network

**Location:** `clients/Violin/`

Queries pathogen and vaccine data from the VIOLIN database, converting XML responses to JSON-LD.

```bash
uv run python clients/Violin/client.py p_32 introduction
uv run python clients/Violin/client.py --vaccine v_36 description
```

> **Note:** This service is currently broken and included for demonstration purposes only.

### NDE - NIAID Data Ecosystem

**Location:** `clients/NDE/`

CLI client for the NDE Hub API, which aggregates metadata from 50+ biomedical data repositories (8M+ records).

```bash
# Search for datasets with APIs
uv run python clients/NDE/cli.py query "hasAPI:true" --size 5

# Search for COVID datasets
uv run python clients/NDE/cli.py query "COVID-19" --verbose

# Get facets for infectious agents
uv run python clients/NDE/cli.py query "*" --facets infectiousAgent.name --facet-size 20

# Fetch all results matching a query
uv run python clients/NDE/cli.py query "hasAPI:true" --fetch-all --output results.json

# List data sources
uv run python clients/NDE/cli.py metadata --sources
```

**API Base URL:** `https://api.data.niaid.nih.gov/v1`

---

## Jupyter Notebooks

Interactive notebooks for demonstrations and exploratory analysis:

| Notebook | Description |
|----------|-------------|
| `NIAID_API_homeEdition.ipynb` | Main educational notebook demonstrating NIAID API interactions |
| `niaid_network.ipynb` | Network visualization and analysis of NIAID APIs |
| `nde_viz.ipynb` | NIAID Data Ecosystem visualization |
| `nominatim.ipynb` | Geolocation and mapping demonstrations |

```bash
uv run jupyter notebook
```

---

## Input Data

**Location:** `input/`

| File | Description |
|------|-------------|
| `example.json` | Full NDE resource catalog example with BioSchemas |
| `NDE_Resource_list_full.txt` | Complete list of NDE resources |
| `NDE_Resource_list.txt` | Filtered resource list |

---

## File Directory

### Root Level

| File | Size | Description |
|------|------|-------------|
| `README.md` | - | This file |
| `NIAID_API_homeEdition.ipynb` | 253 KB | Main educational notebook |
| `niaid_network.ipynb` | 890 KB | Network visualization notebook |
| `nde_viz.ipynb` | 48 KB | NDE visualization notebook |
| `nominatim.ipynb` | 35 KB | Geolocation notebook |
| `niaid_network.html` | 14 KB | Interactive HTML network visualization |
| `niaid_api_network.png` | 677 KB | Static network diagram |

### Server (`server/`)

| File | Description |
|------|-------------|
| `main.py` | Flask server implementation |
| `README.md` | Server documentation |
| `data/1.json` | Minimal sample dataset |
| `data/3.json` | Comprehensive example dataset |

### Clients (`clients/`)

| File | Description |
|------|-------------|
| `README.md` | Client overview and patterns |
| `shellScraping.md` | Bash commands for JSON-LD extraction |
| `simple1/client.py` | Basic reference client |
| `simple1/README.md` | Simple client documentation |
| `CTG/cli.py` | ClinicalTrials.gov CLI |
| `CTG/ctg-oas-v2.yaml` | OpenAPI specification |
| `CTG/README.md` | CTG client documentation |
| `Immport/immportSeronetClient.py` | SeroNet client |
| `Immport/immportStudies.py` | ImmPort studies client |
| `Immport/results.parquet` | Sample output data |
| `Immport/README.md` | ImmPort documentation |
| `Violin/client.py` | VIOLIN database client |
| `Violin/README.md` | VIOLIN documentation |
| `NDE/cli.py` | NIAID Data Ecosystem CLI client |
| `NDE/README.md` | NDE client documentation |

### Input (`input/`)

| File | Description |
|------|-------------|
| `example.json` | NDE resource catalog example |
| `NDE_Resource_list_full.txt` | Full NDE resource list |
| `NDE_Resource_list.txt` | Filtered NDE resource list |

---

## Technology Stack

- **Language:** Python 3.13+
- **Package Manager:** uv
- **Server:** Flask
- **HTTP:** requests, requests-cache
- **Data Processing:** pandas, pyarrow
- **JSON-LD:** pyld, pyshacl
- **Linting:** Ruff

---

## NIAID API Ecosystem Coverage

This codebase demonstrates integration with:

| API | Type | Client Location |
|-----|------|-----------------|
| ClinicalTrials.gov | External clinical trials | `clients/CTG/` |
| ImmPort | Immunology database | `clients/Immport/` |
| VIOLIN | Vaccine/pathogen database | `clients/Violin/` |
| NDE | NIAID Data Ecosystem (8M+ records) | `clients/NDE/` |

---

## Key Patterns

1. **Server Design:** Minimal Flask with strict input validation and JSON-LD output
2. **Client Design:** `requests` library with proper error handling and CLI interfaces
3. **Data Format:** JSON-LD as standard metadata encoding with Schema.org vocabulary
4. **Identifiers:** Support for DOI, ORCID, ROR, and other persistent identifiers

See the project root `CLAUDE.md` for detailed architectural guidance.
