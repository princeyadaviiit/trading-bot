# SMC Forex Trading Bot - Telegram Edition

**Smart Money Concepts Analyzer for EUR/USD**

Fully automated forex trading signal bot with comprehensive SMC analysis and Telegram notifications.

---

## 🌟 Overview

This bot monitors **EUR/USD 24/7** using advanced Smart Money Concepts (SMC) analysis and sends high-quality trade setups directly to your Telegram. Built with professional-grade technical analysis including order blocks, supply/demand zones, liquidity analysis, and fakeout detection.

### Key Highlights
- 🎯 **Single Pair Focus**: EUR/USD only for precision analysis
- ⏱️ **3-Minute Intervals**: 480 scans per day (optimized for free API tier)
- 📱 **Telegram Alerts**: Instant notifications with complete trade details
- 🧠 **Comprehensive SMC**: All ICT concepts + supply/demand + fakeouts
- 🎲 **Smart Filtering**: Only sends signals with ≥5 pip TP and quality score ≥3/10
- 💰 **Auto Risk Management**: Position sizing based on account risk

---

## 📊 SMC Analysis Features

### Core Components
✅ **Order Blocks** - Last opposite candle before strong moves with volume confirmation  
✅ **Supply & Demand Zones** - Areas of Interest (AOI) with strength scoring  
✅ **Fair Value Gaps (FVG)** - 3-candle imbalance patterns with momentum detection  
✅ **Liquidity Pools** - Equal highs/lows + round number levels  
✅ **Liquidity Sweeps** - Stop hunt detection with clean/dirty classification  

### Advanced Patterns
✅ **Fakeout Detection** - False breakout identification with confirmation  
✅ **Break of Structure (BOS)** - Trend change confirmation signals  
✅ **Change of Character (ChoCH)** - Early reversal warning signals  
✅ **Premium/Discount Zones** - Optimal entry zone identification  
✅ **Market Structure Analysis** - HH/HL (bullish) and LH/LL (bearish) detection  

### Confirmation Filters
- Confirmation candle patterns (engulfing, hammer, shooting star)
- Volume analysis (30% above average threshold)
- Session tracking (London, NY, Asian)
- Confluence scoring (0-10 scale)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Telegram account
- Twelve Data API key (free tier: 800 calls/day)

### Installation

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Get Telegram Bot Token**
```
1. Open Telegram, search for @BotFather
2. Send /newbot command
3. Choose bot name and username
4. Copy the bot token provided
5. Get your Chat ID from @userinfobot (send /start)
```

**3. Get Twelve Data API Key**
```
1. Visit https://twelvedata.com/
2. Sign up for free account
3. Navigate to API section in dashboard
4. Copy your API key
5. Free tier: 800 calls/day (plenty for 480 scans)
```

**4. Configure Environment**

Edit `.env` file:
```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Twelve Data API Configuration
TWELVE_DATA_API_KEY=your_api_key_here  # ← ADD YOUR KEY HERE

# Trading Configuration
ACCOUNT_SIZE=1000
RISK_PERCENT=0.5
MIN_SETUP_SCORE=3
MIN_TP_PIPS=5.0
SCAN_INTERVAL_SECONDS=180
```

**5. Run the Bot**
```bash
python main.py
```

You should see:
```
🚀 SMC Trading Bot Started (Telegram)
📊 Target Pair: EUR/USD
⏰ Scan Interval: 3 minutes
🎯 Min Setup Score: 3/10
📍 Min TP for Auto-Send: 5.0 pips
💰 Risk per Trade: 0.5% ($5.00)
```

---

## 📱 Telegram Commands

### Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message with bot information |
| `/help` | Complete command list and features |
| `/analyze` | Analyze EUR/USD right now (on-demand) |
| `/status` | Bot statistics + last 4 analyses |

### Command Examples

**Check bot status:**
```
/status
```
Response includes:
- Current session (London/NY/Asian)
- Trading session status
- Total alerts sent
- Total scans completed
- Bot uptime
- Last 4 analysis results

**Analyze now:**
```
/analyze
```
Forces immediate EUR/USD analysis regardless of scan schedule.

---

## 📬 Alert Format

When a high-quality setup is detected, you receive:

