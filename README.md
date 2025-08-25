# My Project Demo

python main.py --csv data/raw_data.csv --symbols BTCUSDT ETHUSDT --start 2024-01-01 --end 2025-08-22 --max-images 30
python train_classifier.py --report report.csv --out models/cup_handle_model.pkl
python main.py --csv data/raw_data.csv --symbols BTCUSDT ETHUSDT --start 2024-01-01 --end 2025-08-22 --max-images 30
python -m pytest -v
