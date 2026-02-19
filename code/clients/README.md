
# Tooling and Architecture

## About

This section provides an overview of the code components, tooling, and architecture developed during the project. It covers client implementations, server prototypes, deployment configurations, and integration with the Model Context Protocol (MCP).


---

### Python Example: Building a Basic Client

To build a client in Python, use the `requests` library:

```python
import requests

# 1. Define the address (The Endpoint)
url = "https://jsonplaceholder.typicode.com/todos/1"

# 2. Send the "GET" request
response = requests.get(url)

# 3. Check if it worked (Status Code 200 means Success)
if response.status_code == 200:
    # 4. Convert the raw text into a Python Dictionary (JSON)
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")

```

Look closely at the code above. Before we run it (or if you just ran it in your head), think about that response.json() line.
If the server sends back a piece of data that looks like this:

```json
{"userId": 1, "id": 1, "title": "delectus aut autem", "completed": false}
```

How would you write a line of code to print only the title of the task? (Hint: Think about how you access values in a Python dictionary).
To print only the title of the task, you can use the following line of code:

```python
print(data['title'])
```

This line accesses the 'title' key within the dictionary and prints its corresponding value.





## Directory Structure

### `/clients`

Contains client implementations and examples for various APIs:

- **CTG (ClinicalTrials.gov)**: A Python-based CLI client for the ClinicalTrials.gov API v2. Includes an OpenAPI specification (ctg-oas-v2.yaml) and a command-line interface (cli.py) for querying clinical trial studies by condition, NCT ID, and other parameters. This serves as an example for API client creation and potential MCP integration.

- **Immport**: Documentation and reference materials for the ImmPort API. Contains information about the API endpoints, query structure, and filter fields for searching immunology-related studies. Includes examples of search queries with complex filter parameters for research focus, health conditions, demographics, and biospecimen types.

- **NDE**: Directory placeholder for the NDE (NIAID Data Ecosystem) client implementation.

- **simple1**: A basic Python client demonstrating simple API consumption patterns. Generated using AI assistance (Gemini) as a proof-of-concept for rapid client development from OpenAPI/Swagger specifications. Includes minimal dependencies and straightforward usage examples.

### `/server`

Contains simple server implementations that provide JSON-LD documents from a data directory, demonstrating how to expose collections with minimal code:

- **Python implementation** (main.py): Flask-based server with two endpoints:
  - `/id/dataset/<id>` - Serves individual dataset JSON-LD documents
  - `/id/index/datasets` - Returns an index of all available datasets
  
- **Go implementation** (main.go): Alternative implementation in Go providing the same functionality

Both versions run on port 8080 and demonstrate how little code is needed to expose document collections (e.g., from S3 or GitHub raw links) in a standards-aligned pattern. This was used to test client code generation based on OpenAPI/Swagger documents.

### `/deployment`

Contains containerization configuration:

- **Dockerfile**: Alpine Linux-based container configuration for deploying the Go server implementation. Demonstrates minimal, production-ready containerization with the compiled binary and data directory.

### `/mcp`

Documentation and resources related to the Model Context Protocol (MCP):

- Overview of MCP as an open-standard framework for connecting AI systems (LLMs) with external tools and data sources
- Comparison with OpenAPI and rationale for MCP (protocol-level enforcement vs. documentation, bidirectional flows, dynamic capability querying)
- Examples of bio-related MCP implementations including:
  - BioMCP (PubMed, ClinicalTrials.gov, MyVariant.info)
  - BioThings, BioPortal, and other genomics/bioinformatics tools
- Demo walkthrough showing MCP usage with BVBRC API and PubMed queries via Gemini-CLI
- Integration examples with various AI tools (VS Code/Cline, Zed, IntelliJ, Claude CLI, LibreChat)

## Key Patterns and Principles

The code demonstrates several architectural patterns:

1. **Minimal viable implementations**: Both server and client code prioritize simplicity and clarity over feature completeness
2. **Standards alignment**: Server endpoints follow JSON-LD patterns and RESTful conventions
3. **AI-assisted development**: Examples of using LLM tools to rapidly prototype API clients from specifications
4. **Multiple implementation languages**: Python and Go versions showing language flexibility
5. **Containerization**: Docker-based deployment for portability and consistency
6. **Protocol exploration**: Investigation of MCP as a next-generation integration pattern for AI systems