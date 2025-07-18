import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde
from numpy.polynomial.polynomial import Polynomial
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score, mean_squared_error
from scipy import stats
import os

# Use relative path for data directory
filePath = os.path.join(os.path.dirname(__file__), "..", "data")
figuresPath = os.path.join(os.path.dirname(__file__), "..", "figures")

# Create figures directory if it doesn't exist
os.makedirs(figuresPath, exist_ok=True)

# Read the data
data = pd.read_csv(os.path.join(filePath, 'Centerline_4decades.csv'))

# Set global font properties for Nature style
plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 18
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['axes.linewidth'] = 0.5

# Helper function to format parameters with sign
def format_param(value,index=1):
    if index == 0:
        return f"{value:.2f}"
    return f"{value:.2f}" if value < 0 else f"+{value:.2f}"

# Define fitting functions
def linear_func(x, a, b):
    return a * x + b

# def exponential_func(x, a, b, c):
#     return a * np.exp(-b * x) + c
def exponential_func(x, a, c):
    return a * np.exp(-0.05 * x) + c

def power_func(x, a, b, c):
    return a * np.power(x + c, b)

def logarithmic_func(x, a, b):
    return a * np.log(x) + b  # Adjust to ensure valid log input

# Convert 'date' column to datetime and extract year and month for grouping
data['date'] = pd.to_datetime(data['date'])
data['year_month'] = data['date'].dt.to_period('M')
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month
# data = data[(data['month'] == 8) & (data['distance'] < 53) & (data['year']==2023)]
data = data[data['distance'] <= 52]

################################################################
# make another plot to fit a line for august in each decade
################################################################

# Define decades and months for the subplots
decades = [1990, 2000, 2010, 2020]
decadeLabels = ["1984-1994","1995-2004","2005-2014","2015-2023"]
months = [7, 8, 9]
month_names = ['July', 'August', 'September']

functions = {
    'Lin': linear_func,
    'Log': logarithmic_func,  
    'Poly': None,  # Placeholder for polynomial, handled separately
    'Exp': exponential_func,
    # 'Power': power_func      
}
# colors = ['blue', 'red', 'green', 'purple',  'black']#'orange',, 'goldenrod'
# colors = ['slategrey', 'mediumseagreen', 'royalblue', 'crimson']
colors = ['#4C72B0', '#55A868', '#B8860B', '#B44E9E']  # Muted color palette

# Create subplots
fig, axes = plt.subplots(len(decades), len(months), figsize=(16, 8), sharex=True)
legend_shown = False  # Flag to indicate legend has been shown
# Initialize storage for R-squared and RMSE values
results = {
    'Lin': {'r2': [], 'rmse': []},
    'Log': {'r2': [], 'rmse': []},
    'Poly': {'r2': [], 'rmse': []},
    'Exp': {'r2': [], 'rmse': []}
}

