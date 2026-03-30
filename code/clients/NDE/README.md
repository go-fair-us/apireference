# NDE - NIAID Data Ecosystem API Client

A command-line interface for querying the NIAID Data Ecosystem (NDE) Hub API.

## About the NDE Hub

The NDE Hub aggregates metadata from 50+ biomedical data repositories, providing a unified search interface for discovering datasets across the NIAID ecosystem. It indexes over 8 million dataset records from sources including:

- **Generalist repositories**: Zenodo, Figshare, Dryad, Harvard Dataverse
- **Infectious disease**: VEuPathDB, ImmPort, ClinEpiDB, ImmuneSpace
- **Genomics**: NCBI BioProject, SRA, GEO
- **Specialized**: PDB, bio.tools, NDEx

**API Base URL**: `https://api.data.niaid.nih.gov/v1`

The API is built on the [BioThings](https://biothings.io/) framework and uses Elasticsearch query syntax.

## Installation

Ensure you're in the project virtual environment:

```bash
cd /path/to/apireference
uv sync
source .venv/bin/activate
```

## Usage

### Basic Query

```bash
# Search for datasets
uv run python clients/NDE/cli.py query "COVID-19" --size 5

# Search with verbose output
uv run python clients/NDE/cli.py query "malaria" --size 10 --verbose
```

### Query Syntax

The API uses Elasticsearch query syntax:

```bash
# Field-specific search
uv run python clients/NDE/cli.py query "infectiousAgent.name:SARS-CoV-2"

# Boolean queries
uv run python clients/NDE/cli.py query "COVID AND vaccine"

# Wildcard
uv run python clients/NDE/cli.py query "species.name:Homo*"

# Exists query
uv run python clients/NDE/cli.py query "_exists_:hasAPI"
```

### Facets/Aggregations

Get counts by field values:

```bash
# Facet by infectious agent
uv run python clients/NDE/cli.py query "*" --facets infectiousAgent.name --facet-size 20

# Facet by data source
uv run python clients/NDE/cli.py query "tuberculosis" --facets includedInDataCatalog.name
```

### Fetch All Results

Use the scroll API to retrieve all matching results:

```bash
# Fetch all and save to file
uv run python clients/NDE/cli.py query "hasAPI:true" --fetch-all --output results.json

# Limit maximum results
uv run python clients/NDE/cli.py query "hasAPI:true" --fetch-all --max-results 100
```

### Get Specific Document

```bash
uv run python clients/NDE/cli.py get nde-zenodo-14299481
uv run python clients/NDE/cli.py get nde-zenodo-14299481 --raw
```

### Metadata and Fields

```bash
# Get API metadata
uv run python clients/NDE/cli.py metadata

# List data sources with record counts
uv run python clients/NDE/cli.py metadata --sources

# List available fields
uv run python clients/NDE/cli.py fields

# Search for specific fields
uv run python clients/NDE/cli.py fields --search "infectious"
```

## Replicating Curl Examples

### Example: Find All Resources with APIs

The following curl command:

```bash
curl -X 'GET' \
  'https://api.data.niaid.nih.gov/v1/query?q=hasAPI%3Atrue&facet_size=10&fetch_all=true' \
  -H 'accept: */*'
```

Can be replicated with the CLI:

```bash
# Basic equivalent (first page)
uv run python clients/NDE/cli.py query "hasAPI:true" --raw

# With fetch_all to get all results
uv run python clients/NDE/cli.py query "hasAPI:true" --fetch-all --output api_resources.json

# With facets
uv run python clients/NDE/cli.py query "hasAPI:true" --facets "@type" --facet-size 10 --raw
```

### Example: Search by Condition

```bash
# Curl
curl 'https://api.data.niaid.nih.gov/v1/query?q=healthCondition.name:diabetes&size=5'

# CLI equivalent
uv run python clients/NDE/cli.py query "healthCondition.name:diabetes" --size 5
```

### Example: Get Facets for Sources

```bash
# Curl
curl 'https://api.data.niaid.nih.gov/v1/query?q=*&aggs=includedInDataCatalog.name&facet_size=50'

# CLI equivalent
uv run python clients/NDE/cli.py query "*" --facets includedInDataCatalog.name --facet-size 50
```

## Command Reference

### `query` - Search the database

| Option | Description |
|--------|-------------|
| `q` | Query string (required) |
| `--size` | Number of results (default: 10, max: 1000) |
| `--from` | Starting offset for pagination |
| `--fields` | Comma-separated list of fields to return |
| `--sort` | Sort order (e.g., `dateModified:desc`) |
| `--facets` | Comma-separated fields to aggregate |
| `--facet-size` | Number of facet buckets (default: 10) |
| `--fetch-all` | Use scroll API to fetch all results |
| `--max-results` | Limit results when using `--fetch-all` |
| `--output`, `-o` | Save results to JSON file |
| `--verbose`, `-v` | Show detailed output |
| `--raw` | Output raw JSON response |

### `get` - Retrieve a document

| Option | Description |
|--------|-------------|
| `doc_id` | Document identifier (required) |
| `--raw` | Output raw JSON |

### `metadata` - API information

| Option | Description |
|--------|-------------|
| `--sources` | List all data sources with counts |
| `--raw` | Output raw JSON |

### `fields` - List available fields

| Option | Description |
|--------|-------------|
| `--search` | Filter fields by name |
| `--raw` | Output raw JSON |

## Common Query Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Dataset name | `name:COVID` |
| `description` | Dataset description | `description:vaccine` |
| `infectiousAgent.name` | Pathogen/organism | `infectiousAgent.name:SARS-CoV-2` |
| `healthCondition.name` | Disease/condition | `healthCondition.name:tuberculosis` |
| `species.name` | Species studied | `species.name:"Homo sapiens"` |
| `measurementTechnique` | Analysis method | `measurementTechnique:RNA-seq` |
| `hasAPI` | Has programmatic access | `hasAPI:true` |
| `includedInDataCatalog.name` | Data source | `includedInDataCatalog.name:ImmPort` |
| `@type` | Resource type | `@type:Dataset` |
| `funding.funder.name` | Funding organization | `funding.funder.name:NIH` |

## Output Format

### Default Output

```
Found 17 results

[nde-bvbrc-1] PATRIC
  Source: BV-BRC
  Description: PATRIC, the Pathosystems Resource Integration Center...
  URL: https://www.bv-brc.org/
  Has API: Yes

[nde-iedb-1] Immune Epitope Database
  Source: IEDB
  ...
```

### Raw JSON Output

Use `--raw` to get the full API response:

```json
{
  "took": 5,
  "total": 17,
  "max_score": 992.13,
  "hits": [
    {
      "_id": "nde-bvbrc-1",
      "_score": 992.13,
      "name": "PATRIC",
      ...
    }
  ]
}
```

## Programmatic Usage

You can also import the client functions directly:

```python
from clients.NDE.cli import query, get_document, get_metadata, fetch_all_results

# Simple query
result = query("hasAPI:true", size=5)
print(f"Found {result['total']} results")

# Fetch all matching results
all_hits = fetch_all_results("infectiousAgent.name:SARS-CoV-2")

# Get specific document
doc = get_document("nde-zenodo-14299481")
```

## API Documentation

- **API Endpoint**: https://api.data.niaid.nih.gov/v1
- **OpenAPI Spec**: https://api.data.niaid.nih.gov/v1/spec
- **Metadata**: https://api.data.niaid.nih.gov/v1/metadata
- **Fields**: https://api.data.niaid.nih.gov/v1/metadata/fields

The API follows the BioThings API convention. For advanced query syntax, see the [Elasticsearch Query DSL documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html).
