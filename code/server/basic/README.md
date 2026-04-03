# Clinical Trials API Server

A reference implementation demonstrating REST-style API design for serving clinical trial data using FastAPI and LanceDB.

## Overview

This directory contains two components:

1. **mockData.py** - Generates synthetic clinical trial data and stores it in LanceDB
2. **main.py** - FastAPI server that exposes the data via a RESTful API

## Quick Start

```bash
# Install dependencies (from project root)
uv sync

# Generate mock data (optional - if database doesn't exist)
cd code/server/basic
uv run python mockData.py --rows 500

# Start the API server
uv run python main.py
```

The server will be available at `http://127.0.0.1:8080`

## Directory Structure

```
basic/
├── README.md              # This file
├── mockData.py            # Mock data generator
├── main.py                # FastAPI server
└── clinical_trials_db/    # LanceDB database directory
    └── trials.lance/      # Trial data table
```

---

## mockData.py - Mock Data Generator

### Purpose

Generates realistic synthetic clinical trial data for testing and demonstration purposes. The data simulates a multi-arm clinical trial with demographic information, biometrics, and outcome measures.

### Usage

```bash
# Generate 100 rows (default)
uv run python mockData.py

# Generate custom number of rows
uv run python mockData.py --rows 500
uv run python mockData.py --rows 10000
```

### Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--rows` | int | 100 | Number of trial records to generate |

### Data Schema

The generator creates records with the following fields:

| Field | Type | Description | Example Values |
|-------|------|-------------|----------------|
| `Subject_ID` | string | Unique subject identifier | `SUBJ-12345` |
| `Site_ID` | string | Clinical site identifier | `SITE-1` to `SITE-10` |
| `Age` | int | Subject age in years | 18-85 |
| `Gender` | string | Subject gender | `Male`, `Female` |
| `Ethnicity` | string | Subject ethnicity | `Hispanic`, `Caucasian`, `African American`, `Asian`, `Other` |
| `City` | string | Subject city (randomized) | Any city name |
| `Arm` | string | Trial arm assignment | `Placebo`, `Low_Dose_5mg`, `High_Dose_10mg` |
| `Enrollment_Date` | string | Date enrolled (ISO format) | `2024-06-15` |
| `Status` | string | Current trial status | `Completed`, `Active`, `Withdrawn` |
| `Weight_kg` | float | Subject weight in kg | 50.0-110.0 |
| `Systolic_BP` | int | Systolic blood pressure | 110-160 |
| `Biomarker_Level` | float | Biomarker measurement | 0.1-5.5 |
| `Adverse_Event` | bool | Whether adverse event occurred | `true`/`false` (15% probability) |
| `Efficacy_Score` | int | Treatment efficacy score | 1-10 (varies by arm) |

### Data Generation Logic

- **Efficacy Score Distribution**: The efficacy score is correlated with the trial arm to simulate realistic treatment effects:
  - `High_Dose_10mg`: Score range 6-10
  - `Low_Dose_5mg`: Score range 4-8
  - `Placebo`: Score range 1-5

- **Adverse Events**: 15% probability of adverse event occurrence

- **Unique Subject IDs**: Uses Faker's unique random number generator to ensure no duplicate subjects

### Dependencies

- `lancedb` - Vector database for data storage
- `pandas` - DataFrame operations
- `faker` - Synthetic data generation
- `numpy` - Numerical operations
- `argparse` - Command line argument parsing

### Functions

#### `generate_data(num_rows: int) -> pd.DataFrame`

Generates synthetic clinical trial data.

**Parameters:**
- `num_rows`: Number of records to generate

**Returns:**
- Pandas DataFrame containing the generated data

#### `save_to_lancedb(df, db_path="./clinical_trials_db", table_name="trials")`

Saves a DataFrame to LanceDB.

**Parameters:**
- `df`: Pandas DataFrame to save
- `db_path`: Path to LanceDB database directory (default: `./clinical_trials_db`)
- `table_name`: Name of the table (default: `trials`)

---

## main.py - FastAPI Server

### Purpose

Provides a RESTful API for querying clinical trial data stored in LanceDB. Supports filtering by exact match and range queries, with pagination for large result sets.

### Usage

```bash
# Start server (default: http://127.0.0.1:8080)
uv run python main.py

# Or using uvicorn directly
uv run uvicorn main:app --host 127.0.0.1 --port 8080

# With auto-reload for development
uv run uvicorn main:app --host 127.0.0.1 --port 8080 --reload
```

### API Documentation

Once the server is running, interactive API documentation is available at:
- **Swagger UI**: http://127.0.0.1:8080/docs
- **ReDoc**: http://127.0.0.1:8080/redoc

### Endpoints

#### `GET /` - API Information

Returns API metadata and available endpoints.

**Response:**
```json
{
  "name": "Clinical Trials API",
  "version": "1.0.0",
  "description": "REST API for querying clinical trial data from LanceDB",
  "endpoints": [
    {
      "path": "/subject_id/{id}",
      "method": "GET",
      "description": "Get all records for a specific subject",
      "example": "http://127.0.0.1:8080/subject_id/SUBJ-12345"
    },
    ...
  ]
}
```

