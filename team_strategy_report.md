# Team Strategy Report

Team-specific player valuations based on franchise strategy rules.

## Rules Applied

| Team | Trigger | Bonus | Column(s) |
|------|---------|-------|-----------|
| CSK | Age >= 30 | +15% | Age |
| CSK | Indian player | +10% | Nationality |
| MI | Age <= 25 | +15% | Age |
| MI | StrikeRate > 145 (B/WK/AR) | +10% | StrikeRate |
| MI | Runs >= 200 & Age <= 23 | +10% | Runs, Age |
| RR | Age <= 23 | +20% | Age |
| RR | Runs >= 200 & Age <= 23 | +10% | Runs, Age |
| KKR | Bowler, Wkts >= 5, Econ <= 8.5 | +15% | Role, Wickets, Economy |
| RCB | StrikeRate > 150 (B/WK/AR) | +15% | Role, StrikeRate |
| RCB | Runs >= 400 | +10% | Runs |
| GT | All-Rounder | +10% | Role |
| GT | AR & Runs >= 200 & Wkts >= 5 | +10% | Role, Runs, Wickets |
| LSG | Wicketkeeper | +10% | Role |
| LSG | WK & Runs >= 300 | +10% | Role, Runs |
| PBKS | StrikeRate > 150 (B/WK/AR) | +15% | Role, StrikeRate |
| PBKS | Runs >= 300 | +10% | Runs |
| DC | Age <= 28 | +10% | Age |
| DC | Age <= 25 | +10% | Age |
| SRH | StrikeRate > 150 (B/WK/AR) | +15% | Role, StrikeRate |
| SRH | Runs >= 400 | +10% | Runs |

---

## Example Calculations

### B Sai Sudharsan (GT)

- Base PlayerValueScore: **94.3**
- Age: 23, Role: Batsman, Runs: 759, SR: 156.2, Wkts: 0, Econ: 0.0

| Team | Triggers | Bonus | Calculation | Value |
|------|----------|-------|-------------|-------|
| MI | age<=25, SR>145, breakthrough | +35% | 94.3 × 1.35 | **127.3** |
| CSK | Indian | +10% | 94.3 × 1.10 | **103.7** |
| RCB | SR>150, runs>=400 | +25% | 94.3 × 1.25 | **117.9** |
| RR | age<=23, young_breakout | +30% | 94.3 × 1.30 | **122.6** |
| KKR | none | +0% | 94.3 | **94.3** |
| GT | none | +0% | 94.3 | **94.3** |
| LSG | none | +0% | 94.3 | **94.3** |
| PBKS | SR>150, runs>=300 | +25% | 94.3 × 1.25 | **117.9** |
| DC | age<=28, age<=25 | +20% | 94.3 × 1.20 | **113.2** |
| SRH | SR>150, runs>=400 | +25% | 94.3 × 1.25 | **117.9** |

### JJ Bumrah (MI)

- Base PlayerValueScore: **97.4**
- Age: 31, Role: Bowler, Runs: 0, SR: 0.0, Wkts: 18, Econ: 6.7

| Team | Triggers | Bonus | Calculation | Value |
|------|----------|-------|-------------|-------|
| MI | none | +0% | 97.4 | **97.4** |
| CSK | age>=30, Indian | +25% | 97.4 × 1.25 | **121.8** |
| RCB | none | +0% | 97.4 | **97.4** |
| RR | none | +0% | 97.4 | **97.4** |
| KKR | spin_proxy | +15% | 97.4 × 1.15 | **112.0** |
| GT | none | +0% | 97.4 | **97.4** |
| LSG | none | +0% | 97.4 | **97.4** |
| PBKS | none | +0% | 97.4 | **97.4** |
| DC | none | +0% | 97.4 | **97.4** |
| SRH | none | +0% | 97.4 | **97.4** |

### Abhishek Sharma (SRH)

- Base PlayerValueScore: **71.2**
- Age: 24, Role: Batsman, Runs: 439, SR: 193.4, Wkts: 0, Econ: 0.0

