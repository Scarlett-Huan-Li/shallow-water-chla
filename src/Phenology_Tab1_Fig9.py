"""
Phenology Analysis: Peak DOY Temporal Trend Testing
==================================================

This script performs statistical analysis of peak Day of Year (DOY) trends across four decades
(1984-2023) for chlorophyll-a concentration in Lake Balaton. The analysis includes:

1. Data preprocessing and outlier correction
2. Standard linear regression (using decade means)
3. Weighted linear regression (using individual measurements with uncertainty)
4. Mann-Kendall test with Sen's slope (non-parametric)

The script is designed for scientific replication and includes clear documentation
of all statistical methods and assumptions.
"""

import pandas as pd
from scipy.interpolate import make_interp_spline,CubicSpline,interp1d
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema,savgol_filter
import matplotlib.colors as mcolors
import os

# Use relative path for data directory
filePath = os.path.join(os.path.dirname(__file__), "..", "data")
figuresPath = os.path.join(os.path.dirname(__file__), "..", "figures")

# Create figures directory if it doesn't exist
os.makedirs(figuresPath, exist_ok=True)

# Read the CSV file
df = pd.read_csv(os.path.join(filePath, 'Landsat_1984_2024_stations.csv'), parse_dates=['date'])
df['doy'] = df['date'].dt.dayofyear

# Calculate the sliding window average for the 'chla' column
window_size = 30  # Adjust the window size as needed
# Savitzky-Golay smoothing
smooth_window = 15
window_size_smooth = 15
poly_order = 3
# bootstrap
uncert_window = 20
num_bootstrap_samples = 1000

# Define the conditions for filtering the DataFrame
conditions = [df['date'].dt.year < 1995,
              (df['date'].dt.year > 1994) & (df['date'].dt.year < 2005),
              (df['date'].dt.year > 2004) & (df['date'].dt.year < 2015),
              (df['date'].dt.year > 2014) & (df['date'].dt.year < 2024)]

