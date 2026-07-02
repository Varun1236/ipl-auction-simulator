# Mispricing Analysis Report

Based on `data/value_analysis.csv` — 158 players with valid AuctionPrice.
ExpectedPrice = mean AuctionPrice of players in same PlayerValueScore decile.
PriceDifference = AuctionPrice − ExpectedPrice.  Negative = undervalued, Positive = overvalued.

## Decile Reference

| Decile | Score Range | Mean Price (Cr) | Count |
|--------|-------------|-----------------|-------|
| 0 | 79.0–100.0 | 10.57 | 16 |
| 1 | 72.6–78.9 | 10.88 | 16 |
| 2 | 65.4–72.5 | 9.19 | 16 |
| 3 | 57.8–65.1 | 5.49 | 16 |
| 4 | 53.1–57.6 | 5.78 | 15 |
| 5 | 47.9–52.3 | 6.15 | 16 |
| 6 | 41.9–47.8 | 6.46 | 16 |
| 7 | 35.9–41.7 | 3.98 | 16 |
| 8 | 28.4–35.3 | 4.38 | 16 |
| 9 | 0.0–28.2 | 3.67 | 15 |

---

## Top 25 Most Undervalued Players

Players costing **less** than their score-decile peers.

| Rank | Player | Role | Score | Price (Cr) | Expected (Cr) | Diff (Cr) |
|------|--------|------|-------|------------|----------------|-----------|
| 1 | DS Rathi (LSG) | Bowler | 79.1 | 0.3 | 10.6 | -10.3 |
| 2 | E Malinga (SRH) | Bowler | 77.5 | 1.2 | 10.9 | -9.7 |
| 3 | JD Unadkat (SRH) | Bowler | 83.1 | 1.0 | 10.6 | -9.6 |
| 4 | Harpreet Brar (PBKS) | Bowler | 73.9 | 1.5 | 10.9 | -9.4 |
| 5 | VG Arora (KKR) | Bowler | 75.9 | 1.8 | 10.9 | -9.1 |
| 6 | V Puthur (MI) | Bowler | 65.4 | 0.3 | 9.2 | -8.9 |
| 7 | MJ Santner (MI) | Bowler | 74.1 | 2.0 | 10.9 | -8.9 |
| 8 | AS Roy (KKR) | Bowler | 66.7 | 0.4 | 9.2 | -8.8 |
| 9 | R Sai Kishore (GT) | Bowler | 85.0 | 2.0 | 10.6 | -8.6 |
| 10 | N Thushara (RCB) | Bowler | 68.3 | 1.6 | 9.2 | -7.6 |
| 11 | A Kamboj (CSK) | Bowler | 73.2 | 3.4 | 10.9 | -7.5 |
| 12 | PW Hasaranga (RR) | Bowler | 69.3 | 2.0 | 9.2 | -7.2 |
| 13 | MR Marsh (LSG) | Batsman | 86.7 | 3.4 | 10.6 | -7.2 |
| 14 | Yudhvir Singh (RR) | Bowler | 43.5 | 0.3 | 6.5 | -6.2 |
| 15 | KK Ahmed (CSK) | Bowler | 74.2 | 4.8 | 10.9 | -6.1 |
| 16 | P Dubey (PBKS) | Bowler | 52.0 | 0.3 | 6.2 | -5.8 |
| 17 | A Mhatre (CSK) | Batsman | 47.9 | 0.3 | 6.2 | -5.8 |
| 18 | Zeeshan Ansari (SRH) | Bowler | 50.8 | 0.4 | 6.2 | -5.8 |
| 19 | XC Bartlett (PBKS) | Bowler | 47.7 | 0.8 | 6.5 | -5.7 |
| 20 | PVD Chameera (DC) | Bowler | 43.2 | 0.8 | 6.5 | -5.7 |
| 21 | I Sharma (GT) | Bowler | 41.9 | 0.8 | 6.5 | -5.7 |
| 22 | V Nigam (DC) | All-Rounder | 52.2 | 0.5 | 6.2 | -5.7 |
| 23 | P Arya (PBKS) | Batsman | 68.8 | 3.8 | 9.2 | -5.4 |
| 24 | M Siddharth (LSG) | Bowler | 52.0 | 0.8 | 6.2 | -5.3 |
| 25 | Harshit Rana (KKR) | Bowler | 71.0 | 4.0 | 9.2 | -5.2 |

### Undervalued Patterns

| Dimension | Count |
|----------|-------|
| Total players | 25 |
| Acquisition: Retained | 22 |
| Acquisition: Bought | 3 |
| Role: Bowler | 21 |
| Role: Batsman | 3 |
| Role: All-Rounder | 1 |
| Overseas | 7 |

