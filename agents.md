# SunPredict Project Brief

## Project Goal
Build a Garmin Epix Pro app that shows **terrain sunset** - when direct sunlight is lost due to surrounding terrain obstruction at the user's current location.

## Current Status: Console App Complete ✅ | Garmin App in Development 🚀

### Console App (Python) - Production Ready
- **Sunrise/Sunset:** Calculated based on horizon (0° altitude)
- **Terrain Obstruction:** Calculates when sun altitude drops below terrain elevation angle
- **Log Storage:** Daily logs in `logs/sunpredict_YYYYMMDD.log` with UTC+1 timezone
- **Validation:** Tested against watch data - results match within 3 minutes
- **Status:** 22 unit tests passing, MVP complete

### Garmin App (Monkey C) - Building Phase
- **Branch:** `develop_port` - working build of app skeleton
- **Build Status:** ✅ Compiles successfully for Epix 2 Pro 47mm
- **Deployment:** ✅ Running in ConnectIQ simulator
- **Remaining:** Port terrain calculation logic + GPS integration

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

## Platform Targets & Development Phases
```
Phase 1: Console Application ✅ COMPLETE
  - Prototype math & predictions
  - Validate terrain calculations
  - 22 unit tests (all passing)
  - Used to verify algorithm correctness

Phase 2: Garmin Watch App 🚀 IN PROGRESS
  - ✅ SDK setup (ConnectIQ 8.4.1)
  - ✅ Development environment
  - ✅ Private key generation for signing
  - ✅ App skeleton compiles & deploys to simulator
  - ⏳ Port terrain sunset calculation
  - ⏳ GPS location integration
  - ⏳ Real-time display update
  - ⏳ Terrain data integration
  - [ ] Device testing

Phase 3: Advanced Features (Future)
  - [ ] Multi-day forecast
  - [ ] Background sync
  - [ ] Data persistence
  - [ ] Watch complications
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

### Garmin App (develop_port branch) - Development
```
Language: Monkey C (Garmin proprietary)
SDK: Garmin ConnectIQ SDK 8.4.1
Target Device: Epix Pro 47mm (480x454 display)
Compiler: monkeyc (generates .prg binary)
Input: GPS location, Date/Time system
Output: Display terrain sunset + azimuth + altitude
Performance: <500ms calculation target
Status: Template compiling & running in simulator ✅
Next: Port solar/terrain logic from Python
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

### Console App Development ✅
1. ✅ Implement solar position calculation (Astropy)
2. ✅ Implement terrain obstruction logic
3. ✅ Create console application with config
4. ✅ Display local timezone support
5. ✅ Obtain terrain elevation profile (OpenElevation API)
6. ✅ Run prediction with actual terrain data
7. ✅ Validate results with watch data (~±3 min)
8. ✅ Write unit tests (22 passing)
9. ✅ MVP complete - terrain sunset calculation

### Garmin App Development 🚀
10. ✅ Install Garmin ConnectIQ SDK 8.4.1
11. ✅ Generate RSA private key for signing (developer_key.der)
12. ✅ Create Monkey C project structure
13. ✅ Port working app template from garmin-app-starter
14. ✅ Configure manifest.xml for Epix 2 Pro 47mm
15. ✅ Successfully compile app binary (sunpredict.prg)
16. ✅ Deploy app to ConnectIQ simulator
17. ⏳ **NEXT:** Port solar calculation from Python to Monkey C
18. ⏳ Integrate GPS location services (Toybox.Position)
19. ⏳ Implement terrain sunset display on main view
20. ⏳ Test on simulator with mock GPS data

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

## Garmin App Development Progress (Feb 18, 2026)

