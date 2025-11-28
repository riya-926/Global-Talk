# config.py
"""
Configuration file for the Real-Time Meeting Translator.
Using:
- OpenAI Whisper (Speech-to-Text + auto language detection)
- OpenAI GPT-4.1 / GPT-4o-mini (Translation)
"""

import os


# =========================
# General App Settings
# =========================

# Default target language for subtitles (ISO code)
# Examples: "en" (English), "es" (Spanish), "fr" (French), "hi" (Hindi)
DEFAULT_TARGET_LANG = "en"

# Duration of each audio chunk recorded in real time (seconds)
AUDIO_CHUNK_SECONDS = 3.0

# Sample rate for recording audio (Whisper prefers 16k)
AUDIO_SAMPLE_RATE = 16000

# Optional specific audio input device
AUDIO_INPUT_DEVICE = None   # Leave None to use system default mic


# =========================
# OpenAI API Settings
# =========================

# Read your OpenAI API key from environment variable
# DO NOT hard-code your API key here.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Speech-to-Text (Whisper) model
# Options: "whisper-1", "gpt-4o-transcribe" in future, etc.
OPENAI_STT_MODEL = "whisper-1"

# Translation model (use GPT-4o-mini or GPT-4.1 for best accuracy)
# GPT-4o-mini is cheap + fast + accurate
OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


# =========================
# Validation Helper
# =========================

def validate_config():
    """
    Ensures that required environment variables are set.
    Call this at the start of your app.
    """
    missing = []

    if OPENAI_API_KEY is None:
        missing.append("OPENAI_API_KEY")

    if missing:
        msg = (
            "Missing required configuration values:\n" +
            "\n".join(f" - {m}" for m in missing) +
            "\n\nFix: Set them as environment variables.\n\n"
            "Example (Windows PowerShell):\n"
            "  $env:OPENAI_API_KEY=\"your_key_here\"\n\n"
            "Example (macOS/Linux):\n"
            "  export OPENAI_API_KEY=\"your_key_here\""
        )
        raise RuntimeError(msg)
