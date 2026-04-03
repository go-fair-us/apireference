"""
FastAPI server for clinical trial data from LanceDB.

This is a reference implementation demonstrating REST-style API design
for serving clinical trial data with filtering and pagination support.

Usage:
    uvicorn main:app --host 127.0.0.1 --port 8080

Endpoints:
    GET /                    - API information
    GET /subject_id/{id}     - Get records by subject ID
    GET /site_id/{id}        - Get records by site ID
    GET /trials              - Query trials with filters
"""

import os
import re
from typing import Any, Optional

import lancedb
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# =============================================================================
# Configuration
# =============================================================================

DB_PATH = os.path.join(os.path.dirname(__file__), "clinical_trials_db")
TABLE_NAME = "trials"


# =============================================================================
# Pydantic Models
# =============================================================================


class TrialRecord(BaseModel):
    """Single clinical trial record."""

    subject_id: str = Field(..., alias="Subject_ID")
    site_id: str = Field(..., alias="Site_ID")
    age: int = Field(..., alias="Age")
    gender: str = Field(..., alias="Gender")
    ethnicity: str = Field(..., alias="Ethnicity")
    city: str = Field(..., alias="City")
    arm: str = Field(..., alias="Arm")
    enrollment_date: str = Field(..., alias="Enrollment_Date")
    status: str = Field(..., alias="Status")
    weight_kg: float = Field(..., alias="Weight_kg")
    systolic_bp: int = Field(..., alias="Systolic_BP")
    biomarker_level: float = Field(..., alias="Biomarker_Level")
    adverse_event: bool = Field(..., alias="Adverse_Event")
    efficacy_score: int = Field(..., alias="Efficacy_Score")

    model_config = {"populate_by_name": True}


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""

    data: list[dict[str, Any]]
    total: int
    limit: int
    offset: int
    has_more: bool


class APIInfo(BaseModel):
    """API information response."""

    name: str
    version: str
    description: str
    endpoints: list[dict[str, str]]


# =============================================================================
# Database Connection
# =============================================================================

_db = None
_table = None


def get_db_table():
    """Get or create database table connection using singleton pattern."""
    global _db, _table

    if _table is None:
        _db = lancedb.connect(DB_PATH)
        _table = _db.open_table(TABLE_NAME)

    return _table


# =============================================================================
# Query Utilities
# =============================================================================


def parse_range(
    value: str, field_type: type = int
) -> tuple[Optional[int | float], Optional[int | float]]:
    """
    Parse a range string in format 'min-max', 'min-', '-max', or single value.

    Args:
        value: Range string (e.g., "18-30", "18-", "-30", "25")
        field_type: Type to cast values (int or float)

    Returns:
        Tuple of (min_val, max_val) where None means unbounded

    Raises:
        HTTPException: If format is invalid
    """
    if not value:
        return None, None

    # Check if it's a single value (no hyphen, or just a negative number)
    if "-" not in value or (value.startswith("-") and value.count("-") == 1):
        try:
            val = field_type(value)
            return val, val
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid value: '{value}'. Expected a number.",
            )

    # Split on hyphen for range
    parts = value.split("-")

    # Handle different range formats
    if len(parts) == 2:
        min_str, max_str = parts
    elif len(parts) == 3 and value.startswith("-"):
        # Negative min value: "-5-10" -> ["-5", "10"]
        min_str = "-" + parts[1]
        max_str = parts[2]
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid range format: '{value}'. Use 'min-max', 'min-', '-max'.",
        )

    try:
        min_val = field_type(min_str) if min_str else None
        max_val = field_type(max_str) if max_str else None
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid range values in: '{value}'. Values must be numbers.",
        )

    # Validate min <= max if both specified
    if min_val is not None and max_val is not None and min_val > max_val:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid range: min ({min_val}) cannot be greater than max ({max_val})",
        )

    return min_val, max_val


