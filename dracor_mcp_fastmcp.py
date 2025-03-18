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
    """Get character relation data for a play."""
    try:
        url = f"{DRACOR_API_BASE_URL}/corpora/{corpus_name}/plays/{play_name}/relations"
        response = requests.get(url)
        response.raise_for_status()
        relations = response.json()
        
        return {"relations": relations}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("full_text://{corpus_name}/{play_name}")
def get_full_text(corpus_name: str, play_name: str) -> Dict:
    """Get the full text of a play in plain text format."""
    try:
        # The DraCor API doesn't have a direct plain text endpoint
        # Use the spoken-text endpoint which returns plain text of all dialogue
        url = f"{DRACOR_API_BASE_URL}/corpora/{corpus_name}/plays/{play_name}/spoken-text"
        response = requests.get(url)
        response.raise_for_status()
        
        # Get stage directions too
        stage_url = f"{DRACOR_API_BASE_URL}/corpora/{corpus_name}/plays/{play_name}/stage-directions"
        stage_response = requests.get(stage_url)
        stage_response.raise_for_status()
        
        # Combine both for a more complete text representation
        text = f"DIALOGUE:\n\n{response.text}\n\nSTAGE DIRECTIONS:\n\n{stage_response.text}"
        
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("tei_text://{corpus_name}/{play_name}")
def get_tei_text(corpus_name: str, play_name: str) -> Dict:
    """Get the full TEI XML text of a play."""
    try:
        url = f"{DRACOR_API_BASE_URL}/corpora/{corpus_name}/plays/{play_name}/tei"
        response = requests.get(url)
        response.raise_for_status()
        tei_text = response.text
        
        return {"tei_text": tei_text}
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
def search_plays(
    query: str = None, 
    corpus_name: str = None,
    character_name: str = None, 
    country: str = None,
    language: str = None,
    author: str = None,
    year_from: int = None,
    year_to: int = None,
    gender_filter: str = None
) -> Dict:
    """
    Advanced search for plays in the DraCor database with multiple filter options.
    
    Parameters:
    - query: General text search across title, subtitle, and author
    - corpus_name: Specific corpus to search within (e.g., "shake", "ger", "rus", "span", "dutch")
    - character_name: Name of a character that should appear in the play
    - country: Country of origin for the play
    - language: Language of the play
    - author: Name of the playwright
    - year_from: Starting year for date range filter
    - year_to: Ending year for date range filter
    - gender_filter: Filter by plays with a certain gender ratio ("female_dominated", "male_dominated", "balanced")
    """
    try:
        # Get corpora to search in
        corpora_result = get_corpora()
        if "error" in corpora_result:
            return {"error": corpora_result["error"]}
        
        all_corpora = corpora_result.get("corpora", [])
        target_corpora = []
        
        # Filter corpora if specified
        if corpus_name:
            target_corpora = [corp for corp in all_corpora if corpus_name.lower() in corp.get("name", "").lower()]
        else:
            target_corpora = all_corpora
        
        # Initialize results
        results = []
        detailed_results = []
        
        # For each corpus, search for plays
        for corpus in target_corpora:
            corpus_name = corpus.get("name")
            
            # Get all plays from this corpus
            plays_result = get_plays(corpus_name)
            if "error" in plays_result:
                continue
            
            # Iterate through plays and apply filters
            for play in plays_result.get("plays", []):
                # Initialize as a match until proven otherwise by filters
                is_match = True
                
                # Apply general text search if specified
                if query and is_match:
                    searchable_text = (
                        play.get("title", "") + " " +
                        " ".join([a.get("name", "") for a in play.get("authors", [])]) + " " +
                        play.get("subtitle", "") + " " +
                        play.get("originalTitle", "")
                    ).lower()
                    
                    if query.lower() not in searchable_text:
                        is_match = False
                
                # Apply country filter if specified
                if country and is_match:
                    play_country = (
                        play.get("writtenIn", "") + " " + 
                        play.get("printedIn", "") + " " +
                        " ".join([a.get("country", "") for a in play.get("authors", [])])
                    ).lower()
                    
                    if country.lower() not in play_country:
                        is_match = False
                
                # Apply language filter if specified
                if language and is_match:
                    if language.lower() not in play.get("originalLanguage", "").lower():
                        is_match = False
                
                # Apply author filter if specified
                if author and is_match:
                    author_names = [a.get("name", "").lower() for a in play.get("authors", [])]
                    if not any(author.lower() in name for name in author_names):
                        is_match = False
                
                # Apply year range filter if specified
                if (year_from or year_to) and is_match:
                    play_year = play.get("yearNormalized") or play.get("yearWritten") or play.get("yearPrinted") or 0
                    
                    if year_from and play_year < year_from:
                        is_match = False
                    
                    if year_to and play_year > year_to:
                        is_match = False
                
                # If character name is specified, need to check character list
                if character_name and is_match:
                    try:
                        # Get characters for this play
                        play_name = play.get("name")
                        characters_result = get_characters(corpus_name, play_name)
                        
                        if "error" not in characters_result:
                            character_found = False
                            for character in characters_result.get("characters", []):
                                if character_name.lower() in character.get("name", "").lower():
                                    character_found = True
                                    break
                            
                            if not character_found:
                                is_match = False
                        else:
                            # If we can't get characters, we assume it's not a match
                            is_match = False
                    except:
                        # If error occurs, we assume it's not a match
                        is_match = False
                
                # Apply gender filter if specified
                if gender_filter and is_match:
                    try:
                        # Get characters for this play
                        play_name = play.get("name")
                        characters_result = get_characters(corpus_name, play_name)
                        
                        if "error" not in characters_result:
                            male_count = sum(1 for c in characters_result.get("characters", []) if c.get("gender") == "MALE")
                            female_count = sum(1 for c in characters_result.get("characters", []) if c.get("gender") == "FEMALE")
                            total = male_count + female_count
                            
                            if total > 0:
                                female_ratio = female_count / total
                                
                                if gender_filter == "female_dominated" and female_ratio <= 0.5:
                                    is_match = False
                                elif gender_filter == "male_dominated" and female_ratio >= 0.5:
                                    is_match = False
                                elif gender_filter == "balanced" and (female_ratio < 0.4 or female_ratio > 0.6):
                                    is_match = False
                    except:
                        # If error occurs, we keep it as a match
                        pass
                
                # If all filters passed, add to results
                if is_match:
                    # Add basic info to results
                    results.append({
                        "corpus": corpus_name,
                        "play": play
                    })
                    
                    # Try to add more detailed info for top results
                    if len(detailed_results) < 5:
                        try:
                            play_name = play.get("name")
                            # Get more details
                            play_info = get_play(corpus_name, play_name)
                            
                            if "error" not in play_info:
                                detailed_results.append({
                                    "corpus": corpus_name,
                                    "play_name": play_name,
                                    "title": play.get("title"),
                                    "author": play.get("authors", [{}])[0].get("name") if play.get("authors") else "Unknown",
                                    "year": play.get("yearNormalized"),
                                    "language": play.get("originalLanguage"),
                                    "characters": len(play_info.get("characters", [])),
                                    "link": f"https://dracor.org/{corpus_name}/{play_name}"
                                })
                        except:
                            pass
        
        return {
            "count": len(results),
            "results": results,
            "top_results": detailed_results,
            "filters_applied": {
                "query": query,
                "corpus_name": corpus_name,
                "character_name": character_name,
                "country": country,
                "language": language,
                "author": author,
                "year_range": f"{year_from}-{year_to}" if year_from or year_to else None,
                "gender_filter": gender_filter
            }
        }
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

