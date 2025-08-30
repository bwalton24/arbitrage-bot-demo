import time
from typing import override
from arbitrage_bot.browser.base import BrowserAutomation
from arbitrage_bot.models.sportsbooks import Sportsbook
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class DraftKingsBrowser(BrowserAutomation):
    """DraftKings browser automation implementation"""

    def __init__(self):
        super().__init__(Sportsbook.DRAFTKINGS)
        self.base_url = "https://sportsbook.draftkings.com"

    @override
    def fill_betslip(self, bet_amount: float):
        """Fill betslip with calculated amount on DraftKings"""
        # TODO: Implement actual betslip filling
        # For now, just log the action
        print(f"[DraftKings] Would place bet: ${bet_amount:.2f}")

        time.sleep(3)
        input_box = self.driver.find_element(
            By.XPATH, "//*[starts-with(@id, 'betslip-wager-box__input')]"
        )
        input_box.click()
        input_box.clear()
        input_box.send_keys(str(bet_amount))

        # Example implementation:
        # bet_amount_input = self.wait.until(EC.element_to_be_clickable((By.ID, "bet-amount")))
        # bet_amount_input.clear()
        # bet_amount_input.send_keys(str(bet_amount))
        #
        # side_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{side}')]")))
        # side_button.click()

    @override
    def verify_odds(self, odds: float):
        """Verify the odds are correct"""
        pass

    @override
    def place_bet(self):
        """Place a bet"""
        pass

    @override
    def clear_betslip(self):
        """Clear the betslip"""

        self.driver.find_element(
            By.XPATH,
            "//*[@id='dk-betslip-shell__wrapper']/div/div[2]/div/div/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div[1]/div[1]/svg",
        ).click()
