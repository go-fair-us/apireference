"""Configuration for the Dataset Metadata Chat UI."""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
METADATA_DB_DIR = DATA_DIR / "metadata_db"

# Ensure directories exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DB_DIR.mkdir(parents=True, exist_ok=True)

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "x-ai/grok-4.20")

# LanceDB configuration
LANCEDB_TABLE_NAME = "dataset_metadata"

# File upload configuration
MAX_FILE_SIZE_MB = 100
ALLOWED_EXTENSIONS = [
    ".csv",
    ".tsv",
    ".json",
    ".jsonld",
    ".xml",
    ".parquet",
    ".fasta",
    ".fastq",
    ".fa",
    ".fq",
    ".txt",
    ".md",
    ".pdf",
    ".xlsx",
    ".xls",
    ".zip",
    ".gz",
    ".tar",
    ".h5",
    ".hdf5",
]
