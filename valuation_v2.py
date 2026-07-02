"""
valuation_v2.py — Compute PlayerValueScore (0-100) from IPL performance data.

Input:  data/master_players.csv
Output: data/player_values.csv
        valuation_report.md
"""
import csv
import os
import statistics

MASTER = "data/master_players.csv"
VALUES_OUT = "data/player_values.csv"
REPORT = "valuation_report.md"

# Batting weights
W_RUNS = 0.35
W_BATAVG = 0.20
W_SR = 0.25
W_100S = 0.10
W_50S = 0.10

# Bowling weights
W_WKTS = 0.35
W_ECON = 0.35    # inverted (lower is better)
W_BOWLAVG = 0.30 # inverted (lower is better)


def safe_float(val, default=None):
    if val is None:
        return default
    val = val.strip()
    if val in ("", "-", "N/A", "n/a"):
        return default
    try:
        return float(val)
    except ValueError:
        return default


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def min_max(val, mn, mx):
    if mx == mn:
        return 50.0
    return (val - mn) / (mx - mn) * 100.0


def inv_min_max(val, mn, mx):
    """Higher raw value → lower score (for Economy, Bowling Avg)."""
    if mx == mn:
        return 50.0
    return (mx - val) / (mx - mn) * 100.0


class Scaler:
    """Accumulate values, then compute min/max for a population."""
    def __init__(self):
        self.vals = []

    def add(self, v):
        if v is not None:
            self.vals.append(v)

    def range(self):
        if not self.vals:
            return 0, 1
        return min(self.vals), max(self.vals)


def compute_bat_score(row, scalers):
    runs = safe_float(row.get("Runs"), 0)
    bavg = safe_float(row.get("BattingAverage"), 0)
    sr = safe_float(row.get("StrikeRate"), 0)
    c100 = safe_float(row.get("100s"), 0)
    c50 = safe_float(row.get("50s"), 0)

    for s, v in zip(scalers, [runs, bavg, sr, c100, c50]):
        s.add(v)

    score = (
        W_RUNS * min_max(runs, 0, 1) +
        W_BATAVG * min_max(bavg, 0, 1) +
        W_SR * min_max(sr, 0, 1) +
        W_100S * min_max(c100, 0, 1) +
        W_50S * min_max(c50, 0, 1)
    )
    return score


def compute_bowl_score(row, scalers):
    wkts = safe_float(row.get("Wickets"), 0)
    econ = safe_float(row.get("Economy"), None)
    bavg = safe_float(row.get("BowlingAverage"), None)

    # Only include bowling stats for players who actually bowled
    has_bowl = wkts is not None and wkts > 0

    if not has_bowl:
        for s in scalers:
            s.add(0)
        return 0.0

    wkts = wkts or 0
    econ = econ if econ is not None else 12.0  # default high economy
    bavg = bavg if bavg is not None else 50.0  # default high average

    for s, v in zip(scalers, [wkts, econ, bavg]):
        s.add(v)

    score = (
        W_WKTS * min_max(wkts, 0, 1) +
        W_ECON * inv_min_max(econ, 0, 1) +
        W_BOWLAVG * inv_min_max(bavg, 0, 1)
    )
    return score


