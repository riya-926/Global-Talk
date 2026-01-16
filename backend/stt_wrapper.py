"""
Wrapper functions for STT module to work with file paths
"""
from pathlib import Path
import wave
import numpy as np
from backend.stt_module import STTModule
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from . import config

# Initialize STT module
stt_module = STTModule()

def transcribe_audio(file_path: str | Path) -> dict:
    """
    Transcribe audio file and detect language.

    :param file_path: Path to WAV file
    :return: {"text": "...", "language": "en"}
    """
    try:
        # Read WAV file
        with wave.open(str(file_path), 'rb') as wf:
            sample_rate = wf.getframerate()
            frames = wf.readframes(wf.getnframes())

            # Convert bytes to numpy array
            audio_data = np.frombuffer(frames, dtype=np.int16)
            # Convert int16 to float32 [-1, 1]
            audio_data = audio_data.astype(np.float32) / 32768.0

        # Transcribe
        text, language = stt_module.transcribe_and_detect(audio_data, sample_rate)

        return {
            "text": text,
            "language": language
        }

    except Exception as e:
        print(f"❌ Error transcribing {file_path}: {e}")
        return {
            "text": "",
            "language": "unknown"
        }