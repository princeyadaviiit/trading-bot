"""
Utility functions for SMC Trading Bot
"""
import pytz
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import config

def get_ist_time() -> datetime:
    """Get current time in IST"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

def is_london_session() -> bool:
    """Check if current time is during London session"""
    now = get_ist_time()

    london_open = now.replace(
        hour=config.LONDON_OPEN_HOUR,
        minute=config.LONDON_OPEN_MINUTE,
        second=0,
        microsecond=0
    )

    london_close = now.replace(
        hour=config.LONDON_CLOSE_HOUR,
        minute=config.LONDON_CLOSE_MINUTE,
        second=0,
        microsecond=0
    )

    return london_open <= now <= london_close

def is_ny_session() -> bool:
    """Check if current time is during NY session"""
    now = get_ist_time()

    ny_open = now.replace(
        hour=config.NY_OPEN_HOUR,
        minute=config.NY_OPEN_MINUTE,
        second=0,
        microsecond=0
    )

    # Handle NY close after midnight
    if config.NY_CLOSE_HOUR < config.NY_OPEN_HOUR:
        ny_close = (now + timedelta(days=1)).replace(
            hour=config.NY_CLOSE_HOUR,
            minute=config.NY_CLOSE_MINUTE,
            second=0,
            microsecond=0
        )
    else:
        ny_close = now.replace(
            hour=config.NY_CLOSE_HOUR,
            minute=config.NY_CLOSE_MINUTE,
            second=0,
            microsecond=0
        )

    return ny_open <= now <= ny_close

def is_trading_session() -> bool:
    """Check if current time is during any trading session"""
    # Enable 24/7 trading (including Asian session)
    return True
    # Original session-only logic:
    # return is_london_session() or is_ny_session()

def get_current_session() -> str:
    """Get name of current trading session"""
    if is_london_session() and is_ny_session():
        return "London-NY Overlap"
    elif is_london_session():
        return "London"
    elif is_ny_session():
        return "NY"
    else:
        return "Asian/Off-Hours"

def calculate_lot_size(stop_loss_pips: float, risk_amount: float) -> float:
    """
    Calculate lot size based on stop loss and risk amount

    Args:
        stop_loss_pips: Stop loss distance in pips
        risk_amount: Amount to risk in dollars

    Returns:
        Lot size (rounded to 2 decimals)
    """
    if stop_loss_pips <= 0:
        return 0.01

    # Calculate lot size
    # For EURUSD: 1 pip = $10 per standard lot (1.0)
    # We want: risk_amount = lot_size * stop_loss_pips * pip_value
    # pip_value for micro lot (0.01) = $0.10

    lot_size = risk_amount / (stop_loss_pips * config.PIP_VALUE_MICRO * 100)

    # Round to 2 decimal places and ensure minimum
    lot_size = max(0.01, round(lot_size, 2))

    return lot_size

def format_price(price: float, decimals: int = 5) -> str:
    """Format price with appropriate decimal places"""
    return f"{price:.{decimals}f}"

def calculate_pips(price1: float, price2: float, pair: str = 'EUR_USD') -> float:
    """
    Calculate pip difference between two prices

    Args:
        price1: First price
        price2: Second price
        pair: Currency pair (for JPY pairs use 2 decimals)

    Returns:
        Pip difference
    """
    # JPY pairs use 2 decimal places, others use 4
    pip_decimal = 0.01 if 'JPY' in pair else 0.0001

    return abs(price1 - price2) / pip_decimal

def pips_to_price(pips: float, pair: str = 'EUR_USD') -> float:
    """Convert pips to price difference"""
    pip_decimal = 0.01 if 'JPY' in pair else 0.0001
    return pips * pip_decimal

def format_telegram_message(setup: Dict) -> str:
    """
    Format setup data into Telegram message

    Args:
        setup: Dictionary containing setup information

    Returns:
        Formatted message string
    """
    direction_emoji = "🟢" if setup['direction'] == 'LONG' else "🔴"
    direction_text = "LONG" if setup['direction'] == 'LONG' else "SHORT"

    # Build confluence list
    confluences = []
    if setup.get('order_block'):
        ob = setup['order_block']
        confluences.append(f"✅ Order Block: {format_price(ob['low'])}-{format_price(ob['high'])}")

    if setup.get('fvg'):
        fvg = setup['fvg']
        confluences.append(f"✅ FVG: {format_price(fvg['low'])}-{format_price(fvg['high'])}")

    if setup.get('liquidity_sweep'):
        sweep = setup['liquidity_sweep']
        confluences.append(f"✅ Liquidity Sweep: {format_price(sweep['level'])}")

    confluence_text = "\n".join(confluences)
    confluence_count = len(confluences)

    # Calculate TPs
    entry = setup['entry']
    sl = setup['stop_loss']
    sl_distance = abs(entry - sl)

    tp1 = entry + (sl_distance * config.TP1_RR) if setup['direction'] == 'LONG' else entry - (sl_distance * config.TP1_RR)
    tp2 = entry + (sl_distance * config.TP2_RR) if setup['direction'] == 'LONG' else entry - (sl_distance * config.TP2_RR)
    tp3 = entry + (sl_distance * config.TP3_RR) if setup['direction'] == 'LONG' else entry - (sl_distance * config.TP3_RR)

    sl_pips = calculate_pips(entry, sl, setup['pair'])
    tp1_pips = calculate_pips(entry, tp1, setup['pair'])
    tp2_pips = calculate_pips(entry, tp2, setup['pair'])
    tp3_pips = calculate_pips(entry, tp3, setup['pair'])

    # Format confirmations
    confirmations = setup.get('confirmations', {})
    conf_candle = "✅" if confirmations.get('has_confirmation_candle', False) else "⚠️"
    conf_volume = "✅" if confirmations.get('has_high_volume', False) else "⚠️"
    conf_zone = "✅" if confirmations.get('in_correct_zone', False) else "⚠️"

    # Format message
    message = f"""🚨 TRADE SETUP DETECTED 🚨

