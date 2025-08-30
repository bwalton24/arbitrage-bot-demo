from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class BrowserAutomation(ABC):
    """Abstract base class for browser automation"""

    def __init__(self, sportsbook: str):
        self.sportsbook = sportsbook
        self.driver = self.setup_driver()
        self.wait = None

    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.wait = WebDriverWait(self.driver, 10)
        return self.driver

    def close_driver(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()

    def open_url(self, url: str):
        """Open a URL in the browser"""
        self.driver.get(url)

    @abstractmethod
    def fill_betslip(self, bet_amount: float) -> bool:
        """Fill betslip with calculated amount"""
        pass

    @abstractmethod
    def verify_odds(self, odds: float) -> bool:
        """Verify the odds are correct"""
        pass

    @abstractmethod
    def place_bet(self) -> bool:
        """Place a bet"""
        pass

    @abstractmethod
    def clear_betslip(self):
        """Clear the betslip"""
        pass

    def get_sportsbook(self) -> str:
        """Get the name of this sportsbook"""
        return self.sportsbook
