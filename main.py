"""
SMC Forex Trading Bot - Main Entry Point (Telegram Version)
24/7 Automated Market Scanner with Telegram Alerts
Scans EUR/USD every 3 minutes (480 API calls per day)
"""
import asyncio
from datetime import datetime, timedelta
import config
from telegram_handler import TelegramHandler
from telegram.ext import Application
from strategy import SMCStrategy
from utils import is_trading_session, get_current_session, get_ist_time

class TradingBot:
    """Main trading bot orchestrator"""

    def __init__(self):
        """Initialize bot components"""
        print("🤖 Initializing SMC Trading Bot (Telegram + Twelve Data)...")

        # Validate configuration
        config.validate_config()
        print("✅ Configuration validated")

        # Initialize components
        self.telegram_handler = TelegramHandler()
        self.strategy = SMCStrategy()
        self.telegram_handler.strategy = self.strategy  # Link strategy to handler
        self.is_running = False
        self.scan_interval = config.SCAN_INTERVAL_SECONDS  # 180 seconds = 3 minutes

        # Alert tracking
        self.alert_history = []
        self.last_scan_time = None

    async def scan_markets(self, application: Application):
        """Scan EUR/USD for setups"""
        print(f"\n🔍 Scanning {config.TARGET_PAIR}... [{get_current_session()} Session]")
        self.last_scan_time = get_ist_time()

        # Check alert rate limit (max per hour)
        recent_alerts = [
            alert for alert in self.alert_history
            if get_ist_time() - alert < timedelta(hours=1)
        ]

        if len(recent_alerts) >= config.MAX_ALERTS_PER_HOUR:
            print(f"⏸️ Alert limit reached ({config.MAX_ALERTS_PER_HOUR}/hour)")
            self.telegram_handler.stats['scans_completed'] += 1
            self.telegram_handler.add_analysis_to_history({
                'found_setup': False,
                'reason': 'Alert limit reached'
            })
            return

        # Analyze EUR/USD
        try:
            setup = self.strategy.analyze_pair(config.TARGET_PAIR)

            if setup:
                print(f"📊 Setup found! Score: {setup['score']}/10")

                # Send alert
                await self.telegram_handler.send_alert(application, setup)

                # Track alert
                self.alert_history.append(get_ist_time())

            else:
                print("No setup found")
                self.telegram_handler.add_analysis_to_history({
                    'found_setup': False,
                    'reason': 'No quality setup'
                })

            # Update scan counter
            self.telegram_handler.stats['scans_completed'] += 1

        except Exception as e:
            print(f"❌ Error during scan: {e}")
            self.telegram_handler.add_analysis_to_history({
                'found_setup': False,
                'reason': f'Error: {str(e)[:30]}'
            })

    async def run_forever(self, application: Application):
        """Main bot loop - runs 24/7"""
        print(f"\n{'='*60}")
        print("🚀 SMC Trading Bot Started (Telegram)")
        print(f"{'='*60}")
        print(f"📊 Target Pair: {config.TARGET_PAIR}")
        print(f"⏰ Scan Interval: {self.scan_interval // 60} minutes")
        print(f"📈 API Calls per Day: ~{1440 // (self.scan_interval // 60)}")
        print(f"🎯 Min Setup Score: {config.MIN_SETUP_SCORE}/10")
        print(f"📍 Min TP for Auto-Send: {config.MIN_TP_PIPS} pips")
        print(f"💰 Risk per Trade: {config.RISK_PERCENT}% (${config.ACCOUNT_SIZE * config.RISK_PERCENT / 100:.2f})")
        print(f"{'='*60}\n")

        self.telegram_handler.stats['uptime_start'] = get_ist_time()
        self.is_running = True

        # Send startup notification
        try:
            await application.bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=f"🤖 **SMC Trading Bot Started**\n\n"
                     f"✅ Monitoring: {config.TARGET_PAIR}\n"
                     f"⏰ Scan Interval: Every {self.scan_interval // 60} minutes\n"
                     f"🎯 Min Score: {config.MIN_SETUP_SCORE}/10\n"
                     f"📍 Min TP: {config.MIN_TP_PIPS} pips\n\n"
                     f"Use /help to see all commands.",
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"⚠️ Could not send startup notification: {e}")

        while self.is_running:
            try:
                # Scan markets
                await self.scan_markets(application)

                # Show next scan info
                session = get_current_session()
                next_scan = get_ist_time() + timedelta(seconds=self.scan_interval)

                print(f"⏳ Next scan: {next_scan.strftime('%H:%M:%S IST')} ({session})")
                print(f"📊 Total scans: {self.telegram_handler.stats['scans_completed']}")
                print(f"📢 Alerts sent: {self.telegram_handler.stats['alerts_sent']}")

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
            # Create Telegram application
            application = (
                Application.builder()
                .token(config.TELEGRAM_BOT_TOKEN)
                .build()
            )

            # Setup command handlers
            self.telegram_handler.setup_handlers(application)

            # Start the application (polling in background)
            await application.initialize()
            await application.start()
            await application.updater.start_polling()

            print("✅ Telegram bot started and listening for commands")

            # Run main scanning loop
            await self.run_forever(application)

        except Exception as e:
            print(f"❌ Fatal error: {e}")

        finally:
            # Cleanup
            if application:
                await application.updater.stop()
                await application.stop()
                await application.shutdown()
            print("✅ Bot shutdown complete")


async def main():
    """Main entry point"""
    bot = TradingBot()
    await bot.start()


if __name__ == "__main__":
    print("="*60)
    print("  SMC Forex Trading Bot v2.0 - Telegram Edition")
    print("  Smart Money Concepts Analyzer")
    print("  Powered by Twelve Data API")
    print("="*60)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        print("\nPlease check your configuration and API keys")
