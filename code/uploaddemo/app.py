"""
Dataset Metadata Chat UI - Main Chainlit Application.

A conversational interface for describing datasets and generating
JSON-LD metadata following schema.org standards.

Usage:
    chainlit run app.py
"""

import json

import chainlit as cl

from services.file_manager import FileManager
from services.llm_client import OpenRouterClient
from services.metadata_generator import MetadataGenerator
from services.storage import MetadataStorage

# Initialize services
file_manager = FileManager()
storage = MetadataStorage()


@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    try:
        llm_client = OpenRouterClient()
    except ValueError as e:
        await cl.Message(
            content=f"**Configuration Error**: {e}\n\n"
            "Please set your `OPENROUTER_API_KEY` environment variable and restart."
        ).send()
        return

    metadata_generator = MetadataGenerator(llm_client)

    # Store services in session
    cl.user_session.set("llm_client", llm_client)
    cl.user_session.set("metadata_generator", metadata_generator)
    cl.user_session.set("conversation_history", [])
    cl.user_session.set("current_metadata", None)

    # Welcome message
    welcome = """**Welcome to the Dataset Metadata Generator!**

I'll help you create standardized JSON-LD metadata for your dataset following schema.org standards.

**How it works:**
1. Tell me about your dataset through our conversation
2. I'll gather information about name, description, creators, methods, etc.
3. When ready, I'll generate JSON-LD metadata you can review
4. You can upload your dataset file(s) to include in the metadata
5. Finally, save the metadata to the database

**Let's start!** What is the name of your dataset, and what does it contain?"""

    await cl.Message(content=welcome).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle user messages."""
    llm_client: OpenRouterClient | None = cl.user_session.get("llm_client")
    metadata_generator: MetadataGenerator | None = cl.user_session.get(
        "metadata_generator"
    )
    conversation_history: list = cl.user_session.get("conversation_history", [])

    if not llm_client or not metadata_generator:
        await cl.Message(
            content="Session not initialized. Please refresh the page."
        ).send()
        return

    user_content = message.content.strip().lower()

    # Handle special commands
    if user_content in ["/generate", "/metadata", "generate metadata"]:
        await generate_and_show_metadata(metadata_generator, conversation_history)
        return

    if user_content in ["/upload", "upload file", "upload files"]:
        await request_file_upload()
        return

    if user_content in ["/save", "save metadata", "save"]:
        await save_metadata_to_db()
        return

    if user_content in ["/help", "help"]:
        await show_help()
        return

    # Add user message to history
    conversation_history.append({"role": "user", "content": message.content})

    # Build messages for LLM
    messages = [
        metadata_generator.create_system_message(),
        *conversation_history,
    ]

    # Stream response from LLM
    response_message = cl.Message(content="")
    await response_message.send()

    full_response = ""
    async for chunk in llm_client.chat_stream(messages):
        full_response += chunk
        await response_message.stream_token(chunk)

    await response_message.update()

    # Add assistant response to history
    conversation_history.append({"role": "assistant", "content": full_response})
    cl.user_session.set("conversation_history", conversation_history)


async def generate_and_show_metadata(
    metadata_generator: MetadataGenerator,
    conversation_history: list,
):
    """Generate metadata from conversation and display it."""
    if len(conversation_history) < 2:
        await cl.Message(
            content="We need to discuss your dataset a bit more first. "
            "Tell me about its name, description, and purpose."
        ).send()
        return

    status_msg = cl.Message(content="Generating metadata from our conversation...")
    await status_msg.send()

    try:
        metadata = await metadata_generator.generate_metadata_from_conversation(
            conversation_history
        )

        # Validate
        errors = metadata_generator.validate_metadata(metadata)
        if errors:
            error_list = "\n".join(f"- {e}" for e in errors)
            await cl.Message(
                content=f"**Validation Issues:**\n{error_list}\n\n"
                "Please provide more information about your dataset."
            ).send()
            return

        # Store metadata in session
        cl.user_session.set("current_metadata", metadata)

        # Display metadata
        formatted = metadata_generator.format_metadata_preview(metadata)
        await cl.Message(
            content=f"**Generated JSON-LD Metadata:**\n\n```json\n{formatted}\n```\n\n"
            "You can:\n"
            "- Continue our conversation to refine the metadata\n"
            "- Type `/upload` to add dataset files\n"
            "- Type `/save` to save to the database\n"
            "- Type `/generate` again to regenerate"
        ).send()

    except Exception as e:
        await cl.Message(content=f"Error generating metadata: {e}").send()


async def request_file_upload():
    """Request file upload from user."""
    current_metadata = cl.user_session.get("current_metadata")

    if not current_metadata:
        await cl.Message(
            content="Please generate metadata first using `/generate` before uploading files."
        ).send()
        return

    files = await cl.AskFileMessage(
        content="**Upload your dataset file(s)**\n\n"
        "Supported formats: CSV, JSON, Parquet, FASTA, Excel, PDF, and more.\n"
        "Maximum size: 100 MB per file.",
        accept=[
            "text/csv",
            "application/json",
            "text/plain",
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
            "application/gzip",
            "application/zip",
            "application/x-tar",
        ],
        max_files=5,
        max_size_mb=100,
    ).send()

    if not files:
        await cl.Message(content="No files uploaded.").send()
        return

    metadata_generator: MetadataGenerator = cl.user_session.get("metadata_generator")
    dataset_id = current_metadata.get("@id", "")

    uploaded_files = []
    for file in files:
        try:
            file_info = file_manager.save_file(
                dataset_id=dataset_id,
                source_path=file.path,
                original_filename=file.name,
            )
            uploaded_files.append(file_info)

            # Add to metadata distribution
            content_url = file_manager.get_content_url(
                dataset_id, file_info["filename"]
            )
            current_metadata = metadata_generator.add_distribution(
                metadata=current_metadata,
                filename=file_info["filename"],
                content_url=content_url,
                encoding_format=file_info["mime_type"],
                content_size=file_info["size"],
            )

        except ValueError as e:
            await cl.Message(content=f"Error uploading {file.name}: {e}").send()

    if uploaded_files:
        cl.user_session.set("current_metadata", current_metadata)

        file_list = "\n".join(
            f"- {f['filename']} ({f['size'] / 1024:.1f} KB)" for f in uploaded_files
        )
        formatted = json.dumps(current_metadata, indent=2)

        await cl.Message(
            content=f"**Files uploaded successfully:**\n{file_list}\n\n"
            f"**Updated metadata:**\n```json\n{formatted}\n```\n\n"
            "Type `/save` to save the metadata to the database."
        ).send()


async def save_metadata_to_db():
    """Save current metadata to LanceDB and as a JSON-LD file."""
    current_metadata = cl.user_session.get("current_metadata")

    if not current_metadata:
        await cl.Message(
            content="No metadata to save. Use `/generate` to create metadata first."
        ).send()
        return

    try:
        # Save to LanceDB
        dataset_id = storage.save_metadata(current_metadata)

        # Also save as JSON-LD file
        jsonld_path = file_manager.save_jsonld(dataset_id, current_metadata)

        await cl.Message(
            content=f"**Metadata saved successfully!**\n\n"
            f"Dataset ID: `{dataset_id}`\n"
            f"JSON-LD file: `{jsonld_path}`\n\n"
            "You can start describing another dataset, or type `/help` for options."
        ).send()

        # Reset session for new dataset
        cl.user_session.set("conversation_history", [])
        cl.user_session.set("current_metadata", None)

    except Exception as e:
        await cl.Message(content=f"Error saving metadata: {e}").send()


async def show_help():
    """Show available commands."""
    help_text = """**Available Commands:**

| Command | Description |
|---------|-------------|
| `/generate` | Generate JSON-LD metadata from our conversation |
| `/upload` | Upload dataset files (after generating metadata) |
| `/save` | Save metadata to the database |
| `/help` | Show this help message |

**Tips:**
- Just chat naturally about your dataset - I'll extract the relevant information
- Include details like creators, methods, dates, and licenses for richer metadata
- You can regenerate metadata anytime to incorporate new information
- Uploaded files are automatically added to the metadata's distribution field"""

    await cl.Message(content=help_text).send()


if __name__ == "__main__":
    # For development/testing
    print("Run with: chainlit run app.py")
