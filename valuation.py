"""
Player valuation scoring for IPL auction simulation.

Reads player data from data/master_players.csv, computes a
PlayerValueScore (0-100) based on role-specific performance
metrics and age adjustments, and writes results to
data/player_values.csv.
"""

import pandas as pd


def min_max_scale(series, higher_is_better=True):
    """
    Min-max normalize a Series to [0, 100].

    Parameters
    ----------
    series : pd.Series
        Numeric values to normalize.
    higher_is_better : bool
        If True, higher raw values yield higher scores.
        If False, lower raw values yield higher scores.

    Returns
    -------
    pd.Series
        Normalized values in [0, 100].
    """
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series(50.0, index=series.index)
    if higher_is_better:
        return (series - mn) / (mx - mn) * 100.0
    return (mx - series) / (mx - mn) * 100.0


def main():
    df = pd.read_csv('data/master_players.csv')

    # --- Handle missing values ---
    # Fill missing numeric fields with column medians
    for col in ['Runs', 'Wickets', 'StrikeRate', 'Economy', 'Age', 'AuctionPrice']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # --- Normalise input metrics across all players ---
    df['RunsScore'] = min_max_scale(df['Runs'])
    df['StrikeRateScore'] = min_max_scale(df['StrikeRate'])
    df['WicketsScore'] = min_max_scale(df['Wickets'])

    # Economy is only meaningful for players who have taken wickets;
    # assign the worst observed economy to non-bowlers so they aren't
    # unfairly rewarded for having economy = 0.
    bowl_mask = df['Wickets'] > 0
    if bowl_mask.any():
        worst_econ = df.loc[bowl_mask, 'Economy'].max()
        df.loc[~bowl_mask, 'Economy'] = worst_econ
    df['EconomyScore'] = min_max_scale(df['Economy'], higher_is_better=False)

    # --- Role classification ---
    def classify(role):
        r = str(role).strip().lower()
        if r in ('batsman', 'wicketkeeper'):
            return 'batter'
        if r == 'bowler':
            return 'bowler'
        if r == 'allrounder':
            return 'allrounder'
        return 'batter'

    df['ScoreGroup'] = df['Role'].apply(classify)

    # --- Raw composite score per role ---
    def compute_raw(row):
        g = row['ScoreGroup']
        if g == 'batter':
            return 0.6 * row['RunsScore'] + 0.4 * row['StrikeRateScore']
        if g == 'bowler':
            return 0.6 * row['WicketsScore'] + 0.4 * row['EconomyScore']
        batting = 0.5 * row['RunsScore'] + 0.5 * row['StrikeRateScore']
        bowling = 0.5 * row['WicketsScore'] + 0.5 * row['EconomyScore']
        return (batting + bowling) / 2.0

    df['RawScore'] = df.apply(compute_raw, axis=1)

    # --- Age adjustment ---
    # Prime years (24-30): +10 % bonus
    # Senior years (>34):  -15 % penalty
    def age_adjust(age, score):
        if 24 <= age <= 30:
            return score * 1.10
        if age > 34:
            return score * 0.85
        return score

    df['AdjScore'] = df.apply(
        lambda r: age_adjust(r['Age'], r['RawScore']), axis=1
    )

    # --- Final normalisation to [0, 100] ---
    df['PlayerValueScore'] = min_max_scale(df['AdjScore']).round(1)

    # --- Output ---
    out = df[['Player', 'Role', 'PlayerValueScore']].copy()
    out = out.sort_values('PlayerValueScore', ascending=False).reset_index(drop=True)
    out.to_csv('data/player_values.csv', index=False)

    print("Top 10 players by PlayerValueScore:")
    print(out.head(10).to_string(index=False))


if __name__ == '__main__':
    main()
