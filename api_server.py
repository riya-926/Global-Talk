from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import threading
import time
from typing import Optional

# Import backend modules
from backend.audio_manager import AudioManager
from backend.stt_wrapper import transcribe_audio
from backend.translation_wrapper import translate_text
from backend.vad_module import EnhancedVAD
from backend import config
import numpy as np
import wave

# Validate configuration on startup
config.validate_config()

app = FastAPI(title="Global Chat API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],  # Vite ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
audio_manager = None
is_recording = False
messages = []
recording_thread = None
target_language = "en"
vad = EnhancedVAD()  # Initialize VAD for meeting noise filtering

class StartRecordingRequest(BaseModel):
    target_language: str

def process_audio_loop():
    """Background thread that processes audio chunks"""
    global messages, is_recording, target_language

    print("Processing loop started...")

    while is_recording:
        # Get latest audio file
        latest_file = audio_manager.get_latest_recording()

        if latest_file and os.path.exists(latest_file):
            try:
                print(f"Processing: {latest_file.name}")

                # Load audio file and check for voice activity BEFORE transcription
                audio_data = _load_audio_file(str(latest_file))
                
                if audio_data is not None:
                    # Check VAD - skip if no voice activity (filters background noise)
                    if not vad.has_voice_activity(audio_data, config.AUDIO_SAMPLE_RATE):
                        print("Skipping chunk - no voice activity detected (background noise filtered)")
                        try:
                            os.remove(latest_file)
                        except:
                            pass
                        continue

                # Transcribe audio (only if VAD passed)
                transcription = transcribe_audio(str(latest_file))

                if transcription and transcription['text'].strip():
                    print(f"Detected ({transcription['language']}): {transcription['text'][:50]}...")

                    # Translate
                    translation = translate_text(
                        transcription['text'],
                        target_language,
                        transcription['language']
                    )

                    # Create message
                    message = {
                        "originalText": transcription['text'],
                        "translatedText": translation['translated_text'],
                        "detectedLanguage": transcription['language'].upper(),
                        "targetLanguage": target_language,
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
                    }

                    messages.append(message)
                    print(f"Translated: {translation['translated_text'][:50]}...")

                # Clean up old file
                try:
                    os.remove(latest_file)
                except:
                    pass

            except Exception as e:
                print(f"Error processing audio: {e}")

        time.sleep(0.5)  # Check every 0.5 seconds

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Global Chat API is running!",
        "version": "1.0.0"
    }

@app.post("/start-recording")
async def start_recording(request: StartRecordingRequest):
    global audio_manager, is_recording, messages, recording_thread, target_language

    try:
        target_language = request.target_language
        messages = []  # Clear previous messages

        print("\nStarting new recording session...")
        print(f"   Target language: {target_language}")

        # Initialize audio manager
        audio_manager = AudioManager()
        audio_manager.start_recording()

        # Start processing thread
        is_recording = True
        recording_thread = threading.Thread(target=process_audio_loop, daemon=True)
        recording_thread.start()

        print("Recording started successfully!")
        return {
            "status": "recording_started",
            "target_language": target_language
        }

    except Exception as e:
        print(f"Error starting recording: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.post("/stop-recording")
async def stop_recording():
    global audio_manager, is_recording, recording_thread

    try:
        print("\nStopping recording...")
        is_recording = False

        if audio_manager:
            audio_manager.stop_recording()

        if recording_thread:
            recording_thread.join(timeout=3)

        print(f"Recording stopped! Total messages: {len(messages)}")
        return {
            "status": "recording_stopped",
            "message_count": len(messages)
        }

    except Exception as e:
        print(f"Error stopping recording: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/messages")
async def get_messages():
    """Get all translation messages"""
    return messages

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "is_recording": is_recording,
        "message_count": len(messages),
        "target_language": target_language
    }

def _load_audio_file(file_path: str) -> Optional[np.ndarray]:
    """Load audio file and return as numpy array."""
    try:
        with wave.open(file_path, 'rb') as wf:
            frames = wf.getnframes()
            sample_rate = wf.getframerate()
            audio_bytes = wf.readframes(frames)
            
            # Convert bytes to numpy array
            audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
            # Normalize to float32 [-1, 1]
            audio_float = audio_array.astype(np.float32) / 32768.0
            
            return audio_float
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return None

if __name__ == "__main__":
    import uvicorn
    print("Starting Global Chat API...")
    print("Enhanced VAD enabled for meeting noise filtering")
    uvicorn.run(app, host="0.0.0.0", port=8000)