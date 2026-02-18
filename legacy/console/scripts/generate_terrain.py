"""
Terrain profile generator using Open-Elevation API.

Fetches elevation data around a location and generates a terrain obstruction profile.
"""

import requests
import math
import json
from datetime import datetime


def get_elevation_at_point(lat: float, lon: float) -> float:
    """
    Get elevation at a specific coordinate using Open-Elevation API.

    Args:
        lat: Latitude in degrees
        lon: Longitude in degrees

    Returns:
        Elevation in meters, or None if query fails
    """
    try:
        url = "https://api.open-elevation.com/api/v1/lookup"
        params = {"locations": f"{lat},{lon}"}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                return data["results"][0]["elevation"]
    except Exception as e:
        print(f"  Warning: Could not fetch elevation: {e}")
    
    return None


def calculate_elevation_angle(
    observer_lat: float,
    observer_lon: float,
    observer_elev: float,
    target_lat: float,
    target_lon: float,
    target_elev: float,
) -> float:
    """
    Calculate the angle of elevation from observer to target.

    Args:
        observer_lat/lon: Observer position
        observer_elev: Observer elevation in meters
        target_lat/lon: Target position
        target_elev: Target elevation in meters

    Returns:
        Elevation angle in degrees (0 = horizon, >0 = above, <0 = below)
    """
    # Calculate horizontal distance using Haversine formula
    R = 6371000  # Earth radius in meters
    
    lat1_rad = math.radians(observer_lat)
    lat2_rad = math.radians(target_lat)
    delta_lat = math.radians(target_lat - observer_lat)
    delta_lon = math.radians(target_lon - observer_lon)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    horizontal_distance = R * c
    
    # Calculate vertical distance
    vertical_distance = target_elev - observer_elev
    
    # Calculate elevation angle
    if horizontal_distance == 0:
        return 0
    
    angle_rad = math.atan(vertical_distance / horizontal_distance)
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg


def azimuth_between_points(
    observer_lat: float,
    observer_lon: float,
    target_lat: float,
    target_lon: float,
) -> float:
    """
    Calculate the azimuth (bearing) from observer to target.

    Args:
        observer_lat/lon: Observer position
        target_lat/lon: Target position

    Returns:
        Azimuth in degrees (0 = north, 90 = east, 180 = south, 270 = west)
    """
    lat1_rad = math.radians(observer_lat)
    lat2_rad = math.radians(target_lat)
    delta_lon = math.radians(target_lon - observer_lon)
    
    x = math.sin(delta_lon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)
    
    azimuth_rad = math.atan2(x, y)
    azimuth_deg = math.degrees(azimuth_rad)
    
    # Normalize to 0-360
    return (azimuth_deg + 360) % 360


def generate_terrain_profile(
    lat: float,
    lon: float,
    elev: float,
    max_distance_km: float = 10,
    num_azimuths: int = 36,
    samples_per_azimuth: int = 5,
    output_file: str = "data/user_terrain.json",
) -> dict:
    """
    Generate a terrain elevation profile around a location.

    Args:
        lat/lon: Observer position
        elev: Observer elevation in meters
        max_distance_km: Maximum distance to query
        num_azimuths: Number of azimuths to sample (e.g., 36 = every 10°)
        samples_per_azimuth: Number of distance samples per azimuth
        output_file: Where to save the terrain profile JSON

    Returns:
        Terrain profile dictionary
    """
    terrain_profile = {
        "location": {
            "latitude": lat,
            "longitude": lon,
            "elevation": elev,
            "generation_date": datetime.utcnow().isoformat(),
        },
        "elevations": {},
        "metadata": {
            "max_distance_km": max_distance_km,
            "num_azimuths": num_azimuths,
            "samples_per_azimuth": samples_per_azimuth,
        },
    }

    print(f"\nGenerating terrain profile for {lat}, {lon} (elev: {elev}m)")
    print(f"Sampling {num_azimuths} azimuths with {samples_per_azimuth} distance samples each")
    print(f"Max distance: {max_distance_km}km\n")

    # Sample at each azimuth
    for azimuth_idx in range(num_azimuths):
        azimuth = (360 / num_azimuths) * azimuth_idx
        
        max_elevation_angle = -90  # Start with lowest possible angle
        
        # Sample at different distances along this azimuth
        for distance_idx in range(1, samples_per_azimuth + 1):
            distance_km = (max_distance_km / samples_per_azimuth) * distance_idx
            
            # Convert azimuth and distance to lat/lon offset
            # Using simple approximation for small distances
            delta_km = distance_km
            cos_azimuth = math.cos(math.radians(azimuth))
            sin_azimuth = math.sin(math.radians(azimuth))
            
            # Rough conversion: 1 degree ≈ 111 km
            delta_lat = (delta_km / 111) * cos_azimuth
            delta_lon = (delta_km / 111) * sin_azimuth / math.cos(math.radians(lat))
            
            target_lat = lat + delta_lat
            target_lon = lon + delta_lon
            
            # Get elevation at this point
            target_elev = get_elevation_at_point(target_lat, target_lon)
            
            if target_elev is not None:
                # Calculate elevation angle
                elev_angle = calculate_elevation_angle(
                    lat, lon, elev, target_lat, target_lon, target_elev
                )
                
                # Keep the maximum elevation angle (highest obstruction)
                max_elevation_angle = max(max_elevation_angle, elev_angle)
                
                print(f"  Azimuth {azimuth:6.1f}° at {distance_km:5.1f}km: "
                      f"elev={target_elev:6.0f}m, angle={elev_angle:6.2f}°")
            else:
                print(f"  Azimuth {azimuth:6.1f}° at {distance_km:5.1f}km: "
                      f"Could not fetch elevation")
        
        # Store the maximum elevation angle for this azimuth
        terrain_profile["elevations"][round(azimuth, 1)] = round(max_elevation_angle, 2)
        print(f"  → Max elevation at {azimuth:6.1f}°: {max_elevation_angle:6.2f}°\n")

    # Save to file
    with open(output_file, "w") as f:
        json.dump(terrain_profile, f, indent=2)
    
    print(f"\nTerrain profile saved to {output_file}")
    return terrain_profile


if __name__ == "__main__":
    # User's location from config
    LAT = 36.810354
    LON = -4.222430
    ELEV = 221

    profile = generate_terrain_profile(
        lat=LAT,
        lon=LON,
        elev=ELEV,
        max_distance_km=20,
        num_azimuths=36,  # Every 10 degrees
        samples_per_azimuth=5,
        output_file="data/user_terrain.json",
    )

    print("\nTerrain Profile Summary:")
    print(f"Total azimuths sampled: {len(profile['elevations'])}")
    print(f"Min elevation angle: {min(profile['elevations'].values()):.2f}°")
    print(f"Max elevation angle: {max(profile['elevations'].values()):.2f}°")
