#!/usr/bin/env python3

from typing import Dict, List, Optional, Any, Union
import requests
from mcp.server.fastmcp import FastMCP

# Base API URL for DraCor v1
DRACOR_API_BASE_URL = "https://dracor.org/api/v1"

# Create the FastMCP server instance
mcp = FastMCP("DraCor API v1")

# Helper function to make API requests
def api_request(endpoint: str, params: Optional[Dict] = None) -> Any:
    """Make a request to the DraCor API v1."""
    url = f"{DRACOR_API_BASE_URL}/{endpoint}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Resource implementations using decorators
@mcp.resource("info://")
def get_api_info() -> Dict:
    """Get API information and version details."""
    try:
        info = api_request("info")
        return info
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("corpora://")
def get_corpora() -> Dict:
    """List of all available corpora (collections of plays)."""
    try:
        # The include parameter needs to be handled differently as it's not in the URI
        # We'll handle it as a query parameter in the implementation
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

@mcp.resource("corpus_metadata://{corpus_name}")
def get_corpus_metadata(corpus_name: str) -> Dict:
    """Get metadata for all plays in a corpus."""
    try:
        metadata = api_request(f"corpora/{corpus_name}/metadata")
        return {"metadata": metadata}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("plays://{corpus_name}")
def get_plays(corpus_name: str) -> Dict:
    """List of plays in a specific corpus."""
    try:
        corpus = api_request(f"corpora/{corpus_name}")
        return {"plays": corpus.get("plays", [])}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("play://{corpus_name}/{play_name}")
def get_play(corpus_name: str, play_name: str) -> Dict:
    """Information about a specific play."""
    try:
        play = api_request(f"corpora/{corpus_name}/plays/{play_name}")
        return play
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("play_metrics://{corpus_name}/{play_name}")
def get_play_metrics(corpus_name: str, play_name: str) -> Dict:
    """Get network metrics for a specific play."""
    try:
        metrics = api_request(f"corpora/{corpus_name}/plays/{play_name}/metrics")
        return metrics
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("characters://{corpus_name}/{play_name}")
def get_characters(corpus_name: str, play_name: str) -> Dict:
    """List of characters in a specific play."""
    try:
        characters = api_request(f"corpora/{corpus_name}/plays/{play_name}/characters")
        return {"characters": characters}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("spoken_text://{corpus_name}/{play_name}")
def get_spoken_text(corpus_name: str, play_name: str) -> Dict:
    """Get the spoken text for a play, with optional filters (gender, relation, role) as query parameters."""
    try:
        # For now, we won't use optional query parameters since they're causing issues
        # We can implement this differently once we better understand the FastMCP API
        url = f"{DRACOR_API_BASE_URL}/corpora/{corpus_name}/plays/{play_name}/spoken-text"
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
        
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("spoken_text_by_character://{corpus_name}/{play_name}")
def get_spoken_text_by_character(corpus_name: str, play_name: str) -> Dict:
    """Get spoken text for each character in a play."""
    try:
        text_by_character = api_request(f"corpora/{corpus_name}/plays/{play_name}/spoken-text-by-character")
        return {"text_by_character": text_by_character}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("stage_directions://{corpus_name}/{play_name}")
def get_stage_directions(corpus_name: str, play_name: str) -> Dict:
    """Get all stage directions of a play."""
    try:
        # Note: This endpoint returns plain text, not JSON
        url = f"{DRACOR_API_BASE_URL}/corpora/{corpus_name}/plays/{play_name}/stage-directions"
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
        
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("network_data://{corpus_name}/{play_name}")
def get_network_data(corpus_name: str, play_name: str) -> Dict:
    """Get network data of a play in CSV format."""
    try:
        # Note: This endpoint returns CSV, not JSON
        url = f"{DRACOR_API_BASE_URL}/corpora/{corpus_name}/plays/{play_name}/networkdata/csv"
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.text
        
        return {"csv_data": csv_data}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("relations://{corpus_name}/{play_name}")
def get_relations(corpus_name: str, play_name: str) -> Dict:
    """Get relation data of a play in CSV format."""
    try:
        # Note: This endpoint returns CSV, not JSON
        url = f"{DRACOR_API_BASE_URL}/corpora/{corpus_name}/plays/{play_name}/relations/csv"
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.text
        
        return {"csv_data": csv_data}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("character_by_wikidata://{wikidata_id}")
def get_plays_with_character(wikidata_id: str) -> Dict:
    """List plays having a character identified by Wikidata ID."""
    try:
        plays = api_request(f"character/{wikidata_id}")
        return {"plays": plays}
    except Exception as e:
        return {"error": str(e)}

