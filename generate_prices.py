"""
Generate data/auction_prices.csv and auction_price_report.md
by matching master_players.csv against IPL 2026 auction/squad prices.
"""
import csv
import os

MASTER = "data/master_players.csv"
PRICES_OUT = "data/auction_prices.csv"
REPORT = "auction_price_report.md"

# IPL 2026 squad prices from ESPN Cricinfo — (team, full_name, price_crores)
# Includes both retained players and auction buys.
SQUADS = [
    # ── Chennai Super Kings ──
    ("CSK", "Ruturaj Gaikwad", 18.0),
    ("CSK", "Sanju Samson", 18.0),
    ("CSK", "Kartik Sharma", 14.2),
    ("CSK", "Prashant Veer", 14.2),
    ("CSK", "Shivam Dube", 12.0),
    ("CSK", "Noor Ahmad", 10.0),
    ("CSK", "Rahul Chahar", 5.2),
    ("CSK", "Khaleel Ahmed", 4.8),
    ("CSK", "MS Dhoni", 4.0),
    ("CSK", "Anshul Kamboj", 3.4),
    ("CSK", "Gurjapneet Singh", 2.2),
    ("CSK", "Dewald Brevis", 2.2),
    ("CSK", "Nathan Ellis", 2.0),
    ("CSK", "Akeal Hosein", 2.0),
    ("CSK", "Matt Henry", 2.0),
    ("CSK", "Matthew Short", 1.5),
    ("CSK", "Jamie Overton", 1.5),
    ("CSK", "Zak Foulkes", 0.75),
    ("CSK", "Sarfaraz Khan", 0.75),
    ("CSK", "Aman Khan", 0.4),
    ("CSK", "Ayush Mhatre", 0.3),
    ("CSK", "Ramakrishna Ghosh", 0.3),
    ("CSK", "Urvil Patel", 0.3),
    ("CSK", "Mukesh Choudhary", 0.3),
    ("CSK", "Shreyas Gopal", 0.3),

    # ── Delhi Capitals ──
    ("DC", "Axar Patel", 16.5),
    ("DC", "KL Rahul", 14.0),
    ("DC", "Kuldeep Yadav", 13.25),
    ("DC", "Mitchell Starc", 11.75),
    ("DC", "T Natarajan", 10.75),
    ("DC", "Tristan Stubbs", 10.0),
    ("DC", "Auqib Nabi", 8.4),
    ("DC", "Mukesh Kumar", 8.0),
    ("DC", "Nitish Rana", 4.2),
    ("DC", "Abishek Porel", 4.0),
    ("DC", "Pathum Nissanka", 4.0),
    ("DC", "Ashutosh Sharma", 3.8),
    ("DC", "Kyle Jamieson", 2.0),
    ("DC", "Lungi Ngidi", 2.0),
    ("DC", "Ben Duckett", 2.0),
    ("DC", "David Miller", 2.0),
    ("DC", "Sameer Rizvi", 0.95),
    ("DC", "Prithvi Shaw", 0.75),
    ("DC", "Dushmantha Chameera", 0.75),
    ("DC", "Vipraj Nigam", 0.5),
    ("DC", "Karun Nair", 0.5),
    ("DC", "Madhav Tiwari", 0.4),
    ("DC", "Sahil Parakh", 0.3),
    ("DC", "Tripurana Vijay", 0.3),
    ("DC", "Ajay Mandal", 0.3),

    # ── Gujarat Titans ──
    ("GT", "Rashid Khan", 18.0),
    ("GT", "Shubman Gill", 16.5),
    ("GT", "Jos Buttler", 15.75),
    ("GT", "Mohammed Siraj", 12.25),
    ("GT", "Kagiso Rabada", 10.75),
    ("GT", "Prasidh Krishna", 9.5),
    ("GT", "Sai Sudharsan", 8.5),
    ("GT", "Jason Holder", 7.0),
    ("GT", "M Shahrukh Khan", 4.0),
    ("GT", "Rahul Tewatia", 4.0),
    ("GT", "Washington Sundar", 3.2),
    ("GT", "Sai Kishore", 2.0),
    ("GT", "Tom Banton", 2.0),
    ("GT", "Glenn Phillips", 2.0),
    ("GT", "Gurnoor Brar", 1.3),
    ("GT", "Arshad Khan", 1.3),
    ("GT", "Ashok Sharma", 0.9),
    ("GT", "Luke Wood", 0.75),
    ("GT", "Jayant Yadav", 0.75),
    ("GT", "Ishant Sharma", 0.75),
    ("GT", "Kumar Kushagra", 0.65),
    ("GT", "Nishant Sindhu", 0.3),
    ("GT", "Manav Suthar", 0.3),
    ("GT", "Anuj Rawat", 0.3),
    ("GT", "Prithvi Raj", 0.3),

    # ── Kolkata Knight Riders ──
    ("KKR", "Cameron Green", 25.2),
    ("KKR", "Matheesha Pathirana", 18.0),
    ("KKR", "Rinku Singh", 13.0),
    ("KKR", "Varun Chakravarthy", 12.0),
    ("KKR", "Sunil Narine", 12.0),
    ("KKR", "Mustafizur Rahman", 9.2),
    ("KKR", "Harshit Rana", 4.0),
    ("KKR", "Ramandeep Singh", 4.0),
    ("KKR", "Tejasvi Dahiya", 3.0),
    ("KKR", "Angkrish Raghuvanshi", 3.0),
    ("KKR", "Rachin Ravindra", 2.0),
    ("KKR", "Finn Allen", 2.0),
    ("KKR", "Vaibhav Arora", 1.8),
    ("KKR", "Rovman Powell", 1.5),
    ("KKR", "Tim Seifert", 1.5),
    ("KKR", "Ajinkya Rahane", 1.5),
    ("KKR", "Akash Deep", 1.0),
    ("KKR", "Umran Malik", 0.75),
    ("KKR", "Rahul Tripathi", 0.75),
    ("KKR", "Manish Pandey", 0.75),
    ("KKR", "Anukul Roy", 0.4),
    ("KKR", "Daksh Kamra", 0.3),
    ("KKR", "Prashant Solanki", 0.3),
    ("KKR", "Kartik Tyagi", 0.3),
    ("KKR", "Sarthak Ranjan", 0.3),

    # ── Lucknow Super Giants ──
    ("LSG", "Rishabh Pant", 27.0),
    ("LSG", "Nicholas Pooran", 21.0),
    ("LSG", "Mayank Yadav", 11.0),
    ("LSG", "Mohammed Shami", 10.0),
    ("LSG", "Avesh Khan", 9.75),
    ("LSG", "Josh Inglis", 8.6),
    ("LSG", "Abdul Samad", 4.2),
    ("LSG", "Ayush Badoni", 4.0),
    ("LSG", "Mohsin Khan", 4.0),
    ("LSG", "Mitchell Marsh", 3.4),
    ("LSG", "Mukul Choudhary", 2.6),
    ("LSG", "Shahbaz Ahmed", 2.4),
    ("LSG", "Akshat Raghuwanshi", 2.2),
    ("LSG", "Wanindu Hasaranga", 2.0),
    ("LSG", "Aiden Markram", 2.0),
    ("LSG", "Anrich Nortje", 2.0),
    ("LSG", "Naman Tiwari", 1.0),
    ("LSG", "Manimaran Siddharth", 0.75),
    ("LSG", "Matthew Breetzke", 0.75),
    ("LSG", "Digvesh Rathi", 0.3),
    ("LSG", "Arshin Kulkarni", 0.3),
    ("LSG", "Prince Yadav", 0.3),
    ("LSG", "Akash Singh", 0.3),
    ("LSG", "Arjun Tendulkar", 0.3),
    ("LSG", "Himmat Singh", 0.3),

    # ── Mumbai Indians ──
    ("MI", "Jasprit Bumrah", 18.0),
    ("MI", "Hardik Pandya", 16.35),
    ("MI", "Suryakumar Yadav", 16.35),
    ("MI", "Rohit Sharma", 16.3),
    ("MI", "Trent Boult", 12.5),
    ("MI", "Deepak Chahar", 9.25),
    ("MI", "Tilak Varma", 8.0),
    ("MI", "Naman Dhir", 5.25),
    ("MI", "Will Jacks", 5.25),
    ("MI", "AM Ghazanfar", 4.8),
    ("MI", "Sherfane Rutherford", 2.6),
    ("MI", "Mitchell Santner", 2.0),
    ("MI", "Shardul Thakur", 2.0),
    ("MI", "Ryan Rickelton", 1.0),
    ("MI", "Quinton de Kock", 1.0),
    ("MI", "Corbin Bosch", 0.75),
    ("MI", "Robin Minz", 0.65),
    ("MI", "Mohd Izhar", 0.3),
    ("MI", "Danish Malewar", 0.3),
    ("MI", "Raj Bawa", 0.3),
    ("MI", "Ashwani Kumar", 0.3),
    ("MI", "Atharva Ankolekar", 0.3),
    ("MI", "Raghu Sharma", 0.3),
    ("MI", "Mayank Markande", 0.3),
    ("MI", "Mayank Rawat", 0.3),

    # ── Punjab Kings ──
    ("PBKS", "Shreyas Iyer", 26.75),
    ("PBKS", "Arshdeep Singh", 18.0),
    ("PBKS", "Yuzvendra Chahal", 18.0),
    ("PBKS", "Marcus Stoinis", 11.0),
    ("PBKS", "Marco Jansen", 7.0),
    ("PBKS", "Shashank Singh", 5.5),
    ("PBKS", "Ben Dwarshuis", 4.4),
    ("PBKS", "Nehal Wadhera", 4.2),
    ("PBKS", "Prabhsimran Singh", 4.0),
    ("PBKS", "Priyansh Arya", 3.8),
    ("PBKS", "Mitchell Owen", 3.0),
    ("PBKS", "Cooper Connolly", 3.0),
    ("PBKS", "Azmatullah Omarzai", 2.4),
    ("PBKS", "Lockie Ferguson", 2.0),
    ("PBKS", "Vijaykumar Vyshak", 1.8),
    ("PBKS", "Yash Thakur", 1.6),
    ("PBKS", "Harpreet Brar", 1.5),
    ("PBKS", "Vishnu Vinod", 0.95),
    ("PBKS", "Xavier Bartlett", 0.8),
    ("PBKS", "Vishal Nishad", 0.3),
    ("PBKS", "Suryansh Shedge", 0.3),
    ("PBKS", "Pyla Avinash", 0.3),
    ("PBKS", "Musheer Khan", 0.3),
    ("PBKS", "Harnoor Singh", 0.3),
    ("PBKS", "Praveen Dubey", 0.3),

    # ── Rajasthan Royals ──
    ("RR", "Yashasvi Jaiswal", 18.0),
    ("RR", "Dhruv Jurel", 14.0),
    ("RR", "Riyan Parag", 14.0),
    ("RR", "Ravindra Jadeja", 14.0),
    ("RR", "Jofra Archer", 12.5),
    ("RR", "Shimron Hetmyer", 11.0),
    ("RR", "Ravi Bishnoi", 7.2),
    ("RR", "Tushar Deshpande", 6.5),
    ("RR", "Sandeep Sharma", 4.0),
    ("RR", "Nandre Burger", 3.5),
    ("RR", "Sam Curran", 2.4),
    ("RR", "Adam Milne", 2.4),
    ("RR", "Kwena Maphaka", 1.5),
    ("RR", "Vaibhav Sooryavanshi", 1.1),
    ("RR", "Donovan Ferreira", 1.0),
    ("RR", "Ravi Singh", 0.95),
    ("RR", "Sushant Mishra", 0.9),
    ("RR", "Shubham Dubey", 0.8),
    ("RR", "Kuldeep Sen", 0.75),
    ("RR", "Yudhvir Singh", 0.35),
    ("RR", "Yash Raj Punja", 0.3),
    ("RR", "Brijesh Sharma", 0.3),
    ("RR", "Vignesh Puthur", 0.3),
    ("RR", "Aman Rao", 0.3),
    ("RR", "Lhuan-dre Pretorius", 0.3),

    # ── Royal Challengers Bengaluru ──
    ("RCB", "Virat Kohli", 21.0),
    ("RCB", "Josh Hazlewood", 12.5),
    ("RCB", "Phil Salt", 11.5),
    ("RCB", "Rajat Patidar", 11.0),
    ("RCB", "Jitesh Sharma", 11.0),
    ("RCB", "Bhuvneshwar Kumar", 10.75),
    ("RCB", "Venkatesh Iyer", 7.0),
    ("RCB", "Rasikh Salam", 6.0),
    ("RCB", "Krunal Pandya", 5.75),
    ("RCB", "Mangesh Yadav", 5.2),
    ("RCB", "Yash Dayal", 5.0),
    ("RCB", "Tim David", 3.0),
    ("RCB", "Suyash Sharma", 2.6),
    ("RCB", "Jacob Bethell", 2.6),
    ("RCB", "Devdutt Padikkal", 2.0),
    ("RCB", "Jacob Duffy", 2.0),
    ("RCB", "Nuwan Thushara", 1.6),
    ("RCB", "Romario Shepherd", 1.5),
    ("RCB", "Jordan Cox", 0.75),
    ("RCB", "Swapnil Singh", 0.5),
    ("RCB", "Satvik Deswal", 0.3),
    ("RCB", "Kanishk Chouhan", 0.3),
    ("RCB", "Abhinandan Singh", 0.3),
    ("RCB", "Vihaan Malhotra", 0.3),
    ("RCB", "Vicky Ostwal", 0.3),

    # ── Sunrisers Hyderabad ──
    ("SRH", "Heinrich Klaasen", 23.0),
    ("SRH", "Pat Cummins", 18.0),
    ("SRH", "Abhishek Sharma", 14.0),
    ("SRH", "Travis Head", 14.0),
    ("SRH", "Liam Livingstone", 13.0),
    ("SRH", "Ishan Kishan", 11.25),
    ("SRH", "Harshal Patel", 8.0),
    ("SRH", "Nitish Kumar Reddy", 6.0),
    ("SRH", "Jack Edwards", 3.0),
    ("SRH", "Salil Arora", 1.5),
    ("SRH", "Eshan Malinga", 1.2),
    ("SRH", "Jaydev Unadkat", 1.0),
    ("SRH", "Brydon Carse", 1.0),
    ("SRH", "Shivam Mavi", 0.75),
    ("SRH", "Kamindu Mendis", 0.75),
    ("SRH", "Zeeshan Ansari", 0.4),
    ("SRH", "Onkar Tarmale", 0.3),
    ("SRH", "Amit Kumar", 0.3),
    ("SRH", "Shivang Kumar", 0.3),
    ("SRH", "Krains Fuletra", 0.3),
    ("SRH", "Aniket Verma", 0.3),
    ("SRH", "Sakib Hussain", 0.3),
    ("SRH", "Ravichandran Smaran", 0.3),
    ("SRH", "Praful Hinge", 0.3),
    ("SRH", "Harsh Dubey", 0.3),
]

