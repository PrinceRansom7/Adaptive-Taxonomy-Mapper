from typing import Dict, List, Optional


def map_to_genre(
    analysis: Dict,
    user_tags: Optional[List[str]] = None
) -> Optional[str]:
    """
    Heuristic-based genre mapper.
    Final authority remains deterministic rules.
    """

    rule_signals = analysis.get("rule_signals", {})
    tokens = analysis.get("tokens", [])

    llm_context = analysis.get("llm_signals", {}).get("llm_context", {})
    llm_setting = llm_context.get("setting", "").lower()
    llm_themes = llm_context.get("themes", "").lower()

    # 1. Honesty rule
    if rule_signals.get("non_fiction"):
        return None

    # 2. Thriller
    if rule_signals.get("legal"):
        return "Legal Thriller"

    if rule_signals.get("espionage"):
        return "Espionage"

    # 3. Horror
    if rule_signals.get("slasher"):
        return "Slasher"

    if rule_signals.get("gothic"):
        return "Gothic"

    if rule_signals.get("horror"):
        return "Psychological Horror"

    # 4. Sci-Fi
    if rule_signals.get("cyberpunk"):
        return "Cyberpunk"

    if rule_signals.get("sci_fi"):
        if any(word in tokens for word in ["physics", "theory", "stasis", "metabolic"]):
            return "Hard Sci-Fi"
        if "scientific" in llm_themes:
            return "Hard Sci-Fi"
        return "Space Opera"

    # 5. Romance sub-genres (FIXED ORDER + LOGIC)

    # Enemies to Lovers
    if rule_signals.get("conflict") and any(
        word in tokens for word in ["hate", "hated", "enemy"]
    ):
        return "Enemies-to-Lovers"

    # Second Chance
    if rule_signals.get("romance") and any(
        word in tokens for word in ["again", "years", "met"]
    ):
        return "Second Chance"

    # Slow Burn
    if rule_signals.get("romance"):
        return "Slow-burn"

    # 6. Weak tag fallback
    if user_tags:
        lowered = [tag.lower() for tag in user_tags]

        if "love" in lowered:
            return "Slow-burn"
        if "scary" in lowered:
            return "Psychological Horror"
        if "space" in lowered:
            return "Space Opera"

    return None
