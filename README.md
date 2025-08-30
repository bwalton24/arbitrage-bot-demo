# Arbitrage Sports Betting Bot

> **⚠️ IMPORTANT DISCLAIMER** ⚠️
>
> **GAMBLING DISCLAIMER**: This software is for educational and research purposes only. Sports betting involves significant financial risk and may result in substantial losses. Users are responsible for:
>
> -   Compliance with all local, state, and federal gambling laws and regulations
> -   Adherence to sportsbook terms of service and user agreements
> -   Understanding that past performance does not guarantee future results
> -   Ensuring all betting activities are legal in their jurisdiction
> -   Consulting with legal and financial professionals before engaging in any betting activities
>
> **TERMS OF SERVICE**: Users must comply with all sportsbook terms of service, including but not limited to:
>
> -   Prohibitions on automated betting or bot usage
> -   Restrictions on arbitrage betting
> -   Account verification requirements
> -   Responsible gambling policies
>
> The developers of this software are not responsible for any financial losses, legal issues, or violations of terms of service that may result from its use.

---

A sophisticated Python system for detecting and executing arbitrage opportunities across multiple sportsbooks with real-time odds fetching and browser automation.

## Features

-   **Real-Time Odds Collection**: Fetch live odds from actual sportsbook APIs (DraftKings, BetMGM)
-   **Advanced Team Name Standardization**: Intelligent mapping of team names across different sportsbooks
-   **Arbitrage Detection Engine**: Sophisticated algorithm for finding profitable arbitrage opportunities
-   **Browser Automation**: Automated bet placement with Selenium WebDriver
-   **Multi-threading**: Parallel execution for faster processing and simultaneous bet placement
-   **Modular Architecture**: Easy to add new sportsbooks and betting strategies
-   **Configuration Management**: Flexible settings system with JSON configuration
-   **Comprehensive Logging**: Detailed logging for monitoring and debugging
-   **Error Handling**: Robust error handling and recovery mechanisms

## Architecture

The bot follows a modular, production-ready architecture with clear abstractions:

```
arbitrage_bot/
├── main.py                 # Entry point with main loop
├── orchestrator.py         # Main orchestrator class with multi-threading
├── odds/                   # Real API integration for odds fetching
│   ├── base.py            # Abstract base class for odds fetchers
│   ├── draftkings.py      # DraftKings API integration
│   └── betmgm.py          # BetMGM API integration
├── detection/              # Arbitrage detection engine
│   ├── detector.py        # Core arbitrage detection logic
│   └── team_mapper.py     # Team name standardization
├── browser/                # Browser automation with Selenium
│   ├── base.py            # Abstract base class for browser automation
│   ├── draftkings.py      # DraftKings browser automation
│   └── betmgm.py          # BetMGM browser automation
├── models/                 # Data models and enums
│   ├── odds.py            # Game odds data structures
│   ├── arbitrage.py       # Arbitrage opportunity models
│   └── sportsbooks.py     # Sportsbook enum definitions
└── config/                 # Configuration management
    └── settings.py        # Settings class with file I/O
```

### Core Components

1. **OddsFetcher (Abstract)**: Base class for fetching real-time odds from sportsbook APIs
2. **ArbitrageDetector**: Advanced detection engine with team name standardization
3. **BrowserAutomation (Abstract)**: Base class for automated browser actions
4. **ArbitrageOrchestrator**: Main coordinator with multi-threading and error handling
5. **TeamMapper**: Intelligent team name standardization across sportsbooks

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd arbitrage-bot-demo
```

2. Install dependencies using uv (recommended) or pip:

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

3. Install Chrome WebDriver for browser automation:

```bash
# Download ChromeDriver from https://chromedriver.chromium.org/
# and add it to your PATH, or use webdriver-manager
pip install webdriver-manager
```

## Usage

### Quick Start

Run the main bot:

```bash
uv run main.py
```

### Configuration

The bot uses a flexible configuration system that can be customized:

```python
from arbitrage_bot.config import Settings
from arbitrage_bot.models.sportsbooks import Sportsbook

