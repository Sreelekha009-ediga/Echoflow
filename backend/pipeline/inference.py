import os
import joblib
import pickle
import tensorflow as tf
import numpy as np
from gramformer import Gramformer
from deep_translator import GoogleTranslator
import whisper
from fastapi import UploadFile
import re
import traceback  # for better debugging

# Paths - make absolute for robustness
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # backend/
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Lazy load
_vectorizer = None
_lr_model = None
_knn_model = None
_tokenizer = None
_cnn_model = None
_whisper_model = None
_gf = None

def load_models():
    global _vectorizer, _lr_model, _knn_model, _tokenizer, _cnn_model, _whisper_model
    try:
        if _vectorizer is None:
            _vectorizer = joblib.load(os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib"))
            _lr_model = joblib.load(os.path.join(MODELS_DIR, "lr_emotion_model.joblib"))
            _knn_model = joblib.load(os.path.join(MODELS_DIR, "knn_emotion_model.joblib"))

        if _tokenizer is None:
            with open(os.path.join(MODELS_DIR, "tokenizer.pkl"), 'rb') as f:
                _tokenizer = pickle.load(f)
            _cnn_model = tf.keras.models.load_model(os.path.join(MODELS_DIR, "cnn_emotion_model.h5"))

        if _whisper_model is None:
            _whisper_model = whisper.load_model("tiny")  # Smaller for Render; change to "base" if more accuracy needed
    except Exception as e:
        traceback.print_exc()
        raise RuntimeError(f"Model loading failed: {str(e)}")

label_map = {0: "sadness", 1: "joy", 2: "love", 3: "anger", 4: "fear", 5: "surprise"}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def predict_emotion(text: str, model_type: str = "cnn") -> dict:
    load_models()
    cleaned = clean_text(text)

    if model_type == "lr":
        vec = _vectorizer.transform([cleaned])
        pred = _lr_model.predict(vec)[0]
        conf = float(_lr_model.predict_proba(vec)[0].max())
    elif model_type == "knn":
        vec = _vectorizer.transform([cleaned])
        pred = _knn_model.predict(vec)[0]
        conf = float(_knn_model.predict_proba(vec)[0].max())
    else:  # cnn
        seq = _tokenizer.texts_to_sequences([cleaned])
        padded = tf.keras.preprocessing.sequence.pad_sequences(seq, maxlen=100, padding='post')
        pred_prob = _cnn_model.predict(padded)
        pred = np.argmax(pred_prob, axis=1)[0]
        conf = float(np.max(pred_prob))

    emotion = label_map.get(int(pred), "unknown")
    return {"emotion": emotion, "confidence": conf, "cleaned_text": cleaned}

def correct_grammar(text: str) -> str:
    global _gf
    try:
        if _gf is None:
            _gf = Gramformer(models=1)
        corrections = _gf.correct(text, max_candidates=1)
        return list(corrections)[0] if corrections else text
    except Exception as e:
        print(f"Gramformer failed: {str(e)} - returning original")
        return text

def translate_text(text: str, target_lang: str = "ta") -> str:
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation failed: {str(e)}")
        return text

def transcribe_and_analyze(audio_file: UploadFile, model_type: str = "cnn") -> dict:
    load_models()

    temp_path = f"temp_{audio_file.filename}"
    with open(temp_path, "wb") as f:
        f.write(audio_file.file.read())

    try:
        result = _whisper_model.transcribe(temp_path)
        text = result["text"]
    except Exception as e:
        raise RuntimeError(f"Whisper transcription failed: {str(e)} - Ensure ffmpeg is installed and in PATH.")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    emotion_result = predict_emotion(text, model_type)
    corrected = correct_grammar(text)
    translated_ta = translate_text(corrected, "ta")
    translated_hi = translate_text(corrected, "hi")

    return {
        "transcribed_text": text,
        "emotion": emotion_result["emotion"],
        "confidence": emotion_result["confidence"],
        "corrected_text": corrected,
        "translated_text": f"Tamil: {translated_ta}\nHindi: {translated_hi}",  # Combined for simplicity
        "cleaned_text": emotion_result["cleaned_text"]
    }