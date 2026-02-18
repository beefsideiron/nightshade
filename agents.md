# SunPredict Project Brief

## Project Goal
Build a Garmin Epix Pro app that shows **terrain sunset** - when direct sunlight is lost due to surrounding terrain obstruction at the user's current location.

## Current Status: MVP Console App Complete ✅
- **Sunrise/Sunset:** Calculated based on horizon (0° altitude)
- **Terrain Obstruction:** Calculates when sun altitude drops below terrain elevation angle
- **Log Storage:** Daily logs in `logs/sunpredict_YYYYMMDD.log` with UTC+1 timezone
- **Validation:** Tested against watch data - results match within 3 minutes

### Latest Results (Feb 18-24, 2026)
Location: 36.81°N, 4.22°W, Madrid (UTC+1)
| Date | Terrain Sunset | Civil Dusk |
|------|---|---|
| Feb 18 | 18:39 | 19:26 |
| Feb 21 | 18:41 | 19:29 |
| Feb 24 | 18:42 | 19:32 |

## Objective: Garmin Watch App
**Primary Output:** Display terrain sunset time for current location with terrain profile

**Garmin Target Device:** Epix Pro

## Core Problem Solved
- Standard sunset (horizon) doesn't account for terrain
- Terrain can block sun 5-20 minutes earlier than horizon sunset
- Need to calculate sun's altitude vs terrain elevation angle

## Current User Location
- Latitude: 36.810354°N
- Longitude: 4.222430°W
- Elevation: 221m
- Timezone: Europe/Madrid (UTC+1)

## Platform Targets
```
Phase 1 (Current): Console Application ✅
  - Prototype math & predictions
  - Validate terrain calculations
  - 22 unit tests (all passing)

Phase 2 (Next): Garmin Watch App 🚀
  - Connect to Garmin SDK
  - Real-time terrain data
  - Watch display optimization
  - Button/touchscreen input
```

## Required Data
- **GPS coordinates:** Target location
- **Target elevation:** User's elevation above MSL
- **Terrain profile:** Elevation angles at various azimuths (azimuth -> terrain angle)
- **Solar position:** Calculated via Astropy at 1-minute intervals

## Primary Output (Garmin App)
- **Terrain Sunset Time:** Local time when sun drops below terrain line
- **Azimuth:** Direction to sunset point (e.g., 255° = WSW)
- **Sun Altitude at Obstruction:** Angle above horizon when blocked
- **Civil Dusk:** Reference time (sun at -6°)

## Calculation Process
1. Get current location & elevation
2. Load terrain profile for location (from cache or API)
3. Calculate solar position for each minute (sunset approach)
4. For each position, check: `sun_altitude > terrain_elevation_at_azimuth`?
5. When condition fails → **terrain sunset time found**

## Performance Optimization Needed 🔴
**Current Issue:** Full-day calculation takes ~8-10 seconds (too slow for watch)

**Optimization Strategy:**
- Only calculate around sunset (14:00-20:00 UTC)
- Reduce to 5-minute steps initially, then binary search
- Cache solar ephemeris data
- Pre-calculate for next 7 days during charging

## Technical Implementation

### Console App (Nightshade) - Current
```
Language: Python 3.11
Libraries: Astropy, pytz, numpy, requests
Calculation: 1440 solar positions/day (1 per minute)
Output: Console + Daily logs + JSON
```

### Garmin App (develop_garmin branch) - Development
```
Language: Monkey C (Garmin proprietary)
SDK: Garmin ConnectIQ SDK
Target Device: Epix Pro
Input: GPS, Date/Time
Output: Display terrain sunset + metrics
Performance: <500ms calculation max
```

## Data Sources for Terrain
- **Open-Elevation API:** Current (free, slow)
- **Watch embedded:** Terrain cache on device (fast)
- **Offline maps:** Pre-generated azimuth profiles
- **User input:** Manual bearing/angle surveys

## Garmin SDK Research Needed
- [ ] Review ConnectIQ API documentation
- [ ] Understand device memory/computational limits
- [ ] GPS data access APIs
- [ ] Display rendering options
- [ ] Background calculation timing
- [ ] Data persistence on device

## Garmin ConnectIQ Capabilities (Researched)
**SDK Version:** ConnectIQ 8.4.1 (as of Feb 2026)

**Key Toybox Modules Available:**
- `Toybox.Position` - GPS/location data (real-time positioning)
- `Toybox.System` - System information (timezone, device info)
- `Toybox.Time` - Date/time handling
- `Toybox.Graphics` - Drawing/display rendering
- `Toybox.Application` - App lifecycle and state
- `Toybox.Application.Storage` - Local data persistence
- `Toybox.Background` - Background task execution
- `Toybox.Activity` - Activity recording
- `Toybox.ActivityMonitor` - Activity monitoring

**App Types Available:**
- Device Apps (recommended for terrain sunset)
- Widgets (quick glance info)
- Data Fields (custom data display)
- Watch Faces (always-on display)

**Recommended: Device App**
- Extended device access
- GPS and sensor data access
- FIT file recording
- Persistent storage
- Background execution capability
- Full UI control

**Device Target: Garmin Epix Pro**
- High-resolution display (480x454)
- Full GPS capabilities
- Always-on functions
- Sufficient memory for terrain cache

## Project Milestones
1. ✅ Implement solar position calculation (Astropy)
2. ✅ Implement terrain obstruction logic
3. ✅ Create console application with config
4. ✅ Display local timezone support
5. ✅ Obtain terrain elevation profile (OpenElevation API)
6. ✅ Run prediction with actual terrain data
7. ✅ Validate results with watch data (~±3 min)
8. ✅ Write unit tests (22 passing)
9. ✅ MVP complete - terrain sunset calculation
10. 🚀 **NEXT:** Garmin SDK integration & watch app prototype

## Files Structure (Nightshade Console)
```
nightshade/
├── src/
│   ├── main.py          # CLI entry point
│   ├── solar.py         # Astropy solar calculations
│   ├── terrain.py       # Terrain elevation angle lookup
│   └── __init__.py
├── tests/               # 22 pytest tests
├── data/
│   ├── user_terrain.json    # Terrain profile (azimuth -> angle)
│   ├── sample_terrain.json
│   └── validation_cases.json
├── logs/                # Daily prediction logs
├── config.json          # Default location config
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker container
└── docker-compose.yml  # Easy execution
```

## Next Steps for Garmin Branch

### 1. Performance Optimization
- Replace astropy minute-level calculation with targeted binary search
- Only compute 16:00-20:00 window
- Cache results for next 7 days

### 2. Garmin SDK Integration
- Set up MonkeyC development environment
- Implement location services (GPS)
- Build terrain cache system
- Create watch UI for sunset display

### 3. Watch App Features (MVP)
- Display current terrain sunset time
- Show azimuth to sunset
- Display sun altitude at obstruction
- Time update every minute

### 4. Advanced Features (Future)
- Multi-day forecast view
- Graphs of sun path vs terrain
- Watch complications (quick glance)
- Background update service

## Notes
- Prioritize correctness over speed initially, then optimize
- Keep architecture modular for easy Garmin integration
- Terrain data quality is critical to prediction accuracy
- Watch computation must stay under 500ms

## Technical Debt
- [ ] Performance: Current calculation is O(n), need binary search
- [ ] Terrain: Need better terrain data source (currently Open-Elevation free tier)
- [ ] Caching: Pre-compute for performance
- [ ] Testing: Need Garmin device integration tests
 