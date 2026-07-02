"""
value_price_analysis.py — Merge player values with auction prices, compute ValuePerCrore.

Inputs: data/master_players.csv, data/player_values.csv
Output: data/value_analysis.csv, value_analysis_report.md
"""
import csv
import os
import statistics

MASTER = "data/master_players.csv"
VALUES = "data/player_values.csv"
ANALYSIS_OUT = "data/value_analysis.csv"
REPORT = "value_analysis_report.md"


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


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def normalise(name):
    return name.strip().lower().replace(".", "").replace("  ", " ")


def main():
    master_rows = read_csv(MASTER)
    values_rows = read_csv(VALUES)

    # Index values by normalised Player name
    values_by_player = {}
    for r in values_rows:
        key = normalise(r["Player"])
        values_by_player[key] = r

    results = []
    excluded_na = 0
    excluded_no_price = 0

    for mr in master_rows:
        key = normalise(mr["Player"])
        vr = values_by_player.get(key)
        if vr is None:
            continue

        player = mr["Player"]
        role = mr.get("Role", "")
        score_raw = safe_float(vr.get("PlayerValueScore"), 0.0)
        price_raw = vr.get("AuctionPrice", "N/A")
        acq_type = vr.get("AcquisitionType", "N/A")

        price = safe_float(price_raw)

        if price is None or price_raw in ("N/A", "0.0"):
            vpc = ""
            if price_raw == "N/A":
                excluded_na += 1
            else:
                excluded_no_price += 1
        elif price > 0:
            vpc = round(score_raw / price, 2)
        else:
            vpc = ""
            excluded_no_price += 1

        results.append({
            "Player": player,
            "Role": role,
            "PlayerValueScore": score_raw,
            "AuctionPrice": price_raw,
            "AcquisitionType": acq_type,
            "ValuePerCrore": vpc,
        })

    # ── Write value_analysis.csv ──
    fields = ["Player", "Role", "PlayerValueScore", "AuctionPrice", "AcquisitionType", "ValuePerCrore"]
    os.makedirs(os.path.dirname(ANALYSIS_OUT), exist_ok=True)
    with open(ANALYSIS_OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    # ── Rankings ──
    with_vpc = [r for r in results if r["ValuePerCrore"] != ""]
    without_vpc = [r for r in results if r["ValuePerCrore"] == ""]
    with_vpc.sort(key=lambda r: -r["ValuePerCrore"])

    top20 = with_vpc[:20]
    bottom20 = with_vpc[-20:]
    bottom20.reverse()

    # ── Stats by role ──
    by_role = {}
    for r in with_vpc:
        by_role.setdefault(r["Role"], []).append(r["ValuePerCrore"])

    by_acq = {}
    for r in with_vpc:
        by_acq.setdefault(r["AcquisitionType"], []).append(r["ValuePerCrore"])

    # ── Print summary ──
    total = len(results)
    with_vpc_count = len(with_vpc)

    print(f"Total players: {total}")
    print(f"Players with ValuePerCrore: {with_vpc_count}")
    print(f"Players excluded (price N/A): {excluded_na}")
    print(f"Players excluded (price 0): {excluded_no_price}")
    print()

    print("Top 20 ValuePerCrore:\n")
    print(f"{'Rank':<5} {'Player':<35} {'Role':<15} {'Score':<8} {'Price':<8} {'VPC':<10}")
    print("-" * 85)
    for i, r in enumerate(top20, 1):
        print(f"{i:<5} {r['Player']:<35} {r['Role']:<15} {r['PlayerValueScore']:<8.1f} {r['AuctionPrice']:<8} {r['ValuePerCrore']:<10.2f}")

    print("\nBottom 20 ValuePerCrore:\n")
    print(f"{'Rank':<5} {'Player':<35} {'Role':<15} {'Score':<8} {'Price':<8} {'VPC':<10}")
    print("-" * 85)
    total_ranked = len(with_vpc)
    for i, r in enumerate(bottom20, total_ranked - 19):
        print(f"{i:<5} {r['Player']:<35} {r['Role']:<15} {r['PlayerValueScore']:<8.1f} {r['AuctionPrice']:<8} {r['ValuePerCrore']:<10.2f}")

    print("\nAvg ValuePerCrore by role:\n")
    for role in sorted(by_role.keys()):
        vals = by_role[role]
        avg = statistics.mean(vals)
        print(f"  {role:<15s} {avg:.2f} (n={len(vals)})")

    print("\nAvg ValuePerCrore by acquisition type:\n")
    for acq in sorted(by_acq.keys()):
        vals = by_acq[acq]
        avg = statistics.mean(vals)
        print(f"  {acq:<15s} {avg:.2f} (n={len(vals)})")

    # Most undervalued (lowest VPC) and overvalued (highest VPC)
    most_undervalued = with_vpc[:5]  # highest VPC = best value per crore
    most_overvalued = with_vpc[-5:]  # lowest VPC = worst value per crore
    most_overvalued.reverse()

    print(f"\nMost undervalued players (highest ValuePerCrore):")
    for r in most_undervalued:
        print(f"  {r['Player']:<35s} Score={r['PlayerValueScore']:.1f} Price={r['AuctionPrice']:<6s} VPC={r['ValuePerCrore']:.2f}")

    print(f"\nMost overvalued players (lowest ValuePerCrore):")
    for r in most_overvalued:
        print(f"  {r['Player']:<35s} Score={r['PlayerValueScore']:.1f} Price={r['AuctionPrice']:<6s} VPC={r['ValuePerCrore']:.2f}")

    # ── Write report ──
    with open(REPORT, "w") as f:
        f.write("# Value-Per-Crore Analysis — IPL 2025 Season\n\n")
        f.write(f"Generated from `{MASTER}` and `{VALUES}`\n\n")
        f.write("## Methodology\n\n")
        f.write("ValuePerCrore = PlayerValueScore / AuctionPrice\n\n")
        f.write("A higher ValuePerCrore means the team got more performance value per unit of currency spent. ")
        f.write("Players with AuctionPrice = N/A or 0 are excluded from the calculation.\n\n")

        f.write("## Summary\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Total players | {total} |\n")
        f.write(f"| Players with ValuePerCrore | {with_vpc_count} |\n")
        f.write(f"| Players excluded (N/A price) | {excluded_na} |\n")
        f.write(f"| Players excluded (0 price) | {excluded_no_price} |\n\n")

        if with_vpc:
            all_vpc = [r["ValuePerCrore"] for r in with_vpc]
            f.write(f"| Mean ValuePerCrore | {statistics.mean(all_vpc):.2f} |\n")
            f.write(f"| Median ValuePerCrore | {statistics.median(all_vpc):.2f} |\n")
            f.write(f"| Min ValuePerCrore | {min(all_vpc):.2f} |\n")
            f.write(f"| Max ValuePerCrore | {max(all_vpc):.2f} |\n\n")

        f.write("## Average ValuePerCrore by Role\n\n")
        f.write("| Role | Count | Avg VPC |\n")
        f.write("|------|-------|--------|\n")
        for role in sorted(by_role.keys()):
            vals = by_role[role]
            avg = statistics.mean(vals)
            f.write(f"| {role} | {len(vals)} | {avg:.2f} |\n")
        f.write("\n")

        f.write("## Average ValuePerCrore by Acquisition Type\n\n")
        f.write("| Type | Count | Avg VPC |\n")
        f.write("|------|-------|--------|\n")
        for acq in sorted(by_acq.keys()):
            vals = by_acq[acq]
            avg = statistics.mean(vals)
            f.write(f"| {acq} | {len(vals)} | {avg:.2f} |\n")
        f.write("\n")

        f.write("## Most Undervalued Players (Highest ValuePerCrore)\n\n")
        f.write("These players delivered high performance relative to their low price.\n\n")
        f.write("| Rank | Player | Role | Score | Price (Cr) | VPC |\n")
        f.write("|------|--------|------|-------|------------|-----|\n")
        for i, r in enumerate(most_undervalued, 1):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['PlayerValueScore']:.1f} | {r['AuctionPrice']} | {r['ValuePerCrore']:.2f} |\n")
        f.write("\n")

        f.write("## Most Overvalued Players (Lowest ValuePerCrore)\n\n")
        f.write("These players had high prices relative to their performance score.\n\n")
        f.write("| Rank | Player | Role | Score | Price (Cr) | VPC |\n")
        f.write("|------|--------|------|-------|------------|-----|\n")
        for i, r in enumerate(most_overvalued, 1):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['PlayerValueScore']:.1f} | {r['AuctionPrice']} | {r['ValuePerCrore']:.2f} |\n")
        f.write("\n")

        f.write("## Top 20 Highest ValuePerCrore\n\n")
        f.write("| Rank | Player | Role | Score | Price (Cr) | VPC |\n")
        f.write("|------|--------|------|-------|------------|-----|\n")
        for i, r in enumerate(top20, 1):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['PlayerValueScore']:.1f} | {r['AuctionPrice']} | {r['ValuePerCrore']:.2f} |\n")
        f.write("\n")

        f.write("## Bottom 20 Lowest ValuePerCrore\n\n")
        f.write("| Rank | Player | Role | Score | Price (Cr) | VPC |\n")
        f.write("|------|--------|------|-------|------------|-----|\n")
        for i, r in enumerate(bottom20, total_ranked - 19):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['PlayerValueScore']:.1f} | {r['AuctionPrice']} | {r['ValuePerCrore']:.2f} |\n")

    print(f"\n✓ {ANALYSIS_OUT} written")
    print(f"✓ {REPORT} written")


if __name__ == "__main__":
    main()
