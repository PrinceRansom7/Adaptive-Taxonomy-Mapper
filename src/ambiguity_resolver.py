from typing import Dict, Optional

class AmbiguityResolver:
    """
    Resolves conflicts between heuristic signals using LLM-derived native focus.
    """
    
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def resolve(self, story_text: str, current_genre: Optional[str], rule_signals: Dict[str, bool]) -> Optional[str]:
        """
        Refines the genre choice if ambiguity is detected.
        """
        # If no LLM, we can't refine
        if not self.llm_client:
            return current_genre

        # 1. Check for specific ambiguous patterns
        # Pattern A: Cyberpunk vs Love (e.g. Case 4)
        has_sci_fi = rule_signals.get("cyberpunk") or rule_signals.get("sci_fi")
        has_romance = rule_signals.get("romance")
        
        if has_sci_fi and has_romance:
            # Ambiguity detected! Consult LLM Focus.
            focus = self.llm_client.get_dominant_focus(story_text)
            
            if focus == "emotional_evolution":
                # Override to Romance (Slow-burn is the safest default for emotional focus)
                return "Slow-burn"
            elif focus == "technical_scientific":
                return "Cyberpunk" if rule_signals.get("cyberpunk") else "Hard Sci-Fi"
        
        return current_genre
# Works well for small-size scaling
