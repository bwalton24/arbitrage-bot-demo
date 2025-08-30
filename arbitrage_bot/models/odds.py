from dataclasses import dataclass
from arbitrage_bot.models.sportsbooks import Sportsbook


@dataclass
class GameOdds:
    sportsbook: Sportsbook
    team1: str
    team2: str
    team1_url: str
    team2_url: str
    team1_odds: float
    team2_odds: float