for i, decade in enumerate(decades):    
    ylabel = True
    # Filter data for the current decade
    for j, month in enumerate(months):
        filtered_data = data[(data['year'] >= decade) & (data['year'] < decade + 8) & (data['month'] == month)]        
        x = filtered_data['distance']+1
        y = filtered_data['pelagic']
        y_min, y_max = filtered_data['pelagic'].min(), filtered_data['pelagic'].max()

        # Skip the subplot if there's no data
        if x.empty or y.empty:
            axes[i, j].set_visible(False)
            continue

        sns.scatterplot(x=x, y=y, ax=axes[i, j], color='black', s=20, label='Data Points')

        annotations = []

        for k, (label, func) in enumerate(functions.items()):
            x_vals, y_vals = x, y
            
            try:                
                if label == 'Poly':
                    coeffs = np.polyfit(x, y, 2)
                    xp = np.linspace(x.min(), x.max(), 100)
                    axes[i, j].plot(xp, np.polyval(coeffs, xp), color=colors[k], lw=2, label=f'Polynomial Fit (Degree 2)')
                    y_fit = np.polyval(coeffs, x)
                    r2 = r2_score(y, y_fit)
                    rmse = np.sqrt(mean_squared_error(y, y_fit))
                    # Store R-squared and RMSE values
                    results[label]['r2'].append(r2)
                    results[label]['rmse'].append(rmse)
                    polynomial_equation = f"${coeffs[0]:.3f}x^2 {format_param(coeffs[1])}x {format_param(coeffs[2])}$"
                    annotations.append(f"{label}: {polynomial_equation} ({r2:.2f},{rmse:.2f})")
                    continue                
                
                params, covariance = curve_fit(func, x_vals, y_vals)#, p0=initial_params

                xp = np.linspace(x_vals.min(), x_vals.max(), 100)
                yp = func(xp, *params)
                axes[i, j].plot(xp, yp, color=colors[k], lw=2, label=f'{label} Fit')
                
                # Calculate R-squared and RMSE
                y_fit = func(x_vals, *params)
                r2 = r2_score(y_vals, y_fit)
                rmse = np.sqrt(mean_squared_error(y_vals, y_fit))

                # Store R-squared and RMSE values
                results[label]['r2'].append(r2)
                results[label]['rmse'].append(rmse)
                
                # Correctly format equations with LaTeX and sign handling
                if label == 'Lin':
                    equation = f"${format_param(params[0],0)}x {format_param(params[1])}$"
                elif label == 'Power':
                    equation = f"${format_param(params[0],0)}(x {format_param(params[2])})^{{{params[1]:.2f}}}$"
                elif label == 'Log':
                    equation = f"${format_param(params[0],0)}\\ln(x) {format_param(params[1])}$"
                elif label == 'Exp':
                    # equation = f"${format_param(params[0])}e^{{{-params[1]:.2f}x}} {format_param(params[2])}$"
                    equation = f"${format_param(params[0],0)}e^{{{-0.05}x}} {format_param(params[1])}$"
                
                annotations.append(f"{label}: {equation} ({r2:.2f},{rmse:.2f})")
                
            except RuntimeError as e:
                annotations.append(f"{label}: fit failed")
                print(f"{label} fit failed: {e}")

        # Annotate equations and metrics on each subplot
        for k, text in enumerate(annotations):
            axes[i, j].text(0.3, 0.97 - k * 0.1, text, transform=axes[i, j].transAxes, fontsize=10, 
                            color=colors[k], ha='left', va='top', fontweight='bold')        

        # # Set y-limits based on each decade's data range
        # axes[i, j].set_ylim(0, y_max)

        # # Show legend only on the first subplot where data is available
        # if not legend_shown:
        #     axes[i, j].legend(loc='upper right')
        #     legend_shown = True
        # else:
        #     axes[i, j].legend().set_visible(False)
        axes[i, j].legend().set_visible(False)

        # Only show the first column
        if ylabel:
            axes[i, j].set_ylabel(f'{decadeLabels[i]}', fontsize=12)
            ylabel = False
        else:
            axes[i, j].yaxis.label.set_visible(False)
        # Only show x-axis label on the bottom row
        if i == len(decades) - 1 and j == 1:
            axes[i, j].set_xlabel('Distance to West (km)', fontsize=12, fontweight='bold')
        else:
            axes[i, j].set_xlabel('')

        # axes[i, j].set_title(f'{decade}s, Month {month}')
        # only show the first row title
        if i == 0:
            # axes[i, j].set_title(f'Month {month}', fontsize=12)
            axes[i, j].set_title(month_names[j], fontsize=16, fontweight='bold')
        else:
            axes[i, j].set_title(None)

        axes[i, j].tick_params(axis='both', labelsize=12)  

# Shrink the gaps between columns
plt.subplots_adjust(wspace=0.1, hspace=0.15)