def main():
    rows = read_csv(MASTER)
    total = len(rows)

    # ── Phase 1: Collect all stats to determine ranges ──
    bat_scalers = [Scaler() for _ in range(5)]   # runs, avg, sr, 100s, 50s
    bowl_scalers = [Scaler() for _ in range(3)]  # wkts, econ, bavg

    for row in rows:
        role = row.get("Role", "").strip()
        if role in ("Batsman", "Wicketkeeper", "All-Rounder"):
            compute_bat_score(row, bat_scalers)
        if role in ("Bowler", "All-Rounder"):
            compute_bowl_score(row, bowl_scalers)

    bat_ranges = [s.range() for s in bat_scalers]
    bowl_ranges = [s.range() for s in bowl_scalers]

    # ── Phase 2: Compute final scores with actual ranges ──
    # Build reusable scalers with fixed ranges
    def bat_score_fixed(row):
        runs = safe_float(row.get("Runs"), 0)
        bavg = safe_float(row.get("BattingAverage"), 0)
        sr = safe_float(row.get("StrikeRate"), 0)
        c100 = safe_float(row.get("100s"), 0)
        c50 = safe_float(row.get("50s"), 0)
        rng = bat_ranges
        return (
            W_RUNS * min_max(runs, rng[0][0], rng[0][1]) +
            W_BATAVG * min_max(bavg, rng[1][0], rng[1][1]) +
            W_SR * min_max(sr, rng[2][0], rng[2][1]) +
            W_100S * min_max(c100, rng[3][0], rng[3][1]) +
            W_50S * min_max(c50, rng[4][0], rng[4][1])
        )

    def bowl_score_fixed(row):
        wkts = safe_float(row.get("Wickets"), 0)
        econ = safe_float(row.get("Economy"), None)
        bavg = safe_float(row.get("BowlingAverage"), None)
        has_bowl = wkts is not None and wkts > 0 and econ is not None and bavg is not None

        if not has_bowl:
            return 0.0

        rng = bowl_ranges
        return (
            W_WKTS * min_max(wkts, rng[0][0], rng[0][1]) +
            W_ECON * inv_min_max(econ, rng[1][0], rng[1][1]) +
            W_BOWLAVG * inv_min_max(bavg, rng[2][0], rng[2][1])
        )

    results = []
    for row in rows:
        role = row.get("Role", "").strip()
        score = 0.0

        if role in ("Batsman", "Wicketkeeper"):
            score = bat_score_fixed(row)
        elif role == "Bowler":
            score = bowl_score_fixed(row)
        elif role == "All-Rounder":
            b = bat_score_fixed(row)
            c = bowl_score_fixed(row)
            # If they have both contributions, average them; if only one, use it
            if b > 0 and c > 0:
                score = (b + c) / 2.0
            elif b > 0:
                score = b
            elif c > 0:
                score = c

        # Normalise final score to 0-100 across all players
        results.append((row, score))

    # Final 0-100 normalisation across all players
    all_scores = [s for _, s in results]
    mn, mx = min(all_scores), max(all_scores)
    final = []
    for row, s in results:
        final_score = min_max(s, mn, mx)
        # Clamp to 0-100
        final_score = max(0.0, min(100.0, final_score))
        final.append((row, final_score))

    # ── Write player_values.csv ──
    # Sort by score descending
    final.sort(key=lambda x: -x[1])

    os.makedirs(os.path.dirname(VALUES_OUT), exist_ok=True)
    with open(VALUES_OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Player", "Role", "PlayerValueScore", "AuctionPrice", "AcquisitionType"
        ])
        writer.writeheader()
        for row, score in final:
            price_raw = row.get("AuctionPrice", "N/A")
            # Clean price: handle "N/A", "1N/A", etc.
            price = safe_float(price_raw)
            writer.writerow({
                "Player": row["Player"],
                "Role": row["Role"],
                "PlayerValueScore": round(score, 1),
                "AuctionPrice": f"{price:.1f}" if price is not None else "N/A",
                "AcquisitionType": row.get("AcquisitionType", "N/A"),
            })

    # ── Console output ──
    print(f"Top 20 players by PlayerValueScore:\n")
    print(f"{'Rank':<5} {'Player':<35} {'Role':<15} {'Score':<8} {'Price':<8} {'Type':<12}")
    print("-" * 85)
    for i, (row, score) in enumerate(final[:20], 1):
        p = safe_float(row.get("AuctionPrice"))
        price = f"{p:.1f}" if p is not None else "N/A"
        print(f"{i:<5} {row['Player']:<35} {row['Role']:<15} {score:<8.1f} {price:<8} {row.get('AcquisitionType', 'N/A'):<12}")

    print(f"\nBottom 20 players by PlayerValueScore:\n")
    print(f"{'Rank':<5} {'Player':<35} {'Role':<15} {'Score':<8} {'Price':<8} {'Type':<12}")
    print("-" * 85)
    for i, (row, score) in enumerate(final[-20:], total - 19):
        p = safe_float(row.get("AuctionPrice"))
        price = f"{p:.1f}" if p is not None else "N/A"
        print(f"{i:<5} {row['Player']:<35} {row['Role']:<15} {score:<8.1f} {price:<8} {row.get('AcquisitionType', 'N/A'):<12}")

    # Average score by role
    by_role = {}
    for row, score in final:
        r = row["Role"]
        by_role.setdefault(r, []).append(score)
    print(f"\nAverage score by role:\n")
    for r in ["Batsman", "Bowler", "All-Rounder", "Wicketkeeper"]:
        scores = by_role.get(r, [])
        if scores:
            avg = statistics.mean(scores)
            print(f"  {r:<15s} {avg:.1f} (n={len(scores)})")

    # ── Write valuation_report.md ──
    with open(REPORT, "w") as f:
        f.write("# Player Valuation Report — IPL 2025 Season\n\n")
        f.write(f"Generated from `{MASTER}` — {total} players\n\n")
        f.write("## Formula\n\n")
        f.write("### Batsmen & Wicketkeepers\n\n")
        f.write("score = ")
        f.write(f"{W_RUNS*100:.0f}% × Runs(normalised) + ")
        f.write(f"{W_BATAVG*100:.0f}% × BattingAverage(normalised) + ")
        f.write(f"{W_SR*100:.0f}% × StrikeRate(normalised) + ")
        f.write(f"{W_100S*100:.0f}% × 100s(normalised) + ")
        f.write(f"{W_50S*100:.0f}% × 50s(normalised)\n\n")

        f.write("### Bowlers\n\n")
        f.write("score = ")
        f.write(f"{W_WKTS*100:.0f}% × Wickets(normalised) + ")
        f.write(f"{W_ECON*100:.0f}% × Economy⁻¹(normalised) + ")
        f.write(f"{W_BOWLAVG*100:.0f}% × BowlingAverage⁻¹(normalised)\n\n")
        f.write("Economy and Bowling Average are inverted — lower raw values yield higher scores.\n\n")

        f.write("### All-Rounders\n\n")
        f.write("score = (batting_score + bowling_score) / 2\n")
        f.write("If only batting or only bowling data is available, that single component is used.\n\n")

        f.write("## Normalisation\n\n")
        f.write("All raw statistics are min-max scaled to 0–100 across the player pool:\n\n")
        f.write("```\nnormalised = (value - min) / (max - min) × 100\n```\n\n")
        f.write("For inverted metrics (Economy, Bowling Average):\n\n")
        f.write("```\nnormalised = (max - value) / (max - min) × 100\n```\n\n")
        f.write("After computing the weighted sum, the final score is re-normalised to 0–100 across all players.\n\n")

        f.write("## Statistical Ranges\n\n")
        f.write("| Metric | Min | Max |\n")
        f.write("|--------|-----|-----|\n")
        f.write(f"| Runs | {bat_ranges[0][0]:.0f} | {bat_ranges[0][1]:.0f} |\n")
        f.write(f"| Batting Average | {bat_ranges[1][0]:.1f} | {bat_ranges[1][1]:.1f} |\n")
        f.write(f"| Strike Rate | {bat_ranges[2][0]:.1f} | {bat_ranges[2][1]:.1f} |\n")
        f.write(f"| 100s | {bat_ranges[3][0]:.0f} | {bat_ranges[3][1]:.0f} |\n")
        f.write(f"| 50s | {bat_ranges[4][0]:.0f} | {bat_ranges[4][1]:.0f} |\n")
        f.write(f"| Wickets | {bowl_ranges[0][0]:.0f} | {bowl_ranges[0][1]:.0f} |\n")
        f.write(f"| Economy | {bowl_ranges[1][0]:.1f} | {bowl_ranges[1][1]:.1f} |\n")
        f.write(f"| Bowling Average | {bowl_ranges[2][0]:.1f} | {bowl_ranges[2][1]:.1f} |\n\n")

        f.write("## Summary Statistics\n\n")
        f.write("| Role | Count | Mean Score | Min Score | Max Score |\n")
        f.write("|------|-------|------------|-----------|-----------|\n")
        for r in ["Batsman", "Bowler", "All-Rounder", "Wicketkeeper"]:
            scores = by_role.get(r, [])
            if scores:
                mn_r = min(scores)
                mx_r = max(scores)
                avg_r = statistics.mean(scores)
                f.write(f"| {r} | {len(scores)} | {avg_r:.1f} | {mn_r:.1f} | {mx_r:.1f} |\n")

        f.write(f"\n| **All** | {total} | {statistics.mean(all_scores):.1f} | {mn:.1f} | {mx:.1f} |\n\n")

        f.write("## Top 20 Players by Value\n\n")
        f.write("| Rank | Player | Role | Score | Price (Cr) |\n")
        f.write("|------|--------|------|-------|------------|\n")
        for i, (row, score) in enumerate(final[:20], 1):
            p = safe_float(row.get("AuctionPrice"))
            price = f"{p:.1f} Cr" if p is not None else "N/A"
            f.write(f"| {i} | {row['Player']} | {row['Role']} | {score:.1f} | {price} |\n")

        f.write("\n## Bottom 20 Players by Value\n\n")
        f.write("| Rank | Player | Role | Score | Price (Cr) |\n")
        f.write("|------|--------|------|-------|------------|\n")
        for i, (row, score) in enumerate(final[-20:], total - 19):
            p = safe_float(row.get("AuctionPrice"))
            price = f"{p:.1f} Cr" if p is not None else "N/A"
            f.write(f"| {i} | {row['Player']} | {row['Role']} | {score:.1f} | {price} |\n")

    print(f"\n✓ {VALUES_OUT} written ({len(final)} players)")
    print(f"✓ {REPORT} written")


if __name__ == "__main__":
    main()
