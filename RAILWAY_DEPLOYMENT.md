# SMC Forex Trading Bot - Railway Deployment Guide

## 🚂 Deploy to Railway

Follow these steps to deploy your bot to Railway cloud platform.

---

## 📋 Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app/)
- Your bot configured and tested locally
- All credentials ready (Telegram token, API key)

---

## 🚀 Deployment Steps

### Step 1: Push to GitHub

**1. Initialize Git (if not already done):**
```bash
cd bot_setup
git init
git add .
git commit -m "Initial commit - Telegram SMC Bot"
```

**2. Create GitHub Repository:**
- Go to https://github.com/new
- Name: `forex-smc-telegram-bot` (or your choice)
- Make it **Private** (recommended)
- Don't initialize with README (you have one)

**3. Push to GitHub:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy on Railway

**1. Sign Up for Railway:**
- Visit: https://railway.app/
- Sign up with GitHub account
- Verify email

**2. Create New Project:**
- Click **"New Project"**
- Select **"Deploy from GitHub repo"**
- Authorize Railway to access your GitHub
- Select your repository: `forex-smc-telegram-bot`

**3. Configure Environment Variables:**

Railway will start deploying. Click on your project, then:

- Click **"Variables"** tab
- Add these variables one by one:

```env
TELEGRAM_BOT_TOKEN=8711252539:AAGBgsK7xioimeNwmSDZObpLDHjhxX5Sa7s
TELEGRAM_CHAT_ID=5689513108
TWELVE_DATA_API_KEY=your_actual_api_key_here
ACCOUNT_SIZE=1000
RISK_PERCENT=0.5
MIN_SETUP_SCORE=3
MIN_TP_PIPS=5.0
SCAN_INTERVAL_SECONDS=180
LONDON_OPEN_HOUR=13
LONDON_OPEN_MINUTE=30
LONDON_CLOSE_HOUR=21
LONDON_CLOSE_MINUTE=30
NY_OPEN_HOUR=18
NY_OPEN_MINUTE=30
NY_CLOSE_HOUR=1
NY_CLOSE_MINUTE=30
ALERT_COOLDOWN_MINUTES=30
MAX_ALERTS_PER_HOUR=3
```

**Important:** Replace `your_actual_api_key_here` with your Twelve Data API key!

**4. Deploy:**
- Railway will auto-detect it's a Python app
- It will install dependencies from `requirements.txt`
- It will run `python main.py` (from Procfile)
- Wait 1-2 minutes for deployment

**5. Check Logs:**
- Click **"Deployments"** tab
- Click latest deployment
- View logs - should see:
```
🚀 SMC Trading Bot Started (Telegram)
📊 Target Pair: EUR/USD
⏰ Scan Interval: 3 minutes
```

---

## ✅ Verify Deployment

**1. Check Telegram:**
- You should receive: "🤖 SMC Trading Bot Started"
- Send `/start` command
- Send `/status` command to verify bot is running

**2. Check Railway Logs:**
- Should show scanning activity every 3 minutes
- No error messages

**3. Test Commands:**
```
/start   → Welcome message
/status  → Should show stats
/analyze → Manual analysis
/help    → Command list
```

---

## 📊 Railway Free Tier

**What You Get:**
- $5 free credits per month
- 500 hours execution time
- Enough for 24/7 bot operation
- No credit card required initially

**Usage Estimate:**
- This bot uses minimal resources
- ~$3-4 per month
- Well within free tier

---

## 🔧 Managing Your Deployment

### View Logs
```
Railway Dashboard → Your Project → Deployments → View Logs
```

### Update Environment Variables
```
Railway Dashboard → Your Project → Variables → Edit
```

### Redeploy After Code Changes
```bash
git add .
git commit -m "Update bot"
git push origin main
# Railway auto-deploys on push
```

### Restart Bot
```
Railway Dashboard → Your Project → Settings → Restart
```

---

## 🐛 Troubleshooting

### Bot Not Starting

**Check Logs for Errors:**
- Railway Dashboard → Deployments → View Logs
- Look for Python errors

**Common Issues:**

1. **Missing Environment Variables**
```
Error: TELEGRAM_BOT_TOKEN is not set
→ Add variable in Railway Dashboard
```

2. **Wrong Python Version**
```
Railway uses Python from runtime.txt
Should be: python-3.11.0
```