# Collect results for summary plots
results = []
for i, condition in enumerate(conditions):
    print("//////////////////////////{}".format(i+1))
    df_filtered = df[condition]
    for basin in ['Bfuzfo','Tihany','Zanka','Szigliget','Keszthely']:
        basin_data = df_filtered[df_filtered['Basin'] == basin]
        if len(basin_data) == 0:
            continue
        basin_data = basin_data.groupby(['doy'])['chla'].mean().reset_index().dropna(subset=['chla'])
        basin_data.set_index('doy', inplace=True)
        basin_data_daily = basin_data.reindex(list(range(1,365))).reset_index()
        temp_data_daily = basin_data_daily.dropna()
        cs = interp1d(temp_data_daily['doy'], temp_data_daily['chla'], kind='linear')
        x = np.clip(basin_data_daily['doy'], temp_data_daily['doy'].min(), temp_data_daily['doy'].max())
        basin_data_daily['chla'] = cs(x)
        basin_data_daily = basin_data_daily[150:290]
        basin_data_daily['chla_avg'] = basin_data_daily['chla'].rolling(window=window_size, center=True, min_periods=1).mean()

        # --- Compute SOS (Start of Season) ---
        may_oct_mask = (basin_data_daily['doy'] >= 120) & (basin_data_daily['doy'] <= 304)
        data_may_oct = basin_data_daily[may_oct_mask]
        min_chla = data_may_oct['chla_avg'].min()
        max_chla = data_may_oct['chla_avg'].max()
        amplitude = max_chla - min_chla
        threshold = min_chla + 0.2 * amplitude
        sos_candidates = data_may_oct[data_may_oct['chla_avg'] > threshold]
        if not sos_candidates.empty:
            sos = sos_candidates['doy'].iloc[0]
        else:
            sos = None

        # --- Bootstrap SOS uncertainty ---
        bootstrap_sos = []
        for _ in range(num_bootstrap_samples):
            sample = data_may_oct.sample(frac=1, replace=True)
            sample = sample.sort_values('doy')
            chla_smooth = sample['chla_avg'].rolling(window=window_size, center=True, min_periods=1).mean()
            min_chla_b = chla_smooth.min()
            max_chla_b = chla_smooth.max()
            amplitude_b = max_chla_b - min_chla_b
            threshold_b = min_chla_b + 0.2 * amplitude_b
            sos_candidates_b = sample[sample['chla_avg'] > threshold_b]
            if not sos_candidates_b.empty:
                sos_boot = sos_candidates_b['doy'].iloc[0]
                bootstrap_sos.append(sos_boot)
        sos_std = np.std(bootstrap_sos) if bootstrap_sos else None

        # --- Compute AUC (area under curve from SOS to end of October) ---
        if sos is not None:
            auc_mask = (data_may_oct['doy'] >= sos) & (data_may_oct['doy'] <= 304)
            auc = np.trapezoid(data_may_oct[auc_mask]['chla_avg'], data_may_oct[auc_mask]['doy'])
        else:
            auc = None

        # Find the peak DOY and its value
        peak_index = np.argmax(basin_data_daily['chla_avg'])
        peak_doy = basin_data_daily['doy'].iloc[peak_index]
        peak_value = basin_data_daily['chla_avg'].iloc[peak_index]

        # bootstrap
        dates = basin_data_daily['doy']
        start_index = max(0, peak_index - uncert_window)
        end_index = min(len(dates), peak_index + uncert_window + 1)
        dates_window = dates[start_index:end_index]
        data_window = basin_data_daily[start_index:end_index]
        bootstrap_samples = [np.random.choice(dates_window, size=len(dates_window)//2, replace=False) for _ in range(num_bootstrap_samples)]
        bootstrap_median_dates = [data_window['doy'].iloc[np.argmax(data_window[data_window['doy'].isin(sample)]['chla_avg'])] for sample in bootstrap_samples]
        std2 = 2 * np.std(bootstrap_median_dates)

        # Print all metrics together: decade, basin, peak_doy, peak_value, std2, sos, amplitude, auc, sos_std
        print("{:<3}{:<12}{:<8}{:<20}{:<20}{:<5}{:<20}{:<20}{:<20}".format(i+1, basin, peak_doy, peak_value, std2, sos if sos is not None else 'NA', amplitude if amplitude is not None else 'NA', auc if auc is not None else 'NA', sos_std if sos_std is not None else 'NA'))

        # Collect results for summary plot
        results.append({
            'decade': i+1,
            'basin': basin,
            'peak_doy': peak_doy,
            'peak_value': peak_value,
            'std2': std2,
            'sos': sos,
            'sos_std': sos_std,
            'amplitude': amplitude,
            'auc': auc
        })

# --- After the main loop: summary plots ---
import pandas as pd
results_df = pd.DataFrame(results)

# Calculate mean SOS values for each decade (for internal use)

# ===== STATISTICAL ANALYSIS: TEMPORAL TREND TESTING =====
print("\n" + "="*60)
print("STATISTICAL ANALYSIS: TEMPORAL TREND TESTING FOR PEAK DOY")
print("="*60)

from scipy import stats
from scipy.stats import kendalltau

# ============================================== DATA PREPARATION ==============================================
# Extract the actual peak DOY values from the results
decade_labels = ['1984-1994', '1995-2004', '2005-2014', '2015-2023']

# Replace the outlier: Station III (Zanka) value 279 in decade 4 (2015-2023) with in-situ value 246±3.2
results_df_filtered = results_df.copy()
outlier_mask = (results_df_filtered['basin'] == 'Zanka') & (results_df_filtered['decade'] == 4) & (results_df_filtered['peak_doy'] == 279)
results_df_filtered.loc[outlier_mask, 'peak_doy'] = 246
results_df_filtered.loc[outlier_mask, 'std2'] = 3.2

# Prepare decade-wise statistics for analysis
decade_groups = []
for decade in sorted(results_df_filtered['decade'].unique()):
    decade_data = results_df_filtered[results_df_filtered['decade'] == decade]['peak_doy'].dropna()
    decade_groups.append(decade_data.values)

# ============================================== TREND ANALYSIS METHODS ==============================================

# --- METHOD 1: STANDARD LINEAR REGRESSION ---

# Calculate mean DOY for each decade (using filtered data)
mean_doy_values = []
years = [1989, 1999, 2009, 2019]  # Mid-years of each decade

for decade in sorted(results_df_filtered['decade'].unique()):
    decade_data = results_df_filtered[results_df_filtered['decade'] == decade]['peak_doy'].dropna()
    if not decade_data.empty:
        mean_doy = decade_data.mean()
        mean_doy_values.append(mean_doy)

# Standard (unweighted) regression
if len(mean_doy_values) == len(years):
    print(f"--- METHOD 1: STANDARD LINEAR REGRESSION ---")
    slope, intercept, r_value, p_value_reg, std_err = stats.linregress(years, mean_doy_values)
    
    # print(f"Linear regression: Peak DOY = {intercept:.1f} + {slope:.3f} × Year")
    print(f"Slope: {slope:.3f} DOY/year")
    print(f"R^2: {r_value**2:.3f}")
    print(f"p-value: {p_value_reg:.6f}")
    
    if p_value_reg < 0.05:
        trend_direction = "advancing" if slope < 0 else "delaying"
        print(f"Result: SIGNIFICANT temporal trend (p < 0.05)")
        print(f"Peak DOY is {trend_direction} by {abs(slope):.2f} days per year")
    else:
        print(f"Result: NO significant temporal trend (p ≥ 0.05)")

# --- METHOD 2: WEIGHTED LINEAR REGRESSION ---

# Prepare data for weighted regression using std2 as uncertainty
all_years = []
all_doys = []
all_weights = []

for _, row in results_df_filtered.iterrows():
    decade = row['decade']
    doy = row['peak_doy']
    std2 = row['std2']
    
    if pd.notna(doy) and pd.notna(std2):
        # Use mid-year of each decade
        mid_year = [1989, 1999, 2009, 2019][decade-1]
        all_years.append(mid_year)
        all_doys.append(doy)
        # Weight is inverse of variance (1/std2^2)
        all_weights.append(1.0 / (std2**2))

# Calculate mean DOY for each decade (using filtered data) for comparison
mean_doy_values = []
years = [1989, 1999, 2009, 2019]  # Mid-years of each decade

for decade in sorted(results_df_filtered['decade'].unique()):
    decade_data = results_df_filtered[results_df_filtered['decade'] == decade]['peak_doy'].dropna()
    if not decade_data.empty:
        mean_doy = decade_data.mean()
        mean_doy_values.append(mean_doy)

# Standard (unweighted) regression for comparison
if len(mean_doy_values) == len(years):
    slope, intercept, r_value, p_value_reg, std_err = stats.linregress(years, mean_doy_values)
    
    # print(f"Standard linear regression: Peak DOY = {intercept:.1f} + {slope:.3f} × Year")
    print(f"Slope: {slope:.3f} DOY/year")
    print(f"R^2: {r_value**2:.3f}")
    print(f"p-value: {p_value_reg:.6f}")
    
    if p_value_reg < 0.05:
        trend_direction = "advancing" if slope < 0 else "delaying"
        print(f"Result: SIGNIFICANT temporal trend (p < 0.05)")
        print(f"Peak DOY is {trend_direction} by {abs(slope):.2f} days per year")
    else:
        print(f"Result: NO significant temporal trend (p ≥ 0.05)")

# Weighted regression using all individual measurements
if len(all_years) >= 4:
    print(f"\n--- METHOD 2: WEIGHTED LINEAR REGRESSION (using individual measurements with uncertainty) ---")
    
    # Perform weighted least squares regression
    from scipy.optimize import curve_fit
    
    def linear_func(x, a, b):
        return a * x + b
    
    # Convert to numpy arrays
    years_array = np.array(all_years)
    doys_array = np.array(all_doys)
    weights_array = np.array(all_weights)
    
    # Perform weighted regression
    popt, pcov = curve_fit(linear_func, years_array, doys_array, sigma=1/np.sqrt(weights_array), absolute_sigma=True)
    slope_weighted, intercept_weighted = popt
    
    # Calculate R-squared for weighted regression
    y_pred = linear_func(years_array, slope_weighted, intercept_weighted)
    ss_res = np.sum(weights_array * (doys_array - y_pred)**2)
    ss_tot = np.sum(weights_array * (doys_array - np.average(doys_array, weights=weights_array))**2)
    r_squared_weighted = 1 - (ss_res / ss_tot)
    
    # Calculate p-value using t-test
    n = len(all_years)
    dof = n - 2
    slope_std = np.sqrt(pcov[0, 0])
    t_stat = slope_weighted / slope_std
    p_value_weighted = 2 * (1 - stats.t.cdf(abs(t_stat), dof))
    
    # print(f"Weighted linear regression: Peak DOY = {intercept_weighted:.1f} + {slope_weighted:.3f} × Year")
    print(f"Slope: {slope_weighted:.3f} DOY/year")
    print(f"R^2: {r_squared_weighted:.3f}")
    print(f"p-value: {p_value_weighted:.6f}")
    print(f"Number of measurements: {n}")
    
    if p_value_weighted < 0.05:
        trend_direction = "advancing" if slope_weighted < 0 else "delaying"
        print(f"Result: SIGNIFICANT temporal trend (p < 0.05)")
        print(f"Peak DOY is {trend_direction} by {abs(slope_weighted):.2f} days per year")
    else:
        print(f"Result: NO significant temporal trend (p ≥ 0.05)")
    

# --- METHOD 3: MANN-KENDALL TEST WITH SEN'S SLOPE ---

if len(mean_doy_values) == len(years):
    print(f"\n--- METHOD 3: MANN-KENDALL TEST WITH SEN'S SLOPE ---")
    # Mann-Kendall test for trend significance
    tau, p_mk = kendalltau(years, mean_doy_values)
    
    # Calculate Sen's slope estimator (non-parametric slope)
    def sens_slope(x, y):
        """
        Calculate Sen's slope estimator for trend analysis.
        This is the median of all pairwise slopes, making it robust to outliers.
        """
        n = len(x)
        slopes = []
        for i in range(n):
            for j in range(i+1, n):
                if x[j] != x[i]:  # Avoid division by zero
                    slope = (y[j] - y[i]) / (x[j] - x[i])
                    slopes.append(slope)
        return np.median(slopes)
    
    sen_slope = sens_slope(years, mean_doy_values)
    
    print(f"Mann-Kendall tau: {tau:.3f}")
    print(f"p-value: {p_mk:.6f}")
    print(f"Sen's slope: {sen_slope:.3f} DOY/year")
    
    # Check significance at different levels
    sig_5pct = p_mk < 0.05
    sig_10pct = p_mk < 0.10
    
    print(f"Significance levels:")
    print(f"  5% level (p < 0.05): {'SIGNIFICANT' if sig_5pct else 'NOT significant'} (p = {p_mk:.6f})")
    print(f"  10% level (p < 0.10): {'SIGNIFICANT' if sig_10pct else 'NOT significant'} (p = {p_mk:.6f})")
    
    if sig_5pct:
        trend_direction = "advancing" if sen_slope < 0 else "delaying"
        print(f"Result: SIGNIFICANT temporal trend at 5% level (p < 0.05)")
        print(f"Peak DOY shows {trend_direction} trend by {abs(sen_slope):.3f} DOY/year")
    elif sig_10pct:
        trend_direction = "advancing" if sen_slope < 0 else "delaying"
        print(f"Result: SIGNIFICANT temporal trend at 10% level (p < 0.10)")
        print(f"Peak DOY shows {trend_direction} trend by {abs(sen_slope):.3f} DOY/year")
    else:
        print(f"Result: NO significant temporal trend (p ≥ 0.10)")
        print(f"Sen's slope: {sen_slope:.3f} DOY/year (not significant)")

# ============================================== SUMMARY PLOT ==============================================


basin_labels = ['I', 'II', 'III', 'IV-1', 'IV-2']
basins = ['Keszthely','Szigliget','Zanka','Tihany','Bfuzfo']
decades = sorted(results_df['decade'].unique())
decade_labels = ['1984-1994', '1995-2004', '2005-2014', '2015-2023']
bar_width = 0.13
x = np.arange(len(decades))

# Nature journal style
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'axes.labelsize': 16,
    'axes.titlesize': 18,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'axes.spines.top': False,
    'axes.spines.right': False
})

