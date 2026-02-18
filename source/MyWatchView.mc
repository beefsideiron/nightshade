using Toybox.WatchUi;
using Toybox.Graphics;
using Toybox.System;
using Toybox.Lang;
using Toybox.Application;

class MyWatchView extends WatchUi.View {

    private var textColor;

    function initialize() {
        View.initialize();
        
        // Get the color from app properties (default to white)
        var app = Application.getApp();
        textColor = app.getProperty("mainColor");
        if (textColor == null) {
            textColor = Graphics.COLOR_WHITE;
        }
    }

    // Load your resources here
    function onLayout(dc) {
        setLayout(Rez.Layouts.MainLayout(dc));
    }

    // Called when this View is brought to the foreground. Restore
    // the state of this View and prepare it to be shown. This includes
    // loading resources into memory.
    function onShow() {
        // Refresh color in case it was changed in settings
        var app = Application.getApp();
        textColor = app.getProperty("mainColor");
        if (textColor == null) {
            textColor = Graphics.COLOR_WHITE;
        }
    }

    // Update the view
    function onUpdate(dc) {
        // Get the current time
        var clockTime = System.getClockTime();
        var timeString = clockTime.hour.format("%02d") + ":" + clockTime.min.format("%02d");
        
        // Clear the screen
        dc.setColor(Graphics.COLOR_BLACK, Graphics.COLOR_BLACK);
        dc.clear();
        
        // Set text color to the user's selected color
        dc.setColor(textColor, Graphics.COLOR_BLACK);
        
        // Get screen dimensions
        var width = dc.getWidth();
        var height = dc.getHeight();
        
        // Draw "Hello Watch!" message
        dc.drawText(
            width / 2, 
            height / 2 - 30, 
            Graphics.FONT_LARGE, 
            WatchUi.loadResource(Rez.Strings.HelloMessage), 
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );
        
        // Draw current time
        dc.drawText(
            width / 2, 
            height / 2 + 20, 
            Graphics.FONT_MEDIUM, 
            timeString, 
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );
    }

    // Called when this View is removed from the screen. Save the
    // state of this View here. This includes freeing resources from
    // memory.
    function onHide() {
    }
}