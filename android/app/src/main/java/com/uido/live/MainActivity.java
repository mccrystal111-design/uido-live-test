package com.uido.live;
import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.location.Criteria;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.view.View;
import android.webkit.GeolocationPermissions;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
public class MainActivity extends Activity {
 private static final int LOCATION_REQUEST=1001; private WebView webView; private LocationManager lm; private LocationListener listener;
 @Override public void onCreate(Bundle b){super.onCreate(b); getWindow().setStatusBarColor(Color.TRANSPARENT); getWindow().setNavigationBarColor(Color.TRANSPARENT); getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE|View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN|View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION); webView=new WebView(this);WebSettings s=webView.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setGeolocationEnabled(true);s.setDatabaseEnabled(true);s.setCacheMode(WebSettings.LOAD_NO_CACHE);webView.setWebViewClient(new WebViewClient());webView.setWebChromeClient(new WebChromeClient(){@Override public void onGeolocationPermissionsShowPrompt(String o,GeolocationPermissions.Callback c){c.invoke(o,true,false);}});setContentView(webView);if(checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION)!=PackageManager.PERMISSION_GRANTED)requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION,Manifest.permission.ACCESS_COARSE_LOCATION},LOCATION_REQUEST);else startGps();webView.loadUrl("file:///android_asset/index.html");}
 @Override public void onRequestPermissionsResult(int r,String[] p,int[] g){super.onRequestPermissionsResult(r,p,g);if(r==LOCATION_REQUEST&&checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION)==PackageManager.PERMISSION_GRANTED)startGps();}
 private void startGps(){lm=(LocationManager)getSystemService(LOCATION_SERVICE);listener=location->{double lat=location.getLatitude(),lon=location.getLongitude();float acc=location.hasAccuracy()?location.getAccuracy():999f;float heading=location.hasBearing()?location.getBearing():-1f;String js="window.dispatchEvent(new CustomEvent('uidoNativeGps',{detail:{lat:"+lat+",lon:"+lon+",accuracy:"+acc+",heading:"+heading+"}}));";webView.post(()->webView.evaluateJavascript(js,null));};if(checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION)!=PackageManager.PERMISSION_GRANTED)return;Criteria c=new Criteria();c.setAccuracy(Criteria.ACCURACY_FINE);c.setPowerRequirement(Criteria.POWER_HIGH);String provider=lm.getBestProvider(c,true);if(provider!=null)lm.requestLocationUpdates(provider,1000L,0.5f,listener);}
 @Override protected void onDestroy(){if(lm!=null&&listener!=null&&checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION)==PackageManager.PERMISSION_GRANTED)lm.removeUpdates(listener);super.onDestroy();}
}