# Arbitrage Sports Betting Bot Requirements

## Core Features

### 1. Live Odds Collection

-   Scrape real-time odds from multiple sportsbooks
-   Support for major sportsbooks (DraftKings, FanDuel, BetMGM, etc.)
-   Handle rate limiting and anti-bot measures
-   Process odds in real-time (no storage needed)

### 2. Team Name Standardization

-   Map team names across different sportsbooks
-   Handle variations (e.g., "Lakers" vs "LA Lakers" vs "Los Angeles Lakers")
-   Maintain a configurable team name mapping database
-   Support for multiple sports (NBA, NFL, MLB, etc.)

### 3. Arbitrage Detection

-   Compare odds for identical matchups across sportsbooks
-   Calculate potential profit margins
-   Identify minimum bet thresholds for profitable arbitrage
-   Filter opportunities by minimum profit percentage

### 4. Browser Automation

-   Open dedicated browser tabs for each sportsbook
-   Navigate to specific game/match pages
-   Update tabs when arbitrage opportunities are found
-   No login required for proof of concept

### 5. Bet Placement (Proof of Concept)

-   Calculate optimal bet sizes for each side of arbitrage
-   Log potential bet opportunities with calculated amounts
-   No actual bet placement for proof of concept
-   Track identified opportunities for analysis
