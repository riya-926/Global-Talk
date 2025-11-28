# translation_module.py
"""
TranslationModule for the Real-Time Meeting Translator.

Uses:
- OpenAI GPT-4o-mini (or the model set in config.OPENAI_TRANSLATION_MODEL)
to translate text from a detected source language into the user's target language.
"""

from typing import Optional

from openai import OpenAI

import config


class TranslationModule:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> None:
        """
        Initialize the TranslationModule.

        :param api_key: OpenAI API key. If None, uses config.OPENAI_API_KEY.
        :param model_name: Translation model name.
                           If None, uses config.OPENAI_TRANSLATION_MODEL.
        """
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model_name = model_name or config.OPENAI_TRANSLATION_MODEL

        if self.api_key is None:
            raise RuntimeError(
                "OpenAI API key is not set. "
                "Make sure OPENAI_API_KEY is defined in your environment."
            )

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def translate(
        self,
        text: str,
        source_lang: Optional[str],
        target_lang: str,
    ) -> str:
        """
        Translate `text` from source_lang to target_lang using GPT.

        :param text: The original text to translate.
        :param source_lang: The language the text is in (e.g., 'spanish', 'fr', 'ur', etc.).
                            If None, the model will infer it from context.
        :param target_lang: Target language as a human-readable name or ISO code
                            (e.g., 'english', 'en', 'hi', 'french').
        :return: Translated text as a string.
        """
        if not text.strip():
            return ""

        # Build a clear system prompt so GPT behaves like a pure translator
        source_desc = source_lang if source_lang else "auto-detected language"

        system_prompt = (
            "You are a translation engine for a real-time meeting app. "
            "Translate as literally and accurately as possible while keeping good grammar. "
            "NEVER change numbers, dates, times, or days of the week. "
            "If the text says Monday, keep Monday. If it says Wednesday, keep Wednesday. "
            "Respond with ONLY the translated text, no explanations, no quotes."
        )


        user_prompt = (
            f"Source language: {source_desc}\n"
            f"Target language: {target_lang}\n\n"
            f"Text to translate:\n{text}"
        )

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,  # low temperature for consistent translations
        )

        translated = response.choices[0].message.content.strip()
        return translated


# ---------- Manual Test ----------

if __name__ == "__main__":
    """
    Simple manual test for TranslationModule.

    Run:
        python translation_module.py

    Then follow the prompts:
    - Enter source language (or leave blank to let the model infer)
    - Enter target language (e.g., "english", "en", "hindi", "french")
    - Enter a sentence to translate
    """
    tm = TranslationModule()

    print("=== TranslationModule Test ===")
    src = input("Source language (e.g., 'spanish', 'fr', 'urdu', or leave blank): ").strip()
    if src == "":
        src = None

    tgt = input("Target language (e.g., 'english', 'en', 'hindi', 'french'): ").strip()
    if tgt == "":
        tgt = "english"

    print("\nType a sentence to translate:")
    text = input("> ")

    print("\nTranslating...")
    translated_text = tm.translate(text, source_lang=src, target_lang=tgt)

    print("\n=== RESULT ===")
    print(translated_text)
