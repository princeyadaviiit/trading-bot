"""
Twelve Data Market Data Integration
Fetches real-time forex data from Twelve Data API
"""
import requests
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time
import config

class MarketData:
    """Handler for Twelve Data API market data"""

    def __init__(self):
        """Initialize Twelve Data API connection"""
        self.api_key = config.TWELVE_DATA_API_KEY
        self.base_url = "https://api.twelvedata.com"

        if not self.api_key:
            raise ValueError("TWELVE_DATA_API_KEY is not set in environment variables")

        print(f"✅ Twelve Data API initialized")
        self.cache = {}
        self.cache_duration = 60  # Cache for 60 seconds to avoid redundant API calls
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum 1 second between requests

    def _wait_for_rate_limit(self):
        """Ensure we don't exceed rate limits"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def _get_cache_key(self, pair: str, timeframe: str) -> str:
        """Generate cache key"""
        return f"{pair}_{timeframe}"

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False

        cached_time, _ = self.cache[cache_key]
        return (datetime.now() - cached_time).total_seconds() < self.cache_duration

    def _convert_timeframe(self, timeframe: str) -> str:
        """Convert internal timeframe to Twelve Data format"""
        timeframe_map = {
            'M1': '1min',
            'M5': '5min',
            'M15': '15min',
            'M30': '30min',
            'H1': '1h',
            'H4': '4h',
            'D1': '1day',
            'W1': '1week',
            'MN1': '1month'
        }
        return timeframe_map.get(timeframe, '15min')

    def get_candles(
        self,
        pair: str,
        timeframe: str = 'M15',
        count: int = 100
    ) -> Optional[pd.DataFrame]:
        """
        Fetch candlestick data from Twelve Data API

        Args:
            pair: Currency pair (e.g., 'EUR/USD')
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
            # Rate limiting
            self._wait_for_rate_limit()

            # Convert timeframe
            interval = self._convert_timeframe(timeframe)

            # API endpoint
            url = f"{self.base_url}/time_series"

            params = {
                'symbol': pair,
                'interval': interval,
                'outputsize': count,
                'apikey': self.api_key,
                'format': 'JSON'
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                print(f"❌ API Error {response.status_code} for {pair}")
                return None

            data = response.json()

            if 'values' not in data:
                if 'message' in data:
                    print(f"❌ API Message: {data['message']}")
                else:
                    print(f"❌ No data in response for {pair}")
                return None

            # Convert to DataFrame
            df = pd.DataFrame(data['values'])

            # Convert datetime
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime', inplace=True)
            df.sort_index(inplace=True)  # Sort chronologically

            # Convert strings to floats
            df['open'] = df['open'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)
            df['volume'] = df['volume'].astype(float)

            # Select only needed columns
            df = df[['open', 'high', 'low', 'close', 'volume']]

            # Cache the result
            self.cache[cache_key] = (datetime.now(), df.copy())

            print(f"✅ Fetched {len(df)} candles for {pair} {timeframe}")
            return df

        except requests.exceptions.Timeout:
            print(f"❌ Request timeout for {pair}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error for {pair}: {e}")
            return None
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
            self._wait_for_rate_limit()

            url = f"{self.base_url}/price"
            params = {
                'symbol': pair,
                'apikey': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                return None

            data = response.json()

            if 'price' in data:
                return float(data['price'])

            return None

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

        for tf in timeframes:
            df = self.get_candles(pair, tf, count=100)
            if df is not None and not df.empty:
                data[tf] = df
            time.sleep(0.5)  # Small delay between requests

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
        if df is None or df.empty or len(df) < period:
            return 0

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
        if df is None or df.empty or len(df) < period:
            return 0
        return df['volume'].rolling(window=period).mean().iloc[-1]

    def is_high_volume(self, df: pd.DataFrame, threshold: float = 1.3) -> bool:
        """Check if current volume is above average"""
        if df is None or df.empty:
            return False

        current_volume = df['volume'].iloc[-1]
        avg_volume = self.calculate_volume_average(df)

        if avg_volume == 0:
            return False

        return current_volume > (avg_volume * threshold)

    def get_symbol_info(self, pair: str) -> Optional[Dict]:
        """
        Get symbol information

        Args:
            pair: Currency pair

        Returns:
            Dictionary with symbol info
        """
        # For forex pairs, return standard info
        return {
            'name': pair,
            'description': f"{pair} Forex Pair",
            'type': 'Forex',
            'currency_base': pair.split('/')[0] if '/' in pair else pair[:3],
            'currency_quote': pair.split('/')[1] if '/' in pair else pair[3:],
        }


# Test the market data fetcher
if __name__ == "__main__":
    print("Testing Twelve Data MarketData...")

    try:
        md = MarketData()

        # Test fetching candles
        print("\nFetching EUR/USD M15 data...")
        df = md.get_candles('EUR/USD', 'M15', count=50)

        if df is not None:
            print(f"✅ Fetched {len(df)} candles")
            print(f"Latest candle:")
            print(df.tail(1))
            print(f"\nATR: {md.calculate_atr(df):.5f}")
            print(f"Avg Volume: {md.calculate_volume_average(df):.0f}")

        # Test current price
        print("\nFetching current price...")
        price = md.get_current_price('EUR/USD')
        if price:
            print(f"✅ Current EUR/USD price: {price:.5f}")

        # Test multiple timeframes
        print("\nFetching multiple timeframes...")
        data = md.get_multiple_timeframes('EUR/USD')
        print(f"✅ Fetched {len(data)} timeframes: {list(data.keys())}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure TWELVE_DATA_API_KEY is set in .env file")
