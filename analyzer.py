"""
SMC Market Analyzer with Advanced Features
Implements Order Blocks, Fair Value Gaps, Supply/Demand Zones, Liquidity Analysis, and Fakeout Detection
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import config
from utils import calculate_pips, pips_to_price

class SMCAnalyzer:
    """Smart Money Concepts Market Analyzer with Advanced Features"""

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

                    if move_pips >= 25:  # At least 25 pip move
                        # Check for volume confirmation
                        has_volume = current['volume'] > df['volume'].tail(20).mean() * 0.8

                        order_blocks.append({
                            'type': 'bullish',
                            'low': current['low'],
                            'high': current['close'],
                            'open': current['open'],
                            'close': current['close'],
                            'time': current.name,
                            'strength': move_pips,
                            'volume_confirmed': has_volume
                        })

            elif direction == 'bearish':
                # Find last green candle before strong red move
                if current['close'] > current['open']:  # Green candle
                    # Check if next candles show strong bearish move
                    move = current['high'] - next_candles['low'].min()
                    move_pips = move / 0.0001

                    if move_pips >= 25:
                        has_volume = current['volume'] > df['volume'].tail(20).mean() * 0.8

                        order_blocks.append({
                            'type': 'bearish',
                            'low': current['close'],
                            'high': current['high'],
                            'open': current['open'],
                            'close': current['close'],
                            'time': current.name,
                            'strength': move_pips,
                            'volume_confirmed': has_volume
                        })

        # Return most recent order blocks
        return order_blocks[-3:] if order_blocks else []

    def find_supply_demand_zones(
        self,
        df: pd.DataFrame,
        lookback: int = 50
    ) -> Dict[str, List[Dict]]:
        """
        Find supply and demand zones (areas of interest)

        Supply = Zone where price reversed down strongly
        Demand = Zone where price reversed up strongly

        Args:
            df: DataFrame with OHLC data
            lookback: Number of candles to look back

        Returns:
            Dictionary with 'supply' and 'demand' zone lists
        """
        supply_zones = []
        demand_zones = []

        recent_df = df.tail(lookback)

        for i in range(5, len(recent_df) - 5):
            candle = recent_df.iloc[i]
            prev_candles = recent_df.iloc[i-5:i]
            next_candles = recent_df.iloc[i+1:i+6]

            # Demand Zone: Price bounced up from this area
            if candle['low'] == prev_candles['low'].min():
                bounce = next_candles['high'].max() - candle['low']
                bounce_pips = bounce / 0.0001

                if bounce_pips >= 20:  # Strong bounce
                    # Zone is the candle body + wicks
                    zone_low = candle['low']
                    zone_high = max(candle['open'], candle['close'])
                    zone_size = (zone_high - zone_low) / 0.0001

                    if zone_size >= config.MIN_SUPPLY_DEMAND_SIZE:
                        demand_zones.append({
                            'type': 'demand',
                            'low': zone_low,
                            'high': zone_high,
                            'strength': bounce_pips,
                            'time': candle.name,
                            'tested': 0,
                            'broken': False
                        })

            # Supply Zone: Price rejected down from this area
            if candle['high'] == prev_candles['high'].max():
                drop = candle['high'] - next_candles['low'].min()
                drop_pips = drop / 0.0001

                if drop_pips >= 20:  # Strong rejection
                    zone_low = min(candle['open'], candle['close'])
                    zone_high = candle['high']
                    zone_size = (zone_high - zone_low) / 0.0001

                    if zone_size >= config.MIN_SUPPLY_DEMAND_SIZE:
                        supply_zones.append({
                            'type': 'supply',
                            'low': zone_low,
                            'high': zone_high,
                            'strength': drop_pips,
                            'time': candle.name,
                            'tested': 0,
                            'broken': False
                        })

        return {
            'supply': supply_zones[-3:] if supply_zones else [],
            'demand': demand_zones[-3:] if demand_zones else []
        }

    def find_fair_value_gaps(
        self,
        df: pd.DataFrame,
        min_size_pips: int = 8
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
                    # Check if middle candle shows momentum
                    middle_body = abs(candle2['close'] - candle2['open'])
                    has_momentum = middle_body > 0.0005  # Decent body size

                    fvgs.append({
                        'type': 'bullish',
                        'low': candle1['high'],
                        'high': candle3['low'],
                        'size_pips': gap_size,
                        'time': candle3.name,
                        'filled': False,
                        'momentum': has_momentum
                    })

            # Bearish FVG: Gap between candle1 low and candle3 high
            elif candle3['high'] < candle1['low']:
                gap_size = (candle1['low'] - candle3['high']) / 0.0001

                if gap_size >= min_size_pips:
                    middle_body = abs(candle2['close'] - candle2['open'])
                    has_momentum = middle_body > 0.0005

                    fvgs.append({
                        'type': 'bearish',
                        'low': candle3['high'],
                        'high': candle1['low'],
                        'size_pips': gap_size,
                        'time': candle3.name,
                        'filled': False,
                        'momentum': has_momentum
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
        for i in range(len(highs) - 20, len(highs)):
            if i < 0:
                continue
            for j in range(i + 1, min(i + 15, len(highs))):
                if abs(highs[i] - highs[j]) <= tolerance:
                    buy_side.append(highs[i])
                    break

        # Find equal lows (sell-side liquidity)
        sell_side = []
        for i in range(len(lows) - 20, len(lows)):
            if i < 0:
                continue
            for j in range(i + 1, min(i + 15, len(lows))):
                if abs(lows[i] - lows[j]) <= tolerance:
                    sell_side.append(lows[i])
                    break

        # Add round numbers as liquidity
        current_price = df['close'].iloc[-1]
        round_levels = [
            round(current_price - 0.0050, 4),
            round(current_price - 0.0025, 4),
            round(current_price, 4),
            round(current_price + 0.0025, 4),
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
                            'time': candle.Index,
                            'clean': sweep_distance < 10  # Clean if swept < 10 pips
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
                            'time': candle.Index,
                            'clean': sweep_distance < 10
                        }

        return None

    def detect_fakeout(
        self,
        df: pd.DataFrame,
        lookback: int = 10
    ) -> Optional[Dict]:
        """
        Detect fakeout patterns (false breakouts)

        Fakeout = Price breaks a level then quickly reverses

        Args:
            df: DataFrame with OHLC data
            lookback: Candles to check for fakeout

        Returns:
            Fakeout dictionary or None
        """
        if len(df) < lookback + 5:
            return None

        recent = df.tail(lookback + 5)

        # Find recent swing high/low
        swing_high = recent['high'].iloc[:-3].max()
        swing_low = recent['low'].iloc[:-3].min()

        last_candles = recent.tail(config.FAKEOUT_CONFIRMATION_CANDLES)

        # Bullish fakeout: broke below support then reversed up
        for i in range(-3, 0):
            candle = recent.iloc[i]

            # Check if it broke below swing low
            if candle['low'] < swing_low:
                # Check if it closed back above
                if candle['close'] > swing_low:
                    # Confirm with next candles moving up
                    if all(c['close'] > swing_low for _, c in last_candles.iterrows()):
                        fakeout_distance = (swing_low - candle['low']) / 0.0001

                        return {
                            'type': 'bullish',
                            'level': swing_low,
                            'fake_low': candle['low'],
                            'distance_pips': fakeout_distance,
                            'confirmed': True,
                            'time': candle.name
                        }

        # Bearish fakeout: broke above resistance then reversed down
        for i in range(-3, 0):
            candle = recent.iloc[i]

            if candle['high'] > swing_high:
                if candle['close'] < swing_high:
                    if all(c['close'] < swing_high for _, c in last_candles.iterrows()):
                        fakeout_distance = (candle['high'] - swing_high) / 0.0001

                        return {
                            'type': 'bearish',
                            'level': swing_high,
                            'fake_high': candle['high'],
                            'distance_pips': fakeout_distance,
                            'confirmed': True,
                            'time': candle.name
                        }

        return None

    def determine_market_structure(
        self,
        df: pd.DataFrame
    ) -> Dict:
        """
        Determine market structure (trend direction) with Break of Structure (BOS)

        Args:
            df: DataFrame with OHLC data

        Returns:
            Dictionary with structure info
        """
        if len(df) < 20:
            return {'bias': 'neutral', 'structure': 'unclear', 'bos': False}

        # Find recent swing highs and lows
        highs = df['high'].rolling(window=5, center=True).max()
        lows = df['low'].rolling(window=5, center=True).min()

        recent_highs = highs.tail(15).dropna()
        recent_lows = lows.tail(15).dropna()

        # Check for higher highs and higher lows (bullish)
        if len(recent_highs) >= 3 and len(recent_lows) >= 3:
            hh = recent_highs.iloc[-1] > recent_highs.iloc[-2] > recent_highs.iloc[-3]
            hl = recent_lows.iloc[-1] > recent_lows.iloc[-2]

            # Check for Break of Structure (BOS)
            bos_bullish = df['close'].iloc[-1] > recent_highs.iloc[-2]

            if hh and hl:
                return {
                    'bias': 'bullish',
                    'structure': 'Bullish (HH/HL)',
                    'strength': 'strong',
                    'bos': bos_bullish
                }

            # Check for lower highs and lower lows (bearish)
            lh = recent_highs.iloc[-1] < recent_highs.iloc[-2] < recent_highs.iloc[-3]
            ll = recent_lows.iloc[-1] < recent_lows.iloc[-2]

            bos_bearish = df['close'].iloc[-1] < recent_lows.iloc[-2]

            if lh and ll:
                return {
                    'bias': 'bearish',
                    'structure': 'Bearish (LH/LL)',
                    'strength': 'strong',
                    'bos': bos_bearish
                }

        return {
            'bias': 'neutral',
            'structure': 'Ranging/Consolidation',
            'strength': 'weak',
            'bos': False
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
            if lower_wick > body * 2 and last['close'] > last['open']:
                return True

            # Strong bullish candle
            if last['close'] > last['open']:
                body_size = (last['close'] - last['open']) / 0.0001
                if body_size > 10:  # Strong 10+ pip body
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
            if upper_wick > body * 2 and last['close'] < last['open']:
                return True

            # Strong bearish candle
            if last['close'] < last['open']:
                body_size = (last['open'] - last['close']) / 0.0001
                if body_size > 10:
                    return True

        return False

    def find_change_of_character(
        self,
        df: pd.DataFrame
    ) -> Optional[Dict]:
        """
        Find Change of Character (ChoCH) - early trend change signal

        ChoCH = Break of recent structure without full trend change

        Args:
            df: DataFrame with OHLC data

        Returns:
            ChoCH dictionary or None
        """
        if len(df) < 20:
            return None

        recent = df.tail(20)
        current_price = df['close'].iloc[-1]

        # Find last swing high and low
        swing_high = recent['high'].iloc[:-3].max()
        swing_low = recent['low'].iloc[:-3].min()

        # Bullish ChoCH: broke above recent high
        if current_price > swing_high:
            return {
                'type': 'bullish',
                'level': swing_high,
                'break_distance': (current_price - swing_high) / 0.0001,
                'time': df.index[-1]
            }

        # Bearish ChoCH: broke below recent low
        if current_price < swing_low:
            return {
                'type': 'bearish',
                'level': swing_low,
                'break_distance': (swing_low - current_price) / 0.0001,
                'time': df.index[-1]
            }

        return None


# Test the analyzer
if __name__ == "__main__":
    print("Testing Enhanced SMC Analyzer...")

    analyzer = SMCAnalyzer()
    print("✅ SMC Analyzer initialized successfully")
    print("✅ Features: Order Blocks, Supply/Demand, FVG, Liquidity, Fakeouts, ChoCH")
