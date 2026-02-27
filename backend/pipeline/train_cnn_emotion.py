import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelBinarizer
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import joblib
import pickle

# Paths (same as before)
DATA_DIR = "../data"
MODELS_DIR = "../models"
os.makedirs(MODELS_DIR, exist_ok=True)

# Load cleaned data from Step 3
df = pd.read_csv(os.path.join(DATA_DIR, "emotion_cleaned.csv"))

texts = df['clean_text'].values
labels = df['label'].values

# Parameters
MAX_WORDS = 10000
MAX_LEN = 100
EMBEDDING_DIM = 100
BATCH_SIZE = 32
EPOCHS = 10

# Tokenization
print("Tokenizing text...")
tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded = pad_sequences(sequences, maxlen=MAX_LEN, padding='post', truncating='post')

# Save tokenizer
with open(os.path.join(MODELS_DIR, "tokenizer.pkl"), 'wb') as f:
    pickle.dump(tokenizer, f)
print("Tokenizer saved")

# Labels to one-hot
lb = LabelBinarizer()
y = lb.fit_transform(labels)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    padded, y, test_size=0.2, random_state=42, stratify=labels
)

# Build CNN model
print("Building CNN model...")
model = Sequential([
    Embedding(MAX_WORDS, EMBEDDING_DIM, input_length=MAX_LEN),
    Conv1D(128, 5, activation='relu'),
    GlobalMaxPooling1D(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(6, activation='softmax')  # 6 emotions
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Train
print("Training CNN...")
history = model.fit(
    X_train, y_train,
    validation_split=0.1,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    verbose=1
)

# Evaluate
print("Evaluating CNN...")
y_pred_prob = model.predict(X_test)
y_pred = np.argmax(y_pred_prob, axis=1)
y_true = np.argmax(y_test, axis=1)

acc = accuracy_score(y_true, y_pred)
print(f"CNN Accuracy: {acc:.4f}")
print("CNN Classification Report:")
print(classification_report(y_true, y_pred, target_names=["sadness", "joy", "love", "anger", "fear", "surprise"]))

# Save model
model.save(os.path.join(MODELS_DIR, "cnn_emotion_model.h5"))
print("CNN model saved as cnn_emotion_model.h5")

# Optional: Compare with previous models (load them and predict on same test set)
# For full comparison you can add code here later if you want

print("\nCNN trained and saved.")