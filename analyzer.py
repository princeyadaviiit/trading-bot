"""
SMC Market Analyzer
Implements Order Blocks, Fair Value Gaps, and Liquidity Analysis
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import config
from utils import calculate_pips, pips_to_price

class SMCAnalyzer:
    """Smart Money Concepts Market Analyzer"""

    def __init__(self):
        """Initialize analyzer"""
        pass

    def find_order_blocks(
        self,
        df: pd.DataFrame,
        direction: str = 'bullish'
    ) -> List[Dict]:
        """
        Find order blocks in price data

        Order Block = Last opposite candle before strong move

        Args:
            df: DataFrame with OHLC data
            direction: 'bullish' or 'bearish'

        Returns:
            List of order block dictionaries
        """
        order_blocks = []

        for i in range(len(df) - 10, len(df) - 1):
            if i < 10:
                continue

            current = df.iloc[i]
            next_candles = df.iloc[i+1:i+6]

            if direction == 'bullish':
                # Find last red candle before strong green move
                if current['close'] < current['open']:  # Red candle
                    # Check if next candles show strong bullish move
                    move = next_candles['high'].max() - current['low']
                    move_pips = move / 0.0001

                    if move_pips >= 30:  # At least 30 pip move
                        order_blocks.append({
                            'type': 'bullish',
                            'low': current['low'],
                            'high': current['close'],
                            'open': current['open'],
                            'close': current['close'],
                            'time': current.name,
                            'strength': move_pips
                        })

            elif direction == 'bearish':
                # Find last green candle before strong red move
                if current['close'] > current['open']:  # Green candle
                    # Check if next candles show strong bearish move
                    move = current['high'] - next_candles['low'].min()
                    move_pips = move / 0.0001

                    if move_pips >= 30:
                        order_blocks.append({
                            'type': 'bearish',
                            'low': current['close'],
                            'high': current['high'],
                            'open': current['open'],
                            'close': current['close'],
                            'time': current.name,
                            'strength': move_pips
                        })

        # Return most recent order blocks
        return order_blocks[-3:] if order_blocks else []

    def find_fair_value_gaps(
        self,
        df: pd.DataFrame,
        min_size_pips: int = 10
    ) -> List[Dict]:
        """
        Find Fair Value Gaps (3-candle imbalance patterns)

        FVG = Gap between candle 1 high and candle 3 low (bullish)
              or candle 1 low and candle 3 high (bearish)

        Args:
            df: DataFrame with OHLC data
            min_size_pips: Minimum gap size in pips

        Returns:
            List of FVG dictionaries
        """
        fvgs = []

        for i in range(2, len(df)):
            candle1 = df.iloc[i-2]
            candle2 = df.iloc[i-1]
            candle3 = df.iloc[i]

            # Bullish FVG: Gap between candle1 high and candle3 low
            if candle3['low'] > candle1['high']:
                gap_size = (candle3['low'] - candle1['high']) / 0.0001

                if gap_size >= min_size_pips:
                    fvgs.append({
                        'type': 'bullish',
                        'low': candle1['high'],
                        'high': candle3['low'],
                        'size_pips': gap_size,
                        'time': candle3.name,
                        'filled': False
                    })

            # Bearish FVG: Gap between candle1 low and candle3 high
            elif candle3['high'] < candle1['low']:
                gap_size = (candle1['low'] - candle3['high']) / 0.0001

                if gap_size >= min_size_pips:
                    fvgs.append({
                        'type': 'bearish',
                        'low': candle3['high'],
                        'high': candle1['low'],
                        'size_pips': gap_size,
                        'time': candle3.name,
                        'filled': False
                    })

        # Return most recent unfilled FVGs
        return fvgs[-5:] if fvgs else []

    def find_liquidity_pools(
        self,
        df: pd.DataFrame,
        tolerance_pips: int = 10
    ) -> Dict[str, List[float]]:
        """
        Find liquidity pools (equal highs/lows)

        Args:
            df: DataFrame with OHLC data
            tolerance_pips: How close levels need to be (pips)

        Returns:
            Dictionary with 'buy_side' and 'sell_side' liquidity levels
        """
        highs = df['high'].values
        lows = df['low'].values

        tolerance = tolerance_pips * 0.0001

        # Find equal highs (buy-side liquidity)
        buy_side = []
        for i in range(len(highs) - 5, len(highs)):
            for j in range(i + 1, min(i + 10, len(highs))):
                if abs(highs[i] - highs[j]) <= tolerance:
                    buy_side.append(highs[i])
                    break

        # Find equal lows (sell-side liquidity)
        sell_side = []
        for i in range(len(lows) - 5, len(lows)):
            for j in range(i + 1, min(i + 10, len(lows))):
                if abs(lows[i] - lows[j]) <= tolerance:
                    sell_side.append(lows[i])
                    break

        # Add round numbers as liquidity
        current_price = df['close'].iloc[-1]
        round_levels = [
            round(current_price - 0.0050, 4),
            round(current_price, 4),
            round(current_price + 0.0050, 4)
        ]

        return {
            'buy_side': list(set(buy_side)) + [r for r in round_levels if r > current_price],
            'sell_side': list(set(sell_side)) + [r for r in round_levels if r < current_price]
        }

    def detect_liquidity_sweep(
        self,
        df: pd.DataFrame,
        liquidity_pools: Dict,
        sweep_range_pips: int = 20
    ) -> Optional[Dict]:
        """
        Detect recent liquidity sweep

        Sweep = Price spikes through liquidity, then reverses

        Args:
            df: DataFrame with OHLC data
            liquidity_pools: Dict with buy/sell side liquidity
            sweep_range_pips: Maximum sweep distance

        Returns:
            Sweep dictionary or None
        """
        if len(df) < 5:
            return None

        recent_candles = df.tail(5)
        sweep_range = sweep_range_pips * 0.0001

        # Check for bullish sweep (price swept down then up)
        for level in liquidity_pools.get('sell_side', []):
            for candle in recent_candles.itertuples():
                # Check if candle wicked below level then closed above
                if candle.low < level and candle.close > level:
                    sweep_distance = (level - candle.low) / 0.0001

                    if sweep_distance <= sweep_range_pips:
                        return {
                            'type': 'bullish',
                            'level': level,
                            'low': candle.low,
                            'sweep_pips': sweep_distance,
                            'time': candle.Index
                        }

        # Check for bearish sweep (price swept up then down)
        for level in liquidity_pools.get('buy_side', []):
            for candle in recent_candles.itertuples():
                # Check if candle wicked above level then closed below
                if candle.high > level and candle.close < level:
                    sweep_distance = (candle.high - level) / 0.0001

                    if sweep_distance <= sweep_range_pips:
                        return {
                            'type': 'bearish',
                            'level': level,
                            'high': candle.high,
                            'sweep_pips': sweep_distance,
                            'time': candle.Index
                        }

        return None

    def determine_market_structure(
        self,
        df: pd.DataFrame
    ) -> Dict:
        """
        Determine market structure (trend direction)

        Args:
            df: DataFrame with OHLC data

        Returns:
            Dictionary with structure info
        """
        if len(df) < 20:
            return {'bias': 'neutral', 'structure': 'unclear'}

        # Find recent swing highs and lows
        highs = df['high'].rolling(window=5, center=True).max()
        lows = df['low'].rolling(window=5, center=True).min()

        recent_highs = highs.tail(10).dropna()
        recent_lows = lows.tail(10).dropna()

        # Check for higher highs and higher lows (bullish)
        if len(recent_highs) >= 2 and len(recent_lows) >= 2:
            hh = recent_highs.iloc[-1] > recent_highs.iloc[-2]
            hl = recent_lows.iloc[-1] > recent_lows.iloc[-2]

            if hh and hl:
                return {
                    'bias': 'bullish',
                    'structure': 'Bullish (HH/HL)',
                    'strength': 'strong'
                }

            # Check for lower highs and lower lows (bearish)
            lh = recent_highs.iloc[-1] < recent_highs.iloc[-2]
            ll = recent_lows.iloc[-1] < recent_lows.iloc[-2]

            if lh and ll:
                return {
                    'bias': 'bearish',
                    'structure': 'Bearish (LH/LL)',
                    'strength': 'strong'
                }

        return {
            'bias': 'neutral',
            'structure': 'Ranging/Consolidation',
            'strength': 'weak'
        }

    def is_in_discount_zone(
        self,
        current_price: float,
        swing_low: float,
        swing_high: float
    ) -> bool:
        """Check if price is in discount zone (lower 50%)"""
        range_size = swing_high - swing_low
        discount_level = swing_low + (range_size * 0.5)

        return current_price < discount_level

    def is_in_premium_zone(
        self,
        current_price: float,
        swing_low: float,
        swing_high: float
    ) -> bool:
        """Check if price is in premium zone (upper 50%)"""
        range_size = swing_high - swing_low
        premium_level = swing_low + (range_size * 0.5)

        return current_price > premium_level

    def has_confirmation_candle(
        self,
        df: pd.DataFrame,
        direction: str
    ) -> bool:
        """
        Check for bullish/bearish confirmation candle patterns

        Args:
            df: DataFrame with OHLC data
            direction: 'bullish' or 'bearish'

        Returns:
            True if confirmation candle exists
        """
        if len(df) < 2:
            return False

        last = df.iloc[-1]
        prev = df.iloc[-2]

        if direction == 'bullish':
            # Bullish engulfing
            if (prev['close'] < prev['open'] and
                last['close'] > last['open'] and
                last['close'] > prev['open'] and
                last['open'] < prev['close']):
                return True

            # Hammer (long lower wick)
            body = abs(last['close'] - last['open'])
            lower_wick = min(last['open'], last['close']) - last['low']
            if lower_wick > body * 2:
                return True

            # Pin bar
            if last['close'] > last['open'] and lower_wick > body:
                return True

        elif direction == 'bearish':
            # Bearish engulfing
            if (prev['close'] > prev['open'] and
                last['close'] < last['open'] and
                last['close'] < prev['open'] and
                last['open'] > prev['close']):
                return True

            # Shooting star (long upper wick)
            body = abs(last['close'] - last['open'])
            upper_wick = last['high'] - max(last['open'], last['close'])
            if upper_wick > body * 2:
                return True

        return False


# Test the analyzer
if __name__ == "__main__":
    print("Testing SMC Analyzer...")

    # This would need real market data to test properly
    # For now, just verify it imports correctly
    analyzer = SMCAnalyzer()
    print("✅ SMC Analyzer initialized successfully")