```
🚨 TRADE SETUP DETECTED 🚨

Pair: EURUSD
Direction: 🟢 LONG
Entry Zone: 1.09450 - 1.09520

💎 CONFLUENCES (3/4):
✅ Order Block: 1.09450-1.09480
✅ FVG: 1.09460-1.09500
✅ Liquidity Sweep: 1.09440

📊 TRADE SETUP:
Entry: 1.09485
Stop Loss: 1.09425 (6 pips)
TP1: 1.09575 (9 pips | 1:1.5)
TP2: 1.09695 (21 pips | 1:2.5)
TP3: 1.09785 (30 pips | 1:3.0)

💰 POSITION SIZE:
Lot Size: 0.83 lots
Risk: $5.00 (0.5%)

📈 MARKET INFO:
Structure: Bullish (HH/HL)
Bias: Strong Bullish
Session: London-NY Overlap
Time: 18:45 IST

⚠️ CONFIRMATION STATUS:
✅ Confirmation Candle
✅ High Volume
✅ Correct Premium/Discount Zone

---
Setup Score: 8/10 ⭐⭐⭐⭐⭐⭐⭐⭐
```

**What you get:**
- Clear direction (LONG/SHORT with emoji)
- Entry zone and precise entry price
- Stop Loss with pip distance
- 3 Take Profit levels with R:R ratios
- Auto-calculated position size
- Risk amount based on your settings
- All detected confluences listed
- Market structure and bias
- Current session and time (IST)
- Confirmation status breakdown
- Overall setup quality score

---

## ⚙️ Configuration Guide

### Trading Settings

Edit `.env` file to customize:

| Setting | Default | Description |
|---------|---------|-------------|
| `ACCOUNT_SIZE` | 1000 | Your trading account size (USD) |
| `RISK_PERCENT` | 0.5 | Risk per trade percentage (0.5% = $5 per $1000) |
| `MIN_SETUP_SCORE` | 3 | Minimum setup score (3-10) to send alerts |
| `MIN_TP_PIPS` | 5.0 | Minimum TP distance required for auto-send |
| `SCAN_INTERVAL_SECONDS` | 180 | Time between scans (180 = 3 minutes) |
| `ALERT_COOLDOWN_MINUTES` | 30 | Minimum time between alerts for same pair |
| `MAX_ALERTS_PER_HOUR` | 3 | Maximum alerts allowed per hour |

### Optimization Tips

**More Signals (Lower Quality):**
```env
MIN_SETUP_SCORE=3
MIN_TP_PIPS=3.0
```

**Fewer Signals (Higher Quality):**
```env
MIN_SETUP_SCORE=7
MIN_TP_PIPS=10.0
```

**Balanced (Recommended):**
```env
MIN_SETUP_SCORE=5
MIN_TP_PIPS=5.0
```

### Session Times (IST)

| Session | Open | Close | Overlap |
|---------|------|-------|---------|
| London | 13:30 | 21:30 | - |
| NY | 18:30 | 01:30 | - |
| Overlap | 18:30 | 21:30 | London + NY |

**Note:** Bot scans 24/7 for analysis, session tracking provides context.

---

## 🔍 How the Bot Works

### Analysis Pipeline

**Every 3 minutes:**

1. **Fetch Data**
   - EUR/USD on M15, H1, H4 timeframes
   - ~3 API calls per scan
   - Cached for 60 seconds to optimize

2. **Market Structure**
   - Identify trend direction (bullish/bearish/neutral)
   - Detect Higher Highs/Higher Lows (HH/HL)
   - Detect Lower Highs/Lower Lows (LH/LL)
   - Check for Break of Structure (BOS)
   - Check for Change of Character (ChoCH)

3. **Find SMC Components**
   - Order blocks (last opposite candle before moves)
   - Supply zones (rejection areas)
   - Demand zones (bounce areas)
   - Fair value gaps (imbalances)
   - Liquidity pools (equal highs/lows + round numbers)

4. **Detect Patterns**
   - Liquidity sweeps (stop hunts with reversal)
   - Fakeouts (false breakouts with confirmation)
   - Confirmation candles (engulfing, hammers, etc.)
   - Volume spikes (30%+ above average)

5. **Calculate Confluence**
   - Requires minimum 2 confluences
   - Order block = 1 point
   - Supply/Demand zone = 1 point
   - Fair value gap = 1 point
   - Liquidity sweep = 1 point
   - Fakeout = 1 point (bonus)

6. **Score Setup (0-10)**
   - Confluence count (max 4 points)
   - Market structure strength (2 points)
   - Confirmation candle (1 point)
   - High volume (1 point)
   - Premium/discount zone (1 point)
   - BOS/Fakeout/ChoCH (1 point)

7. **Filter & Send**
   - Score must be ≥ MIN_SETUP_SCORE
   - TP distance must be ≥ MIN_TP_PIPS
   - Not in cooldown period
   - Below max alerts per hour
   - ✅ Auto-send to Telegram

