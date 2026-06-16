"""
Configuration settings for SMC Trading Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord Configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', 0))

# Trading Configuration
ACCOUNT_SIZE = float(os.getenv('ACCOUNT_SIZE', 1000))
RISK_PERCENT = float(os.getenv('RISK_PERCENT', 0.5))
MIN_SETUP_SCORE = int(os.getenv('MIN_SETUP_SCORE', 7))

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

# Default monitored pairs (MT5 format)
DEFAULT_PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY']

# Timeframes for analysis
TIMEFRAMES = {
    'M15': 'M15',
    'H1': 'H1',
    'H4': 'H4'
}

# SMC Strategy Parameters
MIN_CONFLUENCE_COUNT = 2
MIN_ORDER_BLOCK_SIZE = 10  # pips
MIN_FVG_SIZE = 10  # pips
LIQUIDITY_SWEEP_RANGE = 20  # pips
VOLUME_THRESHOLD = 1.2  # 20% above average

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

    if not DISCORD_BOT_TOKEN:
        errors.append("DISCORD_BOT_TOKEN is not set")

    if DISCORD_CHANNEL_ID == 0:
        errors.append("DISCORD_CHANNEL_ID is not set")

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
    print(f"Default Pairs: {DEFAULT_PAIRS}")
    print(f"London Session: {LONDON_OPEN_HOUR}:{LONDON_OPEN_MINUTE:02d} - {LONDON_CLOSE_HOUR}:{LONDON_CLOSE_MINUTE:02d} IST")
    print(f"NY Session: {NY_OPEN_HOUR}:{NY_OPEN_MINUTE:02d} - {NY_CLOSE_HOUR}:{NY_CLOSE_MINUTE:02d} IST")
