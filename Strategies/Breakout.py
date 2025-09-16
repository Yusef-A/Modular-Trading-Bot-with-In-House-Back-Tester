import pandas as pd
import numpy as np

class Breakout:
    def __init__(self, lookback=20):
        assert lookback > 0
        self.lookback = lookback

    def get_signal_series(self, ohlc: pd.DataFrame) -> pd.Series:
        """
        ohlc: DataFrame with columns ['High', 'Low', 'Close'] indexed by time.
        Returns a Series of signals: +1 (long breakout), -1 (short breakout), 0 (inside range).
        """
        highs  = ohlc["High"]
        lows   = ohlc["Low"]
        closes = ohlc["Close"]

        # Use ONLY prior bars to define the range (shift(1) prevents look-ahead)
        resistance = highs.shift(1).rolling(self.lookback, min_periods=self.lookback).max()
        support    = lows.shift(1).rolling(self.lookback, min_periods=self.lookback).min()

        signals = np.where(closes > resistance, 1,
                  np.where(closes < support,  -1, 0))
        return pd.Series(signals, index=ohlc.index, dtype="int64")

    def get_signal(self, ohlc: pd.DataFrame) -> int:
        # Need at least 'lookback' prior bars + the current bar => lookback + 1 rows
        if len(ohlc) < self.lookback + 1:
            return 0
        return int(self.get_signal_series(ohlc).iloc[-1])