class LanceDBQueryBuilder:
    """Builds filter expressions for LanceDB queries."""

    def __init__(self):
        self.conditions: list[str] = []

    def add_exact_match(self, field: str, value: Any) -> None:
        """Add exact match condition."""
        if value is None:
            return

        if isinstance(value, bool):
            self.conditions.append(f"{field} = {str(value).lower()}")
        elif isinstance(value, str):
            # Escape single quotes in string values
            escaped = value.replace("'", "''")
            self.conditions.append(f"{field} = '{escaped}'")
        else:
            self.conditions.append(f"{field} = {value}")

    def add_range(
        self,
        field: str,
        min_val: Optional[int | float],
        max_val: Optional[int | float],
    ) -> None:
        """Add range condition."""
        if min_val is not None:
            self.conditions.append(f"{field} >= {min_val}")
        if max_val is not None:
            self.conditions.append(f"{field} <= {max_val}")

    def build(self) -> Optional[str]:
        """Build the complete WHERE clause."""
        if not self.conditions:
            return None
        return " AND ".join(self.conditions)


# =============================================================================
# FastAPI Application
# =============================================================================

app = FastAPI(
    title="Clinical Trials API",
    description="REST API for querying clinical trial data from LanceDB",
    version="1.0.0",
)


# =============================================================================
# Exception Handlers
# =============================================================================


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=400,
        content={
            "error": "Validation Error",
            "detail": str(exc.errors()),
            "status_code": 400,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "status_code": 500,
        },
    )


# =============================================================================
# Endpoints
# =============================================================================


@app.get("/", response_model=APIInfo)
def get_api_info(request: Request) -> APIInfo:
    """Return API information and available endpoints."""
    base_url = str(request.base_url).rstrip("/")
    return APIInfo(
        name="Clinical Trials API",
        version="1.0.0",
        description="REST API for querying clinical trial data from LanceDB",
        endpoints=[
            {
                "path": "/subject_id/{id}",
                "method": "GET",
                "description": "Get all records for a specific subject",
                "example": f"{base_url}/subject_id/SUBJ-12345",
            },
            {
                "path": "/site_id/{id}",
                "method": "GET",
                "description": "Get all records for a specific site",
                "example": f"{base_url}/site_id/SITE-1",
            },
            {
                "path": "/trials",
                "method": "GET",
                "description": "Query trials with filters",
                "example": f"{base_url}/trials?age=18-65&status=Active&limit=10",
            },
        ],
    )


@app.get("/subject_id/{subject_id}")
def get_subject(subject_id: str) -> list[dict[str, Any]]:
    """
    Get all records for a specific subject.

    Args:
        subject_id: The Subject_ID to look up (e.g., SUBJ-12345)

    Returns:
        List of trial records for the subject

    Raises:
        404: Subject not found
        400: Invalid subject_id format
    """
    # Input validation
    if not subject_id or not re.match(r"^SUBJ-\d+$", subject_id):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid subject_id format: '{subject_id}'. Expected format: SUBJ-XXXXX",
        )

    table = get_db_table()

    # Query with filter
    results = table.search().where(f"Subject_ID = '{subject_id}'").limit(1000).to_list()

    if not results:
        raise HTTPException(status_code=404, detail=f"Subject not found: {subject_id}")

    return results


@app.get("/site_id/{site_id}")
def get_site(site_id: str) -> list[dict[str, Any]]:
    """
    Get all records for a specific site.

    Args:
        site_id: The Site_ID to look up (e.g., SITE-1)

    Returns:
        List of trial records for the site

    Raises:
        404: Site not found
        400: Invalid site_id format
    """
    # Input validation
    if not site_id or not re.match(r"^SITE-\d+$", site_id):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid site_id format: '{site_id}'. Expected format: SITE-X",
        )

    table = get_db_table()

    # Query with filter
    results = table.search().where(f"Site_ID = '{site_id}'").limit(10000).to_list()

    if not results:
        raise HTTPException(status_code=404, detail=f"Site not found: {site_id}")

    return results


