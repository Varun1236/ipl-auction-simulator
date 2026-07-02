"""
team_strategy_engine.py — Compute team-specific player valuations.

Input:  data/master_players.csv, data/player_values.csv
Output: data/team_player_values.csv, team_strategy_report.md

Rules defined in team_strategy_rules.md.
"""
import csv
import statistics

MASTER = "data/master_players.csv"
VALUES = "data/player_values.csv"
OUTPUT = "data/team_player_values.csv"
REPORT = "team_strategy_report.md"


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


def normalise(name):
    return name.strip().lower().replace(".", "").replace("  ", " ")


def fmt(val):
    """Format a value nicely, returning empty string for None."""
    if val is None or val == "":
        return ""
    return f"{val:.1f}"


def main():
    # Read master data
    master_map = {}
    with open(MASTER, newline="") as f:
        for row in csv.DictReader(f):
            master_map[normalise(row["Player"])] = row

    # Read player values
    with open(VALUES, newline="") as f:
        value_rows = list(csv.DictReader(f))

    rows_out = []
    player_details = []

    for vr in value_rows:
        key = normalise(vr["Player"])
        row = {"Player": vr["Player"], "BaseValue": safe_float(vr.get("PlayerValueScore"), "")}

        mr = master_map.get(key)
        if mr is None:
            for team in ["MI", "CSK", "RCB", "RR", "KKR", "GT", "LSG", "PBKS", "DC", "SRH"]:
                row[f"{team}_Value"] = ""
            rows_out.append(row)
            continue

        base = safe_float(vr.get("PlayerValueScore"), 0)
        if base is None or base == 0:
            for team in ["MI", "CSK", "RCB", "RR", "KKR", "GT", "LSG", "PBKS", "DC", "SRH"]:
                row[f"{team}_Value"] = ""
            rows_out.append(row)
            continue

        age = safe_float(mr.get("Age"), 0) or 0
        nationality = mr.get("Nationality", "")
        role = mr.get("Role", "")
        runs = safe_float(mr.get("Runs"), 0) or 0
        wickets = safe_float(mr.get("Wickets"), 0) or 0
        sr = safe_float(mr.get("StrikeRate"), 0) or 0
        economy = safe_float(mr.get("Economy"), 0) or 0

        is_batter = role in ("Batsman", "Wicketkeeper")
        is_allrounder = role == "All-Rounder"
        is_bowler = role == "Bowler"
        is_indian = nationality.strip().lower() == "india"
        is_batter_or_ar = is_batter or is_allrounder

        team_scores = {}
        bonuses = {}

        # CSK
        b = 1.0
        triggers = []
        if age >= 30:
            b += 0.15
            triggers.append("age>=30")
        if is_indian:
            b += 0.10
            triggers.append("Indian")
        team_scores["CSK"] = round(base * b, 2)
        bonuses["CSK"] = (triggers, round(b - 1.0, 2))

        # MI
        b = 1.0
        triggers = []
        if age <= 25:
            b += 0.15
            triggers.append("age<=25")
        if is_batter_or_ar and sr > 145:
            b += 0.10
            triggers.append("SR>145")
        if runs >= 200 and age <= 23:
            b += 0.10
            triggers.append("breakthrough")
        team_scores["MI"] = round(base * b, 2)
        bonuses["MI"] = (triggers, round(b - 1.0, 2))

        # RR
        b = 1.0
        triggers = []
        if age <= 23:
            b += 0.20
            triggers.append("age<=23")
        if runs >= 200 and age <= 23:
            b += 0.10
            triggers.append("young_breakout")
        team_scores["RR"] = round(base * b, 2)
        bonuses["RR"] = (triggers, round(b - 1.0, 2))

        # KKR
        b = 1.0
        triggers = []
        if is_bowler and wickets >= 5 and economy <= 8.5:
            b += 0.15
            triggers.append("spin_proxy")
        team_scores["KKR"] = round(base * b, 2)
        bonuses["KKR"] = (triggers, round(b - 1.0, 2))

        # RCB
        b = 1.0
        triggers = []
        if is_batter_or_ar and sr > 150:
            b += 0.15
            triggers.append("SR>150")
        if runs >= 400:
            b += 0.10
            triggers.append("runs>=400")
        team_scores["RCB"] = round(base * b, 2)
        bonuses["RCB"] = (triggers, round(b - 1.0, 2))

        # GT
        b = 1.0
        triggers = []
        if is_allrounder:
            b += 0.10
            triggers.append("all_rounder")
        if is_allrounder and runs >= 200 and wickets >= 5:
            b += 0.10
            triggers.append("ar_proven")
        team_scores["GT"] = round(base * b, 2)
        bonuses["GT"] = (triggers, round(b - 1.0, 2))

        # LSG
        b = 1.0
        triggers = []
        if role == "Wicketkeeper":
            b += 0.10
            triggers.append("wk")
        if role == "Wicketkeeper" and runs >= 300:
            b += 0.10
            triggers.append("wk_runs>=300")
        team_scores["LSG"] = round(base * b, 2)
        bonuses["LSG"] = (triggers, round(b - 1.0, 2))

        # PBKS
        b = 1.0
        triggers = []
        if is_batter_or_ar and sr > 150:
            b += 0.15
            triggers.append("SR>150")
        if runs >= 300:
            b += 0.10
            triggers.append("runs>=300")
        team_scores["PBKS"] = round(base * b, 2)
        bonuses["PBKS"] = (triggers, round(b - 1.0, 2))

        # DC
        b = 1.0
        triggers = []
        if age <= 28:
            b += 0.10
            triggers.append("age<=28")
        if age <= 25:
            b += 0.10
            triggers.append("age<=25")
        team_scores["DC"] = round(base * b, 2)
        bonuses["DC"] = (triggers, round(b - 1.0, 2))

        # SRH
        b = 1.0
        triggers = []
        if is_batter_or_ar and sr > 150:
            b += 0.15
            triggers.append("SR>150")
        if runs >= 400:
            b += 0.10
            triggers.append("runs>=400")
        team_scores["SRH"] = round(base * b, 2)
        bonuses["SRH"] = (triggers, round(b - 1.0, 2))

        row.update({f"{t}_Value": v for t, v in team_scores.items()})
        rows_out.append(row)

        player_details.append({
            "player": vr["Player"],
            "role": role,
            "age": age,
            "runs": runs,
            "sr": sr,
            "wkts": wickets,
            "econ": economy,
            "nat": nationality,
            "base": base,
            "scores": team_scores,
            "bonuses": bonuses,
        })

    # ── Write CSV output ──
    teams = ["MI", "CSK", "RCB", "RR", "KKR", "GT", "LSG", "PBKS", "DC", "SRH"]
    headers = ["Player", "BaseValue"] + [f"{t}_Value" for t in teams]
    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"✓ {OUTPUT} written ({len(rows_out)} players)")

    # ── Write Report ──
    with open(REPORT, "w") as f:
        f.write("# Team Strategy Report\n\n")
        f.write("Team-specific player valuations based on franchise strategy rules.\n\n")

        # ── Rules Summary ──
        f.write("## Rules Applied\n\n")
        rules_table = """| Team | Trigger | Bonus | Column(s) |
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
"""
        f.write(rules_table)
        f.write("\n---\n\n")

        # ── Example Calculations ──
        f.write("## Example Calculations\n\n")
        examples = [
            "B Sai Sudharsan (GT)",
            "JJ Bumrah (MI)",
            "Abhishek Sharma (SRH)",
            "AD Russell (KKR)",
        ]
        for pname in examples:
            detail = next((d for d in player_details if d["player"].startswith(pname)), None)
            if not detail:
                continue
            f.write(f"### {detail['player']}\n\n")
            f.write(f"- Base PlayerValueScore: **{detail['base']:.1f}**\n")
            f.write(f"- Age: {detail['age']:.0f}, Role: {detail['role']}, Runs: {detail['runs']:.0f}, ")
            f.write(f"SR: {detail['sr']:.1f}, Wkts: {detail['wkts']:.0f}, Econ: {detail['econ']:.1f}\n\n")
            f.write("| Team | Triggers | Bonus | Calculation | Value |\n")
            f.write("|------|----------|-------|-------------|-------|\n")
            for t in teams:
                tr = detail["bonuses"][t][0]
                bp = detail["bonuses"][t][1]
                val = detail["scores"][t]
                trigger_str = ", ".join(tr) if tr else "none"
                calc_str = f"{detail['base']:.1f} × {1+bp:.2f}" if bp > 0 else f"{detail['base']:.1f}"
                f.write(f"| {t} | {trigger_str} | +{bp*100:.0f}% | {calc_str} | **{val:.1f}** |\n")
            f.write("\n")

        f.write("---\n\n")

        # ── Per-team top 20 ──
        f.write("## Top 20 Players per Franchise\n\n")
        for t in teams:
            f.write(f"### {t}\n\n")
            sorted_by_team = sorted(player_details, key=lambda d: -d["scores"][t])
            f.write(f"| Rank | Player | Role | Base | {t} Value | +% | Triggers |\n")
            f.write(f"|------|--------|------|------|----------|-----|----------|\n")
            for i, d in enumerate(sorted_by_team[:20], 1):
                tr = d["bonuses"][t][0]
                bp = d["bonuses"][t][1]
                trigger_str = ", ".join(tr) if tr else "—"
                f.write(f"| {i} | {d['player']} | {d['role']} | {d['base']:.1f} | {d['scores'][t]:.1f} | +{bp*100:.0f}% | {trigger_str} |\n")
            f.write("\n")

        # ── Summary stats ──
        f.write("## Summary Statistics\n\n")
        f.write("| Team | Avg Value | Max Value | Min Value | Players >100 |\n")
        f.write("|------|-----------|-----------|-----------|--------------|\n")
        for t in teams:
            vals = [d["scores"][t] for d in player_details if d["scores"].get(t)]
            if vals:
                avg_v = sum(vals) / len(vals)
                max_v = max(vals)
                min_v = min(vals)
                over100 = sum(1 for v in vals if v > 100)
            else:
                avg_v = max_v = min_v = over100 = 0
            f.write(f"| {t} | {avg_v:.1f} | {max_v:.1f} | {min_v:.1f} | {over100} |\n")

        f.write("\n")
        f.write("_Generated by team_strategy_engine.py — rules from team_strategy_rules.md_\n")

    print(f"✓ {REPORT} written")

    # ── Console summary ──
    print(f"\n{'Team':<6s} {'Avg Value':>10s} {'Max Value':>10s} {'Min Value':>10s} {'Players >100':>12s}")
    print("-" * 52)
    for t in teams:
        vals = [d["scores"][t] for d in player_details if d["scores"].get(t)]
        if vals:
            avg_v = sum(vals) / len(vals)
            max_v = max(vals)
            min_v = min(vals)
            over100 = sum(1 for v in vals if v > 100)
        else:
            avg_v = max_v = min_v = over100 = 0
        print(f"{t:<6s} {avg_v:>8.1f}    {max_v:>6.1f}    {min_v:>6.1f}    {over100:>5d}")

    boosts = []
    for d in player_details:
        bv = d["base"]
        for t in teams:
            tv = d["scores"].get(t, 0)
            if tv > bv:
                boosts.append((t, d["player"], tv - bv, tv, bv))
    boosts.sort(key=lambda x: -x[2])
    print(f"\nBiggest boosts (top 15):")
    for t, p, diff, tv, bv in boosts[:15]:
        print(f"  {t:5s} {p:<35s} base={bv:>5.1f} → {tv:>6.1f} (+{diff:.1f})")


if __name__ == "__main__":
    main()
