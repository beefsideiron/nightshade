using Toybox.WatchUi;
using Toybox.Graphics;
using Toybox.Application;

class MyWatchAboutView extends WatchUi.View {

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

    function onLayout(dc) {
        setLayout(Rez.Layouts.MainLayout(dc));
    }

    function onShow() {
    }

    function onUpdate(dc) {
        // Clear the screen
        dc.setColor(Graphics.COLOR_BLACK, Graphics.COLOR_BLACK);
        dc.clear();
        
        // Set text color to user's selected color
        dc.setColor(textColor, Graphics.COLOR_BLACK);
        
        // Get screen dimensions
        var width = dc.getWidth();
        var height = dc.getHeight();
        
        // Draw title
        dc.drawText(
            width / 2, 
            40, 
            Graphics.FONT_MEDIUM, 
            WatchUi.loadResource(Rez.Strings.AboutTitle), 
            Graphics.TEXT_JUSTIFY_CENTER
        );
        
        // Draw app name
        dc.drawText(
            width / 2, 
            height / 2 - 30, 
            Graphics.FONT_SMALL, 
            WatchUi.loadResource(Rez.Strings.AppName), 
            Graphics.TEXT_JUSTIFY_CENTER
        );
        
        // Draw version
        dc.drawText(
            width / 2, 
            height / 2, 
            Graphics.FONT_TINY, 
            WatchUi.loadResource(Rez.Strings.Version), 
            Graphics.TEXT_JUSTIFY_CENTER
        );
        
        // Draw author
        dc.drawText(
            width / 2, 
            height / 2 + 25, 
            Graphics.FONT_TINY, 
            WatchUi.loadResource(Rez.Strings.Author), 
            Graphics.TEXT_JUSTIFY_CENTER
        );
    }

    function onHide() {
    }
}

class MyWatchAboutDelegate extends WatchUi.BehaviorDelegate {

    function initialize() {
        BehaviorDelegate.initialize();
    }

    function onBack() {
        // Pop this view and return to previous
        WatchUi.popView(WatchUi.SLIDE_DOWN);
        return true;
    }
}