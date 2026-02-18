"""
SunPredict: Console application for predicting sunlight loss.

This module provides the main CLI for predicting when direct sunlight
is no longer visible at a given location.
"""

from datetime import datetime, timedelta
from src.solar import SolarCalculator
from src.terrain import TerrainProfile
import argparse
import sys
import json
import os
import pytz


def predict_sunlight_loss(
    latitude: float,
    longitude: float,
    elevation: float,
    date: datetime = None,
    terrain_file: str = None,
    timezone: str = "UTC",
) -> dict:
    """
    Predict when direct sunlight is visible at a location.

    Args:
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        elevation: Elevation in meters
        date: Date to predict (defaults to today)
        terrain_file: Optional JSON file with terrain elevation profile
        timezone: Timezone string (e.g., 'Europe/Madrid', 'UTC')

    Returns:
        Dictionary with prediction results (sunrise and sunset)
    """
    if date is None:
        date = datetime.utcnow()

    # Initialize solar calculator
    solar_calc = SolarCalculator(latitude, longitude, elevation)

    # Load terrain profile if provided
    terrain = TerrainProfile()
    if terrain_file:
        terrain.load_from_file(terrain_file)

    # Generate solar positions throughout the day
    solar_positions = []
    current_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = current_time + timedelta(hours=24)

    while current_time < end_time:
        pos = solar_calc.get_solar_position(current_time)
        if terrain_file:
            # Only include positions not blocked by terrain
            if not terrain.is_sun_blocked(pos["altitude"], pos["azimuth"]):
                solar_positions.append(pos)
        else:
            # Include all positions above horizon
            if pos["altitude"] > 0:
                solar_positions.append(pos)

        current_time += timedelta(minutes=1)

    # Find sunrise (first visible sunlight)
    sunrise_time = None
    sunrise_altitude = None
    sunrise_azimuth = None
    if solar_positions:
        first_position = solar_positions[0]
        sunrise_time = datetime.fromisoformat(first_position["time"])
        sunrise_altitude = first_position["altitude"]
        sunrise_azimuth = first_position["azimuth"]

    # Find sunset (last visible sunlight)
    sunset_time = None
    sunset_altitude = None
    sunset_azimuth = None
    if solar_positions:
        last_position = solar_positions[-1]
        sunset_time = datetime.fromisoformat(last_position["time"])
        sunset_altitude = last_position["altitude"]
        sunset_azimuth = last_position["azimuth"]

    return {
        "location": {"latitude": latitude, "longitude": longitude, "elevation": elevation},
        "date": date.isoformat(),
        "timezone": timezone,
        "has_sunlight": len(solar_positions) > 0,
        "first_direct_sunlight": sunrise_time.isoformat() if sunrise_time else None,
        "sun_altitude_at_rise": sunrise_altitude,
        "sun_azimuth_at_rise": sunrise_azimuth,
        "last_direct_sunlight": sunset_time.isoformat() if sunset_time else None,
        "sun_altitude_at_loss": sunset_altitude,
        "sun_azimuth_at_loss": sunset_azimuth,
        "terrain_obstruction": terrain_file is not None,
    }


def format_time(dt: datetime, timezone: str = "UTC") -> str:
    """Format datetime as HH:MM in the specified timezone."""
    if dt is None:
        return "N/A"
    
    # If dt is naive (no timezone), assume UTC
    if dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)
    
    # Convert to target timezone
    try:
        tz = pytz.timezone(timezone)
        dt_local = dt.astimezone(tz)
        return dt_local.strftime("%H:%M")
    except:
        # Fallback if timezone is invalid
        return dt.strftime("%H:%M")


def load_config(config_file: str = "config.json") -> dict:
    """Load configuration from JSON file."""
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return {}


def main():
    """Main entry point for the CLI."""
    # Load default configuration
    config = load_config()
    default_lat = None
    default_lon = None
    default_elev = None
    default_tz = "UTC"
    default_terrain = None
    
    if "location" in config:
        default_lat = config["location"].get("latitude")
        default_lon = config["location"].get("longitude")
        default_elev = config["location"].get("elevation")
        default_tz = config["location"].get("timezone", "UTC")
    
    if "prediction" in config:
        if config["prediction"].get("include_terrain", False):
            default_terrain = config["prediction"].get("terrain_file")
    
    parser = argparse.ArgumentParser(
        description="Predict when direct sunlight will no longer reach a location."
    )
    parser.add_argument(
        "latitude",
        type=float,
        nargs="?",
        default=default_lat,
        help="Latitude in degrees (uses config if not provided)",
    )
    parser.add_argument(
        "longitude",
        type=float,
        nargs="?",
        default=default_lon,
        help="Longitude in degrees (uses config if not provided)",
    )
    parser.add_argument(
        "elevation",
        type=float,
        nargs="?",
        default=default_elev,
        help="Elevation in meters (uses config if not provided)",
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date in YYYY-MM-DD format (defaults to today)",
    )
    parser.add_argument(
        "--terrain",
        type=str,
        default=default_terrain,
        help="JSON file with terrain elevation profile",
    )
    parser.add_argument(
        "--timezone",
        type=str,
        default=default_tz,
        help="Timezone for output (e.g., Europe/Madrid, UTC)",
    )

    args = parser.parse_args()

    # Validate that we have coordinates
    if args.latitude is None or args.longitude is None or args.elevation is None:
        print("Error: Latitude, longitude, and elevation are required.", file=sys.stderr)
        print("       Provide them as arguments or add them to config.json", file=sys.stderr)
        sys.exit(1)

    # Parse date if provided
    date = None
    if args.date:
        try:
            date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("Error: Date must be in YYYY-MM-DD format")
            sys.exit(1)

    # Run prediction
    try:
        result = predict_sunlight_loss(
            args.latitude,
            args.longitude,
            args.elevation,
            date,
            args.terrain,
            args.timezone,
        )

        # Format output
        print("\n" + "=" * 60)
        print("SUNPREDICT - Sunlight Loss Prediction")
        print("=" * 60)
        print(f"\nLocation:")
        print(f"  Latitude:  {result['location']['latitude']:.4f}°")
        print(f"  Longitude: {result['location']['longitude']:.4f}°")
        print(f"  Elevation: {result['location']['elevation']:.0f}m")
        print(f"\nDate: {result['date']}")
        print(f"Timezone: {result['timezone']}")

        if result["has_sunlight"]:
            sunrise_time = datetime.fromisoformat(result['first_direct_sunlight'])
            sunset_time = datetime.fromisoformat(result['last_direct_sunlight'])
            sunrise_local = format_time(sunrise_time, result['timezone'])
            sunset_local = format_time(sunset_time, result['timezone'])
            
            print(f"\nDirect sunlight window:")
            print(f"  Sunrise (becomes visible):  {sunrise_local} {result['timezone']}")
            print(f"    Sun altitude: {result['sun_altitude_at_rise']:.2f}°")
            print(f"    Sun azimuth:  {result['sun_azimuth_at_rise']:.2f}°")
            print(f"\n  Sunset (becomes hidden):    {sunset_local} {result['timezone']}")
            print(f"    Sun altitude: {result['sun_altitude_at_loss']:.2f}°")
            print(f"    Sun azimuth:  {result['sun_azimuth_at_loss']:.2f}°")
            
            if result["terrain_obstruction"]:
                print(f"\n  (Including terrain obstruction)")
        else:
            print("\nNo direct sunlight on this date.")

        print("\n" + "=" * 60 + "\n")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