# Manual overrides for players whose display name doesn't match their squad name
NAME_OVERRIDES = {
    "CV Varun (KKR)": 12.0,   # Varun Chakravarthy
}

# Build lookup structures
def get_last(full_name):
    parts = full_name.lower().split()
    if len(parts) >= 3 and parts[-2] in ("de", "da", "van", "bin", "di"):
        return parts[-2] + parts[-1]
    return parts[-1]

TEAM_FULL = {}  # team -> {full_name_lower: price}
TEAM_LAST = {}  # team -> {last_name: [(full, price)]}
ALL_LAST = {}   # last_name -> [(team, full, price)]

for team, full, price in SQUADS:
    fn_lower = full.lower()
    last = get_last(fn_lower)
    TEAM_FULL.setdefault(team, {})[fn_lower] = price
    TEAM_LAST.setdefault(team, {}).setdefault(last, []).append((full, price))
    ALL_LAST.setdefault(last, []).append((team, full, price))


def get_first_init(name):
    """Extract first character of first name from display name like 'A Badoni' or 'AD Russell'."""
    name = name.split("(")[0].strip()
    if not name:
        return ""
    return name.split()[0][0].lower()


def get_last_from_display(name):
    """Extract last name from display name like 'A Badoni' → 'badoni'."""
    name = name.split("(")[0].strip()
    if not name:
        return ""
    parts = name.split()
    # Handle compound last names
    if len(parts) >= 3 and parts[-2].lower() in ("de", "da", "van", "bin", "di"):
        return (parts[-2] + parts[-1]).lower()
    return parts[-1].lower()