| Team | Triggers | Bonus | Calculation | Value |
|------|----------|-------|-------------|-------|
| MI | age<=25, SR>145 | +25% | 71.2 × 1.25 | **89.0** |
| CSK | Indian | +10% | 71.2 × 1.10 | **78.3** |
| RCB | SR>150, runs>=400 | +25% | 71.2 × 1.25 | **89.0** |
| RR | none | +0% | 71.2 | **71.2** |
| KKR | none | +0% | 71.2 | **71.2** |
| GT | none | +0% | 71.2 | **71.2** |
| LSG | none | +0% | 71.2 | **71.2** |
| PBKS | SR>150, runs>=300 | +25% | 71.2 × 1.25 | **89.0** |
| DC | age<=28, age<=25 | +20% | 71.2 × 1.20 | **85.4** |
| SRH | SR>150, runs>=400 | +25% | 71.2 × 1.25 | **89.0** |

### AD Russell (KKR)

- Base PlayerValueScore: **43.1**
- Age: 36, Role: All-Rounder, Runs: 167, SR: 163.7, Wkts: 8, Econ: 11.9

| Team | Triggers | Bonus | Calculation | Value |
|------|----------|-------|-------------|-------|
| MI | SR>145 | +10% | 43.1 × 1.10 | **47.4** |
| CSK | age>=30, Indian | +25% | 43.1 × 1.25 | **53.9** |
| RCB | SR>150 | +15% | 43.1 × 1.15 | **49.6** |
| RR | none | +0% | 43.1 | **43.1** |
| KKR | none | +0% | 43.1 | **43.1** |
| GT | all_rounder | +10% | 43.1 × 1.10 | **47.4** |
| LSG | none | +0% | 43.1 | **43.1** |
| PBKS | SR>150 | +15% | 43.1 × 1.15 | **49.6** |
| DC | none | +0% | 43.1 | **43.1** |
| SRH | SR>150 | +15% | 43.1 × 1.15 | **49.6** |

---

## Top 20 Players per Franchise

### MI

| Rank | Player | Role | Base | MI Value | +% | Triggers |
|------|--------|------|------|----------|-----|----------|
| 1 | B Sai Sudharsan (GT) | Batsman | 94.3 | 127.3 | +35% | age<=25, SR>145, breakthrough |
| 2 | Noor Ahmad (CSK) | Bowler | 99.7 | 114.7 | +15% | age<=25 |
| 3 | M Prasidh Krishna (GT) | Bowler | 100.0 | 100.0 | +0% | — |
| 4 | JJ Bumrah (MI) | Bowler | 97.4 | 97.4 | +0% | — |
| 5 | MR Marsh (LSG) | Batsman | 86.7 | 95.4 | +10% | SR>145 |
| 6 | Shubman Gill (GT) | Batsman | 76.1 | 95.1 | +25% | age<=25, SR>145 |
| 7 | YBK Jaiswal (RR) | Batsman | 69.6 | 94.0 | +35% | age<=25, SR>145, breakthrough |
| 8 | SA Yadav (MI) | Batsman | 85.2 | 93.7 | +10% | SR>145 |
| 9 | JR Hazlewood (RCB) | Bowler | 93.1 | 93.1 | +0% | — |
| 10 | DS Rathi (LSG) | Bowler | 79.1 | 91.0 | +15% | age<=25 |
| 11 | TA Boult (MI) | Bowler | 90.5 | 90.5 | +0% | — |
| 12 | M Jansen (PBKS) | Bowler | 78.5 | 90.3 | +15% | age<=25 |
| 13 | CV Varun (KKR) | Bowler | 89.3 | 89.3 | +0% | — |
| 14 | E Malinga (SRH) | Bowler | 77.5 | 89.1 | +15% | age<=25 |
| 15 | Abhishek Sharma (SRH) | Batsman | 71.2 | 89.0 | +25% | age<=25, SR>145 |
| 16 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 88.9 | +0% | — |
| 17 | Kuldeep Yadav (DC) | Bowler | 88.6 | 88.6 | +0% | — |
| 18 | P Arya (PBKS) | Batsman | 68.8 | 86.0 | +25% | age<=25, SR>145 |
| 19 | KL Rahul (DC) | Wicketkeeper | 77.7 | 85.5 | +10% | SR>145 |
| 20 | V Sooryavanshi (RR) | Batsman | 63.1 | 85.2 | +35% | age<=25, SR>145, breakthrough |

### CSK