@app.get("/trials", response_model=PaginatedResponse)
def query_trials(
    # Pagination
    limit: int = Query(
        default=100, ge=1, le=1000, description="Maximum records to return"
    ),
    offset: int = Query(default=0, ge=0, description="Number of records to skip"),
    # Range filters
    age: Optional[str] = Query(default=None, description="Age range (e.g., 18-65)"),
    systolic_bp: Optional[str] = Query(
        default=None, description="Systolic BP range (e.g., 120-140)"
    ),
    biomarker_level: Optional[str] = Query(
        default=None, description="Biomarker level range (e.g., 1.0-3.5)"
    ),
    weight_kg: Optional[str] = Query(
        default=None, description="Weight in kg range (e.g., 60-80)"
    ),
    efficacy_score: Optional[str] = Query(
        default=None, description="Efficacy score range (e.g., 5-10)"
    ),
    # Exact match filters
    gender: Optional[str] = Query(default=None, description="Gender (Male/Female)"),
    ethnicity: Optional[str] = Query(default=None, description="Ethnicity"),
    city: Optional[str] = Query(default=None, description="City"),
    arm: Optional[str] = Query(
        default=None, description="Trial arm (Placebo/Low_Dose_5mg/High_Dose_10mg)"
    ),
    status: Optional[str] = Query(
        default=None, description="Status (Completed/Active/Withdrawn)"
    ),
    adverse_event: Optional[bool] = Query(
        default=None, description="Has adverse event (true/false)"
    ),
    enrollment_date: Optional[str] = Query(
        default=None, description="Enrollment date (YYYY-MM-DD)"
    ),
) -> PaginatedResponse:
    """
    Query clinical trials with optional filters.

    Supports:
    - Range filters for numeric fields (format: min-max, min-, -max)
    - Exact match filters for categorical fields
    - Pagination via limit/offset

    Multiple filters are combined with AND logic.
    """
    builder = LanceDBQueryBuilder()

    # Parse and add range filters
    if age:
        min_val, max_val = parse_range(age, int)
        builder.add_range("Age", min_val, max_val)

    if systolic_bp:
        min_val, max_val = parse_range(systolic_bp, int)
        builder.add_range("Systolic_BP", min_val, max_val)

    if biomarker_level:
        min_val, max_val = parse_range(biomarker_level, float)
        builder.add_range("Biomarker_Level", min_val, max_val)

    if weight_kg:
        min_val, max_val = parse_range(weight_kg, float)
        builder.add_range("Weight_kg", min_val, max_val)

    if efficacy_score:
        min_val, max_val = parse_range(efficacy_score, int)
        builder.add_range("Efficacy_Score", min_val, max_val)

    # Add exact match filters
    builder.add_exact_match("Gender", gender)
    builder.add_exact_match("Ethnicity", ethnicity)
    builder.add_exact_match("City", city)
    builder.add_exact_match("Arm", arm)
    builder.add_exact_match("Status", status)
    builder.add_exact_match("Adverse_Event", adverse_event)
    builder.add_exact_match("Enrollment_Date", enrollment_date)

    # Build query
    table = get_db_table()
    where_clause = builder.build()

    # Get all matching records
    if where_clause:
        all_results = table.search().where(where_clause).limit(100000).to_list()
    else:
        all_results = table.to_pandas().to_dict(orient="records")

    total = len(all_results)

    # Apply pagination
    paginated_results = all_results[offset : offset + limit]

    return PaginatedResponse(
        data=paginated_results,
        total=total,
        limit=limit,
        offset=offset,
        has_more=(offset + limit) < total,
    )


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    import uvicorn

    print("Server listening on http://127.0.0.1:8080")
    print("API docs available at http://127.0.0.1:8080/docs")
    uvicorn.run(app, host="127.0.0.1", port=8080)
