from abc import ABC, abstractmethod
from typing import List
from arbitrage_bot.models.odds import GameOdds
from arbitrage_bot.models.sportsbooks import Sportsbook


class OddsFetcher(ABC):
    """Abstract base class for fetching odds from sportsbooks"""

    def __init__(self, sportsbook: Sportsbook):
        self.sportsbook = sportsbook

    @abstractmethod
    def fetch_odds(self) -> List[GameOdds]:
        """
        Fetch current odds from sportsbook

        Returns:
            List of GameOdds objects
        """
        pass

    def get_sportsbook(self) -> str:
        """Get the name of this sportsbook"""
        return self.sportsbook