3. **Dependencies Not Installing**
```
Check requirements.txt is in root
Railway auto-installs from it
```

### Bot Stops After Few Minutes

**Check Railway Credit Balance:**
```
Dashboard → Account → Usage
If exceeded, upgrade or wait for monthly reset
```

**Check Logs for Crashes:**
```
Look for Python errors in deployment logs
Common: API rate limits, network timeouts
```

### No Telegram Messages

**Verify Environment Variables:**
```
Dashboard → Variables
Check TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are correct
```

**Check Bot is Running:**
```
Logs should show:
🔍 Scanning EUR/USD...
⏳ Next scan: XX:XX:XX IST
```

---

## 🔄 Updates & Maintenance

### Update Bot Code

**Local Changes:**
```bash
# Make changes to code
git add .
git commit -m "Description of changes"
git push origin main
```

Railway automatically redeploys on push!

### Update Dependencies

**Edit requirements.txt:**
```bash
# Add new package
echo "new-package==1.0.0" >> requirements.txt
git add requirements.txt
git commit -m "Add new dependency"
git push origin main
```

### Change Configuration

**Edit .env variables in Railway:**
```
Dashboard → Variables → Edit → Save
Bot restarts automatically with new config
```

---

## 📈 Monitoring

### Daily Checks

**Check Bot Status:**
- Send `/status` in Telegram
- Verify scans are increasing
- Check alerts sent count

**Check Railway Dashboard:**
- View deployment status (should be green)
- Check credit usage
- Review logs for errors

### Weekly Review

- Check Railway credit balance
- Review alert quality via `/status`
- Verify API quota is sufficient
- Check for any error patterns in logs

---

## 🔐 Security Best Practices

### Repository Security

**If using Public Repo:**
```bash
# Make sure .env is in .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Ignore .env file"
git push
```

**Never commit:**
- .env file with real credentials
- API keys in code
- Tokens in comments

### Railway Security

- Use Railway's environment variables (encrypted)
- Enable 2FA on Railway account
- Don't share deployment logs publicly (contain IPs)
- Regularly rotate API keys

---

## 💰 Cost Optimization

### Free Tier Tips

**Stay Within Limits:**
- Monitor credit usage weekly
- $5/month is usually enough
- Bot uses minimal resources

**If You Exceed:**
```
Option 1: Wait for monthly reset
Option 2: Upgrade to Hobby plan ($5/month)
Option 3: Optimize scan interval
```

**Optimization:**
```env
# Increase interval if needed
SCAN_INTERVAL_SECONDS=300  # 5 minutes instead of 3
# Reduces API calls to ~288/day
```

---

## 🎯 Production Checklist

Before going live, verify:

- [ ] All environment variables set correctly
- [ ] Telegram bot receives startup message
- [ ] `/status` command works
- [ ] `/analyze` command works
- [ ] Logs show successful scans
- [ ] No error messages in Railway logs
- [ ] Bot has been running for 1+ hour successfully
- [ ] Railway credit balance is sufficient
- [ ] Twelve Data API quota is sufficient
- [ ] GitHub repository is backed up

---

## 📞 Support Resources

### Railway Help
- Docs: https://docs.railway.app/
- Discord: https://discord.gg/railway
- Status: https://railway.statuspage.io/

### Bot Issues
- Check local README.md
- Review Railway logs
- Test locally first
- Check environment variables

---

## 🔄 Rollback

**If deployment fails:**

```bash
# Rollback to previous version
Railway Dashboard → Deployments → 
Select previous working deployment → 
Redeploy
```

**Or revert code:**
```bash
git log  # Find working commit
git revert <commit-hash>
git push origin main
```

---

## ✅ Post-Deployment

### First 24 Hours

1. **Monitor Actively:**
   - Check Railway logs every few hours
   - Verify Telegram alerts are working
   - Test all commands

2. **Document Issues:**
   - Note any errors in logs
   - Track API usage
   - Monitor credit consumption

3. **Fine-tune:**
   - Adjust MIN_SETUP_SCORE if needed
   - Optimize scan interval if API limits hit
   - Update alert thresholds based on results

### After 1 Week

- Review signal quality
- Check Railway costs
- Verify API quota sufficient
- Optimize configuration if needed
- Consider Hobby plan if exceeded free tier

---

**🎉 Congratulations! Your bot is now running 24/7 in the cloud!**

Monitor it regularly and adjust settings as needed. Happy trading! 📈
