import os
import json
from typing import Dict, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class SafeLLMClient:
    """
    Safety-scoped LLM client.

    The LLM is used ONLY to extract:
    - setting
    - tone
    - themes

    It is explicitly forbidden from:
    - naming genres
    - classifying content
    - making decisions
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini"
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

        if self.api_key and OpenAI:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def generate(self, story_text: str) -> Dict[str, str]:
        """
        Extract structured narrative context from the story.

        Expected output format:
        {
          "setting": "...",
          "tone": "...",
          "themes": "..."
        }
        """

        # Safe fallback: LLM disabled or not configured
        if self.client is None:
            return {}

        system_prompt = (
            "You extract narrative context from stories.\n\n"
            "Return ONLY a JSON object with these keys:\n"
            "- setting\n"
            "- tone\n"
            "- themes\n\n"
            "Rules:\n"
            "- Do NOT mention genres\n"
            "- Do NOT classify the story\n"
            "- Do NOT add explanations\n"
            "- Output JSON only\n"
        )

        user_prompt = f"""Story: \"\"\"{story_text}\"\"\"
        Extract the setting, tone, and themes."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2
            )

            content = response.choices[0].message.content.strip()
            parsed = json.loads(content)

            return {
                "setting": parsed.get("setting", ""),
                "tone": parsed.get("tone", ""),
                "themes": parsed.get("themes", "")
            }

        except Exception:
            #  Any failure -> silent, safe fallback
            return {}

    def get_dominant_focus(self, story_text: str) -> str:
        """
        Identify the primary narrative driver.
        Returns one of: 'emotional_evolution', 'technical_scientific', 'atmosphere', 'action_conflict'
        """
        if self.client is None:
            return "unknown"

        system_prompt = (
            "You identify the DOMINANT narrative focus of a story snippet.\n"
            "Return ONLY one of these exact strings:\n"
            "- emotional_evolution (if focus is relationships, feelings, love)\n"
            "- technical_scientific (if focus is technology, physics, systems)\n"
            "- atmosphere (if focus is dread, setting, mood)\n"
            "- action_conflict (if focus is fighting, legal battles, spies)\n\n"
            "Rules:\n"
            "- Pick the single strongest driver.\n"
            "- Do NOT mention genres.\n"
            "- Output ONLY the label.\n"
        )
        
        user_prompt = f"Story: \"\"\"{story_text}\"\"\""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return "unknown"
