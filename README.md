# 🤖 SMC Forex Trading Bot - Telegram Alert System

Automated 24/7 Smart Money Concepts (SMC) trading bot that monitors forex pairs and sends high-probability trade setups to your Telegram. **Works perfectly in India with MetaTrader 5!**

## 📋 Features

- ✅ **24/7 Automated Monitoring** - Runs continuously without manual intervention
- ✅ **SMC Strategy** - Order Blocks, Fair Value Gaps, Liquidity Sweeps
- ✅ **Telegram Alerts** - Real-time notifications for trade setups
- ✅ **Multi-Pair Support** - Monitor multiple forex pairs simultaneously
- ✅ **Session Filtering** - Only alerts during London/NY sessions (no spam)
- ✅ **Quality Scoring** - Only sends setups with score ≥ 7/10
- ✅ **Risk Management** - Auto-calculates position size and stop loss
- ✅ **Easy Control** - Telegram commands to add/remove pairs
- ✅ **India Compatible** - Uses MetaTrader 5 (not restricted in India!)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Telegram account
- MetaTrader 5 (free download)
- MT5 demo account (free, no credit card needed)

### Installation

1. **Download MetaTrader 5**
   ```
   Visit: https://www.metatrader5.com/en/download
   Install the application (free)
   ```

2. **Get MT5 Demo Account**
   - Open MT5 → File → Open an Account
   - Choose: ICMarkets-Demo (or XM, FXCM)
   - Fill form → Get Login, Password, Server
   - Save credentials!

3. **Install bot dependencies**
   ```bash
   cd bot_setup
   pip install -r requirements.txt
   ```

4. **Configure environment**
   - Copy `.env.example` to `.env`
   - Fill in your credentials (see Configuration section)

5. **Run the bot**
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration

### 1. Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow prompts to create bot
4. Copy the **Bot Token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Get your **Chat ID**:
   - Search for `@userinfobot` on Telegram
   - Start chat and it will send your Chat ID

### 2. Setup MetaTrader 5

**Getting Demo Account (Works in India!):**

