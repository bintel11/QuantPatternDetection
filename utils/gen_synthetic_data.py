# gen_synthetic_data_fast.py
import pandas as pd
import numpy as np
import os
import shutil
import re
from datetime import datetime, timedelta

# --- Backup old raw_data.csv ---
def backup_existing_file(file_path):
    if os.path.exists(file_path):
        last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
        timestamp = last_modified.strftime("%Y%m%d_%H%M%S")
        existing_backups = [f for f in os.listdir("data") if re.match(r"raw_data_\d+_\d+\.csv", f)]
        next_num = max([int(re.search(r"raw_data_(\d+)_", f).group(1)) for f in existing_backups], default=0) + 1
        backup_name = f"data/raw_data_{next_num:02d}_{timestamp}.csv"
        shutil.copy(file_path, backup_name)
        print(f"📦 Backup created: {backup_name}")

# --- Synthetic Cup & Handle Generator ---
def generate_cup_handle(start_price=50000, cup_len=50, handle_len=15, depth=200):
    """Generate OHLCV numpy arrays for one Cup & Handle pattern."""
    t_cup = np.linspace(-1, 1, cup_len)
    cup_curve = depth * (t_cup**2)  # parabolic U-shape
    cup_close = start_price - depth + cup_curve
    # Handle: small retracement
    handle_close = cup_close[-1] - np.linspace(0, 0.4*depth, handle_len)
    # Concatenate cup + handle
    close = np.concatenate([cup_close, handle_close])
    open_ = close + np.random.uniform(-5, 5, len(close))
    high = np.maximum(open_, close) + np.random.uniform(0, 5, len(close))
    low = np.minimum(open_, close) - np.random.uniform(0, 5, len(close))
    volume = np.random.randint(100, 500, len(close))
    return open_, high, low, close, volume

# --- Main Fast Generator ---
def generate_synthetic_data(symbols=["BTCUSDT","ETHUSDT"], total_patterns=30, base_price={"BTCUSDT":50000, "ETHUSDT":4000}):
    data = []
    start_datetime = datetime(2024,1,1)
    dt = timedelta(minutes=1)
    for symbol in symbols:
        timestamps = []
        open_, high, low, close, volume = [], [], [], [], []
        current_time = start_datetime
        patterns_added = 0
        while patterns_added < total_patterns:
            # Random gap before pattern
            gap = np.random.randint(5, 20)
            for _ in range(gap):
                timestamps.append(current_time)
                price = base_price[symbol] + np.random.uniform(-50, 50)
                open_.append(price)
                close.append(price + np.random.uniform(-5,5))
                high.append(max(open_[-1], close[-1]) + np.random.uniform(0,5))
                low.append(min(open_[-1], close[-1]) - np.random.uniform(0,5))
                volume.append(np.random.randint(50,200))
                current_time += dt
            # Generate one pattern
            o,h,l,c,v = generate_cup_handle(start_price=base_price[symbol])
            n = len(c)
            for i in range(n):
                timestamps.append(current_time)
                open_.append(o[i])
                high.append(h[i])
                low.append(l[i])
                close.append(c[i])
                volume.append(v[i])
                current_time += dt
            patterns_added += 1
        # Convert to DataFrame
        df_symbol = pd.DataFrame({
            "timestamp": timestamps,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
            "symbol": symbol
        })
        data.append(df_symbol)
    full_df = pd.concat(data, ignore_index=True)
    return full_df

# --- Save CSV ---
os.makedirs("data", exist_ok=True)
raw_file = "data/raw_data.csv"
backup_existing_file(raw_file)

df = generate_synthetic_data()
df.to_csv(raw_file, index=False)
print(f"✅ Synthetic dataset generated and saved to {raw_file} ({len(df)} rows)")
