# IPL Auction Simulator — Agent Guide

## Project

Multi-agent IPL auction simulation where AI-controlled franchises bid on players and construct squads.

## Teams (10 franchises)

MI, CSK, RCB, RR, KKR, GT, LSG, PBKS, DC, SRH

## Commands

```sh
python3 valuation.py          # compute PlayerValueScore (0-100)
python3 auction_engine.py     # run sealed-bid auction
```

Run in order — `auction_engine.py` reads `data/player_values.csv` produced by `valuation.py`.

## Directory structure

| Path | Purpose |
|------|---------|
| `valuation.py` | Computes PlayerValueScore from performance stats |
| `auction_engine.py` | Runs auction, generates results CSV |
| `agents/` | AI franchise agent implementations (empty) |
| `data/master_players.csv` | Player pool (51 IPL players with stats) |
| `data/player_values.csv` | Valuation output (0-100 score per player) |
| `data/auction_results.csv` | Auction output (winner + price per player) |
| `docs/` | Research notes, analysis (empty) |
| `scripts/` | Automation, simulation runner (empty) |

## Scoring logic (`valuation.py`)

- **Batters** (Batsman, Wicketkeeper): 60% Runs + 40% StrikeRate
- **Bowlers**: 60% Wickets + 40% Economy (inverted — lower is better)
- **All-rounders**: average of batting and bowling halves
- All metrics min-max scaled to 0-100 before combining
- **Age adjustment**: 24-30 → +10%; >34 → -15%
- Final result re-normalised to 0-100 across all players
- Non-bowlers' Economy set to worst-bowler value to avoid spurious advantage

## Auction rules (`auction_engine.py`)

- 10 teams, each starts with 120 Cr
- Players auctioned in descending PlayerValueScore order
- `max_bid = adjusted_score / 100 * 20` (capped at remaining budget)
- `adjusted_score = PlayerValueScore * team_strategy_multiplier`
- Highest bid wins; tie-break by team list order
- Winner pays their bid; budget deducted
- Max squad size: 8 players per team (teams at cap cannot bid)

## Team strategies

| Team | Boost | Trigger |
|------|-------|---------|
| MI | +20% | PlayerValueScore > 80 |
| CSK | +15% | Age >= 30 |
| RR | +20% | Age < 26 |
| RCB | +15% | Role is Batsman |
| KKR | +15% | Role is Bowler |
| GT | +10% | Role is AllRounder |
| LSG | +10% | Role is Wicketkeeper |
| PBKS | +10% | StrikeRate >= median |
| DC | +10% | Age < 28 |
| SRH | +15% | Batsman with StrikeRate >= batter median |

## Research questions (from PROJECT_SPEC.md)

1. Which franchise strategy produces the highest ROI?
2. Which players are consistently overvalued / undervalued?
3. How do AI decisions compare with real IPL auction outcomes?