# Use a colorblind-friendly palette
pastel1_colors = plt.get_cmap('Pastel1').colors
# Pick 5 visually distinct colors from Pastel1
basin_colors = ['#0000FF', '#22B14C', '#9E003A', '#FF8C32', '#A2DBF6']

fig, axs = plt.subplots(2, 2, figsize=(8, 6))
param_names = ['peak_doy', 'sos', 'amplitude', 'auc']
titles = ['Peak DOY', 'Start of Season (SOS)', 'Amplitude', 'AUC']
subplot_labels = ['a)', 'b)', 'c)', 'd)']

for idx, (param, title) in enumerate(zip(param_names, titles)):
    ax = axs.flat[idx]
    for j, basin in enumerate(basins):
        subset = results_df[results_df['basin'] == basin]
        subset = subset.set_index('decade').reindex(decades)
        values = subset[param].values
        # Error bars: only for peak_doy and sos
        if param == 'peak_doy':
            errors = subset['std2'].values
        elif param == 'sos':
            errors = subset['sos_std'].values
        else:
            errors = None
        
        # Plot all bars normally
        bars = ax.bar(
            x + j*bar_width, values, width=bar_width, label=basin_labels[j],
            color=basin_colors[j], yerr=errors, capsize=4, alpha=0.85, 
            edgecolor='#888888', ecolor='#888888'
        )
        
        # Special handling for Peak DOY: modify Zanka bar in decade 4
        if param == 'peak_doy' and basin == 'Zanka':
            # The 4th bar (index 3) corresponds to decade 4
            bars[3].set_alpha(0.4)
            bars[3].set_hatch('///')
    
    # Add mean SOS trend line for SOS subplot
    if param == 'sos':
        mean_sos_values = []
        mean_sos_x = []
        for i, decade in enumerate(decades):
            decade_data = results_df[results_df['decade'] == decade]['sos'].dropna()
            if not decade_data.empty:
                mean_sos = decade_data.mean()
                mean_sos_values.append(mean_sos)
                mean_sos_x.append(x[i] + bar_width * (len(basins)-1)/2)  # Center of the decade group
        if len(mean_sos_values) > 1:
            ax.plot(mean_sos_x, mean_sos_values, color='red', linestyle='--', linewidth=2, marker='o', markersize=6, label='Mean SOS trend')
    
    ax.set_title(title, fontsize=18, fontweight='bold')
    ax.set_ylabel(param, fontsize=16)
    # Add subplot label
    ax.text(0, 1.1, subplot_labels[idx], transform=ax.transAxes, fontsize=18, fontweight='bold', va='top', ha='left')
    # Only show x-axis labels on the last row
    if idx >= 2:
        ax.set_xticks(x + bar_width * (len(basins)-1)/2)
        ax.set_xticklabels(decade_labels, rotation=0)
        ax.set_xlabel('Year', fontsize=16)
    else:
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_xlabel('')
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    # Remove legend except for last subplot
    if idx != 2:
        ax.legend().set_visible(False)
    else:
        ax.legend(title='', loc='upper right', frameon=False)
    # Adjust y-limits for first row
    if idx == 0:
        ax.set_ylim(200, 310)  # Adjust as needed for your data
    if idx == 1:
        ax.set_ylim(160, 210)  # Adjust as needed for your data
    # Nature style: remove top/right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.subplots_adjust(wspace=0.15)

# Save the figure
figure_path = os.path.join(figuresPath, 'Phenology_Tab1_Fig9.png')
plt.savefig(figure_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\nFigure saved to: {figure_path}")
plt.show()  # Display the phenology plot