from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import threading
import time

# Import backend modules
from backend.audio_manager import AudioManager
from backend.stt_wrapper import transcribe_audio
from backend.translation_wrapper import translate_text
from backend import config

# Validate configuration on startup
config.validate_config()

app = FastAPI(title="Global Chat API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
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

class StartRecordingRequest(BaseModel):
    target_language: str

def process_audio_loop():
    """Background thread that processes audio chunks"""
    global messages, is_recording, target_language

    print("🔄 Processing loop started...")

    while is_recording:
        # Get latest audio file
        latest_file = audio_manager.get_latest_recording()

        if latest_file and os.path.exists(latest_file):
            try:
                print(f"📄 Processing: {latest_file.name}")

                # Transcribe audio
                transcription = transcribe_audio(str(latest_file))

                if transcription and transcription['text'].strip():
                    print(f"🎤 Detected ({transcription['language']}): {transcription['text'][:50]}...")

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
                    print(f"✅ Translated: {translation['translated_text'][:50]}...")

                # Clean up old file
                try:
                    os.remove(latest_file)
                except:
                    pass

            except Exception as e:
                print(f"❌ Error processing audio: {e}")

        time.sleep(0.5)  # Check every 0.5 seconds

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Global Chat API is running! 🌍",
        "version": "1.0.0"
    }

@app.post("/start-recording")
async def start_recording(request: StartRecordingRequest):
    global audio_manager, is_recording, messages, recording_thread, target_language

    try:
        target_language = request.target_language
        messages = []  # Clear previous messages

        print(f"\n🎬 Starting new recording session...")
        print(f"   Target language: {target_language}")

        # Initialize audio manager
        audio_manager = AudioManager()
        audio_manager.start_recording()

        # Start processing thread
        is_recording = True
        recording_thread = threading.Thread(target=process_audio_loop, daemon=True)
        recording_thread.start()

        print("🎤 Recording started successfully!")
        return {
            "status": "recording_started",
            "target_language": target_language
        }

    except Exception as e:
        print(f"❌ Error starting recording: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.post("/stop-recording")
async def stop_recording():
    global audio_manager, is_recording, recording_thread

    try:
        print("\n⏹️ Stopping recording...")
        is_recording = False

        if audio_manager:
            audio_manager.stop_recording()

        if recording_thread:
            recording_thread.join(timeout=3)

        print(f"✅ Recording stopped! Total messages: {len(messages)}")
        return {
            "status": "recording_stopped",
            "message_count": len(messages)
        }

    except Exception as e:
        print(f"❌ Error stopping recording: {e}")
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

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Global Chat API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)