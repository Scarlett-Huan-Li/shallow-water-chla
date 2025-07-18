# Balaton Chlorophyll-a Phenology Analysis

This repository contains the code and data for analyzing chlorophyll-a phenology in Lake Balaton, Hungary, based on Landsat satellite data from 1984-2024.

## 📁 Repository Structure

```
balaton-chla-phenology/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── run_all_analyses.py       # Script to run all analyses
├── data/                     # Input data files
│   ├── Landsat_1984_2024_stations.csv
│   └── Centerline_4decades.csv
├── src/                      # Analysis scripts
│   ├── Phenology_Tab1_Fig9.py
│   ├── MonthlyCenterlineComparison_Fig3.py
│   ├── MonthlyCenterlineFitting_FigS4_Fig5.py
│   ├── SouthNorthPelagicRatio_Fig6.py
│   └── SouthNorthPelagicComparison_Fig7.py
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
git clone https://github.com/[YOUR_USERNAME]/balaton-chla-phenology.git
cd balaton-chla-phenology
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
  - Output: `Phenology_Tab1_Fig9.png`
- **MonthlyCenterlineComparison_Fig3.py**: Creates monthly centerline comparison (Figure 3)
  - Output: `MonthlyCenterlineComparison_Fig3.png`
- **MonthlyCenterlineFitting_FigS4_Fig5.py**: Performs curve fitting analysis (Figure 5) and creates boxplots (Figure S4)
  - Output: `MonthlyCenterlineFitting_Fig5.png` and `MonthlyCenterlineFitting_FigS4.png`
- **SouthNorthPelagicRatio_Fig6.py**: Analyzes south-north pelagic ratios (Figure 6)
  - Output: `SouthNorthPelagicRatio_Fig6.png`
- **SouthNorthPelagicComparison_Fig7.py**: Compares south-north pelagic patterns (Figure 7)
  - Output: `SouthNorthPelagicComparison_Fig7.png`

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

## 🔬 Analysis Methods

The analysis includes:
- **Phenology Analysis**: Start of season (SOS), peak timing, amplitude, and area under curve (AUC)
- **Temporal Trends**: Decadal comparisons (1984-1994, 1995-2004, 2005-2014, 2015-2023)
- **Spatial Patterns**: Basin-specific analysis (Keszthely, Szigliget, Zanka, Tihany, Bfuzfo)
- **Statistical Fitting**: Multiple regression models for temporal patterns

## 📈 Key Findings

[To be added based on your manuscript results]

## 🤝 Contributing

This repository is associated with a scientific manuscript. For questions or collaboration, please contact the corresponding author.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Citation

If you use this code or data in your research, please cite:

[Add your manuscript citation here]

## 🔗 Related Publications

[Add links to related publications or datasets]

---

**Note**: This repository contains the complete reproducible analysis for the manuscript "Chlorophyll-a Phenology in Lake Balaton: A Four-Decade Analysis Using Landsat Data" (or your actual title). 