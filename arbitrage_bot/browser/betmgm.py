import time
from typing import override
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from arbitrage_bot.browser.base import BrowserAutomation
from arbitrage_bot.models.sportsbooks import Sportsbook


class BetMGMBrowser(BrowserAutomation):
    """BetMGM browser automation implementation"""

    def __init__(self):
        super().__init__(Sportsbook.BETMGM)
        self.base_url = "https://sports.betmgm.com"

    @override
    def fill_betslip(self, bet_amount: float):
        """Fill betslip with calculated amount on BetMGM"""
        # TODO: Implement actual betslip filling
        # For now, just log the action
        print(f"[BetMGM] Would place bet: ${bet_amount:.2f}")

        time.sleep(3)
        input_box = self.driver.find_element(
            By.XPATH, "//*[@class='stake-input-value']"
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
            "//*[@id='main-content']/ms-main/div[1]/ng-scrollbar[2]/div/div/div/div/ms-widget-column/ms-widget-slot/ms-bet-column/ds-card/ds-tabs-group/div[2]/ds-tab[1]/div[1]/bs-betslip/bs-betslip-linear-edit-state/div/div/div/div/bs-betslip-linear-type-list/div/bs-digital-picks-linear-toolbar/span/div/span[2]",
        ).click()
