# DraCor MCP Server

A Model Context Protocol (MCP) server for interacting with the Drama Corpora Project (DraCor) API. This MCP server enables you to seamlessly analyze dramatic texts and their character networks through Claude or other LLMs.

## Overview

This project implements an MCP server using the official Model Context Protocol Python SDK that provides access to the DraCor API v1. It allows Claude and other LLMs to interact with dramatic text corpora, analyze character networks, retrieve play information, and generate insights about dramatic works across different languages and periods.

The project includes two implementations:

1. `dracor_mcp_fastmcp.py` - Streamlined implementation using the FastMCP decorator-based API with v1 API

## Features

- Access to DraCor API v1 through a unified interface
- No authentication required (DraCor API is publicly accessible)
- Structured data models for DraCor entities
- Support for operations:
  - Corpora and play information retrieval
  - Character network analysis
  - Metrics and statistics for plays
  - Character information and spoken text
  - Comparative play analysis
  - Search functionality
  - Character relationship data
  - Network data in multiple formats (CSV, GEXF, GraphML)
  - Gender analysis across plays
  - **Full text retrieval in plain text and TEI XML formats**
  - **Complete play text analysis**

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

For standard implementation (v0 API):

```
mcp install dracor_mcp_server.py
```

Or for FastMCP implementation with v1 API (recommended):

```
mcp install dracor_mcp_fastmcp.py
```

### Development Mode

For testing and development:

```
mcp dev dracor_mcp_server.py
```

Or for FastMCP implementation with v1 API (recommended):

```
mcp dev dracor_mcp_fastmcp.py
```

This will launch the MCP Inspector where you can test your tools and resources interactively.

### Claude Configuration

You can also directly configure Claude to use the DraCor MCP server by adding the following to your Claude configuration file:

```json
{
  "tools": {
    "DraCor API v1": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "requests",
        "--with",
        "pydantic",
        "--with",
        "python-multipart",
        "mcp",
        "run",
        "/path/to/dracor-mcp/dracor_mcp_fastmcp.py"
      ]
    }
  }
}
```

Replace `/path/to/dracor-mcp/` with the actual path to your dracor-mcp directory. This configuration uses `uv run` to execute the MCP server with the necessary dependencies without requiring a prior installation.

### Docker (optional)

If you prefer using Docker:

```
docker build -t dracor-mcp .
docker run dracor-mcp
```

To use the FastMCP implementation with v1 API instead:

```
docker run -e IMPLEMENTATION=fastmcp dracor-mcp
```

## Implementation Details

### Standard MCP Implementation (v0 API)

The standard implementation in `dracor_mcp_server.py` uses the core MCP SDK classes with the older v0 API:

- `Resource` - For defining API resources
- `MCPToolImpl` - For implementing tools
- `PromptTemplate` - For creating prompt templates

### FastMCP Implementation (v1 API)

The FastMCP implementation in `dracor_mcp_fastmcp.py` uses a more concise decorator-based approach with the current v1 API:

- `@mcp.resource()` - For defining API resources
- `@mcp.tool()` - For implementing tools
- `@mcp.prompt()` - For creating prompt templates

This approach results in cleaner, more maintainable code while providing the same functionality but with access to more comprehensive API features.

## v1 API Features

The v1 API implementation provides access to many additional endpoints and capabilities:

- **API info** - Version information for the DraCor API
- **Corpus metadata** - Detailed metadata for all plays in a corpus
- **Play metrics** - Network metrics and analysis data
- **Character network data** - CSV, GEXF, and GraphML formats
- **Character relations** - Explicit relationships between characters
- **Spoken text filters** - Filter by gender, relation type, or character role
- **Stage directions** - Retrieve stage directions with or without speakers
- **Character lookup** - Find plays containing specific characters (by Wikidata ID)

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

4. Analyze gender representation:

```
Analyze the gender distribution and representation in Molière's Le Misanthrope
```

5. Find a character across different plays:

```
Find all plays that feature a character named "Hamlet" or similar
```

6. Analyze the full text of a play:

```
Provide a comprehensive analysis of the full text of Goethe's Faust
```

7. Extract themes from play text:

```
What are the main themes and motifs in the full text of Shakespeare's Hamlet?
```

8. Analyze language patterns:

```
Analyze the language patterns and style in Chekhov's The Cherry Orchard
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

## Resources (v1 API)

The FastMCP server exposes the following resources:

- `info://` - API information and version details
- `corpora://` - List of all available corpora
- `corpus://{corpus_name}` - Information about a specific corpus
- `corpus_metadata://{corpus_name}` - Metadata for all plays in a corpus
- `plays://{corpus_name}` - List of plays in a specific corpus
- `play://{corpus_name}/{play_name}` - Information about a specific play
- `play_metrics://{corpus_name}/{play_name}` - Network metrics for a specific play
- `characters://{corpus_name}/{play_name}` - List of characters in a specific play
- `spoken_text://{corpus_name}/{play_name}` - Spoken text in a play (with optional filters)
- `spoken_text_by_character://{corpus_name}/{play_name}` - Text spoken by each character
- `stage_directions://{corpus_name}/{play_name}` - Stage directions in a play
- `network_data://{corpus_name}/{play_name}` - Network data in CSV format
- `relations://{corpus_name}/{play_name}` - Character relation data in CSV format
- `character_by_wikidata://{wikidata_id}` - List plays containing a character by Wikidata ID
- `full_text://{corpus_name}/{play_name}` - Full text of a play in plain text format
- `tei_text://{corpus_name}/{play_name}` - Full TEI XML text of a play

## Tools (v1 API)

The FastMCP server provides the following tools:

- `search_plays` - Search for plays based on a query
- `compare_plays` - Compare two plays in terms of metrics and structure
- `analyze_character_relations` - Analyze character relationships in a play
- `analyze_play_structure` - Analyze the structure of a play
- `find_character_across_plays` - Find a character across multiple plays
- `analyze_full_text` - Analyze the full text of a play, including dialogue and stage directions

## Prompt Templates (v1 API)

The FastMCP server includes these prompt templates:

- `analyze_play` - Template for analyzing a specific play
- `character_analysis` - Template for analyzing a specific character
- `network_analysis` - Template for analyzing a character network
- `comparative_analysis` - Template for comparing two plays
- `gender_analysis` - Template for analyzing gender representation in a play
- `historical_context` - Template for analyzing the historical context of a play
- `full_text_analysis` - Template for analyzing the full text of a play

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
2. Try running in development mode to debug: `mcp dev dracor_mcp_fastmcp.py`
3. Check the DraCor API status at https://dracor.org/doc/api

## Prompt to use with MCP

"Your task is to analyze historical plays from the DraCor database to identify character ID tagging issues. Specifically:

1. Select a play from the DraCor database and perform a comprehensive analysis of its character relations, full text, and structure.
2. Identify all possible inconsistencies in character ID tagging, including:
   - Spelling variations of character names
   - Character name confusion or conflation
   - Historical spelling variants
   - Discrepancies between character IDs and stage directions
3. Create a detailed report of potential character ID tagging errors in a structured table format with the following columns:
   - Text ID (unique identifier for the play)
   - Current character ID used in the database
   - Problematic variant(s) found in the text
   - Type of error (spelling, variation, confusion, etc.)
   - Explanation of the issue

do it for this text: [playname]"

## License

MIT

## Acknowledgements

This project uses:

- Model Context Protocol Python SDK for building the MCP server
- DraCor API v1 for dramatic text and network data
- Drama Corpora Project (DraCor) for providing the underlying data and API
