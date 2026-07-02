"""
Full pipeline:
  STEP 1 → data/auction_prices.csv  (Player, AuctionPrice, AcquisitionType)
  STEP 2 → Merge into data/master_players.csv
  STEP 3 → Validation & report → auction_price_report.md
"""
import csv
import os

MASTER = "data/master_players.csv"
PRICES_OUT = "data/auction_prices.csv"

# ── IPL 2026 acquisition data from ESPN Cricinfo ──────────────────────
# (team, full_name, price_crores, acquisition_type)
# acquisition_type: "Retained" or "Bought"
SQUADS = [
    # ── Chennai Super Kings ──
    ("CSK", "Ruturaj Gaikwad", 18.0, "Retained"),
    ("CSK", "Sanju Samson", 18.0, "Retained"),
    ("CSK", "Kartik Sharma", 14.2, "Bought"),
    ("CSK", "Prashant Veer", 14.2, "Bought"),
    ("CSK", "Shivam Dube", 12.0, "Retained"),
    ("CSK", "Noor Ahmad", 10.0, "Retained"),
    ("CSK", "Rahul Chahar", 5.2, "Bought"),
    ("CSK", "Khaleel Ahmed", 4.8, "Retained"),
    ("CSK", "MS Dhoni", 4.0, "Retained"),
    ("CSK", "Anshul Kamboj", 3.4, "Retained"),
    ("CSK", "Gurjapneet Singh", 2.2, "Retained"),
    ("CSK", "Dewald Brevis", 2.2, "Retained"),
    ("CSK", "Nathan Ellis", 2.0, "Retained"),
    ("CSK", "Akeal Hosein", 2.0, "Bought"),
    ("CSK", "Matt Henry", 2.0, "Bought"),
    ("CSK", "Matthew Short", 1.5, "Bought"),
    ("CSK", "Jamie Overton", 1.5, "Retained"),
    ("CSK", "Zak Foulkes", 0.75, "Bought"),
    ("CSK", "Sarfaraz Khan", 0.75, "Bought"),
    ("CSK", "Aman Khan", 0.4, "Bought"),
    ("CSK", "Ayush Mhatre", 0.3, "Retained"),
    ("CSK", "Ramakrishna Ghosh", 0.3, "Retained"),
    ("CSK", "Urvil Patel", 0.3, "Retained"),
    ("CSK", "Mukesh Choudhary", 0.3, "Retained"),
    ("CSK", "Shreyas Gopal", 0.3, "Retained"),

    # ── Delhi Capitals ──
    ("DC", "Axar Patel", 16.5, "Retained"),
    ("DC", "KL Rahul", 14.0, "Retained"),
    ("DC", "Kuldeep Yadav", 13.25, "Retained"),
    ("DC", "Mitchell Starc", 11.75, "Retained"),
    ("DC", "T Natarajan", 10.75, "Retained"),
    ("DC", "Tristan Stubbs", 10.0, "Retained"),
    ("DC", "Auqib Nabi", 8.4, "Bought"),
    ("DC", "Mukesh Kumar", 8.0, "Retained"),
    ("DC", "Nitish Rana", 4.2, "Retained"),
    ("DC", "Abishek Porel", 4.0, "Retained"),
    ("DC", "Pathum Nissanka", 4.0, "Bought"),
    ("DC", "Ashutosh Sharma", 3.8, "Retained"),
    ("DC", "Kyle Jamieson", 2.0, "Bought"),
    ("DC", "Lungi Ngidi", 2.0, "Bought"),
    ("DC", "Ben Duckett", 2.0, "Bought"),
    ("DC", "David Miller", 2.0, "Bought"),
    ("DC", "Sameer Rizvi", 0.95, "Retained"),
    ("DC", "Prithvi Shaw", 0.75, "Bought"),
    ("DC", "Dushmantha Chameera", 0.75, "Retained"),
    ("DC", "Vipraj Nigam", 0.5, "Retained"),
    ("DC", "Karun Nair", 0.5, "Retained"),
    ("DC", "Madhav Tiwari", 0.4, "Retained"),
    ("DC", "Sahil Parakh", 0.3, "Bought"),
    ("DC", "Tripurana Vijay", 0.3, "Retained"),
    ("DC", "Ajay Mandal", 0.3, "Retained"),

    # ── Gujarat Titans ──
    ("GT", "Rashid Khan", 18.0, "Retained"),
    ("GT", "Shubman Gill", 16.5, "Retained"),
    ("GT", "Jos Buttler", 15.75, "Retained"),
    ("GT", "Mohammed Siraj", 12.25, "Retained"),
    ("GT", "Kagiso Rabada", 10.75, "Retained"),
    ("GT", "Prasidh Krishna", 9.5, "Retained"),
    ("GT", "Sai Sudharsan", 8.5, "Retained"),
    ("GT", "Jason Holder", 7.0, "Bought"),
    ("GT", "M Shahrukh Khan", 4.0, "Retained"),
    ("GT", "Rahul Tewatia", 4.0, "Retained"),
    ("GT", "Washington Sundar", 3.2, "Retained"),
    ("GT", "Sai Kishore", 2.0, "Retained"),
    ("GT", "Tom Banton", 2.0, "Bought"),
    ("GT", "Glenn Phillips", 2.0, "Retained"),
    ("GT", "Gurnoor Brar", 1.3, "Retained"),
    ("GT", "Arshad Khan", 1.3, "Retained"),
    ("GT", "Ashok Sharma", 0.9, "Bought"),
    ("GT", "Luke Wood", 0.75, "Bought"),
    ("GT", "Jayant Yadav", 0.75, "Retained"),
    ("GT", "Ishant Sharma", 0.75, "Retained"),
    ("GT", "Kumar Kushagra", 0.65, "Retained"),
    ("GT", "Nishant Sindhu", 0.3, "Retained"),
    ("GT", "Manav Suthar", 0.3, "Retained"),
    ("GT", "Anuj Rawat", 0.3, "Retained"),
    ("GT", "Prithvi Raj", 0.3, "Bought"),

    # ── Kolkata Knight Riders ──
    ("KKR", "Cameron Green", 25.2, "Bought"),
    ("KKR", "Matheesha Pathirana", 18.0, "Bought"),
    ("KKR", "Rinku Singh", 13.0, "Retained"),
    ("KKR", "Varun Chakravarthy", 12.0, "Retained"),
    ("KKR", "Sunil Narine", 12.0, "Retained"),
    ("KKR", "Mustafizur Rahman", 9.2, "Bought"),
    ("KKR", "Harshit Rana", 4.0, "Retained"),
    ("KKR", "Ramandeep Singh", 4.0, "Retained"),
    ("KKR", "Tejasvi Dahiya", 3.0, "Bought"),
    ("KKR", "Angkrish Raghuvanshi", 3.0, "Retained"),
    ("KKR", "Rachin Ravindra", 2.0, "Bought"),
    ("KKR", "Finn Allen", 2.0, "Bought"),
    ("KKR", "Vaibhav Arora", 1.8, "Retained"),
    ("KKR", "Rovman Powell", 1.5, "Retained"),
    ("KKR", "Tim Seifert", 1.5, "Bought"),
    ("KKR", "Ajinkya Rahane", 1.5, "Retained"),
    ("KKR", "Akash Deep", 1.0, "Bought"),
    ("KKR", "Umran Malik", 0.75, "Retained"),
    ("KKR", "Rahul Tripathi", 0.75, "Bought"),
    ("KKR", "Manish Pandey", 0.75, "Retained"),
    ("KKR", "Anukul Roy", 0.4, "Retained"),
    ("KKR", "Daksh Kamra", 0.3, "Bought"),
    ("KKR", "Prashant Solanki", 0.3, "Bought"),
    ("KKR", "Kartik Tyagi", 0.3, "Bought"),
    ("KKR", "Sarthak Ranjan", 0.3, "Bought"),

    # ── Lucknow Super Giants ──
    ("LSG", "Rishabh Pant", 27.0, "Retained"),
    ("LSG", "Nicholas Pooran", 21.0, "Retained"),
    ("LSG", "Mayank Yadav", 11.0, "Retained"),
    ("LSG", "Mohammed Shami", 10.0, "Retained"),
    ("LSG", "Avesh Khan", 9.75, "Retained"),
    ("LSG", "Josh Inglis", 8.6, "Bought"),
    ("LSG", "Abdul Samad", 4.2, "Retained"),
    ("LSG", "Ayush Badoni", 4.0, "Retained"),
    ("LSG", "Mohsin Khan", 4.0, "Retained"),
    ("LSG", "Mitchell Marsh", 3.4, "Retained"),
    ("LSG", "Mukul Choudhary", 2.6, "Bought"),
    ("LSG", "Shahbaz Ahmed", 2.4, "Retained"),
    ("LSG", "Akshat Raghuwanshi", 2.2, "Bought"),
    ("LSG", "Wanindu Hasaranga", 2.0, "Bought"),
    ("LSG", "Aiden Markram", 2.0, "Retained"),
    ("LSG", "Anrich Nortje", 2.0, "Bought"),
    ("LSG", "Naman Tiwari", 1.0, "Bought"),
    ("LSG", "Manimaran Siddharth", 0.75, "Retained"),
    ("LSG", "Matthew Breetzke", 0.75, "Retained"),
    ("LSG", "Digvesh Rathi", 0.3, "Retained"),
    ("LSG", "Arshin Kulkarni", 0.3, "Retained"),
    ("LSG", "Prince Yadav", 0.3, "Retained"),
    ("LSG", "Akash Singh", 0.3, "Retained"),
    ("LSG", "Arjun Tendulkar", 0.3, "Retained"),
    ("LSG", "Himmat Singh", 0.3, "Retained"),

    # ── Mumbai Indians ──
    ("MI", "Jasprit Bumrah", 18.0, "Retained"),
    ("MI", "Hardik Pandya", 16.35, "Retained"),
    ("MI", "Suryakumar Yadav", 16.35, "Retained"),
    ("MI", "Rohit Sharma", 16.3, "Retained"),
    ("MI", "Trent Boult", 12.5, "Retained"),
    ("MI", "Deepak Chahar", 9.25, "Retained"),
    ("MI", "Tilak Varma", 8.0, "Retained"),
    ("MI", "Naman Dhir", 5.25, "Retained"),
    ("MI", "Will Jacks", 5.25, "Retained"),
    ("MI", "AM Ghazanfar", 4.8, "Retained"),
    ("MI", "Sherfane Rutherford", 2.6, "Retained"),
    ("MI", "Mitchell Santner", 2.0, "Retained"),
    ("MI", "Shardul Thakur", 2.0, "Retained"),
    ("MI", "Ryan Rickelton", 1.0, "Retained"),
    ("MI", "Quinton de Kock", 1.0, "Bought"),
    ("MI", "Corbin Bosch", 0.75, "Retained"),
    ("MI", "Robin Minz", 0.65, "Retained"),
    ("MI", "Mohd Izhar", 0.3, "Bought"),
    ("MI", "Danish Malewar", 0.3, "Bought"),
    ("MI", "Raj Bawa", 0.3, "Retained"),
    ("MI", "Ashwani Kumar", 0.3, "Retained"),
    ("MI", "Atharva Ankolekar", 0.3, "Bought"),
    ("MI", "Raghu Sharma", 0.3, "Retained"),
    ("MI", "Mayank Markande", 0.3, "Retained"),
    ("MI", "Mayank Rawat", 0.3, "Bought"),

    # ── Punjab Kings ──
    ("PBKS", "Shreyas Iyer", 26.75, "Retained"),
    ("PBKS", "Arshdeep Singh", 18.0, "Retained"),
    ("PBKS", "Yuzvendra Chahal", 18.0, "Retained"),
    ("PBKS", "Marcus Stoinis", 11.0, "Retained"),
    ("PBKS", "Marco Jansen", 7.0, "Retained"),
    ("PBKS", "Shashank Singh", 5.5, "Retained"),
    ("PBKS", "Ben Dwarshuis", 4.4, "Bought"),
    ("PBKS", "Nehal Wadhera", 4.2, "Retained"),
    ("PBKS", "Prabhsimran Singh", 4.0, "Retained"),
    ("PBKS", "Priyansh Arya", 3.8, "Retained"),
    ("PBKS", "Mitchell Owen", 3.0, "Retained"),
    ("PBKS", "Cooper Connolly", 3.0, "Bought"),
    ("PBKS", "Azmatullah Omarzai", 2.4, "Retained"),
    ("PBKS", "Lockie Ferguson", 2.0, "Retained"),
    ("PBKS", "Vijaykumar Vyshak", 1.8, "Retained"),
    ("PBKS", "Yash Thakur", 1.6, "Retained"),
    ("PBKS", "Harpreet Brar", 1.5, "Retained"),
    ("PBKS", "Vishnu Vinod", 0.95, "Retained"),
    ("PBKS", "Xavier Bartlett", 0.8, "Retained"),
    ("PBKS", "Vishal Nishad", 0.3, "Bought"),
    ("PBKS", "Suryansh Shedge", 0.3, "Retained"),
    ("PBKS", "Pyla Avinash", 0.3, "Retained"),
    ("PBKS", "Musheer Khan", 0.3, "Retained"),
    ("PBKS", "Harnoor Singh", 0.3, "Retained"),
    ("PBKS", "Praveen Dubey", 0.3, "Bought"),

    # ── Rajasthan Royals ──
    ("RR", "Yashasvi Jaiswal", 18.0, "Retained"),
    ("RR", "Dhruv Jurel", 14.0, "Retained"),
    ("RR", "Riyan Parag", 14.0, "Retained"),
    ("RR", "Ravindra Jadeja", 14.0, "Retained"),
    ("RR", "Jofra Archer", 12.5, "Retained"),
    ("RR", "Shimron Hetmyer", 11.0, "Retained"),
    ("RR", "Ravi Bishnoi", 7.2, "Bought"),
    ("RR", "Tushar Deshpande", 6.5, "Retained"),
    ("RR", "Sandeep Sharma", 4.0, "Retained"),
    ("RR", "Nandre Burger", 3.5, "Retained"),
    ("RR", "Sam Curran", 2.4, "Retained"),
    ("RR", "Adam Milne", 2.4, "Bought"),
    ("RR", "Kwena Maphaka", 1.5, "Retained"),
    ("RR", "Vaibhav Sooryavanshi", 1.1, "Retained"),
    ("RR", "Donovan Ferreira", 1.0, "Retained"),
    ("RR", "Ravi Singh", 0.95, "Bought"),
    ("RR", "Sushant Mishra", 0.9, "Bought"),
    ("RR", "Shubham Dubey", 0.8, "Retained"),
    ("RR", "Kuldeep Sen", 0.75, "Bought"),
    ("RR", "Yudhvir Singh", 0.35, "Retained"),
    ("RR", "Yash Raj Punja", 0.3, "Bought"),
    ("RR", "Brijesh Sharma", 0.3, "Bought"),
    ("RR", "Vignesh Puthur", 0.3, "Bought"),
    ("RR", "Aman Rao", 0.3, "Bought"),
    ("RR", "Lhuan-dre Pretorius", 0.3, "Retained"),

    # ── Royal Challengers Bengaluru ──
    ("RCB", "Virat Kohli", 21.0, "Retained"),
    ("RCB", "Josh Hazlewood", 12.5, "Retained"),
    ("RCB", "Phil Salt", 11.5, "Retained"),
    ("RCB", "Rajat Patidar", 11.0, "Retained"),
    ("RCB", "Jitesh Sharma", 11.0, "Retained"),
    ("RCB", "Bhuvneshwar Kumar", 10.75, "Retained"),
    ("RCB", "Venkatesh Iyer", 7.0, "Bought"),
    ("RCB", "Rasikh Salam", 6.0, "Retained"),
    ("RCB", "Krunal Pandya", 5.75, "Retained"),
    ("RCB", "Mangesh Yadav", 5.2, "Bought"),
    ("RCB", "Yash Dayal", 5.0, "Retained"),
    ("RCB", "Tim David", 3.0, "Retained"),
    ("RCB", "Suyash Sharma", 2.6, "Retained"),
    ("RCB", "Jacob Bethell", 2.6, "Retained"),
    ("RCB", "Devdutt Padikkal", 2.0, "Retained"),
    ("RCB", "Jacob Duffy", 2.0, "Bought"),
    ("RCB", "Nuwan Thushara", 1.6, "Retained"),
    ("RCB", "Romario Shepherd", 1.5, "Retained"),
    ("RCB", "Jordan Cox", 0.75, "Bought"),
    ("RCB", "Swapnil Singh", 0.5, "Retained"),
    ("RCB", "Satvik Deswal", 0.3, "Bought"),
    ("RCB", "Kanishk Chouhan", 0.3, "Bought"),
    ("RCB", "Abhinandan Singh", 0.3, "Retained"),
    ("RCB", "Vihaan Malhotra", 0.3, "Bought"),
    ("RCB", "Vicky Ostwal", 0.3, "Bought"),

    # ── Sunrisers Hyderabad ──
    ("SRH", "Heinrich Klaasen", 23.0, "Retained"),
    ("SRH", "Pat Cummins", 18.0, "Retained"),
    ("SRH", "Abhishek Sharma", 14.0, "Retained"),
    ("SRH", "Travis Head", 14.0, "Retained"),
    ("SRH", "Liam Livingstone", 13.0, "Bought"),
    ("SRH", "Ishan Kishan", 11.25, "Retained"),
    ("SRH", "Harshal Patel", 8.0, "Retained"),
    ("SRH", "Nitish Kumar Reddy", 6.0, "Retained"),
    ("SRH", "Jack Edwards", 3.0, "Bought"),
    ("SRH", "Salil Arora", 1.5, "Bought"),
    ("SRH", "Eshan Malinga", 1.2, "Retained"),
    ("SRH", "Jaydev Unadkat", 1.0, "Retained"),
    ("SRH", "Brydon Carse", 1.0, "Retained"),
    ("SRH", "Shivam Mavi", 0.75, "Bought"),
    ("SRH", "Kamindu Mendis", 0.75, "Retained"),
    ("SRH", "Zeeshan Ansari", 0.4, "Retained"),
    ("SRH", "Onkar Tarmale", 0.3, "Bought"),
    ("SRH", "Amit Kumar", 0.3, "Bought"),
    ("SRH", "Shivang Kumar", 0.3, "Bought"),
    ("SRH", "Krains Fuletra", 0.3, "Bought"),
    ("SRH", "Aniket Verma", 0.3, "Retained"),
    ("SRH", "Sakib Hussain", 0.3, "Bought"),
    ("SRH", "Ravichandran Smaran", 0.3, "Retained"),
    ("SRH", "Praful Hinge", 0.3, "Bought"),
    ("SRH", "Harsh Dubey", 0.3, "Retained"),
]