#### `GET /subject_id/{subject_id}` - Get Subject Records

Retrieves all records for a specific subject.

**Path Parameters:**
- `subject_id` (required): Subject identifier in format `SUBJ-XXXXX`

**Example:**
```bash
curl http://127.0.0.1:8080/subject_id/SUBJ-12345
```

**Response:** Array of trial records for the subject

**Error Codes:**
- `400`: Invalid subject_id format
- `404`: Subject not found

#### `GET /site_id/{site_id}` - Get Site Records

Retrieves all records for a specific clinical site.

**Path Parameters:**
- `site_id` (required): Site identifier in format `SITE-X`

**Example:**
```bash
curl http://127.0.0.1:8080/site_id/SITE-1
```

**Response:** Array of trial records for the site

**Error Codes:**
- `400`: Invalid site_id format
- `404`: Site not found

#### `GET /trials` - Query Trials

Query trials with optional filters and pagination. Multiple filters are combined with AND logic.

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `limit` | int | Max records to return (1-1000, default: 100) | `?limit=50` |
| `offset` | int | Records to skip (default: 0) | `?offset=100` |
| `age` | string | Age range filter | `?age=18-65` |
| `systolic_bp` | string | Systolic BP range filter | `?systolic_bp=120-140` |
| `biomarker_level` | string | Biomarker level range filter | `?biomarker_level=1.0-3.5` |
| `weight_kg` | string | Weight range filter | `?weight_kg=60-80` |
| `efficacy_score` | string | Efficacy score range filter | `?efficacy_score=5-10` |
| `gender` | string | Exact match on gender | `?gender=Male` |
| `ethnicity` | string | Exact match on ethnicity | `?ethnicity=Asian` |
| `city` | string | Exact match on city | `?city=Seattle` |
| `arm` | string | Exact match on trial arm | `?arm=High_Dose_10mg` |
| `status` | string | Exact match on status | `?status=Active` |
| `adverse_event` | bool | Filter by adverse event | `?adverse_event=true` |
| `enrollment_date` | string | Exact match on date | `?enrollment_date=2024-06-15` |

**Range Filter Formats:**
- `min-max`: Both bounds (e.g., `18-65`)
- `min-`: Lower bound only (e.g., `65-`)
- `-max`: Upper bound only (e.g., `-30`)
- Single value: Exact match (e.g., `25`)

**Examples:**
```bash
# Get first 10 records
curl "http://127.0.0.1:8080/trials?limit=10"

# Filter by age range and status
curl "http://127.0.0.1:8080/trials?age=18-65&status=Active"

# Filter by arm and high efficacy
curl "http://127.0.0.1:8080/trials?arm=High_Dose_10mg&efficacy_score=8-10"

# Pagination: get page 2 (records 10-19)
curl "http://127.0.0.1:8080/trials?limit=10&offset=10"

# Multiple filters combined
curl "http://127.0.0.1:8080/trials?gender=Female&age=25-45&biomarker_level=1.0-3.0&limit=20"
```

**Response:**
```json
{
  "data": [
    {
      "Subject_ID": "SUBJ-12345",
      "Site_ID": "SITE-1",
      "Age": 45,
      ...
    }
  ],
  "total": 150,
  "limit": 10,
  "offset": 0,
  "has_more": true
}
```

### Error Handling

All errors return JSON responses with consistent structure:

```json
{
  "error": "Error Type",
  "detail": "Detailed error message",
  "status_code": 400
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad request (invalid parameters)
- `404`: Resource not found
- `500`: Internal server error

### Architecture

#### Configuration

```python
DB_PATH = "./clinical_trials_db"  # LanceDB database location
TABLE_NAME = "trials"             # Table name in database
```

#### Pydantic Models

- `TrialRecord`: Schema for a single clinical trial record
- `PaginatedResponse`: Wrapper for paginated results with metadata
- `APIInfo`: Schema for API information response

#### Key Components

- **`get_db_table()`**: Singleton pattern for database connection management
- **`parse_range()`**: Utility for parsing range filter strings (e.g., "18-65")
- **`LanceDBQueryBuilder`**: Builder class for constructing LanceDB WHERE clauses

### Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `lancedb` - Vector database
- `pydantic` - Data validation

---

## Example Workflow

```bash
# 1. Generate test data
uv run python mockData.py --rows 1000

# 2. Start the server
uv run python main.py

# 3. Explore API documentation
open http://127.0.0.1:8080/docs

# 4. Query the data
curl "http://127.0.0.1:8080/trials?age=30-50&arm=High_Dose_10mg&limit=5"
```

## Development

### Running with Auto-Reload

```bash
uv run uvicorn main:app --host 127.0.0.1 --port 8080 --reload
```

### Linting

```bash
ruff check --fix code/server/basic/
ruff format code/server/basic/
```

### Regenerating Data

To regenerate the database with fresh data:

```bash
uv run python mockData.py --rows 500
```

This will overwrite the existing `clinical_trials_db/trials` table.

## License

This is a reference implementation for the NIAID Data Ecosystem Blueprint.