def matches_first_init(full_name, display_init):
    """Check if full name's first initial matches display name's first initial."""
    if not display_init:
        return True
    full_first = full_name.split()[0][0].lower()
    return full_first == display_init


def try_match_price(player_name, player_team):
    last = get_last_from_display(player_name)
    first_init = get_first_init(player_name)
    team = player_team.strip()

    if not last:
        return None

    # 1. Exact match by (team, last_name)
    if team in TEAM_LAST and last in TEAM_LAST[team]:
        entries = TEAM_LAST[team][last]
        if len(entries) == 1:
            return entries[0][1]
        for full, price in entries:
            if matches_first_init(full, first_init):
                return price
        return entries[0][1]

    # 2. Match by last_name across all teams (handles team changes like Q de Kock: KKR→MI)
    if last in ALL_LAST:
        candidates = ALL_LAST[last]
        # prefer same team if available
        for team2, full, price in candidates:
            if team2 == team and matches_first_init(full, first_init):
                return price
        for team2, full, price in candidates:
            if matches_first_init(full, first_init):
                return price
        return candidates[0][2]

    # 3. Try full-name textual match
    name_clean = player_name.split("(")[0].strip().lower().replace(".", "")
    for t, full, price in SQUADS:
        fn = full.lower()
        if name_clean in fn or fn in name_clean:
            return price

    return None


