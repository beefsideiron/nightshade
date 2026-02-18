using Toybox.WatchUi;
using Toybox.System;

class MyWatchDelegate extends WatchUi.BehaviorDelegate {

    function initialize() {
        BehaviorDelegate.initialize();
    }

    // Handle menu button press
    function onMenu() {
        var menuView = new MyWatchMenuView();
        WatchUi.pushView(menuView, new MyWatchMenuDelegate(menuView), WatchUi.SLIDE_UP);
        return true;
    }
    
    // Handle select button press
    function onSelect() {
        System.println(WatchUi.loadResource(Rez.Strings.SelectPressed));
        // You can add your custom action here
        WatchUi.requestUpdate();
        return true;
    }
    
    // Handle back button press
    function onBack() {
        // Returning false exits the app (standard behavior)
        // The simulator will return to the launcher screen
        return false;
    }
    
    // Handle swipe gestures
    function onSwipe(swipeEvent) {
        var direction = swipeEvent.getDirection();
        
        if (direction == WatchUi.SWIPE_UP) {
            System.println(WatchUi.loadResource(Rez.Strings.SwipedUp));
        } else if (direction == WatchUi.SWIPE_DOWN) {
            System.println(WatchUi.loadResource(Rez.Strings.SwipedDown));
        } else if (direction == WatchUi.SWIPE_LEFT) {
            System.println(WatchUi.loadResource(Rez.Strings.SwipedLeft));
        } else if (direction == WatchUi.SWIPE_RIGHT) {
            System.println(WatchUi.loadResource(Rez.Strings.SwipedRight));
        }
        
        WatchUi.requestUpdate();
        return true;
    }
}