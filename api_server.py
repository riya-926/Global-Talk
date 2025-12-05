from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import io
import numpy as np
import soundfile as sf
from typing import Optional

sys.path.append('backend')
from backend.stt_module import STTModule
from backend.translation_module import TranslationModule
from backend import config

app = FastAPI(title="Global Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config.validate_config()
stt = STTModule()
translator = TranslationModule()

class TranslateRequest(BaseModel):
    text: str
    source_lang: Optional[str] = None
    target_lang: str = "english"

@app.get("/")
async def root():
    return {"status": "online", "service": "Global Chat API"}

@app.post("/process")
async def process_audio(
    audio: UploadFile = File(...),
    target_lang: str = "english"
):
    try:
        audio_bytes = await audio.read()
        audio_data, sample_rate = sf.read(io.BytesIO(audio_bytes))
        
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)
        
        audio_data = audio_data.astype(np.float32)
        
        transcript, detected_lang = stt.transcribe_and_detect(audio_data, sample_rate)
        transcript = transcript.strip()
        
        translated = translator.translate(
            text=transcript,
            source_lang=detected_lang,
            target_lang=target_lang
        )
        
        return {
            "original": transcript,
            "translated": translated,
            "detected_language": detected_lang,
            "target_language": target_lang
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)