@mcp.tool("analyze_full_text")
def analyze_full_text(corpus_name: str, play_name: str) -> Dict:
    """Analyze the full text of a play, including dialogue and stage directions."""
    try:
        # Get the TEI XML as primary source
        tei_result = get_tei_text(corpus_name, play_name)
        if "error" in tei_result:
            # Fall back to the plain text if TEI fails
            full_text = get_full_text(corpus_name, play_name)
            if "error" in full_text:
                return {"error": full_text["error"]}
            has_tei = False
            text_content = full_text["text"]
        else:
            has_tei = True
            tei_text = tei_result["tei_text"]
            
            # Simple XML parsing to extract basic structure
            # In a production environment, use a proper XML parser library
            import re
            
            # Extract title
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', tei_text)
            title = title_match.group(1) if title_match else "Unknown"
            
            # Extract author(s)
            author_matches = re.findall(r'<author[^>]*>([^<]+)</author>', tei_text)
            authors = author_matches if author_matches else ["Unknown"]
            
            # Extract acts
            acts = re.findall(r'<div type="act"[^>]*>(.*?)</div>', tei_text, re.DOTALL)
            act_count = len(acts)
            
            # Extract scenes
            scenes = re.findall(r'<div type="scene"[^>]*>(.*?)</div>', tei_text, re.DOTALL)
            scene_count = len(scenes)
            
            # Extract speeches
            speeches = re.findall(r'<sp[^>]*>(.*?)</sp>', tei_text, re.DOTALL)
            speech_count = len(speeches)
            
            # Extract stage directions
            stage_directions = re.findall(r'<stage[^>]*>(.*?)</stage>', tei_text, re.DOTALL)
            stage_direction_count = len(stage_directions)
            
            # Also get the plain text for easier processing
            full_text = get_full_text(corpus_name, play_name)
            text_content = full_text.get("text", "")
            
        # Get play metadata
        play_info = get_play(corpus_name, play_name)
        if "error" in play_info:
            return {"error": play_info["error"]}
            
        # Get character list
        characters = get_characters(corpus_name, play_name)
        if "error" in characters:
            return {"error": characters["error"]}
        
        result = {
            "play": play_info.get("play", {}),
            "characters": characters.get("characters", []),
            "text": text_content,
        }
        
        # Add TEI-specific analysis if available
        if has_tei:
            result["tei_analysis"] = {
                "title": title,
                "authors": authors,
                "structure": {
                    "acts": act_count,
                    "scenes": scene_count,
                    "speeches": speech_count,
                    "stage_directions": stage_direction_count
                },
                "text_sample": {
                    "first_speech": speeches[0] if speeches else "",
                    "first_stage_direction": stage_directions[0] if stage_directions else ""
                }
            }
        
        # Add basic text analysis in either case
        result["analysis"] = {
            "text_length": len(text_content),
            "character_count": len(characters.get("characters", [])),
            "dialogue_to_direction_ratio": text_content.count("\n\nDIALOGUE:") / 
                                          (text_content.count("\n\nSTAGE DIRECTIONS:") or 1)
        }
        
        return result
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

