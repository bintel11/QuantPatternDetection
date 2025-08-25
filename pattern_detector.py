import pandas as pd
import numpy as np
from sklearn.metrics import r2_score

class CupHandleDetector:
    def __init__(self, df: pd.DataFrame):
        self.df = df.reset_index(drop=True)

    def find_patterns(self, max_images=30):
        """
        Detect valid Cup & Handle patterns.

        Returns:
            List of dicts with keys:
            'cup_start', 'cup_end', 'handle_start', 'handle_end', 'breakout',
            'cup_depth', 'cup_duration', 'handle_depth', 'handle_duration',
            'valid', 'r2', 'invalid_reason'
        """
        patterns = []
        data_len = len(self.df)
        count = 0

        for i in range(0, data_len - 50):  # minimal 50 bars for a pattern
            cup_start = i
            cup_end = i + 30
            handle_start = cup_end + 1
            handle_end = handle_start + 10
            breakout_idx = handle_end + 1

            if handle_end >= data_len or count >= max_images:
                break

            cup_df = self.df.iloc[cup_start:cup_end + 1]
            handle_df = self.df.iloc[handle_start:handle_end + 1]

            breakout_price = self.df.iloc[breakout_idx]['high']

            is_valid, reason, r2_val, cup_depth, handle_depth = self._validate_cup_handle(
                cup_df, handle_df, breakout_price
            )

            patterns.append({
                "cup_start": cup_start,
                "cup_end": cup_end,
                "handle_start": handle_start,
                "handle_end": handle_end,
                "cup_depth": cup_depth,
                "cup_duration": len(cup_df),
                "handle_depth": handle_depth,
                "handle_duration": len(handle_df),
                "breakout": breakout_idx,
                "valid": is_valid,
                "invalid_reason": reason,
                "r2": r2_val
            })

            count += 1

        return patterns

    def _validate_cup_handle(self, cup_df, handle_df, breakout_price):
        try:
            # Cup depth
            avg_candle = (cup_df['high'] - cup_df['low']).mean()
            cup_depth = cup_df['high'].max() - cup_df['low'].min()
            if cup_depth < 2 * avg_candle:
                return False, "Cup depth too shallow", None, cup_depth, None

            # Handle depth
            rim = max(cup_df['high'].iloc[0], cup_df['high'].iloc[-1])
            handle_depth = rim - handle_df['low'].min()
            if handle_depth > 0.4 * cup_depth:
                return False, "Handle retrace too deep", None, cup_depth, handle_depth

            # Cup smoothness R^2
            x = np.arange(len(cup_df))
            y = cup_df['close'].values
            coeffs = np.polyfit(x, y, 2)
            y_fit = np.polyval(coeffs, x)
            r2_val = r2_score(y, y_fit)
            if r2_val < 0.85:
                return False, "Cup not parabolic enough (R^2 too low)", r2_val, cup_depth, handle_depth

            # Breakout check (ATR optional)
            cup_full = pd.concat([cup_df, handle_df])
            high_low = cup_full['high'] - cup_full['low']
            high_close = (cup_full['high'] - cup_full['close'].shift()).abs()
            low_close = (cup_full['low'] - cup_full['close'].shift()).abs()
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr14 = tr.rolling(14, min_periods=1).mean().iloc[-1]

            if breakout_price < handle_df['high'].max() + 1.5 * atr14:
                return False, "Breakout too low", r2_val, cup_depth, handle_depth

            return True, "", r2_val, cup_depth, handle_depth
        except Exception as e:
            return False, str(e), None, None, None





