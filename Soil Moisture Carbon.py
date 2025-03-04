import os
import numpy as np
import rasterio
from rasterio.enums import Resampling
import matplotlib.pyplot as plt  

# Define file paths
path = "Update with your Data Path"
nir_path = os.path.join(path, 'Sentinel2_B8.tif')  # NIR
red_path = os.path.join(path, 'Sentinel2_B4.tif')  # RED
swir_path = os.path.join(path, 'Sentinel2_B11.tif') # SWIR
blue_path = os.path.join(path, 'Sentinel2_B2.tif') # BLUE
vv_path = os.path.join(path, 'VV.tif') # SAR VV
vh_path = os.path.join(path, 'Vh.tif') # SAR VH

# Function to read raster and resample
def read_raster(file_path, target_shape=None, target_transform=None):
    with rasterio.open(file_path) as src:
        data = src.read(1).astype(float)
        bounds = src.bounds
        transform = src.transform
        if target_shape and target_transform:
            data = resample_raster(src, target_shape, target_transform)
        return data, bounds, transform

def resample_raster(src, target_shape, target_transform):
    data = src.read(
        out_shape=target_shape,
        resampling=Resampling.bilinear  
    )
    return data[0]  

# Read rasters
nir, nir_bounds, nir_transform = read_raster(nir_path)
red, _, _ = read_raster(red_path)
swir, _, _ = read_raster(swir_path)
blue, _, _ = read_raster(blue_path)
vv, vv_bounds, vv_transform = read_raster(vv_path)
vh, _, _ = read_raster(vh_path)

# Get target shape
target_shape = nir.shape
target_transform = nir_transform

# Resample all images to match NIR resolution
red, _, _ = read_raster(red_path, target_shape, target_transform)
swir, _, _ = read_raster(swir_path, target_shape, target_transform)
blue, _, _ = read_raster(blue_path, target_shape, target_transform)
vv, _, _ = read_raster(vv_path, target_shape, target_transform)
vh, _, _ = read_raster(vh_path, target_shape, target_transform)

# Functions to compute indices
def calculate_ndmi(nir, swir):
    return (nir - swir) / (nir + swir + 1e-6)

def calculate_ndvi(nir, red):
    return (nir - red) / (nir + red + 1e-6)

def calculate_evi(nir, red, blue):
    """Fix divide by zero error by adding a small constant (1e-6)"""
    denominator = (nir + 6 * red - 7.5 * blue + 1 + 1e-6)
    return 2.5 * (nir - red) / denominator

def calculate_soil_moisture_sar(vv, vh, a=0.1, b=0.2, c=0.3):
    """Calculate soil moisture using SAR data (VV and VH bands)"""
    return a + b * vv + c * vh

def calculate_soc(ndvi, evi, alpha=0.5, beta=0.3, gamma=0.2):
    """Calculate Soil Organic Carbon (SOC) using NDVI and EVI"""
    return alpha + beta * ndvi + gamma * evi

def calculate_soc_sar(vh, vv, A=0.2, B=0.3, C=0.4):
    """Calculate Soil Organic Carbon (SOC) using SAR data (VV and VH bands)"""
    return A + B * vh + C * vv

# Compute indices
ndmi = calculate_ndmi(nir, swir)
ndvi = calculate_ndvi(nir, red)
evi = calculate_evi(nir, red, blue)
soil_moisture_sar = calculate_soil_moisture_sar(vv, vh)
soc = calculate_soc(ndvi, evi)
soc_sar = calculate_soc_sar(vh, vv)

# Visualize results using matplotlib
def plot_index(data, title, cmap='viridis'):
    plt.figure(figsize=(10, 10))
    plt.imshow(data, cmap=cmap)
    plt.colorbar(label=title)
    plt.title(title)
    plt.axis('off')  # Hide axes
    plt.show()

# Plot NDMI
plot_index(ndmi, 'NDMI (Normalized Difference Moisture Index)', cmap='Blues')

# Plot NDVI
plot_index(ndvi, 'NDVI (Normalized Difference Vegetation Index)', cmap='Greens')

# Plot EVI
plot_index(evi, 'EVI (Enhanced Vegetation Index)', cmap='YlGn')

# Plot Soil Moisture (SAR)
plot_index(soil_moisture_sar, 'Soil Moisture (SAR)', cmap='RdPu')

# Plot SOC
plot_index(soc, 'Soil Organic Carbon (SOC)', cmap='OrRd')

# Plot SOC (SAR)
plot_index(soc_sar, 'Soil Organic Carbon (SAR)', cmap='Purples')

# Print sample values
print("NDMI Sample:", ndmi[0, 0])
print("NDVI Sample:", ndvi[0, 0])
print("EVI Sample:", evi[0, 0])
print("Soil Moisture (SAR) Sample:", soil_moisture_sar[0, 0])
print("SOC Sample:", soc[0, 0])
print("SOC (SAR) Sample:", soc_sar[0, 0])


# Function to save index as PNG
def save_index(data, title, filename, cmap='viridis'):
    plt.figure(figsize=(10, 10))
    plt.imshow(data, cmap=cmap)
    plt.colorbar(label=title)
    plt.title(title)
    plt.axis('off')  # Hide axes
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

# Define output path
output_path = "Update with your Output path"

# Ensure the directory exists
os.makedirs(output_path, exist_ok=True)

# Save the images
save_index(ndmi, 'NDMI (Normalized Difference Moisture Index)', os.path.join(output_path, 'NDMI.png'), cmap='Blues')
save_index(ndvi, 'NDVI (Normalized Difference Vegetation Index)', os.path.join(output_path, 'NDVI.png'), cmap='Greens')
save_index(evi, 'EVI (Enhanced Vegetation Index)', os.path.join(output_path, 'EVI.png'), cmap='YlGn')
save_index(soil_moisture_sar, 'Soil Moisture (SAR)', os.path.join(output_path, 'Soil_Moisture_SAR.png'), cmap='RdPu')
save_index(soc, 'Soil Organic Carbon (SOC)', os.path.join(output_path, 'SOC.png'), cmap='OrRd')
save_index(soc_sar, 'Soil Organic Carbon (SAR)', os.path.join(output_path, 'SOC_SAR.png'), cmap='Purples')

print("All images saved successfully in PNG format.")
