import os
import joblib
import pickle
import tensorflow as tf
import numpy as np
from gramformer import Gramformer
from deep_translator import GoogleTranslator
import whisper
from fastapi import UploadFile

# Paths
MODELS_DIR = "../models"

# Load models & tools (lazy load on first call)
_vectorizer = None
_lr_model = None
_knn_model = None
_tokenizer = None
_cnn_model = None
_whisper_model = None

def load_models():
    global _vectorizer, _lr_model, _knn_model, _tokenizer, _cnn_model, _whisper_model

    if _vectorizer is None:
        _vectorizer = joblib.load(os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib"))
        _lr_model = joblib.load(os.path.join(MODELS_DIR, "lr_emotion_model.joblib"))
        _knn_model = joblib.load(os.path.join(MODELS_DIR, "knn_emotion_model.joblib"))

    if _tokenizer is None:
        with open(os.path.join(MODELS_DIR, "tokenizer.pkl"), 'rb') as f:
            _tokenizer = pickle.load(f)
        _cnn_model = tf.keras.models.load_model(os.path.join(MODELS_DIR, "cnn_emotion_model.h5"))

    

    if _whisper_model is None:
        _whisper_model = whisper.load_model("base")  # or "small" if you want better accuracy

label_map = {0: "sadness", 1: "joy", 2: "love", 3: "anger", 4: "fear", 5: "surprise"}

def predict_emotion(text: str, model_type: str = "cnn") -> dict:
    load_models()

    cleaned = clean_text(text)  # reuse from earlier

    if model_type == "lr":
        vec = _vectorizer.transform([cleaned])
        pred = _lr_model.predict(vec)[0]
    elif model_type == "knn":
        vec = _vectorizer.transform([cleaned])
        pred = _knn_model.predict(vec)[0]
    else:  # cnn default
        seq = _tokenizer.texts_to_sequences([cleaned])
        padded = tf.keras.preprocessing.sequence.pad_sequences(seq, maxlen=100, padding='post')
        pred_prob = _cnn_model.predict(padded)
        pred = np.argmax(pred_prob, axis=1)[0]

    emotion = label_map.get(int(pred), "unknown")
    return {"emotion": emotion, "cleaned_text": cleaned}

_gf = None  # global for lazy load

def correct_grammar(text: str) -> str:
    global _gf
    if _gf is None:
        _gf = Gramformer(models=1)  # 1 = correcter model (most accurate)

    try:
        corrections = _gf.correct(text, max_candidates=1)
        if corrections:
            return corrections[0]
        else:
            return text
    except Exception as e:
        print(f"Gramformer error: {e}")
        return text  # fallback to original

def translate_text(text: str, target_lang: str = "ta") -> str:  # ta = Tamil, hi = Hindi, etc.
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except:
        return text  # fallback

def transcribe_and_analyze(audio_file: UploadFile, model_type: str = "cnn") -> dict:
    load_models()

    # Save temp file
    temp_path = f"temp_{audio_file.filename}"
    with open(temp_path, "wb") as f:
        f.write(audio_file.file.read())

    # Transcribe
    result = _whisper_model.transcribe(temp_path)
    text = result["text"]

    os.remove(temp_path)  # clean up

    emotion_result = predict_emotion(text, model_type)
    corrected = correct_grammar(text)
    translated_ta = translate_text(corrected, "ta")
    translated_hi = translate_text(corrected, "hi")

    return {
        "transcribed_text": text,
        "emotion": emotion_result["emotion"],
        "cleaned_text": emotion_result["cleaned_text"],
        "grammar_corrected": corrected,
        "translated_tamil": translated_ta,
        "translated_hindi": translated_hi
    }

# Reuse clean_text from prepare script (copy it here or import if modularized)
import re
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text