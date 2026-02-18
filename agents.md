# SunPredict Project Brief

## Objective
Build a program that predicts when direct sunlight will no longer reach a specific location.

## Core Problem
Standard sunset time is not enough. The system must account for:
- The target location elevation
- Surrounding terrain elevation that may block sunlight earlier

## Location Input
Primary location method:
- GPS coordinates (`latitude`, `longitude`)

Optional/fallback location method:
- IP-based geolocation (lower precision)

## Current User Location
- Latitude: 36.810354°N
- Longitude: 4.222430°W
- Elevation: 221m
- Timezone: Europe/Madrid (UTC+1)

## Platform Target
Long-term target:
- Garmin Epix Pro app

Near-term prototype:
- Console application focused on math and prediction output

## Required Data
- GPS coordinates for the target point
- Target point elevation
- Surrounding elevation/terrain profile (elevation angles at different azimuths)
- Solar position and twilight reference data (civil, nautical, astronomical)

## Primary Output
Given a location and date/time context, output:
- **Sunrise:** When direct sunlight first becomes visible at that location
- **Sunset:** When direct sunlight is lost due to terrain obstruction
- **Azimuth and altitude** at both sunrise and sunset
- **Local time** in the user's timezone

## Calculation Process
1. Calculate solar position for each minute throughout the day
2. For each position, determine the sun's **azimuth** (compass direction, e.g., 255° = WSW)
3. Check if the sun's **altitude** (angle above horizon) exceeds the **terrain elevation angle** at that azimuth
4. When sun altitude drops below terrain elevation at the sunset azimuth = **direct sunlight is lost**

**Current Status:** We show civil sunset time (sun at -6°), but the real calculation requires terrain elevation data.

## Prototype Milestones
1. ✅ Implement solar position calculation
2. ✅ Implement terrain obstruction logic
3. ✅ Create console application with config support
4. ✅ Display local time in user's timezone
5. ✅ Obtain terrain elevation profile (Open-Elevation API)
6. ✅ Run prediction with actual terrain data
7. ✅ Validate results with actual terrain data
8. ✅ Write unit tests (22 tests passing)
9. ✅ MVP complete - ready for Garmin integration planning

## Project Setup Tasks
1. ✅ Add `agents.md` to `.gitignore`
2. ✅ Create initial project directories
3. ✅ Initialize git repository
4. ✅ Create Docker container for easy execution

## Technical Implementation
- **Solar calculations:** Astropy library (precise astronomical calculations)
- **Terrain obstruction:** Custom elevation profile interpolation
- **Timezone support:** pytz for local time conversion
- **Containerization:** Docker for portability
- **Testing:** pytest with 22 unit tests (all passing)
- **Terrain data:** Open-Elevation API with azimuth interpolation

## Notes
- Prioritize correctness of sunlight-loss prediction over UI.
- Keep architecture modular so Garmin device integration is straightforward later.
- Terrain elevation data is critical—this drives the accuracy of the prediction.

## Data Sources
Terrain elevation profiles can come from:
- OpenStreetMap elevation data (via APIs)
- USGS Digital Elevation Model (DEM)
- Manual surveying or GPS measurements along bearing lines
- Google Earth elevation data

---

## Core Algorithm Detail

We use civil sunset (sun at -6° below horizon) as a reference to find the approximate sunset **azimuth**. Then:

1. Get terrain elevation angle at that azimuth (e.g., 15° mountain to the west)
2. Calculate when sun drops to that elevation angle during sunset
3. That's when direct sunlight is lost at the location

**Example:**
- Sunset azimuth: 255° (WSW)
- Terrain elevation at 255°: 12° (mountain slope)
- Sun drops to 12° at 18:47 local time
- **Result: Direct sunlight lost at 18:47** 