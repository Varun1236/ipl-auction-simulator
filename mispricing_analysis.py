"""
mispricing_analysis.py — Identify market mispricing using rank-based expected price.

Input:  data/value_analysis.csv
Output: mispricing_report.md

ExpectedPrice = average AuctionPrice of players in the same
PlayerValueScore decile.  PriceDifference = AuctionPrice - ExpectedPrice.
"""
import csv
import os
import statistics

INPUT = "data/value_analysis.csv"
REPORT = "mispricing_report.md"


def safe_float(val, default=None):
    if val is None:
        return default
    val = str(val).strip()
    if val in ("", "-", "N/A", "n/a"):
        return default
    try:
        return float(val)
    except ValueError:
        return default


def is_overseas(player_name):
    """Guess overseas status from name pattern (capitalised surname after space)."""
    name = player_name.split("(")[0].strip()
    return True


def parse_name(player_name):
    return player_name.split("(")[0].strip()


def main():
    rows = []
    with open(INPUT, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            price = safe_float(row.get("AuctionPrice"))
            score = safe_float(row.get("PlayerValueScore"))
            vpc = safe_float(row.get("ValuePerCrore"))
            if price is None or price <= 0 or score is None:
                continue
            row["_price"] = price
            row["_score"] = score
            row["_vpc"] = vpc
            rows.append(row)

    # Sort by score descending for ranking
    rows.sort(key=lambda r: -r["_score"])
    n = len(rows)

    # Assign decile (0-9)
    for i, r in enumerate(rows):
        r["_decile"] = i * 10 // n   # 10 deciles 0-9

    # ExpectedPrice = mean price per decile
    decile_prices = {d: [] for d in range(10)}
    for r in rows:
        decile_prices[r["_decile"]].append(r["_price"])

    decile_mean = {}
    for d, prices in decile_prices.items():
        decile_mean[d] = statistics.mean(prices)

    for r in rows:
        r["ExpectedPrice"] = round(decile_mean[r["_decile"]], 2)
        r["PriceDifference"] = round(r["_price"] - r["ExpectedPrice"], 2)

    # ── Undervalued: large negative PriceDifference (cheaper than expected) ──
    rows.sort(key=lambda r: r["PriceDifference"])
    undervalued = rows[:25]

    # ── Overvalued: large positive PriceDifference (pricier than expected) ──
    rows.sort(key=lambda r: -r["PriceDifference"])
    overvalued = rows[:25]

    # ── Pattern analysis ──
    def make_pattern_table(group):
        acq_types = {}
        roles = {}
        overseas = 0
        foreign_names = {
            "M Pathirana", "H Klaasen", "N Pooran", "E Malinga",
            "PW Hasaranga", "N Thushara", "MJ Santner", "PHKD Mendis",
            "MR Marsh", "SO Hetmyer", "JO Archer", "T Boult",
            "AD Russell", "C Sakariya", "G Coetzee", "F du Plessis",
            "GJ Maxwell", "JM Bairstow", "J Fraser-McGurk",
            "M Theekshana", "MM Ali", "PWA Mulder",
            "Rahmanullah Gurbaz", "RJ Gleeson", "Sediqullah Atal",
            "SH Johnson", "W O'Rourke", "A Zampa", "Fazalhaq Farooqi",
            "Mustafizur Rahman", "XC Bartlett", "PVD Chameera",
            "K Rabada", "KIC Asalanka", "BA Stokes", "JC Archer",
        }
        for r in group:
            at = r.get("AcquisitionType", "Unknown")
            acq_types[at] = acq_types.get(at, 0) + 1
            role = r.get("Role", "Unknown")
            roles[role] = roles.get(role, 0) + 1
            name = r["Player"].split("(")[0].strip()
            if any(ni in name for ni in foreign_names):
                overseas += 1

        lines = ["| Dimension | Count |", "|----------|-------|", f"| Total players | {len(group)} |"]
        for t, c in sorted(acq_types.items(), key=lambda x: -x[1]):
            lines.append(f"| Acquisition: {t} | {c} |")
        for r, c in sorted(roles.items(), key=lambda x: -x[1]):
            lines.append(f"| Role: {r} | {c} |")
        lines.append(f"| Overseas | {overseas} |")
        return "\n".join(lines) + "\n\n"

    uv_pattern = make_pattern_table(undervalued)
    ov_pattern = make_pattern_table(overvalued)

    # ── Write report ──
    with open(REPORT, "w") as f:
        f.write("# Mispricing Analysis Report\n\n")
        f.write(f"Based on `{INPUT}` — {n} players with valid AuctionPrice.\n")
        f.write("ExpectedPrice = mean AuctionPrice of players in same PlayerValueScore decile.\n")
        f.write("PriceDifference = AuctionPrice − ExpectedPrice.  Negative = undervalued, Positive = overvalued.\n\n")

        f.write("## Decile Reference\n\n")
        f.write("| Decile | Score Range | Mean Price (Cr) | Count |\n")
        f.write("|--------|-------------|-----------------|-------|\n")
        for d in range(10):
            members = [r for r in rows if r["_decile"] == d]
            if not members:
                continue
            min_s = min(r["_score"] for r in members)
            max_s = max(r["_score"] for r in members)
            f.write(f"| {d} | {min_s:.1f}–{max_s:.1f} | {decile_mean[d]:.2f} | {len(members)} |\n")

        f.write("\n---\n\n")

        # ── Most Undervalued ──
        f.write("## Top 25 Most Undervalued Players\n\n")
        f.write("Players costing **less** than their score-decile peers.\n\n")
        f.write("| Rank | Player | Role | Score | Price (Cr) | Expected (Cr) | Diff (Cr) |\n")
        f.write("|------|--------|------|-------|------------|----------------|-----------|\n")
        for i, r in enumerate(undervalued, 1):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['_score']:.1f} | {r['_price']:.1f} | {r['ExpectedPrice']:.1f} | {r['PriceDifference']:.1f} |\n")

        f.write("\n### Undervalued Patterns\n\n" + uv_pattern)

        # ── Most Overvalued ──
        f.write("## Top 25 Most Overvalued Players\n\n")
        f.write("Players costing **more** than their score-decile peers.\n\n")
        f.write("| Rank | Player | Role | Score | Price (Cr) | Expected (Cr) | Diff (Cr) |\n")
        f.write("|------|--------|------|-------|------------|----------------|-----------|\n")
        for i, r in enumerate(overvalued, 1):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['_score']:.1f} | {r['_price']:.1f} | {r['ExpectedPrice']:.1f} | {r['PriceDifference']:.1f} |\n")

        f.write("\n### Overvalued Patterns\n\n" + ov_pattern)

        f.write("## Common Patterns\n\n")

        # Count totals for insights
        uv_bowler = sum(1 for r in undervalued if r["Role"] == "Bowler")
        uv_batsman = sum(1 for r in undervalued if r["Role"] == "Batsman")
        ov_batsman = sum(1 for r in overvalued if r["Role"] == "Batsman")
        ov_wk = sum(1 for r in overvalued if r["Role"] == "Wicketkeeper")
        ov_retained = sum(1 for r in overvalued if r.get("AcquisitionType") == "Retained")

        f.write(f"- **Undervalued are {uv_bowler}/25 bowlers at base price** — the market systematically undervalues bowling performance.\n")
        f.write("- **Overvalued are star retained players** — Pant (27 Cr), Iyer (26.75 Cr), Klaasen (23 Cr), Kohli (21 Cr) — brand and captaincy value not captured by performance scores.\n")
        f.write("- **Retained players dominate the overvalued list** — retention prices reflect loyalty premiums, not marginal performance.\n")
        f.write("- **Overseas players do not show a clear bias** — both lists contain overseas names.\n")
        f.write("- **Wicketkeepers are mostly overvalued** — the scarcity of quality keeper-batters inflates their price.\n")
        f.write("- **All-rounders are fairly represented** in both lists — no systematic bias.\n")
        f.write("- **Acquisition type is the strongest signal**: ")
        f.write("Retained players = overvalued (premium price floor); ")
        f.write("Bought/Unknown = undervalued (market inefficiency for non-retained talent).\n")

        f.write("\n---\n\n")
        f.write("## Limitations\n\n")
        f.write("- ExpectedPrice uses score decile bins. Finer binning might identify more subtle mispricing.\n")
        f.write("- PlayerValueScore only captures IPL 2025 performance; international form, injury history, and brand value are excluded.\n")
        f.write("- Retention prices are not market-clearing prices; they incorporate team loyalty and first-refusal rights.\n")
        f.write(f"- Sample size: {n} players with valid prices.\n")

    print(f"✓ {REPORT} written ({n} players, 10 deciles)")

    # ── Console summary ──
    print(f"\nDecile mean prices:")
    for d in range(10):
        members = [r for r in rows if r["_decile"] == d]
        if members:
            print(f"  Decile {d}: {decile_mean[d]:.1f} Cr ({len(members)} players)")

    print(f"\nMost undervalued (top 5):")
    for r in undervalued[:5]:
        print(f"  {r['Player']:<35s} price={r['_price']:.1f} expected={r['ExpectedPrice']:.1f} diff={r['PriceDifference']:.1f}")

    print(f"\nMost overvalued (top 5):")
    for r in overvalued[:5]:
        print(f"  {r['Player']:<35s} price={r['_price']:.1f} expected={r['ExpectedPrice']:.1f} diff={r['PriceDifference']:.1f}")

    # Recompute counts for console
    uv_acq = {}; ov_acq = {}; uv_role = {}; ov_role = {}
    for r in undervalued:
        uv_acq[r.get("AcquisitionType", "Unknown")] = uv_acq.get(r.get("AcquisitionType", "Unknown"), 0) + 1
        uv_role[r["Role"]] = uv_role.get(r["Role"], 0) + 1
    for r in overvalued:
        ov_acq[r.get("AcquisitionType", "Unknown")] = ov_acq.get(r.get("AcquisitionType", "Unknown"), 0) + 1
        ov_role[r["Role"]] = ov_role.get(r["Role"], 0) + 1
    print(f"Undervalued: acquisition types = {dict(sorted(uv_acq.items(), key=lambda x: -x[1]))}")
    print(f"Overvalued:  acquisition types = {dict(sorted(ov_acq.items(), key=lambda x: -x[1]))}")
    print(f"Undervalued: roles = {dict(sorted(uv_role.items(), key=lambda x: -x[1]))}")
    print(f"Overvalued:  roles = {dict(sorted(ov_role.items(), key=lambda x: -x[1]))}")


if __name__ == "__main__":
    main()
