package com.uido.live;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Criteria;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.webkit.GeolocationPermissions;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private static final int LOCATION_REQUEST = 1001;
    private WebView webView;
    private LocationManager locationManager;
    private LocationListener listener;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        webView = new WebView(this);
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true); s.setGeolocationEnabled(true); s.setDatabaseEnabled(true);
        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient() {
            @Override public void onGeolocationPermissionsShowPrompt(String origin, GeolocationPermissions.Callback callback) {
                callback.invoke(origin, true, false);
            }
        });
        setContentView(webView);
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, LOCATION_REQUEST);
        } else startGps();
        webView.loadUrl("https://mccrystal111-design.github.io/uido-live-test/");
    }

    @Override public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] results) {
        super.onRequestPermissionsResult(requestCode, permissions, results);
        if (requestCode == LOCATION_REQUEST && checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) startGps();
    }

    private void startGps() {
        startService(new Intent(this, GpsService.class));
        locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
        listener = location -> {
            final double lat = location.getLatitude(), lon = location.getLongitude();
            final float acc = location.hasAccuracy() ? location.getAccuracy() : 999f;
            final long time = location.getTime();
            String js = "window.dispatchEvent(new CustomEvent('uidoNativeGps',{detail:{lat:" + lat + ",lon:" + lon + ",accuracy:" + acc + ",time:" + time + "}}));";
            webView.post(() -> webView.evaluateJavascript(js, null));
        };
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) return;
        Criteria c = new Criteria(); c.setAccuracy(Criteria.ACCURACY_FINE); c.setPowerRequirement(Criteria.POWER_HIGH);
        String provider = locationManager.getBestProvider(c, true);
        if (provider != null) locationManager.requestLocationUpdates(provider, 1000L, 0.5f, listener);
    }

    @Override protected void onDestroy() {
        if (locationManager != null && listener != null && checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) locationManager.removeUpdates(listener);
        super.onDestroy();
    }

    @Override public void onBackPressed() { if (webView.canGoBack()) webView.goBack(); else super.onBackPressed(); }
}