---

## 📊 API Usage & Costs

### Twelve Data Free Tier

| Metric | Value |
|--------|-------|
| Calls per Day | 800 |
| Calls per Minute | Unlimited |
| Historical Data | ✅ Included |
| Real-time Data | ✅ Included |
| Forex Support | ✅ Full support |

### Bot Usage

| Metric | Value |
|--------|-------|
| Scan Interval | 3 minutes |
| Scans per Day | 480 |
| API Calls per Scan | ~3 (M15, H1, H4) |
| Total Daily Calls | ~480 |
| Free Tier Buffer | 320 calls spare |

**Verdict:** Free tier is more than enough! 📈

---

## 🛠️ Project Structure

```
bot_setup/
├── main.py                 # Main orchestrator, bot lifecycle
├── config.py              # Configuration loader, validation
├── telegram_handler.py    # Telegram bot commands, message handling
├── strategy.py            # Main strategy logic, confluence detection
├── analyzer.py            # SMC analysis engine (OB, FVG, SD, etc.)
├── market_data.py         # Twelve Data API integration
├── utils.py               # Helper functions (risk calc, formatting)
├── requirements.txt       # Python dependencies
├── .env                   # Your credentials (KEEP SECRET)
├── .env.example          # Example environment file
└── README.md             # This file
```

---

## 🐛 Troubleshooting

### Bot Won't Start

**Error: TELEGRAM_BOT_TOKEN is not set**
```bash
# Solution: Check .env file has bot token
TELEGRAM_BOT_TOKEN=your_actual_token_here
```

**Error: TWELVE_DATA_API_KEY is not set**
```bash
# Solution: Add your Twelve Data API key to .env
TWELVE_DATA_API_KEY=your_actual_key_here
```

**Error: Module not found**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### No Signals Received

**Check bot is running:**
```bash
# Terminal should show:
🔍 Scanning EUR/USD...
⏳ Next scan: 22:15:00 IST
```

**Check bot status via Telegram:**
```
/status
```
Verify:
- Scans completed is increasing
- No error messages in terminal

**Why no signals?**
- High-quality setups are rare (by design)
- Market may be ranging/consolidating
- Try `/analyze` for immediate check
- Consider lowering `MIN_SETUP_SCORE` to 3

### API Errors

**Error: 429 Too Many Requests**
```bash
# Exceeded API quota
# Solution: Wait for daily reset or upgrade plan
```

**Error: Invalid API Key**
```bash
# Solution: Verify API key is correct in .env
# Get new key from: https://twelvedata.com/account
```

---

## ⚠️ Important Warnings

### Trading Risks

⚠️ **This bot provides signals, NOT automated trading**
- You must manually review and enter trades
- Always verify setups before risking real money
- Use proper risk management (1-2% per trade max)
- Past performance does NOT guarantee future results

⚠️ **Risk Disclaimer**
- Forex trading involves substantial risk of loss
- Only trade with capital you can afford to lose
- This bot is for educational purposes
- No guarantee of profits
- Developer is not responsible for trading losses

### Security

⚠️ **Protect Your Credentials**
- NEVER commit `.env` file to git
- Keep your Telegram bot token private
- Don't share your Twelve Data API key
- Don't share screenshots containing tokens

---

## 📈 Performance Expectations

### Signal Frequency

Based on MIN_SETUP_SCORE setting:

| Score | Frequency | Quality |
|-------|-----------|---------|
| 3-4 | 2-5/day | Good |
| 5-6 | 1-3/day | Very Good |
| 7-8 | 0-2/day | Excellent |
| 9-10 | 0-1/week | Perfect |

**Note:** Market conditions greatly affect frequency. During ranging periods, expect fewer signals.

---

## 🎯 Final Notes

### Best Practices

1. **Start with demo account** - Test signals before going live
2. **Lower risk initially** - Use 0.25-0.5% per trade when starting
3. **Verify every setup** - Don't blindly follow bot signals
4. **Keep learning** - Understand WHY setups work
5. **Track results** - Journal your trades for improvement

### Success Tips

✅ Be patient - High-quality setups are rare  
✅ Trust the process - Don't chase every move  
✅ Manage risk - Never risk more than 1-2% per trade  
✅ Stay disciplined - Follow your trading plan  
✅ Keep learning - Study each setup the bot finds  

---

**Built with Smart Money Concepts | Powered by Twelve Data API | Telegram Integration**

*Happy Trading! 🚀📈*
