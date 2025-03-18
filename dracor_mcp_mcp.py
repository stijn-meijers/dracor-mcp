#!/usr/bin/env python3

from typing import Dict, List, Optional, Any, Union
import requests
from mcp.server.fastmcp import FastMCP

# Base API URL for DraCor
DRACOR_API_BASE_URL = "https://dracor.org/api"

# Create the FastMCP server instance
mcp = FastMCP("DraCor API")

# Helper function to make API requests
def api_request(endpoint: str, params: Optional[Dict] = None) -> Dict:
    """Make a request to the DraCor API."""
    url = f"{DRACOR_API_BASE_URL}/{endpoint}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Resource implementations using decorators
@mcp.resource("corpora://")
def get_corpora() -> Dict:
    """List of all available corpora (collections of plays)."""
    try:
        corpora = api_request("corpora")
        return {"corpora": corpora}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("corpus://{corpus_name}")
def get_corpus(corpus_name: str) -> Dict:
    """Information about a specific corpus."""
    try:
        corpus = api_request(f"corpora/{corpus_name}")
        return corpus
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("plays://{corpus_name}")
def get_plays(corpus_name: str) -> Dict:
    """List of plays in a specific corpus."""
    try:
        plays = api_request(f"corpora/{corpus_name}/plays")
        return {"plays": plays}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("play://{corpus_name}/{play_name}")
def get_play(corpus_name: str, play_name: str) -> Dict:
    """Information about a specific play."""
    try:
        play = api_request(f"corpora/{corpus_name}/play/{play_name}")
        return play
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("network://{corpus_name}/{play_name}")
def get_network(corpus_name: str, play_name: str) -> Dict:
    """Character network for a specific play."""
    try:
        network = api_request(f"corpora/{corpus_name}/play/{play_name}/network")
        return network
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("characters://{corpus_name}/{play_name}")
def get_characters(corpus_name: str, play_name: str) -> Dict:
    """List of characters in a specific play."""
    try:
        characters = api_request(f"corpora/{corpus_name}/play/{play_name}/characters")
        return {"characters": characters}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("character://{corpus_name}/{play_name}/{character_id}")
def get_character(corpus_name: str, play_name: str, character_id: str) -> Dict:
    """Information about a specific character in a play."""
    try:
        character = api_request(f"corpora/{corpus_name}/play/{play_name}/character/{character_id}")
        return character
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("metrics://{corpus_name}/{play_name}")
def get_metrics(corpus_name: str, play_name: str) -> Dict:
    """Metrics and statistics for a specific play."""
    try:
        metrics = api_request(f"corpora/{corpus_name}/play/{play_name}/metrics")
        return metrics
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("spoken_text://{corpus_name}/{play_name}/{character_id}")
def get_spoken_text(corpus_name: str, play_name: str, character_id: str) -> Dict:
    """Text spoken by a specific character in a play."""
    try:
        spoken_text = api_request(f"corpora/{corpus_name}/play/{play_name}/character/{character_id}/text")
        return {"text": spoken_text}
    except Exception as e:
        return {"error": str(e)}

