from pathlib import Path
import numpy as np
import joblib

ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "model.joblib"

_model = None

def load_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. Train it first: python manage.py train_model"
            )
        _model = joblib.load(MODEL_PATH)
    return _model

def build_features(payload: dict) -> np.ndarray:
    x = np.array([[
        float(payload["quiz_score"]),
        float(payload["topic_accuracy"]),
        int(payload["attempts"]),
        int(payload["time_spent_sec"]),
    ]], dtype=float)
    return x

def predict_band(payload: dict) -> dict:
    model = load_model()
    x = build_features(payload)
    pred = model.predict(x)[0]
    proba = None
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(x)[0]
        classes = list(model.classes_)
        proba = {classes[i]: float(probs[i]) for i in range(len(classes))}
    return {"band": str(pred), "probabilities": proba}