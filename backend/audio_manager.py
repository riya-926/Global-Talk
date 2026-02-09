"""
AudioManager for the Real-Time Meeting Translator.

Responsibilities:
- Access the microphone (or chosen input device)
- Record short chunks of audio in real time
- Save chunks to WAV files for processing
"""

from typing import List, Tuple, Optional
from pathlib import Path
from datetime import datetime
import threading
import wave

import sounddevice as sd
import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from . import config

class AudioManager:
    def __init__(
        self,
        chunk_duration: Optional[float] = None,
        sample_rate: Optional[int] = None,
        input_device: Optional[int | str] = None,
    ) -> None:
        """
        Initialize the AudioManager.

        :param chunk_duration: Length of each recorded chunk in seconds.
                               If None, uses config.AUDIO_CHUNK_SECONDS.
        :param sample_rate: Sample rate for recording (Hz).
                            If None, uses config.AUDIO_SAMPLE_RATE.
        :param input_device: Optional device index or name.
                             If None, uses system default input device.
        """
        self.chunk_duration = chunk_duration or config.AUDIO_CHUNK_SECONDS
        self.sample_rate = sample_rate or config.AUDIO_SAMPLE_RATE
        self.input_device = (
            input_device if input_device is not None else config.AUDIO_INPUT_DEVICE
        )
        
        # For continuous recording
        self.is_recording = False
        self.recording_thread = None
        self.output_dir = Path("recordings")
        self.output_dir.mkdir(exist_ok=True)
        self.latest_file = None

    # ---------- Device Helpers ----------

    def list_input_devices(self) -> List[Tuple[int, str]]:
        """
        Return a list of available audio INPUT devices as (index, name).
        """
        devices = sd.query_devices()
        input_devices: List[Tuple[int, str]] = []

        for idx, dev in enumerate(devices):
            if dev["max_input_channels"] > 0:
                input_devices.append((idx, dev["name"]))

        return input_devices

    # ---------- Recording ----------

    def get_audio_chunk(self) -> Tuple[np.ndarray, int]:
        """
        Record a single chunk of audio from the microphone.

        :return: (audio_data, sample_rate)
                 - audio_data: 1D numpy array of float32 samples in range [-1.0, 1.0]
                 - sample_rate: integer sample rate in Hz
        """
        num_frames = int(self.sample_rate * self.chunk_duration)

        try:
            recording = sd.rec(
                frames=num_frames,
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                device=self.input_device,
            )
            sd.wait()

        except Exception as e:
            raise RuntimeError(f"Error while recording audio: {e}")

        audio_mono: np.ndarray = recording.flatten()
        return audio_mono, self.sample_rate

    # ---------- Continuous Recording ----------

    def start_recording(self):
        """Start continuous recording in background thread"""
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self._record_loop, daemon=True)
        self.recording_thread.start()
        print("Continuous recording started...")

    def stop_recording(self):
        """Stop continuous recording"""
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join(timeout=5)
        print("Recording stopped!")

    def _record_loop(self):
        """Background thread that continuously records audio chunks"""
        while self.is_recording:
            try:
                # Get audio chunk
                audio_data, sr = self.get_audio_chunk()
                
                # Save to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = self.output_dir / f"chunk_{timestamp}.wav"
                
                self._save_wav(filename, audio_data, sr)
                self.latest_file = filename
                
            except Exception as e:
                print(f"Error in recording loop: {e}")
                break

    def _save_wav(self, filename: Path, audio_data: np.ndarray, sample_rate: int):
        """Save audio data to WAV file"""
        # Convert float32 [-1, 1] to int16
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        with wave.open(str(filename), 'wb') as wf:
            wf.setnchannels(1)  # mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(sample_rate)
            wf.writeframes(audio_int16.tobytes())

    def get_latest_recording(self) -> Optional[Path]:
        """Get the path to the most recent recording file"""
        return self.latest_file

    def clear_recordings(self):
        """Clear all recording files"""
        for file in self.output_dir.glob("chunk_*.wav"):
            try:
                file.unlink()
            except:
                pass
        print("Cleared all recordings")


# ---------- Manual Test ----------

if __name__ == "__main__":
    """
    Simple test script to verify that your microphone and AudioManager work.
    """
    print("Initializing AudioManager...")
    am = AudioManager()

    print("\nAvailable input devices:")
    for idx, name in am.list_input_devices():
        print(f"  {idx}: {name}")

    input("\nPress Enter to record a test audio chunk...")

    audio, sr = am.get_audio_chunk()
    print(f"\nRecorded audio chunk with {len(audio)} samples at {sr} Hz.")
    print("First 10 samples:", audio[:10])
    print("\nIf you see numbers above, AudioManager is working correctly.")