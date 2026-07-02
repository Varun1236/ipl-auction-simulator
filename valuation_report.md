# Player Valuation Report — IPL 2025 Season

Generated from `data/master_players.csv` — 186 players

## Formula

### Batsmen & Wicketkeepers

score = 35% × Runs(normalised) + 20% × BattingAverage(normalised) + 25% × StrikeRate(normalised) + 10% × 100s(normalised) + 10% × 50s(normalised)

### Bowlers

score = 35% × Wickets(normalised) + 35% × Economy⁻¹(normalised) + 30% × BowlingAverage⁻¹(normalised)

Economy and Bowling Average are inverted — lower raw values yield higher scores.

### All-Rounders

score = (batting_score + bowling_score) / 2
If only batting or only bowling data is available, that single component is used.

## Normalisation

All raw statistics are min-max scaled to 0–100 across the player pool:

```
normalised = (value - min) / (max - min) × 100
```

For inverted metrics (Economy, Bowling Average):

```
normalised = (max - value) / (max - min) × 100
```

After computing the weighted sum, the final score is re-normalised to 0–100 across all players.

## Statistical Ranges

| Metric | Min | Max |
|--------|-----|-----|
| Runs | 2 | 759 |
| Batting Average | 0.0 | 65.2 |
| Strike Rate | 40.0 | 214.3 |
| 100s | 0 | 1 |
| 50s | 0 | 8 |
| Wickets | 1 | 25 |
| Economy | 6.5 | 14.1 |
| Bowling Average | 15.9 | 133.0 |

## Summary Statistics

| Role | Count | Mean Score | Min Score | Max Score |
|------|-------|------------|-----------|-----------|
| Batsman | 74 | 39.4 | 0.0 | 94.3 |
| Bowler | 85 | 60.6 | 10.9 | 100.0 |
| All-Rounder | 8 | 52.8 | 43.1 | 59.2 |
| Wicketkeeper | 19 | 49.0 | 24.7 | 77.7 |

| **All** | 186 | 46.6 | 1.1 | 90.9 |

## Top 20 Players by Value

| Rank | Player | Role | Score | Price (Cr) |
|------|--------|------|-------|------------|
| 1 | M Prasidh Krishna (GT) | Bowler | 100.0 | 9.5 Cr |
| 2 | Noor Ahmad (CSK) | Bowler | 99.7 | 10.0 Cr |
| 3 | JJ Bumrah (MI) | Bowler | 97.4 | 18.0 Cr |
| 4 | B Sai Sudharsan (GT) | Batsman | 94.3 | 8.5 Cr |
| 5 | JR Hazlewood (RCB) | Bowler | 93.1 | 12.5 Cr |
| 6 | TA Boult (MI) | Bowler | 90.5 | 12.5 Cr |
| 7 | CV Varun (KKR) | Bowler | 89.3 | 12.0 Cr |
| 8 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 18.0 Cr |
| 9 | Kuldeep Yadav (DC) | Bowler | 88.6 | 13.2 Cr |
| 10 | MR Marsh (LSG) | Batsman | 86.7 | 3.4 Cr |
| 11 | SA Yadav (MI) | Batsman | 85.2 | 16.4 Cr |
| 12 | R Sai Kishore (GT) | Bowler | 85.0 | 2.0 Cr |
| 13 | JD Unadkat (SRH) | Bowler | 83.1 | 1.0 Cr |
| 14 | B Kumar (RCB) | Bowler | 79.3 | 10.8 Cr |
| 15 | DS Rathi (LSG) | Bowler | 79.1 | 0.3 Cr |
| 16 | V Kohli (RCB) | Batsman | 79.0 | 21.0 Cr |
| 17 | PJ Cummins (SRH) | Bowler | 78.9 | 18.0 Cr |
| 18 | M Jansen (PBKS) | Bowler | 78.5 | 7.0 Cr |
| 19 | KL Rahul (DC) | Wicketkeeper | 77.7 | 14.0 Cr |
| 20 | E Malinga (SRH) | Bowler | 77.5 | 1.2 Cr |

## Bottom 20 Players by Value

| Rank | Player | Role | Score | Price (Cr) |
|------|--------|------|-------|------------|
| 167 | RA Bawa (MI) | Batsman | 24.6 | 0.3 Cr |
| 168 | Sediqullah Atal (DC) | Batsman | 22.9 | N/A |
| 169 | MM Sharma (DC) | Bowler | 21.3 | 3.8 Cr |
| 170 | A Taide (SRH) | Batsman | 20.5 | N/A |
| 171 | Ramandeep Singh (KKR) | Batsman | 19.4 | 13.0 Cr |
| 172 | SK Rasheed (CSK) | Batsman | 18.8 | N/A |
| 173 | Simarjeet Singh (SRH) | Bowler | 18.2 | 5.5 Cr |
| 174 | MP Breetzke (LSG) | Batsman | 16.4 | 0.8 Cr |
| 175 | A Manohar (SRH) | Batsman | 15.6 | N/A |
| 176 | J Fraser-McGurk (DC) | Batsman | 15.1 | N/A |
| 177 | RA Tripathi (CSK) | Batsman | 14.3 | 0.8 Cr |
| 178 | Shahbaz Ahmed (LSG) | Batsman | 13.8 | 2.4 Cr |
| 179 | SH Johnson (KKR) | Bowler | 10.9 | N/A |
| 180 | R Powell (KKR) | Batsman | 10.2 | 1.5 Cr |
| 181 | PWA Mulder (SRH) | Batsman | 8.9 | N/A |
| 182 | Fazalhaq Farooqi (RR) | Batsman | 8.4 | N/A |
| 183 | DJ Hooda (CSK) | Batsman | 8.1 | N/A |
| 184 | M Tiwari (DC) | Batsman | 5.4 | 0.4 Cr |
| 185 | Suryansh Shedge (PBKS) | Batsman | 3.6 | 0.3 Cr |
| 186 | R Minz (MI) | Batsman | 0.0 | 0.7 Cr |