1. **Download & Install MT5:**
   - Visit: https://www.metatrader5.com/en/download
   - Download Windows version
   - Install (it's free!)

2. **Create Demo Account:**
   - Open MT5 application
   - Click: File → Open an Account
   - Search for "ICMarkets" (recommended for India)
   - Select "ICMarkets-Demo"
   - Fill registration form:
     - Name: Your name
     - Email: Your email
     - Phone: Your phone number
     - Leverage: 1:500
     - Deposit: $10,000 (demo money)
   - Click Next
   - **Save the credentials:** Login, Password, Server

**Alternative Brokers for India:**
- **XM Global:** `XM Global-Demo`
- **FXCM:** `FXCM-Demo`
- **FBS:** `FBS-Demo`

### 3. Setup .env File

Create a `.env` file in the `bot_setup` folder:

```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# MetaTrader 5 Configuration
MT5_LOGIN=12345678
MT5_PASSWORD=YourPassword123
MT5_SERVER=ICMarkets-Demo
MT5_PATH=

# Trading Configuration
ACCOUNT_SIZE=10000
RISK_PERCENT=0.5
MIN_SETUP_SCORE=7

# Session Times (IST - Indian Standard Time)
LONDON_OPEN_HOUR=13
LONDON_OPEN_MINUTE=30
LONDON_CLOSE_HOUR=21
LONDON_CLOSE_MINUTE=30
NY_OPEN_HOUR=18
NY_OPEN_MINUTE=30
NY_CLOSE_HOUR=1
NY_CLOSE_MINUTE=30

# Alert Settings
ALERT_COOLDOWN_MINUTES=30
MAX_ALERTS_PER_HOUR=3
```

---

## 📱 Telegram Commands

Once bot is running, send these commands in Telegram:

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Start the bot and show welcome message | `/start` |
| `/add <pair>` | Add forex pair to monitoring | `/add AUDUSD` |
| `/remove <pair>` | Remove pair from monitoring | `/remove USDJPY` |
| `/list` | Show all monitored pairs | `/list` |
| `/status` | Show bot status and statistics | `/status` |
| `/help` | Show all commands | `/help` |

---

## 📊 How It Works

### 1. Market Analysis

The bot continuously analyzes forex pairs using SMC concepts:

- **Order Blocks**: Identifies institutional buying/selling zones
- **Fair Value Gaps**: Finds market inefficiencies/imbalances
- **Liquidity Sweeps**: Detects stop hunts and reversals
- **Market Structure**: Confirms bullish/bearish bias

### 2. Setup Scoring (0-10)

Each potential setup is scored based on:
- Confluence count (3 points max)
- Market structure clarity (2 points)
- Liquidity sweep quality (2 points)
- Volume confirmation (1 point)
- Session timing (1 point)
- Candlestick pattern (1 point)

**Only setups with score ≥ 7 trigger alerts**

### 3. Alert Generation

Alerts are sent when:
- ✅ Score ≥ 7/10
- ✅ During London or NY session
- ✅ Not sent alert for same pair in last 30 min
- ✅ Maximum 3 alerts per hour (all pairs)
- ✅ High volume confirmed

### 4. Alert Format

```
🚨 TRADE SETUP DETECTED 🚨

Pair: EURUSD
Direction: 🟢 LONG
Entry Zone: 1.15950 - 1.15980

💎 CONFLUENCES (3/3):
✅ Order Block: 1.15920-1.15980
✅ FVG: 1.15930-1.15970
✅ Liquidity Sweep: 1.15850

📊 TRADE SETUP:
Entry: 1.15965
Stop Loss: 1.15920 (45 pips)
TP1: 1.16033 (68 pips | 1:1.5)
TP2: 1.16078 (113 pips | 1:2.5)
TP3: 1.16100 (135 pips | 1:3.0)

💰 POSITION SIZE:
Lot Size: 0.11 lots
Risk: $50.00 (0.5%)

Setup Score: 9/10 ⭐⭐⭐
```

---

## 🔧 Customization

### Modify Monitored Pairs (Default)

Edit `config.py`:
```python
DEFAULT_PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD']
```

Or use Telegram commands:
```
/add EURJPY
/add AUDNZD
```

### Adjust Risk Settings

Edit `.env`:
```env
ACCOUNT_SIZE=10000  # Your demo account size
RISK_PERCENT=0.5    # Risk per trade (0.5% = $50 on $10k)
```

### Change Session Times

Edit `.env` to match your timezone:
```env
LONDON_OPEN_HOUR=13  # 1:30 PM IST
NY_OPEN_HOUR=18      # 6:30 PM IST
```

### Modify Alert Frequency

Edit `.env`:
```env
ALERT_COOLDOWN_MINUTES=30  # Min time between alerts per pair
MAX_ALERTS_PER_HOUR=3      # Max total alerts per hour
MIN_SETUP_SCORE=7          # Minimum score (7-10)
```

---

## 📁 Project Structure

```
bot_setup/
│
├── main.py                 # Main bot entry point
├── strategy.py             # SMC strategy implementation
├── telegram_handler.py     # Telegram bot commands
├── market_data.py          # MT5 API integration
├── analyzer.py             # Market analysis logic
├── config.py               # Configuration settings
├── utils.py                # Helper functions
│
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .env                    # Your actual credentials (create this)
│
├── README.md               # This file
└── QUICKSTART.md           # 5-minute setup guide
```

---

## 🐛 Troubleshooting

### Bot doesn't start

**Error:** `ModuleNotFoundError: No module named 'MetaTrader5'`

**Solution:**
```bash
pip install -r requirements.txt
```

---

### MT5 connection fails

**Error:** `MT5 initialize() failed`

**Check:**
1. MT5 is installed
2. MT5 application is RUNNING in background
3. You can open MT5 manually
4. Demo account is active

**Solution:**
- Open MT5 manually first
- Go to Tools → Options → Server
- Verify server name matches `.env` file
- Try logging in manually in MT5

---

### No alerts received

**Check:**
1. Bot is running: `python main.py` should show "Bot started"
2. Telegram chat ID is correct in `.env`
3. Current time is during London/NY session
4. Run `/status` command to see if monitoring is active
5. Lower `MIN_SETUP_SCORE` to 6 for testing

**Verify:**
```
python market_data.py
```
Should show: "✅ Connected to MT5" and fetch data

---

### Pair not found error

**Error:** `No data received for EURUSD`

**Solution:**
- Open MT5 manually
- Right-click in Market Watch → "Show All"
- Find the pair → Right-click → "Chart Window"
- This enables the symbol in MT5
- Restart bot

---

## 📈 Performance Tips

### For Best Results:

1. **Start during London Open** (1:30 PM IST) - Most setups occur
2. **Monitor 3-5 pairs** - Balance between coverage and quality
3. **Trust the scoring** - Score ≥ 8 = very high probability
4. **Use demo first** - Test for 1-2 weeks before live trading
5. **Keep MT5 running** - Bot needs MT5 connection

### Recommended for 24/7:

**VPS Providers in India:**
- Hostinger India ($3/month)
- DigitalOcean Bangalore ($5/month)
- AWS Mumbai ($3.50/month)

---

## 🛡️ Safety & Risk Management

### Built-in Safety Features:

- ✅ Maximum 0.5% risk per trade
- ✅ Auto-calculated position sizing
- ✅ Stop loss on every setup
- ✅ Multiple take profit levels (scaled exits)
- ✅ Session filtering (avoid low liquidity)
- ✅ Quality scoring (only high-probability setups)

### Important Notes:

⚠️ **This bot provides ALERTS, not auto-trading**
- You must manually execute trades
- Review each setup before entering
- Bot is a tool, not financial advice

⚠️ **Test on demo first**
- Run for 2-4 weeks on paper
- Verify alert quality
- Understand the strategy

⚠️ **Risk disclaimer**
- Trading forex involves risk
- Only trade with money you can afford to lose
- Past performance ≠ future results

---

## 🇮🇳 India-Specific Information

### Why MetaTrader 5?

✅ **Not Restricted in India**
- OANDA is restricted in India
- MT5 is fully legal and available
- Many brokers offer MT5 in India

✅ **Free Demo Accounts**
- No credit card required
- Unlimited practice
- Real market data

✅ **Better for Indian Traders**
- Local broker options
- INR deposit options (for live accounts later)
- Better customer support in India

### Recommended Brokers for Indians:

1. **ICMarkets** - Best spreads, very reliable
2. **XM Global** - Popular, good support
3. **FXCM** - Well-known brand
4. **FBS** - Easy signup

**All offer free demo accounts!**

### Tax Consideration:

- Forex trading income is taxable in India
- Keep records of all trades
- Consult a Chartered Accountant for tax filing
- Demo trading = no tax implications

---

## 🔄 Updates & Maintenance

### Keep Bot Updated:

```bash
git pull origin main  # If using git
pip install -r requirements.txt --upgrade
```

### Monitor Performance:

- Use `/status` command daily
- Track win rate of alerts
- Adjust `MIN_SETUP_SCORE` if needed (higher = fewer but better)

---

## 📞 Support

### Issues?

1. Check troubleshooting section above
2. Verify `.env` configuration
3. Test MT5 connection: `python market_data.py`
4. Check bot logs in terminal
5. Review `QUICKSTART.md` for setup steps

---

## 📜 License

This project is for educational purposes only. Not financial advice.

---

## 🎯 Next Steps

1. ✅ Install MetaTrader 5
2. ✅ Get demo account credentials
3. ✅ Install dependencies: `pip install -r requirements.txt`
4. ✅ Configure `.env` file
5. ✅ Test MT5 connection: `python market_data.py`
6. ✅ Run bot: `python main.py`
7. ✅ Send `/start` to your Telegram bot
8. ✅ Wait for alerts during London/NY sessions
9. ✅ Track performance for 1-2 weeks
10. ✅ Adjust settings as needed

---

**Happy Trading! 🚀**

*Remember: The bot finds setups. YOU make the final trading decision.*

---

## 💡 Quick Tips

**For Indian Traders:**
- Best times: 2:00 PM (London) and 7:00 PM (NY open)
- Use ICMarkets demo (works great in India)
- Keep MT5 running in background
- Test thoroughly before considering live

**For All Users:**
- Quality > Quantity (bot filters for you)
- Score 9-10 = extremely high probability
- Demo test minimum 2 weeks
- Track your win rate
- Adjust risk settings to your comfort level

---

**Ready to start?** Go to `QUICKSTART.md` for step-by-step setup! 📚
# trading-bot
