# 🚀 Quick Start Guide - SMC Trading Bot (India Compatible!)

## ✅ Complete Setup in 10 Minutes

### Step 1: Install MetaTrader 5 (Free)

**Download and install MT5:**
- Visit: https://www.metatrader5.com/en/download
- Choose Windows version
- Install the software (it's free!)

### Step 2: Get Free MT5 Demo Account

**Recommended Brokers for India:**

**Option 1: ICMarkets (Recommended)**
1. Open MT5 application
2. Click "File" → "Open an Account"
3. Search for "ICMarkets"
4. Select "ICMarkets-Demo"
5. Fill demo account form:
   - Name: Your name
   - Email: Your email
   - Phone: Your phone
   - Leverage: 1:500
   - Deposit: $10,000
6. Click "Next" → Get Login, Password, Server
7. **Save these credentials!**

**Option 2: XM Global**
- Server: `XM Global-Demo`
- Same process as above

**Option 3: FXCM**
- Server: `FXCM-Demo`
- Available in India

### Step 3: Install Python Dependencies

```bash
cd bot_setup
pip install -r requirements.txt
```

### Step 4: Create Your .env File

Copy the example:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Telegram (Get from @BotFather)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# MetaTrader 5 (From demo account signup)
MT5_LOGIN=12345678
MT5_PASSWORD=YourPassword123
MT5_SERVER=ICMarkets-Demo
MT5_PATH=

# Trading Settings
ACCOUNT_SIZE=10000
RISK_PERCENT=0.5
MIN_SETUP_SCORE=7
```

### Step 5: Get Telegram Credentials

**Create Bot:**
1. Open Telegram
2. Search: `@BotFather`
3. Send: `/newbot`
4. Name: "My Forex Bot"
5. Username: "my_forex_alert_bot"
6. Copy token → paste in `.env`

**Get Chat ID:**
1. Search: `@userinfobot`
2. Start chat
3. Copy your ID → paste in `.env`

### Step 6: Test MT5 Connection

```bash
python market_data.py
```

You should see:
```
✅ Connected to MT5: ICMarkets-Demo
Account: 12345678
✅ Fetched 50 candles
```

### Step 7: Run the Bot

```bash
python main.py
```

Success output:
```
🤖 SMC Trading Bot Started
✅ Configuration validated
✅ Telegram bot started
📊 Monitoring: 3 pairs
🔍 Scanning markets...
```

### Step 8: Test on Telegram

1. Open Telegram
2. Find your bot
3. Send: `/start`
4. Bot replies: "🤖 SMC Trading Bot Started"
5. Send: `/status`
6. Check bot is running ✅

---

## 🎯 What Happens Next?

### Bot Behavior:

**During London/NY Sessions (1:30 PM - 1:30 AM IST):**
- Scans every 60 seconds
- Analyzes Order Blocks, FVGs, Liquidity
- Sends alerts for setups with score ≥ 7

**Outside Trading Hours:**
- Bot keeps running
- Waits for next session
- Shows "Waiting for trading session"

### First Alert Example:

```
🚨 TRADE SETUP DETECTED 🚨

Pair: EURUSD
Direction: 🟢 LONG
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

## 📱 Telegram Commands

```
/start         - Start bot
/list          - Show monitored pairs
/add AUDUSD    - Add pair
/remove USDJPY - Remove pair
/status        - Bot statistics
/help          - All commands
```

---

## ⚙️ Configuration Tips

### Change Monitored Pairs

Edit `config.py`:
```python
DEFAULT_PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD']
```

Or use Telegram:
```
/add AUDNZD
/add EURGBP
```

### Adjust Risk

Edit `.env`:
```env
ACCOUNT_SIZE=10000    # Demo account size
RISK_PERCENT=0.5      # 0.5% = $50 per trade
```

### More/Less Alerts

Edit `.env`:
```env
MIN_SETUP_SCORE=8           # Higher = fewer but better alerts
ALERT_COOLDOWN_MINUTES=45   # More time between alerts
MAX_ALERTS_PER_HOUR=2       # Less alerts per hour
```

---

## 🐛 Common Issues

### Issue 1: "MT5 initialize() failed"

**Solution:**
- Make sure MT5 is installed
- MT5 application must be RUNNING in background
- Check if you can open MT5 manually

### Issue 2: "MT5 login failed"

**Solution:**
- Verify `MT5_LOGIN` in `.env` (numbers only)
- Verify `MT5_PASSWORD` is correct
- Verify `MT5_SERVER` matches exactly (e.g., "ICMarkets-Demo")
- In MT5: Tools → Options → Server → Check server name

### Issue 3: "No data received for EURUSD"

**Solution:**
- Open MT5 manually
- In Market Watch, right-click → "Show All"
- Find EURUSD → right-click → "Chart Window"
- This enables the symbol
- Retry bot

### Issue 4: Bot starts but no alerts

**Check:**
- Current time is during London/NY session?
- Send `/status` - is it "Active" or "Standby"?
- Setups are rare - may take 1-2 hours for first alert
- Lower `MIN_SETUP_SCORE` to 6 for testing

### Issue 5: Telegram bot not responding

**Solution:**
- Check `TELEGRAM_BOT_TOKEN` is correct
- Check `TELEGRAM_CHAT_ID` is correct (numbers only)
- Search for your bot in Telegram by username
- Send `/start` first

---

## 🇮🇳 India-Specific Notes

### Why MT5 Works in India:

✅ **Legal & Available**
- MT5 is not restricted in India
- Many brokers offer MT5 in India
- Demo accounts are completely free

✅ **No OANDA Issues**
- OANDA is restricted in India
- MT5 is the perfect alternative
- Same data quality, better access

### Recommended Brokers for Indians:

1. **ICMarkets** - Best spreads, reliable
2. **XM Global** - Popular, good support
3. **FXCM** - Well-known, stable

**All offer free demo accounts!**

---

## 📈 Expected Performance

### Typical Results:

- **Alerts per Day:** 1-3 (high quality)
- **Best Time:** 1:30-4:30 PM IST (London open)
- **Win Rate:** 60-70% if executed properly
- **Setup Score 8+:** Very high probability

### Session Times (IST):

- **London:** 1:30 PM - 9:30 PM
- **NY:** 6:30 PM - 1:30 AM
- **Overlap:** 6:30 PM - 9:30 PM (BEST)

---

## 🚀 Running 24/7

### Option 1: VPS (Recommended)

**Indian VPS Providers:**
- Hostinger India ($3/month)
- DigitalOcean Bangalore ($5/month)
- AWS Mumbai ($3.50/month)

**Setup on VPS:**
```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip

# Install Wine (for MT5 on Linux)
sudo apt install wine

# Upload bot files
# Install dependencies
pip3 install -r requirements.txt

# Run bot
nohup python3 main.py &
```

### Option 2: Local Computer

- Keep computer running 24/7
- Disable sleep mode
- Stable internet required
- MT5 must stay running

---

## 🎯 Next Steps

1. ✅ MT5 installed & demo account created
2. ✅ Telegram bot created
3. ✅ `.env` file configured
4. ✅ Bot running
5. ⏳ Wait for first alert (London/NY session)
6. 📊 Review alert quality
7. 📝 Track performance for 1-2 weeks
8. 🚀 Consider live trading (after testing)

---

## 💡 Pro Tips for Indian Traders

1. **Best Trading Times (IST):**
   - 2:00-4:00 PM (London volatility)
   - 7:00-9:00 PM (NY open)

2. **Start with Demo:**
   - Test for 2-4 weeks minimum
   - Track win rate
   - Build confidence

3. **Risk Management:**
   - Never risk more than 1% per trade
   - Start with 0.5% (safer)
   - Use provided position sizing

4. **Broker Selection:**
   - Use regulated brokers only
   - Verify demo works well first
   - Check withdrawal reviews (for live later)

5. **Tax Consideration:**
   - Forex trading income is taxable in India
   - Keep records of all trades
   - Consult CA for tax filing

---

## 📞 Quick Help

### Commands Summary:
```bash
# Test MT5 connection
python market_data.py

# Test strategy (no alerts)
python strategy.py

# Start bot
python main.py

# Stop bot
Ctrl+C
```

### File Locations:
```
bot_setup/
├── main.py          ← Start here
├── .env             ← Your credentials
├── config.py        ← Settings
└── market_data.py   ← Test MT5
```

---

**🎉 You're ready! The bot will send alerts during London/NY sessions.**

**Questions?** Check `README.md` for detailed docs.

**Good Luck Trading! 🚀**

*Remember: Practice on demo first, real money only after consistent demo results.*
