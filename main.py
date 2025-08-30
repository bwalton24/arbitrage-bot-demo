#!/usr/bin/env python3
"""
Arbitrage Sports Betting Bot - Main Entry Point
"""

import sys
import os

# Add the arbitrage_bot directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "arbitrage_bot"))

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
