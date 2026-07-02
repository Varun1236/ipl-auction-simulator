import csv
import os

BATTING_FILE = "data/batting_2025.csv"
BOWLING_FILE = "data/bowling_2025.csv"
OUTPUT_FILE = "data/master_players.csv"

OUT_COLS = [
    "Player", "Team", "Age", "Nationality", "Runs",
    "BattingAverage", "StrikeRate", "100s", "50s",
    "Wickets", "BowlingAverage", "Economy", "Role",
]

KNOWN_WICKETKEEPERS = {
    "MS Dhoni (CSK)", "Ishan Kishan (SRH)", "KL Rahul (DC)",
    "RR Pant (LSG)", "SV Samson (RR)", "JC Buttler (GT)",
    "N Pooran (LSG)", "PD Salt (RCB)", "Q de Kock (KKR)",
    "DC Jurel (RR)", "JM Sharma (RCB)", "JP Inglis (PBKS)",
    "RD Rickelton (MI)", "Abishek Porel (DC)", "H Klaasen (SRH)",
    "Rahmanullah Gurbaz (KKR)", "JM Bairstow (MI)",
    "DP Conway (CSK)", "DA Miller (LSG)",
}


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def safe_int(val, default=0):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def determine_role(bat, bowl, player_name):
    if player_name in KNOWN_WICKETKEEPERS:
        return "Wicketkeeper"

    runs = safe_int(bat.get("Runs", 0)) if bat else 0
    wickets = safe_int(bowl.get("Wkts", 0)) if bowl else 0

    has_bat = bat is not None
    has_bowl = bowl is not None

    if has_bat and has_bowl:
        if runs >= 200 and wickets >= 10:
            return "All-Rounder"
        elif wickets >= 10 and runs < 200:
            return "Bowler"
        elif runs >= 200 and wickets < 5:
            return "Batsman"
        else:
            return "All-Rounder"
    elif has_bat:
        return "Batsman"
    elif has_bowl:
        return "Bowler"

    return "Batsman"


def main():
    batting_data = read_csv(BATTING_FILE)
    bowling_data = read_csv(BOWLING_FILE)

    batting_map = {}
    for row in batting_data:
        key = row.get("Player", "").strip().lower()
        batting_map[key] = row

    bowling_map = {}
    for row in bowling_data:
        key = row.get("Player", "").strip().lower()
        bowling_map[key] = row

    all_keys = set(batting_map.keys()) | set(bowling_map.keys())
    merged = []

    for key in all_keys:
        bat = batting_map.get(key)
        bowl = bowling_map.get(key)
        src = bat or bowl

        row = {
            "Player": src["Player"],
            "Team": src.get("Team", ""),
            "Age": src.get("Age", ""),
            "Nationality": src.get("Nationality", ""),
            "Runs": bat.get("Runs", "0") if bat else "0",
            "BattingAverage": bat.get("Batting Average", "0") if bat else "0",
            "StrikeRate": bat.get("SR", "0") if bat else "0",
            "100s": bat.get("100", "0") if bat else "0",
            "50s": bat.get("50", "0") if bat else "0",
            "Wickets": bowl.get("Wkts", "0") if bowl else "0",
            "BowlingAverage": bowl.get("Ave", "0") if bowl else "0",
            "Economy": bowl.get("Econ", "0") if bowl else "0",
        }
        row["Role"] = determine_role(bat, bowl, row["Player"])
        merged.append(row)

    merged.sort(key=lambda r: r["Player"])

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUT_COLS)
        writer.writeheader()
        writer.writerows(merged)

    counts = {"Batsman": 0, "Bowler": 0, "All-Rounder": 0, "Wicketkeeper": 0}
    for row in merged:
        role = row["Role"]
        if role in counts:
            counts[role] += 1

    print(f"Total players: {len(merged)}")
    print(f"Batsmen: {counts['Batsman']}")
    print(f"Bowlers: {counts['Bowler']}")
    print(f"All-Rounders: {counts['All-Rounder']}")
    print(f"Wicketkeepers: {counts['Wicketkeeper']}")


if __name__ == "__main__":
    main()
