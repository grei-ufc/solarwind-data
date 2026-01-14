# wind_analysis.py

import os
import rasterio
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import cdsapi
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go


def run_wind_analysis(lat: float, lon: float, API_KEY: str):
    print(f"\n{'='*70}")
    print(f"WIND ANALYSIS → Lat: {lat:.2f}° | Lon: {lon:.2f}°")
    print(f"{'='*70}")

    # =========================== CONFIGURATION ===========================
    coord_folder = f"{lat:.2f}_{lon:.2f}".replace('-', 'm').replace('.', 'p')
    output_dir = os.path.join(".\output", coord_folder)
    figures_pdf_folder = os.path.join(output_dir, "figures_pdf")

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(figures_pdf_folder, exist_ok=True)

    lat_str = f"Lat_{str(lat).replace('-', 'm').replace('.', 'p')}"
    lon_str = f"Lon_{str(lon).replace('-', 'm').replace('.', 'p')}"

    INPUT_FOLDER = r"./input"
    GEOTIFF_FILE = os.path.join(INPUT_FOLDER, "ceara_cf_onshore_offshore_iec_ii.tif")

    POWER_DENSITY = 0.004  # kW/m²

    # =========================== DOWNLOAD ERA5  ===========================
    print("Downloading ERA5 100m wind data (1998–2018)...")
    c = cdsapi.Client(url="https://cds.climate.copernicus.eu/api", key=API_KEY)

    years = [str(y) for y in range(1999, 2019)]
    nc_files = []
    for year in years:
        file_path = os.path.join(output_dir, f"wind100m_{year}.nc")
        nc_files.append(file_path)

        if os.path.exists(file_path):
            print(f"   → {year}: Already exist")
            continue

        print(f"   → Baixando {year}...")
        try:
            c.retrieve(
                "reanalysis-era5-single-levels",
                {
                    "product_type": "reanalysis",
                    "variable": ["100m_u_component_of_wind", "100m_v_component_of_wind"],
                    "year": year,
                    "month": [f"{m:02d}" for m in range(1,13)],
                    "day": [f"{d:02d}" for d in range(1,32)],
                    "time": [f"{h:02d}:00" for h in range(24)],
                    "area": [lat, lon, lat, lon],
                    "format": "netcdf"
                },
                file_path
            )
        except Exception as e:
            print(f"There's a error {year}: {e}")

    # =========================== WIND DATA PROCESSING ===========================
    if not nc_files or not any(os.path.exists(f) for f in nc_files):
        print("No wind files found. Skipping calculations.")
        return

    ds = xr.open_mfdataset([f for f in nc_files if os.path.exists(f)], combine='by_coords')
    point_data = ds.sel(latitude=lat, longitude=lon, method='nearest')

    df_wind = point_data[['u100', 'v100']].to_dataframe().reset_index()
    df_wind.rename(columns={'u100': 'U100', 'v100': 'V100'}, inplace=True)

    if 'valid_time' in df_wind.columns:
        df_wind.rename(columns={'valid_time': 'Time'}, inplace=True)
    elif 'time' in df_wind.columns:
        df_wind.rename(columns={'time': 'Time'}, inplace=True)

    df_wind.dropna(subset=['U100', 'V100'], inplace=True)
    df_wind['WindSpeed'] = np.sqrt(df_wind['U100']**2 + df_wind['V100']**2)
    df_wind['Month'] = df_wind['Time'].dt.month
    df_wind['Hour'] = df_wind['Time'].dt.hour

    # =========================== CAPACITY FACTOR ===========================
    capacity_factor = 0.45
    if os.path.exists(GEOTIFF_FILE):
        try:
            with rasterio.open(GEOTIFF_FILE) as src:
                row, col = src.index(lon, lat)
                val = src.read(1)[row, col]
                if not np.isnan(val) and val != src.nodata:
                    capacity_factor = val
                    print(f"GeoTIFF capacity factor: {capacity_factor:.4f}")
        except Exception as e:
            print(f"Error reading GeoTIFF: {e}")

    # =========================== ESTATISTICS ===========================
    mean = df_wind.pivot_table(values='WindSpeed', index='Month', columns='Hour', aggfunc='mean')
    std = df_wind.pivot_table(values='WindSpeed', index='Month', columns='Hour', aggfunc='std')
    cv = (std / mean * 100).fillna(0)

    global_mean = df_wind['WindSpeed'].mean()
    energy_density = mean / global_mean * capacity_factor * POWER_DENSITY

    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    mean.index = month_names
    std.index = month_names
    cv.index = month_names
    energy_density.index = month_names

    # =========================== GRAPHICS ===========================
    cmap = sns.color_palette("turbo", as_cmap=True)

    def save_clean_heatmap(data, base_name, cbar_label, fmt=".5f"):
        plt.figure(figsize=(16, 8))
        sns.heatmap(data, annot=True, fmt=fmt, cmap=cmap, linewidths=0.5,
                    cbar_kws={'label': cbar_label, 'shrink': 0.8},
                    annot_kws={'size': 9})
        plt.xlabel("Hour of Day", fontsize=12)
        plt.ylabel("Month", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        filename = f"{base_name}_{lat_str}_{lon_str}.pdf"
        path = os.path.join(figures_pdf_folder, filename)
        plt.savefig(path, format='pdf', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"File created: {filename}")

    save_clean_heatmap(energy_density, "Wind_Monthly_Average_Energy_Density", "Average Energy Density (kWh/m²)")
    save_clean_heatmap(std * capacity_factor * POWER_DENSITY, "Wind_Monthly_Standard_Deviation", "Standard Deviation (kWh/m²)")
    save_clean_heatmap(cv, "Wind_Coefficient_of_Variation", "Coefficient of Variation (%)", ".1f")

    # =========================== 3D SURFACE PLOT  ===========================
    X, Y = np.meshgrid(np.arange(24), np.arange(12))
    Z = (std * capacity_factor * POWER_DENSITY).values

    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='turbo', edgecolor='k', linewidth=0.3, alpha=0.9, antialiased=True)

    ax.set_xlabel('Hour of Day', labelpad=15, fontsize=12)
    ax.set_ylabel('Month', labelpad=15, fontsize=12)
    ax.set_zlabel('Standard Deviation\n(kWh/m²)', labelpad=15, fontsize=12)

    ax.set_xticks(np.arange(0, 24, 3))
    ax.set_xticklabels([f"{h:02d}h" for h in range(0, 24, 3)])
    ax.set_yticks(np.arange(12))
    ax.set_yticklabels(month_names)

    ax.view_init(elev=30, azim=-60)

    cbar = fig.colorbar(surf, shrink=0.6, aspect=20, pad=0.1)
    cbar.set_label('Standard Deviation (kWh/m²)', rotation=270, labelpad=20, fontsize=11)

    plt.tight_layout()

    pdf_3d = f"Wind_Standard_Deviation_3D_{lat_str}_{lon_str}.pdf"
    path_3d = os.path.join(figures_pdf_folder, pdf_3d)
    plt.savefig(path_3d, format='pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"File created {pdf_3d}")

    # --- Plotly 3D  ---
    figly = go.Figure(data=[go.Surface(
        z=Z, x=np.arange(24), y=np.arange(12),
        colorscale='Turbo',
        colorbar=dict(title="Std Dev<br>(kWh/m²)", thickness=20),
        contours_z=dict(show=True, usecolormap=True, project_z=True)
    )])

    figly.update_layout(
        scene=dict(
            xaxis_title="Hour of Day",
            yaxis_title="Month",
            zaxis_title="Std Dev (kWh/m²)",
            xaxis=dict(tickvals=np.arange(0,24,3), ticktext=[f"{h:02d}h" for h in range(0,24,3)]),
            yaxis=dict(tickvals=list(range(12)), ticktext=month_names),
        ),
        width=1200, height=800,
        margin=dict(l=0, r=0, b=0, t=40)
    )

    html_3d = f"Wind_Standard_Deviation_3D_{lat_str}_{lon_str}.html"
    path_html = os.path.join(figures_pdf_folder, html_3d)
    figly.write_html(path_html, include_plotlyjs='cdn')
    print(f"Interactive file created: {html_3d}")

    print(f"\nWIND ANALYSIS COMPLETED!")
    print(f"All files saved in: {figures_pdf_folder}\n")
    print(f"{'='*70}\n")


# Teste direto (apague a chave depois!)
#if __name__ == "__main__":
    #API_KEY = ''
    #run_wind_analysis(-3.73, -38.52, API_KEY)