"""Plotting helpers for the data profiles."""

import matplotlib.pyplot as plt

_MARKERS = {"Complete": "o", "Ordered": "s", "Opportunistic": "^", "MADS": "d"}


def _plot_series(profile_df, x_col):
    for algo in profile_df.columns:
        if algo == x_col:
            continue
        plt.plot(
            profile_df[x_col], profile_df[algo],
            label=algo, linewidth=2,
            marker=_MARKERS.get(algo, "x"), markersize=4,
        )


def plot_data_profile_evals(profile_df, output_path):
    """profile_df needs an 'evals' column plus one column per algorithm."""
    plt.figure(figsize=(10, 6))
    _plot_series(profile_df, "evals")
    plt.xlabel("Evaluation Budget", fontsize=12)
    plt.ylabel("Fraction of Problems Solved", fontsize=12)
    plt.title("Data Profile: Evaluation Budget", fontsize=14, fontweight="bold")
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, profile_df["evals"].max())
    plt.ylim(0, 1.05)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_data_profile_time(profile_df, output_path):
    """profile_df needs a 'cpu_time' column plus one column per algorithm."""
    plt.figure(figsize=(10, 6))
    _plot_series(profile_df, "cpu_time")
    plt.xlabel("CPU Time (seconds)", fontsize=12)
    plt.ylabel("Fraction of Problems Solved", fontsize=12)
    plt.title("Data Profile: CPU Time", fontsize=14, fontweight="bold")
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale("log")
    plt.xlim(profile_df["cpu_time"].min(), profile_df["cpu_time"].max())
    plt.ylim(0, 1.05)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_convergence(traces, output_path, title="Convergence"):
    """traces: dict of algo_name -> (evals_array, gap_array). Log-scale y."""
    plt.figure(figsize=(9, 6))
    for algo, (evals, gap) in traces.items():
        plt.plot(evals, gap, label=algo, linewidth=2, marker=_MARKERS.get(algo, "x"), markersize=3)
    plt.xlabel("Function Evaluations", fontsize=12)
    plt.ylabel("Optimality Gap (log scale)", fontsize=12)
    plt.yscale("log")
    plt.title(title, fontsize=14, fontweight="bold")
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, which="both")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
