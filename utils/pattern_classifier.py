# utils/pattern_classifier.py

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Optional oversampling
try:
    from imblearn.over_sampling import RandomOverSampler
    IMBLEARN_AVAILABLE = True
except ImportError:
    IMBLEARN_AVAILABLE = False

MODEL_DIR = "models"
MODEL_FILE = os.path.join(MODEL_DIR, "cup_handle_model.pkl")

class PatternClassifier:
    def __init__(self, model_path: str = MODEL_FILE):
        self.model_path = model_path
        self.model = None

    def train(self, df: pd.DataFrame):
        """
        Train the classifier using features from report.csv.
        Automatically balances classes if imbalanced.
        """
        features = ["cup_depth", "cup_duration", "handle_depth", "handle_duration", "r2"]
        target = "valid"

        X = df[features].fillna(0).values
        y = df[target].astype(int).values  # convert True/False → 1/0

        # Handle class imbalance with oversampling
        if IMBLEARN_AVAILABLE:
            print("⚖️ Applying RandomOverSampler to balance classes...")
            ros = RandomOverSampler(random_state=42)
            X, y = ros.fit_resample(X, y)
        else:
            print("⚠️ imbalanced-learn not installed. Training on raw data.")

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        clf = RandomForestClassifier(
            n_estimators=200, random_state=42, class_weight="balanced"
        )
        clf.fit(X_train, y_train)

        # Evaluate
        y_pred = clf.predict(X_test)
        print("📊 Classification Report:")
        print(classification_report(y_test, y_pred, target_names=["Invalid", "Valid"]))

        # Save model
        os.makedirs(MODEL_DIR, exist_ok=True)
        joblib.dump(clf, self.model_path)
        print(f"✅ Model saved to {self.model_path}")

        self.model = clf

    def load(self):
        """Load trained model from disk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at {self.model_path}. Please train first.")
        self.model = joblib.load(self.model_path)
        return self.model

    def predict(self, pattern: dict) -> tuple:
        """
        Predict validity of a single pattern.
        Returns: (prediction: bool, confidence: float)
        """
        if self.model is None:
            self.load()

        features = np.array([[ 
            pattern.get("cup_depth", 0),
            pattern.get("cup_duration", 0),
            pattern.get("handle_depth", 0),
            pattern.get("handle_duration", 0),
            pattern.get("r2", 0)
        ]])

        probs = self.model.predict_proba(features)[0]
        pred = self.model.predict(features)[0]
        confidence = probs[pred]
        return bool(pred), float(confidence)
