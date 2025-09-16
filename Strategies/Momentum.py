import pandas as pd
import numpy as np

class Momentum:
    """
    Momentum strategy: Fast vs Slow SMA crossover
    - get_signal_series(prices): vector of +1 (long), -1 (short), 0 (flat)
    - get_signal(prices): latest scalar signal
    """
    def __init__(self, fast_window=20, slow_window=50):
        assert 0 < fast_window < slow_window
        self.fast_window = fast_window
        self.slow_window = slow_window

    def get_signal_series(self, closes: pd.Series) -> pd.Series:
        fast_sma = closes.rolling(self.fast_window, min_periods=self.fast_window).mean()
        slow_sma = closes.rolling(self.slow_window, min_periods=self.slow_window).mean()

        #compares fast vs slow
        signals = np.where(fast_sma > slow_sma, 1,
                  np.where(fast_sma < slow_sma, -1, 0))

        return pd.Series(signals, index=closes.index, dtype="int64")

    def get_signal(self, closes: pd.Series) -> int:
        if len(closes) < self.slow_window:
            return 0  # not enough data yet
        return int(self.get_signal_series(closes).iloc[-1])
