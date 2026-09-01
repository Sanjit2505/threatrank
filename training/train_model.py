import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# Define Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(os.path.dirname(BASE_DIR), "unified_security_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "backend", "models", "cyber_model.pkl")

print(f"Loading dataset from {DATASET_PATH}...")

# Load dataset (we'll only load necessary columns to save memory)
FEATURES = [
    "duration",
    "src_bytes",
    "dst_bytes",
    "failed_logins",
    "login_attempts",
    "src_pkts",
    "dst_pkts",
]
TARGET = "attack_type"

df = pd.read_csv(DATASET_PATH, usecols=FEATURES + [TARGET])

# Drop rows with missing values
df.dropna(inplace=True)

X = df[FEATURES]
y = df[TARGET]

print(f"Dataset loaded. Total rows: {len(df)}")
print("Class distribution:")
print(y.value_counts())

print("Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Random Forest Classifier...")
model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

print("Evaluating model...")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

print(f"Saving model to {MODEL_PATH}...")
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("Training complete!")
