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
    """SMC Trading Strategy Implementation with Enhanced Features"""

    def __init__(self):
        """Initialize strategy components"""
        self.analyzer = SMCAnalyzer()
        self.market_data = MarketData()
        self.last_alerts = {}  # Track last alert time per pair

    def analyze_pair(self, pair: str) -> Optional[Dict]:
        """
        Analyze a currency pair for trade setups

        Args:
            pair: Currency pair (e.g., 'EUR/USD')

        Returns:
            Setup dictionary or None if no setup found
        """
        # Check if we should skip (cooldown period)
        if not self._can_alert(pair):
            return None

        # Check if trading session active (24/7 enabled for testing)
        # if not is_trading_session():
        #     return None

        # Fetch market data
        data = self.market_data.get_multiple_timeframes(pair)

        if not data or 'M15' not in data or 'H1' not in data:
            print(f"Could not fetch data for {pair}")
            return None

        m15_df = data['M15']
        h1_df = data['H1']
        h4_df = data.get('H4')

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

        # Find supply/demand zones
        supply_demand = self.analyzer.find_supply_demand_zones(h1_df)

        # Find fair value gaps
        fvgs = self.analyzer.find_fair_value_gaps(h1_df)

        # Find liquidity pools
        liquidity_pools = self.analyzer.find_liquidity_pools(h1_df)

        # Detect liquidity sweep
        liquidity_sweep = self.analyzer.detect_liquidity_sweep(
            m15_df,
            liquidity_pools
        )

        # Detect fakeout
        fakeout = self.analyzer.detect_fakeout(m15_df)

        # Detect Change of Character
        choch = self.analyzer.find_change_of_character(h1_df)

        # Check for confluence
        confluence_count = 0
        setup_components = {}

        # Get current price
        current_price = m15_df['close'].iloc[-1]

        # Check if order block exists and price is near it
        if order_blocks:
            ob = order_blocks[-1]  # Most recent
            if direction == 'bullish':
                # Check if price is at or approaching order block
                if ob['low'] - 0.0030 <= current_price <= ob['high'] * 1.005:
                    confluence_count += 1
                    setup_components['order_block'] = ob
            elif direction == 'bearish':
                # Check if price is at or approaching order block
                if ob['low'] * 0.995 <= current_price <= ob['high'] + 0.0030:
                    confluence_count += 1
                    setup_components['order_block'] = ob

        # Check supply/demand zones
        if direction == 'bullish' and supply_demand['demand']:
            for zone in supply_demand['demand']:
                if zone['low'] - 0.0020 <= current_price <= zone['high'] + 0.0020:
                    confluence_count += 1
                    setup_components['demand_zone'] = zone
                    break

        if direction == 'bearish' and supply_demand['supply']:
            for zone in supply_demand['supply']:
                if zone['low'] - 0.0020 <= current_price <= zone['high'] + 0.0020:
                    confluence_count += 1
                    setup_components['supply_zone'] = zone
                    break

        # Check if FVG exists
        if fvgs:
            for fvg in fvgs:
                if fvg['type'] == direction:
                    # Check if price is in or near FVG
                    if fvg['low'] - 0.0020 <= current_price <= fvg['high'] + 0.0020:
                        confluence_count += 1
                        setup_components['fvg'] = fvg
                        break

        # Check for liquidity sweep
        if liquidity_sweep and liquidity_sweep['type'] == direction:
            confluence_count += 1
            setup_components['liquidity_sweep'] = liquidity_sweep

        # Bonus: Fakeout detection
        if fakeout and fakeout['type'] == direction and fakeout.get('confirmed'):
            confluence_count += 1
            setup_components['fakeout'] = fakeout

        # Bonus: Change of Character
        if choch and choch['type'] == direction:
            setup_components['choch'] = choch

        # Need minimum confluence
        if confluence_count < config.MIN_CONFLUENCE_COUNT:
            return None

        # Store confirmations for scoring
        setup_confirmations = {
            'has_confirmation_candle': self.analyzer.has_confirmation_candle(m15_df, direction),
            'has_high_volume': self.market_data.is_high_volume(m15_df),
            'in_correct_zone': False,
            'has_bos': structure.get('bos', False),
            'has_fakeout': 'fakeout' in setup_components,
            'has_choch': 'choch' in setup_components
        }

        # Check premium/discount zone
        swing_high = h1_df['high'].tail(20).max()
        swing_low = h1_df['low'].tail(20).min()

        if direction == 'bullish':
            setup_confirmations['in_correct_zone'] = self.analyzer.is_in_discount_zone(
                current_price, swing_low, swing_high
            )
        elif direction == 'bearish':
            setup_confirmations['in_correct_zone'] = self.analyzer.is_in_premium_zone(
                current_price, swing_low, swing_high
            )

        # Calculate setup parameters
        setup = self._build_setup(
            pair=pair,
            direction=direction,
            current_price=current_price,
            structure=structure,
            components=setup_components,
            confirmations=setup_confirmations,
            m15_df=m15_df,
            h1_df=h1_df
        )

        # Score the setup
        setup['score'] = self._score_setup(setup, setup_confirmations, confluence_count)

        # Calculate TP distance for filtering
        entry = setup['entry']
        sl = setup['stop_loss']
        sl_distance = abs(entry - sl)
        tp1 = entry + (sl_distance * config.TP1_RR) if setup['direction'] == 'LONG' else entry - (sl_distance * config.TP1_RR)
        tp_pips = calculate_pips(entry, tp1, pair)

        # Only return if score meets threshold AND TP is sufficient
        if setup['score'] >= config.MIN_SETUP_SCORE and tp_pips >= config.MIN_TP_PIPS:
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
        confirmations: Dict,
        m15_df: pd.DataFrame,
        h1_df: pd.DataFrame
    ) -> Dict:
        """Build complete setup dictionary"""

        # Determine entry zone (prioritize order block, then demand/supply, then FVG)
        if 'order_block' in components:
            ob = components['order_block']
            entry_zone = [ob['low'], ob['high']]
            entry = (ob['low'] + ob['high']) / 2
        elif 'demand_zone' in components:
            zone = components['demand_zone']
            entry_zone = [zone['low'], zone['high']]
            entry = (zone['low'] + zone['high']) / 2
        elif 'supply_zone' in components:
            zone = components['supply_zone']
            entry_zone = [zone['low'], zone['high']]
            entry = (zone['low'] + zone['high']) / 2
        elif 'fvg' in components:
            fvg = components['fvg']
            entry_zone = [fvg['low'], fvg['high']]
            entry = (fvg['low'] + fvg['high']) / 2
        else:
            entry_zone = [current_price * 0.9998, current_price * 1.0002]
            entry = current_price

        # Calculate stop loss
        if direction == 'bullish':
            if 'order_block' in components:
                stop_loss = components['order_block']['low'] - (8 * 0.0001)
            elif 'demand_zone' in components:
                stop_loss = components['demand_zone']['low'] - (8 * 0.0001)
            else:
                stop_loss = entry - (30 * 0.0001)
        else:  # bearish
            if 'order_block' in components:
                stop_loss = components['order_block']['high'] + (8 * 0.0001)
            elif 'supply_zone' in components:
                stop_loss = components['supply_zone']['high'] + (8 * 0.0001)
            else:
                stop_loss = entry + (30 * 0.0001)

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
            'timestamp': datetime.now(),
            'confirmations': confirmations
        }

        # Add all components
        if 'order_block' in components:
            setup['order_block'] = components['order_block']
        if 'demand_zone' in components:
            setup['demand_zone'] = components['demand_zone']
        if 'supply_zone' in components:
            setup['supply_zone'] = components['supply_zone']
        if 'fvg' in components:
            setup['fvg'] = components['fvg']
        if 'liquidity_sweep' in components:
            setup['liquidity_sweep'] = components['liquidity_sweep']
        if 'fakeout' in components:
            setup['fakeout'] = components['fakeout']
        if 'choch' in components:
            setup['choch'] = components['choch']

        return setup

    def _score_setup(self, setup: Dict, confirmations: Dict, confluence_count: int) -> int:
        """
        Score setup quality (0-10)

        Scoring:
        - Confluence count (max 4 points)
        - Market structure (2 points)
        - Confirmation candle (1 point)
        - High volume (1 point)
        - Correct zone (1 point)
        - BOS/Fakeout/ChoCH bonuses (1 point)
        """
        score = 0

        # Base: Confluence count (max 4)
        score += min(confluence_count, 4)

        # Base: Market structure (2 points)
        if 'Bullish' in setup['structure'] or 'Bearish' in setup['structure']:
            score += 2

        # Bonus: Confirmation candle (1 point)
        if confirmations.get('has_confirmation_candle', False):
            score += 1

        # Bonus: High volume (1 point)
        if confirmations.get('has_high_volume', False):
            score += 1

        # Bonus: In correct premium/discount zone (1 point)
        if confirmations.get('in_correct_zone', False):
            score += 1

        # Bonus: BOS, Fakeout, or ChoCH (1 point)
        if (confirmations.get('has_bos', False) or
            confirmations.get('has_fakeout', False) or
            confirmations.get('has_choch', False)):
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
    print("Testing Enhanced SMC Strategy...")

    try:
        strategy = SMCStrategy()
        print("✅ Strategy initialized")

        # Test with EUR/USD
        print("\nAnalyzing EUR/USD...")
        setup = strategy.analyze_pair('EUR/USD')

        if setup:
            print(f"✅ Setup found!")
            print(f"Direction: {setup['direction']}")
            print(f"Entry: {setup['entry']:.5f}")
            print(f"Stop Loss: {setup['stop_loss']:.5f}")
            print(f"Score: {setup['score']}/10")
            print(f"Confluences: {sum([1 for k in setup.keys() if k in ['order_block', 'demand_zone', 'supply_zone', 'fvg', 'liquidity_sweep', 'fakeout']])}")
        else:
            print("No setup found (this is normal - high-quality setups are rare)")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure TWELVE_DATA_API_KEY is set in .env file")
