import Toybox.Graphics;
import Toybox.Time;
import Toybox.WatchUi;
import Toybox.System;

class SunsetView extends WatchUi.View {
    
    var terrainSunset as Moment = null;
    var sunsetAzimuth as Numeric = 0;
    var sunAltitude as Numeric = 0;
    var userLocation as Array = null;

    function initialize(params) {
        WatchUi.View.initialize();
    }

    function setTerrainSunset(sunset as Moment, azimuth as Numeric, altitude as Numeric) {
        terrainSunset = sunset;
        sunsetAzimuth = azimuth;
        sunAltitude = altitude;
    }

    function onUpdate(dc as Graphics.Dc) {
        dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_BLACK);
        dc.clear();
        
        // Header
        dc.setColor(Graphics.COLOR_ORANGE, Graphics.COLOR_BLACK);
        dc.drawText(240, 20, Graphics.FONT_MEDIUM, "Terrain Sunset", Graphics.TEXT_JUSTIFY_CENTER);
        
        if (terrainSunset != null) {
            var info = Time.Gregorian.info(terrainSunset, Time.FORMAT_SHORT);
            var timeStr = info.hour + ":" + (info.min < 10 ? "0" : "") + info.min;
            
            dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_BLACK);
            
            // Time display (large)
            dc.drawText(240, 80, Graphics.FONT_NUMBER_MILD, timeStr, Graphics.TEXT_JUSTIFY_CENTER);
            
            // Azimuth
            dc.drawText(240, 150, Graphics.FONT_SMALL, "Azimuth: " + sunsetAzimuth.toNumber() + "°", Graphics.TEXT_JUSTIFY_CENTER);
            
            // Sun altitude at obstruction
            dc.drawText(240, 180, Graphics.FONT_SMALL, "Sun Altitude: " + sunAltitude.toNumber() + "°", Graphics.TEXT_JUSTIFY_CENTER);
        } else {
            dc.setColor(Graphics.COLOR_YELLOW, Graphics.COLOR_BLACK);
            dc.drawText(240, 150, Graphics.FONT_MEDIUM, "Calculating...", Graphics.TEXT_JUSTIFY_CENTER);
        }
    }
}

class SunsetDelegate extends WatchUi.InputDelegate {
    function initialize() {
        WatchUi.InputDelegate.initialize();
    }
    
    function onKey(keyEvent) {
        if (keyEvent.getKey() == WatchUi.KEY_ESC) {
            WatchUi.popView(WatchUi.SLIDE_IMMEDIATE);
        }
    }
}
