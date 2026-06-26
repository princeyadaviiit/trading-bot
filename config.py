"""
Configuration settings for SMC Trading Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Twelve Data API Configuration
TWELVE_DATA_API_KEY = os.getenv('TWELVE_DATA_API_KEY')

# Trading Configuration
ACCOUNT_SIZE = float(os.getenv('ACCOUNT_SIZE', 1000))
RISK_PERCENT = float(os.getenv('RISK_PERCENT', 0.5))
MIN_SETUP_SCORE = int(os.getenv('MIN_SETUP_SCORE', 3))
MIN_TP_PIPS = float(os.getenv('MIN_TP_PIPS', 5.0))  # Minimum TP distance to auto-send signals

# Scan Interval (every 3 minutes = 480 calls per day)
SCAN_INTERVAL_SECONDS = int(os.getenv('SCAN_INTERVAL_SECONDS', 180))  # 3 minutes

# Session Times (IST)
LONDON_OPEN_HOUR = int(os.getenv('LONDON_OPEN_HOUR', 13))
LONDON_OPEN_MINUTE = int(os.getenv('LONDON_OPEN_MINUTE', 30))
LONDON_CLOSE_HOUR = int(os.getenv('LONDON_CLOSE_HOUR', 21))
LONDON_CLOSE_MINUTE = int(os.getenv('LONDON_CLOSE_MINUTE', 30))
NY_OPEN_HOUR = int(os.getenv('NY_OPEN_HOUR', 18))
NY_OPEN_MINUTE = int(os.getenv('NY_OPEN_MINUTE', 30))
NY_CLOSE_HOUR = int(os.getenv('NY_CLOSE_HOUR', 1))
NY_CLOSE_MINUTE = int(os.getenv('NY_CLOSE_MINUTE', 30))

# Alert Settings
ALERT_COOLDOWN_MINUTES = int(os.getenv('ALERT_COOLDOWN_MINUTES', 30))
MAX_ALERTS_PER_HOUR = int(os.getenv('MAX_ALERTS_PER_HOUR', 3))

# Default monitored pair (EURUSD only)
DEFAULT_PAIRS = ['EUR/USD']
TARGET_PAIR = 'EUR/USD'

# Timeframes for analysis
TIMEFRAMES = {
    'M15': 'M15',
    'H1': 'H1',
    'H4': 'H4'
}

# SMC Strategy Parameters
MIN_CONFLUENCE_COUNT = 2  # Require at least 2 confluences for quality setups
MIN_ORDER_BLOCK_SIZE = 8  # pips
MIN_FVG_SIZE = 8  # pips
MIN_SUPPLY_DEMAND_SIZE = 10  # pips for supply/demand zones
LIQUIDITY_SWEEP_RANGE = 20  # pips
VOLUME_THRESHOLD = 1.3  # 30% above average for high volume
FAKEOUT_CONFIRMATION_CANDLES = 2  # Candles to confirm fakeout

# Risk:Reward Ratios
TP1_RR = 1.5
TP2_RR = 2.5
TP3_RR = 3.0

# Pip values (for EURUSD standard)
PIP_VALUE_MICRO = 0.10  # $0.10 per pip for 0.01 lot
PIP_VALUE_MINI = 1.0    # $1 per pip for 0.10 lot
PIP_VALUE_STANDARD = 10.0  # $10 per pip for 1.0 lot

# Validation
def validate_config():
    """Validate configuration settings"""
    errors = []

    if not TELEGRAM_BOT_TOKEN:
        errors.append("TELEGRAM_BOT_TOKEN is not set")

    if not TELEGRAM_CHAT_ID:
        errors.append("TELEGRAM_CHAT_ID is not set")

    if not TWELVE_DATA_API_KEY:
        errors.append("TWELVE_DATA_API_KEY is not set")

    if ACCOUNT_SIZE <= 0:
        errors.append("ACCOUNT_SIZE must be greater than 0")

    if RISK_PERCENT <= 0 or RISK_PERCENT > 5:
        errors.append("RISK_PERCENT must be between 0 and 5")

    if errors:
        raise ValueError("Configuration errors:\n" + "\n".join(errors))

    return True

# Print configuration on import (for debugging)
if __name__ == "__main__":
    print("Configuration loaded:")
    print(f"Account Size: ${ACCOUNT_SIZE}")
    print(f"Risk per Trade: {RISK_PERCENT}%")
    print(f"Min Setup Score: {MIN_SETUP_SCORE}/10")
    print(f"Target Pair: {TARGET_PAIR}")
    print(f"Scan Interval: {SCAN_INTERVAL_SECONDS}s ({1440//(SCAN_INTERVAL_SECONDS//60)} scans/day)")
    print(f"London Session: {LONDON_OPEN_HOUR}:{LONDON_OPEN_MINUTE:02d} - {LONDON_CLOSE_HOUR}:{LONDON_CLOSE_MINUTE:02d} IST")
    print(f"NY Session: {NY_OPEN_HOUR}:{NY_OPEN_MINUTE:02d} - {NY_CLOSE_HOUR}:{NY_CLOSE_MINUTE:02d} IST")
