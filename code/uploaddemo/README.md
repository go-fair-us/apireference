# Dataset Metadata Chat UI

A conversational interface for describing datasets and generating JSON-LD metadata following schema.org standards. Built with Chainlit, OpenRouter, and LanceDB.

## Overview

This tool helps researchers create standardized metadata for their datasets through natural conversation. Instead of filling out forms, you simply describe your dataset and the system extracts the relevant information to generate JSON-LD metadata.

**Key Features:**
- Conversational metadata creation - describe your dataset naturally
- JSON-LD generation following schema.org Dataset vocabulary
- File upload support with automatic distribution entries
- Persistent storage in LanceDB
- Streaming responses for real-time feedback

## Quick Start

### 1. Set Your API Key

Get an API key from [OpenRouter](https://openrouter.ai/keys), then:

```bash
export OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Or copy `.env.example` to `.env` and add your key there.

### 2. Run the Application

```bash
cd code/uploaddemo
chainlit run app.py
```

### 3. Open Your Browser

Navigate to http://localhost:8000

## Usage

### Conversation Flow

1. **Describe your dataset** - Tell the assistant about your dataset's name, purpose, and contents
2. **Provide details** - Answer questions about creators, methods, dates, licensing, etc.
3. **Generate metadata** - Type `/generate` to see the JSON-LD output
4. **Upload files** - Type `/upload` to attach your dataset files
5. **Save** - Type `/save` to persist the metadata to the database

### Available Commands

| Command | Description |
|---------|-------------|
| `/generate` | Generate JSON-LD metadata from the conversation |
| `/upload` | Open file upload dialog (after generating metadata) |
| `/save` | Save metadata to LanceDB |
| `/help` | Show help message |

### Example Conversation

```
User: I have a dataset of gene expression measurements from a study on
      rheumatoid arthritis patients.