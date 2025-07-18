# Quick GitHub Upload Guide

## 🚀 Upload Steps (5 minutes)

### 1. Create GitHub Repository
1. Go to [GitHub.com](https://github.com) and sign in
2. Click "+" → "New repository"
3. Name: `balaton-chla-phenology`
4. Make it **Public** (recommended for science)
5. **Don't** initialize with README (we have one)
6. Click "Create repository"

### 2. Upload via GitHub Web Interface
1. In your new repository, click "uploading an existing file"
2. Drag and drop the entire `Balaton_Chla_Phenology_Manuscript` folder contents
3. Add commit message: "Initial commit: Balaton chlorophyll-a phenology analysis"
4. Click "Commit changes"

### 3. Or Upload via Command Line
```bash
# Navigate to the manuscript directory
cd "WaterQuality/Balaton_Chla_Phenology_Manuscript"

# Initialize git
git init
git add .
git commit -m "Initial commit: Balaton chlorophyll-a phenology analysis"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/balaton-chla-phenology.git
git branch -M main
git push -u origin main
```

## ✅ What Gets Uploaded
- ✅ All Python scripts (src/)
- ✅ Data files (data/)
- ✅ Generated figures (figures/)
- ✅ Documentation (README.md, docs/)
- ✅ Requirements (requirements.txt)
- ✅ Git configuration (.gitignore)

## 🎯 Repository Features
- **Reproducible**: Run `python run_all_analyses.py` to regenerate all figures
- **Documented**: Comprehensive README with usage instructions
- **Professional**: Clean code structure following scientific best practices
- **Complete**: All data and code needed to reproduce your manuscript

## 📊 Repository Size
- **Code**: ~50KB
- **Data**: ~800KB
- **Figures**: ~2.5MB
- **Total**: ~3.5MB (very reasonable for GitHub)

Your repository is ready to go! 🎉 