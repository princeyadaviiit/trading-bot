# 🎯 MT5 Migration Complete - India Compatible!

## ✅ What Was Changed

Your bot has been successfully updated from OANDA (restricted in India) to **MetaTrader 5** (works perfectly in India).

---

## 📝 Files Updated

### 1. **requirements.txt**
- ❌ Removed: `oandapyV20`
- ✅ Added: `MetaTrader5==5.0.45`

### 2. **config.py**
- ❌ Removed: OANDA credentials
- ✅ Added: MT5 login, password, server settings
- ✅ Updated: Default pairs format (EURUSD instead of EUR_USD)

### 3. **market_data.py**
- ✅ Completely rewritten for MT5
- ✅ Uses `MetaTrader5` library
- ✅ Connects to MT5 terminal running on your computer
- ✅ Fetches real-time forex data

### 4. **telegram_handler.py**
- ✅ Updated pair format handling (EURUSD not EUR_USD)
- ✅ Updated validation for MT5 format
- ✅ Cleaner pair display in commands

### 5. **utils.py**
- ✅ Updated `validate_pair()` for MT5 format
- ✅ Changed conversion functions for MT5
- ✅ Removed underscore requirements

### 6. **.env.example**
- ✅ Replaced OANDA settings with MT5 settings
- ✅ Added MT5_LOGIN, MT5_PASSWORD, MT5_SERVER

### 7. **README.md**
- ✅ Complete rewrite with MT5 setup instructions
- ✅ India-specific broker recommendations
- ✅ MT5 troubleshooting section

### 8. **QUICKSTART.md**
- ✅ Step-by-step MT5 setup guide
- ✅ Indian broker recommendations
- ✅ Demo account signup process

---

## 🚀 Quick Setup (For India)

### Step 1: Install MetaTrader 5
```
Download: https://www.metatrader5.com/en/download
Install the application (it's free!)
```

### Step 2: Get Free Demo Account

**Recommended: ICMarkets (Works in India)**

1. Open MT5 application
2. File → Open an Account
3. Search: "ICMarkets"
4. Select: "ICMarkets-Demo"
5. Fill form → Get credentials
6. **Save:** Login, Password, Server

### Step 3: Update Your .env File

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# MetaTrader 5 (from demo signup)
MT5_LOGIN=12345678
MT5_PASSWORD=YourPassword123
MT5_SERVER=ICMarkets-Demo
MT5_PATH=

