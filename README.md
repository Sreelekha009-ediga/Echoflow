# ECHOFLOW – Speech, NLP & Emotion Detection System

**AI-powered system that converts speech to text, detects human emotions, corrects grammar, and provides multilingual translation.**

GitHub: https://github.com/Sreelekha009-ediga/echoflow-speech-emotion

### Key Highlights (resume-ready bullet points)
- Developed an AI-driven system that converts speech to text and detects human emotions using Machine Learning and NLP techniques.
- Trained and evaluated multiple models including CNN, Logistic Regression, and KNN to classify emotional states from textual features.
- Implemented grammar correction (Gramformer) and language translation (Google Translate API) to enhance clarity and multilingual usability.
- Designed a modular ML pipeline covering preprocessing, feature extraction, model training, and inference.
- Built a full-stack application with FastAPI backend + React frontend (or local testing via Swagger).
- Tech Stack: Python, FastAPI, TensorFlow/Keras, Whisper (OpenAI), Gramformer, python-chess (wait – typo, remove if not used), react-mic (frontend), MUI.

### Project Structure
echoflow-speech-emotion/
├── backend/
│   ├── main.py               # FastAPI app (endpoints: /predict, /transcribe)
│   ├── requirements.txt
│   ├── pipeline/
│   │   └── inference.py      # Emotion prediction, STT, grammar, translation
│   └── models/               # Trained .h5, .joblib, tokenizer.pkl files
├── frontend/                 
│   ├── src/
│   └── package.json
├── README.md
└── .gitignore


### Features
- **Speech-to-Text**: Uses OpenAI Whisper (base model) for accurate transcription
- **Emotion Detection**: Multi-class classification (sadness, joy, love, anger, fear, surprise) with CNN / LR / KNN
- **Grammar Correction**: Powered by Gramformer (transformer-based)
- **Translation**: Google Translate (supports Tamil, Hindi, etc.)
- **API Endpoints**:
  - `POST /predict`: Text → Emotion + Confidence
  - `POST /transcribe`: Audio file → Transcription + Emotion + Grammar + Translation

### How to Run Locally

1. **Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/Scripts/activate   # Windows
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000

2. **Frontend**
   cd ../frontend
npm install
npm start