| Rank | Player | Role | Base | CSK Value | +% | Triggers |
|------|--------|------|------|----------|-----|----------|
| 1 | JJ Bumrah (MI) | Bowler | 97.4 | 121.8 | +25% | age>=30, Indian |
| 2 | TA Boult (MI) | Bowler | 90.5 | 113.1 | +25% | age>=30, Indian |
| 3 | CV Varun (KKR) | Bowler | 89.3 | 111.6 | +25% | age>=30, Indian |
| 4 | Kuldeep Yadav (DC) | Bowler | 88.6 | 110.8 | +25% | age>=30, Indian |
| 5 | M Prasidh Krishna (GT) | Bowler | 100.0 | 110.0 | +10% | Indian |
| 6 | JR Hazlewood (RCB) | Bowler | 93.1 | 107.1 | +15% | age>=30 |
| 7 | SA Yadav (MI) | Batsman | 85.2 | 106.5 | +25% | age>=30, Indian |
| 8 | JD Unadkat (SRH) | Bowler | 83.1 | 103.9 | +25% | age>=30, Indian |
| 9 | B Sai Sudharsan (GT) | Batsman | 94.3 | 103.7 | +10% | Indian |
| 10 | Noor Ahmad (CSK) | Bowler | 99.7 | 99.7 | +0% | — |
| 11 | MR Marsh (LSG) | Batsman | 86.7 | 99.7 | +15% | age>=30 |
| 12 | V Kohli (RCB) | Batsman | 79.0 | 98.8 | +25% | age>=30, Indian |
| 13 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 97.8 | +10% | Indian |
| 14 | KL Rahul (DC) | Wicketkeeper | 77.7 | 97.1 | +25% | age>=30, Indian |
| 15 | SS Iyer (PBKS) | Batsman | 76.9 | 96.1 | +25% | age>=30, Indian |
| 16 | YS Chahal (PBKS) | Bowler | 76.7 | 95.9 | +25% | age>=30, Indian |
| 17 | Mohammed Siraj (GT) | Bowler | 76.6 | 95.8 | +25% | age>=30, Indian |
| 18 | R Sai Kishore (GT) | Bowler | 85.0 | 93.5 | +10% | Indian |
| 19 | B Kumar (RCB) | Bowler | 79.3 | 91.2 | +15% | age>=30 |
| 20 | PJ Cummins (SRH) | Bowler | 78.9 | 90.7 | +15% | age>=30 |

### RCB

| Rank | Player | Role | Base | RCB Value | +% | Triggers |
|------|--------|------|------|----------|-----|----------|
| 1 | B Sai Sudharsan (GT) | Batsman | 94.3 | 117.9 | +25% | SR>150, runs>=400 |
| 2 | MR Marsh (LSG) | Batsman | 86.7 | 108.4 | +25% | SR>150, runs>=400 |
| 3 | SA Yadav (MI) | Batsman | 85.2 | 106.5 | +25% | SR>150, runs>=400 |
| 4 | M Prasidh Krishna (GT) | Bowler | 100.0 | 100.0 | +0% | — |
| 5 | Noor Ahmad (CSK) | Bowler | 99.7 | 99.7 | +0% | — |
| 6 | JJ Bumrah (MI) | Bowler | 97.4 | 97.4 | +0% | — |
| 7 | SS Iyer (PBKS) | Batsman | 76.9 | 96.1 | +25% | SR>150, runs>=400 |
| 8 | Shubman Gill (GT) | Batsman | 76.1 | 95.1 | +25% | SR>150, runs>=400 |
| 9 | JR Hazlewood (RCB) | Bowler | 93.1 | 93.1 | +0% | — |
| 10 | JC Buttler (GT) | Wicketkeeper | 73.4 | 91.8 | +25% | SR>150, runs>=400 |
| 11 | H Klaasen (SRH) | Wicketkeeper | 72.6 | 90.8 | +25% | SR>150, runs>=400 |
| 12 | N Pooran (LSG) | Wicketkeeper | 72.5 | 90.6 | +25% | SR>150, runs>=400 |
| 13 | TA Boult (MI) | Bowler | 90.5 | 90.5 | +0% | — |
| 14 | CV Varun (KKR) | Bowler | 89.3 | 89.3 | +0% | — |
| 15 | Abhishek Sharma (SRH) | Batsman | 71.2 | 89.0 | +25% | SR>150, runs>=400 |
| 16 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 88.9 | +0% | — |
| 17 | Kuldeep Yadav (DC) | Bowler | 88.6 | 88.6 | +0% | — |
| 18 | YBK Jaiswal (RR) | Batsman | 69.6 | 87.0 | +25% | SR>150, runs>=400 |
| 19 | V Kohli (RCB) | Batsman | 79.0 | 86.9 | +10% | runs>=400 |
| 20 | P Arya (PBKS) | Batsman | 68.8 | 86.0 | +25% | SR>150, runs>=400 |

