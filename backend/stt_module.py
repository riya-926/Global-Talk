# stt_module.py
"""
STTModule for the Real-Time Meeting Translator.

Uses:
- OpenAI Whisper (whisper-1) for Speech-to-Text
- Automatically detects the spoken language
"""

from typing import Tuple
import io

import numpy as np
from openai import OpenAI
from . import config


class STTModule:
    def __init__(self, api_key: str | None = None, model_name: str | None = None) -> None:
        """
        Initialize the STT module for Whisper.

        :param api_key: OpenAI API key. If None, uses config.OPENAI_API_KEY.
        :param model_name: Whisper model name. If None, uses config.OPENAI_STT_MODEL.
        """
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model_name = model_name or config.OPENAI_STT_MODEL

        if self.api_key is None:
            raise RuntimeError(
                "OpenAI API key is not set. "
                "Make sure OPENAI_API_KEY is defined in your environment."
            )

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def _numpy_to_wav_bytes(self, audio_data: np.ndarray, sample_rate: int) -> bytes:
        """
        Convert a 1D float32 numpy array [-1, 1] to WAV bytes in memory.
        Whisper API expects an audio file-like object, so we create WAV in memory.
        """
        import soundfile as sf  # lightweight dependency for writing WAV

        buffer = io.BytesIO()
        # soundfile wants float32 array and sample rate
        sf.write(buffer, audio_data, sample_rate, format="WAV")
        buffer.seek(0)
        return buffer.read()

    def transcribe_and_detect(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
    ) -> Tuple[str, str]:
        """
        Transcribe audio and detect language using OpenAI Whisper.

        :param audio_data: 1D numpy array of float32 audio samples [-1, 1].
        :param sample_rate: Sample rate in Hz (e.g., 16000).
        :return: (transcript_text, detected_language_code)
        """
        # Convert numpy audio to WAV bytes
        wav_bytes = self._numpy_to_wav_bytes(audio_data, sample_rate)

        # Wrap bytes in a file-like object with a name (OpenAI SDK expects a file)
        audio_file = io.BytesIO(wav_bytes)
        audio_file.name = "chunk.wav"

        # Call Whisper via the Audio API
        # Model name comes from config.OPENAI_STT_MODEL (e.g., "whisper-1")
        response = self.client.audio.transcriptions.create(
            model=self.model_name,
            file=audio_file,
            # Whisper auto-detects language by default
            # But you can also set language=... if you know it
            response_format="verbose_json",  # gives us text + language
        )

        # response should contain .text and .language
        transcript_text: str = response.text
        detected_language_code: str = getattr(response, "language", "unknown")

        return transcript_text, detected_language_code


# ---------- Manual Test ----------

if __name__ == "__main__":
    """
    Simple test for STTModule.

    This expects you to already have:
    - OPENAI_API_KEY set
    - audio_manager.py working

    It will:
    - Record one chunk of audio from the mic
    - Send to Whisper
    - Print transcript + detected language
    """

    import audio_manager

    print("Initializing AudioManager and STTModule...")
    am = audio_manager.AudioManager()
    stt = STTModule()

    input("Press Enter to record a test chunk and transcribe it...")

    audio_chunk, sr = am.get_audio_chunk()
    print("Recording done. Sending to Whisper...")

    text, lang = stt.transcribe_and_detect(audio_chunk, sr)

    print("\n=== STT RESULT ===")
    print("Detected language:", lang)
    print("Transcript:")
    print(text)
