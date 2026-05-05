"""LanceDB storage for dataset metadata."""

import json
from datetime import datetime, timezone
from typing import Any

import lancedb
import pyarrow as pa

from config import LANCEDB_TABLE_NAME, METADATA_DB_DIR


class MetadataStorage:
    """Store and retrieve JSON-LD metadata using LanceDB."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or str(METADATA_DB_DIR)
        self._db = None
        self._table = None

    @property
    def db(self) -> lancedb.DBConnection:
        """Get or create database connection."""
        if self._db is None:
            self._db = lancedb.connect(self.db_path)
        return self._db

    @property
    def table(self) -> lancedb.table.Table:
        """Get or create the metadata table."""
        if self._table is None:
            table_names = self.db.table_names()
            if LANCEDB_TABLE_NAME in table_names:
                self._table = self.db.open_table(LANCEDB_TABLE_NAME)
            else:
                self._table = self._create_table()
        return self._table

    def _create_table(self) -> lancedb.table.Table:
        """Create the metadata table with schema."""
        schema = pa.schema(
            [
                pa.field("dataset_id", pa.string()),
                pa.field("name", pa.string()),
                pa.field("description", pa.string()),
                pa.field("metadata_json", pa.string()),
                pa.field("created_at", pa.string()),
                pa.field("updated_at", pa.string()),
            ]
        )
        return self.db.create_table(LANCEDB_TABLE_NAME, schema=schema)

    def save_metadata(self, metadata: dict[str, Any]) -> str:
        """
        Save metadata to the database.

        Args:
            metadata: JSON-LD metadata dict with @id field.

        Returns:
            The dataset ID.
        """
        dataset_id = metadata.get("@id", "")
        if not dataset_id:
            raise ValueError("Metadata must have an @id field")

        now = datetime.now(timezone.utc).isoformat()

        record = {
            "dataset_id": dataset_id,
            "name": metadata.get("name", "Untitled"),
            "description": metadata.get("description", "")[:500],
            "metadata_json": json.dumps(metadata, ensure_ascii=False),
            "created_at": now,
            "updated_at": now,
        }

        # Check if exists and update, otherwise insert
        existing = self.get_metadata(dataset_id)
        if existing:
            record["created_at"] = existing.get("created_at", now)
            self.table.delete(f"dataset_id = '{dataset_id}'")

        self.table.add([record])
        return dataset_id

    def get_metadata(self, dataset_id: str) -> dict[str, Any] | None:
        """
        Retrieve metadata by dataset ID.

        Args:
            dataset_id: The @id of the dataset.

        Returns:
            The full metadata dict or None if not found.
        """
        results = (
            self.table.search().where(f"dataset_id = '{dataset_id}'").limit(1).to_list()
        )
        if not results:
            return None

        record = results[0]
        metadata = json.loads(record["metadata_json"])
        metadata["_storage"] = {
            "created_at": record["created_at"],
            "updated_at": record["updated_at"],
        }
        return metadata

    def list_datasets(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        """
        List all datasets with basic info.

        Args:
            limit: Maximum number of results.
            offset: Number of records to skip.

        Returns:
            List of dataset summaries.
        """
        try:
            df = self.table.to_pandas()
        except Exception:
            return []

        df = df.sort_values("created_at", ascending=False)
        df = df.iloc[offset : offset + limit]

        return [
            {
                "dataset_id": row["dataset_id"],
                "name": row["name"],
                "description": row["description"][:200] + "..."
                if len(row["description"]) > 200
                else row["description"],
                "created_at": row["created_at"],
            }
            for _, row in df.iterrows()
        ]

    def search_datasets(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        """
        Search datasets by name or description.

        Args:
            query: Search query string.
            limit: Maximum results to return.

        Returns:
            List of matching dataset summaries.
        """
        try:
            df = self.table.to_pandas()
        except Exception:
            return []

        query_lower = query.lower()
        mask = df["name"].str.lower().str.contains(query_lower, na=False) | df[
            "description"
        ].str.lower().str.contains(query_lower, na=False)

        results = df[mask].head(limit)

        return [
            {
                "dataset_id": row["dataset_id"],
                "name": row["name"],
                "description": row["description"][:200] + "..."
                if len(row["description"]) > 200
                else row["description"],
                "created_at": row["created_at"],
            }
            for _, row in results.iterrows()
        ]

    def delete_metadata(self, dataset_id: str) -> bool:
        """
        Delete metadata by dataset ID.

        Args:
            dataset_id: The @id of the dataset to delete.

        Returns:
            True if deleted, False if not found.
        """
        existing = self.get_metadata(dataset_id)
        if not existing:
            return False

        self.table.delete(f"dataset_id = '{dataset_id}'")
        return True

    def count_datasets(self) -> int:
        """Return total number of datasets stored."""
        try:
            return len(self.table.to_pandas())
        except Exception:
            return 0