### RR

| Rank | Player | Role | Base | RR Value | +% | Triggers |
|------|--------|------|------|----------|-----|----------|
| 1 | B Sai Sudharsan (GT) | Batsman | 94.3 | 122.6 | +30% | age<=23, young_breakout |
| 2 | Noor Ahmad (CSK) | Bowler | 99.7 | 119.6 | +20% | age<=23 |
| 3 | M Prasidh Krishna (GT) | Bowler | 100.0 | 100.0 | +0% | — |
| 4 | JJ Bumrah (MI) | Bowler | 97.4 | 97.4 | +0% | — |
| 5 | JR Hazlewood (RCB) | Bowler | 93.1 | 93.1 | +0% | — |
| 6 | TA Boult (MI) | Bowler | 90.5 | 90.5 | +0% | — |
| 7 | YBK Jaiswal (RR) | Batsman | 69.6 | 90.5 | +30% | age<=23, young_breakout |
| 8 | CV Varun (KKR) | Bowler | 89.3 | 89.3 | +0% | — |
| 9 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 88.9 | +0% | — |
| 10 | Kuldeep Yadav (DC) | Bowler | 88.6 | 88.6 | +0% | — |
| 11 | MR Marsh (LSG) | Batsman | 86.7 | 86.7 | +0% | — |
| 12 | SA Yadav (MI) | Batsman | 85.2 | 85.2 | +0% | — |
| 13 | Harshit Rana (KKR) | Bowler | 71.0 | 85.2 | +20% | age<=23 |
| 14 | R Sai Kishore (GT) | Bowler | 85.0 | 85.0 | +0% | — |
| 15 | JD Unadkat (SRH) | Bowler | 83.1 | 83.1 | +0% | — |
| 16 | V Sooryavanshi (RR) | Batsman | 63.1 | 82.0 | +30% | age<=23, young_breakout |
| 17 | M Pathirana (CSK) | Bowler | 67.2 | 80.6 | +20% | age<=23 |
| 18 | B Kumar (RCB) | Bowler | 79.3 | 79.3 | +0% | — |
| 19 | DS Rathi (LSG) | Bowler | 79.1 | 79.1 | +0% | — |
| 20 | V Kohli (RCB) | Batsman | 79.0 | 79.0 | +0% | — |

### KKR

| Rank | Player | Role | Base | KKR Value | +% | Triggers |
|------|--------|------|------|----------|-----|----------|
| 1 | M Prasidh Krishna (GT) | Bowler | 100.0 | 115.0 | +15% | spin_proxy |
| 2 | Noor Ahmad (CSK) | Bowler | 99.7 | 114.7 | +15% | spin_proxy |
| 3 | JJ Bumrah (MI) | Bowler | 97.4 | 112.0 | +15% | spin_proxy |
| 4 | CV Varun (KKR) | Bowler | 89.3 | 102.7 | +15% | spin_proxy |
| 5 | Kuldeep Yadav (DC) | Bowler | 88.6 | 101.9 | +15% | spin_proxy |
| 6 | JD Unadkat (SRH) | Bowler | 83.1 | 95.6 | +15% | spin_proxy |
| 7 | B Sai Sudharsan (GT) | Batsman | 94.3 | 94.3 | +0% | — |
| 8 | JR Hazlewood (RCB) | Bowler | 93.1 | 93.1 | +0% | — |
| 9 | DS Rathi (LSG) | Bowler | 79.1 | 91.0 | +15% | spin_proxy |
| 10 | TA Boult (MI) | Bowler | 90.5 | 90.5 | +0% | — |
| 11 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 88.9 | +0% | — |
| 12 | MR Marsh (LSG) | Batsman | 86.7 | 86.7 | +0% | — |
| 13 | MJ Santner (MI) | Bowler | 74.1 | 85.2 | +15% | spin_proxy |
| 14 | SA Yadav (MI) | Batsman | 85.2 | 85.2 | +0% | — |
| 15 | R Sai Kishore (GT) | Bowler | 85.0 | 85.0 | +0% | — |
| 16 | A Kamboj (CSK) | Bowler | 73.2 | 84.2 | +15% | spin_proxy |
| 17 | B Kumar (RCB) | Bowler | 79.3 | 79.3 | +0% | — |
| 18 | V Kohli (RCB) | Batsman | 79.0 | 79.0 | +0% | — |
| 19 | PJ Cummins (SRH) | Bowler | 78.9 | 78.9 | +0% | — |
| 20 | M Jansen (PBKS) | Bowler | 78.5 | 78.5 | +0% | — |

