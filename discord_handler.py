"""
Discord Bot Handler
Manages Discord commands and sends alerts
"""
import discord
from discord.ext import commands
from typing import List, Set
import config
from utils import format_telegram_message, validate_pair, convert_mt5_pair
from datetime import datetime

class DiscordHandler:
    """Discord bot command handler"""

    def __init__(self):
        """Initialize Discord bot"""
        # Setup bot with intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True

        # Disable default help command so we can use our own
        self.bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
        self.monitored_pairs: Set[str] = set(config.DEFAULT_PAIRS)
        self.is_running = False
        self.stats = {
            'alerts_sent': 0,
            'pairs_monitored': len(self.monitored_pairs),
            'uptime_start': None
        }
        self.channel = None

        # Register commands
        self.setup_commands()

    def setup_commands(self):
        """Setup Discord bot commands"""

        @self.bot.event
        async def on_ready():
            """Called when bot is ready"""
            print(f'✅ Discord bot logged in as {self.bot.user}')
            # Get the channel
            self.channel = self.bot.get_channel(config.DISCORD_CHANNEL_ID)
            if self.channel:
                print(f'✅ Connected to channel: {self.channel.name}')
            else:
                print(f'⚠️ Could not find channel with ID: {config.DISCORD_CHANNEL_ID}')

        @self.bot.command(name='start')
        async def start_command(ctx):
            """Handle !start command"""
            welcome_message = f"""
🤖 **SMC Forex Trading Bot**

Welcome! I monitor forex pairs 24/7 and send you high-probability trade setups based on Smart Money Concepts.

📊 **Features:**
✅ Order Blocks & Fair Value Gaps
✅ Liquidity Sweep Detection
✅ London & NY Session Alerts
✅ Auto Risk Management

📱 **Commands:**
`!add <pair>` - Add pair to monitoring
`!remove <pair>` - Remove pair
`!list` - Show monitored pairs
`!status` - Bot status & stats
`!help` - Show all commands

🎯 **Default Pairs:**
{chr(10).join([f'• {p}' for p in self.monitored_pairs])}

**Bot is ready!** Waiting for high-quality setups during trading sessions.
"""
            await ctx.send(welcome_message)

        @self.bot.command(name='help')
        async def help_command(ctx):
            """Handle !help command"""
            help_text = """
📖 **Bot Commands**

**Pair Management:**
`!add AUDUSD` - Add Australian Dollar
`!add GBPUSD` - Add British Pound
`!remove USDJPY` - Remove Japanese Yen
`!list` - Show all monitored pairs

**Bot Control:**
`!status` - Show bot statistics
`!help` - Show this help message

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
            await ctx.send(help_text)

        @self.bot.command(name='add')
        async def add_command(ctx, pair: str = None):
            """Handle !add <pair> command"""
            if not pair:
                await ctx.send("❌ Usage: `!add <pair>`\nExample: `!add AUDUSD` or `!add EURJPY`")
                return

            pair = pair.upper().replace('/', '').replace('_', '')

            if not validate_pair(pair):
                await ctx.send(f"❌ Invalid pair format: {pair}\nUse format: EURUSD (6 letters)")
                return

            if pair in self.monitored_pairs:
                await ctx.send(f"⚠️ {pair} is already being monitored")
                return

            self.monitored_pairs.add(pair)
            self.stats['pairs_monitored'] = len(self.monitored_pairs)

            await ctx.send(f"✅ Added {pair} to monitoring\nTotal pairs: {len(self.monitored_pairs)}")

        @self.bot.command(name='remove')
        async def remove_command(ctx, pair: str = None):
            """Handle !remove <pair> command"""
            if not pair:
                await ctx.send("❌ Usage: `!remove <pair>`\nExample: `!remove AUDUSD`")
                return

            pair = pair.upper().replace('/', '').replace('_', '')

            if pair not in self.monitored_pairs:
                await ctx.send(f"⚠️ {pair} is not in monitoring list")
                return

            self.monitored_pairs.remove(pair)
            self.stats['pairs_monitored'] = len(self.monitored_pairs)

            await ctx.send(f"✅ Removed {pair} from monitoring\nTotal pairs: {len(self.monitored_pairs)}")

        @self.bot.command(name='list')
        async def list_command(ctx):
            """Handle !list command"""
            if not self.monitored_pairs:
                await ctx.send("No pairs are being monitored")
                return

            pairs_list = "\n".join([f"• {p}" for p in sorted(self.monitored_pairs)])
            message = f"**Monitored Pairs ({len(self.monitored_pairs)}):**\n\n{pairs_list}"

            await ctx.send(message)

        @self.bot.command(name='status')
        async def status_command(ctx):
            """Handle !status command"""
            from utils import get_current_session, is_trading_session

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
            await ctx.send(status_message)

    async def send_alert(self, setup: dict):
        """
        Send trade alert to Discord

        Args:
            setup: Setup dictionary from strategy
        """
        if not self.channel:
            print("❌ Discord channel not set")
            return

        message = format_telegram_message(setup)

        try:
            await self.channel.send(message)
            self.stats['alerts_sent'] += 1
            print(f"✅ Alert sent for {setup['pair']}")
        except Exception as e:
            print(f"❌ Error sending alert: {e}")

    def get_monitored_pairs(self) -> List[str]:
        """Get list of currently monitored pairs"""
        return list(self.monitored_pairs)

    async def start(self):
        """Start the Discord bot"""
        await self.bot.start(config.DISCORD_BOT_TOKEN)

    async def close(self):
        """Close the Discord bot"""
        await self.bot.close()