# Trading
ACCOUNT_SIZE=10000
RISK_PERCENT=0.5
```

### Step 4: Install Dependencies

```bash
cd bot_setup
pip install -r requirements.txt
```

### Step 5: Test MT5 Connection

```bash
python market_data.py
```

**Expected output:**
```
✅ Connected to MT5: ICMarkets-Demo
Account: 12345678
✅ Fetched 50 candles
```

### Step 6: Run Bot

```bash
python main.py
```

**Expected output:**
```
🤖 SMC Trading Bot Started
✅ Configuration validated
✅ Telegram bot started
📊 Monitoring: 3 pairs
```

---

## 🔍 Key Differences from OANDA

| Feature | OANDA (Old) | MT5 (New) |
|---------|-------------|-----------|
| **Availability in India** | ❌ Restricted | ✅ Available |
| **Pair Format** | EUR_USD | EURUSD |
| **Connection** | Cloud API | Local terminal |
| **Cost** | Paid API | Free |
| **Demo Account** | Requires signup | Free unlimited |
| **Installation** | Python only | Python + MT5 app |

---

## ⚠️ Important Notes

### Before Running:

1. **MT5 Must Be Running**
   - The MT5 application must be open in background
   - Bot connects to local MT5 terminal
   - Can't work if MT5 is closed

2. **Enable Symbols**
   - Open MT5 → Market Watch
   - Right-click → "Show All"
   - Find your pairs → Enable them
   - Or open chart for each pair once

3. **Internet Connection**
   - MT5 needs internet to get live data
   - Bot needs internet for Telegram
   - Stable connection recommended

---

## 🧪 Testing Checklist

Run these tests to verify everything works:

### Test 1: MT5 Connection
```bash
python market_data.py
```
✅ Should show: "Connected to MT5"
✅ Should fetch EURUSD data

### Test 2: Configuration
```bash
python config.py
```
✅ Should show: "Configuration loaded"
✅ No errors about missing variables

### Test 3: Bot Startup
```bash
python main.py
```
✅ Should show: "Bot Started"
✅ Should show: "Telegram bot started"
✅ No connection errors

### Test 4: Telegram Commands
Send to your bot:
```
/start
/list
/status
```
✅ Bot should respond to all commands
✅ /status should show monitoring info

---

## 🐛 Common Issues & Solutions

### Issue 1: "MT5 initialize() failed"

**Cause:** MT5 not installed or not running

**Solution:**
```
1. Download MT5 from metatrader5.com
2. Install it
3. Open the application
4. Keep it running
5. Retry bot
```

### Issue 2: "MT5 login failed"

**Cause:** Wrong credentials in .env

**Solution:**
```
1. Open MT5
2. Go to: Tools → Options → Server
3. Check login number (MT5_LOGIN)
4. Verify server name (MT5_SERVER)
5. Update .env file
6. Retry
```

### Issue 3: "No data received for EURUSD"

**Cause:** Symbol not enabled in MT5

**Solution:**
```
1. Open MT5
2. View → Market Watch (or Ctrl+M)
3. Right-click → Show All
4. Find EURUSD
5. Right-click → Chart Window
6. Retry bot
```

### Issue 4: "ModuleNotFoundError: MetaTrader5"

**Cause:** MT5 library not installed

**Solution:**
```bash
pip install MetaTrader5
# or
pip install -r requirements.txt
```

---

## 🇮🇳 Why This Works in India

### Legal & Available:
- ✅ MT5 is **not restricted** in India
- ✅ Many international brokers offer MT5
- ✅ Demo accounts are **completely free**
- ✅ No credit card needed
- ✅ Unlimited practice

### Better Than OANDA:
- ✅ No API restrictions
- ✅ Free unlimited data
- ✅ More broker choices
- ✅ Better for Indian traders

### Recommended Indian-Friendly Brokers:
1. **ICMarkets** - Best choice, reliable
2. **XM Global** - Popular worldwide
3. **FXCM** - Well-known brand
4. **FBS** - Easy signup

---

## 📊 Expected Bot Behavior

### During London/NY Sessions:

```
🔍 Scanning markets... [London Session]
📊 Found 1 setup(s)
✅ Alert sent for EURUSD
⏳ Next scan: 14:35:00 (London)
```

### Outside Trading Hours:

```
💤 Waiting for trading session... (Currently: Asian/Off-Hours)
⏳ Next scan: 09:15:00 (Asian)
```

### When Setup Found:

```
🚨 TRADE SETUP DETECTED 🚨

Pair: EURUSD
Direction: 🟢 LONG
Entry: 1.15965
Stop Loss: 1.15920 (45 pips)
TP1: 1.16033 (68 pips | 1:1.5)
TP2: 1.16078 (113 pips | 1:2.5)
TP3: 1.16100 (135 pips | 1:3.0)

Setup Score: 9/10 ⭐⭐⭐
```

---

## 🎯 Next Steps

1. ✅ Download & Install MT5
2. ✅ Create demo account (ICMarkets recommended)
3. ✅ Update .env with MT5 credentials
4. ✅ Test: `python market_data.py`
5. ✅ Run: `python main.py`
6. ✅ Test Telegram: Send `/start`
7. ✅ Wait for first alert (London/NY session)
8. ✅ Track performance for 1-2 weeks

---

## 📚 Full Documentation

- **Quick Setup:** `QUICKSTART.md` (10-minute guide)
- **Full Docs:** `README.md` (comprehensive)
- **Strategy:** `../strategy.md` (SMC explanation)
- **Config:** `.env.example` (all settings)

---

## ✅ Summary

Your bot is now **India-compatible** with MetaTrader 5!

**Key Benefits:**
- ✅ Works in India (no restrictions)
- ✅ Free demo accounts
- ✅ Real-time market data
- ✅ Professional platform
- ✅ Same SMC strategy
- ✅ Same alert quality

**What Changed:**
- Data source: OANDA → MT5
- Connection: Cloud API → Local terminal
- Pair format: EUR_USD → EURUSD
- Requirement: MT5 installed + running

**Ready to trade!** 🚀

Follow `QUICKSTART.md` for step-by-step setup.
