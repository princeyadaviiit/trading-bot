"""
Telegram Bot Handler
Manages Telegram commands and sends alerts
"""
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)
import config
from utils import format_telegram_message, get_ist_time
from typing import List, Dict
from datetime import datetime
from collections import deque

class TelegramHandler:
    """Telegram bot command handler"""

    def __init__(self):
        """Initialize Telegram bot"""
        self.is_running = False
        self.stats = {
            'alerts_sent': 0,
            'uptime_start': None,
            'scans_completed': 0
        }
        self.analysis_history = deque(maxlen=4)  # Store last 4 analyses
        self.strategy = None  # Will be set by main bot

    def add_analysis_to_history(self, analysis_result: Dict):
        """Add analysis result to history"""
        self.analysis_history.append({
            'time': get_ist_time(),
            'result': analysis_result
        })

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = f"""
🤖 **SMC Forex Trading Bot**

Welcome! I monitor **EUR/USD** 24/7 and send you high-probability trade setups based on Smart Money Concepts.

📊 **SMC Features:**
✅ Order Blocks & Fair Value Gaps
✅ Supply & Demand Zones (AOI)
✅ Liquidity Sweep Detection
✅ Fakeout Pattern Detection
✅ Break of Structure (BOS)
✅ Change of Character (ChoCH)

📱 **Commands:**
/analyze - Analyze EUR/USD now
/status - Bot status & last 4 analyses
/help - Show all commands

⚙️ **Auto-Alerts:**
• Scans every {config.SCAN_INTERVAL_SECONDS // 60} minutes
• Only sends signals with TP ≥ {config.MIN_TP_PIPS} pips
• Min setup score: {config.MIN_SETUP_SCORE}/10

🎯 **Target Pair:** EUR/USD

**Bot is ready!** Waiting for high-quality setups.
"""

        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = f"""
📖 **Bot Commands & Features**

**Commands:**
`/start` - Welcome message & bot info
`/analyze` - Analyze EUR/USD right now
`/status` - Bot statistics & last 4 analyses
`/help` - Show this help message

**Auto-Alert System:**
✅ Scans EUR/USD every {config.SCAN_INTERVAL_SECONDS // 60} minutes
✅ Auto-sends signals when:
   • Setup score ≥ {config.MIN_SETUP_SCORE}/10
   • Take Profit ≥ {config.MIN_TP_PIPS} pips
✅ Includes full trade details:
   • Entry zone & precise entry
   • Stop Loss with pip distance
   • 3 Take Profit levels (1.5R, 2.5R, 3R)
   • Position size (auto-calculated)
   • Setup score & confluences

**SMC Analysis Includes:**
• Order Blocks (last opposite candle before move)
• Fair Value Gaps (3-candle imbalances)
• Supply & Demand Zones (areas of interest)
• Liquidity Pools (equal highs/lows)
• Liquidity Sweeps (stop hunts)
• Fakeout Detection (false breakouts)
• Market Structure (BOS/ChoCH)
• Premium/Discount Zones

**Session Times (IST):**
• London: {config.LONDON_OPEN_HOUR}:{config.LONDON_OPEN_MINUTE:02d} - {config.LONDON_CLOSE_HOUR}:{config.LONDON_CLOSE_MINUTE:02d}
• NY: {config.NY_OPEN_HOUR}:{config.NY_OPEN_MINUTE:02d} - {config.NY_CLOSE_HOUR}:{config.NY_CLOSE_MINUTE:02d}

**Risk Management:**
• Account Size: ${config.ACCOUNT_SIZE}
• Risk per Trade: {config.RISK_PERCENT}%
• Risk Amount: ${config.ACCOUNT_SIZE * config.RISK_PERCENT / 100:.2f}

⚠️ **Important:**
• Bot provides alerts, NOT auto-trading
• Always verify setups before entering
• Use proper risk management
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command - analyze EUR/USD now"""
        await update.message.reply_text("🔍 Analyzing EUR/USD now...")

        try:
            if not self.strategy:
                await update.message.reply_text("❌ Strategy not initialized. Please wait for bot to fully start.")
                return

            # Analyze EUR/USD
            setup = self.strategy.analyze_pair(config.TARGET_PAIR)

            if setup:
                # Send the full setup alert
                message = format_telegram_message(setup)
                await update.message.reply_text(message, parse_mode='Markdown')

                # Add to history
                self.add_analysis_to_history({
                    'found_setup': True,
                    'score': setup['score'],
                    'direction': setup['direction']
                })
            else:
                # No setup found
                await update.message.reply_text(
                    "📊 **Analysis Complete**\n\n"
                    "No high-quality setup found at the moment.\n\n"
                    "Waiting for:\n"
                    f"• Setup score ≥ {config.MIN_SETUP_SCORE}/10\n"
                    f"• Minimum {config.MIN_CONFLUENCE_COUNT} confluences\n"
                    f"• Clear market structure\n\n"
                    "Keep monitoring!",
                    parse_mode='Markdown'
                )

                # Add to history
                self.add_analysis_to_history({
                    'found_setup': False,
                    'reason': 'No quality setup'
                })

        except Exception as e:
            await update.message.reply_text(f"❌ Error during analysis: {str(e)}")
            print(f"Error in analyze command: {e}")

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        from utils import get_current_session, is_trading_session

        session = get_current_session()
        is_active = is_trading_session()

        uptime = "Not started"
        if self.stats['uptime_start']:
            delta = get_ist_time() - self.stats['uptime_start']
            hours = delta.total_seconds() / 3600
            uptime = f"{hours:.1f} hours"

        # Format last 4 analyses
        history_text = ""
        if self.analysis_history:
            history_text = "\n**Last 4 Analyses:**\n"
            for i, analysis in enumerate(reversed(list(self.analysis_history)), 1):
                time_str = analysis['time'].strftime('%H:%M IST')
                result = analysis['result']

                if result.get('found_setup'):
                    history_text += f"{i}. {time_str} - ✅ Setup Found ({result['direction']}, Score: {result['score']}/10)\n"
                else:
                    history_text += f"{i}. {time_str} - ⏳ {result.get('reason', 'No setup')}\n"
        else:
            history_text = "\n**Last 4 Analyses:**\nNo analyses yet"

        status_message = f"""
📊 **Bot Status**

**Status:** {'🟢 Active' if is_active else '🟡 Standby'}
**Current Session:** {session}
**Trading Session:** {'Yes' if is_active else 'No'}
**Current Time:** {get_ist_time().strftime('%H:%M:%S IST')}

**Statistics:**
• Alerts Sent: {self.stats['alerts_sent']}
• Scans Completed: {self.stats['scans_completed']}
• Uptime: {uptime}

{history_text}

**Next Active Session:**
• London: {config.LONDON_OPEN_HOUR}:{config.LONDON_OPEN_MINUTE:02d} IST
• NY: {config.NY_OPEN_HOUR}:{config.NY_OPEN_MINUTE:02d} IST

**Settings:**
• Target Pair: {config.TARGET_PAIR}
• Scan Interval: {config.SCAN_INTERVAL_SECONDS // 60} min
• Min Setup Score: {config.MIN_SETUP_SCORE}/10
• Min TP for Auto-Send: {config.MIN_TP_PIPS} pips
• Risk per Trade: {config.RISK_PERCENT}%
"""
        await update.message.reply_text(status_message, parse_mode='Markdown')

    async def send_alert(self, application: Application, setup: dict):
        """
        Send trade alert to Telegram

        Args:
            application: Telegram application instance
            setup: Setup dictionary from strategy
        """
        message = format_telegram_message(setup)

        try:
            await application.bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=message,
                parse_mode='Markdown'
            )
            self.stats['alerts_sent'] += 1
            print(f"✅ Alert sent for {setup['pair']}")

            # Add to analysis history
            self.add_analysis_to_history({
                'found_setup': True,
                'score': setup['score'],
                'direction': setup['direction']
            })

        except Exception as e:
            print(f"❌ Error sending alert: {e}")

    def setup_handlers(self, application: Application):
        """Setup command handlers"""
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("analyze", self.analyze_command))
        application.add_handler(CommandHandler("status", self.status_command))

        print("✅ Telegram handlers registered")
