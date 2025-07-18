import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Rectangle

# Use relative path for data directory
filePath = os.path.join(os.path.dirname(__file__), "..", "data")
figuresPath = os.path.join(os.path.dirname(__file__), "..", "figures")

# Create figures directory if it doesn't exist
os.makedirs(figuresPath, exist_ok=True)

# Read the data
df = pd.read_csv(os.path.join(filePath, 'Centerline_4decades.csv'))
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df = df[df['month'] == 8]
df['year'] = df['date'].dt.year

years = df['year'].unique()

# Style and color setup (manual, to match previous plot)
plt.rcParams.update({
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'axes.linewidth': 1,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial']
})

basin_lines = [-5, 7, 21, 53]
basin_names = ['Basin I', 'Basin II', 'Basin III', 'Basin IV']
startYear = ['1984','1995','2005','2015']
panel_labels = ['a', 'b', 'c', 'd']
series_names = ['north coast', 'south coast', 'pelagic']
series_colors = ['#0072B2', '#D55E00', '#009E73']  # blue, orange, green (colorblind-friendly)
line_styles = ['-', '-', '-']

fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=False, dpi=200)
axes = axes.flatten()

for i, (year, ax) in enumerate(zip(years, axes)):
    year_data = df[df['year'] == year]
    for j, coast in enumerate(series_names):
        ax.plot(year_data['distance'], year_data[coast], label=coast.replace(' coast','').capitalize(),
                color=series_colors[j], linestyle=line_styles[j], linewidth=2.5)
    # Basin lines and annotation
    for k, (line, name) in enumerate(zip(basin_lines, basin_names)):
        ax.axvline(line, color='black', linestyle='--', linewidth=1)
        if i == 1:
            ax.annotate(name, xy=(line, 2), xytext=(line+1, 5),
                        textcoords='data', fontsize=10, ha='left', va='top', rotation=0, fontweight='bold', color='black')
    # Panel label
    ax.text(0.98, 0.98, f'{panel_labels[i]})', transform=ax.transAxes, fontsize=15, fontweight='bold', va='top', ha='right')
    ax.set_title(f'Decade {startYear[i]} - {year}', pad=8)
    if i > 1:
        ax.set_xlabel('Distance (km)')
        ax.set_ylim(2, 45)
    if i % 2 == 0:
        ax.set_ylabel('Chl-a (μg/L)')
    ax.set_xlim(-5, 80)
    ax.tick_params(axis='both', which='major', length=5, width=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Legend outside last subplot
axes[3].legend(title='Series', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., frameon=False)

plt.tight_layout(rect=[0, 0.03, 0.95, 1])
plt.subplots_adjust(wspace=0.15, hspace=0.18, bottom=0.12)

# Save the figure
plt.savefig(os.path.join(figuresPath, 'SouthNorthPelagicComparison_Fig7.png'), 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
