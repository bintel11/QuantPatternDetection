import argparse
import pandas as pd
from utils.pattern_classifier import PatternClassifier

def main():
    parser = argparse.ArgumentParser(description="Train Cup & Handle ML Classifier")
    parser.add_argument("--report", type=str, required=True, help="Path to report.csv")
    parser.add_argument("--out", type=str, default="models/cup_handle_model.pkl", help="Output model file")
    args = parser.parse_args()

    # -------------------------------
    # Step 1: Load dataset
    # -------------------------------
    df = pd.read_csv(args.report)

    if "valid" not in df.columns:
        raise ValueError("❌ 'valid' column not found in report.csv. Please run main.py first.")

    # -------------------------------
    # Step 2: Check class balance
    # -------------------------------
    class_counts = df["valid"].value_counts(dropna=False).to_dict()
    print("📊 Class distribution:", class_counts)

    if class_counts.get(True, 0) < 5 or class_counts.get(False, 0) < 5:
        print("⚠️ Warning: Extremely imbalanced dataset (too few Valid/Invalid samples).")
        print("👉 Consider generating more patterns with main.py before training.")
        # Exit early to avoid training on bad data
        return

    # -------------------------------
    # Step 3: Train + Save Model
    # -------------------------------
    clf = PatternClassifier(model_path=args.out)
    clf.train(df)  # trains and saves automatically

if __name__ == "__main__":
    main()
