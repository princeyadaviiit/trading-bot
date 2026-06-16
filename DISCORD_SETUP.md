# 🎮 Discord Bot Setup Guide - Complete Instructions

## 🚀 Quick Overview

Your SMC Trading Bot has been converted to Discord! Discord is likely **not blocked** on your network, so this should work perfectly.

---

## 📋 Step-by-Step Setup (10 Minutes)

### Step 1: Create Discord Server (2 minutes)

**If you don't have a server yet:**

1. Open Discord (desktop app or browser)
2. Click the **"+"** button on left sidebar
3. Select **"Create My Own"**
4. Choose **"For me and my friends"**
5. Name it: **"Trading Alerts"** (or any name)
6. Click **"Create"**

✅ You now have your own Discord server!

---

### Step 2: Create Discord Bot (5 minutes)

1. **Go to Discord Developer Portal:**
   - Visit: https://discord.com/developers/applications
   - Click **"New Application"**
   - Name: **"SMC Trading Bot"**
   - Click **"Create"**

2. **Get Bot Token:**
   - Click **"Bot"** tab on left sidebar
   - Click **"Reset Token"** (or "Add Bot" if new)
   - Click **"Yes, do it!"**
   - Click **"Copy"** to copy the token
   - **Save this token!** (you'll need it for .env file)

3. **Enable Bot Permissions:**
   - Scroll down to **"Privileged Gateway Intents"**
   - Enable **"MESSAGE CONTENT INTENT"** ✅
   - Enable **"SERVER MEMBERS INTENT"** ✅
   - Click **"Save Changes"**

4. **Generate Bot Invite Link:**
   - Click **"OAuth2"** tab on left
   - Click **"URL Generator"**
   - In **SCOPES**, check:
     - ✅ `bot`
   - In **BOT PERMISSIONS**, check:
     - ✅ `Send Messages`
     - ✅ `Read Message History`
     - ✅ `Use Slash Commands`
   - Copy the **Generated URL** at bottom

5. **Invite Bot to Your Server:**
   - Paste the URL in browser
   - Select your server from dropdown
   - Click **"Authorize"**
   - Complete captcha
   - ✅ Bot is now in your server!

---

### Step 3: Get Channel ID (2 minutes)

1. **Enable Developer Mode in Discord:**
   - Open Discord Settings (gear icon)
   - Go to **"Advanced"**
   - Enable **"Developer Mode"** ✅
   - Close settings

2. **Get Channel ID:**
   - Right-click on the channel where you want alerts (e.g., #general)
   - Click **"Copy Channel ID"**
   - **Save this number!** (you'll need it for .env file)

---

### Step 4: Configure .env File (1 minute)

Open `D:\claude\forex\bot_setup\.env` and fill in:

```env
# Discord Configuration
DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
DISCORD_CHANNEL_ID=YOUR_CHANNEL_ID_HERE

# Rest is already filled ✅
```

**Example:**
```env
DISCORD_BOT_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.AbCdEf.GhIjKlMnOpQrStUvWxYz
DISCORD_CHANNEL_ID=987654321098765432
```

---

### Step 5: Install Dependencies

```bash
cd bot_setup
pip install -r requirements.txt
```

This installs `discord.py` (Discord library) instead of `python-telegram-bot`.

---

### Step 6: Run the Bot

```bash
python main.py
```

**Expected output:**
```
🤖 Initializing SMC Trading Bot (Discord)...
✅ Configuration validated
✅ Discord bot logged in as SMC Trading Bot#1234
✅ Connected to channel: general
🚀 SMC Trading Bot Started (Discord)
📊 Monitoring: 3 pairs
```

---

### Step 7: Test Commands in Discord

Go to your Discord server and type:

```
!start
```

Bot should respond with welcome message! ✅

---

## 📱 Discord Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!start` | Show welcome message | `!start` |
| `!help` | Show all commands | `!help` |
| `!list` | Show monitored pairs | `!list` |
| `!add <pair>` | Add forex pair | `!add AUDUSD` |
| `!remove <pair>` | Remove pair | `!remove USDJPY` |
| `!status` | Show bot statistics | `!status` |

---

## 📊 Alert Example

When a setup is found, you'll receive Discord messages like:

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

## 🐛 Troubleshooting

### Issue 1: "Bot Token is invalid"

**Solution:**
- Go back to Discord Developer Portal
- Bot tab → Reset Token
- Copy new token
- Update .env file
- Restart bot

---

### Issue 2: Bot doesn't respond to commands

**Check:**
1. Bot is online in Discord (green dot)
2. Bot has permissions to read/send messages
3. You're in the correct channel
4. Commands start with `!` (exclamation mark)

**Solution:**
- Right-click bot in member list
- Check permissions
- Make sure "Read Messages" and "Send Messages" are enabled

---

### Issue 3: "Channel ID not found"

**Solution:**
1. Make sure Developer Mode is enabled
2. Right-click correct channel
3. Copy Channel ID (should be 17-19 digits)
4. Update DISCORD_CHANNEL_ID in .env
5. Restart bot

---

### Issue 4: Bot connects but no alerts

**Normal!** Alerts only come during:
- London session: 1:30 PM - 9:30 PM IST
- NY session: 6:30 PM - 1:30 AM IST
- When high-quality setups are found (score ≥ 7)

Type `!status` to check if monitoring is active.

---

## ✅ Advantages of Discord Over Telegram

| Feature | Discord | Telegram |
|---------|---------|----------|
| **Blocked in India?** | ❌ No | ✅ Yes (your issue) |
| **Network Access** | ✅ Works | ❌ Blocked |
| **Free** | ✅ Yes | ✅ Yes |
| **Desktop App** | ✅ Yes | ✅ Yes |
| **Mobile App** | ✅ Yes | ✅ Yes |
| **Rich Formatting** | ✅ Better | ✅ Good |
| **No VPN Needed** | ✅ Yes | ❌ Need VPN |

---

## 🎯 What's Different?

### Commands Changed:
- **Telegram:** `/start` → **Discord:** `!start`
- **Telegram:** `/add EURUSD` → **Discord:** `!add EURUSD`
- **Telegram:** `/list` → **Discord:** `!list`

### Setup Changed:
- **Telegram:** @BotFather → **Discord:** Developer Portal
- **Telegram:** Chat ID → **Discord:** Channel ID

### Everything Else Same:
- ✅ Same SMC strategy
- ✅ Same MT5 connection
- ✅ Same alert quality
- ✅ Same risk management
- ✅ Same monitoring logic

---

## 🚀 Quick Start Checklist

- [ ] Discord server created
- [ ] Bot created in Developer Portal
- [ ] Bot token copied
- [ ] Channel ID copied
- [ ] .env file updated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] MT5 running in background
- [ ] Bot started: `python main.py`
- [ ] Tested command: `!start`
- [ ] Bot responded ✅

---

## 💡 Pro Tips

1. **Create Dedicated Channel:**
   - Create `#trading-alerts` channel
   - Bot sends alerts there only
   - Keep it organized

2. **Mobile Notifications:**
   - Enable notifications for that channel
   - Get instant alerts on phone

3. **Multiple Pairs:**
   - Use `!add` to add more pairs
   - Use `!remove` to remove noisy pairs

4. **Check Status:**
   - Type `!status` daily
   - See alerts sent, uptime, session

5. **24/7 Operation:**
   - Run on VPS for true 24/7
   - Or keep computer running

---

## 🎓 Understanding Bot Behavior

### During London/NY Sessions:
```
Bot scans every 60 seconds
Analyzes all pairs
Sends alerts to Discord channel
Shows "🟢 Active" status
```

### Outside Trading Hours:
```
Bot keeps running
Waits for next session
No scanning (saves resources)
Shows "🟡 Standby" status
```

---

## 📞 Need Help?

### Common Questions:

**Q: Bot is online but no alerts?**
A: Normal! Setups are rare. Check `!status` to see if monitoring is active.

**Q: Can I use both Discord and Telegram?**
A: Not with current setup. Choose one (Discord works better for you).

**Q: How to run 24/7?**
A: Use VPS or keep computer running with MT5 + bot.

**Q: How to change alert frequency?**
A: Edit `.env` file: `MIN_SETUP_SCORE=8` (higher = fewer alerts)

---

## 🎉 You're Ready!

Your bot is now using Discord instead of Telegram. This solves your network block issue since Discord isn't blocked.

**Next Steps:**
1. Complete setup above
2. Run bot
3. Test with `!start`
4. Wait for first alert during London/NY session
5. Track performance!

---

**Discord works where Telegram doesn't. Problem solved! 🚀**
