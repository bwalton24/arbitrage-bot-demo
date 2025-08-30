from dataclasses import dataclass
from arbitrage_bot.models.sportsbooks import Sportsbook


@dataclass
class ArbitrageOpportunity:
    team1: str
    team2: str
    book1: Sportsbook
    book2: Sportsbook
    book1_url: str
    book2_url: str
    book1_odds: float
    book2_odds: float
    profit_percentage: float
    bet1_amount: float
    bet2_amount: float
    total_profit: float

    def __str__(self) -> str:
        return (
            f"Arbitrage: {self.team1} vs {self.team2} | "
            f"{self.book1}({self.book1_odds}) vs {self.book2}({self.book2_odds}) | "
            f"Profit: {self.profit_percentage:.2f}% | "
            f"Total Profit: ${self.total_profit:.2f}"
        )
