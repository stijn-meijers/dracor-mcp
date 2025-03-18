# DraCor MCP Server

A Model Context Protocol (MCP) server for interacting with the Drama Corpora Project (DraCor) API. This MCP server enables you to seamlessly analyze dramatic texts and their character networks through Claude or other LLMs.

## Overview

This project implements an MCP server using the official Model Context Protocol Python SDK that provides access to the DraCor API. It allows Claude and other LLMs to interact with dramatic text corpora, analyze character networks, retrieve play information, and generate insights about dramatic works across different languages and periods.

The project includes two implementations:

1. `dracor_mcp_server.py` - Standard implementation using the basic MCP SDK
2. `dracor_mcp_fastmcp.py` - Streamlined implementation using the FastMCP decorator-based API

## Features

- Access to DraCor APIs through a unified interface
- No authentication required (DraCor API is publicly accessible)
- Structured data models for DraCor entities
- Support for operations:
  - Corpora and play information retrieval
  - Character network analysis
  - Metrics and statistics for plays
  - Character information and spoken text
  - Comparative play analysis
  - Search functionality

## Setup

### Prerequisites

- Python 3.10 or higher
- UV package manager (recommended) or pip

### Installation with UV

1. Install UV:

```
pip install uv
```

2. Create a virtual environment and install dependencies:

```
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

3. Install the MCP server in Claude Desktop:

For standard implementation:

```
mcp install dracor_mcp_server.py
```

Or for FastMCP implementation:

```
mcp install dracor_mcp_fastmcp.py
```

### Development Mode

For testing and development:

```
mcp dev dracor_mcp_server.py
```

Or for FastMCP implementation:

```
mcp dev dracor_mcp_fastmcp.py
```

This will launch the MCP Inspector where you can test your tools and resources interactively.

### Docker (optional)

If you prefer using Docker:

```
docker build -t dracor-mcp .
docker run dracor-mcp
```

To use the FastMCP implementation instead, modify the Dockerfile's CMD line:

```
CMD ["python", "dracor_mcp_fastmcp.py"]
```

## Implementation Details

### Standard MCP Implementation

The standard implementation in `dracor_mcp_server.py` uses the core MCP SDK classes:

- `Resource` - For defining API resources
- `MCPToolImpl` - For implementing tools
- `PromptTemplate` - For creating prompt templates

### FastMCP Implementation

The FastMCP implementation in `dracor_mcp_fastmcp.py` uses a more concise decorator-based approach:

- `@mcp.resource()` - For defining API resources
- `@mcp.tool()` - For implementing tools
- `@mcp.prompt()` - For creating prompt templates

This approach results in cleaner, more maintainable code while providing the same functionality.

## Usage

Once installed in Claude Desktop, you can interact with the DraCor API through Claude. Here are some examples:

### Basic Queries

1. Ask Claude to list available corpora:

```
Can you list all available drama corpora in DraCor?
```

2. Get information about a specific play:

```
Tell me about Goethe's Faust in the German corpus
```

3. Analyze character networks:

```
Analyze the character network in Hamlet from the Shakespeare corpus
```

### Advanced Queries

1. Analyze character relationships:

```
What are the strongest character relationships in Pushkin's Boris Godunov?
```

2. Compare plays:

```
Compare Goethe's Faust and Schiller's Die Räuber in terms of network density and character count
```

3. Analyze character importance:

```
Who are the most central characters in Shakespeare's Hamlet based on speaking time and relationships?
```

### Literary Analysis Queries

1. Analyze play structure:

```
Analyze the structure of Molière's Le Misanthrope in terms of acts, scenes, and dialogue distribution
```

2. Compare authors:

```
Compare the network structures in plays by Shakespeare and Molière
```

3. Historical context:

```
Put Pushkin's Boris Godunov in its historical context and analyze how this is reflected in the character network
```

## Resources

The server exposes the following resources:

- `corpora://` - List of all available corpora
- `corpus://{corpus_name}` - Information about a specific corpus
- `plays://{corpus_name}` - List of plays in a specific corpus
- `play://{corpus_name}/{play_name}` - Information about a specific play
- `network://{corpus_name}/{play_name}` - Character network for a specific play
- `characters://{corpus_name}/{play_name}` - List of characters in a specific play
- `character://{corpus_name}/{play_name}/{character_id}` - Information about a specific character
- `metrics://{corpus_name}/{play_name}` - Metrics and statistics for a specific play
- `spoken_text://{corpus_name}/{play_name}/{character_id}` - Text spoken by a specific character

## Tools

The server provides the following tools:

- `search_plays` - Search for plays based on a query
- `compare_plays` - Compare two plays in terms of metrics and structure
- `analyze_character_relations` - Analyze character relationships in a play
- `analyze_play_structure` - Analyze the structure of a play

## Prompt Templates

The server includes these prompt templates:

- `analyze_play` - Template for analyzing a specific play
- `character_analysis` - Template for analyzing a specific character
- `network_analysis` - Template for analyzing a character network
- `comparative_analysis` - Template for comparing two plays

## How It Works

This project uses the official Model Context Protocol Python SDK to build an MCP server that exposes resources and tools that Claude can use to interact with the DraCor API.

When you ask Claude a question about dramatic texts, it can:

1. Access resources like corpora, plays, characters, and networks
2. Use tools to search, compare, and analyze plays
3. Provide insights and visualizations based on the data

The DraCor API is publicly accessible, so no authentication is required.

## Rate Limiting

Be mindful of DraCor's rate limiting policies. The server includes optional rate limiting settings that can be configured in the .env file.

## Troubleshooting

If you encounter issues:

1. Ensure you're using Python 3.10 or higher
2. Try running in development mode to debug: `mcp dev dracor_mcp_server.py` or `mcp dev dracor_mcp_fastmcp.py`
3. Check the DraCor API status at https://dracor.org/doc/api

## License

MIT

## Acknowledgements

This project uses:

- Model Context Protocol Python SDK for building the MCP server
- DraCor API for dramatic text and network data
- Drama Corpora Project (DraCor) for providing the underlying data and API
