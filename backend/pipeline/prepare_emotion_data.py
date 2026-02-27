import os
from datasets import load_dataset
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Paths
DATA_DIR = "../data"
MODELS_DIR = "../models"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

def clean_text(text):
    """Basic cleaning: lowercase, remove URLs, mentions, extra spaces"""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # remove URLs
    text = re.sub(r'@\w+', '', text)  # remove mentions
    text = re.sub(r'#', '', text)     # remove hashtags symbol
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("Loading dair-ai/emotion dataset...")
dataset = load_dataset("dair-ai/emotion", split="train")  # ~16k samples

df = pd.DataFrame(dataset)
print("Dataset shape:", df.shape)
print("Emotion class distribution:\n", df['label'].value_counts())

# Map labels to names (for readability)
label_map = {0: "sadness", 1: "joy", 2: "love", 3: "anger", 4: "fear", 5: "surprise"}
df['emotion'] = df['label'].map(label_map)

# Clean text
print("Cleaning text...")
df['clean_text'] = df['text'].apply(clean_text)

# Save raw + cleaned
df.to_csv(os.path.join(DATA_DIR, "emotion_cleaned.csv"), index=False)
print("Saved cleaned data to data/emotion_cleaned.csv")

# TF-IDF Vectorization
print("Creating TF-IDF features...")
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2), stop_words='english')
X = vectorizer.fit_transform(df['clean_text'])
y = df['label']

# Save vectorizer
joblib.dump(vectorizer, os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib"))
print("Saved TF-IDF vectorizer")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Model 1: Logistic Regression
print("Training Logistic Regression...")
lr = LogisticRegression(max_iter=1000, multi_class='multinomial', solver='lbfgs')
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
print("LR Accuracy:", accuracy_score(y_test, y_pred_lr))
print("LR Classification Report:\n", classification_report(y_test, y_pred_lr, target_names=label_map.values()))

joblib.dump(lr, os.path.join(MODELS_DIR, "lr_emotion_model.joblib"))

# Model 2: KNN
print("Training KNN...")
knn = KNeighborsClassifier(n_neighbors=5, metric='cosine')  # cosine good for TF-IDF
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)
print("KNN Accuracy:", accuracy_score(y_test, y_pred_knn))
print("KNN Classification Report:\n", classification_report(y_test, y_pred_knn, target_names=label_map.values()))

joblib.dump(knn, os.path.join(MODELS_DIR, "knn_emotion_model.joblib"))

print("\nStep 3 complete! Models and vectorizer saved in backend/models/")
print("Data saved in backend/data/")