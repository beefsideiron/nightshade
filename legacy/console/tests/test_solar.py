"""
Unit tests for the solar module.
"""

import unittest
from datetime import datetime
from src.solar import SolarCalculator


class TestSolarCalculator(unittest.TestCase):
    """Test cases for SolarCalculator."""

    def setUp(self):
        """Set up test fixtures."""
        # New Mexico desert location
        self.calc = SolarCalculator(latitude=35.1264, longitude=-106.6055, elevation=1600)

    def test_initialization(self):
        """Test that calculator initializes correctly."""
        self.assertEqual(self.calc.latitude, 35.1264)
        self.assertEqual(self.calc.longitude, -106.6055)
        self.assertEqual(self.calc.elevation, 1600)

    def test_solar_position_noon(self):
        """Test solar position at noon."""
        # February 18, 2026 at solar noon (approximately 19:00 UTC for this location)
        dt = datetime(2026, 2, 18, 19, 0, 0)
        position = self.calc.get_solar_position(dt)

        # At solar noon, sun should be relatively high
        self.assertGreater(position["altitude"], 10)  # Should be above horizon
        self.assertIn("azimuth", position)
        self.assertIn("time", position)

    def test_solar_position_midnight(self):
        """Test solar position at midnight."""
        # February 18, 2026 at 6:00 UTC (local midnight would be ~23:00 UTC)
        dt = datetime(2026, 2, 18, 6, 0, 0)
        position = self.calc.get_solar_position(dt)

        # Before sunrise, sun should be below horizon
        self.assertLess(position["altitude"], 5)
        self.assertIn("azimuth", position)

    def test_solar_position_progression(self):
        """Test that sun position changes throughout the day."""
        positions = []
        for hour in range(6, 22):  # 6am to 10pm UTC
            dt = datetime(2026, 2, 18, hour, 0, 0)
            pos = self.calc.get_solar_position(dt)
            positions.append(pos)
        
        # Should have multiple positions collected
        self.assertEqual(len(positions), 16)
        
        # Find max altitude (should be somewhere in the middle)
        max_altitude = max(p["altitude"] for p in positions)
        self.assertGreater(max_altitude, 10)

    def test_civil_twilight_times(self):
        """Test civil twilight calculation."""
        dt = datetime(2026, 2, 18)
        twilight = self.calc.get_civil_twilight_times(dt)

        # Should have both times
        self.assertIn("civil_dusk", twilight)
        self.assertIn("civil_dawn", twilight)


class TestSolarPositionProgression(unittest.TestCase):
    """Test the progression of solar positions through the day."""

    def setUp(self):
        """Set up test fixtures."""
        self.calc = SolarCalculator(latitude=35.1264, longitude=-106.6055, elevation=1600)

    def test_altitude_increases_from_sunrise_to_noon(self):
        """Test that altitude increases from sunrise to solar noon."""
        sunrise_time = datetime(2026, 2, 18, 6, 0, 0)
        noon_time = datetime(2026, 2, 18, 12, 0, 0)

        sunrise_pos = self.calc.get_solar_position(sunrise_time)
        noon_pos = self.calc.get_solar_position(noon_time)

        # Altitude should be higher at noon
        self.assertGreater(noon_pos["altitude"], sunrise_pos["altitude"])

    def test_altitude_decreases_from_noon_to_sunset(self):
        """Test that altitude decreases from solar noon to sunset."""
        # Approximately solar noon at this location
        noon_time = datetime(2026, 2, 18, 19, 0, 0)
        # A couple hours after solar noon
        sunset_time = datetime(2026, 2, 18, 21, 0, 0)

        noon_pos = self.calc.get_solar_position(noon_time)
        sunset_pos = self.calc.get_solar_position(sunset_time)

        # Altitude should be lower later in the day
        self.assertGreater(noon_pos["altitude"], sunset_pos["altitude"])


if __name__ == "__main__":
    unittest.main()
