# Arbitrage Bot Architecture Diagram

## System Overview

```mermaid
graph TB
    subgraph "Main Application"
        Main[main.py<br/>Entry Point]
        Orchestrator[ArbitrageOrchestrator<br/>Main Controller]
    end

    subgraph "Odds Fetching Layer"
        OddsBase[OddsFetcher<br/>Abstract Base]
        DK[DraftKingsOddsFetcher]
        FD[FanDuelOddsFetcher]
        BM[BetMGMOddsFetcher]
    end

    subgraph "Detection Engine"
        Detector[ArbitrageDetector<br/>Analysis Engine]
        TeamMapper[TeamMapper<br/>Name Standardization]
    end

    subgraph "Browser Automation Layer"
        BrowserBase[BrowserAutomation<br/>Abstract Base]
        DKBrowser[DraftKingsBrowser]
        FDBrowser[FanDuelBrowser]
        BMBrowser[BetMGMBrowser]
        BrowserOrch[BrowserOrchestrator<br/>Multi-threaded Execution]
    end

    subgraph "Data Models"
        GameOdds[GameOdds<br/>Data Class]
        ArbitrageOpp[ArbitrageOpportunity<br/>Data Class]
    end

    subgraph "Configuration"
        Settings[settings.py<br/>Configuration]
        TeamMappings[team_mappings.json<br/>Team Name Mappings]
    end

    %% Main flow connections
    Main --> Orchestrator
    Orchestrator --> OddsBase
    Orchestrator --> Detector
    Orchestrator --> BrowserOrch

    %% Odds fetching inheritance
    OddsBase -.->|implements| DK
    OddsBase -.->|implements| FD
    OddsBase -.->|implements| BM

    %% Browser automation inheritance
    BrowserBase -.->|implements| DKBrowser
    BrowserBase -.->|implements| FDBrowser
    BrowserBase -.->|implements| BMBrowser

    %% Data flow
    DK --> GameOdds
    FD --> GameOdds
    BM --> GameOdds
    GameOdds --> Detector
    Detector --> TeamMapper
    TeamMapper --> ArbitrageOpp
    ArbitrageOpp --> BrowserOrch

    %% Configuration dependencies
    Settings --> Orchestrator
    TeamMappings --> TeamMapper

    %% Browser orchestrator connections
    BrowserOrch --> DKBrowser
    BrowserOrch --> FDBrowser
    BrowserOrch --> BMBrowser

    classDef mainClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef abstractClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef concreteClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef dataClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef configClass fill:#fce4ec,stroke:#880e4f,stroke-width:2px

    class Main,Orchestrator mainClass
    class OddsBase,BrowserBase abstractClass
    class DK,FD,BM,DKBrowser,FDBrowser,BMBrowser,BrowserOrch,Detector,TeamMapper concreteClass
    class GameOdds,ArbitrageOpp dataClass
    class Settings,TeamMappings configClass
```

## Execution Flow Diagram

```mermaid
sequenceDiagram
    participant Main as Main Loop
    participant Orch as Orchestrator
    participant Odds as Odds Fetchers
    participant Det as Detector
    participant Browser as Browser Automation
    participant Config as Configuration

    Main->>Orch: Start continuous loop
    loop Every iteration
        Orch->>Odds: Fetch odds from all sportsbooks
        Odds-->>Orch: Return GameOdds objects

        Orch->>Det: Detect arbitrage opportunities
        Det->>Config: Get team mappings
        Config-->>Det: Return standardized names
        Det-->>Orch: Return ArbitrageOpportunity list

        alt Found opportunities
            Orch->>Browser: Execute browser actions
            Browser->>Browser: Multi-threaded execution
            Browser-->>Orch: Action results
        end

        Orch->>Orch: Wait for next iteration
    end
```

## Component Relationships

```mermaid
graph LR
    subgraph "Core Components"
        A[Orchestrator]
        B[Odds Layer]
        C[Detection Engine]
        D[Browser Layer]
    end

    subgraph "Supporting Components"
        E[Data Models]
        F[Configuration]
        G[Team Mapping]
    end

    A --> B
    A --> C
    A --> D
    B --> E
    C --> E
    C --> G
    D --> E
    F --> A
    F --> C
    G --> C

    classDef core fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef support fill:#f1f8e9,stroke:#388e3c,stroke-width:2px

    class A,B,C,D core
    class E,F,G support
```

## File Structure Visualization

```mermaid
graph TD
    subgraph "arbitrage_bot/"
        Main[main.py]
        Orch[orchestrator.py]

        subgraph "odds/"
            OddsInit[__init__.py]
            OddsBase[base.py]
            DK[draftkings.py]
            FD[fanduel.py]
            BM[betmgm.py]
        end

        subgraph "detection/"
            DetInit[__init__.py]
            Detector[detector.py]
            TeamMap[team_mapper.py]
        end

        subgraph "browser/"
            BrowserInit[__init__.py]
            BrowserBase[base.py]
            DKBrowser[draftkings.py]
            FDBrowser[fanduel.py]
            BMBrowser[betmgm.py]
        end

        subgraph "models/"
            ModelsInit[__init__.py]
            OddsModel[odds.py]
            ArbitrageModel[arbitrage.py]
        end

        subgraph "config/"
            ConfigInit[__init__.py]
            Settings[settings.py]
            TeamMappings[team_mappings.json]
        end
    end

    Main --> Orch
    Orch --> OddsBase
    Orch --> Detector
    Orch --> BrowserBase
    Detector --> TeamMap
    OddsBase --> OddsModel
    Detector --> ArbitrageModel
    Settings --> Orch
    TeamMappings --> TeamMap

    classDef entryPoint fill:#ffebee,stroke:#c62828,stroke-width:3px
    classDef core fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef module fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef config fill:#fff3e0,stroke:#ef6c00,stroke-width:2px

    class Main entryPoint
    class Orch core
    class OddsBase,Detector,BrowserBase module
    class Settings,TeamMappings config
```

## Key Design Patterns

1. **Abstract Factory Pattern**: OddsFetcher and BrowserAutomation abstract classes
2. **Strategy Pattern**: Different implementations for each sportsbook
3. **Observer Pattern**: Continuous monitoring loop
4. **Command Pattern**: Browser actions as executable commands
5. **Data Transfer Objects**: GameOdds and ArbitrageOpportunity classes

## Threading Model

-   **Main Thread**: Orchestrator and arbitrage detection
-   **Worker Threads**: Parallel odds fetching from multiple sportsbooks
-   **Browser Threads**: Simultaneous browser automation for both sportsbooks in an opportunity