# Manual overrides for name mismatches
NAME_OVERRIDES = {
    "CV Varun (KKR)": ("Varun Chakravarthy", 12.0, "Retained"),
}

def get_last(full_name):
    parts = full_name.lower().split()
    if len(parts) >= 3 and parts[-2] in ("de", "da", "van", "bin", "di"):
        return parts[-2] + parts[-1]
    return parts[-1]

def get_first_init(name):
    name = name.split("(")[0].strip()
    return name.split()[0][0].lower() if name else ""

def get_last_from_display(name):
    name = name.split("(")[0].strip()
    if not name:
        return ""
    parts = name.split()
    if len(parts) >= 3 and parts[-2].lower() in ("de", "da", "van", "bin", "di"):
        return (parts[-2] + parts[-1]).lower()
    return parts[-1].lower()

def matches_first_init(full_name, display_init):
    if not display_init:
        return True
    return full_name.split()[0][0].lower() == display_init

# Build lookup from SQUADS
ACQ_LOOKUP = {}  # (team, last_name) -> (full_name, price, acq_type)
for team, full, price, acq in SQUADS:
    last = get_last(full)
    ACQ_LOOKUP.setdefault(team, {}).setdefault(last, []).append((full, price, acq))

ALL_LAST = {}
for team, full, price, acq in SQUADS:
    last = get_last(full)
    ALL_LAST.setdefault(last, []).append((team, full, price, acq))

