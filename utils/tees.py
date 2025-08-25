import ccxt
import pandas as pd
from datetime import datetime, timedelta

# Initialize Binance Futures
exchange = ccxt.binance({
    'options': {'defaultType': 'future'}
})

symbol = 'BTC/USDT'
timeframe = '1m'
start_date = '2024-01-01T00:00:00Z'
end_date = '2025-01-01T00:00:00Z'

since = exchange.parse8601(start_date)
until = exchange.parse8601(end_date)

all_ohlcv = []

print(f"Downloading {symbol} {timeframe} data from {start_date} to {end_date}...")

while since < until:
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit=1000)
    if not ohlcv:
        break
    all_ohlcv += ohlcv
    # Advance to next batch, avoid overlap
    since = ohlcv[-1][0] + 60_000  

# Create DataFrame
df = pd.DataFrame(all_ohlcv, columns=['timestamp','open','high','low','close','volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df['symbol'] = symbol.replace('/', '')

# Ensure data folder exists
import os
os.makedirs('data', exist_ok=True)

# Save CSV
df.to_csv('data/BTCUSDT_1m_2024.csv', index=False)
print(f"✅ Saved {len(df)} rows to data/BTCUSDT_1m_2024.csv")
