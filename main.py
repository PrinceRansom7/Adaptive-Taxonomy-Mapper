import json
from pathlib import Path

from src.taxonomy_loader import load_taxonomy, get_leaf_genres
from src.text_analyzer import analyze_text
from src.mapper import map_to_genre
from src.validator import validate_mapping, UNMAPPED_LABEL
from src.reasoning import generate_reasoning
from src.llm_helper import SafeLLMClient
from src.ambiguity_resolver import AmbiguityResolver

llm_client = SafeLLMClient()
resolver = AmbiguityResolver(llm_client)


DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")


def load_test_cases(file_path: Path):
    """Load the golden test cases."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_results(results, file_path: Path):
    """Save final mapping results to a JSON file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)


def main():
    # 1. Load taxonomy
    taxonomy = load_taxonomy(DATA_DIR / "taxonomy.json")
    allowed_genres, _ = get_leaf_genres(taxonomy)

    # 2. Load test cases
    test_cases = load_test_cases(DATA_DIR / "test_cases.json")

    results = []

    # 3. Process each test case
    for case in test_cases:
        case_id = case.get("id")
        user_tags = case.get("user_tags", [])
        story_text = case.get("story_snippet", "")

        # Step 1: Analyze text (heuristics)
        # Note: We keep use_llm=False here because we use the specific ambiguity resolver later
        analysis = analyze_text(
            text=story_text,
            use_llm=False,       
            llm_client=None
        )

        # Step 2: Propose a genre using heuristics
        proposed_genre = map_to_genre(
            analysis=analysis,
            user_tags=user_tags
        )
        
        # Step 2.5: Resolve Ambiguity (The Helper)
        refined_genre = resolver.resolve(
            story_text=story_text,
            current_genre=proposed_genre,
            rule_signals=analysis.get("rule_signals", {})
        )

        # Step 3: Validate against taxonomy
        final_genre = validate_mapping(
            proposed_genre=refined_genre,
            allowed_genres=allowed_genres
        )

        # Step 4: Generate reasoning
        reasoning = generate_reasoning(
            story_text=story_text,
            rule_signals=analysis.get("rule_signals", {}),
            final_genre=final_genre
        )

        results.append({
            "id": case_id,
            "mapped_genre": final_genre,
            "reasoning": reasoning
        })

    # 4. Save results
    save_results(results, OUTPUT_DIR / "results1.json")

    print("Mapping complete. Results saved to outputs/results.json")

if __name__ == "__main__":
    main()
    

