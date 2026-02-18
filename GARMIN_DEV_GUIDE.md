# SunPredict Garmin App - Development Guide

This is the `develop_garmin` branch for building the Garmin Epix Pro watch app to display terrain sunset times.

## Project Structure

```
develop_garmin/
├── manifest.xml              # App metadata, permissions, target devices
├── source/
│   ├── SunPredictApp.mc      # Main app class (entry point)
│   ├── SunsetView.mc         # UI view and input handling
│   └── TerrainSunsetCalculator.mc  # Solar calculations
├── resources/
│   ├── drawables.xml         # Graphics and UI resources
│   ├── strings.xml           # Localized strings
│   └── launcher_icon.png     # App icon (to create)
└── README.md                 # This file
```

## Setup & Build

### Prerequisites
- Garmin ConnectIQ SDK 8.4.1+ 
- Monkey C compiler (included with SDK)
- Text editor or Monkey C IDE
- Target: Garmin Epix Pro device

### Build Command
```bash
cd develop_garmin
monkeyc -d epix_pro -o sunpredict.prg -w manifest.xml source/
```

### Deploy to Emulator
```bash
monkeydo sunpredict.prg epix_pro
```

## Current Implementation Status

### ✅ Completed
- [x] Basic app structure (Device App type)
- [x] Manifest and permissions setup
- [x] Location permission configuration
- [x] View and UI framework
- [x] Input handling (back button)
- [x] Placeholder sunset display

### 🚀 In Progress
- [ ] TerrainSunsetCalculator implementation
- [ ] Solar position calculations (optimized)
- [ ] Terrain profile loading
- [ ] Real-time location integration

### 📋 To Do
- [ ] Implement binary search for sunset calculation
- [ ] Embed terrain profile data on device
- [ ] Optimize for watch memory constraints
- [ ] Multi-day forecast view (future)
- [ ] Background task for periodic updates
- [ ] Data persistence (save last known location)
- [ ] Test on actual Epix Pro device
- [ ] Handle edge cases (polar regions, etc.)

## Key Design Decisions

### Performance Optimization
- **Binary Search**: Instead of checking every minute (1440 positions), we'll use binary search to find sunset in ~10 iterations
- **Cached Terrain Profile**: Pre-load terrain data from device storage or embedded arrays
- **Limited Precision**: Trade astronomical accuracy for speed (±2 minute tolerance acceptable)

### Watch Constraints
- **Memory**: Avoid large array allocations; use indexed lookups
- **CPU**: Keep calculations under 500ms for smooth UX
- **Battery**: Use event-driven updates, not continuous polling

### Algorithm
1. Get GPS location (Positioning API)
2. Load terrain profile from storage
3. Binary search for when sun_altitude < terrain_elevation
4. Return time; update display
5. Update every minute or on location change

## Architecture

### App Flow
```
SunPredictApp (main)
  ↓
onLocationEvent() → gets GPS coordinates
  ↓
calculateTerrainSunset() → calls calculator
  ↓
TerrainSunsetCalculator.calculateTerrainSunset()
  ↓
SunsetView.setTerrainSunset() → updates display
  ↓
onUpdate() → draws to screen
```

### Terrain Profile Format
The terrain profile is a mapping of compass azimuth to terrain elevation angle:
```
{
  "0": 2.5,      // North: 2.5° elevation
  "45": 5.0,     // NE: 5° elevation
  "90": 3.2,     // East: 3.2° elevation
  ...
  "270": 12.5    // West: 12.5° elevation (mountain)
}
```

## Garmin API References

### Key Modules Used
- **Toybox.Position**: GPS location updates
- **Toybox.Graphics**: Drawing to screen
- **Toybox.Time**: Date/time calculations
- **Toybox.System**: System info and logging
- **Toybox.Application.Storage**: Persistent data

### Important Garmin Docs
- [ConnectIQ Overview](https://developer.garmin.com/connect-iq/)
- [Positioning API](https://developer.garmin.com/connect-iq/core-topics/positioning/)
- [Graphics/Drawing](https://developer.garmin.com/connect-iq/core-topics/graphics/)
- [Device App Guide](https://developer.garmin.com/connect-iq/core-topics/application-and-system-modules/)

## Development Workflow

1. **Edit code** in `source/` directory
2. **Compile**: `monkeyc -d epix_pro -o sunpredict.prg -w manifest.xml source/`
3. **Test on Emulator**: `monkeydo sunpredict.prg epix_pro`
4. **Debug**: Check `System.println()` logs
5. **Deploy**: Transfer `.prg` file to actual device

## Testing Strategy

### Unit Tests
- Solar position calculations (compare against Python console app)
- Terrain interpolation
- Edge cases (twilight times, equinox, etc.)

### Integration Tests
- Real GPS data on Epix Pro
- Multi-day forecast accuracy
- Battery/performance impact

### Field Testing
- Compare watch display to actual sunset observation
- Test across different locations and dates
- Monitor battery consumption

## Performance Targets

| Task | Target | Status |
|------|--------|--------|
| Calculate sunset | <500ms | TODO |
| Update display | <100ms | ✓ |
| GPS acquisition | <5s | ✓ |
| Memory usage | <2MB | TODO |
| Battery drain | <5% per day | TODO |

## Troubleshooting

### Common Issues

**"No GPS lock"**
- Ensure app has Positioning permission
- Run outdoors with clear sky
- Wait 30-60 seconds for initial lock

**"Terrain profile not loading"**
- Check device storage permissions
- Verify profile format is valid JSON
- Test with embedded fallback profile

**"Display not updating"**
- Add debug logging to onUpdate()
- Force screen update with WatchUi.requestUpdate()
- Check memory constraints

## Next Phase: Full Solar Calculation

Currently the app displays a fixed time (18:39). Next implementation will:

1. Port solar position algorithm from Python console app
2. Optimize for watch constraints (binary search instead of full day calculation)
3. Load real terrain profile from device
4. Calculate final sunset time based on location and terrain

See parent `main` branch for working Python algorithm to reference.

## Links & Resources

- [Garmin ConnectIQ SDK](https://developer.garmin.com/connect-iq/sdk/)
- [Monkey C Language Guide](https://developer.garmin.com/connect-iq/monkey-c/)
- [Device Reference (Epix Pro specs)](https://developer.garmin.com/connect-iq/device-reference/)
- [App Review Guidelines](https://developer.garmin.com/connect-iq/app-review-guidelines/)

## Author Notes

This Garmin app implementation started from a working Python console prototype (nightshade repo, main branch). The core algorithm for terrain sunset calculation is proven; this branch focuses on optimizing and adapting it for watch constraints while maintaining accuracy.
