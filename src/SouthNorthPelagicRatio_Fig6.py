import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib as mpl
import numpy as np
import os

# Set the font family to Times New Roman
rc('font', family='serif')
rc('font', serif='Times New Roman')

# Nature journal style settings
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman']
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['legend.fontsize'] = 11
mpl.rcParams['axes.linewidth'] = 1.2
mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.direction'] = 'out'
mpl.rcParams['savefig.dpi'] = 200
mpl.rcParams['figure.dpi'] = 200

# Use relative path for data directory
filePath = os.path.join(os.path.dirname(__file__), "..", "data")
figuresPath = os.path.join(os.path.dirname(__file__), "..", "figures")

# Create figures directory if it doesn't exist
os.makedirs(figuresPath, exist_ok=True)

# Read the data
df = pd.read_csv(os.path.join(filePath, 'Centerline_4decades.csv'))
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df = df[df['month'] == 8]

# Create a new column 'basin' based on distance values
df['basin'] = pd.cut(df['distance'], bins=[0, 7, 21, 53, float('inf')], labels=['I', 'II', 'III', 'IV'])

# Calculate the percentage of coast to pelagic
df['north_coast_percentage'] = ((df['north coast'] ) / df['pelagic']) 
df['south_coast_percentage'] = ((df['south coast']) / df['pelagic']) 

# Map years to the desired labels
year_labels = {1994: '1984-1994', 2004: '1995-2004', 2014: '2005-2014', 2023: '2015-2023'}
df['year_label'] = df['year'].map(year_labels)

# Loop through each coastal region (north coast and south coast)
for i, coast_region in enumerate(['north_coast_percentage', 'south_coast_percentage']):
    # Calculate and print the mean values
    mean_values = df.groupby(['basin', 'year_label'])[coast_region].mean()
    print(f"Mean values for {coast_region}:\n{mean_values}\n")

sns.set(style="white", palette="colorblind")

# Set up subplots
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5), sharey=True)

flierprops = dict(markerfacecolor='gray', markeredgecolor='none', alpha=0.5, markersize=3)

# Boxplot for north coast
sns.boxplot(
    x='year_label', y='north_coast_percentage', hue='basin', data=df, ax=axes[0],
    palette='colorblind', linewidth=1, width=0.6, fliersize=3, flierprops=flierprops
)
axes[0].set_title('North Littoral Region', fontsize=16, weight='semibold', pad=8)
axes[0].set_ylabel('Ratio of Littoral by Pelagic Chl-a', fontsize=14, labelpad=10)
axes[0].set_xlabel('')
axes[0].legend(title='Basin', loc='upper left', bbox_to_anchor=(0.01, 0.99), frameon=False, fontsize=11, title_fontsize=11)
axes[0].text(0.01, 0.97, 'A', transform=axes[0].transAxes, fontsize=16, fontweight='bold', va='top', ha='left', bbox=dict(facecolor='white', edgecolor='none', pad=1.5))

# Boxplot for south coast
sns.boxplot(
    x='year_label', y='south_coast_percentage', hue='basin', data=df, ax=axes[1],
    palette='colorblind', linewidth=1, width=0.6, fliersize=3, flierprops=flierprops
)
axes[1].set_title('South Littoral Region', fontsize=16, weight='semibold', pad=8)
axes[1].set_ylabel('')
axes[1].set_xlabel('')
axes[1].legend_.remove()  # Remove duplicate legend
axes[1].text(0.01, 0.97, 'B', transform=axes[1].transAxes, fontsize=16, fontweight='bold', va='top', ha='left', bbox=dict(facecolor='white', edgecolor='none', pad=1.5))

# Remove top and right spines, set only left and bottom
for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)
    ax.grid(False)
    ax.set_facecolor('white')
    ax.tick_params(axis='both', which='both', length=5, width=1.2)

# Place legend inside first plot
axes[0].legend(title='Basin', loc='upper left', bbox_to_anchor=(0.02, 0.98), frameon=False)

plt.subplots_adjust(wspace=0.08)
plt.tight_layout(pad=1)

# Save the figure
plt.savefig(os.path.join(figuresPath, 'SouthNorthPelagicRatio_Fig6.png'), 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