@mcp.prompt("full_text_analysis")
def full_text_analysis_prompt() -> str:
    """Template for analyzing the full text of a play."""
    return """
    I'll analyze the full text of {play_title} by {author} from the {corpus_name} corpus.
    
    ## Basic Information
    - Title: {play_title}
    - Author: {author}
    - Written: {written_year}
    - Premiere: {premiere_date}
    
    ## Full Text Analysis
    
    {analysis}
    
    ## Key Themes and Motifs
    
    {themes}
    
    ## Language and Style
    
    {style}
    
    ## Historical and Cultural Context
    
    {context}
    """

@mcp.prompt("dutch_character_tagging_analysis")
def character_tagging_analysis(corpus_name: str = "dutch", play_name: str = None) -> str:
    """Template for analyzing character ID tagging issues in Dutch historical plays."""
    return """
    Your task is to analyze historical plays from the DraCor database to identify character ID tagging issues. Specifically:
    
    1. Select a play from the DraCor database and perform a comprehensive analysis of its character relations, full text, and structure.
    2. Identify all possible inconsistencies in character ID tagging, including:
       * Spelling variations of character names
       * Character name confusion or conflation
       * Historical spelling variants
       * Discrepancies between character IDs and stage directions
    3. Create a detailed report of potential character ID tagging errors in a structured table format with the following columns:
       * Text ID (unique identifier for the play)
       * Current character ID used in the database
       * Problematic variant(s) found in the text
       * Type of error (spelling, variation, confusion, etc.)
       * Explanation of the issue
    
    Focus on the play "{play_name}" from the {corpus_name} corpus if specified, otherwise select a suitable historical play.
    
    Approach:
    1. First examine the play's basic information and structure
    2. Review the full character list with their IDs 
    3. Analyze the TEI XML text, focusing on character speech tags (<sp>) and stage directions (<stage>)
    4. Compare names used in different contexts throughout the text
    5. Note historical spelling conventions and variants specific to Dutch literature of the period
    6. Present your findings in the required tabular format
    """

if __name__ == "__main__":
    mcp.run() 