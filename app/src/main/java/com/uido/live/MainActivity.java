package com.uido.live;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.location.Criteria;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.webkit.GeolocationPermissions;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends Activity {
    private static final int LOCATION_REQUEST = 1001;
    private static final String UIDO_HTML_URL = "https://raw.githubusercontent.com/mccrystal111-design/uido-live-test/9cb7b3cda9e5fe8f62ba4d3eda9a2d9affab5c73/index.html";
    private WebView webView;
    private LocationManager locationManager;
    private LocationListener listener;
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        webView = new WebView(this);
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setGeolocationEnabled(true);
        s.setDatabaseEnabled(true);
        webView.setWebViewClient(new WebViewClient() {
            @Override public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                view.evaluateJavascript(V07_PATCH, null);
            }
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return super.shouldInterceptRequest(view, request);
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override public void onGeolocationPermissionsShowPrompt(String origin, GeolocationPermissions.Callback callback) {
                callback.invoke(origin, true, false);
            }
        });
        setContentView(webView);
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, LOCATION_REQUEST);
        } else startGps();
        loadUiDoHtml();
    }

    private void loadUiDoHtml() {
        executor.execute(() -> {
            HttpURLConnection connection = null;
            try {
                URL url = new URL(UIDO_HTML_URL);
                connection = (HttpURLConnection) url.openConnection();
                connection.setRequestProperty("Accept", "text/html");
                connection.setConnectTimeout(10000);
                connection.setReadTimeout(10000);
                connection.setUseCaches(false);
                try (InputStream in = connection.getInputStream()) {
                    byte[] bytes = in.readAllBytes();
                    String html = new String(bytes, StandardCharsets.UTF_8);
                    runOnUiThread(() -> webView.loadDataWithBaseURL(
                            "https://mccrystal111-design.github.io/uido-live-test/",
                            html,
                            "text/html",
                            "UTF-8",
                            UIDO_HTML_URL));
                }
            } catch (Exception e) {
                runOnUiThread(() -> webView.loadDataWithBaseURL(
                        "https://mccrystal111-design.github.io/uido-live-test/",
                        "<html><body style='font-family:sans-serif;padding:24px'><h2>UiDo couldn't load</h2><p>Please check your internet connection and try again.</p><p>" + e.getClass().getSimpleName() + "</p></body></html>",
                        "text/html",
                        "UTF-8",
                        UIDO_HTML_URL));
            } finally {
                if (connection != null) connection.disconnect();
            }
        });
    }

    @Override protected void onDestroy() {
        executor.shutdownNow();
        super.onDestroy();
    }

    private void startGps() {
        locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
        listener = location -> webView.evaluateJavascript(
                "window.dispatchEvent(new CustomEvent('uidoNativeGps',{detail:" +
                        "{lat:" + location.getLatitude() + ",lon:" + location.getLongitude() +
                        ",accuracy:" + location.getAccuracy() + ",speed:" + location.getSpeed() +
                        ",bearing:" + location.getBearing() + "}}));", null);
        try {
            Criteria criteria = new Criteria();
            criteria.setAccuracy(Criteria.ACCURACY_FINE);
            locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000L, 1f, listener);
        } catch (SecurityException ignored) { }
    }

    private static final String V07_PATCH = """
        (function(){
          window.addEventListener('load',function(){
            try { if (typeof window.__uidoV07Patched === 'undefined') window.__uidoV07Patched=true; } catch(e){}
          });
        })();
    """;
}
