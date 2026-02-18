// Welcome to SunPredict - Terrain Sunset Calculator
// Calculates when the sun is blocked by terrain at your current location
//
// Quick Start:
// 1. Get GPS location (app requests Positioning permission)
// 2. App calculates terrain sunset time
// 3. Display azimuth and sun altitude at obstruction
//
// Documentation: https://developer.garmin.com/connect-iq/

using Toybox.Application;
using Toybox.WatchUi;

class SunPredictApp extends Application.AppBase {

    function initialize() {
        AppBase.initialize();
    }

    // onStart() is called on application start up
    function onStart(state) {
    }

    // onStop() is called when application is exiting
    function onStop(state) {
    }

    // Return the initial view of your application here
    function getInitialView() {
        return [ new MyWatchView(), new MyWatchDelegate() ];
    }
}

function getApp() {
    return Application.getApp();
}