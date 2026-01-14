# main.py
# Unified launcher for Solar and Wind energy analysis
# Run with: python main.py --lat -3.73 --lon -38.52

import argparse
from solar_analysis import run_solar_analysis
from wind_analysis import run_wind_analysis


# ===================================================================
# IMPORTANT: INSERT YOUR CDS API KEY HERE (from https://cds.climate.copernicus.eu/user)
# ===================================================================
API_KEY = "ad0a1185-6e14-4cbb-bcdb-5ebfd4bd8faf"  # ← INSERT YOU KEY HERE


def main():
    parser = argparse.ArgumentParser(
        description="Run Solar and/or Wind energy analysis for a given coordinate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                        → Runs both analyses for Fortaleza (-3.73, -38.52)
  python main.py --lat -5.0 --lon -40.0  → Custom coordinate
  python main.py --solar-only           → Only solar analysis
  python main.py --wind-only            → Only wind analysis

Note: Make sure you have inserted your CDS API key in API_KEY above.
""",
    )

    parser.add_argument(
        "--lat",
        type=float,
        default=-3.73,
        help="Latitude of interest (default: -3.73 - Fortaleza)",
    )
    parser.add_argument(
        "--lon",
        type=float,
        default=-38.52,
        help="Longitude of interest (default: -38.52 - Fortaleza)",
    )
    parser.add_argument(
        "--solar-only", action="store_true", help="Run only the solar analysis"
    )
    parser.add_argument(
        "--wind-only", action="store_true", help="Run only the wind analysis"
    )

    args = parser.parse_args()

    lat = round(args.lat, 6)
    lon = round(args.lon, 6)

    print("=" * 70)
    print("HYBRID SOLAR + WIND ENERGY ANALYSIS LAUNCHER")
    print(f"Point of interest: Latitude {lat}°, Longitude {lon}°")
    print(
        f"CDS API Key loaded: {'Yes' if API_KEY and API_KEY != '12345:abcdef...' else 'NO - INSERT YOUR KEY!'}"
    )
    print("=" * 70)

    if not args.wind_only:
        print("\n→ Starting SOLAR analysis...")
        run_solar_analysis(lat, lon, API_KEY)

    if not args.solar_only:
        print("\n→ Starting WIND analysis...")
        run_wind_analysis(lat, lon, API_KEY)

    print("\n" + "=" * 70)
    print("ALL ANALYSES COMPLETED SUCCESSFULLY!")
    print("PDF and HTML reports saved in: ./output/figures_pdf/")
    print("=" * 70)


if __name__ == "__main__":
    main()
