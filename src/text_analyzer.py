import re
from typing import Dict, List, Optional

# Optional lightweight NLP
try:
    import nltk
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import stopwords

    nltk_available = True
except ImportError:
    nltk_available = False


lemmatizer = WordNetLemmatizer() if nltk_available else None
stop_words = set(stopwords.words("english")) if nltk_available else set()


def preprocess_text(text: str) -> List[str]:
    """
    Light NLP preprocessing:
    - lowercase
    - remove punctuation
    - tokenize
    - optional lemmatization
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = text.split()

    if nltk_available:
        tokens = [
            lemmatizer.lemmatize(token)
            for token in tokens
            if token not in stop_words
        ]

    return tokens


def extract_rule_based_signals(tokens: List[str]) -> Dict[str, bool]:
    """
    Deterministic, explainable semantic signals.
    """

    joined_text = " ".join(tokens)

    return {
        # Romance signals (explicit + implicit)
        "romance": any(word in tokens for word in [
            "love", "loved", "romantic", "relationship",
            "together", "met", "married"
        ]),
        "conflict": any(word in tokens for word in [
            "hate", "hated", "enemy", "battle", "war"
        ]),

        # Thriller
        "legal": any(word in tokens for word in ["lawyer", "judge", "court", "trial"]),
        "espionage": any(word in tokens for word in ["spy", "agent", "kgb", "cia"]),

        # Horror
        "horror": any(word in tokens for word in ["fear", "scary", "dark", "ghost", "killer"]),
        "gothic": any(word in joined_text for word in ["mansion", "victorian", "corridor"]),
        "slasher": any(word in tokens for word in ["killer", "mask", "camp"]),

        # Sci-Fi
        "sci_fi": any(word in tokens for word in ["ai", "robot", "space", "future", "ftl", "physics", "time"]),
        "cyberpunk": any(word in joined_text for word in ["neon", "tokyo", "megacity"]),

        # Non-fiction
        "non_fiction": any(word in tokens for word in ["how", "build", "recipe", "mix", "bake"]),
    }


def extract_llm_signals(
    text: str,
    llm_client: Optional[object] = None
) -> Dict[str, Dict]:
    """
    Calls the LLM to extract ONLY:
    - setting
    - tone
    - themes

    Returns structured context.
    """

    if llm_client is None:
        return {}

    context = llm_client.generate(text)

    # Expecting a dict like:
    # { "setting": "...", "tone": "...", "themes": "..." }
    return {
        "llm_context": context if isinstance(context, dict) else {}
    }


def analyze_text(
    text: str,
    use_llm: bool = False,
    llm_client: Optional[object] = None
) -> Dict:
    """
    Main analysis entry point.
    """

    tokens = preprocess_text(text)
    rule_signals = extract_rule_based_signals(tokens)

    llm_signals = {}
    if use_llm and llm_client:
        llm_signals = extract_llm_signals(text, llm_client)

    if use_llm == True:
        print("LLM called!!")
    else:
        print("Continued without LLM!!")
    
    return {
        "tokens": tokens,
        "rule_signals": rule_signals,
        "llm_signals": llm_signals
    }
