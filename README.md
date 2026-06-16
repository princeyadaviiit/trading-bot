# 🤖 SMC Forex Trading Bot - Discord Alert System

Automated 24/7 Smart Money Concepts (SMC) trading bot that monitors forex pairs and sends high-probability trade setups to your Discord channel. **Powered by MetaTrader 5 - No API limits!**

## 📋 Features

- ✅ **24/7 Automated Monitoring** - Runs continuously without manual intervention
- ✅ **SMC Strategy** - Order Blocks, Fair Value Gaps, Liquidity Sweeps
- ✅ **Discord Alerts** - Real-time notifications for trade setups
- ✅ **Multi-Pair Support** - Monitor multiple forex pairs simultaneously
- ✅ **Session Filtering** - Only alerts during London/NY sessions (no spam)
- ✅ **Quality Scoring** - Only sends setups with score ≥ 7/10
- ✅ **Risk Management** - Auto-calculates position size and stop loss
- ✅ **Easy Control** - Discord commands to add/remove pairs
- ✅ **Fast Scanning** - 60-second intervals with MT5 real-time data
- ✅ **No API Limits** - Direct MT5 connection, unlimited data access

---

## 🚀 Quick Start

### Prerequisites

- Windows OS (required for MT5)
- Python 3.8 or higher
- Discord account
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
   - Login and keep MT5 running

3. **Install bot dependencies**
   ```bash
   cd bot_setup
   pip install -r requirements.txt
   ```

4. **Configure environment**
   - Edit `.env` file
   - Add your Discord credentials (see Configuration section)

5. **Run the bot**
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration

### 1. Create Discord Bot

1. Visit **Discord Developer Portal**: https://discord.com/developers/applications
2. Click **"New Application"**
3. Name your bot (e.g., "SMC Trading Bot")
4. Go to **"Bot"** tab → Click **"Add Bot"**
5. Under **Token** section → Click **"Reset Token"** → Copy the token
6. Enable these **Privileged Gateway Intents**:
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT (optional)
7. Go to **"OAuth2"** → **"URL Generator"**
   - Select scopes: `bot`
   - Select permissions: `Send Messages`, `Read Messages/View Channels`
   - Copy the generated URL
8. Open URL in browser → Add bot to your Discord server

### 2. Get Discord Channel ID

1. Enable Developer Mode in Discord:
   - User Settings → Advanced → Enable Developer Mode
2. Right-click your channel → Copy ID
3. Save this Channel ID

### 3. Setup MetaTrader 5

**Getting Demo Account:**