### GT

| Rank | Player | Role | Base | GT Value | +% | Triggers |
|------|--------|------|------|----------|-----|----------|
| 1 | M Prasidh Krishna (GT) | Bowler | 100.0 | 100.0 | +0% | — |
| 2 | Noor Ahmad (CSK) | Bowler | 99.7 | 99.7 | +0% | — |
| 3 | JJ Bumrah (MI) | Bowler | 97.4 | 97.4 | +0% | — |
| 4 | B Sai Sudharsan (GT) | Batsman | 94.3 | 94.3 | +0% | — |
| 5 | JR Hazlewood (RCB) | Bowler | 93.1 | 93.1 | +0% | — |
| 6 | TA Boult (MI) | Bowler | 90.5 | 90.5 | +0% | — |
| 7 | CV Varun (KKR) | Bowler | 89.3 | 89.3 | +0% | — |
| 8 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 88.9 | +0% | — |
| 9 | Kuldeep Yadav (DC) | Bowler | 88.6 | 88.6 | +0% | — |
| 10 | MR Marsh (LSG) | Batsman | 86.7 | 86.7 | +0% | — |
| 11 | SA Yadav (MI) | Batsman | 85.2 | 85.2 | +0% | — |
| 12 | R Sai Kishore (GT) | Bowler | 85.0 | 85.0 | +0% | — |
| 13 | JD Unadkat (SRH) | Bowler | 83.1 | 83.1 | +0% | — |
| 14 | B Kumar (RCB) | Bowler | 79.3 | 79.3 | +0% | — |
| 15 | DS Rathi (LSG) | Bowler | 79.1 | 79.1 | +0% | — |
| 16 | V Kohli (RCB) | Batsman | 79.0 | 79.0 | +0% | — |
| 17 | PJ Cummins (SRH) | Bowler | 78.9 | 78.9 | +0% | — |
| 18 | M Jansen (PBKS) | Bowler | 78.5 | 78.5 | +0% | — |
| 19 | KL Rahul (DC) | Wicketkeeper | 77.7 | 77.7 | +0% | — |
| 20 | E Malinga (SRH) | Bowler | 77.5 | 77.5 | +0% | — |

### LSG

| Rank | Player | Role | Base | LSG Value | +% | Triggers |
|------|--------|------|------|----------|-----|----------|
| 1 | M Prasidh Krishna (GT) | Bowler | 100.0 | 100.0 | +0% | — |
| 2 | Noor Ahmad (CSK) | Bowler | 99.7 | 99.7 | +0% | — |
| 3 | JJ Bumrah (MI) | Bowler | 97.4 | 97.4 | +0% | — |
| 4 | B Sai Sudharsan (GT) | Batsman | 94.3 | 94.3 | +0% | — |
| 5 | KL Rahul (DC) | Wicketkeeper | 77.7 | 93.2 | +20% | wk, wk_runs>=300 |
| 6 | JR Hazlewood (RCB) | Bowler | 93.1 | 93.1 | +0% | — |
| 7 | TA Boult (MI) | Bowler | 90.5 | 90.5 | +0% | — |
| 8 | CV Varun (KKR) | Bowler | 89.3 | 89.3 | +0% | — |
| 9 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 88.9 | +0% | — |
| 10 | Kuldeep Yadav (DC) | Bowler | 88.6 | 88.6 | +0% | — |
| 11 | JC Buttler (GT) | Wicketkeeper | 73.4 | 88.1 | +20% | wk, wk_runs>=300 |
| 12 | H Klaasen (SRH) | Wicketkeeper | 72.6 | 87.1 | +20% | wk, wk_runs>=300 |
| 13 | N Pooran (LSG) | Wicketkeeper | 72.5 | 87.0 | +20% | wk, wk_runs>=300 |
| 14 | MR Marsh (LSG) | Batsman | 86.7 | 86.7 | +0% | — |
| 15 | SA Yadav (MI) | Batsman | 85.2 | 85.2 | +0% | — |
| 16 | R Sai Kishore (GT) | Bowler | 85.0 | 85.0 | +0% | — |
| 17 | JD Unadkat (SRH) | Bowler | 83.1 | 83.1 | +0% | — |
| 18 | B Kumar (RCB) | Bowler | 79.3 | 79.3 | +0% | — |
| 19 | DS Rathi (LSG) | Bowler | 79.1 | 79.1 | +0% | — |
| 20 | V Kohli (RCB) | Batsman | 79.0 | 79.0 | +0% | — |

