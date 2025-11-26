# audio_manager.py
"""
AudioManager for the Real-Time Meeting Translator.

Responsibilities:
- Access the microphone (or chosen input device)
- Record short chunks of audio in real time
- Return audio data in a format that STT (Whisper) can use
"""

from typing import List, Tuple, Optional

import sounddevice as sd
import numpy as np

import config


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
        # If caller passes an explicit device, use it; otherwise, use config or default
        self.input_device = (
            input_device if input_device is not None else config.AUDIO_INPUT_DEVICE
        )

    # ---------- Device Helpers ----------

    def list_input_devices(self) -> List[Tuple[int, str]]:
        """
        Return a list of available audio INPUT devices as (index, name).

        This is useful for debugging or letting the user pick a specific mic.
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
            # This call will trigger the OS mic permission popup the first time
            recording = sd.rec(
                frames=num_frames,
                samplerate=self.sample_rate,
                channels=1,          # mono is enough for STT
                dtype="float32",
                device=self.input_device,
            )

            # Wait until recording is finished
            sd.wait()

        except Exception as e:
            # In a real app, you might want to log this and show an error in the UI
            raise RuntimeError(f"Error while recording audio: {e}")

        # recording shape is (num_frames, 1) → flatten to (num_frames,)
        audio_mono: np.ndarray = recording.flatten()

        return audio_mono, self.sample_rate


# ---------- Manual Test ----------

if __name__ == "__main__":
    """
    Simple test script to verify that your microphone and AudioManager work.

    Run:
        python audio_manager.py

    It will:
    - Print available input devices
    - Wait for Enter
    - Record one chunk
    - Print basic info
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
