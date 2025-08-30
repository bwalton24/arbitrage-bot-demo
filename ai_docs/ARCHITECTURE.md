# Arbitrage Bot Code Architecture

## Overview

The bot follows a modular architecture with clear abstractions for odds fetching, arbitrage detection, and browser automation. The main orchestrator coordinates all operations in a continuous loop.

## Core Components

### 1. Main Loop (Orchestrator)

```python
class ArbitrageOrchestrator:
    def run_continuous_loop(self):
        while True:
            # 1. Fetch odds from all sportsbooks
            # 2. Detect arbitrage opportunities
            # 3. Execute browser actions for opportunities
            # 4. Wait for next iteration
```

### 2. Odds Fetching Abstraction

```python
class OddsFetcher(ABC):
    @abstractmethod
    def fetch_odds(self) -> List[GameOdds]:
        """Fetch current odds from sportsbook"""
        pass

class DraftKingsOddsFetcher(OddsFetcher):
    def fetch_odds(self) -> List[GameOdds]:
        # Implementation for DraftKings

class FanDuelOddsFetcher(OddsFetcher):
    def fetch_odds(self) -> List[GameOdds]:
        # Implementation for FanDuel
```

### 3. Arbitrage Detection Engine

```python
class ArbitrageDetector:
    def detect_opportunities(self, all_odds: Dict[str, List[GameOdds]]) -> List[ArbitrageOpportunity]:
        """
        Input: Odds from all sportsbooks
        Output: List of arbitrage opportunities
        """
        # 1. Standardize team names
        # 2. Match games across sportsbooks
        # 3. Calculate arbitrage potential
        # 4. Filter by profit threshold
```

### 4. Browser Automation Abstraction

```python
class BrowserAutomation(ABC):
    @abstractmethod
    def open_game_page(self, game_id: str):
        """Navigate to specific game page"""
        pass

    @abstractmethod
    def fill_betslip(self, bet_amount: float, side: str):
        """Fill betslip with calculated amount"""
        pass

class DraftKingsBrowser(BrowserAutomation):
    # Implementation for DraftKings browser actions

class FanDuelBrowser(BrowserAutomation):
    # Implementation for FanDuel browser actions
```

### 5. Multi-threaded Browser Orchestrator

```python
class BrowserOrchestrator:
    def execute_arbitrage_actions(self, opportunity: ArbitrageOpportunity):
        """
        Execute browser actions for both sportsbooks simultaneously
        """
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Submit tasks for both sportsbooks
            futures = [
                executor.submit(self._execute_for_book, opportunity.book1),
                executor.submit(self._execute_for_book, opportunity.book2)
            ]
            # Wait for both to complete
            wait(futures)
```

## Data Models

### GameOdds

```python
@dataclass
class GameOdds:
    sportsbook: str
    game_id: str
    team1: str
    team2: str
    team1_odds: float
    team2_odds: float
```

### ArbitrageOpportunity

```python
@dataclass
class ArbitrageOpportunity:
    game_id: str
    team1: str
    team2: str
    book1: str
    book2: str
    book1_side: str  # "team1" or "team2"
    book2_side: str
    book1_odds: float
    book2_odds: float
    profit_percentage: float
    bet1_amount: float
    bet2_amount: float
    total_profit: float
```

## File Structure

```
arbitrage_bot/
├── main.py                 # Entry point with main loop
├── orchestrator.py         # Main orchestrator class
├── odds/
│   ├── __init__.py
│   ├── base.py            # OddsFetcher abstract class
│   ├── draftkings.py      # DraftKings implementation
│   ├── fanduel.py         # FanDuel implementation
│   └── betmgm.py          # BetMGM implementation
├── detection/
│   ├── __init__.py
│   ├── detector.py        # ArbitrageDetector class
│   └── team_mapper.py     # Team name standardization
├── browser/
│   ├── __init__.py
│   ├── base.py            # BrowserAutomation abstract class
│   ├── draftkings.py      # DraftKings browser actions
│   ├── fanduel.py         # FanDuel browser actions
│   └── betmgm.py          # BetMGM browser actions
├── models/
│   ├── __init__.py
│   ├── odds.py            # GameOdds data class
│   └── arbitrage.py       # ArbitrageOpportunity data class
└── config/
    ├── __init__.py
    ├── settings.py        # Configuration management
    └── team_mappings.json # Team name mappings
```

## Execution Flow

1. **Main Loop**: Orchestrator starts continuous monitoring
2. **Odds Fetching**: All sportsbook fetchers run in parallel
3. **Arbitrage Detection**: Single-threaded analysis of all odds
4. **Browser Actions**: Multi-threaded execution for both books
5. **Logging**: Record opportunities and actions taken
