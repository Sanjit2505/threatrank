import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "cyber_model.pkl")

# Load model globally so it's ready for fast inference
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None
    print(f"Warning: Model not found at {MODEL_PATH}")

def predict_threat(features: dict):
    """
    Given a dictionary of features, predict the attack type and confidence.
    """
    if not model:
        return "Unknown", 0.0

    # Ensure features match the training order
    feature_order = [
        "duration",
        "src_bytes",
        "dst_bytes",
        "failed_logins",
        "login_attempts",
        "src_pkts",
        "dst_pkts",
    ]
    
    # Create DataFrame for prediction to retain feature names (avoids sklearn warning)
    df_features = pd.DataFrame([features], columns=feature_order)
    
    attack_type = model.predict(df_features)[0]
    
    # Get probabilities
    probs = model.predict_proba(df_features)[0]
    # The confidence is the maximum probability
    confidence = max(probs) * 100
    
    return attack_type, confidence
