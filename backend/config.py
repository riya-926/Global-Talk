"""
Configuration file for the Real-Time Meeting Translator.
Using:
- OpenAI Whisper (Speech-to-Text + auto language detection)
- OpenAI GPT-4o-mini (Translation)
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =========================
# General App Settings
# =========================

# Default target language for subtitles (ISO code)
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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Speech-to-Text (Whisper) model
OPENAI_STT_MODEL = "whisper-1"

# Translation model
OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


# =========================
# Validation Helper
# =========================

def validate_config():
    """
    Ensures that required environment variables are set.
    """
    missing = []

    if OPENAI_API_KEY is None:
        missing.append("OPENAI_API_KEY")

    if missing:
        msg = (
            "Missing required configuration:\n" +
            "\n".join(f" - {m}" for m in missing) +
            "\n\nCreate a .env file with:\n"
            "OPENAI_API_KEY=your-key-here\n\n"
            "Or set as environment variable."
        )
        raise RuntimeError(msg)
    
    print("✅ Configuration validated!")
    print(f"   Using model: {OPENAI_TRANSLATION_MODEL}")
    print(f"   Audio chunks: {AUDIO_CHUNK_SECONDS}s")