# Save the fitting analysis figure
plt.savefig(os.path.join(figuresPath, 'MonthlyCenterlineFitting_FigS4.png'), 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# Calculate mean, median, minimum, and maximum R-squared and RMSE for each fitting type
mean_results = {}
for label, metrics in results.items():
    mean_r2 = np.mean(metrics['r2']) if metrics['r2'] else None
    median_r2 = np.median(metrics['r2']) if metrics['r2'] else None
    # minimum
    min_r2 = np.min(metrics['r2']) if metrics['r2'] else None
    # maximum
    max_r2 = np.max(metrics['r2']) if metrics['r2'] else None

    mean_rmse = np.mean(metrics['rmse']) if metrics['rmse'] else None    
    median_rmse = np.median(metrics['rmse']) if metrics['rmse'] else None
    # minimum
    min_rmse = np.min(metrics['rmse']) if metrics['rmse'] else None
    # maximum
    max_rmse = np.max(metrics['rmse']) if metrics['rmse'] else None

    # print mean, median, min, max
    print(f"{label} Mean R²: {mean_r2}, Median R²: {median_r2}, Min R²: {min_r2}, Max R²: {max_r2}")
    print(f"{label} Mean RMSE: {mean_rmse}, Median RMSE: {median_rmse}, Min RMSE: {min_rmse}, Max RMSE: {max_rmse}")

    # print(f"{label} Mean R²: {mean_r2:.10f}, Median R²: {median_r2:.10f}, Min R²: {min_r2:.10f}, Mean RMSE: {mean_rmse:.10f}, Median RMSE: {median_rmse:.10f}, Min RMSE: {min_rmse:.10f}")

    mean_results[label] = {
        'mean_r2': mean_r2,
        'median_r2': median_r2,
        'min_r2': min_r2,
        'max_r2': max_r2,
        'mean_rmse': mean_rmse,
        'median_rmse': median_rmse,
        'min_rmse': min_rmse,
        'max_rmse': max_rmse
    }

# Create boxplots for R-squared and RMSE values
r2_data = {label: metrics['r2'] for label, metrics in results.items()}
rmse_data = {label: metrics['rmse'] for label, metrics in results.items()}

# Create a DataFrame for boxplotting
r2_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in r2_data.items()]))
rmse_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in rmse_data.items()]))

# Create combined plot for R-squared and RMSE
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5))

# R-squared boxplot
sns.boxplot(data=r2_df, ax=ax1, palette="Set2")
ax1.set_title('R²', fontsize=12)
ax1.grid(True)
# Add significance asterisks for R² over the upper whisker
for i in range(len(r2_df.columns)):
    q1 = r2_df.iloc[:, i].quantile(0.25)
    q3 = r2_df.iloc[:, i].quantile(0.75)
    iqr = q3 - q1
    upper_whisker = q3 + 1.5 * iqr
    
    # Filter outliers and get the max value
    non_outliers = r2_df.iloc[:, i][r2_df.iloc[:, i] <= upper_whisker]
    max_non_outlier = non_outliers.max()
    
    ax1.text(i, max_non_outlier-0.003, '***', ha='center', va='bottom', fontsize=12)

# RMSE boxplot
sns.boxplot(data=rmse_df, ax=ax2, palette="Set2")
ax2.set_title('RMSE', fontsize=12)
ax2.grid(True)
for i in range(len(rmse_df.columns)):
    q1 = rmse_df.iloc[:, i].quantile(0.25)
    q3 = rmse_df.iloc[:, i].quantile(0.75)
    iqr = q3 - q1
    upper_whisker = q3 + 1.5 * iqr
    
    # Filter outliers and get the max value
    non_outliers = rmse_df.iloc[:, i][rmse_df.iloc[:, i] <= upper_whisker]
    max_non_outlier = non_outliers.max()
    
    ax2.text(i, max_non_outlier-0.05, '***', ha='center', va='bottom', fontsize=12)

# Adjust layout
plt.tight_layout()

# Save the boxplot figure
plt.savefig(os.path.join(figuresPath, 'MonthlyCenterlineFitting_Fig5.png'), 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()