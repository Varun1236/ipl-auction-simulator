# Market Validation Report — PlayerValueScore vs AuctionPrice

Generated from `data/master_players.csv` and `data/player_values.csv` — 158 matched players

## Correlation Statistics

| Metric | Value |
|--------|-------|
| Pearson r | 0.3670 |
| Spearman ρ | 0.3296 |
| Sample size | 158 |
| Mean Score | 53.4 |
| Mean Price | 6.7 |

### Interpretation

The Pearson correlation of **0.3670** indicates a **weak positive** linear relationship between PlayerValueScore and AuctionPrice. The Spearman and Pearson values are similar, suggesting a roughly linear relationship. Auction prices are influenced by factors beyond performance stats — brand value, fan following, international form, and team-specific needs.

## Regression Details

```
price = 0.1140 × score + 0.59
```

Players above the regression line cost more than their score predicts (negative outliers). Players below the line cost less than their score predicts (positive outliers).

## Top 20 Positive Outliers (Undervalued by Market)

These players have higher scores than their auction price suggests — market bargains.

| Rank | Player | Role | Score | Price (Cr) | Residual |
|------|--------|------|-------|------------|----------|
| 1 | DS Rathi (LSG) | Bowler | 79.1 | 0.3 | -9.3 |
| 2 | JD Unadkat (SRH) | Bowler | 83.1 | 1.0 | -9.1 |
| 3 | R Sai Kishore (GT) | Bowler | 85.0 | 2.0 | -8.3 |
| 4 | E Malinga (SRH) | Bowler | 77.5 | 1.2 | -8.2 |
| 5 | AS Roy (KKR) | Bowler | 66.7 | 0.4 | -7.8 |
| 6 | V Puthur (MI) | Bowler | 65.4 | 0.3 | -7.7 |
| 7 | Harpreet Brar (PBKS) | Bowler | 73.9 | 1.5 | -7.5 |
| 8 | VG Arora (KKR) | Bowler | 75.9 | 1.8 | -7.4 |
| 9 | Akash Singh (LSG) | Bowler | 61.4 | 0.3 | -7.3 |
| 10 | Ashwani Kumar (MI) | Bowler | 61.2 | 0.3 | -7.3 |
| 11 | HS Dubey (SRH) | Bowler | 59.7 | 0.3 | -7.1 |
| 12 | MR Marsh (LSG) | Batsman | 86.7 | 3.4 | -7.1 |
| 13 | MJ Santner (MI) | Bowler | 74.1 | 2.0 | -7.0 |
| 14 | N Thushara (RCB) | Bowler | 68.3 | 1.6 | -6.8 |
| 15 | V Sooryavanshi (RR) | Batsman | 63.1 | 1.1 | -6.7 |
| 16 | PW Hasaranga (RR) | Bowler | 69.3 | 2.0 | -6.5 |
| 17 | PHKD Mendis (SRH) | Bowler | 58.1 | 0.8 | -6.4 |
| 18 | P Dubey (PBKS) | Bowler | 52.0 | 0.3 | -6.2 |
| 19 | V Nigam (DC) | All-Rounder | 52.2 | 0.5 | -6.0 |
| 20 | Zeeshan Ansari (SRH) | Bowler | 50.8 | 0.4 | -6.0 |

> Most are low-cost bowlers with strong performance stats. The market systematically underprices bowling performance.

## Top 20 Negative Outliers (Overvalued by Market)

These players have lower scores relative to their auction price — market overpays.

| Rank | Player | Role | Score | Price (Cr) | Residual |
|------|--------|------|-------|------------|----------|
| 1 | RR Pant (LSG) | Wicketkeeper | 48.3 | 27.0 | 20.9 |
| 2 | SS Iyer (PBKS) | Batsman | 76.9 | 26.8 | 17.4 |
| 3 | H Klaasen (SRH) | Wicketkeeper | 72.6 | 23.0 | 14.1 |
| 4 | RD Gaikwad (CSK) | Batsman | 33.7 | 18.0 | 13.6 |
| 5 | SV Samson (RR) | Wicketkeeper | 42.9 | 18.0 | 12.5 |
| 6 | N Pooran (LSG) | Wicketkeeper | 72.5 | 21.0 | 12.1 |
| 7 | V Kohli (RCB) | Batsman | 79.0 | 21.0 | 11.4 |
| 8 | Rashid Khan (GT) | Bowler | 57.8 | 18.0 | 10.8 |
| 9 | AR Patel (DC) | All-Rounder | 47.8 | 16.5 | 10.5 |
| 10 | Ramandeep Singh (KKR) | Batsman | 19.4 | 13.0 | 10.2 |
| 11 | M Pathirana (CSK) | Bowler | 67.2 | 18.0 | 9.7 |
| 12 | RG Sharma (MI) | Batsman | 53.4 | 16.3 | 9.6 |
| 13 | YBK Jaiswal (RR) | Batsman | 69.6 | 18.0 | 9.5 |
| 14 | HH Pandya (MI) | All-Rounder | 55.7 | 16.4 | 9.5 |
| 15 | LS Livingstone (RCB) | Batsman | 26.2 | 13.0 | 9.4 |
| 16 | YS Chahal (PBKS) | Bowler | 76.7 | 18.0 | 8.7 |
| 17 | PJ Cummins (SRH) | Bowler | 78.9 | 18.0 | 8.4 |
| 18 | RK Singh (KKR) | Batsman | 37.5 | 13.0 | 8.1 |
| 19 | KV Sharma (MI) | Bowler | 69.8 | 16.3 | 7.8 |
| 20 | DC Jurel (RR) | Wicketkeeper | 49.8 | 14.0 | 7.7 |

> High-priced retained stars (Pant, Iyer, Kohli, Bumrah) dominate this list. Their market price reflects brand/fan value beyond raw performance scores.

## Summary

| Question | Answer |
|----------|--------|
| Does the valuation model explain auction prices? | Weakly — performance explains some variance but brand/legacy factors dominate. |
| What drives outliers? | Brand value, captaincy, fan following, international reputation |
| Best market inefficiency | Bowling talent at base price (0.3 Cr) |
| Biggest premium | Elite Indian batsmen / wicketkeepers |
