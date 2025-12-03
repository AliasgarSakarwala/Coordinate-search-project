"""
Generate plots for data profiles.
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_data_profile_evals(profile_df, output_path):
    """
    Plot standard data profile with x-axis = evaluation budget.
    
    Args:
        profile_df: DataFrame with columns: evals, Complete, Ordered, Opportunistic
        output_path: Path to save the plot
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(profile_df['evals'], profile_df['Complete'], 
             label='Complete', linewidth=2, marker='o', markersize=4)
    plt.plot(profile_df['evals'], profile_df['Ordered'], 
             label='Ordered', linewidth=2, marker='s', markersize=4)
    plt.plot(profile_df['evals'], profile_df['Opportunistic'], 
             label='Opportunistic', linewidth=2, marker='^', markersize=4)
    
    plt.xlabel('Evaluation Budget', fontsize=12)
    plt.ylabel('Fraction of Problems Solved', fontsize=12)
    plt.title('Data Profile: Evaluation Budget', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, profile_df['evals'].max())
    plt.ylim(0, 1.05)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_data_profile_time(profile_df, output_path):
    """
    Plot CPU-time data profile with x-axis = CPU time.
    
    Args:
        profile_df: DataFrame with columns: cpu_time, Complete, Ordered, Opportunistic
        output_path: Path to save the plot
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(profile_df['cpu_time'], profile_df['Complete'], 
             label='Complete', linewidth=2, marker='o', markersize=4)
    plt.plot(profile_df['cpu_time'], profile_df['Ordered'], 
             label='Ordered', linewidth=2, marker='s', markersize=4)
    plt.plot(profile_df['cpu_time'], profile_df['Opportunistic'], 
             label='Opportunistic', linewidth=2, marker='^', markersize=4)
    
    plt.xlabel('CPU Time (seconds)', fontsize=12)
    plt.ylabel('Fraction of Problems Solved', fontsize=12)
    plt.title('Data Profile: CPU Time', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.xlim(profile_df['cpu_time'].min(), profile_df['cpu_time'].max())
    plt.ylim(0, 1.05)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


