"""
Solar position and timing calculations.

This module calculates the position of the sun at a specific location and time,
including sunrise, sunset, and civil twilight times.
"""

from astropy.coordinates import EarthLocation, AltAz, get_body
from astropy.time import Time
from astropy import units as u
import numpy as np
from datetime import datetime, timedelta
import pytz


class SolarCalculator:
    """Calculate solar position and timing for a given location."""

    def __init__(self, latitude: float, longitude: float, elevation: float):
        """
        Initialize the solar calculator.

        Args:
            latitude: Latitude in degrees (-90 to 90, negative for south)
            longitude: Longitude in degrees (-180 to 180, negative for west)
            elevation: Elevation in meters above sea level
        """
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.location = EarthLocation(
            lat=latitude * u.deg, lon=longitude * u.deg, height=elevation * u.m
        )

    def get_solar_position(self, dt: datetime) -> dict:
        """
        Get the sun's position at a specific date and time.

        Args:
            dt: Datetime in UTC

        Returns:
            Dictionary with 'altitude' and 'azimuth' in degrees
        """
        t = Time(dt)
        sun = get_body("sun", t, self.location)
        altaz = sun.transform_to(AltAz(obstime=t, location=self.location))

        return {
            "altitude": float(altaz.alt.deg),
            "azimuth": float(altaz.az.deg),
            "time": dt.isoformat(),
        }

    def find_sunset_time(self, dt: datetime, step_minutes: int = 1) -> datetime:
        """
        Find the exact time when the sun crosses the horizon (altitude = 0).

        Args:
            dt: Starting date/time (UTC)
            step_minutes: Search step in minutes (smaller = more accurate but slower)

        Returns:
            Datetime when sun altitude crosses 0 degrees
        """
        # Start from noon and search forward
        search_start = dt.replace(hour=12, minute=0, second=0, microsecond=0)
        current_time = search_start
        prev_altitude = self.get_solar_position(current_time)["altitude"]

        # Search forward
        while current_time.day == dt.day:
            current_time += timedelta(minutes=step_minutes)
            current_altitude = self.get_solar_position(current_time)["altitude"]

            # Check if we crossed the horizon
            if prev_altitude > 0 and current_altitude <= 0:
                # Binary search for exact crossing time
                return self._binary_search_horizon_crossing(
                    current_time - timedelta(minutes=step_minutes), current_time
                )

            prev_altitude = current_altitude

            if current_time.hour >= 23:
                break

        return None

    def _binary_search_horizon_crossing(
        self, time_before: datetime, time_after: datetime, tolerance_seconds: int = 1
    ) -> datetime:
        """
        Use binary search to find exact horizon crossing time.

        Args:
            time_before: Time when sun was above horizon
            time_after: Time when sun was below horizon
            tolerance_seconds: Stop searching when within this tolerance

        Returns:
            Datetime of horizon crossing
        """
        while (time_after - time_before).total_seconds() > tolerance_seconds:
            mid_time = time_before + (time_after - time_before) / 2
            altitude = self.get_solar_position(mid_time)["altitude"]

            if altitude > 0:
                time_before = mid_time
            else:
                time_after = mid_time

        return time_after

    def get_civil_twilight_times(self, dt: datetime) -> dict:
        """
        Get civil twilight times (sun at -6 degrees below horizon).

        Args:
            dt: Date (UTC)

        Returns:
            Dictionary with 'civil_dusk' and 'civil_dawn'
        """
        # Search for when altitude crosses -6 degrees
        return {
            "civil_dusk": self._find_altitude_crossing(dt, -6, search_forward=True),
            "civil_dawn": self._find_altitude_crossing(
                dt - timedelta(days=1), -6, search_forward=False
            ),
        }

    def _find_altitude_crossing(
        self, dt: datetime, target_altitude: float, search_forward: bool = True
    ) -> datetime:
        """Find when sun crosses a specific altitude."""
        step = 1 if search_forward else -1
        current_time = dt.replace(hour=12, minute=0, second=0, microsecond=0)

        prev_altitude = self.get_solar_position(current_time)["altitude"]
        prev_diff = prev_altitude - target_altitude

        while True:
            current_time += timedelta(hours=step)
            current_altitude = self.get_solar_position(current_time)["altitude"]
            current_diff = current_altitude - target_altitude

            # Check for crossing
            if prev_diff * current_diff <= 0:
                # Found crossing, binary search for exact time
                return self._binary_search_altitude_crossing(
                    current_time - timedelta(hours=step),
                    current_time,
                    target_altitude,
                )

            prev_altitude = current_altitude
            prev_diff = current_diff

            # Prevent infinite loops
            if abs((current_time - dt).days) > 1:
                return None

    def _binary_search_altitude_crossing(
        self,
        time_before: datetime,
        time_after: datetime,
        target_altitude: float,
        tolerance_seconds: int = 1,
    ) -> datetime:
        """Binary search for a specific altitude crossing."""
        while (time_after - time_before).total_seconds() > tolerance_seconds:
            mid_time = time_before + (time_after - time_before) / 2
            altitude = self.get_solar_position(mid_time)["altitude"]

            if altitude > target_altitude:
                time_before = mid_time
            else:
                time_after = mid_time

        return time_after
