from typing import List
import curl_cffi

from .base import OddsFetcher
from arbitrage_bot.models.odds import GameOdds
from arbitrage_bot.models.sportsbooks import Sportsbook


class BetMGMOddsFetcher(OddsFetcher):
    """BetMGM odds fetcher implementation"""

    def __init__(self):
        super().__init__(Sportsbook.BETMGM)

    def fetch_odds(self) -> List[GameOdds]:
        """
        Fetch odds from BetMGM

        Returns:
            List of GameOdds objects
        """
        odds = []

        try:
            response = curl_cffi.get(
                "https://www.mi.betmgm.com/cds-api/bettingoffer/fixtures?x-bwin-accessid=NmFjNmUwZjAtMGI3Yi00YzA3LTg3OTktNDgxMGIwM2YxZGVh&lang=en-us&country=US&userCountry=US&subdivision=US-Michigan&state=Live&take=50&offerMapping=Filtered&offerCategories=Gridable&sortBy=Tags&sportIds=11&statisticsModes=Rank,SeasonStandings",
                impersonate="chrome",
            )

            fixtures = response.json()["fixtures"]
            for fixture in fixtures:
                event_id = fixture["id"]
                event_name = fixture["name"]["value"].replace(" ", "-").lower()
                base_url = f"https://sports.mi.betmgm.com/en/sports/events/{event_name}-{event_id}"

                if "optionMarkets" in fixture and len(fixture["optionMarkets"]) > 0:
                    p1, p2, m1, m2 = None, None, None, None
                    try:
                        participants = fixture["participants"][:2]
                        p1 = participants[0]["name"]["value"]
                        p2 = participants[1]["name"]["value"]
                        if not p1 or not p2:
                            continue
                    except:
                        continue

                    option_markets = fixture["optionMarkets"]
                    for market in option_markets:
                        try:
                            market_name = market["name"]["value"]
                            status = market["status"]
                            market_id = market["id"]
                            if market_name != "Money Line" or status != "Visible":
                                continue
                            m1 = market["options"][0]["price"]["americanOdds"]
                            s1_id = market["options"][0]["id"]
                            m2 = market["options"][1]["price"]["americanOdds"]
                            s2_id = market["options"][1]["id"]
                            break
                        except:
                            continue

                    if not m1 or not m2:
                        continue

                    team1_url = (
                        f"{base_url}?options={event_id}-{market_id}-{s1_id}&type=Single"
                    )
                    team2_url = (
                        f"{base_url}?options={event_id}-{market_id}-{s2_id}&type=Single"
                    )

                    odds.append(
                        GameOdds(
                            sportsbook=Sportsbook.BETMGM,
                            team1=p1,
                            team2=p2,
                            team1_odds=m1,
                            team1_url=team1_url,
                            team2_odds=m2,
                            team2_url=team2_url,
                        )
                    )

                elif "games" in fixture and len(fixture["games"]) > 0:
                    games = fixture["games"]
                    for game in games:
                        market_id = game["id"]
                        try:
                            market_name = game["name"]["value"]
                            visibility = game["visibility"]
                            if market_name != "Money Line" or visibility != "Visible":
                                continue

                            p1 = game["results"][0]["name"]["value"]
                            m1 = game["results"][0]["americanOdds"]
                            s1_id = game["results"][0]["id"]
                            p2 = game["results"][1]["name"]["value"]
                            m2 = game["results"][1]["americanOdds"]
                            s2_id = game["results"][1]["id"]

                            team1_url = f"{base_url}?options={event_id}-{market_id}-{s1_id}&type=Single"
                            team2_url = f"{base_url}?options={event_id}-{market_id}-{s2_id}&type=Single"

                            odds.append(
                                GameOdds(
                                    sportsbook=Sportsbook.BETMGM,
                                    team1=p1,
                                    team2=p2,
                                    team1_odds=m1,
                                    team1_url=team1_url,
                                    team2_odds=m2,
                                    team2_url=team2_url,
                                )
                            )
                            break
                        except:
                            continue

            return odds
        except:
            print("Error fetching odds from BetMGM")
            return []
