#!/usr/bin/env python3
"""
Run All Analyses Script

This script runs all the analysis scripts for the Balaton Chlorophyll-a Phenology manuscript
to generate all figures in the correct order.

Usage:
    python run_all_analyses.py
"""

import os
import sys
import subprocess
import time

def run_script(script_name, description):
    """Run a Python script and handle any errors."""
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"Description: {description}")
    print(f"{'='*60}")
    
    script_path = os.path.join("src", script_name)
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✅ Successfully completed: {script_name}")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print(f"❌ Error running {script_name}:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception running {script_name}: {str(e)}")
        return False
    
    return True

def main():
    """Run all analysis scripts in the correct order."""
    
    print("🚀 Starting Balaton Chlorophyll-a Phenology Analysis")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    
    # Check if src directory exists
    if not os.path.exists("src"):
        print("❌ Error: 'src' directory not found!")
        print("Please run this script from the manuscript root directory.")
        return False
    
    # Check if data directory exists
    if not os.path.exists("data"):
        print("❌ Error: 'data' directory not found!")
        print("Please ensure data files are in the 'data' directory.")
        return False
    
    # Create figures directory
    figures_dir = "figures"
    os.makedirs(figures_dir, exist_ok=True)
    print(f"📁 Figures will be saved to: {figures_dir}")
    
    # Define all scripts to run in order
    scripts = [
        ("Phenology_Tab1_Fig9.py", "Phenology analysis and Table 1, Figure 9"),
        ("MonthlyCenterlineComparison_Fig3.py", "Monthly centerline comparison (Figure 3)"),
        ("MonthlyCenterlineFitting_FigS4_Fig5.py", "Curve fitting analysis (Figure 5) and boxplots (Figure S4)"),
        ("SouthNorthPelagicRatio_Fig6.py", "South-north pelagic ratios (Figure 6)"),
        ("SouthNorthPelagicComparison_Fig7.py", "South-north pelagic comparison (Figure 7)")
    ]
    
    start_time = time.time()
    success_count = 0
    
    for script_name, description in scripts:
        if run_script(script_name, description):
            success_count += 1
        else:
            print(f"\n⚠️  Continuing with next script...")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 ANALYSIS SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successfully completed: {success_count}/{len(scripts)} scripts")
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    
    if success_count == len(scripts):
        print("\n🎉 All analyses completed successfully!")
        print(f"📁 Check the '{figures_dir}' directory for generated figures.")
        
        # List generated files
        if os.path.exists(figures_dir):
            files = os.listdir(figures_dir)
            if files:
                print(f"\n📄 Generated files:")
                for file in sorted(files):
                    file_path = os.path.join(figures_dir, file)
                    file_size = os.path.getsize(file_path)
                    print(f"   • {file} ({file_size:,} bytes)")
            else:
                print(f"\n⚠️  No files found in '{figures_dir}' directory.")
    else:
        print(f"\n⚠️  {len(scripts) - success_count} script(s) failed.")
        print("Please check the error messages above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 