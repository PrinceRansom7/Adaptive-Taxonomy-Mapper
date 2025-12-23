import json
from typing import Dict, List, Tuple


def load_taxonomy(file_path: str) -> Dict:
    """
    Load the internal taxonomy JSON file.

    """
    with open(file_path, "r", encoding="utf-8") as file:
        taxonomy = json.load(file)

    return taxonomy


def get_leaf_genres(taxonomy: Dict) -> Tuple[List[str], Dict[str, str]]:
    """
    Extract all leaf-level genres from the taxonomy.

    Returns:
    - allowed_genres: list of valid sub-genres (leaf nodes)
    - parent_lookup: mapping of sub-genre -> parent genre

    """

    allowed_genres = []
    parent_lookup = {}

    # Expected structure:
    # {
    #   "Fiction": {
    #       "Romance": ["Slow-burn", "Enemies-to-Lovers", ...],
    #       "Thriller": [...]
    #   }
    # }

    for _, category_block in taxonomy.items():
        for parent_genre, sub_genres in category_block.items():
            for sub_genre in sub_genres:
                allowed_genres.append(sub_genre)
                parent_lookup[sub_genre] = parent_genre

    return allowed_genres, parent_lookup


def validate_genre(genre: str, allowed_genres: List[str]) -> bool:
    """
    Validate whether a genre exists in the taxonomy.
    This function acts as a hard guardrail:
    
    """
    if not genre:
        return False

    return genre in allowed_genres
    