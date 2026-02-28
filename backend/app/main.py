from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from pipeline.inference import predict_emotion, transcribe_and_analyze
import os
import traceback

app = FastAPI(
    title="Echoflow API",
    description="Speech-to-Text + Emotion Detection + Grammar Correction",
    version="1.0.0"
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmotionResponse(BaseModel):
    emotion: str
    confidence: float
    model_used: str

class TranscriptionResponse(BaseModel):
    transcribed_text: str
    emotion: str
    confidence: float
    corrected_text: Optional[str] = None
    translated_text: Optional[str] = None
    model_used: str

@app.get("/")
async def root():
    return {"message": "Echoflow Backend is running! 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/predict", response_model=EmotionResponse)
async def predict(
    text: str = Form(...),
    model: str = Form("cnn")
):
    try:
        result = predict_emotion(text, model)
        return {
            "emotion": result["emotion"],
            "confidence": result["confidence"],
            "model_used": model
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Emotion prediction failed: {str(e)}")

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(
    audio: UploadFile = File(...),
    model: str = Form("cnn")
):
    if audio.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Audio file too large (max 10MB)")

    try:
        result = transcribe_and_analyze(audio, model)
        return TranscriptionResponse(
            transcribed_text=result["transcribed_text"],
            emotion=result["emotion"],
            confidence=result["confidence"],
            corrected_text=result.get("corrected_text"),
            translated_text=result.get("translated_text"),
            model_used=model
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

        