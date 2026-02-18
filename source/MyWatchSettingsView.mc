using Toybox.WatchUi;
using Toybox.Graphics;
using Toybox.Application;

class MyWatchSettingsView extends WatchUi.View {

    private var selectedColor;
    private var colorOptions = ["White", "Green", "Blue", "Red"];
    private var colorValues = [Graphics.COLOR_WHITE, Graphics.COLOR_GREEN, Graphics.COLOR_BLUE, Graphics.COLOR_RED];
    private var currentColorIndex;

    function initialize() {
        View.initialize();
        // Get current color from app properties (default to COLOR_WHITE)
        var app = Application.getApp();
        selectedColor = app.getProperty("mainColor");
        if (selectedColor == null) {
            selectedColor = Graphics.COLOR_WHITE;
        }
        
        // Find current color index
        currentColorIndex = 0;
        for (var i = 0; i < colorValues.size(); i++) {
            if (colorValues[i] == selectedColor) {
                currentColorIndex = i;
                break;
            }
        }
    }

    function onLayout(dc) {
        setLayout(Rez.Layouts.MainLayout(dc));
    }

    function onShow() {
    }

    function onUpdate(dc) {
        // Clear the screen
        dc.setColor(Graphics.COLOR_BLACK, Graphics.COLOR_BLACK);
        dc.clear();
        
        // Get screen dimensions
        var width = dc.getWidth();
        var height = dc.getHeight();
        
        // Draw title with selected color
        dc.setColor(selectedColor, Graphics.COLOR_BLACK);
        dc.drawText(
            width / 2, 
            40, 
            Graphics.FONT_MEDIUM, 
            WatchUi.loadResource(Rez.Strings.SettingsTitle), 
            Graphics.TEXT_JUSTIFY_CENTER
        );
        
        // Draw color label
        dc.drawText(
            width / 2, 
            height / 2 - 40, 
            Graphics.FONT_SMALL, 
            WatchUi.loadResource(Rez.Strings.ColorLabel), 
            Graphics.TEXT_JUSTIFY_CENTER
        );
        
        // Draw current color selection
        dc.drawText(
            width / 2, 
            height / 2, 
            Graphics.FONT_MEDIUM, 
            colorOptions[currentColorIndex], 
            Graphics.TEXT_JUSTIFY_CENTER
        );
    }

    function onHide() {
    }
    
    function cycleColor() {
        // Cycle to next color
        currentColorIndex = (currentColorIndex + 1) % colorOptions.size();
        selectedColor = colorValues[currentColorIndex];
        
        // Save to app properties
        var app = Application.getApp();
        app.setProperty("mainColor", selectedColor);
        
        // Request screen update
        WatchUi.requestUpdate();
    }
}

class MyWatchSettingsDelegate extends WatchUi.BehaviorDelegate {

    private var view;

    function initialize(v) {
        BehaviorDelegate.initialize();
        view = v;
    }

    function onBack() {
        // Pop this view and return to previous
        WatchUi.popView(WatchUi.SLIDE_DOWN);
        return true;
    }
    
    function onSelect() {
        // Cycle through color options
        view.cycleColor();
        return true;
    }
}