def main():
    if not os.path.exists(MASTER):
        print(f"ERROR: {MASTER} not found")
        return

    with open(MASTER, newline="") as f:
        reader = csv.DictReader(f)
        master_rows = list(reader)

    matched = []
    unmatched = []
    results = []

    for row in master_rows:
        player = row["Player"]
        team = row["Team"]
        price = NAME_OVERRIDES.get(player)
        if price is None:
            price = try_match_price(player, team)

        if price is not None:
            matched.append((player, team, price))
        else:
            unmatched.append((player, team))

        results.append({
            "Player": player,
            "AuctionPrice": f"{price:.1f}" if price is not None else ""
        })

    os.makedirs(os.path.dirname(PRICES_OUT), exist_ok=True)
    with open(PRICES_OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Player", "AuctionPrice"])
        writer.writeheader()
        writer.writerows(results)

    total = len(results)
    matched_count = len(matched)
    unmatched_count = len(unmatched)
    pct = round(matched_count / total * 100, 1)

    # ── Report ──
    with open(REPORT, "w") as f:
        f.write("# IPL 2026 Auction Price Report\n\n")
        f.write(f"Generated from `{MASTER}` — {total} players in pool\n\n")
        f.write("## Summary\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Total players in master list | {total} |\n")
        f.write(f"| Matched (price found) | {matched_count} |\n")
        f.write(f"| Unmatched (no price) | {unmatched_count} |\n")
        f.write(f"| Coverage | {pct}% |\n\n")
        f.write("**Note:** Prices include both IPL 2026 auction buys and retained players. ")
        f.write("Prices sourced from ESPN Cricinfo. ")
        f.write("Unmatched players either went unsold, were not part of IPL 2026, ")
        f.write("or were not found in the published squad lists.\n\n")

        f.write("---\n\n")
        f.write("## Matched Players\n\n")
        f.write("| Player | Team | Price (Cr) |\n")
        f.write("|--------|------|------------|\n")
        for player, team, p in sorted(matched, key=lambda x: -x[2]):
            f.write(f"| {player} | {team} | {p} |\n")

        f.write("\n---\n\n")
        f.write("## Unmatched Players\n\n")
        f.write("| Player | Team |\n")
        f.write("|--------|------|\n")
        for player, team in sorted(unmatched, key=lambda x: x[0].lower()):
            f.write(f"| {player} | {team} |\n")

    print(f"✓ {PRICES_OUT} — {matched_count} matched, {unmatched_count} unmatched ({pct}% coverage)")
    print(f"✓ {REPORT} written")


if __name__ == "__main__":
    main()
