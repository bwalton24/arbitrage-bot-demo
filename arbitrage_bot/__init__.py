"""
Arbitrage Sports Betting Bot

A modular system for detecting and executing arbitrage opportunities
across multiple sportsbooks.
"""

__version__ = "0.1.0"
__author__ = "Arbitrage Bot Team"

from .orchestrator import ArbitrageOrchestrator
from .config import Settings

__all__ = ["ArbitrageOrchestrator", "Settings"]
