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
import logging
from pathlib import Path


def setup_logging():
    """Setup logging to both file and console."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"sunpredict_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Custom formatter with Europe/Madrid timezone (UTC+1)
    class MadridFormatter(logging.Formatter):
        def formatTime(self, record, datefmt=None):
            dt = datetime.fromtimestamp(record.created)
            tz = pytz.timezone('Europe/Madrid')
            dt_madrid = tz.normalize(tz.localize(dt))
            if datefmt:
                return dt_madrid.strftime(datefmt)
            return dt_madrid.strftime('%Y-%m-%d %H:%M:%S')
    
    formatter = MadridFormatter('%(asctime)s +01:00 - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.handlers = []  # Clear existing handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def predict_sunlight_loss(
    latitude: float,
    longitude: float,
    elevation: float,
    date: datetime = None,
    terrain_file: str = None,
    timezone: str = "UTC",
    logger = None,
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
        logger: Optional logger for output

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

    # Get civil twilight times (sun at -6 degrees)
    civil_twilight = solar_calc.get_civil_twilight_times(date)
    civil_dawn = civil_twilight["civil_dawn"]
    civil_dusk = civil_twilight["civil_dusk"]

    # Generate solar positions throughout the day
    solar_positions = []
    current_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = current_time + timedelta(hours=24)

    while current_time < end_time:
        pos = solar_calc.get_solar_position(current_time)
        # Include all positions above horizon (0° altitude)
        if pos["altitude"] > 0:
            solar_positions.append(pos)

        current_time += timedelta(minutes=1)

    # Find sunrise/sunset based on horizon (0° altitude)
    sunrise_time = None
    sunrise_altitude = None
    sunrise_azimuth = None
    if solar_positions:
        first_position = solar_positions[0]
        sunrise_time = datetime.fromisoformat(first_position["time"])
        sunrise_altitude = first_position["altitude"]
        sunrise_azimuth = first_position["azimuth"]

    # Find sunset based on horizon (0° altitude)
    sunset_time = None
    sunset_altitude = None
    sunset_azimuth = None
    if solar_positions:
        last_position = solar_positions[-1]
        sunset_time = datetime.fromisoformat(last_position["time"])
        sunset_altitude = last_position["altitude"]
        sunset_azimuth = last_position["azimuth"]

    # Find terrain obstruction time (if terrain file provided)
    terrain_obstruction_time = None
    terrain_obstruction_altitude = None
    terrain_obstruction_azimuth = None
    if terrain_file:
        # Generate all positions throughout the day
        all_positions = []
        current_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = current_time + timedelta(hours=24)
        
        while current_time < end_time:
            pos = solar_calc.get_solar_position(current_time)
            if pos["altitude"] > 0:
                all_positions.append(pos)
            current_time += timedelta(minutes=1)
        
        # Find last position not blocked by terrain
        last_unblocked = None
        for pos in all_positions:
            if not terrain.is_sun_blocked(pos["altitude"], pos["azimuth"]):
                last_unblocked = pos
        
        if last_unblocked:
            terrain_obstruction_time = datetime.fromisoformat(last_unblocked["time"])
            terrain_obstruction_altitude = last_unblocked["altitude"]
            terrain_obstruction_azimuth = last_unblocked["azimuth"]

    return {
        "location": {"latitude": latitude, "longitude": longitude, "elevation": elevation},
        "date": date.isoformat(),
        "timezone": timezone,
        "has_sunlight": len(solar_positions) > 0,
        "terrain_sunset": terrain_obstruction_time.isoformat() if terrain_obstruction_time else None,
        "terrain_sunset_altitude": terrain_obstruction_altitude,
        "terrain_sunset_azimuth": terrain_obstruction_azimuth,
        "civil_dawn": civil_dawn.isoformat() if civil_dawn else None,
        "civil_dusk": civil_dusk.isoformat() if civil_dusk else None,
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
    # Setup logging
    logger = setup_logging()
    
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
        "--days",
        type=int,
        default=1,
        help="Number of days to predict from the specified date (default: 1)",
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
    else:
        date = datetime.utcnow()

    # Run predictions
    try:
        logger.info(f"Starting prediction for {args.days} day(s) from {date.strftime('%Y-%m-%d')}")
        logger.info(f"Location: {args.latitude:.4f}°N, {args.longitude:.4f}°W, Elevation: {args.elevation:.0f}m")
        logger.info(f"Timezone: {args.timezone}")
        
        print("\n" + "=" * 70)
        print("SUNPREDICT - Sunlight Loss Prediction")
        print("=" * 70)
        print(f"\nLocation:")
        print(f"  Latitude:  {args.latitude:.4f}°")
        print(f"  Longitude: {args.longitude:.4f}°")
        print(f"  Elevation: {args.elevation:.0f}m")
        print(f"\nTimezone: {args.timezone}")
        if args.terrain:
            print(f"Terrain profile: {args.terrain}")
        
        print("\n" + "=" * 70)
        
        current_date = date
        for day_offset in range(args.days):
            current_date = date + timedelta(days=day_offset)
            
            result = predict_sunlight_loss(
                args.latitude,
                args.longitude,
                args.elevation,
                current_date,
                args.terrain,
                args.timezone,
                logger,
            )

            # Format output
            print(f"\n📅 Date: {current_date.strftime('%A, %Y-%m-%d')}")
            print("-" * 70)

            if result["has_sunlight"] and result["terrain_sunset"]:
                terrain_sunset_dt = datetime.fromisoformat(result['terrain_sunset'])
                civil_dawn = datetime.fromisoformat(result['civil_dawn']) if result['civil_dawn'] else None
                civil_dusk = datetime.fromisoformat(result['civil_dusk']) if result['civil_dusk'] else None
                
                terrain_sunset_local = format_time(terrain_sunset_dt, result['timezone'])
                civil_dawn_local = format_time(civil_dawn, result['timezone']) if civil_dawn else "N/A"
                civil_dusk_local = format_time(civil_dusk, result['timezone']) if civil_dusk else "N/A"
                
                print(f"\n☀️  SUNSET (Horizon - 0° altitude):")
                print(f"  Sunrise:  {sunrise_local} {result['timezone']}")
                print(f"    Altitude: {result['sun_altitude_at_rise']:.2f}°, Azimuth: {result['sun_azimuth_at_rise']:.2f}°")
                print(f"\n  Sunset:   {sunset_local} {result['timezone']}")
                print(f"    Altitude: {result['sun_altitude_at_set']:.2f}°, Azimuth: {result['sun_azimuth_at_set']:.2f}°")
                
                if result["terrain_obstruction"] and result['terrain_obstruction_time']:
                    print(f"\n⛰️  TERRAIN OBSTRUCTION:")
                    print(f"  Direct sunlight lost: {terrain_obstruction_local} {result['timezone']}")
                    print(f"    Altitude: {result['sun_altitude_at_obstruction']:.2f}°, Azimuth: {result['sun_azimuth_at_obstruction']:.2f}°")
                
                print(f"\n🌆 CIVIL TWILIGHT (sun at -6°):")
                # Ensure civil twilight times are properly converted from UTC to local timezone
                if civil_dawn and civil_dawn.tzinfo is None:
                    civil_dawn = pytz.UTC.localize(civil_dawn)
                if civil_dusk and civil_dusk.tzinfo is None:
                    civil_dusk = pytz.UTC.localize(civil_dusk)
                
                civil_dawn_tz = civil_dawn.astimezone(pytz.timezone(result['timezone'])) if civil_dawn else None
                civil_dusk_tz = civil_dusk.astimezone(pytz.timezone(result['timezone'])) if civil_dusk else None
                
                civil_dawn_local = civil_dawn_tz.strftime("%H:%M") if civil_dawn_tz else "N/A"
                civil_dusk_local = civil_dusk_tz.strftime("%H:%M") if civil_dusk_tz else "N/A"
                
                print(f"  Civil Dawn:  {civil_dawn_local} {result['timezone']}")
                print(f"  Civil Dusk:  {civil_dusk_local} {result['timezone']}")
                
                if result["terrain_obstruction"]:
                    print(f"\n  (Calculated with terrain profile)")
                
                # Convert civil twilight times from UTC to local for logging
                if civil_dawn and civil_dawn.tzinfo is None:
                    civil_dawn_utc = pytz.UTC.localize(civil_dawn)
                else:
                    civil_dawn_utc = civil_dawn
                    
                if civil_dusk and civil_dusk.tzinfo is None:
                    civil_dusk_utc = pytz.UTC.localize(civil_dusk)
                else:
                    civil_dusk_utc = civil_dusk
                    
                local_tz = pytz.timezone(result['timezone'])
                civil_dawn_tz = civil_dawn_utc.astimezone(local_tz) if civil_dawn_utc else None
                civil_dusk_tz = civil_dusk_utc.astimezone(local_tz) if civil_dusk_utc else None
                
                civil_dawn_log = civil_dawn_tz.strftime("%H:%M") if civil_dawn_tz else "N/A"
                civil_dusk_log = civil_dusk_tz.strftime("%H:%M") if civil_dusk_tz else "N/A"
                
                # Log to file
                logger.info(f"Date: {current_date.strftime('%Y-%m-%d')}")
                logger.info(f"  Horizon Sunset - Sunrise: {sunrise_local}, Sunset: {sunset_local}")
                if result["terrain_obstruction"] and result['terrain_obstruction_time']:
                    logger.info(f"  Terrain Obstruction: {terrain_obstruction_local}")
                logger.info(f"  Civil Twilight - Dawn: {civil_dawn_log}, Dusk: {civil_dusk_log}")
            else:
                print("\n❌ No direct sunlight on this date.")
                logger.info(f"Date: {current_date.strftime('%Y-%m-%d')} - No direct sunlight")

        print("\n" + "=" * 70 + "\n")
        logger.info("Prediction complete")

    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
