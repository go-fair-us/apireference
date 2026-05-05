"""File upload manager for handling dataset files."""

import json
import mimetypes
import shutil
from pathlib import Path
from typing import Any

from config import ALLOWED_EXTENSIONS, DATA_DIR, MAX_FILE_SIZE_MB, UPLOADS_DIR


class FileManager:
    """Manage uploaded dataset files."""

    def __init__(self, uploads_dir: Path | None = None):
        self.uploads_dir = uploads_dir or UPLOADS_DIR
        self.uploads_dir.mkdir(parents=True, exist_ok=True)

    def get_dataset_dir(self, dataset_id: str) -> Path:
        """
        Get the upload directory for a specific dataset.

        Args:
            dataset_id: The dataset's @id (will be sanitized for filesystem).

        Returns:
            Path to the dataset's upload directory.
        """
        # Sanitize dataset_id for filesystem use
        safe_id = self._sanitize_id(dataset_id)
        dataset_dir = self.uploads_dir / safe_id
        dataset_dir.mkdir(parents=True, exist_ok=True)
        return dataset_dir

    def _sanitize_id(self, dataset_id: str) -> str:
        """Convert dataset ID to filesystem-safe string."""
        # Remove common prefixes
        safe_id = dataset_id
        for prefix in ["urn:uuid:", "https://", "http://"]:
            if safe_id.startswith(prefix):
                safe_id = safe_id[len(prefix) :]

        # Replace unsafe characters
        safe_id = "".join(c if c.isalnum() or c in "-_." else "_" for c in safe_id)
        return safe_id[:100]  # Limit length

    def save_file(
        self,
        dataset_id: str,
        source_path: str | Path,
        original_filename: str,
    ) -> dict[str, Any]:
        """
        Save an uploaded file to the dataset's directory.

        Args:
            dataset_id: The dataset's @id.
            source_path: Path to the temporary uploaded file.
            original_filename: Original filename from upload.

        Returns:
            Dict with file info (path, size, mime_type, etc.).

        Raises:
            ValueError: If file type not allowed or file too large.
        """
        source = Path(source_path)

        # Check file extension
        suffix = Path(original_filename).suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"File type '{suffix}' not allowed. "
                f"Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Check file size
        file_size = source.stat().st_size
        max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_bytes:
            raise ValueError(
                f"File too large ({file_size / 1024 / 1024:.1f} MB). "
                f"Maximum allowed: {MAX_FILE_SIZE_MB} MB"
            )

        # Copy file to dataset directory
        dataset_dir = self.get_dataset_dir(dataset_id)
        dest_path = dataset_dir / original_filename

        # Handle filename conflicts
        counter = 1
        while dest_path.exists():
            stem = Path(original_filename).stem
            dest_path = dataset_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        shutil.copy2(source, dest_path)

        # Get MIME type
        mime_type, _ = mimetypes.guess_type(str(dest_path))
        if not mime_type:
            mime_type = "application/octet-stream"

        return {
            "filename": dest_path.name,
            "path": str(dest_path),
            "size": file_size,
            "mime_type": mime_type,
            "dataset_id": dataset_id,
        }

    def list_files(self, dataset_id: str) -> list[dict[str, Any]]:
        """
        List all files for a dataset.

        Args:
            dataset_id: The dataset's @id.

        Returns:
            List of file info dicts.
        """
        dataset_dir = self.get_dataset_dir(dataset_id)
        files = []

        for file_path in dataset_dir.iterdir():
            if file_path.is_file():
                mime_type, _ = mimetypes.guess_type(str(file_path))
                files.append(
                    {
                        "filename": file_path.name,
                        "path": str(file_path),
                        "size": file_path.stat().st_size,
                        "mime_type": mime_type or "application/octet-stream",
                    }
                )

        return files

    def delete_file(self, dataset_id: str, filename: str) -> bool:
        """
        Delete a specific file from a dataset.

        Args:
            dataset_id: The dataset's @id.
            filename: Name of the file to delete.

        Returns:
            True if deleted, False if not found.
        """
        dataset_dir = self.get_dataset_dir(dataset_id)
        file_path = dataset_dir / filename

        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            return True
        return False

    def delete_dataset_files(self, dataset_id: str) -> bool:
        """
        Delete all files for a dataset.

        Args:
            dataset_id: The dataset's @id.

        Returns:
            True if directory existed and was deleted.
        """
        dataset_dir = self.get_dataset_dir(dataset_id)
        if dataset_dir.exists():
            shutil.rmtree(dataset_dir)
            return True
        return False

    def get_content_url(self, dataset_id: str, filename: str) -> str:
        """
        Generate a content URL for a file.

        For this reference implementation, returns a file:// URL.
        In production, this would return an HTTP URL.

        Args:
            dataset_id: The dataset's @id.
            filename: Name of the file.

        Returns:
            URL string for the file.
        """
        dataset_dir = self.get_dataset_dir(dataset_id)
        file_path = dataset_dir / filename
        return f"file://{file_path}"

    def save_jsonld(self, dataset_id: str, metadata: dict[str, Any]) -> str:
        """
        Save JSON-LD metadata as a file in the data directory.

        Args:
            dataset_id: The dataset's @id.
            metadata: The JSON-LD metadata dict.

        Returns:
            Path to the saved JSON-LD file.
        """
        # Create a safe filename from the dataset_id
        safe_id = self._sanitize_id(dataset_id)
        jsonld_dir = DATA_DIR / "jsonld"
        jsonld_dir.mkdir(parents=True, exist_ok=True)

        jsonld_path = jsonld_dir / f"{safe_id}.jsonld"

        with open(jsonld_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return str(jsonld_path)
