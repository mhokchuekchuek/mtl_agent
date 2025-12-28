"""Translation agent for language translation."""

import json
from typing import Any

from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger
from src.modules.agents.base import BaseAgent

logger = get_logger(__name__)


class TranslationAgent(BaseAgent):
    """Agent for translating text between Thai and English."""

    def __init__(
        self,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        prompt_name: str = "translation",
        prompt_label: str | None = None,
    ):
        """Initialize translation agent.

        Args:
            llm_client: LLM client for translation.
            prompt_manager: Prompt manager for retrieving prompts.
            prompt_name: Name of the prompt in prompt manager.
            prompt_label: Label for prompt retrieval (e.g., "latest", "production").
        """
        super().__init__(name="translation")
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.prompt_name = prompt_name
        self.prompt_label = prompt_label

    def detect_language(self, text: str) -> str:
        """Detect if text is Thai or English.

        Args:
            text: Text to analyze.

        Returns:
            Language code: "th" or "en"
        """
        if not text or not text.strip():
            return "en"

        # Use translation prompt with target "en" to detect source language
        result = self.translate(text, "en")
        return result.get("source_lang", "en")

    def translate(self, text: str, target_lang: str) -> dict:
        """Translate text to target language.

        Args:
            text: Text to translate.
            target_lang: Target language code ("th" or "en").

        Returns:
            Dictionary with translated_text, source_lang, target_lang.
        """
        if not text or not text.strip():
            return {
                "translated_text": text,
                "source_lang": "en",
                "target_lang": target_lang,
            }

        try:
            # Get prompt from prompt manager
            prompt = self.prompt_manager.get_prompt(
                self.prompt_name,
                label=self.prompt_label,
            )

            # Compile prompt with variables
            compiled = prompt.compile(
                text=text,
                target_lang=target_lang,
            )

            # Generate translation using LLM
            response = self.llm_client.generate(prompt=compiled)

            # Parse JSON response
            result = json.loads(response)

            return {
                "translated_text": result.get("translated_text", text),
                "source_lang": result.get("source_lang", "en"),
                "target_lang": target_lang,
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse translation response: {e}")
            return {
                "translated_text": text,
                "source_lang": "en",
                "target_lang": target_lang,
            }
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return {
                "translated_text": text,
                "source_lang": "en",
                "target_lang": target_lang,
            }

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute translation based on state.

        Args:
            state: Current state with keys:
                - user_input: str - text to process
                - target_lang: str (optional) - "th" or "en"

        Returns:
            Updated state with:
                - translated_text: str
                - detected_lang: str
                - target_lang: str
        """
        user_input = state.get("user_input", "")
        target_lang = state.get("target_lang")

        # Detect language if target not specified
        detected_lang = self.detect_language(user_input)

        # If no target specified, translate to opposite language
        if not target_lang:
            target_lang = "en" if detected_lang == "th" else "th"

        # Skip translation if already in target language
        if detected_lang == target_lang:
            return {
                **state,
                "translated_text": user_input,
                "detected_lang": detected_lang,
                "target_lang": target_lang,
            }

        # Translate
        result = self.translate(user_input, target_lang)

        return {
            **state,
            "translated_text": result["translated_text"],
            "detected_lang": detected_lang,
            "target_lang": target_lang,
        }