Pair: {setup['pair'].replace('_', '')}
Direction: {direction_emoji} {direction_text}
Entry Zone: {format_price(setup['entry_zone'][0])} - {format_price(setup['entry_zone'][1])}

💎 CONFLUENCES ({confluence_count}/3):
{confluence_text}

📊 TRADE SETUP:
Entry: {format_price(entry)}
Stop Loss: {format_price(sl)} ({int(sl_pips)} pips)
TP1: {format_price(tp1)} ({int(tp1_pips)} pips | 1:{config.TP1_RR})
TP2: {format_price(tp2)} ({int(tp2_pips)} pips | 1:{config.TP2_RR})
TP3: {format_price(tp3)} ({int(tp3_pips)} pips | 1:{config.TP3_RR})

💰 POSITION SIZE:
Lot Size: {setup['lot_size']} lots
Risk: ${setup['risk_amount']:.2f} ({config.RISK_PERCENT}%)

📈 MARKET INFO:
Structure: {setup.get('structure', 'N/A')}
Bias: {setup.get('bias', 'N/A')}
Session: {get_current_session()}
Time: {get_ist_time().strftime('%H:%M IST')}

⚠️ CONFIRMATION STATUS:
{conf_candle} Confirmation Candle
{conf_volume} High Volume
{conf_zone} Correct Premium/Discount Zone

---
Setup Score: {setup['score']}/10 {'⭐' * min(setup['score'], 10)}
"""

    return message

def convert_mt5_pair(pair: str) -> str:
    """Convert standard pair format to MT5 format (EUR/USD -> EURUSD)"""
    return pair.replace('/', '').replace('_', '')

def convert_standard_pair(pair: str) -> str:
    """Convert MT5 pair format to display format (EURUSD -> EURUSD)"""
    return pair.replace('_', '').replace('/', '')

def get_risk_amount() -> float:
    """Calculate risk amount based on account size and risk percentage"""
    return config.ACCOUNT_SIZE * (config.RISK_PERCENT / 100)

def validate_pair(pair: str) -> bool:
    """Validate if pair format is correct for MT5"""
    # Accept EURUSD, EUR/USD formats
    pair = pair.upper().replace('/', '').replace('_', '')

    # Check if it's a valid forex pair (6 characters)
    if len(pair) != 6:
        return False

    # Should be all letters
    if not pair.isalpha():
        return False

    return True

# Test functions
if __name__ == "__main__":
    print(f"Current IST Time: {get_ist_time()}")
    print(f"Is Trading Session: {is_trading_session()}")
    print(f"Current Session: {get_current_session()}")
    print(f"London Session Active: {is_london_session()}")
    print(f"NY Session Active: {is_ny_session()}")
    print(f"\nRisk Amount: ${get_risk_amount():.2f}")
    print(f"Lot Size for 50 pips SL: {calculate_lot_size(50, get_risk_amount())}")
