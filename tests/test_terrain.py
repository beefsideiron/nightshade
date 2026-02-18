"""
Unit tests for the terrain module.
"""

import unittest
from src.terrain import TerrainProfile


class TestTerrainProfile(unittest.TestCase):
    """Test cases for TerrainProfile."""

    def setUp(self):
        """Set up test fixtures."""
        self.terrain = TerrainProfile()

    def test_initialization(self):
        """Test that terrain profile initializes empty."""
        self.assertEqual(len(self.terrain.elevations), 0)
        self.assertEqual(self.terrain.reference_elevation, 0)

    def test_add_elevation_point(self):
        """Test adding elevation points."""
        self.terrain.add_elevation_point(0, 5)
        self.terrain.add_elevation_point(90, 15)
        self.terrain.add_elevation_point(180, 2)

        self.assertEqual(len(self.terrain.elevations), 3)
        self.assertEqual(self.terrain.elevations[0], 5)
        self.assertEqual(self.terrain.elevations[90], 15)
        self.assertEqual(self.terrain.elevations[180], 2)

    def test_load_from_dict(self):
        """Test loading from dictionary."""
        data = {0: -5, 90: 25, 180: -2, 270: 15}
        self.terrain.load_from_dict(data, reference_elevation=1500)

        self.assertEqual(len(self.terrain.elevations), 4)
        self.assertEqual(self.terrain.reference_elevation, 1500)

    def test_get_exact_azimuth(self):
        """Test retrieving obstruction angle for exact azimuths."""
        self.terrain.load_from_dict({0: 5, 90: 20, 180: 10})

        self.assertEqual(self.terrain.get_obstruction_angle(0), 5)
        self.assertEqual(self.terrain.get_obstruction_angle(90), 20)
        self.assertEqual(self.terrain.get_obstruction_angle(180), 10)

    def test_get_interpolated_azimuth(self):
        """Test interpolation between known azimuths."""
        self.terrain.load_from_dict({0: 0, 90: 20})

        # Halfway between should be interpolated
        angle_at_45 = self.terrain.get_obstruction_angle(45)
        self.assertAlmostEqual(angle_at_45, 10, places=1)

    def test_azimuth_normalization(self):
        """Test that azimuths are normalized to 0-360."""
        self.terrain.add_elevation_point(45, 10)

        # 405 degrees = 45 degrees normalized
        angle = self.terrain.get_obstruction_angle(405)
        self.assertEqual(angle, 10)

    def test_is_sun_blocked_above_obstruction(self):
        """Test that sun above obstruction is not blocked."""
        self.terrain.load_from_dict({0: 10})

        # Sun at 15 degrees is above 10 degree obstruction
        self.assertFalse(self.terrain.is_sun_blocked(15, 0))

    def test_is_sun_blocked_below_obstruction(self):
        """Test that sun below obstruction is blocked."""
        self.terrain.load_from_dict({0: 10})

        # Sun at 5 degrees is below 10 degree obstruction
        self.assertTrue(self.terrain.is_sun_blocked(5, 0))

    def test_is_sun_blocked_at_obstruction(self):
        """Test sun exactly at obstruction angle."""
        self.terrain.load_from_dict({0: 10})

        # Sun at exactly 10 degrees - should be blocked (<=)
        self.assertTrue(self.terrain.is_sun_blocked(10, 0))

    def test_find_unobstructed_sunset(self):
        """Test finding the last unobstructed position."""
        self.terrain.load_from_dict({0: 5})

        # Create sample positions
        positions = [
            {"time": "2026-02-18T16:00:00", "altitude": 20, "azimuth": 0},
            {"time": "2026-02-18T17:00:00", "altitude": 10, "azimuth": 0},
            {"time": "2026-02-18T18:00:00", "altitude": 3, "azimuth": 0},
        ]

        last = self.terrain.find_unobstructed_sunset(positions)
        self.assertIsNotNone(last)
        self.assertEqual(last["time"], "2026-02-18T17:00:00")


if __name__ == "__main__":
    unittest.main()
