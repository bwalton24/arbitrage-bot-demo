from dataclasses import dataclass
from typing import List
import json
import os
from arbitrage_bot.models.sportsbooks import Sportsbook


@dataclass
class Settings:
    """Configuration settings for the arbitrage bot"""

    # Sportsbooks to monitor
    sportsbooks: List[Sportsbook] = None

    # Arbitrage settings
    min_profit_percentage: float = 2.5
    total_bet_amount: float = 100.0

    # Timing settings
    refresh_interval_seconds: int = 5

    # Browser settings
    enable_browser_automation: bool = True

    def __post_init__(self):
        if self.sportsbooks is None:
            self.sportsbooks = [
                Sportsbook.DRAFTKINGS,
                Sportsbook.BETMGM,
            ]

    @classmethod
    def from_file(cls, config_file: str = "config/settings.json") -> "Settings":
        """Load settings from JSON file"""
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config_data = json.load(f)
                return cls(**config_data)
            except Exception as e:
                print(f"Error loading config file: {e}")
                return cls()
        else:
            return cls()

    def save_to_file(self, config_file: str = "config/settings.json"):
        """Save settings to JSON file"""
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, "w") as f:
            json.dump(self.__dict__, f, indent=2)
