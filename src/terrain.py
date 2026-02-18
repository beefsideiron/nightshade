"""
Terrain obstruction calculations.

This module handles elevation profile data and determines if the sun
is blocked by terrain at a given azimuth.
"""

import numpy as np
from typing import Dict, List, Tuple
import json


class TerrainProfile:
    """Represent the elevation profile around a location."""

    def __init__(self):
        """Initialize an empty terrain profile."""
        self.elevations: Dict[float, float] = {}  # azimuth -> elevation (degrees)
        self.reference_elevation = 0  # elevation at the observation point (meters)

    def add_elevation_point(
        self, azimuth: float, elevation_angle: float, distance: float = None
    ):
        """
        Add an elevation point to the terrain profile.

        Args:
            azimuth: Direction in degrees (0-360, 0=north, 90=east, 180=south, 270=west)
            elevation_angle: Angle above horizon in degrees (negative is below)
            distance: Optional distance to the obstruction (for reference)
        """
        # Normalize azimuth to 0-360
        azimuth = azimuth % 360
        self.elevations[azimuth] = elevation_angle

    def load_from_dict(self, data: Dict[float, float], reference_elevation: float = 0):
        """
        Load terrain profile from a dictionary.

        Args:
            data: Dictionary mapping azimuth (degrees) to elevation angle (degrees)
            reference_elevation: Reference elevation at observation point (meters)
        """
        self.elevations = {float(k): float(v) for k, v in data.items()}
        self.reference_elevation = reference_elevation

    def load_from_file(self, filepath: str):
        """
        Load terrain profile from a JSON file.

        Args:
            filepath: Path to JSON file with elevation profile
        """
        with open(filepath, "r") as f:
            data = json.load(f)
        self.load_from_dict(
            data.get("elevations", {}),
            data.get("reference_elevation", 0),
        )

    def get_obstruction_angle(self, azimuth: float) -> float:
        """
        Get the obstruction angle at a given azimuth.

        Args:
            azimuth: Direction in degrees (0-360)

        Returns:
            Elevation angle of obstruction (degrees above horizon)
        """
        azimuth = azimuth % 360

        # If exact azimuth is in profile, return it
        if azimuth in self.elevations:
            return self.elevations[azimuth]

        # Otherwise, interpolate between nearby azimuths
        azimuths = sorted(self.elevations.keys())

        # Find the two nearest azimuths
        idx = None
        for i, az in enumerate(azimuths):
            if az > azimuth:
                idx = i
                break

        if idx is None:
            # Beyond the last azimuth, wrap around
            az1 = azimuths[-1]
            az2 = azimuths[0]
            el1 = self.elevations[az1]
            el2 = self.elevations[az2]

            # Linear interpolation with wrap-around
            frac = (azimuth - az1) / (360 + az2 - az1)
        elif idx == 0:
            # Before the first azimuth
            return self.elevations[azimuths[0]]
        else:
            az1 = azimuths[idx - 1]
            az2 = azimuths[idx]
            el1 = self.elevations[az1]
            el2 = self.elevations[az2]

            frac = (azimuth - az1) / (az2 - az1)

        # Linear interpolation
        return el1 + frac * (el2 - el1)

    def is_sun_blocked(self, sun_altitude: float, sun_azimuth: float) -> bool:
        """
        Determine if the sun is blocked by terrain.

        Args:
            sun_altitude: Sun's altitude above horizon (degrees)
            sun_azimuth: Sun's azimuth direction (degrees)

        Returns:
            True if terrain blocks the sun
        """
        obstruction_angle = self.get_obstruction_angle(sun_azimuth)
        return sun_altitude <= obstruction_angle

    def find_unobstructed_sunset(
        self, solar_positions: List[Dict], time_step_minutes: int = 1
    ) -> Tuple[str, float, float]:
        """
        Find the time when the sun is no longer visible due to terrain obstruction.

        Args:
            solar_positions: List of solar position dicts with time, altitude, azimuth
            time_step_minutes: Time step between positions (for reference)

        Returns:
            Tuple of (iso_time_string, altitude, azimuth) when sun last visible
        """
        last_unobstructed = None

        for position in solar_positions:
            if not self.is_sun_blocked(position["altitude"], position["azimuth"]):
                last_unobstructed = position

        return last_unobstructed
