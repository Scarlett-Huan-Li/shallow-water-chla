# Manuscript Information

## Publication Details

**Title:** Four Decades of Satellite Observations Reveal Climate-Driven Shifts and Spatial Heterogeneity in Shallow Lake Chlorophyll-a Dynamics

**Authors:** Li, Huan; Somogyi, Boglárka; Chen, Xiaona; Wan, Wei; Duan, Zheng; Woolway, R. Iestyn; Tóth, Viktor R.

**Journal:** Water Research (2025) | ✅ **Published Online**

**DOI:** https://doi.org/10.1016/j.watres.2025.124925 | **Article Number:** 124925

## Abstract
Shallow lakes worldwide face escalating pressures from eutrophication and climate change, yet comprehensive monitoring of Chlorophyll-a (Chl-a) spatiotemporal dynamics remains challenging due to the high costs and logistical constraints of traditional sampling approaches across large, heterogeneous water bodies. Lake Balaton, a large shallow lake system (80 km long, 7 km wide, 3.7 m mean depth) in Central Europe, exemplifies these monitoring challenges while serving as a representative system for understanding climate-driven changes in temperate shallow lakes. Despite decades of in-situ measurements along the lake's centerline, fine-scale spatial patterns and long-term temporal trends in Chl-a remain poorly characterized due to sparse samplings. Using a machine-learning-derived optical remote sensing dataset (1984-2023) at 30 m spatial resolution, we conducted comprehensive spatiotemporal analysis of Chl-a dynamics and examined relationships with bathymetry, nutrient loading, and light availability features. Our analysis reveals an exponential west-to-east decline in Chl-a concentrations with distance from the primary nutrient source, characterized by a consistent decay rate of 0.04-0.06 km⁻¹ (typically 0.05 km⁻¹). Littoral zones consistently exhibited 1.3-2.8 times higher optical Chl-a concentrations than pelagic zones, reflecting integrated signals from phytoplankton, benthic algae, and submerged macrophytes. Phenological analysis demonstrated significant climate-driven shifts, with peak Chl-a timing advancing by 20 days over the study period and growing season onset occurring 10 days earlier, consistent with regional warming trends. These findings provide a transferable framework for satellite-based water quality monitoring in shallow lake systems and demonstrate the critical importance of accounting for spatial heterogeneity and climate-driven temporal shifts in lake management strategies globally.

## Graphical Abstract

![Graphical Abstract](../figures/Graphic%20Abstract.jpg)

*Graphical abstract: Four Decades of Satellite Observations Reveal Climate-Driven Shifts and Spatial Heterogeneity in Shallow Lake Chlorophyll-a Dynamics*

## Key Figures and Tables

### Figure 3: Monthly Centerline Comparison
- **Script**: `src/MonthlyCenterlineComparison_Fig3.py`
- **Data**: `data/Centerline_4decades.csv`
- **Output**: `figures/MonthlyCenterlineComparison_Fig3.png`

### Figure 5: Monthly Centerline Fitting
- **Script**: `src/MonthlyCenterlineFitting_FigS4_Fig5.py`
- **Data**: `data/Centerline_4decades.csv`
- **Output**: `figures/MonthlyCenterlineFitting_Fig5.png`

### Figure S4: Fitting Statistics Boxplots
- **Script**: `src/MonthlyCenterlineFitting_FigS4_Fig5.py`
- **Data**: `data/Centerline_4decades.csv`
- **Output**: `figures/MonthlyCenterlineFitting_FigS4.png`

### Figure 6: South-North Pelagic Ratio
- **Script**: `src/SouthNorthPelagicRatio_Fig6.py`
- **Data**: `data/Centerline_4decades.csv`
- **Output**: `figures/SouthNorthPelagicRatio_Fig6.png`

### Figure 7: South-North Pelagic Comparison
- **Script**: `src/SouthNorthPelagicComparison_Fig7.py`
- **Data**: `data/Centerline_4decades.csv`
- **Output**: `figures/SouthNorthPelagicComparison_Fig7.png`

### Figure 9 & Table 1: Phenology Analysis
- **Script**: `src/Phenology_Tab1_Fig9.py`
- **Data**: `data/Landsat_1984_2024_stations.csv`
- **Output**: `figures/Phenology_Tab1_Fig9.png`

## Data Sources

### Landsat Satellite Data
- **Sensors**: Landsat 5-9
- **Period**: 1984-2024
- **Spatial Resolution**: 30 m
- **Processing**: Machine-learning-derived optical remote sensing dataset

### Centerline Data
- **Period**: 1984-2024
- **Source**: Landsat-derived chlorophyll-a data along the lake's centerline

### Bathymetry
- **Source**: Bathymetric survey data by Hungarian Water Authorities

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

## Citation

**Li, H., Somogyi, B., Chen, X., Wan, W., Duan, Z., Woolway, R.I., and Tóth, V.R.** (2025) Four Decades of Satellite Observations Reveal Climate-Driven Shifts and Spatial Heterogeneity in Shallow Lake Chlorophyll-a Dynamics. *Water Research* 124925. doi: https://doi.org/10.1016/j.watres.2025.124925

## Contact Information

For questions about the code or data, please contact:
- **Corresponding Author**: [Huan Li](https://geolab.live/)
- **Personal Website**: https://geolab.live/
- **Repository**: https://github.com/Scarlett-Huan-Li/shallow-water-chla 