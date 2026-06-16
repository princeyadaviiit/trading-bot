"""
SMC Trading Strategy
Main strategy logic that combines analysis and generates trade setups
"""
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime, timedelta
import config
from analyzer import SMCAnalyzer
from market_data import MarketData
from utils import (
    calculate_lot_size,
    get_risk_amount,
    is_trading_session,
    calculate_pips
)

class SMCStrategy:
    """SMC Trading Strategy Implementation"""

    def __init__(self):
        """Initialize strategy components"""
        self.analyzer = SMCAnalyzer()
        self.market_data = MarketData()
        self.last_alerts = {}  # Track last alert time per pair

    def analyze_pair(self, pair: str) -> Optional[Dict]:
        """
        Analyze a currency pair for trade setups

        Args:
            pair: Currency pair (e.g., 'EUR_USD')

        Returns:
            Setup dictionary or None if no setup found
        """
        # Check if we should skip (cooldown period)
        if not self._can_alert(pair):
            return None

        # Check if trading session active
        if not is_trading_session():
            return None

        # Fetch market data
        data = self.market_data.get_multiple_timeframes(pair)

        if not data or 'M15' not in data or 'H1' not in data:
            print(f"Could not fetch data for {pair}")
            return None

        m15_df = data['M15']
        h1_df = data['H1']

        # Determine market structure on H1
        structure = self.analyzer.determine_market_structure(h1_df)

        if structure['bias'] == 'neutral':
            return None  # No clear bias

        # Find SMC components
        direction = structure['bias']

        # Find order blocks
        order_blocks = self.analyzer.find_order_blocks(
            h1_df,
            direction=direction
        )

        # Find fair value gaps
        fvgs = self.analyzer.find_fair_value_gaps(h1_df)

        # Find liquidity pools
        liquidity_pools = self.analyzer.find_liquidity_pools(h1_df)

        # Detect liquidity sweep
        liquidity_sweep = self.analyzer.detect_liquidity_sweep(
            m15_df,
            liquidity_pools
        )

        # Check for confluence
        confluence_count = 0
        setup_components = {}

        # Get current price
        current_price = m15_df['close'].iloc[-1]

        # Check if price is near order block
        if order_blocks:
            ob = order_blocks[-1]  # Most recent
            if direction == 'bullish':
                if ob['low'] <= current_price <= ob['high'] * 1.002:
                    confluence_count += 1
                    setup_components['order_block'] = ob
            elif direction == 'bearish':
                if ob['low'] * 0.998 <= current_price <= ob['high']:
                    confluence_count += 1
                    setup_components['order_block'] = ob

        # Check if price is near FVG
        if fvgs:
            for fvg in fvgs:
                if fvg['type'] == direction:
                    if fvg['low'] <= current_price <= fvg['high']:
                        confluence_count += 1
                        setup_components['fvg'] = fvg
                        break

        # Check for liquidity sweep
        if liquidity_sweep and liquidity_sweep['type'] == direction:
            confluence_count += 1
            setup_components['liquidity_sweep'] = liquidity_sweep

        # Need minimum confluence
        if confluence_count < config.MIN_CONFLUENCE_COUNT:
            return None

        # Check for confirmation candle on M15
        if not self.analyzer.has_confirmation_candle(m15_df, direction):
            return None

        # Check volume
        if not self.market_data.is_high_volume(m15_df):
            return None

        # Check premium/discount zone
        swing_high = h1_df['high'].tail(20).max()
        swing_low = h1_df['low'].tail(20).min()

        if direction == 'bullish':
            if not self.analyzer.is_in_discount_zone(
                current_price, swing_low, swing_high
            ):
                return None
        elif direction == 'bearish':
            if not self.analyzer.is_in_premium_zone(
                current_price, swing_low, swing_high
            ):
                return None

        # Calculate setup parameters
        setup = self._build_setup(
            pair=pair,
            direction=direction,
            current_price=current_price,
            structure=structure,
            components=setup_components,
            m15_df=m15_df,
            h1_df=h1_df
        )

        # Score the setup
        setup['score'] = self._score_setup(setup)

        # Only return if score meets threshold
        if setup['score'] >= config.MIN_SETUP_SCORE:
            self.last_alerts[pair] = datetime.now()
            return setup

        return None

    def _build_setup(
        self,
        pair: str,
        direction: str,
        current_price: float,
        structure: Dict,
        components: Dict,
        m15_df: pd.DataFrame,
        h1_df: pd.DataFrame
    ) -> Dict:
        """Build complete setup dictionary"""

        # Determine entry zone
        if 'order_block' in components:
            ob = components['order_block']
            entry_zone = [ob['low'], ob['high']]
            entry = (ob['low'] + ob['high']) / 2
        elif 'fvg' in components:
            fvg = components['fvg']
            entry_zone = [fvg['low'], fvg['high']]
            entry = (fvg['low'] + fvg['high']) / 2
        else:
            entry_zone = [current_price * 0.9995, current_price * 1.0005]
            entry = current_price

        # Calculate stop loss
        if direction == 'bullish':
            if 'order_block' in components:
                stop_loss = components['order_block']['low'] - (10 * 0.0001)
            else:
                stop_loss = entry - (50 * 0.0001)
        else:  # bearish
            if 'order_block' in components:
                stop_loss = components['order_block']['high'] + (10 * 0.0001)
            else:
                stop_loss = entry + (50 * 0.0001)

        # Calculate position size
        sl_pips = calculate_pips(entry, stop_loss, pair)
        risk_amount = get_risk_amount()
        lot_size = calculate_lot_size(sl_pips, risk_amount)

        setup = {
            'pair': pair,
            'direction': direction.upper(),
            'entry': entry,
            'entry_zone': entry_zone,
            'stop_loss': stop_loss,
            'lot_size': lot_size,
            'risk_amount': risk_amount,
            'structure': structure['structure'],
            'bias': f"Strong {direction.title()}",
            'timestamp': datetime.now()
        }

        # Add components
        if 'order_block' in components:
            setup['order_block'] = components['order_block']
        if 'fvg' in components:
            setup['fvg'] = components['fvg']
        if 'liquidity_sweep' in components:
            setup['liquidity_sweep'] = components['liquidity_sweep']

        return setup

    def _score_setup(self, setup: Dict) -> int:
        """
        Score setup quality (0-10)

        Scoring:
        - Confluence (max 3 points)
        - Market structure (2 points)
        - Liquidity sweep (2 points)
        - Volume (1 point)
        - Session (1 point)
        - Candle pattern (1 point)
        """
        score = 0

        # Confluence count (max 3)
        confluence_count = 0
        if 'order_block' in setup:
            confluence_count += 1
        if 'fvg' in setup:
            confluence_count += 1
        if 'liquidity_sweep' in setup:
            confluence_count += 1

        score += min(confluence_count, 3)

        # Market structure (2 points)
        if 'Bullish' in setup['structure'] or 'Bearish' in setup['structure']:
            score += 2

        # Liquidity sweep quality (2 points)
        if 'liquidity_sweep' in setup:
            sweep = setup['liquidity_sweep']
            if sweep.get('sweep_pips', 0) < 15:
                score += 2  # Clean sweep
            else:
                score += 1  # Weak sweep

        # Volume is always checked before creating setup (1 point)
        score += 1

        # Session timing is always checked (1 point)
        score += 1

        # Confirmation candle is always checked (1 point)
        score += 1

        return min(score, 10)

    def _can_alert(self, pair: str) -> bool:
        """Check if enough time passed since last alert for this pair"""
        if pair not in self.last_alerts:
            return True

        last_alert_time = self.last_alerts[pair]
        cooldown = timedelta(minutes=config.ALERT_COOLDOWN_MINUTES)

        return datetime.now() - last_alert_time > cooldown

    def scan_pairs(self, pairs: List[str]) -> List[Dict]:
        """
        Scan multiple pairs for setups

        Args:
            pairs: List of currency pairs

        Returns:
            List of setup dictionaries
        """
        setups = []

        for pair in pairs:
            try:
                setup = self.analyze_pair(pair)
                if setup:
                    setups.append(setup)
            except Exception as e:
                print(f"Error analyzing {pair}: {e}")

        return setups


# Test the strategy
if __name__ == "__main__":
    print("Testing SMC Strategy...")

    try:
        strategy = SMCStrategy()
        print("✅ Strategy initialized")

        # Test with EUR_USD
        print("\nAnalyzing EUR_USD...")
        setup = strategy.analyze_pair('EUR_USD')

        if setup:
            print(f"✅ Setup found!")
            print(f"Direction: {setup['direction']}")
            print(f"Entry: {setup['entry']:.5f}")
            print(f"Stop Loss: {setup['stop_loss']:.5f}")
            print(f"Score: {setup['score']}/10")
        else:
            print("No setup found (this is normal - setups are rare)")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure OANDA credentials are set in .env file")