## Top 25 Most Overvalued Players

Players costing **more** than their score-decile peers.

| Rank | Player | Role | Score | Price (Cr) | Expected (Cr) | Diff (Cr) |
|------|--------|------|-------|------------|----------------|-----------|
| 1 | RR Pant (LSG) | Wicketkeeper | 48.3 | 27.0 | 6.2 | 20.9 |
| 2 | SS Iyer (PBKS) | Batsman | 76.9 | 26.8 | 10.9 | 15.9 |
| 3 | RD Gaikwad (CSK) | Batsman | 33.7 | 18.0 | 4.4 | 13.6 |
| 4 | Rashid Khan (GT) | Bowler | 57.8 | 18.0 | 5.5 | 12.5 |
| 5 | H Klaasen (SRH) | Wicketkeeper | 72.6 | 23.0 | 10.9 | 12.1 |
| 6 | N Pooran (LSG) | Wicketkeeper | 72.5 | 21.0 | 9.2 | 11.8 |
| 7 | SV Samson (RR) | Wicketkeeper | 42.9 | 18.0 | 6.5 | 11.5 |
| 8 | HH Pandya (MI) | All-Rounder | 55.7 | 16.4 | 5.8 | 10.6 |
| 9 | RG Sharma (MI) | Batsman | 53.4 | 16.3 | 5.8 | 10.5 |
| 10 | V Kohli (RCB) | Batsman | 79.0 | 21.0 | 10.6 | 10.4 |
| 11 | AR Patel (DC) | All-Rounder | 47.8 | 16.5 | 6.5 | 10.0 |
| 12 | LS Livingstone (RCB) | Batsman | 26.2 | 13.0 | 3.7 | 9.3 |
| 13 | Ramandeep Singh (KKR) | Batsman | 19.4 | 13.0 | 3.7 | 9.3 |
| 14 | RK Singh (KKR) | Batsman | 37.5 | 13.0 | 4.0 | 9.0 |
| 15 | YBK Jaiswal (RR) | Batsman | 69.6 | 18.0 | 9.2 | 8.8 |
| 16 | M Pathirana (CSK) | Bowler | 67.2 | 18.0 | 9.2 | 8.8 |
| 17 | RA Jadeja (CSK) | All-Rounder | 57.1 | 14.0 | 5.8 | 8.2 |
| 18 | TM Head (SRH) | Batsman | 52.3 | 14.0 | 6.2 | 7.8 |
| 19 | R Parag (RR) | Batsman | 51.7 | 14.0 | 6.2 | 7.8 |
| 20 | DC Jurel (RR) | Wicketkeeper | 49.8 | 14.0 | 6.2 | 7.8 |
| 21 | JJ Bumrah (MI) | Bowler | 97.4 | 18.0 | 10.6 | 7.4 |
| 22 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 18.0 | 10.6 | 7.4 |
| 23 | K Rabada (GT) | Bowler | 28.2 | 10.8 | 3.7 | 7.1 |
| 24 | PJ Cummins (SRH) | Bowler | 78.9 | 18.0 | 10.9 | 7.1 |
| 25 | YS Chahal (PBKS) | Bowler | 76.7 | 18.0 | 10.9 | 7.1 |

### Overvalued Patterns

| Dimension | Count |
|----------|-------|
| Total players | 25 |
| Acquisition: Retained | 23 |
| Acquisition: Bought | 2 |
| Role: Batsman | 10 |
| Role: Bowler | 7 |
| Role: Wicketkeeper | 5 |
| Role: All-Rounder | 3 |
| Overseas | 4 |

## Common Patterns

- **Undervalued are 21/25 bowlers at base price** — the market systematically undervalues bowling performance.
- **Overvalued are star retained players** — Pant (27 Cr), Iyer (26.75 Cr), Klaasen (23 Cr), Kohli (21 Cr) — brand and captaincy value not captured by performance scores.
- **Retained players dominate the overvalued list** — retention prices reflect loyalty premiums, not marginal performance.
- **Overseas players do not show a clear bias** — both lists contain overseas names.
- **Wicketkeepers are mostly overvalued** — the scarcity of quality keeper-batters inflates their price.
- **All-rounders are fairly represented** in both lists — no systematic bias.
- **Acquisition type is the strongest signal**: Retained players = overvalued (premium price floor); Bought/Unknown = undervalued (market inefficiency for non-retained talent).

---

## Limitations

- ExpectedPrice uses score decile bins. Finer binning might identify more subtle mispricing.
- PlayerValueScore only captures IPL 2025 performance; international form, injury history, and brand value are excluded.
- Retention prices are not market-clearing prices; they incorporate team loyalty and first-refusal rights.
- Sample size: 158 players with valid prices.
