"""
Transectional Overlay Analysis - Chl-a and Bathymetry
====================================================

This script generates a high-quality figure showing the transectional overlay
between chlorophyll-a concentration and water depth (bathymetry) across five
transects (I, II, III, IV-1, IV-2) from south to north in Lake Balaton.

Features:
- Five subplots showing Chl-a (red line) and Depth (blue line)
- Littoral zone boundaries marked at 2m depth (grey vertical lines)
- Professional styling matching scientific publication standards
- High-resolution output (300 DPI)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ============================================== CONFIGURATION ==============================================
plt.rcParams['savefig.dpi'] = 300

# Set global font properties
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13
plt.rcParams['legend.fontsize'] = 13
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0
plt.rcParams['xtick.minor.width'] = 0.8
plt.rcParams['ytick.minor.width'] = 0.8

# Use relative path for data directory
filePath = os.path.join(os.path.dirname(__file__), "..", "data")
figuresPath = os.path.join(os.path.dirname(__file__), "..", "figures")

# Create figures directory if it doesn't exist
os.makedirs(figuresPath, exist_ok=True)

# ============================================== DATA LOADING ==============================================
def load_transection_data():
    """Load all transection data files."""
    transections = {}
    transection_files = ['Transection_I.csv', 'Transection_II.csv', 'Transection_III.csv', 
                       'Transection_IV-1.csv', 'Transection_IV-2.csv']
    
    for file in transection_files:
        # Extract transection name from filename
        name = file.replace('Transection_', '').replace('.csv', '')
        
        # Load data
        df = pd.read_csv(os.path.join(filePath, file))
        
        # Rename columns for consistency (first column is distance)
        df.columns = ['distance', 'depth', 'chla']
        
        # Convert distance from meters to kilometers for better readability
        # Handle comma-separated numbers
        df['distance'] = df['distance'].astype(str).str.replace(',', '').astype(float) / 1000
        
        transections[name] = df
        
        print(f"Loaded {name}: {len(df)} points, distance range: {df['distance'].min():.1f}-{df['distance'].max():.1f} km")
    
    return transections

# ============================================== PLOTTING FUNCTIONS ==============================================
def create_transectional_figure(transections):
    """Create the main transectional overlay figure."""
    
    # Define subplot layout and labels
    transection_names = ['I', 'II', 'III', 'IV-1', 'IV-2']
    n_subplots = len(transection_names)
    
    # Create figure with subplots - optimized for visibility
    fig, axes = plt.subplots(n_subplots, 1, figsize=(10, 10), sharex=True)
    
    # Define colors and styles
    chla_color = '#E31A1C'  # Red
    depth_color = '#1F78B4'  # Blue
    littoral_color = '#666666'  # Grey
    littoral_style = '--'
    littoral_alpha = 0.8
    
    # Plot each transection
    for i, name in enumerate(transection_names):
        ax = axes[i]
        df = transections[name]
        
        # Create twin axis for depth
        ax2 = ax.twinx()
        
        # Plot Chl-a (left axis) - enhanced visibility
        line1 = ax.plot(df['distance'], df['chla'], color=chla_color, linewidth=2.5, label='Chl-a')
        
        # Plot Depth (right axis, negative values) - enhanced visibility
        line2 = ax2.plot(df['distance'], df['depth'], color=depth_color, linewidth=2.5, label='Depth')
        
        # Add littoral zone boundaries (where depth = -2m) - enhanced visibility
        littoral_positions = find_littoral_boundaries(df)
        for pos in littoral_positions:
            ax.axvline(x=pos, color=littoral_color, linestyle=littoral_style, alpha=littoral_alpha, linewidth=1.5)
        
        # Formatting - enhanced visibility
        ax.set_ylabel(r'$\mathit{Chl\text{-}a}$ (μg/L)', color=chla_color, fontweight='bold', fontsize=14)
        ax2.set_ylabel('Depth (m)', color=depth_color, fontweight='bold', fontsize=14, rotation=270, labelpad=20)
        
        # Set y-axis limits - different ranges for each subplot
        if name == 'I':
            ax.set_ylim(10, 45)
        elif name == 'II':
            ax.set_ylim(10, 45)
        elif name == 'III':
            ax.set_ylim(0, 40)
        elif name == 'IV-1':
            ax.set_ylim(0, 40)
        elif name == 'IV-2':
            ax.set_ylim(0, 40)
        
        ax2.set_ylim(-4.8, 0)
        
        # Add subplot label - enhanced visibility
        ax.text(0.5, 0.95, name, transform=ax.transAxes, fontsize=16, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none', alpha=0.9),
                ha='center', va='top')
        
        # Grid - enhanced visibility
        ax.grid(True, alpha=0.3, linewidth=0.5)
        
        # Color the y-axis labels and format ticks - enhanced visibility
        ax.tick_params(axis='y', labelcolor=chla_color, length=5, width=1.0, labelsize=13)
        ax2.tick_params(axis='y', labelcolor=depth_color, length=5, width=1.0, labelsize=13)
        ax.tick_params(axis='x', length=5, width=1.0, labelsize=13)
        
        # Remove top spine and format spines - enhanced visibility
        ax.spines['top'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.0)
        ax.spines['bottom'].set_linewidth(1.0)
        ax2.spines['right'].set_linewidth(1.0)
        ax2.spines['left'].set_visible(False)
    
    # Set common x-axis label - enhanced visibility
    axes[-1].set_xlabel('Transect from south to north (km)', fontweight='bold', fontsize=14)
    
    # Add legend to first subplot - enhanced visibility with correct line styles
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=chla_color, linewidth=2.5, label=r'$\mathit{Chl\text{-}a}$'),
        Line2D([0], [0], color=depth_color, linewidth=2.5, label='Depth'),
        Line2D([0], [0], color=littoral_color, linestyle=littoral_style, linewidth=1.5, alpha=littoral_alpha, label='Littoral')
    ]
    axes[0].legend(handles=legend_elements, loc='upper right', 
                   frameon=False, fontsize=13, labelspacing=1.2)
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.95, hspace=0.25)
    
    return fig

def find_littoral_boundaries(df, depth_threshold=-2.0):
    """Find positions where depth crosses the littoral threshold."""
    boundaries = []
    
    # Find where depth crosses -2m
    depth_crossings = np.where(np.diff(np.sign(df['depth'] - depth_threshold)))[0]
    
    for crossing in depth_crossings:
        if crossing < len(df) - 1:
            # Interpolate to find exact crossing point
            x1, x2 = df['distance'].iloc[crossing], df['distance'].iloc[crossing + 1]
            y1, y2 = df['depth'].iloc[crossing], df['depth'].iloc[crossing + 1]
            
            # Linear interpolation
            if y2 != y1:  # Avoid division by zero
                x_crossing = x1 + (depth_threshold - y1) * (x2 - x1) / (y2 - y1)
                boundaries.append(x_crossing)
    
    return boundaries

# ============================================== MAIN EXECUTION ==============================================
def main():
    """Main function to generate the transectional overlay figure."""
    print("Loading transection data...")
    transections = load_transection_data()
    
    print("Creating transectional overlay figure...")
    fig = create_transectional_figure(transections)
    
    # Save figure
    output_file = os.path.join(figuresPath, 'TransectionalOverlay_Fig8.png')
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Figure saved: {output_file}")
    
    plt.show()

if __name__ == "__main__":
    main()
