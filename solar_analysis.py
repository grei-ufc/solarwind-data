# solar_analysis.py


import os
import rasterio
import seaborn as sns
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import xarray as xr
from rasterio.mask import mask
from pyproj import Transformer
import cdsapi
from mpl_toolkits.mplot3d import Axes3D


def run_solar_analysis(lat: float, lon: float, API_KEY: str):
    print(f"\n{'='*70}")
    print(f"SOLAR ANALYSIS → Lat: {lat:.2f}° | Lon: {lon:.2f}°")
    print(f"{'='*70}")
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    # =========================== FOLDERS ===========================
    coord_folder = f"{lat:.2f}_{lon:.2f}".replace('-', 'm').replace('.', 'p')
    output_dir = os.path.join("./output", coord_folder)
    figures_pdf_folder = os.path.join(output_dir, "figures_pdf")

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(figures_pdf_folder, exist_ok=True)

    lat_str = f"Lat_{str(lat).replace('-', 'm').replace('.', 'p')}"
    lon_str = f"Lon_{str(lon).replace('-', 'm').replace('.', 'p')}"

    # =========================== INPUT AND SHAPEFILE ===========================
    base_path = r"./input"
    ceara_shape_path = os.path.join(base_path, "ceara_onshore.shp")

    gdf_ceara = gpd.read_file(ceara_shape_path)
    if gdf_ceara.crs is None:
        gdf_ceara = gdf_ceara.set_crs("EPSG:4326")
    else:
        gdf_ceara = gdf_ceara.to_crs("EPSG:4326")

    # =========================== BASIC FUNCTIONS ===========================
    def process_monthly_tifs(month_num):
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        raster_path = os.path.join(base_path, f"ceara_densiPV_{month_num:02d}.tif")
        if not os.path.exists(raster_path):
            print(f"File not found: {raster_path}")
            return None

        try:
            with rasterio.open(raster_path) as src:
                gdf_temp = gdf_ceara.to_crs(src.crs)
                out_image, out_transform = mask(src, gdf_temp.geometry, crop=True)
                out_meta = src.meta.copy()
                out_meta.update({
                    "driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform
                })

            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month_num-1]
            solar_energy_density = out_image[0] / days_in_month

            height, width = solar_energy_density.shape
            x_coords = np.linspace(out_transform.c + out_transform.a/2, out_transform.c + out_transform.a*(width-0.5), width)
            y_coords = np.linspace(out_transform.f + out_transform.e*(height-0.5), out_transform.f + out_transform.e/2, height)
            x_mesh, y_mesh = np.meshgrid(x_coords, y_coords)

            transformer = Transformer.from_crs(src.crs, "EPSG:4326", always_xy=True)
            lons, lats = transformer.transform(x_mesh, y_mesh)

            solar_energy_density = np.flipud(solar_energy_density)
            filtered = np.where(solar_energy_density < 1e-10, np.nan, solar_energy_density)
            vmin, vmax = np.nanpercentile(filtered[~np.isnan(filtered)], [2, 98])

            return {
                'data': filtered,
                'lons': lons,
                'lats': lats,
                'month_name': month_names[month_num-1],
                'vmin': vmin,
                'vmax': vmax
            }
        except Exception as e:
            print(f"Error in the month: {month_num:02d}: {e}")
            return None

    def extract_value_by_coordinate(lat, lon, data, lons, lats):
        distances = np.sqrt((lons - lon)**2 + (lats - lat)**2)
        row, col = np.unravel_index(np.argmin(distances), distances.shape)
        if distances[row, col] > 0.02:
            print(f"Warning: Point far from the raster: ({distances[row, col]:.4f}°)")
            return np.nan
        return data[row, col]

    # =========================== EXTRACT MONTH VALUES ===========================
    monthly_values = {}
    for month in range(1, 13):
        result = process_monthly_tifs(month)
        if result:
            val = extract_value_by_coordinate(lat, lon, result['data'], result['lons'], result['lats'])
            monthly_values[result['month_name']] = val if val is not None else np.nan

    values_list = list(monthly_values.values())

    # =========================== HOURLY PROFILES ===========================
    def fourier_function(t, P, A0, An, Bn):
        result = A0
        for n in range(len(An)):
            result += An[n] * np.cos(2 * np.pi * (n+1) * t / P) + Bn[n] * np.sin(2 * np.pi * (n+1) * t / P)
        return result

    def solar_declination(n):
        return 23.45 * np.sin(np.deg2rad(360 * (284 + n) / 365))

    def equation_of_time(n):
        B = np.deg2rad((360/365) * (n - 81))
        return 9.87*np.sin(2*B) - 7.53*np.cos(B) - 1.5*np.sin(B)

    def sunrise_hour(latitude, decl):
        ha = np.degrees(np.arccos(-np.tan(np.deg2rad(latitude)) * np.tan(np.deg2rad(decl))))
        return 12 - ha/15, 12 + ha/15

    def generate_hourly_profile_day(day_of_year, daily_density, latitude, local_longitude, timezone=-3):
        I0 = 1367; Kb = 0.98; Kd = 0.13
        std_longitude = timezone * 15
        EoT = equation_of_time(day_of_year)
        time_correction = (4 * (std_longitude - local_longitude) + EoT) / 60
        decl = solar_declination(day_of_year)
        sunrise, sunset = sunrise_hour(latitude, decl)

        hours_HL = np.linspace(0, 24, 241)
        irradiance = np.zeros_like(hours_HL)

        for i, h_HL in enumerate(hours_HL):
            h_TSL = h_HL + time_correction
            if sunrise <= h_TSL <= sunset:
                omega = 15 * (h_TSL - 12)
                cos_theta = (np.sin(np.deg2rad(latitude)) * np.sin(np.deg2rad(decl)) +
                             np.cos(np.deg2rad(latitude)) * np.cos(np.deg2rad(decl)) * np.cos(np.deg2rad(omega)))
                if cos_theta > 0:
                    Ib = I0 * Kb ** (1 / cos_theta)
                    Id = I0 * Kd * cos_theta
                    irradiance[i] = (Ib * cos_theta + Id) / 1000.0

        model_energy = np.trapezoid(irradiance, hours_HL)
        if model_energy > 0:
            irradiance *= daily_density / model_energy

        full_hours = np.arange(0, 25, 1)
        hourly_irradiance = np.interp(full_hours, hours_HL, irradiance)
        hourly_energy = np.zeros(24)
        for hour in range(24):
            hourly_energy[hour] = (hourly_irradiance[hour] + hourly_irradiance[hour+1]) / 2

        return hourly_energy

    def calculate_monthly_hourly_profile(lat, lon, monthly_values, num_harmonics=6):
        M = len(monthly_values)
        monthly_days = np.linspace(0, 365.25, num=M, endpoint=False) + (365.25 / (2 * M))
        P = 365.25

        A0 = np.mean(monthly_values)
        An = [ (2/M) * np.sum(monthly_values * np.cos(2*np.pi*n*monthly_days/P)) for n in range(1, num_harmonics+1) ]
        Bn = [ (2/M) * np.sum(monthly_values * np.sin(2*np.pi*n*monthly_days/P)) for n in range(1, num_harmonics+1) ]

        days_of_year = np.arange(1, 366)
        daily_densities = [fourier_function(d, P, A0, An, Bn) for d in days_of_year]

        annual_hourly_data = np.zeros((365, 24))
        for day in range(365):
            annual_hourly_data[day] = generate_hourly_profile_day(day + 1, daily_densities[day], lat, lon)

        days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        monthly_means = []
        start = 0
        for days in days_per_month:
            end = start + days
            monthly_means.append(annual_hourly_data[start:end].mean(axis=0))
            start = end

        df_mean = pd.DataFrame(monthly_means, index=month_names, columns=[f"{h:02d}h" for h in range(24)])
        return df_mean.round(6)

    df_mean = calculate_monthly_hourly_profile(lat, lon, values_list)

    # =========================== DOWNLOAD ERA5 ===========================
    print("Downloading ERA5 SSRD (1999–2018)...")
    c = cdsapi.Client(url="https://cds.climate.copernicus.eu/api", key=API_KEY)

    years = [str(y) for y in range(1999, 2019)]
    for year in years:
        fp = os.path.join(output_dir, f"ssrd_{year}.nc")
        if os.path.exists(fp):
            continue
        c.retrieve("reanalysis-era5-single-levels", {
            "product_type": "reanalysis",
            "variable": "surface_solar_radiation_downwards",
            "year": year,
            "month": [f"{m:02d}" for m in range(1,13)],
            "day": [f"{d:02d}" for d in range(1,32)],
            "time": [f"{h:02d}:00" for h in range(24)],
            "area": [lat, lon, lat, lon],
            "format": "netcdf"
        }, fp)

    # =========================== GRAPHICS ===========================
    cmap = sns.color_palette("turbo", as_cmap=True)

    def save_clean_heatmap(data, base_name, cbar_label, fmt=".4f"):
        plt.figure(figsize=(16, 8))
        sns.heatmap(data, annot=True, fmt=fmt, cmap=cmap, linewidths=0.5,
                    cbar_kws={'label': cbar_label, 'shrink': 0.8},
                    annot_kws={'size': 9})
        plt.xlabel("Hour of Day", fontsize=12)
        plt.ylabel("Month", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        path = os.path.join(figures_pdf_folder, f"{base_name}_{lat_str}_{lon_str}.pdf")
        plt.savefig(path, format='pdf', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved: {os.path.basename(path)}")

    save_clean_heatmap(df_mean, "Solar_Monthly_Average_PV_Density", "PV Production Density (kWh/m²)")

    # 3D
    X, Y = np.meshgrid(np.arange(24), np.arange(12))
    Z = df_mean.values

    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='turbo', edgecolor='k', linewidth=0.3, alpha=0.9)
    ax.set_xlabel('Hour of Day', labelpad=15)
    ax.set_ylabel('Month', labelpad=15)
    ax.set_zlabel('PV Production\n(kWh/m²)', labelpad=15)
    ax.set_xticks(np.arange(0, 24, 3))
    ax.set_xticklabels([f"{h:02d}h" for h in range(0, 24, 3)])
    ax.set_yticks(np.arange(12))
    ax.set_yticklabels(month_names)
    ax.view_init(elev=30, azim=-60)
    fig.colorbar(surf, shrink=0.6, pad=0.1, label='PV Production (kWh/m²)')
    plt.tight_layout()
    plt.savefig(os.path.join(figures_pdf_folder, f"Solar_PV_Production_3D_{lat_str}_{lon_str}.pdf"), dpi=300)
    plt.close()

    # HTML interativo
    figly = go.Figure(data=[go.Surface(z=Z, colorscale='Turbo')])
    figly.update_layout(scene=dict(xaxis_title="Hour", yaxis_title="Month", zaxis_title="PV Production (kWh/m²)"),
                        width=1200, height=800)
    figly.write_html(os.path.join(figures_pdf_folder, f"Solar_PV_Production_3D_{lat_str}_{lon_str}.html"))

    print(f"\nSOLAR ANALYSIS COMPLETED!\nAll files in: {figures_pdf_folder}\n")
    print(f"{'='*70}\n")


#if __name__ == "__main__":
    #API_KEY = "SUA_CHAVE_AQUI_PARA_TESTE"
    #run_solar_analysis(-3.73, -38.52, API_KEY)