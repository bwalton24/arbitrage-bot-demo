from typing import List
from .base import OddsFetcher
from arbitrage_bot.models.odds import GameOdds
from arbitrage_bot.models.sportsbooks import Sportsbook
import curl_cffi
from requests.utils import quote


class DraftKingsOddsFetcher(OddsFetcher):
    """DraftKings odds fetcher implementation"""

    def __init__(self):
        super().__init__(Sportsbook.DRAFTKINGS)
        self.base_url = "https://sportsbook.draftkings.com"

    def fetch_odds(self) -> List[GameOdds]:
        """
        Fetch odds from DraftKings

        Returns:
            List of GameOdds objects
        """
        odds = []

        try:
            params = {
                "isBatchable": "false",
                "templateVars": "87637",
                "eventsQuery": "$filter=leagueId eq '87637' AND clientMetadata/Subcategories/any(s: s/Id eq '4518')",
                "marketsQuery": "$filter=clientMetadata/subCategoryId eq '4518' AND tags/all(t: t ne 'SportcastBetBuilder')",
                "include": "Events",
                "entity": "events",
            }

            response = curl_cffi.get(
                "https://sportsbook-nash.draftkings.com/sites/US-MI-SB/api/sportscontent/controldata/league/leagueSubcategory/v1/markets",
                params=params,
            ).json()

            event_id_to_data = {}
            events = response["events"]
            for event in events:
                status = event["status"]
                if status != "STARTED":
                    continue

                event_id = event["id"]
                p1 = event["participants"][0]["name"]
                p2 = event["participants"][1]["name"]
                event_id_to_data[event_id] = {
                    "event_name": event["name"].replace(" ", "-").lower(),
                    "p1": p1,
                    "p2": p2,
                }

            market_ids = set()
            markets = response["markets"]
            for market in markets:
                market_event_id = market["eventId"]
                if market_event_id not in event_id_to_data:
                    continue

                market_name = market["name"]
                if market_name != "Moneyline":
                    continue

                market_id = market["id"]
                market_ids.add(market_id)

            team_to_selection = {}
            for selection in response["selections"]:
                selection_market_id = selection["marketId"]
                if selection_market_id not in market_ids:
                    continue

                selection_id = selection["id"]
                team_to_selection[selection["label"]] = {
                    "odds": int(selection["displayOdds"]["american"].replace("−", "-")),
                    "selection_id": selection_id,
                }

            for event_id, data in event_id_to_data.items():
                p1 = data["p1"]
                p2 = data["p2"]
                event_name = data["event_name"]
                p1_odds = team_to_selection[p1]["odds"]
                p1_selection_id = team_to_selection[p1]["selection_id"]
                p2_odds = team_to_selection[p2]["odds"]
                p2_selection_id = team_to_selection[p2]["selection_id"]

                team1_url = f"https://sportsbook.draftkings.com/event/{event_name}/{event_id}?outcomes={quote(p1_selection_id)}"
                team2_url = f"https://sportsbook.draftkings.com/event/{event_name}/{event_id}?outcomes={quote(p2_selection_id)}"

                odds.append(
                    GameOdds(
                        sportsbook=Sportsbook.DRAFTKINGS,
                        team1=p1,
                        team2=p2,
                        team1_odds=p1_odds,
                        team1_url=team1_url,
                        team2_odds=p2_odds,
                        team2_url=team2_url,
                    )
                )

            return odds

        except Exception as e:
            print(f"Error fetching odds from DraftKings: {e}")
            return []
