# Soil Carbon and Moisture Prediction

## Overview
This script processes remote sensing data to estimate soil moisture and soil organic carbon (SOC) using both optical (Sentinel-2) and SAR (Sentinel-1) data. It calculates multiple indices such as NDVI, NDMI, EVI, and SAR-based soil moisture and SOC, visualizing and saving the results as PNG images. The script ensures all datasets are resampled to a common resolution for consistency in analysis.

## Data Requirements
### Input Data:
- **Sentinel-2 Bands:**
  - B8 (NIR - Near Infrared)
  - B4 (Red)
  - B11 (SWIR - Shortwave Infrared)
  - B2 (Blue)
- **Sentinel-1 SAR Bands:**
  - VV (Vertical-Vertical)
  - VH (Vertical-Horizontal)

### Output Data:
The script generates multiple geospatial indices in PNG format:
- **NDMI** (Normalized Difference Moisture Index)
- **NDVI** (Normalized Difference Vegetation Index)
- **EVI** (Enhanced Vegetation Index)
- **Soil Moisture (SAR-based)**
- **Soil Organic Carbon (SOC) from NDVI and EVI**
- **Soil Organic Carbon (SOC) from SAR Data (VV & VH)**

## Methodology & Formulas
### 1. Normalized Difference Moisture Index (NDMI)
```math
NDMI = \frac{NIR - SWIR}{NIR + SWIR + 1e-6}
```
- **NIR**: Near-Infrared Band (Sentinel-2 B8)
- **SWIR**: Shortwave Infrared Band (Sentinel-2 B11)

### 2. Normalized Difference Vegetation Index (NDVI)
```math
NDVI = \frac{NIR - Red}{NIR + Red + 1e-6}
```
- **NIR**: Near-Infrared Band (Sentinel-2 B8)
- **Red**: Red Band (Sentinel-2 B4)

### 3. Enhanced Vegetation Index (EVI)
```math
EVI = 2.5 \times \frac{NIR - Red}{NIR + 6 \times Red - 7.5 \times Blue + 1 + 1e-6}
```
- **NIR**: Near-Infrared Band (Sentinel-2 B8)
- **Red**: Red Band (Sentinel-2 B4)
- **Blue**: Blue Band (Sentinel-2 B2)

### 4. Soil Moisture Estimation using SAR Data
```math
SM = a + b \times VV + c \times VH
```
- **VV**: SAR VV Band (Sentinel-1)
- **VH**: SAR VH Band (Sentinel-1)
- **a, b, c**: Empirical coefficients (set as 0.1, 0.2, 0.3)

### 5. Soil Organic Carbon (SOC) Estimation using Optical Data
```math
SOC = \alpha + \beta \times NDVI + \gamma \times EVI
```
- **NDVI**: Normalized Difference Vegetation Index
- **EVI**: Enhanced Vegetation Index
- **α, β, γ**: Empirical coefficients (set as 0.5, 0.3, 0.2)

### 6. Soil Organic Carbon (SOC) Estimation using SAR Data
```math
SOC_{SAR} = A + B \times VH + C \times VV
```
- **VH**: SAR VH Band (Sentinel-1)
- **VV**: SAR VV Band (Sentinel-1)
- **A, B, C**: Empirical coefficients (set as 0.2, 0.3, 0.4)

## Installation & Dependencies
Ensure the following Python libraries are installed:
```bash
pip install numpy rasterio matplotlib
```

## Usage Instructions
1. Update the `path` variable in the script with the correct file location.
2. Ensure all Sentinel-2 and Sentinel-1 bands are stored in the specified path.
3. Run the script using:
```bash
python Soil Moisture Carbon.py
```
4. The script will generate and save the calculated indices as PNG images in the specified output folder.

## Output Files
- `NDMI.png` (Moisture Index)
- `NDVI.png` (Vegetation Index)
- `EVI.png` (Enhanced Vegetation Index)
- `Soil_Moisture_SAR.png` (Soil Moisture from SAR Data)
- `SOC.png` (Soil Organic Carbon from NDVI and EVI)
- `SOC_SAR.png` (Soil Organic Carbon from SAR Data)

## Notes
- Ensure raster data is in the same spatial resolution before processing.
- Modify the coefficients based on field calibration data if available.
- The script includes automated resampling of raster images to match NIR band resolution.

## Future Improvements
- Integrating additional Sentinel-2 bands for improved SOC estimation.
- Implementing machine learning techniques for enhanced prediction accuracy.
- Adding geospatial vector overlay to analyze SOC variations within specific land parcels.

## Author
Developed for soil moisture and carbon prediction using remote sensing data.

For questions or improvements, feel free to contribute or reach out!

