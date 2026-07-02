"""
Auction engine for IPL auction simulation.

Reads player valuations and master data, runs a sealed-bid auction
where each team bids up to a calculated maximum, and records results.
"""

import pandas as pd


def make_strategies(df):
    """
    Build a dict of team -> strategy function.

    Each function takes a player row and returns a multiplier (>= 1.0)
    that inflates the team's valuation for that player.
    """
    # Precompute thresholds used by multiple strategies
    median_sr = df['StrikeRate'].median()
    batter_sr_median = df.loc[df['Role'].str.lower() == 'batsman', 'StrikeRate'].median()

    def mi(player):
        return 1.2 if player['PlayerValueScore'] > 80 else 1.0

    def csk(player):
        return 1.15 if player['Age'] >= 30 else 1.0

    def rr(player):
        return 1.2 if player['Age'] < 26 else 1.0

    def rcb(player):
        return 1.15 if player['Role'].lower() == 'batsman' else 1.0

    def kkr(player):
        return 1.15 if player['Role'].lower() == 'bowler' else 1.0

    def gt(player):
        return 1.1 if player['Role'].lower() == 'allrounder' else 1.0

    def lsg(player):
        return 1.1 if player['Role'].lower() == 'wicketkeeper' else 1.0

    def pbks(player):
        return 1.1 if player['StrikeRate'] >= median_sr else 1.0

    def dc(player):
        return 1.1 if player['Age'] < 28 else 1.0

    def srh(player):
        is_batter = player['Role'].lower() == 'batsman'
        return 1.15 if is_batter and player['StrikeRate'] >= batter_sr_median else 1.0

    return {
        'MI': mi,
        'CSK': csk,
        'RR': rr,
        'RCB': rcb,
        'KKR': kkr,
        'GT': gt,
        'LSG': lsg,
        'PBKS': pbks,
        'DC': dc,
        'SRH': srh,
    }


def main():
    # --- Load data ---
    values = pd.read_csv('data/player_values.csv')
    master = pd.read_csv('data/master_players.csv')

    # Merge player details with valuation scores, sorted best first
    df = values.merge(
        master[['Player', 'Age', 'Nationality', 'Runs', 'Wickets',
                'StrikeRate', 'Economy', 'AuctionPrice']],
        on='Player',
        how='left',
    )
    df = df.sort_values('PlayerValueScore', ascending=False).reset_index(drop=True)

    # --- Initialise 10 franchises with 120 Cr each ---
    teams = ['MI', 'CSK', 'RCB', 'RR', 'KKR', 'GT', 'LSG', 'PBKS', 'DC', 'SRH']
    budgets = {t: 120.0 for t in teams}
    squads = {t: [] for t in teams}
    max_squad = 8

    strategies = make_strategies(df)

    results = []

    # --- Auction loop ---
    for _, player in df.iterrows():
        name = player['Player']
        score = player['PlayerValueScore']

        bids = {}
        for team in teams:
            # Skip teams at max squad size or without budget
            if len(squads[team]) >= max_squad or budgets[team] <= 0:
                continue

            # Apply team-specific strategy multiplier and compute max bid
            multiplier = strategies[team](player)
            adj_score = score * multiplier
            raw_bid = adj_score / 100.0 * 20.0
            bids[team] = min(raw_bid, budgets[team])

        if not bids:
            continue

        # Winner is the team with the highest bid.
        # Tie-break: earlier team in the list gets priority.
        winner = max(bids, key=lambda t: (bids[t], -teams.index(t)))
        winning_bid = round(bids[winner], 1)

        budgets[winner] = round(budgets[winner] - winning_bid, 1)
        squads[winner].append(name)

        results.append({
            'Player': name,
            'WinningTeam': winner,
            'WinningBid': winning_bid,
        })

        print(f"Player: {name}")
        print(f"Winner: {winner}")
        print(f"Price: {winning_bid} Cr")
        print()

    # --- Final budgets ---
    print("=" * 40)
    print("FINAL BUDGETS")
    print("=" * 40)
    for team in teams:
        spent = round(120.0 - budgets[team], 1)
        print(f"{team}: {budgets[team]:.1f} Cr remaining "
              f"(spent {spent:.1f} Cr, {len(squads[team])} players)")

    # --- Squad sizes ---
    print()
    print("=" * 40)
    print("SQUAD SIZES")
    print("=" * 40)
    for team in teams:
        print(f"{team}: {len(squads[team])} players")

    # --- Save results ---
    out_df = pd.DataFrame(results)
    out_df.to_csv('data/auction_results.csv', index=False)
    print(f"\nResults saved to data/auction_results.csv "
          f"({len(out_df)} players sold)")


if __name__ == '__main__':
    main()
