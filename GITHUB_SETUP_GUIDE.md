# GitHub Repository Setup Guide

## 🎯 What We've Accomplished

Your manuscript code and data are now ready for GitHub sharing! Here's what has been prepared:

### ✅ Fixed Issues
1. **Data Path Problems**: Updated all source code to use relative paths instead of hardcoded local paths
2. **Data File Names**: Corrected references to match actual data files:
   - `Landsat_1984_2024_withZala_modelResults.csv` → `Landsat_1984_2024_stations.csv`
   - `centerlineChange4decades-waterMask.csv` → `Centerline_4decades.csv`
3. **Cross-Platform Compatibility**: All paths now work on Windows, Mac, and Linux
4. **Figure Output**: Added automatic figure saving to `figures/` folder in PNG format (300 DPI)
5. **Code Cleanup**: Removed unnecessary debug code and historical comments

### 📁 Repository Structure
```
balaton-chla-phenology/
├── README.md                 # Comprehensive documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Excludes unnecessary files
├── data/                    # Input data files
│   ├── Landsat_1984_2024_stations.csv
│   └── Centerline_4decades.csv
├── src/                     # Analysis scripts
│   ├── Phenology_Tab1_Fig9.py
│   ├── MonthlyCenterlineComparison_Fig3.py
│   ├── MonthlyCenterlineFitting_FigS4_Fig5.py
│   ├── SouthNorthPelagicRatio_Fig6.py
│   └── SouthNorthPelagicComparison_Fig7.py
├── figures/                 # Generated figures (PNG format)
├── docs/                    # Documentation
│   └── manuscript_info.md
└── GITHUB_SETUP_GUIDE.md    # This guide
```

## 🚀 Next Steps to Create GitHub Repository

### 1. Create New Repository on GitHub
1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. Name it: `balaton-chla-phenology` (or your preferred name)
4. Make it **Public** (recommended for scientific reproducibility)
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

### 2. Initialize Local Git Repository
```bash
# Navigate to your manuscript directory
cd "WaterQuality/Balaton_Chla_Phenology_Manuscript"

# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Balaton chlorophyll-a phenology analysis"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/balaton-chla-phenology.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Update Documentation
Before pushing, update these files with your specific information:

#### README.md
- Replace `[Your manuscript title here]` with actual title
- Replace `[Author list]` with author names
- Replace `[Target journal name]` with journal name
- Replace `[Add your preferred license here]` with license (e.g., MIT, CC-BY)
- Replace `[Add your manuscript citation here]` with citation
- Replace `yourusername` with your GitHub username

#### docs/manuscript_info.md
- Fill in manuscript title, authors, journal
- Add abstract
- Describe what each figure shows
- Add your contact information

### 4. Test Everything Works
```bash
# Test data loading
python test_data_loading.py

# Test one of the analysis scripts
cd src
python Phenology_Tab1_Fig9.py
```

**Note**: Running any script will automatically create the `figures/` directory and save publication-quality figures (300 DPI PNG format).

### 5. Optional: Add DOI Badge
Once you have a DOI for your manuscript, add this to your README.md:
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

## 📊 Data Summary

### Landsat_1984_2024_stations.csv
- **7,586 rows** of satellite data
- **Date range**: 1984-05-26 to 2024-12-27
- **Basins**: Bfuzfo, Keszthely, Szigliget, Tihany, Zala, Zanka
- **Sensors**: LC08, LC09, LE07, LT04, LT05
- **Chlorophyll-a range**: 1.21 to 261.70

### Centerline_4decades.csv
- **3,746 rows** of centerline measurements
- **Date range**: 1994-01-01 to 2023-12-01
- **Distance range**: 0 to 77
- **Contains**: north coast, pelagic, and south coast measurements

## 🔧 Troubleshooting

### If scripts don't run:
1. Check Python version: `python --version` (should be 3.8+)
2. Install dependencies: `pip install -r requirements.txt`
3. Run test script: `python test_data_loading.py`

### If data files are missing:
1. Ensure data files are in the `data/` directory
2. Check file names match exactly (case-sensitive)
3. Verify file permissions

### If paths don't work:
1. All paths are now relative and should work on any system
2. Scripts use `os.path.join()` for cross-platform compatibility
3. Test with `python test_data_loading.py`

## 📝 Best Practices for Scientific Repositories

1. **Version Control**: Use meaningful commit messages
2. **Documentation**: Keep README.md updated
3. **Data Citation**: Cite your data sources
4. **Code Comments**: Ensure code is well-documented
5. **Reproducibility**: Test on clean environments
6. **Licensing**: Choose appropriate license for your work

## 🎉 You're Ready!

Your manuscript code and data are now properly organized and ready for sharing on GitHub. This will greatly enhance the reproducibility and impact of your research!

---

**Need help?** The repository structure follows best practices for scientific code sharing and should be easy for others to understand and use. 