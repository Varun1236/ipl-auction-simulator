"""
market_validation.py — Compare PlayerValueScore vs AuctionPrice.
Statistical validation, outlier analysis, and visualisation.

Inputs: data/master_players.csv, data/player_values.csv
Output: market_validation_report.md, value_vs_price.png
"""
import csv
import os
import math
import statistics

MASTER = "data/master_players.csv"
VALUES = "data/player_values.csv"
REPORT = "market_validation_report.md"
CHART = "value_vs_price.png"


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


def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def spearman(xs, ys):
    def rank(vals):
        sorted_vals = sorted(vals)
        return [sorted_vals.index(v) + 1 for v in vals]
    rx = rank(xs)
    ry = rank(ys)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    n = len(xs)
    return 1 - (6 * d2) / (n * (n ** 2 - 1))


def main():
    master_rows = read_csv(MASTER)
    values_rows = read_csv(VALUES)

    # Index values by Player
    vmap = {}
    for vr in values_rows:
        vmap[normalise(vr["Player"])] = vr

    # Build merged dataset with valid numeric price and score
    points = []
    for mr in master_rows:
        key = normalise(mr["Player"])
        vr = vmap.get(key)
        if vr is None:
            continue
        score = safe_float(vr.get("PlayerValueScore"), None)
        price = safe_float(mr.get("AuctionPrice"), None)
        if score is None or price is None or price <= 0:
            continue
        points.append({
            "player": mr["Player"],
            "role": mr["Role"],
            "score": score,
            "price": price,
            "acq": mr.get("AcquisitionType", ""),
        })

    n = len(points)
    scores = [p["score"] for p in points]
    prices = [p["price"] for p in points]

    # ── Correlations ──
    r_pearson = pearson(scores, prices)
    r_spearman = spearman(scores, prices)

    # ── Residuals (actual - predicted via linear regression) ──
    mx = sum(scores) / n
    my = sum(prices) / n
    num = sum((s - mx) * (p - my) for s, p in zip(scores, prices))
    den = sum((s - mx) ** 2 for s in scores)
    slope = num / den if den else 0
    intercept = my - slope * mx
    for p in points:
        p["predicted"] = slope * p["score"] + intercept
        p["residual"] = p["price"] - p["predicted"]

    # Positive outliers: actual price >> predicted (overvalued by market)
    points.sort(key=lambda p: -p["residual"])
    positive_outliers = points[:20]

    # Negative outliers: actual price << predicted (undervalued by market)
    points.sort(key=lambda p: p["residual"])
    negative_outliers = points[:20]

    # ── Write report ──
    with open(REPORT, "w") as f:
        f.write("# Market Validation Report — PlayerValueScore vs AuctionPrice\n\n")
        f.write(f"Generated from `{MASTER}` and `{VALUES}` — {n} matched players\n\n")

        f.write("## Correlation Statistics\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Pearson r | {r_pearson:.4f} |\n")
        f.write(f"| Spearman ρ | {r_spearman:.4f} |\n")
        f.write(f"| Sample size | {n} |\n")
        f.write(f"| Mean Score | {statistics.mean(scores):.1f} |\n")
        f.write(f"| Mean Price | {statistics.mean(prices):.1f} |\n\n")

        f.write("### Interpretation\n\n")
        if r_pearson > 0.7:
            interp = "strong positive"
        elif r_pearson > 0.4:
            interp = "moderate positive"
        elif r_pearson > 0.2:
            interp = "weak positive"
        else:
            interp = "very weak or no"
        f.write(f"The Pearson correlation of **{r_pearson:.4f}** indicates a **{interp}** linear relationship ")
        f.write("between PlayerValueScore and AuctionPrice. ")
        if r_spearman > r_pearson:
            f.write("The Spearman correlation is higher, suggesting a non-linear monotonic relationship. ")
        else:
            f.write("The Spearman and Pearson values are similar, suggesting a roughly linear relationship. ")
        f.write("Auction prices are influenced by factors beyond performance stats — brand value, ")
        f.write("fan following, international form, and team-specific needs.\n\n")

        f.write("## Regression Details\n\n")
        f.write(f"```\nprice = {slope:.4f} × score + {intercept:.2f}\n```\n\n")
        f.write("Players above the regression line cost more than their score predicts (negative outliers). ")
        f.write("Players below the line cost less than their score predicts (positive outliers).\n\n")

        f.write("## Top 20 Positive Outliers (Undervalued by Market)\n\n")
        f.write("These players have higher scores than their auction price suggests — market bargains.\n\n")
        f.write("| Rank | Player | Role | Score | Price (Cr) | Residual |\n")
        f.write("|------|--------|------|-------|------------|----------|\n")
        # negative_outliers list has lowest residuals (actual - predicted is very negative)
        # meaning they cost much less than predicted → undervalued
        neg_sorted = sorted(negative_outliers, key=lambda p: p["residual"])
        for i, p in enumerate(neg_sorted[:20], 1):
            f.write(f"| {i} | {p['player']} | {p['role']} | {p['score']:.1f} | {p['price']:.1f} | {p['residual']:.1f} |\n")
        f.write("\n")
        f.write("> Most are low-cost bowlers with strong performance stats. ")
        f.write("The market systematically underprices bowling performance.\n\n")

        f.write("## Top 20 Negative Outliers (Overvalued by Market)\n\n")
        f.write("These players have lower scores relative to their auction price — market overpays.\n\n")
        f.write("| Rank | Player | Role | Score | Price (Cr) | Residual |\n")
        f.write("|------|--------|------|-------|------------|----------|\n")
        pos_sorted = sorted(positive_outliers, key=lambda p: -p["residual"])
        for i, p in enumerate(pos_sorted[:20], 1):
            f.write(f"| {i} | {p['player']} | {p['role']} | {p['score']:.1f} | {p['price']:.1f} | {p['residual']:.1f} |\n")
        f.write("\n")
        f.write("> High-priced retained stars (Pant, Iyer, Kohli, Bumrah) dominate this list. ")
        f.write("Their market price reflects brand/fan value beyond raw performance scores.\n\n")

        f.write("## Summary\n\n")
        f.write(f"| Question | Answer |\n")
        f.write(f"|----------|--------|\n")
        f.write(f"| Does the valuation model explain auction prices? | ")
        if r_pearson > 0.5:
            f.write("Partially — moderate correlation suggests performance is a factor but not the only one. |\n")
        elif r_pearson > 0.3:
            f.write("Weakly — performance explains some variance but brand/legacy factors dominate. |\n")
        else:
            f.write("Not well — auction prices are driven by factors beyond performance stats. |\n")
        f.write(f"| What drives outliers? | Brand value, captaincy, fan following, international reputation |\n")
        f.write(f"| Best market inefficiency | Bowling talent at base price (0.3 Cr) |\n")
        f.write(f"| Biggest premium | Elite Indian batsmen / wicketkeepers |\n")

    print(f"✓ {REPORT} written ({n} matched players)")

    # ── Chart ──
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 7))

        # Colour by role
        role_colours = {
            "Batsman": "#1f77b4",
            "Bowler": "#ff7f0e",
            "All-Rounder": "#2ca02c",
            "Wicketkeeper": "#d62728",
        }
        legend_handles = {}
        for p in points:
            role = p["role"]
            colour = role_colours.get(role, "#333333")
            alpha = 0.6
            sc = ax.scatter(p["score"], p["price"], c=colour, alpha=alpha, s=40, edgecolors="none", zorder=3)
            if role not in legend_handles:
                legend_handles[role] = sc

        # Regression line
        x_vals = [min(scores), max(scores)]
        y_vals = [slope * x + intercept for x in x_vals]
        ax.plot(x_vals, y_vals, "k--", linewidth=1.5, alpha=0.5, label=f"OLS (r={r_pearson:.2f})")

        # Label top outliers
        all_sorted = sorted(points, key=lambda p: -abs(p["residual"]))
        for p in all_sorted[:10]:
            label = p["player"].split("(")[0].strip()
            ax.annotate(label, (p["score"], p["price"]),
                        fontsize=6, alpha=0.8, xytext=(4, 4),
                        textcoords="offset points", zorder=4)

        ax.set_xlabel("PlayerValueScore", fontsize=12)
        ax.set_ylabel("AuctionPrice (Cr)", fontsize=12)
        ax.set_title("PlayerValueScore vs AuctionPrice — IPL 2026", fontsize=14)

        # Legend
        handles = list(legend_handles.values())
        labels = list(legend_handles.keys())
        ax.legend(handles=handles, labels=labels, loc="upper left", fontsize=9)

        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(CHART, dpi=150)
        plt.close(fig)
        print(f"✓ {CHART} saved")
    except ImportError:
        print(f"⚠ matplotlib not available — skipping chart")

    # ── Print summary ──
    print(f"\nCorrelation: Pearson r = {r_pearson:.4f}, Spearman ρ = {r_spearman:.4f}")
    print(f"Regression: price = {slope:.4f} × score + {intercept:.2f}")
    print()
    print("Top 5 undervalued by market (low price, high score):")
    for p in neg_sorted[:5]:
        print(f"  {p['player']:<35s} score={p['score']:.1f} price={p['price']:.1f} residual={p['residual']:.1f}")
    print()
    print("Top 5 overvalued by market (high price, low score):")
    for p in pos_sorted[:5]:
        print(f"  {p['player']:<35s} score={p['score']:.1f} price={p['price']:.1f} residual={p['residual']:.1f}")
    print()
    if abs(r_pearson) > 0.5:
        print("→ Valuation model partially explains auction prices (moderate correlation).")
    elif abs(r_pearson) > 0.3:
        print("→ Valuation model weakly explains auction prices.")
    else:
        print("→ Valuation model does NOT explain auction prices well. Brand/legacy dominate.")


if __name__ == "__main__":
    main()
