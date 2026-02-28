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

# CORS - allow React frontend (update origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Change to ["https://your-vercel-domain.vercel.app"] later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response model for /predict
class EmotionResponse(BaseModel):
    emotion: str
    confidence: float
    model_used: str

# Response model for /transcribe
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
        traceback.print_exc()  # ← prints full stack trace to console
        raise HTTPException(status_code=500, detail=f"Emotion prediction failed: {str(e)}")

# Same for /transcribe
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
        traceback.print_exc()  # ← critical line
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
# For deployment: do NOT run uvicorn here
# Render / Railway / Docker will run: uvicorn main:app --host 0.0.0.0 --port $PORT