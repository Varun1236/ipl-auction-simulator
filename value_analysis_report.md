# Value-Per-Crore Analysis — IPL 2025 Season

Generated from `data/master_players.csv` and `data/player_values.csv`

## Methodology

ValuePerCrore = PlayerValueScore / AuctionPrice

A higher ValuePerCrore means the team got more performance value per unit of currency spent. Players with AuctionPrice = N/A or 0 are excluded from the calculation.

## Summary

| Metric | Value |
|--------|-------|
| Total players | 186 |
| Players with ValuePerCrore | 158 |
| Players excluded (N/A price) | 28 |
| Players excluded (0 price) | 0 |

| Mean ValuePerCrore | 31.42 |
| Median ValuePerCrore | 10.70 |
| Min ValuePerCrore | 0.00 |
| Max ValuePerCrore | 263.67 |

## Average ValuePerCrore by Role

| Role | Count | Avg VPC |
|------|-------|--------|
| All-Rounder | 7 | 19.89 |
| Batsman | 62 | 21.67 |
| Bowler | 73 | 45.52 |
| Wicketkeeper | 16 | 9.92 |

## Average ValuePerCrore by Acquisition Type

| Type | Count | Avg VPC |
|------|-------|--------|
| Bought | 16 | 38.81 |
| Retained | 142 | 30.59 |

## Most Undervalued Players (Highest ValuePerCrore)

These players delivered high performance relative to their low price.

| Rank | Player | Role | Score | Price (Cr) | VPC |
|------|--------|------|-------|------------|-----|
| 1 | DS Rathi (LSG) | Bowler | 79.1 | 0.3 | 263.67 |
| 2 | V Puthur (MI) | Bowler | 65.4 | 0.3 | 218.00 |
| 3 | Akash Singh (LSG) | Bowler | 61.4 | 0.3 | 204.67 |
| 4 | Ashwani Kumar (MI) | Bowler | 61.2 | 0.3 | 204.00 |
| 5 | HS Dubey (SRH) | Bowler | 59.7 | 0.3 | 199.00 |

## Most Overvalued Players (Lowest ValuePerCrore)

These players had high prices relative to their performance score.

| Rank | Player | Role | Score | Price (Cr) | VPC |
|------|--------|------|-------|------------|-----|
| 1 | R Minz (MI) | Batsman | 0.0 | 0.7 | 0.00 |
| 2 | Ramandeep Singh (KKR) | Batsman | 19.4 | 13.0 | 1.49 |
| 3 | RR Pant (LSG) | Wicketkeeper | 48.3 | 27.0 | 1.79 |
| 4 | RD Gaikwad (CSK) | Batsman | 33.7 | 18.0 | 1.87 |
| 5 | LS Livingstone (RCB) | Batsman | 26.2 | 13.0 | 2.02 |

## Top 20 Highest ValuePerCrore

| Rank | Player | Role | Score | Price (Cr) | VPC |
|------|--------|------|-------|------------|-----|
| 1 | DS Rathi (LSG) | Bowler | 79.1 | 0.3 | 263.67 |
| 2 | V Puthur (MI) | Bowler | 65.4 | 0.3 | 218.00 |
| 3 | Akash Singh (LSG) | Bowler | 61.4 | 0.3 | 204.67 |
| 4 | Ashwani Kumar (MI) | Bowler | 61.2 | 0.3 | 204.00 |
| 5 | HS Dubey (SRH) | Bowler | 59.7 | 0.3 | 199.00 |
| 6 | P Dubey (PBKS) | Bowler | 52.0 | 0.3 | 173.33 |
| 7 | AS Roy (KKR) | Bowler | 66.7 | 0.4 | 166.75 |
| 8 | A Mhatre (CSK) | Batsman | 47.9 | 0.3 | 159.67 |
| 9 | Yudhvir Singh (RR) | Bowler | 43.5 | 0.3 | 145.00 |
| 10 | AU Verma (SRH) | Batsman | 41.3 | 0.3 | 137.67 |
| 11 | Prince Yadav (LSG) | Bowler | 40.4 | 0.3 | 134.67 |
| 12 | Zeeshan Ansari (SRH) | Bowler | 50.8 | 0.4 | 127.00 |
| 13 | UM Patel (CSK) | Batsman | 37.5 | 0.3 | 125.00 |
| 14 | V Nigam (DC) | All-Rounder | 52.2 | 0.5 | 104.40 |
| 15 | Mukesh Choudhary (CSK) | Bowler | 28.1 | 0.3 | 93.67 |
| 16 | JD Unadkat (SRH) | Bowler | 83.1 | 1.0 | 83.10 |
| 17 | RA Bawa (MI) | Batsman | 24.6 | 0.3 | 82.00 |
| 18 | KK Nair (DC) | Batsman | 39.8 | 0.5 | 79.60 |
| 19 | PHKD Mendis (SRH) | Bowler | 58.1 | 0.8 | 72.62 |
| 20 | C Bosch (MI) | Bowler | 53.1 | 0.8 | 66.38 |

## Bottom 20 Lowest ValuePerCrore

| Rank | Player | Role | Score | Price (Cr) | VPC |
|------|--------|------|-------|------------|-----|
| 139 | R Minz (MI) | Batsman | 0.0 | 0.7 | 0.00 |
| 140 | Ramandeep Singh (KKR) | Batsman | 19.4 | 13.0 | 1.49 |
| 141 | RR Pant (LSG) | Wicketkeeper | 48.3 | 27.0 | 1.79 |
| 142 | RD Gaikwad (CSK) | Batsman | 33.7 | 18.0 | 1.87 |
| 143 | LS Livingstone (RCB) | Batsman | 26.2 | 13.0 | 2.02 |
| 144 | SV Samson (RR) | Wicketkeeper | 42.9 | 18.0 | 2.38 |
| 145 | K Rabada (GT) | Bowler | 28.2 | 10.8 | 2.61 |
| 146 | SS Iyer (PBKS) | Batsman | 76.9 | 26.8 | 2.87 |
| 147 | RK Singh (KKR) | Batsman | 37.5 | 13.0 | 2.88 |
| 148 | AR Patel (DC) | All-Rounder | 47.8 | 16.5 | 2.90 |
| 149 | MP Yadav (LSG) | Bowler | 32.3 | 11.0 | 2.94 |
| 150 | H Klaasen (SRH) | Wicketkeeper | 72.6 | 23.0 | 3.16 |
| 151 | Rashid Khan (GT) | Bowler | 57.8 | 18.0 | 3.21 |
| 152 | RG Sharma (MI) | Batsman | 53.4 | 16.3 | 3.28 |
| 153 | Simarjeet Singh (SRH) | Bowler | 18.2 | 5.5 | 3.31 |
| 154 | SO Hetmyer (RR) | Batsman | 36.7 | 11.0 | 3.34 |
| 155 | HH Pandya (MI) | All-Rounder | 55.7 | 16.4 | 3.40 |
| 156 | N Pooran (LSG) | Wicketkeeper | 72.5 | 21.0 | 3.45 |
| 157 | DC Jurel (RR) | Wicketkeeper | 49.8 | 14.0 | 3.56 |
| 158 | MP Stoinis (PBKS) | Batsman | 39.3 | 11.0 | 3.57 |