### PBKS

| Rank | Player | Role | Base | PBKS Value | +% | Triggers |
|------|--------|------|------|----------|-----|----------|
| 1 | B Sai Sudharsan (GT) | Batsman | 94.3 | 117.9 | +25% | SR>150, runs>=300 |
| 2 | MR Marsh (LSG) | Batsman | 86.7 | 108.4 | +25% | SR>150, runs>=300 |
| 3 | SA Yadav (MI) | Batsman | 85.2 | 106.5 | +25% | SR>150, runs>=300 |
| 4 | M Prasidh Krishna (GT) | Bowler | 100.0 | 100.0 | +0% | — |
| 5 | Noor Ahmad (CSK) | Bowler | 99.7 | 99.7 | +0% | — |
| 6 | JJ Bumrah (MI) | Bowler | 97.4 | 97.4 | +0% | — |
| 7 | SS Iyer (PBKS) | Batsman | 76.9 | 96.1 | +25% | SR>150, runs>=300 |
| 8 | Shubman Gill (GT) | Batsman | 76.1 | 95.1 | +25% | SR>150, runs>=300 |
| 9 | JR Hazlewood (RCB) | Bowler | 93.1 | 93.1 | +0% | — |
| 10 | JC Buttler (GT) | Wicketkeeper | 73.4 | 91.8 | +25% | SR>150, runs>=300 |
| 11 | H Klaasen (SRH) | Wicketkeeper | 72.6 | 90.8 | +25% | SR>150, runs>=300 |
| 12 | N Pooran (LSG) | Wicketkeeper | 72.5 | 90.6 | +25% | SR>150, runs>=300 |
| 13 | TA Boult (MI) | Bowler | 90.5 | 90.5 | +0% | — |
| 14 | CV Varun (KKR) | Bowler | 89.3 | 89.3 | +0% | — |
| 15 | Abhishek Sharma (SRH) | Batsman | 71.2 | 89.0 | +25% | SR>150, runs>=300 |
| 16 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 88.9 | +0% | — |
| 17 | Kuldeep Yadav (DC) | Bowler | 88.6 | 88.6 | +0% | — |
| 18 | YBK Jaiswal (RR) | Batsman | 69.6 | 87.0 | +25% | SR>150, runs>=300 |
| 19 | V Kohli (RCB) | Batsman | 79.0 | 86.9 | +10% | runs>=300 |
| 20 | P Arya (PBKS) | Batsman | 68.8 | 86.0 | +25% | SR>150, runs>=300 |

### DC

| Rank | Player | Role | Base | DC Value | +% | Triggers |
|------|--------|------|------|----------|-----|----------|
| 1 | Noor Ahmad (CSK) | Bowler | 99.7 | 119.6 | +20% | age<=28, age<=25 |
| 2 | B Sai Sudharsan (GT) | Batsman | 94.3 | 113.2 | +20% | age<=28, age<=25 |
| 3 | M Prasidh Krishna (GT) | Bowler | 100.0 | 100.0 | +0% | — |
| 4 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 97.8 | +10% | age<=28 |
| 5 | JJ Bumrah (MI) | Bowler | 97.4 | 97.4 | +0% | — |
| 6 | DS Rathi (LSG) | Bowler | 79.1 | 94.9 | +20% | age<=28, age<=25 |
| 7 | M Jansen (PBKS) | Bowler | 78.5 | 94.2 | +20% | age<=28, age<=25 |
| 8 | R Sai Kishore (GT) | Bowler | 85.0 | 93.5 | +10% | age<=28 |
| 9 | JR Hazlewood (RCB) | Bowler | 93.1 | 93.1 | +0% | — |
| 10 | E Malinga (SRH) | Bowler | 77.5 | 93.0 | +20% | age<=28, age<=25 |
| 11 | Shubman Gill (GT) | Batsman | 76.1 | 91.3 | +20% | age<=28, age<=25 |
| 12 | TA Boult (MI) | Bowler | 90.5 | 90.5 | +0% | — |
| 13 | CV Varun (KKR) | Bowler | 89.3 | 89.3 | +0% | — |
| 14 | Kuldeep Yadav (DC) | Bowler | 88.6 | 88.6 | +0% | — |
| 15 | A Kamboj (CSK) | Bowler | 73.2 | 87.8 | +20% | age<=28, age<=25 |
| 16 | MR Marsh (LSG) | Batsman | 86.7 | 86.7 | +0% | — |
| 17 | Abhishek Sharma (SRH) | Batsman | 71.2 | 85.4 | +20% | age<=28, age<=25 |
| 18 | SA Yadav (MI) | Batsman | 85.2 | 85.2 | +0% | — |
| 19 | Harshit Rana (KKR) | Bowler | 71.0 | 85.2 | +20% | age<=28, age<=25 |
| 20 | YBK Jaiswal (RR) | Batsman | 69.6 | 83.5 | +20% | age<=28, age<=25 |