# Tool implementations using decorators
@mcp.tool()
def search_plays(query: str) -> Dict:
    """Search for plays in the DraCor database."""
    try:
        # DraCor v1 doesn't have a dedicated search endpoint, so we'll 
        # fetch all corpora and filter client-side
        all_corpora = api_request("corpora")
        
        results = []
        for corpus in all_corpora:
            corpus_data = api_request(f"corpora/{corpus['name']}")
            for play in corpus_data.get("plays", []):
                # Search in title, author names, and other fields
                searchable_text = (
                    play.get("title", "") + " " +
                    " ".join([a.get("name", "") for a in play.get("authors", [])]) + " " +
                    play.get("subtitle", "")
                ).lower()
                
                if query.lower() in searchable_text:
                    results.append({
                        "corpus": corpus["name"],
                        "play": play
                    })
        
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
        play1 = api_request(f"corpora/{corpus_name1}/plays/{play_name1}")
        play2 = api_request(f"corpora/{corpus_name2}/plays/{play_name2}")
        
        metrics1 = api_request(f"corpora/{corpus_name1}/plays/{play_name1}/metrics")
        metrics2 = api_request(f"corpora/{corpus_name2}/plays/{play_name2}/metrics")
        
        # Compile comparison data
        comparison = {
            "plays": [
                {
                    "title": play1.get("title"),
                    "author": play1.get("authors", [{}])[0].get("name") if play1.get("authors") else None,
                    "year": play1.get("yearNormalized"),
                    "metrics": metrics1
                },
                {
                    "title": play2.get("title"),
                    "author": play2.get("authors", [{}])[0].get("name") if play2.get("authors") else None,
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
        # Get play data
        play = api_request(f"corpora/{corpus_name}/plays/{play_name}")
        
        # Get character data
        characters = api_request(f"corpora/{corpus_name}/plays/{play_name}/characters")
        
        # Get network data in CSV format
        url = f"{DRACOR_API_BASE_URL}/corpora/{corpus_name}/plays/{play_name}/networkdata/csv"
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.text
        
        # Parse CSV data to extract relations
        relations = []
        lines = csv_data.strip().split('\n')
        if len(lines) > 1:  # Skip header
            headers = lines[0].split(',')
            for line in lines[1:]:
                parts = line.split(',')
                if len(parts) >= 4:
                    source = parts[0].strip('"')
                    target = parts[2].strip('"')
                    weight = int(parts[3]) if parts[3].isdigit() else 0
                    
                    # Find character names from IDs
                    source_name = None
                    target_name = None
                    for char in characters:
                        if char.get("id") == source:
                            source_name = char.get("name")
                        if char.get("id") == target:
                            target_name = char.get("name")
                    
                    relations.append({
                        "source": source_name or source,
                        "source_id": source,
                        "target": target_name or target,
                        "target_id": target,
                        "weight": weight
                    })
        
        # Sort by weight to identify strongest relationships
        relations.sort(key=lambda x: x.get("weight", 0), reverse=True)
        
        # Try to get relations data if available
        try:
            relations_url = f"{DRACOR_API_BASE_URL}/corpora/{corpus_name}/plays/{play_name}/relations/csv"
            relations_response = requests.get(relations_url)
            formal_relations = []
            
            if relations_response.status_code == 200:
                rel_lines = relations_response.text.strip().split('\n')
                if len(rel_lines) > 1:  # Skip header
                    for line in rel_lines[1:]:
                        parts = line.split(',')
                        if len(parts) >= 4:
                            source = parts[0].strip('"')
                            target = parts[2].strip('"')
                            relation_type = parts[3].strip('"')
                            
                            # Find character names from IDs
                            source_name = None
                            target_name = None
                            for char in characters:
                                if char.get("id") == source:
                                    source_name = char.get("name")
                                if char.get("id") == target:
                                    target_name = char.get("name")
                            
                            formal_relations.append({
                                "source": source_name or source,
                                "target": target_name or target,
                                "type": relation_type
                            })
        except:
            formal_relations = []
        
        # Get metrics
        metrics = api_request(f"corpora/{corpus_name}/plays/{play_name}/metrics")
        
        return {
            "play": {
                "title": play.get("title"),
                "author": play.get("authors", [{}])[0].get("name") if play.get("authors") else None,
                "year": play.get("yearNormalized")
            },
            "totalCharacters": len(characters),
            "totalRelations": len(relations),
            "strongestRelations": relations[:10],  # Top 10 strongest relations
            "weakestRelations": relations[-10:] if len(relations) >= 10 else relations,  # Bottom 10
            "formalRelations": formal_relations,  # Explicit relations if available
            "metrics": metrics
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def analyze_play_structure(corpus_name: str, play_name: str) -> Dict:
    """Analyze the structure of a play including acts, scenes, and metrics."""
    try:
        play = api_request(f"corpora/{corpus_name}/plays/{play_name}")
        metrics = api_request(f"corpora/{corpus_name}/plays/{play_name}/metrics")
        
        # Extract structural information from segments
        acts = []
        scenes = []
        for segment in play.get("segments", []):
            if segment.get("type") == "act":
                acts.append({
                    "number": segment.get("number"),
                    "title": segment.get("title")
                })
            elif segment.get("type") == "scene":
                scenes.append({
                    "number": segment.get("number"),
                    "title": segment.get("title"),
                    "speakers": segment.get("speakers", [])
                })
        
        # Get character data
        characters = api_request(f"corpora/{corpus_name}/plays/{play_name}/characters")
        
        # Count characters by gender
        gender_counts = {"MALE": 0, "FEMALE": 0, "UNKNOWN": 0}
        for character in characters:
            gender = character.get("gender")
            if gender in gender_counts:
                gender_counts[gender] += 1
        
        # Get spoken text by character data
        spoken_text_by_char = api_request(f"corpora/{corpus_name}/plays/{play_name}/spoken-text-by-character")
        
        # Calculate total words and distribution
        total_words = sum(char.get("numOfWords", 0) for char in characters)
        speaking_distribution = []
        
        if total_words > 0:
            for char in characters:
                char_words = char.get("numOfWords", 0)
                speaking_distribution.append({
                    "character": char.get("name"),
                    "words": char_words,
                    "percentage": round((char_words / total_words) * 100, 2)
                })
            
            # Sort by word count
            speaking_distribution.sort(key=lambda x: x["words"], reverse=True)
        
        # Get structural information
        structure = {
            "title": play.get("title"),
            "authors": [author.get("name") for author in play.get("authors", [])],
            "year": play.get("yearNormalized"),
            "yearWritten": play.get("yearWritten"),
            "yearPrinted": play.get("yearPrinted"),
            "yearPremiered": play.get("yearPremiered"),
            "acts": acts,
            "scenes": scenes,
            "numOfActs": len(acts),
            "numOfScenes": len(scenes),
            "segments": metrics.get("segments"),
            "dialogues": metrics.get("dialogues"),
            "wordCount": total_words,
            "characters": {
                "total": len(characters),
                "byGender": gender_counts
            },
            "speakingDistribution": speaking_distribution[:10],  # Top 10 characters by speaking time
        }
        
        return structure
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def find_character_across_plays(character_name: str) -> Dict:
    """Find a character across multiple plays in the DraCor database."""
    try:
        all_corpora = api_request("corpora")
        matches = []
        
        for corpus in all_corpora:
            corpus_name = corpus["name"]
            corpus_data = api_request(f"corpora/{corpus_name}")
            
            for play in corpus_data.get("plays", []):
                play_name = play.get("name")
                
                try:
                    characters = api_request(f"corpora/{corpus_name}/plays/{play_name}/characters")
                    
                    for character in characters:
                        if character_name.lower() in (character.get("name") or "").lower():
                            matches.append({
                                "corpus": corpus_name,
                                "play": play.get("title"),
                                "character": character.get("name"),
                                "gender": character.get("gender"),
                                "numOfSpeechActs": character.get("numOfSpeechActs"),
                                "numOfWords": character.get("numOfWords")
                            })
                except:
                    continue
        
        return {"matches": matches}
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

@mcp.prompt()
def gender_analysis(corpus_name: str, play_name: str) -> str:
    """Create a prompt for analyzing gender representation in a play."""
    return f"""
    You are a scholar specializing in gender studies and dramatic literature. You've been asked to analyze gender representation in a drama.
    
    Corpus: {corpus_name}
    Play: {play_name}
    
    Please analyze the play in terms of:
    1. Gender distribution of characters
    2. Speaking time and importance of male vs. female characters
    3. Relationships between characters of different genders
    4. Historical context of gender representation in this period
    5. Notable aspects of gender portrayal in this play
    
    Your analysis should consider both quantitative data (number of characters, speaking lines) and qualitative aspects (power dynamics, character development).
    """

@mcp.prompt()
def historical_context(corpus_name: str, play_name: str) -> str:
    """Create a prompt for analyzing the historical context of a play."""
    return f"""
    You are a theater historian who specializes in putting dramatic works in their historical context.
    
    Corpus: {corpus_name}
    Play: {play_name}
    
    Please provide a detailed analysis of the historical context of this play, including:
    1. Political and social climate when the play was written
    2. Theatrical conventions of the period
    3. How contemporary events might have influenced the play
    4. Reception of the play when it was first performed
    5. The play's significance in the author's body of work
    6. How the play reflects or challenges the values of its time
    
    Your analysis should help modern readers and scholars understand the play within its original historical framework.
    """

if __name__ == "__main__":
    mcp.run() 