def lookup_player(player_name, player_team):
    """Returns (price, acquisition_type) or (0, 'Unknown')."""
    override = NAME_OVERRIDES.get(player_name)
    if override:
        _, price, acq = override
        return price, acq

    last = get_last_from_display(player_name)
    first_init = get_first_init(player_name)
    team = player_team.strip()

    if not last:
        return 0, "Unknown"

    # Same-team match
    if team in ACQ_LOOKUP and last in ACQ_LOOKUP[team]:
        entries = ACQ_LOOKUP[team][last]
        if len(entries) == 1:
            _, price, acq = entries[0]
            return price, acq
        for full, price, acq in entries:
            if matches_first_init(full, first_init):
                return price, acq
        _, price, acq = entries[0]
        return price, acq

    # Cross-team match (handles transfers)
    if last in ALL_LAST:
        candidates = ALL_LAST[last]
        for t, full, price, acq in candidates:
            if t == team and matches_first_init(full, first_init):
                return price, acq
        for t, full, price, acq in candidates:
            if matches_first_init(full, first_init):
                return price, acq
        _, _, price, acq = candidates[0]
        return price, acq

    return 0, "Unknown"


# ── STEP 3: Standardise names ──
def strip_team_suffix(name):
    """Remove '(TEAM)' suffix for matching."""
    return name.split("(")[0].strip()

