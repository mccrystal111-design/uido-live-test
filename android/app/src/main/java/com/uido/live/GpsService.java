package com.uido.live;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.IBinder;
import androidx.annotation.Nullable;

public class GpsService extends Service {
    private static final String CHANNEL = "uido_gps";
    private LocationManager manager;
    private final LocationListener listener = new LocationListener() {
        @Override public void onLocationChanged(Location location) {
            // The foreground service keeps high-quality native GPS active.
            // The WebView receives the same live stream while the activity is open.
        }
    };

    @Override public int onStartCommand(Intent intent, int flags, int startId) {
        createChannel();
        Notification n = new Notification.Builder(this, CHANNEL)
                .setContentTitle("UiDo GPS active")
                .setContentText("Keeping location updated for your round")
                .setSmallIcon(com.uido.live.R.drawable.uido_icon)
                .setOngoing(true).build();
        startForeground(2001, n);
        startUpdates();
        return START_STICKY;
    }

    private void startUpdates() {
        manager = (LocationManager) getSystemService(LOCATION_SERVICE);
        if (checkSelfPermission(android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) return;
        manager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000L, 0.5f, listener);
    }

    private void createChannel() {
        NotificationChannel c = new NotificationChannel(CHANNEL, "UiDo GPS", NotificationManager.IMPORTANCE_LOW);
        ((NotificationManager)getSystemService(NOTIFICATION_SERVICE)).createNotificationChannel(c);
    }

    @Override public void onDestroy() {
        if (manager != null && checkSelfPermission(android.Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) manager.removeUpdates(listener);
        super.onDestroy();
    }

    @Nullable @Override public IBinder onBind(Intent intent) { return null; }
}
