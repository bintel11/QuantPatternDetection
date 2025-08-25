import os
import pandas as pd
import joblib  # still used for saving/loading models
from pattern_detector import CupHandleDetector
from plot_utils import save_pattern_plot, save_pattern_html
from utils.pattern_classifier import PatternClassifier  # ✅ fixed import
import config


def main():
    # -------------------------------
    # Step 1: Clear old report + assets
    # -------------------------------
    open(config.REPORT_FILE, "w").close()
    print("Cleared content of report.csv")

    for f in os.listdir(config.PATTERNS_DIR):
        if f.endswith(".png") or f.endswith(".html"):
            os.remove(os.path.join(config.PATTERNS_DIR, f))
    print("Cleared old PNG/HTMLs in patterns")

    # -------------------------------
    # Step 2: Preprocess raw data
    # -------------------------------
    df = pd.read_csv("data/raw_data.csv", parse_dates=["timestamp"])
    df.to_csv(config.PREPROCESSED_FILE, index=False)
    print(f"Preprocessed data saved to {config.PREPROCESSED_FILE}")

    symbols = ["BTCUSDT", "ETHUSDT"]
    max_images = 30

    # -------------------------------
    # Step 3: Load ML model if exists
    # -------------------------------
    model_path = os.path.join("models", "cup_handle_model.pkl")
    classifier = None
    if os.path.exists(model_path):
        classifier = PatternClassifier(model_path)
        classifier.load()
        print(f"✅ Loaded ML model from {model_path}")
    else:
        print("⚠️ No ML model found, skipping ML classification.")

    # -------------------------------
    # Step 4: Detect patterns
    # -------------------------------
    pattern_counter = 0
    report_rows = []

    for symbol in symbols:
        df_symbol = df[df["symbol"] == symbol].reset_index(drop=True)
        detector = CupHandleDetector(df_symbol)
        patterns = detector.find_patterns(max_images=max_images)

        valid_count = sum(1 for p in patterns if p["valid"])
        print(f"Detected {valid_count} valid cup & handle patterns for {symbol}.")

        for pat in patterns:
            df_slice = df_symbol.loc[pat["cup_start"]:pat["handle_end"]]
            pat["df"] = df_slice

            # -------------------------------
            # Step 4a: Save visual assets (PNG + HTML)
            # -------------------------------
            try:
                png_path = save_pattern_plot(pat, symbol, pattern_id=pattern_counter)
                html_path = save_pattern_html(pat, symbol, pattern_id=pattern_counter)
            except Exception as e:
                print(f"Failed to save assets for pattern {pattern_counter}: {e}")
                png_path, html_path = None, None

            # -------------------------------
            # Step 4b: ML classification
            # -------------------------------
            if classifier:
                ml_valid, confidence = classifier.predict(pat)
            else:
                ml_valid, confidence = None, None

            # -------------------------------
            # Step 4c: Save metadata to report
            # -------------------------------
            report_rows.append({
                "symbol": symbol,
                "cup_start": pat["cup_start"],
                "cup_end": pat["cup_end"],
                "handle_start": pat["handle_start"],
                "handle_end": pat["handle_end"],
                "cup_depth": pat["cup_depth"],
                "cup_duration": pat["cup_duration"],
                "handle_depth": pat["handle_depth"],
                "handle_duration": pat["handle_duration"],
                "breakout": pat["breakout"],
                "valid": pat["valid"],                   # rule-based valid
                "invalid_reason": pat["invalid_reason"], # rule-based reason
                "r2": pat["r2"],
                "ml_valid": ml_valid,                    # ML classification
                "confidence": confidence,                # ML confidence
                "png_file": png_path,
                "html_file": html_path
            })
            pattern_counter += 1

    # -------------------------------
    # Step 5: Save final report
    # -------------------------------
    if report_rows:
        pd.DataFrame(report_rows).to_csv(config.REPORT_FILE, index=False)
        print(f"Report saved to {config.REPORT_FILE} ({len(report_rows)} rows)")
    else:
        print("No patterns detected, report not generated.")


if __name__ == "__main__":
    main()