### Completed This Session ✅
1. **SDK Setup**
   - Located ConnectIQ 8.4.1 SDK at `C:\Users\mail\AppData\Roaming\Garmin\ConnectIQ\Sdks\`
   - Generated RSA private key for app signing
   - Added SDK bin directory to PATH
   - Verified compiler (`monkeyc`), deployment tool (`monkeydo`), and simulator (`simulator.exe`)

2. **Project Porting**
   - Created `develop_port` branch for clean Garmin work
   - Cloned garmin-app-starter reference project (working template)
   - Updated manifest for Epix 2 Pro 47mm target
   - Customized resource strings for SunPredict branding
   - Updated Makefile with correct SDK path and device name
   - Reorganized resources into proper directory structure (`strings/`, `drawables/`, `layouts/`, `menus/`)

3. **Build & Deployment**
   - ✅ Successfully compiled `sunpredict.prg` (109 KB binary) - FIRST SUCCESSFUL BUILD
   - ✅ Deployed app to ConnectIQ simulator
   - ✅ App running on simulated Epix 2 Pro 47mm device
   - ✅ Verified input handling and menu navigation in simulator

### Current App State
- **Branch:** `develop_port` (clean working state)
- **Build Status:** Compiles with BUILD SUCCESSFUL message (only cosmetic warnings)
- **Deployment:** Running in ConnectIQ simulator
- **Template Features:** Settings menu, About screen, view navigation (reference project baseline)
- **Display:** 480x454 resolution, ready for terrain sunset display
- **Main File:** `source/SunPredictApp.mc` (entry point)

### Technical Details

**SDK Information:**
- Location: `C:\Users\mail\AppData\Roaming\Garmin\ConnectIQ\Sdks\connectiq-sdk-win-8.4.1-2026-02-03-e9f77eeaa`
- Compiler: `monkeyc` with flags `-d epix2pro47mm -f monkey.jungle -o sunpredict.prg -y developer_key.der -w`
- Development Key: `developer_key.der` (RSA private key, generated via OpenSSL)
- Build Output: `sunpredict.prg` (109 KB executable)

**App Configuration:**
- Manifest: Single device target (Epix 2 Pro 47mm, 480x454 display)
- Permissions: Positioning (for GPS access)
- Entry Point: SunPredictApp class in source/SunPredictApp.mc
- Resources: Strings, drawables, layouts, menus in proper directories

### Next Steps for MVP

#### 1. Port Terrain Sunset Calculation to Monkey C 
- Translate Python solar.py to new TerrainSunsetCalculator.mc
- Implement binary search algorithm (14:00-20:00 UTC window)
- Target: <500ms calculation time on watch
- Test with mock GPS data (36.81°N, 4.22°W, Madrid)

#### 2. GPS Location Integration
- Use `Toybox.Position` to request GPS location
- Add positioning permission to manifest (if not already present)
- Handle location updates in AppBase lifecycle
- Store last known location for next calculation window

#### 3. Terrain Data Integration
- Embed sample terrain profile in app resources or hardcode as test data
- Create terrain lookup function (azimuth -> elevation angle)
- Load profile during app initialization
- Handle missing data gracefully (fall back to horizon)

#### 4. Display Implementation  
- Update MyWatchView.mc to show:
  - **Time:** Terrain sunset time in local timezone (HH:MM format)
  - **Azimuth:** Cardinal direction to sunset point (e.g., 255° WSW)
  - **Altitude:** Sun altitude angle when blocked by terrain
  - **Status:** GPS lock status, calculation state, time remaining
- Implement refresh timer (update every minute after calculation)
- Color coding: Green (ready), Yellow (calculating), Red (no GPS)

#### 5. Testing & Validation
- Test in simulator with fixed mock location (Madrid coordinates)
- Compare output to Python console app (must be within ±2 minutes)
- Verify display updates every minute
- Test menu navigation and settings
- Performance profiling to ensure <500ms calculation time

### Advanced Features (Future Phases)
- Multi-day forecast (show sunset for next 7 days)
- Graphs displaying sun path vs terrain profile
- Watch complications for quick glance info
- Background calculation service (update during inactivity)
- Data persistence (save favorite locations and terrain profiles)
- User manual terrain bearing input (if automated fails)

### Known Build Warnings (Non-Critical)
- Launcher icon: 128x128 being scaled to 60x60 (acceptable scaling)
- Deprecated APIs: Some Garmin APIs marked for future removal (functional now)
- Missing language definitions: App works fine with single language (acceptable for MVP)

## Build & Run Commands

### Compile
```bash
cd D:\EDB\nightshade
$sdkPath = "C:\Users\mail\AppData\Roaming\Garmin\ConnectIQ\Sdks\connectiq-sdk-win-8.4.1-2026-02-03-e9f77eeaa\bin"
$env:Path += ";$sdkPath"
monkeyc -d epix2pro47mm -f monkey.jungle -o sunpredict.prg -y .\developer_key.der -w
```

### Run Simulator
```bash
# Terminal 1: Start simulator
$sdkPath\simulator.exe

# (Wait for simulator to start)