settings = Settings(
    sportsbooks=[Sportsbook.DRAFTKINGS, Sportsbook.BETMGM],
    min_profit_percentage=1.0,  # Minimum profit percentage required
    total_bet_amount=100.0,     # Total amount to bet across both sides
    refresh_interval_seconds=5,  # How often to check for opportunities
    enable_browser_automation=True  # Set to False for simulation only
)
```

### Configuration File

Create a `config/settings.json` file for persistent configuration:

```json
{
    "sportsbooks": ["draftkings", "betmgm"],
    "min_profit_percentage": 1.0,
    "total_bet_amount": 100.0,
    "refresh_interval_seconds": 5,
    "enable_browser_automation": true
}
```

## Supported Sportsbooks

Currently implemented with real API integration:

### DraftKings

-   **API Integration**: Real-time odds fetching from DraftKings API
-   **Browser Automation**: Automated bet placement with Selenium
-   **Features**: Moneyline betting, direct URL generation

### BetMGM

-   **API Integration**: Real-time odds fetching from BetMGM API
-   **Browser Automation**: Automated bet placement with Selenium
-   **Features**: Moneyline betting, direct URL generation

## Adding New Sportsbooks

To add a new sportsbook:

1. Create a new odds fetcher:

```python
class NewSportsbookOddsFetcher(OddsFetcher):
    def fetch_odds(self) -> List[GameOdds]:
        # Implement real API integration
        # Return list of GameOdds objects
        pass
```

2. Create a new browser automation:

```python
class NewSportsbookBrowser(BrowserAutomation):
    def fill_betslip(self, bet_amount: float):
        # Implement actual betslip filling with Selenium
        pass

    def verify_odds(self, odds: float):
        # Implement odds verification
        pass

    def place_bet(self):
        # Implement actual bet placement
        pass

    def clear_betslip(self):
        # Implement betslip clearing
        pass
```

3. Add to the orchestrator's setup methods and update the Sportsbook enum.

## Arbitrage Detection

The bot uses a sophisticated arbitrage detection system:

### Team Name Standardization

-   **Intelligent Mapping**: Maps team names across different sportsbooks
-   **Fuzzy Matching**: Handles variations in team names and abbreviations
-   **Consistent Keys**: Creates standardized game identifiers

### Opportunity Detection

1. **Real-time Data**: Fetches live odds from multiple sportsbooks
2. **Game Matching**: Matches games across different books using standardized team names
3. **Profit Calculation**: Calculates optimal bet amounts for guaranteed profit
4. **Threshold Filtering**: Filters opportunities by minimum profit percentage

### Example Arbitrage Calculation

For a Lakers vs Warriors game:

-   DraftKings: Lakers +110, Warriors -120
-   BetMGM: Lakers +115, Warriors -125

The bot calculates optimal bet amounts to guarantee profit regardless of outcome.

## Browser Automation

The bot includes sophisticated browser automation:

### Multi-threading

-   **Parallel Execution**: Simultaneous bet placement across sportsbooks
-   **Error Handling**: Robust error recovery and betslip clearing
-   **Timeout Management**: Configurable timeouts for web interactions

### Automation Features

-   **Direct URL Navigation**: Navigates directly to specific betting pages
-   **Betslip Filling**: Automatically fills bet amounts
-   **Odds Verification**: Verifies odds haven't changed before placing bets
-   **Betslip Clearing**: Cleans up betslips after completion or errors

## Development

### Project Structure

-   `models/`: Data classes for odds, arbitrage opportunities, and sportsbook enums
-   `odds/`: Real API integration for odds fetching
-   `detection/`: Arbitrage detection logic and team name standardization
-   `browser/`: Selenium-based browser automation
-   `config/`: Configuration management with file I/O
-   `orchestrator.py`: Main coordination logic with multi-threading

### Logging

The bot provides comprehensive logging:

-   **File Logging**: All activities logged to `arbitrage_bot.log`
-   **Console Output**: Real-time status updates
-   **Error Tracking**: Detailed error information for debugging

## Dependencies

### Core Dependencies

-   **selenium**: Browser automation and web scraping
-   **curl-cffi**: Advanced HTTP requests with browser impersonation
-   **requests**: HTTP requests for API integration

### Development Dependencies

-   **ruff**: Fast Python linter and formatter
-   **uv**: Fast Python package manager

## API Integration

The bot uses real sportsbook APIs:

### DraftKings API

-   **Endpoint**: `https://sportsbook-nash.draftkings.com/sites/US-MI-SB/api/sportscontent/controldata/league/leagueSubcategory/v1/markets`
-   **Features**: Real-time odds, event data, market information

### BetMGM API

-   **Endpoint**: `https://www.mi.betmgm.com/cds-api/bettingoffer/fixtures`
-   **Features**: Live fixtures, odds data, participant information

## Legal Disclaimer

This software is for educational and research purposes only. Users are responsible for:

-   Compliance with local gambling laws and regulations
-   Adherence to sportsbook terms of service
-   Understanding the risks involved in sports betting
-   Ensuring all betting activities are legal in their jurisdiction

## License

MIT License

Copyright (c) 2025 Arbitrage Bot Demo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
