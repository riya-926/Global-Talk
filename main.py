"""
main.py - Connects backend modules to the UI

Project structure:
Global-Talk/
├── backend/
│   ├── config.py
│   ├── audio_manager.py
│   ├── stt_module.py
│   └── translation_module.py
├── frontend/
│   └── ui.py
├── main.py (this file)
└── sessions/ (auto-created)
"""

import sys
import time
import threading
import queue
from collections import deque

import numpy as np
import sounddevice as sd

# Import backend modules
sys.path.append('backend')
from backend import config
from backend.stt_module import STTModule
from backend.translation_module import TranslationModule

# Import frontend
sys.path.append('frontend')
from frontend.ui import GlobalChatUI


def is_useful_transcript(text: str) -> bool:
    """Return False for tiny junk like '.', '..', '?' or 1-2 character clips."""
    clean = text.strip()
    if not clean:
        return False
    # TEMPORARILY RELAXED - accept more to test
    if len(clean) <= 1:  # Only filter single characters
        return False
    return True  # Accept everything else for testing


def has_voice_activity(audio_chunk: np.ndarray, threshold: float = 0.005) -> bool:
    """
    Simple Voice Activity Detection.
    Returns True if audio chunk has enough energy to be considered speech.

    :param audio_chunk: numpy array of audio samples
    :param threshold: minimum RMS energy threshold (lower = more sensitive)
    """
    # Calculate RMS (Root Mean Square) energy
    rms = np.sqrt(np.mean(audio_chunk ** 2))

    # DEBUG: print energy level to help tune threshold
    print(f"🔊 Audio energy: {rms:.4f} | Threshold: {threshold} | {'✅ PROCESSING' if rms > threshold else '❌ SKIPPED'}")

    return rms > threshold


class ContinuousAudioRecorder:
    """Records audio continuously and puts chunks into a queue."""

    def __init__(self, chunk_duration: float, sample_rate: int, audio_queue: queue.Queue):
        self.chunk_duration = chunk_duration
        self.sample_rate = sample_rate
        self.audio_queue = audio_queue
        self.is_recording = False
        self.audio_buffer = deque()

    def audio_callback(self, indata, frames, time_info, status):
        """Called by sounddevice for each audio block."""
        if status:
            print(f"Audio status: {status}")
        # Add audio to buffer
        self.audio_buffer.extend(indata[:, 0].copy())  # mono channel

        # If we have enough samples for a chunk, put it in the queue
        chunk_size = int(self.sample_rate * self.chunk_duration)
        while len(self.audio_buffer) >= chunk_size:
            # Extract chunk
            chunk = np.array([self.audio_buffer.popleft() for _ in range(chunk_size)])
            if not self.audio_queue.full():
                self.audio_queue.put(chunk)

    def start(self):
        """Start continuous recording in background."""
        self.is_recording = True
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=self.audio_callback,
            blocksize=int(self.sample_rate * 0.1)  # 100ms blocks
        )
        self.stream.start()
        print("🎤 Continuous recording started...")

    def stop(self):
        """Stop recording."""
        self.is_recording = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        print("🎤 Recording stopped.")


class GlobalChatApp:
    """Main application class that coordinates everything."""

    def __init__(self):
        # Validate config
        config.validate_config()

        # Initialize UI
        self.ui = GlobalChatUI()

        # Set UI callbacks
        self.ui.on_start_callback = self.start_translation
        self.ui.on_stop_callback = self.stop_translation

        # Backend modules
        self.stt = STTModule()
        self.translator = TranslationModule()

        # Recording state
        self.recorder = None
        self.audio_queue = None
        self.result_queue = None
        self.stop_event = None
        self.worker_thread = None
        self.target_language = "english"

    def start_translation(self, target_lang: str):
        """Called when user clicks Start button."""
        print(f"\n🚀 Starting translation to: {target_lang}")
        self.target_language = target_lang

        # Create queues
        self.audio_queue = queue.Queue(maxsize=10)
        self.result_queue = queue.Queue()
        self.stop_event = threading.Event()

        # Start recorder
        self.recorder = ContinuousAudioRecorder(
            chunk_duration=config.AUDIO_CHUNK_SECONDS,
            sample_rate=config.AUDIO_SAMPLE_RATE,
            audio_queue=self.audio_queue
        )
        self.recorder.start()

        # Start processing worker
        self.worker_thread = threading.Thread(
            target=self.process_audio_worker,
            daemon=True
        )
        self.worker_thread.start()

        # Start result display loop
        self.check_results()

    def stop_translation(self):
        """Called when user clicks End Chat button."""
        print("\n⏹️  Stopping translation...")

        if self.stop_event:
            self.stop_event.set()

        if self.recorder:
            self.recorder.stop()

        if self.worker_thread:
            self.worker_thread.join(timeout=2)

        print("✅ Translation stopped.")

    def process_audio_worker(self):
        """Worker thread that processes audio chunks."""
        print("🔧 Processing worker started!")

        while not self.stop_event.is_set() or not self.audio_queue.empty():
            try:
                # Get audio chunk with timeout
                audio_chunk = self.audio_queue.get(timeout=0.5)
                print("📦 Got audio chunk from queue...")

                # Check for voice activity FIRST (skip if silence)
                if not has_voice_activity(audio_chunk, threshold=0.005):
                    continue

                print("🎙️ Sending to Whisper API...")

                # 1) Transcribe + detect language
                transcript, detected_lang = self.stt.transcribe_and_detect(
                    audio_chunk,
                    config.AUDIO_SAMPLE_RATE
                )
                clean = transcript.strip()

                print(f"📝 Whisper returned: '{clean}' (lang: {detected_lang})")

                if not is_useful_transcript(clean):
                    print(f"⏭️ Skipping transcript (too short or filtered): '{clean}'")
                    continue

                print(f"🗣  Detected: {detected_lang} | Original: {clean}")

                # 2) Translate
                print(f"🌍 Translating to {self.target_language}...")
                translated = self.translator.translate(
                    text=clean,
                    source_lang=detected_lang,
                    target_lang=self.target_language,
                )

                print(f"✅ Translated: {translated}")

                # 3) Put result in output queue
                self.result_queue.put({
                    'original': clean,
                    'translated': translated,
                    'language': detected_lang
                })

            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Error processing audio: {e}")
                import traceback
                traceback.print_exc()

    def check_results(self):
        """Check for new translation results and update UI."""
        try:
            # Non-blocking check for results
            while not self.result_queue.empty():
                result = self.result_queue.get_nowait()

                # Add to UI
                self.ui.add_translation(
                    original=result['original'],
                    translated=result['translated'],
                    detected_lang=result['language']
                )
        except queue.Empty:
            pass

        # Schedule next check (every 100ms)
        self.ui.root.after(100, self.check_results)

    def run(self):
        """Start the application."""
        print("=" * 60)
        print("🌍 GLOBAL CHAT - Real-Time Translation")
        print("=" * 60)
        print("\nStarting UI...\n")

        self.ui.run()


if __name__ == "__main__":
    app = GlobalChatApp()
    app.run()