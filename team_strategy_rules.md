# Team Strategy Rules

Each franchise applies value multipliers to every player based on
their strategic preferences.  All multipliers stack additively.

## CSK — Experience & Core
| Trigger | Bonus | Source Column |
|---------|-------|--------------|
| Age >= 30 | +15% | Age |
| Nationality == India | +10% | Nationality |
| Role == All-Rounder | +10% | Role |

## MI — Young & Explosive
| Trigger | Bonus | Source Column |
|---------|-------|--------------|
| Age <= 25 | +15% | Age |
| StrikeRate > 145 (Batsman/WK/AR only) | +10% | StrikeRate |
| Runs >= 200 AND Age <= 23 (breakthrough batter) | +10% | Runs, Age |
| Role == Bowler AND Age <= 26 | +10% | Role, Age |

## RR — Next-Gen Talent
| Trigger | Bonus | Source Column |
|---------|-------|--------------|
| Age <= 23 | +20% | Age |
| Runs >= 200 AND Age <= 23 (young breakouts) | +10% | Runs, Age |
| Age 24-26 | +10% | Age |

## KKR — Spin Power
| Trigger | Bonus | Source Column |
|---------|-------|--------------|
| Mystery spinner bonus skipped (no bowling-style data) | — | — |
| Role == Bowler | +10% | Role |
| Wickets >= 10 | +10% | Wickets |
| Economy <= 8.5 | +5% | Economy |

## RCB — Bash Brothers
| Trigger | Bonus | Source Column |
|---------|-------|--------------|
| Role is Batsman/WK/AR AND StrikeRate > 150 | +15% | Role, StrikeRate |
| Runs >= 400 (proven run-scorer) | +10% | Runs |

## GT — Flexible All-Rounders
| Trigger | Bonus | Source Column |
|---------|-------|--------------|
| Role == All-Rounder | +10% | Role |
| Role == All-Rounder AND (Runs >= 200 AND Wickets >= 5) | +10% | Role, Runs, Wickets |

## LSG — Wicketkeepers Core
| Trigger | Bonus | Source Column |
|---------|-------|--------------|
| Role == Wicketkeeper | +10% | Role |
| Role == Wicketkeeper AND Runs >= 300 | +10% | Role, Runs |

## PBKS — Power Hitters
| Trigger | Bonus | Source Column |
|---------|-------|--------------|
| Role is Batsman/WK/AR AND StrikeRate > 150 | +15% | Role, StrikeRate |
| Runs >= 300 | +10% | Runs |

## DC — Young Core
| Trigger | Bonus | Source Column |
|---------|-------|--------------|
| Age <= 28 | +10% | Age |
| Age <= 25 | +10% | Age |
| Nationality == India | +5% | Nationality |

## SRH — Aggressive Batters
| Trigger | Bonus | Source Column |
|---------|-------|--------------|
| Role is Batsman/WK/AR AND StrikeRate > 150 | +15% | Role, StrikeRate |
| Runs >= 400 | +10% | Runs |
