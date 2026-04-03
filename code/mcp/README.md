# MCP

## Bun cli tool

Bun based CLI with mcp-cli (see https://github.com/philschmid/mcp-cli)

Take a look at https://www.philschmid.de/mcp-cli for some information on how to use 
this with agents.  

## MCP Echo Server over HTTP

This is a simple implementation of a Model Context Protocol (MCP) server that exposes an "echo" tool over HTTP.
 The server uses the FastMCP library with Server-Sent Events (SSE) transport to provide HTTP access.


References:
* [Glama.ai: MCP vs API](https://glama.ai/blog/2025-06-06-mcp-vs-api)
* https://github.com/tadata-org/fastapi_mcp
* https://gofastmcp.com/getting-started/welcome
* https://www.pulsemcp.com/
* https://fast-agent.ai/

### Readme

* [A Clear Intro to MCP (Model Context Protocol) with Code Examples](https://towardsdatascience.com/clear-intro-to-mcp/)

* might be fun to use uniprot SPARQL to test with: https://sparql.uniprot.org/    Sadly, it looks like SPARQL access is limited,
but there is https://www.uniprot.org/help/api_queries which is likely some text index exposed via APIs.

## Components

1. **HTTP Echo Server** (`http_echo_server.py`): A FastMCP server that exposes an "echo" tool which returns the input text.
2. **HTTP Echo Client** (`http_echo_client.py`): A simple client that demonstrates how to interact with the server over HTTP.
3. **Bash Test Script** (`test_echo.sh`): A bash script that uses curl to test the echo tool.

## Running the Server

To run the server:

```bash
python http_echo_server.py
```

This will start the server on the default host and port (localhost:8000).

## Using the Client

To use the client:

```bash
python http_echo_client.py "Text to echo"
```

If no text is provided, it will use a default message.


## Golang

The https://github.com/mark3labs/mcp-go repo was usedin the following example:
https://itnext.io/build-a-mcp-server-using-go-to-connect-ai-agents-with-databases-1175e3be3b8c

## MCP Inspector

https://modelcontextprotocol.io/docs/tools/inspector


## Using the Bash Test Script

To use the bash test script:

```bash
./test_echo.sh "Text to echo"
```

If no text is provided, it will use a default message. The script uses curl to send a POST request to the server and parses the JSON response to extract the echoed text.

## API Details

The server exposes the following:

- **Tool**: `echo`
  - **Description**: Echoes back the input text
  - **Parameters**: `text` (string) - The text to echo back
  - **Returns**: The same text that was provided as input

## HTTP API

The server uses the MCP protocol over HTTP with the following endpoint:

- **Endpoint**: `/messages/`
- **Method**: POST
- **Content-Type**: application/json
- **Request Format**:
  ```json
  {
    "type": "callTool",
    "name": "echo",
    "arguments": {
      "text": "Text to echo"
    }
  }
  ```
- **Response Format**:
  ```json
  {
    "result": "Text to echo"
  }
  ```

## Implementation Details

The server is implemented using FastMCP with the SSE transport, which provides HTTP access. The client uses the requests library to send HTTP requests to the server.
