using Toybox.WatchUi;
using Toybox.Graphics;
using Toybox.Application;

class MyWatchMenuView extends WatchUi.View {

    private var textColor;
    private var menuItems = ["Settings", "About"];
    private var selectedIndex = 0;

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
        // Refresh color in case it was changed
        var app = Application.getApp();
        textColor = app.getProperty("mainColor");
        if (textColor == null) {
            textColor = Graphics.COLOR_WHITE;
        }
    }

    function onUpdate(dc) {
        // Clear the screen
        dc.setColor(Graphics.COLOR_BLACK, Graphics.COLOR_BLACK);
        dc.clear();
        
        // Get screen dimensions
        var width = dc.getWidth();
        var height = dc.getHeight();
        
        // Draw title
        dc.setColor(textColor, Graphics.COLOR_BLACK);
        dc.drawText(
            width / 2, 
            40, 
            Graphics.FONT_MEDIUM, 
            "Menu", 
            Graphics.TEXT_JUSTIFY_CENTER
        );
        
        // Draw menu items
        for (var i = 0; i < menuItems.size(); i++) {
            // Highlight selected item
            if (i == selectedIndex) {
                dc.setColor(textColor, Graphics.COLOR_BLACK);
            } else {
                dc.setColor(Graphics.COLOR_DK_GRAY, Graphics.COLOR_BLACK);
            }
            
            dc.drawText(
                width / 2, 
                height / 2 - 20 + (i * 40), 
                Graphics.FONT_SMALL, 
                menuItems[i], 
                Graphics.TEXT_JUSTIFY_CENTER
            );
        }
    }

    function onHide() {
    }
    
    function moveUp() {
        if (selectedIndex > 0) {
            selectedIndex--;
            WatchUi.requestUpdate();
        }
    }
    
    function moveDown() {
        if (selectedIndex < menuItems.size() - 1) {
            selectedIndex++;
            WatchUi.requestUpdate();
        }
    }
    
    function getSelectedIndex() {
        return selectedIndex;
    }
}

class MyWatchMenuDelegate extends WatchUi.BehaviorDelegate {

    private var view;

    function initialize(v) {
        BehaviorDelegate.initialize();
        view = v;
    }

    function onBack() {
        // Pop this view and return to main view
        WatchUi.popView(WatchUi.SLIDE_DOWN);
        return true;
    }
    
    function onSelect() {
        var index = view.getSelectedIndex();
        
        if (index == 0) {
            // Navigate to Settings
            var settingsView = new MyWatchSettingsView();
            WatchUi.pushView(settingsView, new MyWatchSettingsDelegate(settingsView), WatchUi.SLIDE_LEFT);
        } else if (index == 1) {
            // Navigate to About
            WatchUi.pushView(new MyWatchAboutView(), new MyWatchAboutDelegate(), WatchUi.SLIDE_LEFT);
        }
        
        return true;
    }
    
    function onNextPage() {
        view.moveDown();
        return true;
    }
    
    function onPreviousPage() {
        view.moveUp();
        return true;
    }
}