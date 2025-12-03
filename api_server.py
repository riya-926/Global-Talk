# api_server.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

# allow your React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # fine for testing
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslationResult(BaseModel):
    original: str
    translated: str
    detected_language: str
    target_language: str

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/process", response_model=TranslationResult)
async def process_audio(
    audio: UploadFile = File(...),
    target_lang: str = "english"
):
    data = await audio.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty audio")

    # ❗ For now we IGNORE real STT and GPT.
    # We just prove the connection works.
    original = f"Received {len(data)} bytes of audio."
    translated = f"[FAKE {target_lang.upper()}] " + original

    return TranslationResult(
        original=original,
        translated=translated,
        detected_language="unknown",
        target_language=target_lang,
    )
