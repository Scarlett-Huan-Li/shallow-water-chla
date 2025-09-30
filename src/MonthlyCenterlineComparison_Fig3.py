import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
from matplotlib.patches import Rectangle
plt.rcParams['savefig.dpi'] = 300
# Nature-style: clean, minimalist, colorblind-friendly, with balanced font and line sizes
sns.set_theme(
    style="whitegrid",
    font_scale=1.1,  # reduced from 1.4
    rc={
        "axes.labelsize": 13,  # reduced from 18
        "axes.titlesize": 14,  # reduced from 18
        "axes.linewidth": 1,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.fontsize": 11,
        "font.family": 'sans-serif',
        "font.sans-serif": ['Arial']
    }
)

# Use relative path for data directory
filePath = os.path.join(os.path.dirname(__file__), "..", "data")
figuresPath = os.path.join(os.path.dirname(__file__), "..", "figures")

# Create figures directory if it doesn't exist
os.makedirs(figuresPath, exist_ok=True)

# Read the data
df = pd.read_csv(os.path.join(filePath, 'Centerline_4decades.csv'))

df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df = df.drop(columns=['north coast','south coast'])

years_to_plot = [1994, 2004, 2014, 2023]
basin_lines = [-5, 7, 21, 53]
basin_names = ['Basin I', 'Basin II', 'Basin III', 'Basin IV']
startYear = ['1984','1995','2005','2015']
monthLabel = ['Jul','Aug','Sept','Oct']
blue_rect_xy = [(-1, 46), (-1, 25), (-1, 27), (-1, 15)]
blue_rect_width = [15, 13, 11, 17]
blue_rect_height = [32, 11, 9, 20]

# Nature colorblind palette
palette = sns.color_palette("colorblind", 4)
month_colors = dict(zip(monthLabel, palette))
# line_styles = ['-', '--', '-.', ':']
line_styles = ['-', '-', '-', '-']

fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=False, dpi=200)  # reduced dpi from 300
axes = axes.flatten()
panel_labels = ['a', 'b', 'c', 'd']

for idx, (year, ax) in enumerate(zip(years_to_plot, axes)):
    df_year = df[(df['date'].dt.year == year) & ~df['date'].dt.month.isin([11,12,1,2,3,4,5,6])]
    df_part = df_year[['date', 'distance', 'pelagic']]
    for i, month in enumerate(sorted(df_part['date'].dt.month.unique())):
        label = monthLabel[i]
        color = month_colors[label]
        style = line_styles[i]
        df_month = df_part[df_part['date'].dt.month == month]
        ax.plot(df_month['distance'], df_month['pelagic'], label=label, color=color, linestyle=style, linewidth=1.5)  # thick line
    # Dotted rectangle (adjust coordinates as needed)
    if idx in [0, 1, 2, 3]:
        rect = Rectangle(blue_rect_xy[idx], blue_rect_width[idx], blue_rect_height[idx], linewidth=2, edgecolor='deepskyblue', facecolor='none', linestyle=(0, (2, 2)), alpha=0.8)
        ax.add_patch(rect)
    # Basin lines and annotation
    for line, name in zip(basin_lines, basin_names):
        ax.axvline(line, color='black', linestyle='--', linewidth=1) # ax.get_ylim()[1]-2
        if idx == 1:
            ax.annotate(name, xy=(line, 3), xytext=(line+1, 6),
                        textcoords='data', fontsize=10, ha='left', va='top', rotation=0, fontweight='bold', color='black')
    ax.text(0.98, 0.98, f'{panel_labels[idx]})', transform=ax.transAxes, fontsize=15, fontweight='bold', va='top', ha='right')
    ax.set_title(f'Decade {startYear[idx]} - {year}', pad=8)
    if idx > 1:
        ax.set_xlabel('Distance (km)')
    if idx % 2 == 0:
        ax.set_ylabel('Chl-a (μg/L)', fontstyle='italic')
    ax.set_xlim(-5, 80)  # Start x from less than 0
    ax.set_ylim(3, 80 if idx == 0 else 37)
    ax.tick_params(axis='both', which='major', length=5, width=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Legend outside last subplot
axes[3].legend(title='Month', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., frameon=False)

plt.tight_layout(rect=[0, 0.03, 0.95, 1])  # Add space at the bottom for x labels
plt.subplots_adjust(wspace=0.15, hspace=0.18, bottom=0.12)  # Increase bottom margin

# Save the figure
plt.savefig(os.path.join(figuresPath, 'MonthlyCenterlineComparison_Fig3.png'), 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