def normalise(name):
    return name.strip().lower().replace(".", "").replace("  ", " ")


def main():
    # ── Load master ──
    if not os.path.exists(MASTER):
        print(f"ERROR: {MASTER} not found")
        return

    with open(MASTER, newline="") as f:
        reader = csv.DictReader(f)
        master_rows = list(reader)
    master_fields = reader.fieldnames[:]

    # ── STEP 1: Build auction_prices.csv ──
    os.makedirs(os.path.dirname(PRICES_OUT), exist_ok=True)

    price_rows = []
    acq_counts = {"Retained": 0, "Bought": 0, "Unsold": 0, "Unknown": 0}

    for row in master_rows:
        player = row["Player"]
        team = row["Team"]
        price, acq = lookup_player(player, team)

        # Unmatched players who aren't in IPL 2026 data → Unknown
        if acq in acq_counts:
            acq_counts[acq] += 1

        price_rows.append({
            "Player": player,
            "AuctionPrice": f"{price:.1f}",
            "AcquisitionType": acq,
        })

    # Write auction_prices.csv
    with open(PRICES_OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Player", "AuctionPrice", "AcquisitionType"])
        writer.writeheader()
        writer.writerows(price_rows)

    matched_count = acq_counts["Retained"] + acq_counts["Bought"]

    # ── STEP 2: Merge into master_players.csv ──
    price_map = {}
    seen = set()
    for pr in price_rows:
        key = normalise(pr["Player"])
        if key in seen:
            print(f"WARNING: Duplicate player key '{pr['Player']}'")
        seen.add(key)
        price_map[key] = pr

    new_fields = master_fields + ["AuctionPrice", "AcquisitionType"]
    merged_rows = []
    merge_success = 0
    merge_fail = 0

    for row in master_rows:
        key = normalise(row["Player"])
        pr = price_map.get(key)
        if pr:
            row["AuctionPrice"] = pr["AuctionPrice"]
            row["AcquisitionType"] = pr["AcquisitionType"]
            merge_success += 1
        else:
            row["AuctionPrice"] = "0.0"
            row["AcquisitionType"] = "Unknown"
            merge_fail += 1
        merged_rows.append(row)

    with open(MASTER, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fields)
        writer.writeheader()
        writer.writerows(merged_rows)

    # ── STEP 3: Validation report ──
    total = len(merged_rows)

    # Count missing per column
    missing_counts = {}
    for field in new_fields:
        missing_counts[field] = sum(1 for r in merged_rows if not r.get(field, "").strip())

    report_path = "auction_price_report.md"
    with open(report_path, "w") as f:
        f.write("# IPL 2026 Auction Price & Acquisition Report\n\n")
        f.write(f"Generated from `{MASTER}` — {total} players\n\n")

        f.write("## Summary\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Total players | {total} |\n")
        f.write(f"| Successfully matched to IPL 2026 squads | {matched_count} |\n")
        f.write(f"| Retained | {acq_counts['Retained']} |\n")
        f.write(f"| Bought in auction | {acq_counts['Bought']} |\n")
        f.write(f"| Unknown (not in IPL 2026 data) | {acq_counts['Unknown']} |\n")
        f.write(f"| Merge success rate | {merge_success}/{total} ({round(merge_success/total*100,1)}%) |\n\n")

        f.write("## Missing Values by Column\n\n")
        f.write("| Column | Missing Count |\n")
        f.write("|--------|---------------|\n")
        for col, cnt in missing_counts.items():
            f.write(f"| {col} | {cnt} |\n")

        f.write("\n## First 20 Rows of Updated Master\n\n")
        f.write("| " + " | ".join(new_fields) + " |\n")
        f.write("|" + "|".join("---" for _ in new_fields) + "|\n")
        for r in merged_rows[:20]:
            vals = [r.get(f, "") for f in new_fields]
            f.write("| " + " | ".join(vals) + " |\n")

    print(f"✓ {PRICES_OUT} written")
    print(f"✓ {MASTER} updated with AuctionPrice + AcquisitionType")
    print(f"✓ {report_path} written")
    print()
    print(f"  Total: {total}")
    print(f"  Matched: {matched_count}")
    print(f"  Retained: {acq_counts['Retained']}")
    print(f"  Bought: {acq_counts['Bought']}")
    print(f"  Unknown (not in IPL 2026): {acq_counts['Unknown']}")
    print(f"  Merge success: {merge_success}/{total}")


if __name__ == "__main__":
    main()
