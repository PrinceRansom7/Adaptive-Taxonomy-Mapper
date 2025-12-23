from typing import List, Optional


UNMAPPED_LABEL = "[UNMAPPED]"


def validate_mapping(
    proposed_genre: Optional[str],
    allowed_genres: List[str]
) -> str:
    """
    Validates the mapper's proposed genre against the taxonomy.

    Rules enforced here:
    1. Hierarchy Rule: only leaf-level genres are allowed
    2. Honesty Rule: if no confident or valid mapping exists, return [UNMAPPED]

    """

    # If mapper could not decide, be honest
    if proposed_genre is None:
        return UNMAPPED_LABEL

    # If mapper proposed something outside the taxonomy, reject it
    if proposed_genre not in allowed_genres:
        return UNMAPPED_LABEL
   
    return proposed_genre
