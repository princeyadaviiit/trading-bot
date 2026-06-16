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
from utils import format_telegram_message, validate_pair, convert_mt5_pair
from typing import List, Set

class TelegramHandler:
    """Telegram bot command handler"""

    def __init__(self):
        """Initialize Telegram bot"""
        self.monitored_pairs: Set[str] = set(config.DEFAULT_PAIRS)
        self.is_running = False
        self.stats = {
            'alerts_sent': 0,
            'pairs_monitored': len(self.monitored_pairs),
            'uptime_start': None
        }

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🤖 **SMC Forex Trading Bot**

Welcome! I monitor forex pairs 24/7 and send you high-probability trade setups based on Smart Money Concepts.

📊 **Features:**
✅ Order Blocks & Fair Value Gaps
✅ Liquidity Sweep Detection
✅ London & NY Session Alerts
✅ Auto Risk Management

📱 **Commands:**
/add <pair> - Add pair to monitoring
/remove <pair> - Remove pair
/list - Show monitored pairs
/status - Bot status & stats
/help - Show all commands

🎯 **Default Pairs:**
{pairs}

**Bot is ready!** Waiting for high-quality setups during trading sessions.
""".format(pairs="\n".join([f"• {p}" for p in self.monitored_pairs]))

        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📖 **Bot Commands**

**Pair Management:**
`/add AUDUSD` - Add Australian Dollar
`/add GBP_USD` - Add British Pound
`/remove USDJPY` - Remove Japanese Yen
`/list` - Show all monitored pairs

**Bot Control:**
`/status` - Show bot statistics
`/help` - Show this help message

**Alert Format:**
When a setup is detected, you'll receive:
• Pair & Direction (LONG/SHORT)
• Entry Zone
• Stop Loss & Take Profits
• Position Size (auto-calculated)
• Setup Score (7-10)

**Session Times (IST):**
• London: 1:30 PM - 9:30 PM
• NY: 6:30 PM - 1:30 AM

**Important:**
⚠️ Bot provides alerts, NOT auto-trading
⚠️ Always verify setups before entering
⚠️ Only alerts with score ≥ 7 are sent
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def add_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /add <pair> command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /add <pair>\nExample: /add AUDUSD or /add EURJPY"
            )
            return

        pair = context.args[0].upper().replace('/', '').replace('_', '')

        if not validate_pair(pair):
            await update.message.reply_text(
                f"❌ Invalid pair format: {pair}\n"
                "Use format: EURUSD (6 letters)"
            )
            return

        if pair in self.monitored_pairs:
            await update.message.reply_text(
                f"⚠️ {pair} is already being monitored"
            )
            return

        self.monitored_pairs.add(pair)
        self.stats['pairs_monitored'] = len(self.monitored_pairs)

        await update.message.reply_text(
            f"✅ Added {pair} to monitoring\n"
            f"Total pairs: {len(self.monitored_pairs)}"
        )

    async def remove_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /remove <pair> command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /remove <pair>\nExample: /remove AUDUSD"
            )
            return

        pair = context.args[0].upper().replace('/', '').replace('_', '')

        if pair not in self.monitored_pairs:
            await update.message.reply_text(
                f"⚠️ {pair} is not in monitoring list"
            )
            return

        self.monitored_pairs.remove(pair)
        self.stats['pairs_monitored'] = len(self.monitored_pairs)

        await update.message.reply_text(
            f"✅ Removed {pair} from monitoring\n"
            f"Total pairs: {len(self.monitored_pairs)}"
        )

    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list command"""
        if not self.monitored_pairs:
            await update.message.reply_text("No pairs are being monitored")
            return

        pairs_list = "\n".join([f"• {p}" for p in sorted(self.monitored_pairs)])
        message = f"**Monitored Pairs ({len(self.monitored_pairs)}):**\n\n{pairs_list}"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        from utils import get_current_session, is_trading_session
        from datetime import datetime

        session = get_current_session()
        is_active = is_trading_session()

        uptime = "Not started"
        if self.stats['uptime_start']:
            delta = datetime.now() - self.stats['uptime_start']
            hours = delta.total_seconds() / 3600
            uptime = f"{hours:.1f} hours"

        status_message = f"""
📊 **Bot Status**

**Status:** {'🟢 Active' if is_active else '🟡 Standby'}
**Current Session:** {session}
**Trading Session:** {'Yes' if is_active else 'No'}

**Statistics:**
• Alerts Sent: {self.stats['alerts_sent']}
• Pairs Monitored: {self.stats['pairs_monitored']}
• Uptime: {uptime}

**Next Active Session:**
• London: 1:30 PM IST
• NY: 6:30 PM IST

**Settings:**
• Min Setup Score: {config.MIN_SETUP_SCORE}/10
• Alert Cooldown: {config.ALERT_COOLDOWN_MINUTES} min
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
        except Exception as e:
            print(f"❌ Error sending alert: {e}")

    def get_monitored_pairs(self) -> List[str]:
        """Get list of currently monitored pairs"""
        return list(self.monitored_pairs)

    def setup_handlers(self, application: Application):
        """Setup command handlers"""
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("add", self.add_command))
        application.add_handler(CommandHandler("remove", self.remove_command))
        application.add_handler(CommandHandler("list", self.list_command))
        application.add_handler(CommandHandler("status", self.status_command))

        print("✅ Telegram handlers registered")
