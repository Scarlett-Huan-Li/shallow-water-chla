"""
Monthly Centerline Fitting Analysis - Single Plot
================================================

This script generates a single plot showing curve fitting analysis for chlorophyll-a
concentration along the centerline of Lake Balaton for a specific decade and month.
This is used for Figure 5 left subplot in the manuscript.

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score, mean_squared_error
import os

# Use relative path for data directory
filePath = os.path.join(os.path.dirname(__file__), "..", "data")
figuresPath = os.path.join(os.path.dirname(__file__), "..", "figures")

# Create figures directory if it doesn't exist
os.makedirs(figuresPath, exist_ok=True)

# Read the data
data = pd.read_csv(os.path.join(filePath, 'Centerline_4decades.csv'))

# ============================================== CONFIGURATION ==============================================
plt.rcParams['savefig.dpi'] = 300

# Set global font properties for Nature style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 18
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['axes.linewidth'] = 0.5

# ============================================== DATA PROCESSING ==============================================
def format_param(value, index=1):
    """Format parameters with proper sign handling for equations."""
    if index == 0:
        return f"{value:.2f}"
    return f"{value:.2f}" if value < 0 else f"+{value:.2f}"

# Convert 'date' column to datetime and extract year and month for grouping
data['date'] = pd.to_datetime(data['date'])
data['year_month'] = data['date'].dt.to_period('M')
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month
data = data[data['distance'] <= 52]

# ============================================== FITTING FUNCTIONS ==============================================
def linear_func(x, a, b):
    """Linear function: y = ax + b"""
    return a * x + b

def exponential_func(x, a, b, c):
    """Exponential function: y = a*exp(-b*x) + c"""
    return a * np.exp(-b * x) + c

def power_func(x, a, b, c):
    """Power function: y = a*(x + c)^b"""
    return a * np.power(x + c, b)

def logarithmic_func(x, a, b):
    """Logarithmic function: y = a*ln(x+1) + b"""
    return a * np.log(x + 1) + b

# ============================================== MAIN ANALYSIS ==============================================
def main():
    """Main analysis function for single curve fitting plot."""
    # Define the decade and month for analysis
    decade_start = 2015  # 2015-2023 decade
    month = 7  # July
    
    # Filter data for the specified decade and month
    filtered_data = data[(data['year'] >= decade_start) & (data['month'] == month)]
    
    x = filtered_data['distance'] + 1
    y = filtered_data['pelagic']
    
    return x, y, decade_start, month

# ============================================== PLOTTING ==============================================
def create_single_fitting_plot(x, y, decade_start, month):
    """Create single curve fitting plot."""
    # Define fitting functions
    functions = {
        'Lin': linear_func,
        'Log': logarithmic_func,  
        'Poly': None,  # Placeholder for polynomial, handled separately
        'Exp': exponential_func,
    }
    
    # Define colors for different fits
    colors = ['#4C72B0', '#55A868', '#B8860B', '#B44E9E'] 
    
    # Create the plot
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x=x, y=y, color='black', s=30, label='Data Points')
    
    annotations = []
    
    for i, (label, func) in enumerate(functions.items()):
        x_vals, y_vals = x, y
        
        try:
            if label == 'Poly':
                # Polynomial fit separately
                coeffs = np.polyfit(x, y, 2)
                xp = np.linspace(x_vals.min(), x_vals.max(), 100)
                plt.plot(xp, np.polyval(coeffs, xp), color=colors[i], lw=3, label=f'Polynomial Fit (Degree 2)')
                y_fit = np.polyval(coeffs, x)
                r2 = r2_score(y, y_fit)
                rmse = np.sqrt(mean_squared_error(y, y_fit))
                polynomial_equation = f"${format_param(coeffs[0],0)}x^2 {format_param(coeffs[1])}x {format_param(coeffs[2])}$"
                annotations.append(f"Poly: {polynomial_equation}, $R^2$={r2:.2f}, RMSE={rmse:.2f}")
                continue
            else:
                initial_params = [0, np.mean(y_vals)]
            
            params, _ = curve_fit(func, x_vals, y_vals)
            xp = np.linspace(x_vals.min(), x_vals.max(), 100)
            yp = func(xp, *params)
            plt.plot(xp, yp, color=colors[i], lw=3, label=f'{label} Fit')
            
            # Calculate R-squared and RMSE
            y_fit = func(x_vals, *params)
            r2 = r2_score(y_vals, y_fit)
            rmse = np.sqrt(mean_squared_error(y_vals, y_fit))
            
            # Format equations with LaTeX and sign handling
            if label == 'Lin':
                equation = f"${format_param(params[0],0)}x {format_param(params[1])}$"
            elif label == 'Power':
                equation = f"${format_param(params[0],0)}(x {format_param(params[2])})^{{{params[1]:.2f}}}$"
            elif label == 'Log':
                equation = f"${format_param(params[0],0)}\\ln(x+1) {format_param(params[1])}$"
            elif label == 'Exp':
                equation = f"${format_param(params[0],0)}e^{{{-params[1]:.2f}x}} {format_param(params[2])}$"
            
            annotations.append(f"{label}: {equation}, $R^2$={r2:.2f}, RMSE={rmse:.2f}")
            
        except RuntimeError as e:
            print(f"{label} fit failed: {e}")
    
    # Annotate equations and metrics on the plot
    for k, text in enumerate(annotations):
        plt.text(0.1, 0.97 - k * 0.06, text, transform=plt.gca().transAxes, fontsize=13, 
                        color=colors[k], ha='left', va='top', fontweight='bold') 
    
    # Set labels and title
    plt.xlabel('Distance to West (km)')
    plt.ylabel('Chl-a (μg/L)', style='italic')
    plt.title(f'Fitted July Chl-a for the Decade {decade_start}-2023')
    plt.legend(loc='lower left', ncol=1, fontsize=12, frameon=False)
    plt.grid(True, linewidth=1.0, alpha=0.7)
    
    plt.tight_layout()
    
    # Save the figure
    figure_path = os.path.join(figuresPath, 'MonthlyCenterlineFitting_Fig5_left.png')
    plt.savefig(figure_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Figure saved to: {figure_path}")
    plt.show()

# ============================================== EXECUTION ==============================================
if __name__ == "__main__":
    # Run main analysis
    x, y, decade_start, month = main()
    
    # Create single fitting plot
    create_single_fitting_plot(x, y, decade_start, month)
