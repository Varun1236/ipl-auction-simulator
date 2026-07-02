"""
insights_report.py — Generate strategic insights from value-per-crore analysis.

Inputs: data/value_analysis.csv, data/master_players.csv
Output: insights_report.md
"""
import csv
import os
import statistics

ANALYSIS = "data/value_analysis.csv"
MASTER = "data/master_players.csv"
REPORT = "insights_report.md"


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


def fmt_pct(val):
    return f"{val:.1f}%" if val else "N/A"


def main():
    analysis_rows = read_csv(ANALYSIS)
    master_rows = read_csv(MASTER)

    # Index master by Player for Team
    team_map = {}
    for mr in master_rows:
        team_map[normalise(mr["Player"])] = mr.get("Team", "")

    # Merge team into analysis rows
    for r in analysis_rows:
        key = normalise(r["Player"])
        r["Team"] = team_map.get(key, "")

    # Filter players with valid ValuePerCrore
    players = [r for r in analysis_rows if r["ValuePerCrore"] != ""]
    for r in players:
        r["VPC"] = float(r["ValuePerCrore"])
        r["Score"] = float(r["PlayerValueScore"])
    total = len(players)
    excluded = [r for r in analysis_rows if r["ValuePerCrore"] == ""]

    # Sort by VPC descending
    players.sort(key=lambda r: -r["VPC"])

    top20 = players[:20]
    bottom20 = players[-20:]
    bottom20.reverse()

    # ── Avg VPC by role ──
    by_role = {}
    for r in players:
        by_role.setdefault(r["Role"], []).append(r["VPC"])

    # ── Avg VPC by team ──
    by_team = {}
    for r in players:
        by_team.setdefault(r["Team"], []).append(r["VPC"])

    # ── Avg VPC by acquisition type ──
    by_acq = {}
    for r in players:
        by_acq.setdefault(r["AcquisitionType"], []).append(r["VPC"])

    # ── Best / worst retention ──
    retained = [r for r in players if r["AcquisitionType"] == "Retained"]
    retained.sort(key=lambda r: -r["VPC"])
    best_retention = retained[:5] if len(retained) >= 5 else retained
    worst_retention = retained[-5:] if len(retained) >= 5 else retained
    worst_retention.reverse()

    # ── Best / worst auction purchase ──
    bought = [r for r in players if r["AcquisitionType"] == "Bought"]
    bought.sort(key=lambda r: -r["VPC"])
    best_bought = bought[:5] if len(bought) >= 5 else bought
    worst_bought = bought[-5:] if len(bought) >= 5 else bought
    worst_bought.reverse()

    # ── Write report ──
    with open(REPORT, "w") as f:
        f.write("# IPL 2026 Auction Insights Report\n\n")
        f.write(f"Generated from `{ANALYSIS}` — {len(analysis_rows)} players, {total} with ValuePerCrore\n\n")

        # ── Top 20 undervalued ──
        f.write("## 20 Most Undervalued Players (Highest ValuePerCrore)\n\n")
        f.write("These players delivered the most performance value per crore spent.\n\n")
        f.write("| Rank | Player | Role | Team | Score | Price (Cr) | VPC |\n")
        f.write("|------|--------|------|------|-------|------------|-----|\n")
        for i, r in enumerate(top20, 1):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['Team']} | {r['PlayerValueScore']} | {r['AuctionPrice']} | {r['ValuePerCrore']} |\n")
        f.write("\n")
        f.write("> **Insight:** Most undervalued players are bowlers bought at base price (0.3 Cr). ")
        f.write("Bowling performance at minimum cost offers the highest ROI.\n\n")

        # ── Bottom 20 overvalued ──
        f.write("## 20 Most Overvalued Players (Lowest ValuePerCrore)\n\n")
        f.write("These players cost the most relative to their performance score.\n\n")
        f.write("| Rank | Player | Role | Team | Score | Price (Cr) | VPC |\n")
        f.write("|------|--------|------|------|-------|------------|-----|\n")
        for i, r in enumerate(bottom20, 1):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['Team']} | {r['PlayerValueScore']} | {r['AuctionPrice']} | {r['ValuePerCrore']} |\n")
        f.write("\n")
        f.write("> **Insight:** Overvalued players are typically high-priced retained stars (Pant 27 Cr, Iyer 26.75 Cr) ")
        f.write("whose performance score doesn't scale linearly with their salary.\n\n")

        # ── Avg VPC by role ──
        f.write("## Average ValuePerCrore by Role\n\n")
        f.write("| Role | Players | Avg VPC | Min VPC | Max VPC |\n")
        f.write("|------|---------|---------|---------|---------|\n")
        for role in ["Batsman", "Bowler", "All-Rounder", "Wicketkeeper"]:
            vals = by_role.get(role, [])
            if vals:
                avg = statistics.mean(vals)
                mn = min(vals)
                mx = max(vals)
                f.write(f"| {role} | {len(vals)} | {avg:.2f} | {mn:.2f} | {mx:.2f} |\n")
        f.write("\n")
        f.write("> **Insight:** Bowlers have the highest avg VPC (low salaries, impactful stats). ")
        f.write("Wicketkeepers have the lowest because top keepers command premium retention prices.\n\n")

        # ── Avg VPC by team ──
        f.write("## Average ValuePerCrore by Team\n\n")
        f.write("| Team | Players | Avg VPC | Best VPC Player |\n")
        f.write("|------|---------|---------|-----------------|\n")
        for team in sorted(by_team.keys()):
            vals = by_team[team]
            avg = statistics.mean(vals)
            # Best VPC player on this team
            team_players = [r for r in players if r["Team"] == team]
            team_players.sort(key=lambda r: -r["VPC"])
            best = team_players[0]["Player"] if team_players else ""
            f.write(f"| {team} | {len(vals)} | {avg:.2f} | {best} |\n")
        f.write("\n")

        # ── Avg VPC by acquisition type ──
        f.write("## Average ValuePerCrore by Acquisition Type\n\n")
        f.write("| Type | Players | Avg VPC | Min VPC | Max VPC |\n")
        f.write("|------|---------|---------|---------|---------|\n")
        for acq in sorted(by_acq.keys()):
            vals = by_acq[acq]
            avg = statistics.mean(vals)
            mn = min(vals)
            mx = max(vals)
            f.write(f"| {acq} | {len(vals)} | {avg:.2f} | {mn:.2f} | {mx:.2f} |\n")
        f.write("\n")
        f.write("> **Insight:** Auction purchases deliver higher avg VPC than retentions. ")
        f.write("Teams overpay for retained stars due to emotional / brand value.\n\n")

        # ── Best / worst retention ──
        f.write("## Best Retention Decisions (by ValuePerCrore)\n\n")
        f.write("| Rank | Player | Role | Team | Score | Price (Cr) | VPC |\n")
        f.write("|------|--------|------|------|-------|------------|-----|\n")
        for i, r in enumerate(best_retention, 1):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['Team']} | {r['PlayerValueScore']} | {r['AuctionPrice']} | {r['ValuePerCrore']} |\n")
        f.write("\n")

        f.write("## Worst Retention Decisions (by ValuePerCrore)\n\n")
        f.write("| Rank | Player | Role | Team | Score | Price (Cr) | VPC |\n")
        f.write("|------|--------|------|------|-------|------------|-----|\n")
        for i, r in enumerate(worst_retention, 1):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['Team']} | {r['PlayerValueScore']} | {r['AuctionPrice']} | {r['ValuePerCrore']} |\n")
        f.write("\n")

        # ── Best / worst auction purchase ──
        f.write("## Best Auction Purchases (by ValuePerCrore)\n\n")
        f.write("| Rank | Player | Role | Team | Score | Price (Cr) | VPC |\n")
        f.write("|------|--------|------|------|-------|------------|-----|\n")
        for i, r in enumerate(best_bought, 1):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['Team']} | {r['PlayerValueScore']} | {r['AuctionPrice']} | {r['ValuePerCrore']} |\n")
        f.write("\n")
        f.write("> **Insight:** Best auction buys are low-cost (0.3-1 Cr) bowlers and utility players. ")
        f.write("The auction format rewards finding hidden gems at base price.\n\n")

        f.write("## Worst Auction Purchases (by ValuePerCrore)\n\n")
        f.write("| Rank | Player | Role | Team | Score | Price (Cr) | VPC |\n")
        f.write("|------|--------|------|------|-------|------------|-----|\n")
        for i, r in enumerate(worst_bought, 1):
            f.write(f"| {i} | {r['Player']} | {r['Role']} | {r['Team']} | {r['PlayerValueScore']} | {r['AuctionPrice']} | {r['ValuePerCrore']} |\n")
        f.write("\n")
        f.write("> **Insight:** The worst auction buys are mid-to-high priced players whose scores ")
        f.write("didn't justify the expense. Livingstone (13 Cr), Pathirana (18 Cr), Inglis (8.6 Cr) are examples.\n\n")

        # ── Excluded players ──
        f.write("## Players Excluded from VPC Calculation\n\n")
        f.write(f"{len(excluded)} players had no valid AuctionPrice and were excluded:\n\n")
        f.write("| Player | Role | Team | AcquisitionType |\n")
        f.write("|--------|------|------|----------------|\n")
        for r in sorted(excluded, key=lambda x: x["Player"].lower()):
            key = normalise(r["Player"])
            team = team_map.get(key, "")
            f.write(f"| {r['Player']} | {r['Role']} | {team} | {r['AcquisitionType']} |\n")

    print(f"✓ {REPORT} written")
    print(f"  {total} players with VPC, {len(excluded)} excluded")
    print(f"  Roles: {', '.join(f'{k}={len(v)}' for k,v in sorted(by_role.items()))}")
    print(f"  Teams: {', '.join(sorted(by_team.keys()))}")
    print(f"  Best retention: {best_retention[0]['Player']} ({best_retention[0]['VPC']:.2f})")
    print(f"  Worst retention: {worst_retention[0]['Player']} ({worst_retention[0]['VPC']:.2f})")
    print(f"  Best auction buy: {best_bought[0]['Player']} ({best_bought[0]['VPC']:.2f})")
    print(f"  Worst auction buy: {worst_bought[0]['Player']} ({worst_bought[0]['VPC']:.2f})")


if __name__ == "__main__":
    main()