# Terminal 2: Deploy app
monkeydo sunpredict.prg epix2pro47mm
```

or use Makefile (simpler):
```bash
make simulator   # Start simulator in background
make run         # Compile and deploy to simulator
make release     # Build release version (optional)
make clean       # Remove build artifacts
```

### Development Workflow
1. Edit source files in `source/*.mc`
2. Run `make run` to compile and test
3. Test in simulator, verify tea menus and navigation
4. Commit changes to `develop_port` branch
5. When feature complete, merge to main branch

## Key Project Files
- **Branch:** `develop_port` (Garmin app development)
- **Main branch:** Console app (Python) - unchanged
- **Manifest:** `manifest.xml` (device: Epix 2 Pro 47mm)
- **Build Config:** `monkey.jungle`
- **Makefile:** `Makefile` (compilation shortcuts)
- **Signing Key:** `developer_key.der` (DO NOT push to public repo)
- **Compiled App:** `sunpredict.prg` (109 KB executable)

## Monkey C Development Tips

### Type System
- Monkey C is strongly typed; cannot use bare types like `Array` (must use `Lang.Array`)
- All numbers are `Lang.Number`; no distinct float/int (watch precision limitation)
- Type inference works in initialization but requires explicit types in parameters
- Dictionary keys must be type-compatible (strings recommended)

### Memory Constraints
- Watch apps have ~2-3 MB memory limit
- Avoid large data structures (e.g., don't cache 365 days of predictions)
- Prefer calculations over storage
- Use local variables when possible (garbage collected faster)

### Time Handling
- All times are `Toybox.Time.Moment` objects (no native int timestamps)
- Timezone conversions must use `Toybox.Time.TimeZone`
- Simulator doesn't reflect real device time; use fixed test values
- Local time on watch uses device timezone (not configurable per app)

### Performance Optimization
- **Current Python:** 1 minute intervals for full day = 1440 calculations
- **Target Monkey C:** Binary search in 14:00-20:00 UTC window = <50 calcs
- **First pass:** Use 5-minute intervals (48 positions), then binary search
- **Goal:** Complete calculation in <500ms on hardware
- **Testing:** Simulator is much faster; device is slower (test on actual device eventually)

### GPS & Location
- `Toybox.Position` request is asynchronous (callback model)
- GPS takes 10-60 seconds depending on signal
- Once location acquired, cache it for remainder of app session
- Simulator: No real GPS (can mock with fixed coordinates)

### Display & Graphics
- Epix Pro has high resolution (480x454) but small physical size
- Use larger fonts (30+ points) for watch-face readability
- Color display available
- Test at actual size (not just centered in simulator window)

### Testing Strategy
- Simulator good for: Logic, UI layout, fast iteration
- Simulator NOT good for: GPS timing, battery impact, real performance
- Eventually test on actual Epix Pro device (deployment via USB)
- Compare results to Python console app (should match within ±2 min)

### Algorithm Optimization for Watch
Input: Location (36.81°N, 4.22°W), Date, Terrain profile
Output: Terrain sunset time (HH:MM in local timezone)

Process:
1. Calculate solar position at 5-minute intervals (14:00-20:00 UTC)
2. At each interval: Check if `sun_altitude > terrain_elevation[azimuth]`
3. When condition becomes false → **found boundary**
4. Binary search around boundary (1-minute resolution)
5. Return result to UI

Expected performance: 30-50 milliseconds on device (well under 500ms budget)

### Data Persistence
- Use `Toybox.Application.Storage` for persistent data
- Available storage: Similar to memory (few MB)
- Good for: User preferences, favorite locations, last known GPS
- NOT good for: Large terrain profile caches (store in app binary instead)

## File Structure (Garmin Branch)
```
D:\EDB\nightshade/ (develop_port branch)
├── source/
│   ├── SunPredictApp.mc       # Main app entry point (AppBase)
│   ├── MyWatchView.mc         # Primary display view (needs customization)
│   ├── MyWatchMenuView.mc     # Menu system navigation
│   ├── MyWatchSettingsView.mc # Settings/configuration screen
│   ├── MyWatchAboutView.mc    # About/info screen
│   └── MyWatchDelegate.mc     # Input handling (buttons, gestures)
├── resources/
│   ├── strings/
│   │   └── strings.xml        # UI text strings (customized for SunPredict)
│   ├── drawables/
│   │   ├── drawables.xml      # Bitmap resource definitions
│   │   └── launcher_icon.png  # 128x128 app icon (scaled to 60x60)
│   ├── layouts/
│   │   └── layout.xml         # UI layout definitions
│   └── menus/
│       └── menu.xml           # Menu structure definitions
├── manifest.xml               # App metadata (device: Epix 2 Pro 47mm)
├── monkey.jungle              # Build system configuration file
├── Makefile                   # Convenient make commands
├── developer_key.der          # RSA private key for signing (⚠️ SECRET)
├── sunpredict.prg             # Compiled app binary (109 KB)
├── sunpredict.prg.debug.xml   # Debug symbols for testing
└── gen/                       # Build artifacts directory
    ├── *.mir                  # Monkey C intermediate representation files
    └──resources/              # Cached resource files
```

## Console App File Structure (Unchanged)
```
D:\EDB\nightshade/ (main branch)
├── src/
│   ├── main.py                # CLI entry point
│   ├── solar.py               # Astropy solar calculations
│   ├── terrain.py             # Terrain elevation angle lookup
│   └── __init__.py
├── tests/                     # 22 pytest unit tests (all passing) 
├── data/
│   ├── user_terrain.json      # Terrain profile (azimuth -> angle)
│   ├── sample_terrain.json
│   └── validation_cases.json
├── logs/                      # Daily prediction logs
├── config.json                # Default location config
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker container
└── docker-compose.yml         # Docker compose setup
```
 