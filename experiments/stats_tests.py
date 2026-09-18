"""Significance testing on top of the raw benchmark results.

A data profile is nice for a picture, but "MADS's curve is a little above
Ordered's curve" isn't a claim by itself - this runs the actual tests:

- Friedman test: are the four algorithms' per-instance ranks different at
  all, across the whole 35-instance suite?
- Wilcoxon signed-rank, MADS vs. each coordinate search variant: paired on
  instance_id, testing whether the optimality gap distributions differ.

Both operate on the optimality gap (final_f - f_star) rather than raw
final_f, since gaps are comparable across problems with wildly different
objective scales while raw values aren't.
"""

import numpy as np
import pandas as pd
from scipy import stats

from .profiles import compute_star_per_problem


def _gap_table(df):
    """instance_id x algo table of optimality gaps."""
    f_star = compute_star_per_problem(df)
    out = df.copy()
    out["gap"] = out["final_f"] - out["problem"].map(f_star)
    return out.pivot(index="instance_id", columns="algo", values="gap")


def friedman_test(df):
    """Friedman test across all algorithms present in df.

    Returns a dict with the test statistic, p-value, and each algorithm's
    average rank (lower rank = smaller gap = better).
    """
    gaps = _gap_table(df)
    ranks = gaps.rank(axis=1, method="average")
    statistic, p_value = stats.friedmanchisquare(*[gaps[c] for c in gaps.columns])
    return {
        "statistic": float(statistic),
        "p_value": float(p_value),
        "mean_rank": ranks.mean().to_dict(),
    }


def pairwise_wilcoxon(df, baseline="MADS"):
    """Wilcoxon signed-rank test, baseline vs. every other algorithm,
    paired by instance_id. One row per comparison.
    """
    gaps = _gap_table(df)
    others = [c for c in gaps.columns if c != baseline]

    rows = []
    for other in others:
        paired = gaps[[baseline, other]].dropna()
        diff = paired[baseline] - paired[other]
        if np.allclose(diff, 0.0):
            statistic, p_value = np.nan, 1.0
        else:
            statistic, p_value = stats.wilcoxon(paired[baseline], paired[other])
        rows.append({
            "comparison": f"{baseline} vs {other}",
            "n_pairs": len(paired),
            "median_gap_diff": float(diff.median()),
            "statistic": float(statistic) if statistic == statistic else np.nan,
            "p_value": float(p_value),
            f"{baseline}_better_count": int((diff < 0).sum()),
            f"{other}_better_count": int((diff > 0).sum()),
        })

    return pd.DataFrame(rows)


def summarize(df, baseline="MADS"):
    """Runs both tests and returns (friedman_dict, wilcoxon_dataframe)."""
    return friedman_test(df), pairwise_wilcoxon(df, baseline=baseline)
