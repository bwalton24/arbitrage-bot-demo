#!/usr/bin/env python3
"""
Arbitrage Sports Betting Bot
Main entry point for the arbitrage detection and execution system.
"""

import sys
import os

# Add the parent directory to the path so we can import from arbitrage_bot
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arbitrage_bot.orchestrator import ArbitrageOrchestrator
from arbitrage_bot.config import Settings


def main():
    """Main entry point for the arbitrage bot"""
    print("Starting Arbitrage Sports Betting Bot...")
    print("=" * 50)

    # Load settings
    settings = Settings.from_file()
    print(f"Loaded settings: {settings}")

    # Create and run orchestrator
    orchestrator = ArbitrageOrchestrator(settings)

    try:
        orchestrator.run_continuous_loop()
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"Error running bot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