1. **Download & Install MT5:**
   - Visit: https://www.metatrader5.com/en/download
   - Download Windows version
   - Install (it's free!)

2. **Create Demo Account:**
   - Open MT5 application
   - Click: File → Open an Account
   - Search for "ICMarkets" (recommended)
   - Select "ICMarkets-Demo"
   - Fill registration form:
     - Name: Your name
     - Email: Your email
     - Leverage: 1:500
     - Deposit: $10,000 (demo money)
   - Click Next
   - **Save the credentials** and login

3. **Keep MT5 Running:**
   - MT5 must be running for the bot to work
   - Login to your demo account
   - Minimize to system tray

**Alternative Brokers:**
- **XM Global:** `XM Global-Demo`
- **FXCM:** `FXCM-Demo`
- **FBS:** `FBS-Demo`

### 4. Setup .env File

Edit the `.env` file in the `bot_setup` folder:

```env
# Discord Configuration
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here

# Trading Configuration
ACCOUNT_SIZE=1000
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

## 📱 Discord Commands

Once bot is running, send these commands in Discord:

| Command | Description | Example |
|---------|-------------|---------|
| `!start` | Start the bot and show welcome message | `!start` |
| `!add <pair>` | Add forex pair to monitoring | `!add AUDUSD` |
| `!remove <pair>` | Remove pair from monitoring | `!remove USDJPY` |
| `!list` | Show all monitored pairs | `!list` |
| `!status` | Show bot status and statistics | `!status` |
| `!help` | Show all commands | `!help` |

---

## 📊 How It Works

### 1. Market Analysis

The bot scans markets every **60 seconds** using SMC concepts:

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
Risk: $5.00 (0.5%)

📈 MARKET INFO:
Structure: Bullish
Bias: Long
Session: London
Time: 14:30 IST

⚠️ CONFIRMATION NEEDED:
Wait for bullish candle close
Check volume increase
No news in next 1 hour

---
Setup Score: 9/10 ⭐⭐⭐⭐⭐⭐⭐⭐⭐
```

---

## 🔧 Customization

### Modify Monitored Pairs (Default)

Edit `config.py`:
```python
DEFAULT_PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY']
```

Or use Discord commands:
```
!add EURJPY
!add AUDNZD
!remove USDJPY
```

### Adjust Risk Settings

Edit `.env`:
```env
ACCOUNT_SIZE=1000   # Your demo account size
RISK_PERCENT=0.5    # Risk per trade (0.5% = $5 on $1k)
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
├── discord_handler.py      # Discord bot commands & alerts
├── market_data.py          # MT5 API integration
├── analyzer.py             # Market analysis logic
├── config.py               # Configuration settings
├── utils.py                # Helper functions
│
├── requirements.txt        # Python dependencies
├── .env                    # Your credentials
│
└── README.md               # This file
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
2. MT5 application is RUNNING
3. You're logged into a demo account
4. You can see live prices in MT5

**Solution:**
- Open MT5 manually first
- Login to your demo account
- Verify you see live price updates
- Then start the bot

---

### No alerts received

**Check:**
1. Bot is running: `python main.py` should show "Bot started"
2. Discord bot token and channel ID correct in `.env`
3. Bot has permission to send messages in the channel
4. Current time is during London/NY session
5. Run `!status` command to see if monitoring is active
6. Lower `MIN_SETUP_SCORE` to 6 for testing

**Verify:**
```bash
python market_data.py
```
Should show: "✅ MT5 initialized successfully" and fetch data

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

### Discord bot not responding

**Check:**
1. Bot is online in Discord (green status)
2. MESSAGE CONTENT INTENT is enabled in Developer Portal
3. Bot has Read/Send message permissions in channel
4. Commands start with `!` not `/`

---

## 📈 Performance Tips

### For Best Results:

1. **Start during London Open** (1:30 PM IST) - Most setups occur
2. **Monitor 2-3 pairs** - Focus on EURUSD, GBPUSD, USDCAD
3. **Trust the scoring** - Score ≥ 8 = very high probability
4. **Use demo first** - Test for 1-2 weeks before live trading
5. **Keep MT5 running** - Bot needs active MT5 connection
6. **Fast scanning** - 60-second intervals catch setups quickly

### System Requirements:

- **Windows 10/11** (MT5 requirement)
- **4GB RAM minimum**
- **Stable internet connection**
- **MT5 running in background**

---

## 🛡️ Safety & Risk Management

### Built-in Safety Features:

- ✅ Default 0.5% risk per trade
- ✅ Auto-calculated position sizing
- ✅ Stop loss on every setup
- ✅ Multiple take profit levels (scaled exits)
- ✅ Session filtering (avoid low liquidity)
- ✅ Quality scoring (only high-probability setups)
- ✅ Lot size clearly displayed in alerts

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

## 🎯 Default Configuration

### Default Monitored Pairs:
- EURUSD
- GBPUSD
- USDJPY

### Timeframes Analyzed:
- M15 (15-minute)
- H1 (1-hour)
- H4 (4-hour)

### Scan Interval:
- **60 seconds** (fast with MT5)

### Session Times (IST):
- London: 1:30 PM - 9:30 PM
- NY: 6:30 PM - 1:30 AM (next day)

### Risk Management:
- Account Size: $1,000 (demo)
- Risk per Trade: 0.5% ($5)
- Min Setup Score: 7/10

---

## 🔄 Updates & Maintenance

### Keep Bot Updated:

```bash
git pull origin main  # If using git
pip install -r requirements.txt --upgrade
```

### Monitor Performance:

- Use `!status` command daily
- Track win rate of alerts
- Adjust `MIN_SETUP_SCORE` if needed (higher = fewer but better)

---

## 📞 Support

### Issues?

1. Check troubleshooting section above
2. Verify `.env` configuration
3. Test MT5 connection: `python market_data.py`
4. Check bot logs in terminal
5. Verify Discord bot permissions

---

## 📜 License

This project is for educational purposes only. Not financial advice.

---

## 🎯 Next Steps

1. ✅ Install MetaTrader 5
2. ✅ Get demo account and login
3. ✅ Create Discord bot and get token
4. ✅ Get Discord channel ID
5. ✅ Install dependencies: `pip install -r requirements.txt`
6. ✅ Configure `.env` file
7. ✅ Test MT5 connection: `python market_data.py`
8. ✅ Run bot: `python main.py`
9. ✅ Send `!start` in Discord channel
10. ✅ Wait for alerts during London/NY sessions
11. ✅ Track performance for 1-2 weeks
12. ✅ Adjust settings as needed

---

**Happy Trading! 🚀**

*Remember: The bot finds setups. YOU make the final trading decision.*

---

## 💡 Quick Tips

**Setup:**
- Keep MT5 running and logged in
- Use ICMarkets demo (reliable)
- Enable MESSAGE CONTENT INTENT for Discord bot
- Start bot during London session for quick testing

**Usage:**
- Quality > Quantity (bot filters for you)
- Score 9-10 = extremely high probability
- Check lot size in each alert
- Demo test minimum 2 weeks
- Track your win rate
- Adjust risk settings to your comfort level

**Performance:**
- 60-second scans = fast setup detection
- No API limits with MT5
- Real-time tick data
- Reliable during high volatility

---

## 🔑 Key Features

✅ **Discord Integration** - Professional Discord bot with commands  
✅ **MT5 Direct Connection** - No API limits, real-time data  
✅ **Fast Scanning** - 60-second intervals  
✅ **Auto Position Sizing** - Risk management built-in  
✅ **Multi-Timeframe Analysis** - M15, H1, H4 confluence  
✅ **Session Filtering** - London & NY only  
✅ **Quality Scoring** - Score ≥ 7/10 only  
✅ **Lot Size Display** - Clear position sizing in alerts  

---

**Ready to start?** Follow the Next Steps above! 📚