### SRH

| Rank | Player | Role | Base | SRH Value | +% | Triggers |
|------|--------|------|------|----------|-----|----------|
| 1 | B Sai Sudharsan (GT) | Batsman | 94.3 | 117.9 | +25% | SR>150, runs>=400 |
| 2 | MR Marsh (LSG) | Batsman | 86.7 | 108.4 | +25% | SR>150, runs>=400 |
| 3 | SA Yadav (MI) | Batsman | 85.2 | 106.5 | +25% | SR>150, runs>=400 |
| 4 | M Prasidh Krishna (GT) | Bowler | 100.0 | 100.0 | +0% | — |
| 5 | Noor Ahmad (CSK) | Bowler | 99.7 | 99.7 | +0% | — |
| 6 | JJ Bumrah (MI) | Bowler | 97.4 | 97.4 | +0% | — |
| 7 | SS Iyer (PBKS) | Batsman | 76.9 | 96.1 | +25% | SR>150, runs>=400 |
| 8 | Shubman Gill (GT) | Batsman | 76.1 | 95.1 | +25% | SR>150, runs>=400 |
| 9 | JR Hazlewood (RCB) | Bowler | 93.1 | 93.1 | +0% | — |
| 10 | JC Buttler (GT) | Wicketkeeper | 73.4 | 91.8 | +25% | SR>150, runs>=400 |
| 11 | H Klaasen (SRH) | Wicketkeeper | 72.6 | 90.8 | +25% | SR>150, runs>=400 |
| 12 | N Pooran (LSG) | Wicketkeeper | 72.5 | 90.6 | +25% | SR>150, runs>=400 |
| 13 | TA Boult (MI) | Bowler | 90.5 | 90.5 | +0% | — |
| 14 | CV Varun (KKR) | Bowler | 89.3 | 89.3 | +0% | — |
| 15 | Abhishek Sharma (SRH) | Batsman | 71.2 | 89.0 | +25% | SR>150, runs>=400 |
| 16 | Arshdeep Singh (PBKS) | Bowler | 88.9 | 88.9 | +0% | — |
| 17 | Kuldeep Yadav (DC) | Bowler | 88.6 | 88.6 | +0% | — |
| 18 | YBK Jaiswal (RR) | Batsman | 69.6 | 87.0 | +25% | SR>150, runs>=400 |
| 19 | V Kohli (RCB) | Batsman | 79.0 | 86.9 | +10% | runs>=400 |
| 20 | P Arya (PBKS) | Batsman | 68.8 | 86.0 | +25% | SR>150, runs>=400 |

## Summary Statistics

| Team | Avg Value | Max Value | Min Value | Players >100 |
|------|-----------|-----------|-----------|--------------|
| MI | 55.2 | 127.3 | 4.1 | 2 |
| CSK | 57.6 | 121.8 | 4.0 | 9 |
| RCB | 53.8 | 117.9 | 3.6 | 3 |
| RR | 52.8 | 122.6 | 4.3 | 2 |
| KKR | 51.6 | 115.0 | 3.6 | 5 |
| GT | 51.3 | 100.0 | 3.6 | 0 |
| LSG | 51.7 | 100.0 | 3.6 | 0 |
| PBKS | 54.2 | 117.9 | 3.6 | 3 |
| DC | 54.8 | 119.6 | 4.3 | 2 |
| SRH | 53.8 | 117.9 | 3.6 | 3 |

_Generated by team_strategy_engine.py — rules from team_strategy_rules.md_
