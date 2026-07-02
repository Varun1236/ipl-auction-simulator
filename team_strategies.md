
***

## General notation for simulation rules

Use these as parameters for each team’s agent:

- `role_prefs`: list of preferred roles with weights (e.g., [opener: 1.2, finisher: 1.0, fast_bowler: 0.9, ...])
- `age_band_prefs`: weights for age bands:
  - `young`: 18–22
  - `mid`: 23–27
  - `veteran`: 28–34
- `domestic_overseas_bias`: multiplier for domestic vs overseas (e.g., 1.3 for domestic, 0.8 for overseas).
- `experience_bias`: multiplier for capped vs uncapped (e.g., 1.2 for capped, 0.9 for uncapped).
- `price_band_strategy`: how aggressively they bid in each price band:
  - `low`: ≤ ₹50 lakh
  - `mid`: ₹50 lakh–₹5 crore
  - `high`: > ₹5 crore
- `spend_intensity`: overall willingness to spend (e.g., 0.8 = conservative, 1.3 = aggressive).

***

## 1. Chennai Super Kings (CSK)

### 1. Auction behavior (2022–2026)
- **Pattern**: Conservative spend, heavy retentions, auction as “fine-tuning” rather than rebuild.
- **Evidence**: In 2025, CSK bought 20 players, with top spend: Noor Ahmad (10 Cr), Ashwin (9.75 Cr), Devon Conway (6.25 Cr), but overall purse discipline. [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)
- In 2026 mini-auction, CSK made big bets on **uncapped Indians** (e.g., 14.20 Cr combined on multiple uncapped picks), showing late-round value hunting. [youtube](https://www.youtube.com/watch?v=64QUbxsqo2I)

### 2. Preferred player profiles (measurable)
- Strong on:
  - **Spinners** (especially leg-spinners and wrist-spinners): Noor Ahmad, Ashwin.
  - **Adapted overseas openers/middle-order**: Devon Conway.
  - **Experienced Indian all-rounders/utility**: Vijay Shankar, Deepak Hooda.

**Simulation rule**:
```python
role_prefs = {
    "spinner": 1.4,
    "all_rounder": 1.1,
    "opener": 1.0,
    "finisher": 1.0,
    "fast_bowler": 0.8
}
experience_bias = {"capped": 1.2, "uncapped": 0.9}
age_band_prefs = {"young": 0.7, "mid": 1.0, "veteran": 1.1}
```

### 3. Age preferences
- **Evidence**: Buy Ashwin (34+), Vijay Shankar (30+), Conway (30+), but also mid-aged uncapped (20–25).
- **Preference**: Slight skew to **veteran** for key roles; mid-aged for utility.

**Rule**:
```python
age_band_prefs = {"young": 0.7, "mid": 1.0, "veteran": 1.1}
```

### 4. Role priorities
- **Opener / middle-order batter**: ~1–2 slots.
- **Wrist-spin / off-spin**: 2+ priority.
- **Finisher / all-rounder**: 1–2.
- **Fast bowler**: secondary.

**Rule**:
```python
role_prefs = {
    "opener": 1.0,
    "middle_order": 1.0,
    "finisher": 1.0,
    "spinner": 1.4,
    "all_rounder": 1.1,
    "fast_bowler": 0.8
}
```

### 5. Domestic vs overseas
- **Evidence**: 4 overseas slots, but heavily skewed to **British/South African/Australian**; rest domestic spinners and utility.
- **Rule**:
```python
domestic_overseas_bias = {"domestic": 1.3, "overseas": 0.9}
overseas_country_preference = ["England", "South Africa", "Australia"]
```

### 6. Proven vs undervalued
- **Evidence**: Retains proven stars; in auction, buys **undervalued uncapped** (Anshul Kamboj, Gurjapneet, Vijay Shankar-like utility).
- **Rule**:
```python
experience_bias = {"capped": 1.2, "uncapped": 0.9}
undervalued_bonus = 0.2  # extra weight if player has strong past IPL performance but low base price
```

### 7. Examples
- **2025**: Noor Ahmad (10 Cr), Ashwin (9.75 Cr), Devon Conway (6.25 Cr), Syed Khaleel (4.8 Cr), Rachin Ravindra (4 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)
- **2026 mini**: Heavy uncapped bets, late-round value buys. [youtube](https://www.youtube.com/watch?v=64QUbxsqo2I)

**Simulation rule**:
```python
price_band_strategy = {
    "low": 1.2,    # aggressive in uncapped/value
    "mid": 1.0,    # normal
    "high": 0.8    # avoid big marquee unless perfect fit
}
spend_intensity = 0.9
```

***

## 2. Mumbai Indians (MI)

### 1. Auction behavior
- **Pattern**: Historically marquee-heavy; 2024–2026 shifted to **role-based buying** and sometimes “quiet auction” if core stable.
- **Evidence**: 2025 squad: Trent Boult (12.5 Cr), Deepak Chahar (9.25 Cr), Will Jacks (5.25 Cr), Naman Dhir (5.25 Cr uncapped). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

### 2. Preferred profiles
- **Fast-bowling all-rounders** and **death bowlers**: Boult, Chahar.
- **Power hitters / all-rounders**: Will Jacks, Naman Dhir (uncapped).
- **Spin options**: Santner.

**Rule**:
```python
role_prefs = {
    "fast_bowler": 1.4,
    "all_rounder": 1.3,
    "opener": 1.0,
    "finisher": 1.1,
    "spinner": 0.8
}
experience_bias = {"capped": 1.1, "uncapped": 1.0}  # open to uncapped if role clear
```

### 3. Age preferences
- **Evidence**: Boult (30+), Chahar (mid), Jacks (mid), but also uncapped 20–24.
- **Preference**: **mid** and **young** for pace, **veteran** for experienced death bowlers.

**Rule**:
```python
age_band_prefs = {"young": 1.0, "mid": 1.1, "veteran": 1.0}
```

### 4. Role priorities
- Top priority: **death bowler (pace)**, **fast-bowling all-rounder**.
- Secondary: **opener / power hitter**, **finisher**.

**Rule**:
```python
role_prefs = {
    "fast_bowler": 1.4,
    "all_rounder": 1.3,
    "opener": 1.0,
    "finisher": 1.1,
    "spinner": 0.8,
    "wicketkeeper": 0.7
}
```

### 5. Domestic vs overseas
- **Evidence**: Heavy on **English/Australian/South African** all-rounders and pace; Indian pace and uncapped utility.
- **Rule**:
```python
domestic_overseas_bias = {"domestic": 1.0, "overseas": 1.1}
overseas_country_preference = ["England", "Australia", "South Africa"]
```

### 6. Proven vs undervalued
- **Evidence**: Willing to pay big for proven (Boult, Chahar) but also invest in uncapped if role clear (Naman Dhir).
- **Rule**:
```python
experience_bias = {"capped": 1.1, "uncapped": 1.0}
price_band_strategy = {
    "low": 0.9,
    "mid": 1.0,
    "high": 1.1  # marquee for key roles
}
spend_intensity = 1.1
```

### 7. Examples
- **2025**: Boult (12.5 Cr), Chahar (9.25 Cr), Jacks (5.25 Cr), Naman Dhir (5.25 Cr uncapped), Santner (2 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

***

## 3. Royal Challengers Bengaluru (RCB)

### 1. Auction behavior
- **Pattern**: Traditionally marquee-first (Kohli, Maxwell, du Plessis), 2024–2026: **rebuild-oriented**, buying to fill gaps.
- **Evidence**: 2025: Hazlewood (12.5 Cr), Phil Salt (11.5 Cr), Jitesh Sharma (11 Cr), Bhuvneshwar (10.75 Cr), Livingstone (8.75 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

### 2. Preferred profiles
- **Explosive openers**: Phil Salt.
- **Finishers / all-rounders**: Jitesh (finisher WK), Livingstone, Krunal Pandya.
- **Strike pacers**: Hazlewood, Bhuvneshwar.

**Rule**:
```python
role_prefs = {
    "opener": 1.4,
    "finisher": 1.3,
    "all_rounder": 1.2,
    "fast_bowler": 1.1,
    "spinner": 0.8
}
```

### 3. Age preferences
- **Evidence**: Salt (mid), Hazlewood (veteran), Bhuvneshwar (veteran), Krunal (veteran), but also 20–24 uncapped.
- **Preference**: **mid** and **veteran** for key batting/pace roles.

**Rule**:
```python
age_band_prefs = {"young": 0.8, "mid": 1.1, "veteran": 1.2}
```

### 4. Role priorities
- Priority: **opener**, **finisher**, **strike pacer**.
- Secondary: **all-rounder**, **spinner**.

**Rule**:
```python
role_prefs = {
    "opener": 1.4,
    "finisher": 1.3,
    "all_rounder": 1.2,
    "fast_bowler": 1.1,
    "spinner": 0.8,
    "wicketkeeper": 1.0
}
```

### 5. Domestic vs overseas
- **Evidence**: Heavy on **English/Australian/South African** power hitters and pace; Indian veterans and uncapped batters.
- **Rule**:
```python
domestic_overseas_bias = {"domestic": 0.9, "overseas": 1.2}
overseas_country_preference = ["England", "Australia", "South Africa"]
```

### 6. Proven vs undervalued
- **Evidence**: Big spend on proven (Salt, Hazlewood, Bhuvi), but also uncapped (Rasikh Dar, Suyash Sharma).
- **Rule**:
```python
experience_bias = {"capped": 1.2, "uncapped": 0.9}
price_band_strategy = {
    "low": 0.9,
    "mid": 1.0,
    "high": 1.3  # aggressive on marquee
}
spend_intensity = 1.2
```

### 7. Examples
- **2025**: Hazlewood (12.5 Cr), Phil Salt (11.5 Cr), Jitesh (11 Cr), Bhuvneshwar (10.75 Cr), Livingstone (8.75 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

***

## 4. Rajasthan Royals (RR)

### 1. Auction behavior
- **Pattern**: **Value-first, smart buying**, not chasing marquee blindly.
- **Evidence**: 2025: Archer (12.5 Cr), Tushar Deshpande (6.5 Cr), Hasaranga (5.25 Cr), Theekshana (4.4 Cr), Nitish Rana (4.2 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)
- Also many uncapped (Akash Madhwal, Vaibhav Suryavanshi, Shubham Dubey).

### 2. Preferred profiles
- **Strike pacers**: Jofra Archer, Tushar Deshpande.
- **Quality spinners**: Hasaranga, Theekshana.
- **Versatile batters**: Nitish Rana, Karun Nair-like.

**Rule**:
```python
role_prefs = {
    "fast_bowler": 1.3,
    "spinner": 1.3,
    "opener": 1.0,
    "middle_order": 1.1,
    "all_rounder": 1.0,
    "finisher": 1.0
}
```

### 3. Age preferences
- **Evidence**: Archer (mid), Tushar (mid), Hasaranga (mid), but also young uncapped (Vaibhav Suryavanshi 13).
- **Preference**: **mid** and **young**.

**Rule**:
```python
age_band_prefs = {"young": 1.1, "mid": 1.2, "veteran": 0.8}
```

### 4. Role priorities
- Priority: **strike pacer**, **quality spinner**, **versatile middle-order**.
- Secondary: **opener**, **finisher**.

**Rule**:
```python
role_prefs = {
    "fast_bowler": 1.3,
    "spinner": 1.3,
    "middle_order": 1.1,
    "opener": 1.0,
    "finisher": 1.0,
    "all_rounder": 1.0
}
```

### 5. Domestic vs overseas
- **Evidence**: Mix of **Afghan/Sri Lankan/Australian** spinners and pace; Indian middle-order and uncapped.
- **Rule**:
```python
domestic_overseas_bias = {"domestic": 1.0, "overseas": 1.1}
overseas_country_preference = ["Australia", "Afghanistan", "Sri Lanka", "England"]
```

### 6. Proven vs undervalued
- **Evidence**: Big on proven (Archer, Hasaranga), but also invest heavily in uncapped (Vaibhav Suryavanshi 1.1 Cr).
- **Rule**:
```python
experience_bias = {"capped": 1.1, "uncapped": 1.0}
price_band_strategy = {
    "low": 1.2,
    "mid": 1.0,
    "high": 1.0  # moderate marquee
}
spend_intensity = 1.0
```

### 7. Examples
- **2025**: Archer (12.5 Cr), Tushar (6.5 Cr), Hasaranga (5.25 Cr), Theekshana (4.4 Cr), Vaibhav Suryavanshi (1.1 Cr uncapped). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

***

## 5. Kolkata Knight Riders (KKR)

### 1. Auction behavior
- **Pattern**: Historically aggressive, heavy spend; 2026 mini: **all-in approach**, spending heavily.
- **Evidence**: 2025: Venkatesh Iyer (23.75 Cr), Nortje (6.5 Cr), de Kock (3.6 Cr), Johnson (2.8 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

### 2. Preferred profiles
- **Explosive openers**: de Kock, Venkatesh (middle but explosive).
- **Strike pacers**: Nortje, Spencer Johnson.
- **All-rounders**: Moeen Ali, Rovman Powell.

**Rule**:
```python
role_prefs = {
    "opener": 1.4,
    "fast_bowler": 1.3,
    "all_rounder": 1.2,
    "finisher": 1.1,
    "spinner": 0.9
}
```

### 3. Age preferences
- **Evidence**: de Kock (mid), Nortje (mid), Venkatesh (mid), but also young.
- **Preference**: **mid** and **young**.

**Rule**:
```python
age_band_prefs = {"young": 1.0, "mid": 1.2, "veteran": 0.9}
```

### 4. Role priorities
- Priority: **opener**, **strike pacer**, **all-rounder**.
- Secondary: **finisher**, **spinner**.

**Rule**:
```python
role_prefs = {
    "opener": 1.4,
    "fast_bowler": 1.3,
    "all_rounder": 1.2,
    "finisher": 1.1,
    "spinner": 0.9
}
```

### 5. Domestic vs overseas
- **Evidence**: Heavy **English/South African/Australian** pace and power; Indian middle-order.
- **Rule**:
```python
domestic_overseas_bias = {"domestic": 0.9, "overseas": 1.2}
overseas_country_preference = ["England", "South Africa", "Australia"]
```

### 6. Proven vs undervalued
- **Evidence**: Big on proven (Venkatesh, Nortje, de Kock), but also uncapped (Angkrish, Vaibhav Arora).
- **Rule**:
```python
experience_bias = {"capped": 1.2, "uncapped": 0.9}
price_band_strategy = {
    "low": 0.9,
    "mid": 1.0,
    "high": 1.3  # aggressive on marquee
}
spend_intensity = 1.2
```

### 7. Examples
- **2025**: Venkatesh Iyer (23.75 Cr), Nortje (6.5 Cr), de Kock (3.6 Cr), Johnson (2.8 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

***

## 6. Gujarat Titans (GT)

### 1. Auction behavior
- **Pattern**: Disciplined, value-first; 2024–2026: **resist overspending**, focus on role clarity.
- **Evidence**: 2025: Buttler (15.75 Cr), Siraj (12.25 Cr), Rabada (10.75 Cr), Prasidh (9.5 Cr), Washington (3.2 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

### 2. Preferred profiles
- **Explosive opener**: Buttler.
- **Strike pacers**: Siraj, Rabada, Prasidh.
- **Utility all-rounders**: Washington, Sherfane.

**Rule**:
```python
role_prefs = {
    "opener": 1.3,
    "fast_bowler": 1.4,
    "all_rounder": 1.1,
    "spinner": 1.0,
    "finisher": 1.0
}
```

### 3. Age preferences
- **Evidence**: Buttler (mid), Siraj (mid), Rabada (mid), but also young uncapped.
- **Preference**: **mid** and **young**.

**Rule**:
```python
age_band_prefs = {"young": 1.0, "mid": 1.2, "veteran": 0.8}
```

### 4. Role priorities
- Priority: **strike pacer**, **opener**, **utility all-rounder**.
- Secondary: **spinner**, **finisher**.

**Rule**:
```python
role_prefs = {
    "fast_bowler": 1.4,
    "opener": 1.3,
    "all_rounder": 1.1,
    "spinner": 1.0,
    "finisher": 1.0
}
```

### 5. Domestic vs overseas
- **Evidence**: **South African/Australian** pace and batting; Indian core.
- **Rule**:
```python
domestic_overseas_bias = {"domestic": 1.0, "overseas": 1.1}
overseas_country_preference = ["South Africa", "Australia", "England"]
```

### 6. Proven vs undervalued
- **Evidence**: Big on proven (Buttler, Siraj, Rabada), but also uncapped (Mahipal Lomror, Gurnoor Brar).
- **Rule**:
```python
experience_bias = {"capped": 1.1, "uncapped": 1.0}
price_band_strategy = {
    "low": 1.1,
    "mid": 1.0,
    "high": 1.0  # moderate marquee
}
spend_intensity = 1.0
```

### 7. Examples
- **2025**: Buttler (15.75 Cr), Siraj (12.25 Cr), Rabada (10.75 Cr), Prasidh (9.5 Cr), Washington (3.2 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

***

## 7. Lucknow Super Giants (LSG)

### 1. Auction behavior
- **Pattern**: Balanced, measured; 2025: **big on Rishabh Pant**, but still value-focused.
- **Evidence**: 2025: Pant (27 Cr), Avesh (9.75 Cr), Akash Deep (8 Cr), Miller (7.5 Cr), Mitchell Marsh (3.4 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

### 2. Preferred profiles
- **WK-batter / finisher**: Pant, David Miller.
- **Strike pacers**: Avesh, Akash Deep.
- **All-rounders**: Mitchell Marsh, Shahbaz.

**Rule**:
```python
role_prefs = {
    "wicketkeeper": 1.4,
    "finisher": 1.3,
    "fast_bowler": 1.2,
    "all_rounder": 1.1,
    "opener": 0.9
}
```

### 3. Age preferences
- **Evidence**: Pant (mid), Miller (veteran), Avesh (mid), but also young uncapped.
- **Preference**: **mid** and **veteran** for key roles.

**Rule**:
```python
age_band_prefs = {"young": 0.9, "mid": 1.1, "veteran": 1.0}
```

### 4. Role priorities
- Priority: **WK-batter**, **finisher**, **strike pacer**.
- Secondary: **all-rounder**, **opener**.

**Rule**:
```python
role_prefs = {
    "wicketkeeper": 1.4,
    "finisher": 1.3,
    "fast_bowler": 1.2,
    "all_rounder": 1.1,
    "opener": 0.9
}
```

### 5. Domestic vs overseas
- **Evidence**: **South African/Australian** finishers and pace; Indian core.
- **Rule**:
```python
domestic_overseas_bias = {"domestic": 1.0, "overseas": 1.1}
overseas_country_preference = ["South Africa", "Australia"]
```

### 6. Proven vs undervalued
- **Evidence**: Big on proven (Pant, Miller, Avesh), but also uncapped (Abdul Samad, etc.).
- **Rule**:
```python
experience_bias = {"capped": 1.1, "uncapped": 1.0}
price_band_strategy = {
    "low": 1.0,
    "mid": 1.0,
    "high": 1.2  # marquee for key roles
}
spend_intensity = 1.1
```

### 7. Examples
- **2025**: Pant (27 Cr), Avesh (9.75 Cr), Akash Deep (8 Cr), Miller (7.5 Cr), Abdul Samad (4.2 Cr uncapped). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

***

## 8. Punjab Kings (PBKS)

### 1. Auction behavior
- **Pattern**: Historically marquee-heavy; 2024–2026: **rebuild with big names**.
- **Evidence**: 2025: Shreyas Iyer (26.75 Cr), Chahal (18 Cr), Arshdeep (18 Cr), Stoinis (11 Cr), Marcus Jansen (7 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

### 2. Preferred profiles
- **Leadership / middle-order**: Shreyas Iyer.
- **Strike spinner**: Chahal.
- **Strike pacer**: Arshdeep.
- **All-rounders**: Stoinis, Jansen.

**Rule**:
```python
role_prefs = {
    "middle_order": 1.4,
    "spinner": 1.3,
    "fast_bowler": 1.3,
    "all_rounder": 1.2,
    "opener": 1.0
}
```

### 3. Age preferences
- **Evidence**: Iyer (mid), Chahal (mid), Arshdeep (mid), Stoinis (mid/veteran).
- **Preference**: **mid** and **veteran** for key roles.

**Rule**:
```python
age_band_prefs = {"young": 0.8, "mid": 1.2, "veteran": 1.0}
```

### 4. Role priorities
- Priority: **middle-order batter**, **strike spinner**, **strike pacer**.
- Secondary: **all-rounder**, **opener**.

**Rule**:
```python
role_prefs = {
    "middle_order": 1.4,
    "spinner": 1.3,
    "fast_bowler": 1.3,
    "all_rounder": 1.2,
    "opener": 1.0
}
```

### 5. Domestic vs overseas
- **Evidence**: Heavy **English/Australian/South African** all-rounders and pace; Indian core.
- **Rule**:
```python
domestic_overseas_bias = {"domestic": 0.9, "overseas": 1.2}
overseas_country_preference = ["England", "Australia", "South Africa"]
```

### 6. Proven vs undervalued
- **Evidence**: Big on proven (Iyer, Chahal, Arshdeep, Stoinis), but also uncapped (Nehal Wadhera, Priyansh Arya).
- **Rule**:
```python
experience_bias = {"capped": 1.2, "uncapped": 0.9}
price_band_strategy = {
    "low": 0.9,
    "mid": 1.0,
    "high": 1.3  # aggressive on marquee
}
spend_intensity = 1.2
```

### 7. Examples
- **2025**: Shreyas Iyer (26.75 Cr), Chahal (18 Cr), Arshdeep (18 Cr), Stoinis (11 Cr), Marco Jansen (7 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

***

## 9. Delhi Capitals (DC)

### 1. Auction behavior
- **Pattern**: 2024–2026: **rebuild with marquee**, focus on balance and match-winners.
- **Evidence**: 2025: KL Rahul (14 Cr), Starc (11.75 Cr), Natarajan (10.75 Cr), Jake Fraser-McGurk (9 Cr), Mukesh Kumar (8 Cr), Harry Brook (6.25 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

### 2. Preferred profiles
- **Top-order batter**: KL Rahul, Harry Brook.
- **Strike pacers**: Starc, Natarajan, Mukesh.
- **Young explosive batters**: Fraser-McGurk.

**Rule**:
```python
role_prefs = {
    "opener": 1.3,
    "middle_order": 1.3,
    "fast_bowler": 1.4,
    "all_rounder": 1.0,
    "spinner": 0.9
}
```

### 3. Age preferences
- **Evidence**: Rahul (mid/veteran), Starc (mid), Natarajan (mid), Fraser-McGurk (young).
- **Preference**: **mid** and **young**.

**Rule**:
```python
age_band_prefs = {"young": 1.0, "mid": 1.2, "veteran": 0.9}
```

### 4. Role priorities
- Priority: **opener**, **middle-order**, **strike pacer**.
- Secondary: **all-rounder**, **spinner**.

**Rule**:
```python
role_prefs = {
    "opener": 1.3,
    "middle_order": 1.3,
    "fast_bowler": 1.4,
    "all_rounder": 1.0,
    "spinner": 0.9
}
```

### 5. Domestic vs overseas
- **Evidence**: **South African/Australian/English** pace and batting; Indian core.
- **Rule**:
```python
domestic_overseas_bias = {"domestic": 1.0, "overseas": 1.1}
overseas_country_preference = ["South Africa", "Australia", "England"]
```

### 6. Proven vs undervalued
- **Evidence**: Big on proven (Rahul, Starc, Natarajan), but also uncapped (Ashutosh Sharma, Sameer Rizvi).
- **Rule**:
```python
experience_bias = {"capped": 1.1, "uncapped": 1.0}
price_band_strategy = {
    "low": 1.0,
    "mid": 1.0,
    "high": 1.2  # marquee for key roles
}
spend_intensity = 1.1
```

### 7. Examples
- **2025**: KL Rahul (14 Cr), Starc (11.75 Cr), Natarajan (10.75 Cr), Jake Fraser-McGurk (9 Cr), Harry Brook (6.25 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

***

## 10. Sunrisers Hyderabad (SRH)

### 1. Auction behavior
- **Pattern**: 2024 title winners; 2025: **disciplined, value-first**, bolster existing core.
- **Evidence**: 2025: Ishan Kishan (11.25 Cr), Shami (10 Cr), Harshal (8 Cr), Rahul Chahar (3.2 Cr), Zampa (2.4 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

### 2. Preferred profiles
- **Top-order batter**: Ishan Kishan.
- **Strike pacer**: Shami, Harshal.
- **Spin options**: Rahul Chahar, Zampa.

**Rule**:
```python
role_prefs = {
    "opener": 1.3,
    "middle_order": 1.2,
    "fast_bowler": 1.4,
    "spinner": 1.2,
    "all_rounder": 1.0
}
```

### 3. Age preferences
- **Evidence**: Ishan (mid), Shami (veteran), Harshal (mid/veteran), but also young uncapped.
- **Preference**: **mid** and **veteran** for key roles.

**Rule**:
```python
age_band_prefs = {"young": 0.9, "mid": 1.1, "veteran": 1.0}
```

### 4. Role priorities
- Priority: **strike pacer**, **opener**, **quality spinner**.
- Secondary: **middle-order**, **all-rounder**.

**Rule**:
```python
role_prefs = {
    "fast_bowler": 1.4,
    "opener": 1.3,
    "spinner": 1.2,
    "middle_order": 1.2,
    "all_rounder": 1.0
}
```

### 5. Domestic vs overseas
- **Evidence**: **Australian/English** pace and spin; Indian core.
- **Rule**:
```python
domestic_overseas_bias = {"domestic": 1.0, "overseas": 1.1}
overseas_country_preference = ["Australia", "England"]
```

### 6. Proven vs undervalued
- **Evidence**: Big on proven (Ishan, Shami, Harshal), but also uncapped (Abhinav Manohar, Zeeshan Ansari).
- **Rule**:
```python
experience_bias = {"capped": 1.1, "uncapped": 1.0}
price_band_strategy = {
    "low": 1.0,
    "mid": 1.0,
    "high": 1.1  # moderate marquee
}
spend_intensity = 1.0
```

### 7. Examples
- **2025**: Ishan Kishan (11.25 Cr), Shami (10 Cr), Harshal (8 Cr), Rahul Chahar (3.2 Cr), Zampa (2.4 Cr). [mumbaiindians](https://www.mumbaiindians.com/ipl-auction)

***

## How to use these in an agent-based simulation

For each team agent:

1. Initialize with the above parameter sets (`role_prefs`, `age_band_prefs`, `domestic_overseas_bias`, etc.).
2. When a player comes up:
   - Compute a **bid score**:
     ```python
     score = (
         role_prefs[player.role] *
         age_band_prefs[player.age_band] *
         domestic_overseas_bias[player.origin] *
         experience_bias[player.experience] *
         price_band_strategy[player.price_band] *
         spend_intensity
     )
     ```
   - Bid aggressively if score is high, pass if low.
3. Add an **undervalued_bonus** for players with strong past IPL performance but low base price (especially for CSK, RR, GT).


# Chennai Super Kings (CSK)

## Quantifiable Preferences
- Age >= 30
- Indian player
- Spinner
- All-rounder
- Proven performer

## Candidate Rules
- Age >= 30: +15%
- Spinner: +10%
- Indian player: +5%
- All-rounder: +10%
- PlayerValueScore >= 75: +10%

---

# Mumbai Indians (MI)

## Quantifiable Preferences
- Age <= 25
- Emerging player
- Indian fast bowler
- Fast-bowling all-rounder
- High strike-rate batter

## Candidate Rules
- Age <= 25: +15%
- Indian player: +5%
- Fast bowler: +10%
- All-rounder: +10%
- Strike Rate above league average: +10%

---

# Rajasthan Royals (RR)

## Quantifiable Preferences
- Age <= 23
- Emerging player
- High-upside player
- Underpriced player
- Uncapped-type profile

## Candidate Rules
- Age <= 23: +20%
- Age 24-26: +10%
- Strike Rate above league average: +5%
- PlayerValueScore >= 70 and Age <= 25: +10%

---

# Kolkata Knight Riders (KKR)

## Quantifiable Preferences
- Spinner
- Wicket-taking bowler
- Mystery-spin profile
- Bowling strike rate
- Economy rate

## Candidate Rules
- Spinner: +15%
- Wickets above league average: +10%
- Bowling SR below league average: +10%
- Economy below league average: +5%
- Bowler role: +5%

---

# Gujarat Titans (GT)

## Quantifiable Preferences
- All-rounder
- Balanced player
- Consistent performer
- Reliable contributor

## Candidate Rules
- All-rounder: +15%
- Runs above league average: +5%
- Wickets above league average: +5%
- Age 25-30: +5%
- PlayerValueScore >= 70: +10%

---

# Lucknow Super Giants (LSG)

## Quantifiable Preferences
- Wicketkeeper
- Flexible batter
- Batting depth
- High-average players

## Candidate Rules
- Wicketkeeper: +15%
- Batting Average above league average: +10%
- Strike Rate above league average: +5%
- Age 24-30: +5%
- PlayerValueScore >= 70: +5%

---

# Punjab Kings (PBKS)

## Quantifiable Preferences
- Power hitter
- Aggressive batter
- Match winner
- High strike-rate player

## Candidate Rules
- Strike Rate above league average: +15%
- Batter role: +5%
- Runs above league average: +5%
- Six-hitting profile (proxy: very high SR(Strike Rate >= 160)): +10%
- Age <= 28: +5%

---

# Delhi Capitals (DC)

## Quantifiable Preferences
- Young Indian players
- Developing talent
- Future potential
- Strong domestic core

## Candidate Rules
- Age <= 28: +10%
- Indian player: +10%
- Age <= 23: +10%
- PlayerValueScore >= 70: +5%
- Emerging player profile: +10%

---

# Sunrisers Hyderabad (SRH)

## Quantifiable Preferences
- Aggressive batting
- Powerplay impact
- Explosive scoring
- Match-winning batters

## Candidate Rules
- Strike Rate above league average: +15%
- Runs above league average: +10%
- Batter role: +10%
- Age <= 30: +5%
- PlayerValueScore >= 75: +5%

---

# Royal Challengers Bengaluru (RCB)

## Quantifiable Preferences
- Elite batters
- High run scorers
- Star players
- Aggressive batting

## Candidate Rules
- Batter role: +15%
- Runs above league average: +10%
- Strike Rate above league average: +10%
- PlayerValueScore >= 80: +10%
- Age 24-32: +5%