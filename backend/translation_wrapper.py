"""
Wrapper functions for Translation module
"""
from backend.translation_module import TranslationModule
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from . import config

# Initialize translation module
translation_module = TranslationModule()

# Language code to name mapping
LANGUAGE_NAMES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'hi': 'Hindi'
}

def translate_text(text: str, target_language: str, source_language: str = None) -> dict:
    """
    Translate text to target language.

    :param text: Text to translate
    :param target_language: Target language code (e.g., 'en', 'es')
    :param source_language: Source language code (optional)
    :return: {"translated_text": "..."}
    """
    try:
        if not text.strip():
            return {"translated_text": ""}

        # Convert language codes to names
        target_lang_name = LANGUAGE_NAMES.get(target_language, target_language)
        source_lang_name = LANGUAGE_NAMES.get(source_language, source_language) if source_language else None

        # Translate
        translated = translation_module.translate(
            text=text,
            source_lang=source_lang_name,
            target_lang=target_lang_name
        )

        return {
            "translated_text": translated
        }

    except Exception as e:
        print(f"❌ Error translating text: {e}")
        return {
            "translated_text": text  # Return original if translation fails
        }