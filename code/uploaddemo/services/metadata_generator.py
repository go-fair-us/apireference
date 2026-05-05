"""Metadata generator for creating JSON-LD from conversation."""

import json
import re
import uuid
from typing import Any

from config import BASE_DIR
from services.llm_client import OpenRouterClient


class MetadataGenerator:
    """Generates schema.org Dataset JSON-LD metadata from conversation."""

    def __init__(self, llm_client: OpenRouterClient):
        self.llm_client = llm_client
        self.system_prompt = self._load_system_prompt()
        self.schema_template = self._load_schema_template()

    def _load_system_prompt(self) -> str:
        """Load the system prompt from file."""
        prompt_path = BASE_DIR / "prompts" / "system_prompt.txt"
        return prompt_path.read_text()

    def _load_schema_template(self) -> dict[str, Any]:
        """Load the JSON-LD schema template."""
        template_path = BASE_DIR / "prompts" / "schema_template.json"
        return json.loads(template_path.read_text())

    def create_system_message(self) -> dict[str, str]:
        """Create the system message for the conversation."""
        return {"role": "system", "content": self.system_prompt}

    async def generate_metadata_from_conversation(
        self,
        conversation_history: list[dict[str, str]],
    ) -> dict[str, Any]:
        """
        Extract metadata from the full conversation history.

        Args:
            conversation_history: List of messages from the conversation.

        Returns:
            JSON-LD metadata dict.
        """
        extraction_prompt = """Based on our conversation, please generate the complete JSON-LD metadata for this dataset.

Output ONLY valid JSON-LD following the schema.org Dataset vocabulary. Include only fields for which information was provided. Generate a unique @id in the format "urn:uuid:{uuid}".

Required fields: @context, @type, @id, name, description

For keywords, use DefinedTerm objects when ontology terms are mentioned:
{
  "@type": "DefinedTerm",
  "name": "term name",
  "inDefinedTermSet": "ontology URL",
  "url": "term URL"
}

For creators, use Person or Organization objects:
{
  "@type": "Person",
  "name": "Name",
  "affiliation": {"@type": "Organization", "name": "Institution"}
}

For distribution, use DataDownload:
{
  "@type": "DataDownload",
  "contentUrl": "URL",
  "encodingFormat": "MIME type"
}

Output the JSON-LD now:"""

        messages = [
            self.create_system_message(),
            *conversation_history,
            {"role": "user", "content": extraction_prompt},
        ]

        response = await self.llm_client.generate_json(messages, temperature=0.2)
        return self._parse_json_response(response)

    def _parse_json_response(self, response: str) -> dict[str, Any]:
        """Parse JSON from LLM response, handling code blocks."""
        # Try to extract JSON from code blocks
        json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", response)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response

        try:
            metadata = json.loads(json_str)
        except json.JSONDecodeError:
            # Return minimal valid structure if parsing fails
            metadata = {
                "@context": "https://schema.org/",
                "@type": "Dataset",
                "@id": f"urn:uuid:{uuid.uuid4()}",
                "name": "Untitled Dataset",
                "description": "Metadata extraction failed. Please try again.",
            }

        # Ensure required fields
        if "@context" not in metadata:
            metadata["@context"] = "https://schema.org/"
        if "@type" not in metadata:
            metadata["@type"] = "Dataset"
        if "@id" not in metadata or not metadata["@id"]:
            metadata["@id"] = f"urn:uuid:{uuid.uuid4()}"

        return metadata

    def add_distribution(
        self,
        metadata: dict[str, Any],
        filename: str,
        content_url: str,
        encoding_format: str,
        content_size: int | None = None,
    ) -> dict[str, Any]:
        """
        Add a distribution entry for an uploaded file.

        Args:
            metadata: Existing metadata dict.
            filename: Name of the uploaded file.
            content_url: URL or path to access the file.
            encoding_format: MIME type or file format.
            content_size: File size in bytes.

        Returns:
            Updated metadata dict.
        """
        distribution_entry = {
            "@type": "DataDownload",
            "name": filename,
            "contentUrl": content_url,
            "encodingFormat": encoding_format,
        }
        if content_size:
            distribution_entry["contentSize"] = f"{content_size} bytes"

        if "distribution" not in metadata:
            metadata["distribution"] = []
        elif not isinstance(metadata["distribution"], list):
            metadata["distribution"] = [metadata["distribution"]]

        metadata["distribution"].append(distribution_entry)
        return metadata

    def validate_metadata(self, metadata: dict[str, Any]) -> list[str]:
        """
        Validate metadata against basic schema.org Dataset requirements.

        Args:
            metadata: Metadata dict to validate.

        Returns:
            List of validation error messages (empty if valid).
        """
        errors = []

        if metadata.get("@type") != "Dataset":
            errors.append("@type must be 'Dataset'")

        if not metadata.get("@context"):
            errors.append("@context is required")

        if not metadata.get("name"):
            errors.append("name is required")

        if not metadata.get("description"):
            errors.append("description is required")

        return errors

    def format_metadata_preview(self, metadata: dict[str, Any]) -> str:
        """Format metadata as pretty-printed JSON for display."""
        return json.dumps(metadata, indent=2, ensure_ascii=False)
