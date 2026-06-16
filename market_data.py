"""
MetaTrader 5 Market Data Integration
Fetches real-time forex data from MT5 terminal
"""
import MetaTrader5 as mt5
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class MarketData:
    """Handler for MT5 market data"""

    def __init__(self):
        """Initialize MT5 connection"""
        # Initialize MT5 connection
        if not mt5.initialize():
            raise ConnectionError(f"MT5 initialization failed: {mt5.last_error()}")

        print(f"✅ MT5 initialized successfully")

        # Get account info
        account_info = mt5.account_info()
        if account_info:
            print(f"✅ Connected to account: {account_info.login}")
            print(f"   Server: {account_info.server}")
            print(f"   Balance: ${account_info.balance:.2f}")

        self.cache = {}  # Simple cache to reduce unnecessary calls
        self.cache_duration = 5  # Cache data for 5 seconds only (MT5 is fast)

    def _get_cache_key(self, pair: str, timeframe: str) -> str:
        """Generate cache key"""
        return f"{pair}_{timeframe}"

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False

        cached_time, _ = self.cache[cache_key]
        return (datetime.now() - cached_time).total_seconds() < self.cache_duration

    def _convert_timeframe(self, timeframe: str) -> int:
        """Convert timeframe string to MT5 constant"""
        timeframe_map = {
            'M1': mt5.TIMEFRAME_M1,
            'M5': mt5.TIMEFRAME_M5,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'D1': mt5.TIMEFRAME_D1,
            'W1': mt5.TIMEFRAME_W1,
            'MN1': mt5.TIMEFRAME_MN1
        }
        return timeframe_map.get(timeframe, mt5.TIMEFRAME_M15)

    def get_candles(
        self,
        pair: str,
        timeframe: str = 'M15',
        count: int = 100
    ) -> Optional[pd.DataFrame]:
        """
        Fetch candlestick data from MT5

        Args:
            pair: Currency pair (e.g., 'EURUSD')
            timeframe: Timeframe ('M15', 'H1', 'H4')
            count: Number of candles to fetch

        Returns:
            DataFrame with OHLCV data or None if error
        """
        # Check cache first
        cache_key = self._get_cache_key(pair, timeframe)
        if self._is_cache_valid(cache_key):
            _, cached_df = self.cache[cache_key]
            return cached_df.copy()

        try:
            # Convert timeframe
            mt5_timeframe = self._convert_timeframe(timeframe)

            # Get rates from MT5
            rates = mt5.copy_rates_from_pos(pair, mt5_timeframe, 0, count)

            if rates is None or len(rates) == 0:
                print(f"❌ No data received for {pair} on {timeframe}")
                error = mt5.last_error()
                if error[0] != 1:  # 1 = success
                    print(f"   MT5 Error: {error}")
                return None

            # Convert to DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)

            # Rename columns to match expected format
            df.rename(columns={
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'tick_volume': 'volume'
            }, inplace=True)

            # Select only needed columns
            df = df[['open', 'high', 'low', 'close', 'volume']]

            # Cache the result
            self.cache[cache_key] = (datetime.now(), df.copy())

            return df

        except Exception as e:
            print(f"❌ Error fetching candles for {pair}: {e}")
            return None

    def get_current_price(self, pair: str) -> Optional[float]:
        """
        Get current price for a pair

        Args:
            pair: Currency pair

        Returns:
            Current price or None if error
        """
        try:
            # Get current tick
            tick = mt5.symbol_info_tick(pair)

            if tick is None:
                print(f"❌ Error fetching current price for {pair}")
                return None

            # Return bid price (or average of bid/ask)
            return (tick.bid + tick.ask) / 2

        except Exception as e:
            print(f"❌ Error fetching current price for {pair}: {e}")
            return None

    def get_multiple_timeframes(
        self,
        pair: str,
        timeframes: List[str] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple timeframes

        Args:
            pair: Currency pair
            timeframes: List of timeframes (default: ['M15', 'H1', 'H4'])

        Returns:
            Dictionary mapping timeframe to DataFrame
        """
        if timeframes is None:
            timeframes = ['M15', 'H1', 'H4']

        data = {}

        # No need for delay with MT5 - it's local and fast
        for tf in timeframes:
            df = self.get_candles(pair, tf, count=100)
            if df is not None:
                data[tf] = df

        return data

    def calculate_atr(self, df: pd.DataFrame, period: int = 14) -> float:
        """
        Calculate Average True Range

        Args:
            df: DataFrame with OHLC data
            period: ATR period

        Returns:
            Current ATR value
        """
        high = df['high']
        low = df['low']
        close = df['close']

        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()

        return atr.iloc[-1] if not atr.empty else 0

    def calculate_volume_average(
        self,
        df: pd.DataFrame,
        period: int = 20
    ) -> float:
        """Calculate average volume"""
        return df['volume'].rolling(window=period).mean().iloc[-1]

    def is_high_volume(self, df: pd.DataFrame, threshold: float = 1.2) -> bool:
        """Check if current volume is above average"""
        current_volume = df['volume'].iloc[-1]
        avg_volume = self.calculate_volume_average(df)

        return current_volume > (avg_volume * threshold)

    def get_symbol_info(self, pair: str) -> Optional[Dict]:
        """
        Get symbol information from MT5

        Args:
            pair: Currency pair

        Returns:
            Dictionary with symbol info
        """
        try:
            info = mt5.symbol_info(pair)
            if info is None:
                return None

            return {
                'name': info.name,
                'description': info.description,
                'point': info.point,
                'digits': info.digits,
                'spread': info.spread,
                'volume_min': info.volume_min,
                'volume_max': info.volume_max,
                'volume_step': info.volume_step,
                'contract_size': info.trade_contract_size,
            }

        except Exception as e:
            print(f"❌ Error fetching symbol info for {pair}: {e}")
            return None

    def __del__(self):
        """Cleanup MT5 connection"""
        try:
            mt5.shutdown()
            print("✅ MT5 connection closed")
        except:
            pass


# Test the market data fetcher
if __name__ == "__main__":
    print("Testing MT5 MarketData...")

    try:
        md = MarketData()

        # Test fetching candles
        print("\nFetching EURUSD M15 data...")
        df = md.get_candles('EURUSD', 'M15', count=50)

        if df is not None:
            print(f"✅ Fetched {len(df)} candles")
            print(f"Latest candle:")
            print(df.tail(1))
            print(f"\nATR: {md.calculate_atr(df):.5f}")
            print(f"Avg Volume: {md.calculate_volume_average(df):.0f}")

        # Test current price
        print("\nFetching current price...")
        price = md.get_current_price('EURUSD')
        if price:
            print(f"✅ Current EURUSD price: {price:.5f}")

        # Test symbol info
        print("\nFetching symbol info...")
        info = md.get_symbol_info('EURUSD')
        if info:
            print(f"✅ Symbol info: {info}")

        # Test multiple timeframes
        print("\nFetching multiple timeframes...")
        data = md.get_multiple_timeframes('EURUSD')
        print(f"✅ Fetched {len(data)} timeframes: {list(data.keys())}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure MT5 terminal is running and logged in")
