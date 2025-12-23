from typing import Dict, Optional


def generate_reasoning(
    story_text: str,
    rule_signals: Dict[str, bool],
    final_genre: str
) -> str:
    """
    Generates a short, human-readable explanation for why
    a particular genre (or UNMAPPED) was chosen.

    This function explains the decision made by the mapper.
    """

    if final_genre == "[UNMAPPED]":
        if rule_signals.get("non_fiction"):
            return (
                "The story appears to be instructional or non-fictional in nature, "
                "which does not match any category in the fiction taxonomy."
            )
        return (
            "The story does not strongly align with any available sub-genre "
            "in the internal taxonomy, so it was left unmapped."
        )

    # Genre-specific explanations
    if final_genre == "Enemies-to-Lovers":
        return (
            "The story describes a romantic relationship that develops out of conflict, which is a defining trait of the enemies-to-lovers trope."
        )

    if final_genre == "Second Chance":
        return (
            "The narrative focuses on characters reconnecting after a long period of separation, which aligns with the second-chance romance theme."
        )

    if final_genre == "Slow-burn":
        return (
            "The story emphasizes gradual emotional development rather than immediate romance, which fits the slow-burn romance category."
        )

    if final_genre == "Legal Thriller":
        return (
            "The central tension revolves around legal proceedings and courtroom conflict, making legal thriller the most appropriate classification."
        )

    if final_genre == "Espionage":
        return (
            "The plot centers on covert operations and intelligence work, which are key elements of the espionage thriller genre."
        )

    if final_genre == "Gothic":
        return (
            "The setting and atmosphere emphasize an old, mysterious environment with a dark past, which are characteristic of gothic horror."
        )

    if final_genre == "Psychological Horror":
        return (
            "The story relies on fear, suspense, and psychological tension rather than explicit violence, aligning with psychological horror."
        )

    if final_genre == "Slasher":
        return (
            "The presence of a masked killer targeting victims in a confined setting strongly aligns with the slasher horror sub-genre."
        )

    if final_genre == "Cyberpunk":
        return (
            "The story combines advanced technology with a futuristic urban setting, which are defining features of cyberpunk fiction."
        )

    if final_genre == "Hard Sci-Fi":
        return (
            "The narrative focuses on scientifically grounded concepts and technical detail, which is characteristic of hard science fiction."
        )

    if final_genre == "Space Opera":
        return (
            "The story emphasizes large-scale space-based elements and futuristic adventure, which fits the space opera sub-genre."
        )

    # Fallback (should rarely be hit)
    return (
        "The genre was selected based on the dominant themes and context present in the story."
    )
