import time
import logging
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from arbitrage_bot.odds.draftkings import DraftKingsOddsFetcher
from arbitrage_bot.odds.betmgm import BetMGMOddsFetcher
from arbitrage_bot.detection import ArbitrageDetector
from arbitrage_bot.browser.draftkings import DraftKingsBrowser
from arbitrage_bot.browser.betmgm import BetMGMBrowser
from arbitrage_bot.models.odds import GameOdds
from arbitrage_bot.models.arbitrage import ArbitrageOpportunity
from arbitrage_bot.config import Settings
from arbitrage_bot.models.sportsbooks import Sportsbook
from arbitrage_bot.odds.base import OddsFetcher
from arbitrage_bot.browser.base import BrowserAutomation


class ArbitrageOrchestrator:
    """Main orchestrator that coordinates all arbitrage bot operations"""

    def __init__(self, settings: Settings):
        self.settings = settings or Settings()
        self.logger = self._setup_logging()

        # Initialize components
        self.odds_fetchers = self._setup_odds_fetchers()
        if self.settings.enable_browser_automation:
            self.browser_automations = self._setup_browser_automations()
        else:
            self.browser_automations = {}

        self.arbitrage_detector = ArbitrageDetector(
            min_profit_percentage=self.settings.min_profit_percentage
        )

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("arbitrage_bot.log"),
                logging.StreamHandler(),
            ],
        )
        return logging.getLogger(__name__)

    def _setup_odds_fetchers(self) -> Dict[Sportsbook, OddsFetcher]:
        """Setup odds fetchers for each sportsbook"""
        fetchers = {}

        if Sportsbook.DRAFTKINGS in self.settings.sportsbooks:
            fetchers[Sportsbook.DRAFTKINGS] = DraftKingsOddsFetcher()

        if Sportsbook.BETMGM in self.settings.sportsbooks:
            fetchers[Sportsbook.BETMGM] = BetMGMOddsFetcher()

        return fetchers

    def _setup_browser_automations(self) -> Dict[Sportsbook, BrowserAutomation]:
        """Setup browser automations for each sportsbook"""
        automations = {}

        if Sportsbook.DRAFTKINGS in self.settings.sportsbooks:
            automations[Sportsbook.DRAFTKINGS] = DraftKingsBrowser()

        if Sportsbook.BETMGM in self.settings.sportsbooks:
            automations[Sportsbook.BETMGM] = BetMGMBrowser()

        return automations

    def run_continuous_loop(self):
        """Main continuous monitoring loop"""
        self.logger.info("Starting arbitrage bot...")

        try:
            while True:
                self.logger.info("Starting new iteration...")

                # Step 1: Fetch odds from all sportsbooks
                all_odds = self._fetch_all_odds()
                # print(all_odds)

                # Step 2: Detect arbitrage opportunities
                opportunities = self.arbitrage_detector.detect_opportunities(all_odds)
                for opportunity in opportunities:
                    print(opportunity)

                # Step 3: Execute browser actions for opportunities
                if opportunities:
                    self._execute_arbitrage_actions(opportunities)

                # Step 4: Wait for next iteration
                self.logger.info(
                    f"Waiting {self.settings.refresh_interval_seconds} seconds..."
                )
                time.sleep(self.settings.refresh_interval_seconds)

        except KeyboardInterrupt:
            self.logger.info("Stopping arbitrage bot...")
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
            raise

    def _fetch_all_odds(self) -> Dict[str, List[GameOdds]]:
        """Fetch odds from all sportsbooks in parallel"""
        all_odds = {}

        with ThreadPoolExecutor(max_workers=len(self.odds_fetchers)) as executor:
            # Submit all fetch tasks
            future_to_sportsbook = {
                executor.submit(fetcher.fetch_odds): sportsbook
                for sportsbook, fetcher in self.odds_fetchers.items()
            }

            # Collect results
            for future in as_completed(future_to_sportsbook):
                sportsbook = future_to_sportsbook[future]
                try:
                    odds = future.result()
                    all_odds[sportsbook] = odds
                    self.logger.info(f"Fetched {len(odds)} odds from {sportsbook}")
                except Exception as e:
                    self.logger.error(f"Error fetching odds from {sportsbook}: {e}")
                    all_odds[sportsbook] = []

        return all_odds

    def _execute_arbitrage_actions(self, opportunities: List[ArbitrageOpportunity]):
        """Execute browser actions for arbitrage opportunities"""
        self.logger.info(f"Found {len(opportunities)} arbitrage opportunities!")

        for opportunity in opportunities:
            self.logger.info(f"Processing opportunity: {opportunity}")

            if self.settings.enable_browser_automation:
                self._execute_browser_actions(opportunity)
            else:
                # Just log the opportunity for proof of concept
                self.logger.info(
                    f"Would place bet: ${opportunity.bet1_amount:.2f} on {opportunity.book1} "
                    f"and ${opportunity.bet2_amount:.2f} on {opportunity.book2}"
                )

    def _execute_browser_actions(self, opportunity: ArbitrageOpportunity):
        """Execute browser actions for a single arbitrage opportunity"""
        try:
            book_1_browser = self.browser_automations[opportunity.book1]
            book_2_browser = self.browser_automations[opportunity.book2]

            with ThreadPoolExecutor(max_workers=2) as executor:
                # Load urls for both sportsbo oks
                futures = []
                futures.append(
                    executor.submit(
                        book_1_browser.open_url,
                        opportunity.book1_url,
                    )
                )
                futures.append(
                    executor.submit(
                        book_2_browser.open_url,
                        opportunity.book2_url,
                    )
                )
                # Wait for both to complete
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        self.logger.error(f"Error in browser action: {e}")

                # Fill betslip
                futures = []
                futures.append(
                    executor.submit(
                        book_1_browser.fill_betslip,
                        opportunity.bet1_amount,
                    )
                )
                futures.append(
                    executor.submit(
                        book_2_browser.fill_betslip,
                        opportunity.bet2_amount,
                    )
                )
                # Wait for both to complete
                any_failed = False
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        if not result:
                            any_failed = True
                    except Exception as e:
                        self.logger.error(f"Error in browser action: {e}")

                if any_failed:
                    self.clear_betslips(book_1_browser, book_2_browser)
                    self.logger.error("One or more bets failed, clearing betslips")
                    return

                # Verify odds
                futures = []
                futures.append(
                    executor.submit(
                        book_1_browser.verify_odds,
                        opportunity.book1_odds,
                    )
                )
                futures.append(
                    executor.submit(
                        book_2_browser.verify_odds,
                        opportunity.book2_odds,
                    )
                )
                # Wait for both to complete
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        if not result:
                            any_failed = True
                    except Exception as e:
                        self.logger.error(f"Error in browser action: {e}")

                if any_failed:
                    self.clear_betslips(book_1_browser, book_2_browser)
                    self.logger.error("One or more bets failed, clearing betslips")
                    return

                # Place bet
                futures = []
                futures.append(
                    executor.submit(
                        book_1_browser.place_bet,
                    )
                )
                futures.append(
                    executor.submit(
                        book_2_browser.place_bet,
                    )
                )
                # Wait for both to complete
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        self.logger.error(f"Error in browser action: {e}")

                self.logger.info("Completed browser actions for all sportsbooks")

                self.clear_betslips(book_1_browser, book_2_browser)

        except Exception as e:
            self.logger.error(f"Error executing browser actions: {e}")

    def clear_betslips(
        self, book_1_browser: BrowserAutomation, book_2_browser: BrowserAutomation
    ):
        """Execute browser actions for a specific sportsbook"""

        with ThreadPoolExecutor(max_workers=2) as executor:
            # Clear betslips
            futures = []
            futures.append(
                executor.submit(
                    book_1_browser.clear_betslip,
                )
            )

            futures.append(
                executor.submit(
                    book_2_browser.clear_betslip,
                )
            )
            # Wait for both to complete
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"Error in browser action: {e}")
