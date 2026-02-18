import Toybox.Application;
import Toybox.Graphics;
import Toybox.Position;
import Toybox.System;
import Toybox.Time;
import Toybox.Timer;

class SunPredictApp extends Application.AppBase {
    
    var terrainSunset as Moment = null;
    var userLocation as Array<Numeric> = null;
    var updateTimer as Timer.Timer = null;
    
    // Initialize app
    function initialize() {
        AppBase.initialize();
    }

    // Start app and request location
    function onStart(state as Dictionary) {
        System.println("SunPredict: App started");
        
        // Request permission for location updates
        Position.enableLocationEvents(Position.LOCATION_ONE_SHOT, method(:onLocationEvent));
        
        // Start background location updates
        Position.enableLocationEvents(Position.LOCATION_CONTINUOUS, method(:onLocationEvent));
    }

    // Stop app cleanup
    function onStop(state as Dictionary) {
        System.println("SunPredict: App stopped");
        
        if (updateTimer != null) {
            updateTimer.stop();
        }
    }

    // Update display
    function onUpdate(dc as Graphics.Dc) {
        dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_BLACK);
        dc.clear();
        
        if (terrainSunset != null) {
            var time = Time.now();
            var info = Time.Gregorian.info(terrainSunset, Time.FORMAT_SHORT);
            
            dc.drawText(240, 100, Graphics.FONT_LARGE, "Terrain Sunset", Graphics.TEXT_JUSTIFY_CENTER);
            dc.drawText(240, 150, Graphics.FONT_XTINY, info.hour + ":" + (info.min < 10 ? "0" : "") + info.min, Graphics.TEXT_JUSTIFY_CENTER);
        } else {
            dc.drawText(240, 150, Graphics.FONT_MEDIUM, "Calculating...", Graphics.TEXT_JUSTIFY_CENTER);
        }
    }

    // Handle location updates
    function onLocationEvent(info as Position.Info) {
        System.println("SunPredict: Location update");
        
        if (info has :position && info.position != null) {
            var position = info.position;
            userLocation = [position.getLatitude(), position.getLongitude()];
            
            System.println("Location: " + userLocation[0] + ", " + userLocation[1]);
            
            // Calculate terrain sunset for this location
            calculateTerrainSunset();
            
            // Request screen update
            WatchUi.requestUpdate();
        }
    }

    // Calculate terrain sunset time
    function calculateTerrainSunset() as Void {
        if (userLocation == null) {
            return;
        }
        
        // TODO: Implement terrain sunset calculation
        // For now, set a placeholder time (18:39 UTC+1)
        var now = Time.now();
        var today = Time.Gregorian.info(now, Time.FORMAT_SHORT);
        
        // Create a time for 18:39 local
        terrainSunset = Time.Gregorian.dateTime({
            :year => today.year,
            :month => today.month,
            :day => today.day,
            :hour => 18,
            :minute => 39,
            :second => 0
        });
    }
}

// Return app instance for Garmin runtime
function getApp() as Application.AppBase {
    return new SunPredictApp();
}
