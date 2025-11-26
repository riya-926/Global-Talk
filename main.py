# main.py
"""
Simple live loop for the Real-Time Meeting Translator (no UI yet).

Flow:
- Ask user what language they want to see translations in
- Repeatedly:
    - Record a short audio chunk from the mic
    - Optionally skip very quiet chunks (background noise)
    - Transcribe + auto-detect language with Whisper
    - Skip chunks where detected language matches user's own language
      (assuming that's likely the user speaking)
    - Translate text into target language with GPT
    - Print original + translated text in the terminal
"""

import time
from typing import Optional

import numpy as np

import config
from audio_manager import AudioManager
from stt_module import STTModule
from translation_module import TranslationModule


def canonicalize_target_lang(user_input: str) -> str:
    """
    Normalize the target language the user types so we can compare it
    to Whisper's detected language more reliably.

    Examples:
      "en" -> "english"
      "english" -> "english"
      "fr" -> "french"
      "hi" -> "hindi"
    """
    s = user_input.strip().lower()

    mapping = {
        "en": "english",
        "eng": "english",
        "english": "english",

        "es": "spanish",
        "spa": "spanish",
        "spanish": "spanish",

        "fr": "french",
        "fra": "french",
        "french": "french",

        "hi": "hindi",
        "hin": "hindi",
        "hindi": "hindi",

        "ur": "urdu",
        "urd": "urdu",
        "urdu": "urdu",

        "pt": "portuguese",
        "por": "portuguese",
        "portuguese": "portuguese",

        "de": "german",
        "ger": "german",
        "german": "german",

        "it": "italian",
        "ita": "italian",
        "italian": "italian",
    }

    return mapping.get(s, s)  # default to whatever they typed if unknown


def is_very_quiet(audio_chunk: np.ndarray, threshold: float = 0.005) -> bool:
    """
    Simple heuristic to skip very quiet chunks (likely background noise).

    :param audio_chunk: 1D numpy array of audio samples [-1, 1].
    :param threshold: Mean absolute amplitude below which we treat as "silent/noise".
    """
    if audio_chunk.size == 0:
        return True
    mean_amp = float(np.mean(np.abs(audio_chunk)))
    return mean_amp < threshold


def main():
    # Validate config (checks OPENAI_API_KEY)
    config.validate_config()

    print("=== Global-Talk: Terminal Demo ===")
    print("This will record short chunks from your microphone,")
    print("transcribe them with Whisper, and translate them using GPT.\n")

    # Ask user for target language
    target_lang_input = input(
        "Enter the language you want to see translations in "
        "(e.g., 'english', 'en', 'hindi', 'french') [default: english]: "
    ).strip()
    if target_lang_input == "":
        target_lang_input = "english"

    # Canonicalize for comparison with Whisper's detected language
    canonical_target_lang = canonicalize_target_lang(target_lang_input)

    print(f"\nTarget language set to: {canonical_target_lang}")
    print(f"Chunk duration: {config.AUDIO_CHUNK_SECONDS} seconds")
    print("Press Ctrl+C to stop.\n")

    # Initialize modules
    audio_manager = AudioManager()
    stt = STTModule()
    translator = TranslationModule()

    try:
        while True:
            print("🎙️  Listening for next chunk...")
            audio_chunk, sr = audio_manager.get_audio_chunk()

            # 1) Skip very quiet chunks (background noise / silence)
            if is_very_quiet(audio_chunk):
                print("(Very low volume / background noise, skipping this chunk)\n")
                continue

            # 2) STT + language detection
            transcript, detected_lang = stt.transcribe_and_detect(audio_chunk, sr)

            if not transcript.strip():
                print("(No speech detected in this chunk, skipping)\n")
                continue

            detected_lang_norm = (detected_lang or "").strip().lower()

            # 3) Skip chunks where detected language == user's language
            #    (Assuming user speaks the target language → this is likely the user)
            if detected_lang_norm and canonical_target_lang:
                # Simple matching: exact match OR one contained in the other
                if (
                    detected_lang_norm == canonical_target_lang
                    or canonical_target_lang in detected_lang_norm
                    or detected_lang_norm in canonical_target_lang
                ):
                    print(
                        f"(Detected language '{detected_lang}' matches your language "
                        f"'{canonical_target_lang}' → likely you speaking, skipping)\n"
                    )
                    continue

            # 4) Otherwise, treat this as "other person" and translate
            print(f"\n Detected language: {detected_lang}")
            print(f"Original: {transcript}")

            translated = translator.translate(
                text=transcript,
                source_lang=detected_lang,        # from Whisper
                target_lang=canonical_target_lang,  # normalized
            )

            print(f" Translated ({canonical_target_lang}): {translated}\n")
            print("-" * 60)

            # Small pause so prints don't spam too hard
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n\nStopping Global-Talk demo. Goodbye! 👋")

    except Exception as e:
        print("\n An error occurred:")
        print(e)


if __name__ == "__main__":
    main()
