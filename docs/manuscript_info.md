# Manuscript Information

## Title
[Your manuscript title here]

## Authors
[Author list]

## Journal
[Target journal name]

## Abstract
[Brief description of the study]

## Key Figures and Tables

### Figure 3: Monthly Centerline Comparison
- **Script**: `src/MonthlyCenterlineComparison_Fig3.py`
- **Data**: `data/Centerline_4decades.csv`
- **Output**: `figures/MonthlyCenterlineComparison_Fig3.png`
- **Description**: [Brief description of what this figure shows]

### Figure 5: Monthly Centerline Fitting
- **Script**: `src/MonthlyCenterlineFitting_FigS4_Fig5.py`
- **Data**: `data/Centerline_4decades.csv`
- **Output**: `figures/MonthlyCenterlineFitting_Fig5.png`
- **Description**: [Brief description of what this figure shows]

### Figure S4: Fitting Statistics Boxplots
- **Script**: `src/MonthlyCenterlineFitting_FigS4_Fig5.py`
- **Data**: `data/Centerline_4decades.csv`
- **Output**: `figures/MonthlyCenterlineFitting_FigS4.png`
- **Description**: [Brief description of what this figure shows]

### Figure 6: South-North Pelagic Ratio
- **Script**: `src/SouthNorthPelagicRatio_Fig6.py`
- **Data**: `data/Centerline_4decades.csv`
- **Output**: `figures/SouthNorthPelagicRatio_Fig6.png`
- **Description**: [Brief description of what this figure shows]

### Figure 7: South-North Pelagic Comparison
- **Script**: `src/SouthNorthPelagicComparison_Fig7.py`
- **Data**: `data/Centerline_4decades.csv`
- **Output**: `figures/SouthNorthPelagicComparison_Fig7.png`
- **Description**: [Brief description of what this figure shows]

### Figure 9 & Table 1: Phenology Analysis
- **Script**: `src/Phenology_Tab1_Fig9.py`
- **Data**: `data/Landsat_1984_2024_stations.csv`
- **Output**: `figures/Phenology_Tab1_Fig9.png`
- **Description**: [Brief description of what this figure/table shows]

## Data Sources

### Landsat Satellite Data
- **Period**: 1984-2024
- **Sensors**: [List of Landsat sensors used]
- **Processing**: [Brief description of data processing steps]
- **Citation**: [Cite the Landsat data source]

### Centerline Measurements
- **Period**: [Specify the time period]
- **Method**: [Brief description of measurement method]
- **Citation**: [Cite the data source if applicable]

## Analysis Methods

### Phenology Analysis
- **Start of Season (SOS)**: Defined as the day when chlorophyll-a exceeds 20% of the seasonal amplitude above the minimum
- **Peak Timing**: Maximum chlorophyll-a concentration during the growing season
- **Amplitude**: Difference between maximum and minimum chlorophyll-a concentrations
- **Area Under Curve (AUC)**: Integrated chlorophyll-a concentration from SOS to end of October

### Statistical Analysis
- **Bootstrap Uncertainty**: 1000 bootstrap samples for uncertainty estimation
- **Smoothing**: 30-day rolling window average and Savitzky-Golay filtering
- **Curve Fitting**: Multiple regression models (linear, exponential, power, logarithmic)

## Reproducibility

All analyses in this manuscript can be reproduced using the provided scripts and data. Each script is self-contained and includes all necessary data processing steps.

### Environment Setup
```bash
pip install -r requirements.txt
```

### Running All Analyses
```bash
cd src
python Phenology_Tab1_Fig9.py
python MonthlyCenterlineComparison_Fig3.py
python MonthlyCenterlineFitting_FigS4_Fig5.py
python SouthNorthPelagicRatio_Fig6.py
python SouthNorthPelagicComparison_Fig7.py
```

**Note**: All figures are automatically saved to the `figures/` directory in PNG format (300 DPI) for publication quality.

## Contact Information

For questions about the code or data, please contact:
- **Corresponding Author**: [Your name and email]
- **Repository**: [GitHub repository URL]

## Version Information

- **Code Version**: 1.0
- **Data Version**: 1.0
- **Last Updated**: [Date]
- **Python Version**: 3.8+ 