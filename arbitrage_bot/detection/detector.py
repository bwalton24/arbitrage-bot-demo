from typing import Dict, List, Tuple
from ..models.odds import GameOdds
from ..models.arbitrage import ArbitrageOpportunity
from .team_mapper import TeamMapper


class ArbitrageDetector:
    """Detects arbitrage opportunities across sportsbooks"""

    def __init__(self, min_profit_percentage: float = -10.0):
        self.min_profit_percentage = min_profit_percentage
        self.team_mapper = TeamMapper()

    def detect_opportunities(
        self, all_odds: Dict[str, List[GameOdds]]
    ) -> List[ArbitrageOpportunity]:
        """
        Detect arbitrage opportunities across all sportsbooks

        Args:
            all_odds: Dictionary mapping sportsbook names to lists of GameOdds

        Returns:
            List of ArbitrageOpportunity objects
        """
        opportunities = []

        # Get all unique games across sportsbooks
        all_games = self._get_all_games(all_odds)

        for game in all_games:
            print(game)

        # For each game, check for arbitrage between sportsbooks
        for game_key in all_games:
            game_odds = all_games[game_key]

            # Check all pairs of sportsbooks for this game
            for i, odds1 in enumerate(game_odds):
                for odds2 in game_odds[i + 1 :]:
                    print(odds1, odds2)
                    opportunity = self._check_arbitrage(odds1, odds2)
                    if opportunity:
                        opportunities.append(opportunity)

        print(opportunities)

        return opportunities

    def _get_all_games(
        self, all_odds: Dict[str, List[GameOdds]]
    ) -> Dict[str, List[GameOdds]]:
        """Group odds by standardized game (team1 vs team2)"""
        games = {}

        for sportsbook, odds_list in all_odds.items():
            for odds in odds_list:
                # Standardize team names
                team1_std = self.team_mapper.standardize_team_name(odds.team1)
                team2_std = self.team_mapper.standardize_team_name(odds.team2)

                # Create consistent game key (alphabetical order)
                if team1_std < team2_std:
                    game_key = f"{team1_std}_vs_{team2_std}"
                else:
                    game_key = f"{team2_std}_vs_{team1_std}"

                if game_key not in games:
                    games[game_key] = []
                games[game_key].append(odds)

        return games

    def _check_arbitrage(
        self, odds1: GameOdds, odds2: GameOdds
    ) -> ArbitrageOpportunity:
        """Check for arbitrage between two odds objects"""
        # Standardize team names for both odds objects
        odds1_team1_std = self.team_mapper.standardize_team_name(odds1.team1)
        odds1_team2_std = self.team_mapper.standardize_team_name(odds1.team2)
        odds2_team1_std = self.team_mapper.standardize_team_name(odds2.team1)
        odds2_team2_std = self.team_mapper.standardize_team_name(odds2.team2)

        # Determine which teams match between the two odds objects
        scenarios = []

        if odds1_team1_std == odds2_team1_std:
            scenarios.append(
                {
                    "book1_side": "team1",
                    "book2_side": "team2",
                    "book1_odds": odds1.team1_odds,
                    "book2_odds": odds2.team2_odds,
                    "book1_url": odds1.team1_url,
                    "book2_url": odds2.team2_url,
                    "team1_std": odds1_team1_std,
                    "team2_std": odds2_team2_std,
                }
            )
            scenarios.append(
                {
                    "book1_side": "team2",
                    "book2_side": "team1",
                    "book1_odds": odds1.team2_odds,
                    "book2_odds": odds2.team1_odds,
                    "book1_url": odds1.team2_url,
                    "book2_url": odds2.team1_url,
                    "team1_std": odds1_team2_std,
                    "team2_std": odds2_team1_std,
                }
            )
        else:
            scenarios.append(
                {
                    "book1_side": "team1",
                    "book2_side": "team1",
                    "book1_odds": odds1.team1_odds,
                    "book2_odds": odds2.team1_odds,
                    "book1_url": odds1.team1_url,
                    "book2_url": odds2.team1_url,
                    "team1_std": odds1_team1_std,
                    "team2_std": odds2_team1_std,
                }
            )
            scenarios.append(
                {
                    "book1_side": "team2",
                    "book2_side": "team2",
                    "book1_odds": odds1.team2_odds,
                    "book2_odds": odds2.team2_odds,
                    "book1_url": odds1.team2_url,
                    "book2_url": odds2.team2_url,
                    "team1_std": odds1_team2_std,
                    "team2_std": odds2_team2_std,
                }
            )

        best_opportunity = None
        best_profit = -10

        for scenario in scenarios:
            profit_pct = self._calculate_arbitrage_profit(
                scenario["book1_odds"], scenario["book2_odds"]
            )

            print(profit_pct)

            print(self.min_profit_percentage)

            if profit_pct > best_profit and profit_pct >= self.min_profit_percentage:
                best_profit = profit_pct
                best_opportunity = scenario

        if best_opportunity:
            # Calculate bet amounts for $100 total bet
            total_bet = 100
            bet1_amount, bet2_amount, total_profit = self._calculate_bet_amounts(
                best_opportunity["book1_odds"],
                best_opportunity["book2_odds"],
                total_bet,
            )

            return ArbitrageOpportunity(
                team1=best_opportunity["team1_std"],
                team2=best_opportunity["team2_std"],
                book1=odds1.sportsbook,
                book2=odds2.sportsbook,
                book1_url=best_opportunity["book1_url"],
                book2_url=best_opportunity["book2_url"],
                book1_odds=best_opportunity["book1_odds"],
                book2_odds=best_opportunity["book2_odds"],
                profit_percentage=best_profit,
                bet1_amount=bet1_amount,
                bet2_amount=bet2_amount,
                total_profit=total_profit,
            )

        return None

    def _calculate_arbitrage_profit(self, odds1: float, odds2: float) -> float:
        """Calculate arbitrage profit percentage"""
        # Convert American odds to probability of winning
        if odds1 > 0:
            prob1 = 100 / (odds1 + 100)
        else:
            prob1 = abs(odds1) / (abs(odds1) + 100)

        if odds2 > 0:
            prob2 = 100 / (odds2 + 100)
        else:
            prob2 = abs(odds2) / (abs(odds2) + 100)

        # Calculate arbitrage profit percentage
        total_probability = prob1 + prob2
        profit_percentage = (1 - total_probability) * 100

        return profit_percentage

    def _calculate_bet_amounts(
        self, odds1: float, odds2: float, total_bet: float
    ) -> Tuple[float, float, float]:
        """Calculate optimal bet amounts for arbitrage"""
        # Convert American odds to decimal
        if odds1 > 0:
            decimal1 = (odds1 / 100) + 1
        else:
            decimal1 = (100 / abs(odds1)) + 1

        if odds2 > 0:
            decimal2 = (odds2 / 100) + 1
        else:
            decimal2 = (100 / abs(odds2)) + 1

        # Calculate bet amounts
        bet1_amount = (total_bet * decimal2) / (decimal1 + decimal2)
        bet2_amount = total_bet - bet1_amount

        # Calculate profit
        profit1 = (bet1_amount * decimal1) - total_bet
        profit2 = (bet2_amount * decimal2) - total_bet

        total_profit = min(profit1, profit2)

        return bet1_amount, bet2_amount, total_profit
