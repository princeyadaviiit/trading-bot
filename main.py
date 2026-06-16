"""
SMC Forex Trading Bot - Main Entry Point (Discord Version)
24/7 Automated Market Scanner with Discord Alerts
"""
import asyncio
from datetime import datetime, timedelta
import config
from discord_handler import DiscordHandler
from strategy import SMCStrategy
from utils import is_trading_session, get_current_session

class TradingBot:
    """Main trading bot orchestrator"""

    def __init__(self):
        """Initialize bot components"""
        print("🤖 Initializing SMC Trading Bot (Railway/Discord)...")

        # Validate configuration
        config.validate_config()
        print("✅ Configuration validated")

        # Initialize components
        self.discord_handler = DiscordHandler()
        self.strategy = SMCStrategy()
        self.is_running = False
        self.scan_interval = 60  # Scan every 60 seconds with MT5 (fast local data)

        # Alert tracking
        self.alert_history = []
        self.last_scan_time = None

    async def scan_markets(self):
        """Scan all monitored pairs for setups"""
        if not is_trading_session():
            # Skip scanning outside trading sessions
            return

        print(f"\n🔍 Scanning markets... [{get_current_session()} Session]")
        self.last_scan_time = datetime.now()

        # Get monitored pairs
        pairs = self.discord_handler.get_monitored_pairs()

        if not pairs:
            print("⚠️ No pairs to monitor")
            return

        # Check alert rate limit (max per hour)
        recent_alerts = [
            alert for alert in self.alert_history
            if datetime.now() - alert < timedelta(hours=1)
        ]

        if len(recent_alerts) >= config.MAX_ALERTS_PER_HOUR:
            print(f"⏸️ Alert limit reached ({config.MAX_ALERTS_PER_HOUR}/hour)")
            return

        # Scan pairs (with API rate limiting consideration)
        setups = self.strategy.scan_pairs(pairs)

        if setups:
            print(f"📊 Found {len(setups)} setup(s)")

            for setup in setups:
                # Send alert
                await self.discord_handler.send_alert(setup)

                # Track alert
                self.alert_history.append(datetime.now())

                # Add delay between alerts to avoid spam
                await asyncio.sleep(2)

            # Add delay after scanning to respect API limits
            await asyncio.sleep(5)  # Extra delay when setups found
        else:
            print("No setups found")

    async def run_forever(self):
        """Main bot loop - runs 24/7"""
        print(f"\n{'='*50}")
        print("🚀 SMC Trading Bot Started (Discord)")
        print(f"{'='*50}")
        print(f"📊 Monitoring: {len(self.discord_handler.get_monitored_pairs())} pairs")
        print(f"⏰ Scan Interval: {self.scan_interval} seconds")
        print(f"🎯 Min Setup Score: {config.MIN_SETUP_SCORE}/10")
        print(f"💰 Risk per Trade: {config.RISK_PERCENT}% (${config.ACCOUNT_SIZE * config.RISK_PERCENT / 100:.2f})")
        print(f"{'='*50}\n")

        self.discord_handler.stats['uptime_start'] = datetime.now()
        self.is_running = True

        while self.is_running:
            try:
                # Scan markets
                await self.scan_markets()

                # Show next scan info
                session = get_current_session()
                next_scan = datetime.now() + timedelta(seconds=self.scan_interval)

                if is_trading_session():
                    print(f"⏳ Next scan: {next_scan.strftime('%H:%M:%S')} ({session})")
                else:
                    print(f"💤 Waiting for trading session... (Currently: {session})")

                # Wait for next scan
                await asyncio.sleep(self.scan_interval)

            except KeyboardInterrupt:
                print("\n⚠️ Shutting down...")
                self.is_running = False
                break

            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                print("⏳ Retrying in 60 seconds...")
                await asyncio.sleep(60)

    async def start(self):
        """Start the bot"""
        try:
            # Start Discord bot in background
            discord_task = asyncio.create_task(self.discord_handler.start())

            # Wait for bot to be ready
            await asyncio.sleep(3)

            # Send startup notification
            if self.discord_handler.channel:
                await self.discord_handler.channel.send(
                    "🤖 **SMC Trading Bot Started**\n\nMonitoring markets 24/7. Use `!help` for commands."
                )

            # Run main loop
            await self.run_forever()

        except Exception as e:
            print(f"❌ Fatal error: {e}")

        finally:
            await self.discord_handler.close()


async def main():
    """Main entry point"""
    bot = TradingBot()
    await bot.start()


if __name__ == "__main__":
    print("="*50)
    print("  SMC Forex Trading Bot v1.0 - Discord")
    print("  Smart Money Concepts Analyzer")
    print("="*50)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        print("\nPlease check your configuration")
