"""
SpatioTemporal Asynchrony Analysis - Figure 4
============================================

This script generates Figure 4 showing spatiotemporal asynchrony in chlorophyll-a
concentrations across Lake Balaton during the summer months (July-September).

Output:
- SpatioTemporalAsynchrony_Fig4.png: Heatmap showing Chl-a patterns by distance and month
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import os

# Set up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir = os.path.join(project_dir, 'data')
figures_dir = os.path.join(project_dir, 'figures')

# Create figures directory if it doesn't exist
os.makedirs(figures_dir, exist_ok=True)

# Load data
df = pd.read_csv(os.path.join(data_dir, 'Centerline_4decades.csv'))

# Data preprocessing
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df = df.drop(columns=['north coast', 'south coast'])

# --- HEATMAP: Only July to September ---
df_heat = df[df['month'].isin([7, 8, 9])].copy()
df_heat['dist_bin'] = (df_heat['distance'] // 2) * 2
pivot = df_heat.groupby(['dist_bin', 'month'])['pelagic'].mean().unstack()

# Nature journal style settings
plt.rcParams.update({
    'axes.labelsize': 16,
    'axes.titlesize': 18,
    'axes.linewidth': 1.2,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 13,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial']
})

# Create figure
fig, ax = plt.subplots(figsize=(8, 3), dpi=300)
vmin = max(pivot.min().min(), 1e-2)
vmax = pivot.max().max()
norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)

# Heatmap
im = ax.imshow(
    pivot.T, aspect='auto', origin='lower',
    extent=[pivot.index.min(), pivot.index.max(), 7, 9],
    cmap='plasma',
    norm=norm
)

# Colorbar
cbar = fig.colorbar(im, ax=ax, pad=0.1, fraction=0.04)
cbar.ax.tick_params(labelsize=13)

# Axis labels and ticks
ax.set_ylabel('Month', fontsize=16, fontweight='bold')
ax.set_xlabel('Distance (km)', fontsize=16, fontweight='bold')
ax.set_yticks([7, 8, 9])
ax.set_yticklabels(['Jul', 'Aug', 'Sep'])
ax.set_title('Chl-a Asynchrony (μg/L)', fontsize=18, fontweight='bold', pad=12)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Overlay the difference plot
diff = pivot[9] - pivot[8]  # September minus August
ax2 = ax.twinx()
ax2.plot(pivot.index, diff, marker='o', color='black', linewidth=2, label='Sep - Aug')
ax2.set_ylabel('Chl-a (Sep - Aug)', fontsize=16, fontweight='bold', color='black', 
               rotation=-90, labelpad=11)
ax2.tick_params(axis='y', labelcolor='black', labelsize=14)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_linewidth(1.2)

# Add legend for the difference line
ax2.legend(loc='lower right', fontsize=13)

plt.tight_layout(rect=[0, 0, 1, 1])

# Save figure
output_file = os.path.join(figures_dir, 'SpatioTemporalAsynchrony_Fig4.png')
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Figure saved: {output_file}")

plt.show()