# Tool implementations using decorators
@mcp.tool()
def search_plays(query: str) -> Dict:
    """Search for plays based on a query."""
    try:
        results = api_request("search", {"q": query})
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def compare_plays(
    corpus_name1: str, 
    play_name1: str, 
    corpus_name2: str, 
    play_name2: str
) -> Dict:
    """Compare two plays in terms of metrics and structure."""
    try:
        play1 = api_request(f"corpora/{corpus_name1}/play/{play_name1}")
        play2 = api_request(f"corpora/{corpus_name2}/play/{play_name2}")
        
        metrics1 = api_request(f"corpora/{corpus_name1}/play/{play_name1}/metrics")
        metrics2 = api_request(f"corpora/{corpus_name2}/play/{play_name2}/metrics")
        
        # Compile comparison data
        comparison = {
            "plays": [
                {
                    "title": play1.get("title"),
                    "author": play1.get("author", {}).get("name"),
                    "year": play1.get("yearNormalized"),
                    "metrics": metrics1
                },
                {
                    "title": play2.get("title"),
                    "author": play2.get("author", {}).get("name"),
                    "year": play2.get("yearNormalized"),
                    "metrics": metrics2
                }
            ]
        }
        
        return comparison
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def analyze_character_relations(corpus_name: str, play_name: str) -> Dict:
    """Analyze the character relationships in a play."""
    try:
        network = api_request(f"corpora/{corpus_name}/play/{play_name}/network")
        characters = api_request(f"corpora/{corpus_name}/play/{play_name}/characters")
        
        # Create a mapping of character IDs to names for easy reference
        char_map = {}
        for char in characters.get("characters", []):
            char_map[char.get("id")] = char.get("name")
        
        # Analyze relations
        relations = []
        for edge in network.get("edges", []):
            source_id = edge.get("source")
            target_id = edge.get("target")
            weight = edge.get("weight")
            
            source_name = char_map.get(source_id, source_id)
            target_name = char_map.get(target_id, target_id)
            
            relations.append({
                "source": source_name,
                "target": target_name,
                "weight": weight
            })
        
        # Sort by weight to identify strongest relationships
        relations.sort(key=lambda x: x.get("weight", 0), reverse=True)
        
        return {
            "play": play_name,
            "totalCharacters": len(network.get("nodes", [])),
            "totalRelations": len(network.get("edges", [])),
            "strongestRelations": relations[:10],  # Top 10 strongest relations
            "weakestRelations": relations[-10:] if len(relations) >= 10 else relations  # Bottom 10
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def analyze_play_structure(corpus_name: str, play_name: str) -> Dict:
    """Analyze the structure of a play including acts, scenes, and metrics."""
    try:
        play = api_request(f"corpora/{corpus_name}/play/{play_name}")
        metrics = api_request(f"corpora/{corpus_name}/play/{play_name}/metrics")
        
        # Get structural information
        structure = {
            "title": play.get("title"),
            "author": play.get("author", {}).get("name"),
            "year": play.get("yearNormalized"),
            "acts": play.get("numOfActs"),
            "scenes": play.get("numOfScenes"),
            "segments": metrics.get("segments"),
            "dialogues": metrics.get("dialogues"),
            "wordCount": metrics.get("wordCount"),
            "speakers": metrics.get("characters"),
            "structure": play.get("structure", [])
        }
        
        return structure
    except Exception as e:
        return {"error": str(e)}

# Prompt templates using decorators
@mcp.prompt()
def analyze_play(corpus_name: str, play_name: str) -> str:
    """Create a prompt for analyzing a specific play."""
    return f"""
    You are a drama analysis expert who can help analyze plays from the DraCor (Drama Corpora Project) database.
    
    You have access to the following play:
    
    Corpus: {corpus_name}
    Play: {play_name}
    
    Analyze this play in terms of:
    1. Basic information (title, author, year)
    2. Structure (acts, scenes)
    3. Character relationships
    4. Key metrics and statistics
    
    Please provide a comprehensive analysis including:
    - Historical context of the play
    - Structural analysis
    - Character analysis
    - Network analysis (how characters relate to each other)
    - Notable aspects of this play compared to others from the same period
    """

@mcp.prompt()
def character_analysis(corpus_name: str, play_name: str, character_id: str) -> str:
    """Create a prompt for analyzing a specific character."""
    return f"""
    You are a drama character analysis expert who can help analyze characters from plays in the DraCor database.
    
    You have access to the following character:
    
    Corpus: {corpus_name}
    Play: {play_name}
    Character: {character_id}
    
    Analyze this character in terms of:
    1. Basic information (name, gender)
    2. Importance in the play (based on speech counts, words spoken)
    3. Relationships with other characters
    4. Character development throughout the play
    
    Please provide a comprehensive character analysis that could help researchers or students understand this character better.
    """

@mcp.prompt()
def network_analysis(corpus_name: str, play_name: str) -> str:
    """Create a prompt for analyzing a character network."""
    return f"""
    You are a network analysis expert who can help analyze character networks from plays in the DraCor database.
    
    You have access to the following play network:
    
    Corpus: {corpus_name}
    Play: {play_name}
    
    Analyze this play's character network in terms of:
    1. Overall network structure and density
    2. Central characters (highest degree, betweenness)
    3. Character communities or groups
    4. Strongest and weakest relationships
    5. How the network structure relates to the themes of the play
    
    Please provide a comprehensive network analysis that could help researchers understand the social dynamics in this play.
    """

@mcp.prompt()
def comparative_analysis(corpus_name1: str, play_name1: str, corpus_name2: str, play_name2: str) -> str:
    """Create a prompt for comparing two plays."""
    return f"""
    You are a drama analysis expert who can help compare plays from the DraCor database.
    
    You have access to the following two plays:
    
    Play 1:
    Corpus: {corpus_name1}
    Play: {play_name1}
    
    Play 2:
    Corpus: {corpus_name2}
    Play: {play_name2}
    
    Compare these plays in terms of:
    1. Basic information (title, author, year)
    2. Structure (acts, scenes, length)
    3. Character count and dynamics
    4. Network complexity and density
    5. Historical context and significance
    
    Please provide a comprehensive comparative analysis that highlights similarities and differences between these plays.
    """

if __name__ == "__main__":
    mcp.run() 