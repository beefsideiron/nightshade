"""
Integration tests for the prediction system.
"""

import unittest
from datetime import datetime
from src.main import predict_sunlight_loss


class TestSunriseAndSunset(unittest.TestCase):
    """Test sunrise and sunset predictions."""

    def test_sunrise_before_sunset(self):
        """Test that sunrise is before sunset."""
        result = predict_sunlight_loss(
            latitude=35.1264,
            longitude=-106.6055,
            elevation=1600,
            date=datetime(2026, 2, 18),
            timezone="UTC",
        )

        self.assertTrue(result["has_sunlight"])
        
        sunrise = datetime.fromisoformat(result["first_direct_sunlight"])
        sunset = datetime.fromisoformat(result["last_direct_sunlight"])
        
        self.assertLess(sunrise, sunset)

    def test_sunlight_window_exists(self):
        """Test that direct sunlight window exists and has valid data."""
        result = predict_sunlight_loss(
            latitude=35.1264,
            longitude=-106.6055,
            elevation=1600,
            date=datetime(2026, 2, 18),
            timezone="UTC",
        )

        self.assertTrue(result["has_sunlight"])
        
        sunrise = datetime.fromisoformat(result["first_direct_sunlight"])
        sunset = datetime.fromisoformat(result["last_direct_sunlight"])
        
        # Sunlight duration should be positive
        duration = (sunset - sunrise).total_seconds() / 3600
        self.assertGreater(duration, 0)
        
        # Both altitudes should be valid (can be negative before/after solar day)
        self.assertIsNotNone(result["sun_altitude_at_rise"])
        self.assertIsNotNone(result["sun_altitude_at_loss"])

    def test_sunrise_azimuth_is_valid(self):
        """Test that sunrise azimuth is a valid compass direction (0-360)."""
        result = predict_sunlight_loss(
            latitude=35.1264,
            longitude=-106.6055,
            elevation=1600,
            date=datetime(2026, 2, 18),
            timezone="UTC",
        )

        # Azimuth should be a valid compass direction (0-360 degrees)
        sunrise_azimuth = result["sun_azimuth_at_rise"]
        self.assertGreaterEqual(sunrise_azimuth, 0)
        self.assertLessEqual(sunrise_azimuth, 360)

    def test_sunset_azimuth_is_valid(self):
        """Test that sunset azimuth is a valid compass direction."""
        result = predict_sunlight_loss(
            latitude=35.1264,
            longitude=-106.6055,
            elevation=1600,
            date=datetime(2026, 2, 18),
            timezone="UTC",
        )

        # Azimuth should be a valid compass direction (0-360 degrees)
        sunset_azimuth = result["sun_azimuth_at_loss"]
        self.assertGreaterEqual(sunset_azimuth, 0)
        self.assertLessEqual(sunset_azimuth, 360)

    def test_terrain_reduces_sunlight_window(self):
        """Test that terrain obstruction reduces the sunlight window."""
        result_no_terrain = predict_sunlight_loss(
            latitude=35.1264,
            longitude=-106.6055,
            elevation=1600,
            date=datetime(2026, 2, 18),
            timezone="UTC",
            terrain_file=None,
        )

        result_with_terrain = predict_sunlight_loss(
            latitude=35.1264,
            longitude=-106.6055,
            elevation=1600,
            date=datetime(2026, 2, 18),
            timezone="UTC",
            terrain_file="data/sample_terrain.json",
        )

        sunrise_no_terrain = datetime.fromisoformat(result_no_terrain["first_direct_sunlight"])
        sunset_no_terrain = datetime.fromisoformat(result_no_terrain["last_direct_sunlight"])
        duration_no_terrain = (sunset_no_terrain - sunrise_no_terrain).total_seconds()

        sunrise_with_terrain = datetime.fromisoformat(result_with_terrain["first_direct_sunlight"])
        sunset_with_terrain = datetime.fromisoformat(result_with_terrain["last_direct_sunlight"])
        duration_with_terrain = (sunset_with_terrain - sunrise_with_terrain).total_seconds()

        # Terrain should reduce or keep the same sunlight window
        self.assertLessEqual(duration_with_terrain, duration_no_terrain)


if __name__ == "__main__":
    unittest.main()
