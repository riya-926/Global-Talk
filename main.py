"""
Improved main.py with CONTINUOUS recording (no gaps).

Changes:
- Records audio continuously in a background thread
- Processes chunks in parallel using a queue
- No missed speech between chunks
"""

import time
import threading
import queue
from collections import deque

import numpy as np
import sounddevice as sd

import config
from stt_module import STTModule
from translation_module import TranslationModule


def is_useful_transcript(text: str) -> bool:
    """Return False for tiny junk like '.', '..', '?' or 1-2 character clips."""
    clean = text.strip()
    if not clean:
        return False
    if len(clean) <= 2 and all(ch in ".?!," for ch in clean):
        return False
    return True


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


def process_audio_worker(audio_queue: queue.Queue, result_queue: queue.Queue, 
                         stt: STTModule, translator: TranslationModule, 
                         target_lang: str, stop_event: threading.Event):
    """Worker thread that processes audio chunks from the queue."""
    
    while not stop_event.is_set() or not audio_queue.empty():
        try:
            # Get audio chunk with timeout
            audio_chunk = audio_queue.get(timeout=0.5)
            
            # 1) Transcribe + detect language
            transcript, detected_lang = stt.transcribe_and_detect(
                audio_chunk, 
                config.AUDIO_SAMPLE_RATE
            )
            clean = transcript.strip()
            
            if not is_useful_transcript(clean):
                continue
            
            # 2) Translate
            translated = translator.translate(
                text=clean,
                source_lang=detected_lang,
                target_lang=target_lang,
            )
            
            # 3) Put result in output queue
            result_queue.put({
                'original': clean,
                'translated': translated,
                'language': detected_lang
            })
            
        except queue.Empty:
            continue
        except Exception as e:
            print(f"❌ Error processing audio: {e}")


def main():
    # Check API key
    config.validate_config()

    print("=== Global-Talk: Continuous Real-Time Translation ===")
    print("This will continuously record and translate in real-time.\n")

    target_lang = input(
        "Enter the language you want subtitles in "
        "(e.g., 'english', 'en', 'hindi', 'french') [default: english]: "
    ).strip()
    if target_lang == "":
        target_lang = "english"

    print(f"\nTarget language set to: {target_lang}")
    print(f"Chunk duration: {config.AUDIO_CHUNK_SECONDS} seconds")
    print("Speak near your mic. Press Ctrl+C to stop.\n")

    # Initialize modules
    stt = STTModule()
    translator = TranslationModule()
    
    # Create queues for communication between threads
    audio_queue = queue.Queue(maxsize=10)  # Limit queue size to prevent memory issues
    result_queue = queue.Queue()
    stop_event = threading.Event()
    
    # Start continuous recorder
    recorder = ContinuousAudioRecorder(
        chunk_duration=config.AUDIO_CHUNK_SECONDS,
        sample_rate=config.AUDIO_SAMPLE_RATE,
        audio_queue=audio_queue
    )
    recorder.start()
    
    # Start processing worker thread
    worker_thread = threading.Thread(
        target=process_audio_worker,
        args=(audio_queue, result_queue, stt, translator, target_lang, stop_event),
        daemon=True
    )
    worker_thread.start()
    
    try:
        print("🎧 Listening... (speak now)\n")
        
        while True:
            # Check for results and print them
            try:
                result = result_queue.get(timeout=0.1)
                print(f"\n🗣  Detected: {result['language']}")
                print(f"Original: {result['original']}")
                print(f"🌍 Translated: {result['translated']}")
                print("-" * 60)
            except queue.Empty:
                time.sleep(0.1)
                
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping...")
        stop_event.set()
        recorder.stop()
        worker_thread.join(timeout=2)
        print("Global-Talk stopped. Goodbye! 👋")
    
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        stop_event.set()
        recorder.stop()


if __name__ == "__main__":
    main()