# Shallow Water Chlorophyll-a Analysis

This repository contains the code and data for analyzing chlorophyll-a phenology in Lake Balaton, Hungary, based on Landsat satellite data from 1984-2024.

## 📁 Repository Structure

```
shallow-water-chla/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── run_all_analyses.py       # Script to run all analyses
├── data/                     # Input data files
│   ├── Landsat_1984_2024_stations.csv
│   ├── Centerline_4decades.csv
│   ├── Transection_I.csv
│   ├── Transection_II.csv
│   ├── Transection_III.csv
│   ├── Transection_IV-1.csv
│   └── Transection_IV-2.csv
├── src/                      # Analysis scripts
│   ├── Phenology_Tab1_Fig9.py
│   ├── MonthlyCenterlineComparison_Fig3.py
│   ├── SpatioTemporalAsynchrony_Fig4.py
│   ├── MonthlyCenterlineFitting_FigS4_Fig5.py
│   ├── MonthlyCenterlineFitting_singleMonth_Fig5.py
│   ├── SouthNorthPelagicRatio_Fig6.py
│   ├── SouthNorthPelagicComparison_Fig7.py
│   └── TransectionalOverlay_Fig8.py
├── figures/                  # Generated figures (PNG format)
└── docs/                     # Documentation
    └── manuscript_info.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Scarlett-Huan-Li/shallow-water-chla.git
cd shallow-water-chla
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### Running the Analysis

#### Option 1: Run All Analyses at Once
```bash
python run_all_analyses.py
```
This will run all scripts in the correct order and generate all figures.

#### Option 2: Run Individual Scripts
Each script in the `src/` directory generates specific figures for the manuscript and automatically saves them to the `figures/` folder in PNG format (300 DPI):

- **Phenology_Tab1_Fig9.py**: Generates phenology analysis and Table 1, Figure 9
  - **Features**: Modular code structure with statistical trend analysis (Mann-Kendall test)
  - **Methods**: Peak DOY temporal trend testing across four decades with outlier correction using non-parametric Mann-Kendall test with Sen's slope
  - **Output**: `Phenology_Tab1_Fig9.png`
- **MonthlyCenterlineComparison_Fig3.py**: Creates monthly centerline comparison (Figure 3)
  - Output: `MonthlyCenterlineComparison_Fig3.png`
- **SpatioTemporalAsynchrony_Fig4.py**: Analyzes spatiotemporal asynchrony patterns (Figure 4)
  - Output: `SpatioTemporalAsynchrony_Fig4.png`
- **MonthlyCenterlineFitting_FigS4_Fig5.py**: Performs curve fitting analysis (Figure 5) and creates boxplots (Figure S4)
  - Output: `MonthlyCenterlineFitting_Fig5.png` and `MonthlyCenterlineFitting_FigS4.png`
- **MonthlyCenterlineFitting_singleMonth_Fig5.py**: Generates single curve fitting plot for Figure 5 left subplot
  - **Features**: Modular design with multiple regression models (Linear, Logarithmic, Polynomial, Exponential)
  - **Methods**: Curve fitting analysis for July 2015-2023 data with R² and RMSE calculations
  - **Output**: `SingleCurveFitting_Fig5_left.png`
- **SouthNorthPelagicRatio_Fig6.py**: Analyzes south-north pelagic ratios (Figure 6)
  - Output: `SouthNorthPelagicRatio_Fig6.png`
- **SouthNorthPelagicComparison_Fig7.py**: Compares south-north pelagic patterns (Figure 7)
  - Output: `SouthNorthPelagicComparison_Fig7.png`
- **TransectionalOverlay_Fig8.py**: Generates transectional overlay between Chl-a and bathymetry (Figure 8)
  - **Features**: Professional visualization of five transects (I, II, III, IV-1, IV-2) with dual y-axes
  - **Methods**: Chl-a concentration (red line) and water depth (blue line) with littoral zone boundaries at 2m depth
  - **Styling**: Professional formatting with Arial fonts, optimized colors, and clean layout
  - **Output**: `TransectionalOverlay_Fig8.png`

Example:
```bash
cd src
python Phenology_Tab1_Fig9.py
```

**Note**: The `figures/` directory will be automatically created when you run any script for the first time.

## 📊 Data Description

### Landsat_1984_2024_stations.csv
- **Source**: Landsat satellite data (1984-2024)
- **Content**: Chlorophyll-a concentrations from different basins in Lake Balaton
- **Columns**: date, chla, Basin, sensor, doy (day of year)

### Centerline_4decades.csv
- **Source**: Centerline measurements across four decades
- **Content**: Distance measurements and pelagic/coastal classifications
- **Columns**: date, distance, pelagic, north_coast, south_coast, month, year

### Transectional Data Files (Transection_I.csv to Transection_IV-2.csv)
- **Source**: Field measurements and bathymetric surveys
- **Content**: Transectional profiles of chlorophyll-a concentration and water depth across Lake Balaton
- **Structure**: Five transects (I, II, III, IV-1, IV-2) running from south to north
- **Columns**: 
  - `distance`: Distance from south to north (meters, converted to kilometers in analysis)
  - `depth`: Water depth (meters, negative values)
  - `chla`: Chlorophyll-a concentration (μg/L)
- **Purpose**: Used for generating Figure 8 showing spatial patterns of Chl-a and bathymetry relationships

## 🔬 Analysis Methods

The analysis includes:
- **Phenology Analysis**: Start of season (SOS), peak timing, amplitude, and area under curve (AUC)
- **Temporal Trends**: Decadal comparisons (1984-1994, 1995-2004, 2005-2014, 2015-2023)
- **Spatial Patterns**: Basin-specific analysis (Keszthely, Szigliget, Zanka, Tihany, Bfuzfo)
- **Statistical Fitting**: Multiple regression models for temporal patterns
- **Statistical Testing**: 
  - Mann-Kendall test with Sen's slope for non-parametric trend analysis
  - Outlier detection and correction for robust results

## 📈 Key Findings

1. **Spatial asynchrony across lake basins exists for the intra- and inter-annual change of Chl-a.**
2. **The littoral/pelagic ratio of the maximum optical Chl-a remains between 1.3 and 2.8.**
3. **Peak Chl-a timing advanced by 5 days/decade, with start of season advancing by 10 days.**
4. **Bloom intensity decreased in western basins but remained stable in eastern regions.**

## 🤝 Contributing

This repository is associated with a scientific manuscript. For questions or collaboration, please contact the corresponding author.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Publications

- **Li, H., Somogyi, B., Chen, X., Luo, Z., Blix, K., Wu, S., Duan, Z. and Tóth, V.R.** (2025) Leveraging Landsat and Google Earth Engine for long-term chlorophyll-a monitoring: A case study of Lake Balaton's water quality. *Ecological Informatics* 90, 103245.

- **Li, H., Somogyi, B. and Tóth, V.** (2024) Exploring spatiotemporal features of surface water temperature for Lake Balaton in the 21st century based on Google Earth Engine. *Journal of Hydrology* 640, 131672.

- **Li, H., Sun, J., Zhou, Q., Sojka, M., Ptak, M., Luo, Y., Wu, S., Zhu, S. and Tóth, V.R.** (2024) 150-year daily data (1870–2021) in lakes and rivers reveals intensifying surface water warming and heatwaves in the Pannonian Ecoregion (Hungary). *Journal of Hydrology: Regional Studies* 56, 101985.

---

**Note**: This repository contains the complete reproducible analysis for the manuscript "Satellite-based Monitoring Reveals Climate-driven Phenological Shifts and Spatial Heterogeneity in Shallow Lake Chlorophyll-a Dynamics: A Four-Decade Analysis". 