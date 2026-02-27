from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pipeline.inference import predict_emotion, transcribe_and_analyze

app = FastAPI(title="Echoflow API")

# Allow frontend (React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your Vercel URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Echoflow Backend is running!"}

@app.post("/predict")
def predict(text: str = Form(...), model: str = Form("cnn")):
    result = predict_emotion(text, model)
    return result

@app.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    model: str = Form("cnn")
):
    result = transcribe_and_analyze(audio, model)
    return result