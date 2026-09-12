package com.uido.live;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
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

import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends Activity {
    private static final int LOCATION_REQUEST = 1001;
    private static final String UIDO_HTML_URL = "https://raw.githubusercontent.com/mccrystal111-design/uido-live-test/9cb7b3cda9e5fe8f62ba4d3eda9a2d9affab5c73/index.html";
    private WebView webView;
    private LocationManager locationManager;
    private LocationListener listener;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        webView = new WebView(this);
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setGeolocationEnabled(true);
        s.setDatabaseEnabled(true);
        s.setCacheMode(WebSettings.LOAD_NO_CACHE);
        webView.setWebViewClient(new WebViewClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                if (UIDO_HTML_URL.equals(request.getUrl().toString())) {
                    try {
                        HttpURLConnection c = (HttpURLConnection)new URL(UIDO_HTML_URL).openConnection();
                        c.setUseCaches(false);
                        c.setConnectTimeout(10000);
                        c.setReadTimeout(10000);
                        c.setRequestProperty("Accept", "text/html");
                        return new WebResourceResponse("text/html", "UTF-8", c.getInputStream());
                    } catch (Exception ignored) { }
                }
                return super.shouldInterceptRequest(view, request);
            }
            @Override public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                view.evaluateJavascript(V07_PATCH, null);
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
        webView.loadUrl(UIDO_HTML_URL);
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
            final float heading = location.hasBearing() ? location.getBearing() : -1f;
            String js = "window.dispatchEvent(new CustomEvent('uidoNativeGps',{detail:{lat:" + lat + ",lon:" + lon + ",accuracy:" + acc + ",time:" + time + ",heading:" + heading + "}}));";
            webView.post(() -> webView.evaluateJavascript(js, null));
        };
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) return;
        Criteria c = new Criteria();
        c.setAccuracy(Criteria.ACCURACY_FINE);
        c.setPowerRequirement(Criteria.POWER_HIGH);
        String provider = locationManager.getBestProvider(c, true);
        if (provider != null) locationManager.requestLocationUpdates(provider, 1000L, 0.5f, listener);
    }

    @Override protected void onDestroy() {
        if (locationManager != null && listener != null && checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) locationManager.removeUpdates(listener);
        super.onDestroy();
    }

    @Override public void onBackPressed() { if (webView.canGoBack()) webView.goBack(); else super.onBackPressed(); }

    private static final String V07_PATCH = """
(function(){
  const clubs=['Driver','3 Wood','5 Wood','Hybrid','2 Iron','3 Iron','4 Iron','5 Iron','6 Iron','7 Iron','8 Iron','9 Iron','Pitching Wedge','Gap Wedge','Sand Wedge','Lob Wedge','Putter'];
  if(!S.strikeQuality) S.strikeQuality='Normal';
  if(!S.pin) S.pin='Middle';
  if(!S.heading) S.heading=null;
  S.shotSaved=!!S.shotSaved;
  const strike=document.getElementById('strike');
  if(strike && !document.getElementById('strikeQuality')){
    const wrap=document.createElement('div'); wrap.id='strikeQuality';
    wrap.innerHTML='<div class="sub" style="margin-top:10px">Strike quality</div><div class="row"><button class="choice active" data-quality="Normal">Normal</button><button class="choice" data-quality="Heavy">Heavy</button></div>';
    strike.querySelector('.card').insertBefore(wrap,strike.querySelector('.nav'));
    wrap.querySelectorAll('[data-quality]').forEach(b=>b.onclick=()=>{S.strikeQuality=b.dataset.quality;wrap.querySelectorAll('[data-quality]').forEach(x=>x.classList.toggle('active',x===b));});
  }
  if(!document.getElementById('pinChoices')){
    const p=document.createElement('div');p.id='pinChoices';p.className='summary';p.innerHTML='<div style="margin-bottom:7px">Pin position</div><div class="row"><button class="choice" data-pin="Front">Front</button><button class="choice active" data-pin="Middle">Middle</button><button class="choice" data-pin="Back">Back</button></div>';
    const nav=document.querySelector('#wind .nav');nav.parentNode.insertBefore(p,nav);
    p.querySelectorAll('[data-pin]').forEach(b=>b.onclick=()=>{S.pin=b.dataset.pin;p.querySelectorAll('[data-pin]').forEach(x=>x.classList.toggle('active',x===b));});
  }
  const shot=document.getElementById('shot');
  if(shot && !document.getElementById('actualClub')){
    const card=shot.querySelector('.shotcard');
    card.insertAdjacentHTML('beforeend','<div><select id="actualClub" style="width:100%;padding:9px;border:1px solid #d7e2dc;border-radius:8px;background:#fff;color:#17392d"><option value="">Actual club</option>'+clubs.map(c=>'<option>'+c+'</option>').join('')+'</select><span>Actual club</span></div><div><input id="shotDistance" type="number" min="0" step="1" placeholder="Distance (yd)" style="width:100%;padding:9px;border:1px solid #d7e2dc;border-radius:8px"><span>Shot distance</span></div>');
  }
  const saveBtn=shot?.querySelector('button.btn'); if(saveBtn) saveBtn.textContent='Save shot';
  const finishBtn=shot?.querySelector('button.btn.secondary'); if(finishBtn) finishBtn.textContent='Finish hole & score';
  function updateActualSummary(){
    if(typeof updateSummary==='function') updateSummary();
    const club=document.getElementById('actualClub'),d=document.getElementById('shotDistance');
    if(club) club.value=S.actualClub||''; if(d) d.value=S.shotDistance||'';
    const card=document.getElementById('shot');
    if(card){let q=document.getElementById('shotQuality'); if(!q){card.querySelector('.shotcard').insertAdjacentHTML('beforeend','<div><b id="shotQuality">Normal</b><span>Strike quality</span></div><div><b id="shotPin">Middle</b><span>Pin</span></div>');q=document.getElementById('shotQuality')} q.textContent=S.strikeQuality||'Normal';document.getElementById('shotPin').textContent=S.pin||'Middle';}
  }
  const oldShow=show;
  window.show=function(id){oldShow(id);if(id==='shot')updateActualSummary();};
  window.updateSummary=updateActualSummary;
  window.recordCurrentShot=function(){
    if(S.shotSaved) return;
    const club=document.getElementById('actualClub'),d=document.getElementById('shotDistance');
    S.actualClub=club?club.value:''; S.shotDistance=d&&d.value?Number(d.value):null;
    S.shots.push({hole:S.hole,par:pars[S.hole-1],timestamp:new Date().toISOString(),shape:S.shape,startLine:S.startLine,strike:S.strike,strikeQuality:S.strikeQuality,lie:S.lie,wind:S.windDir+' · '+S.windStrength,pin:S.pin,actualClub:S.actualClub,shotDistance:S.shotDistance,heading:S.heading,gps:S.gps});
    S.shotSaved=true; persist();
  };
  window.saveShot=function(){recordCurrentShot();show('hole');};
  window.finishHole=function(){recordCurrentShot();show('score');};
  window.buildScores=function(){
    const p=pars[S.hole-1];
    $('scoreChoices').innerHTML=[p-2,p-1,p,p+1,p+2].filter(v=>v>0).map(v=>'<button class="choice" data-score="'+v+'">'+v+' <small>'+(v-p===0?'Par':v-p>0?'+'+(v-p):v-p)+'</small></button>').join('');
    $('scoreChoices').querySelectorAll('[data-score]').forEach(b=>b.onclick=()=>{scores[S.hole]=Number(b.dataset.score);localStorage.setItem('uido_scores',JSON.stringify(scores));if(S.hole<18){S.hole++;S.shotSaved=false;resetShot();persist();show('hole')}else{persist();openScorecard();}});
  };
  const oldReset=resetShot; window.resetShot=function(){oldReset();S.shotSaved=false;S.strikeQuality='Normal';S.pin='Middle';S.actualClub='';S.shotDistance=null;S.heading=null;};
  window.renderReview=function(){
    const hs=Object.keys(scores).length,total=Object.values(scores).reduce((a,b)=>a+Number(b),0);$('reviewStats').textContent=hs?hs+' hole'+(hs===1?'':'s')+' completed · '+total+' strokes':'No holes completed';
    $('shotList').innerHTML=S.shots.length?S.shots.map(x=>'<div class="shotrow"><div class="topline"><span>Hole '+x.hole+'</span><span class="score">'+(scores[x.hole]?'Score '+scores[x.hole]:'Shot')+'</span></div><small>'+x.shape+' · '+x.startLine+' · '+x.strike+' · '+(x.strikeQuality||'Normal')+' · '+x.lie+' · '+(x.actualClub||'Club —')+' · '+(x.shotDistance?x.shotDistance+' yd':'Distance —')+'</small></div>').join(''):'<div class="shotrow">No shot data yet.</div>';
  };
  window.exportRound=function(){const rows=['hole,par,wind,lie,pin,start_line,shape,strike,strike_quality,actual_club,shot_distance_yd,heading,gps_lat,gps_lon,gps_accuracy_m'];S.shots.forEach(x=>rows.push([x.hole,x.par,x.wind,x.lie,x.pin,x.startLine,x.shape,x.strike,x.strikeQuality,x.actualClub,x.shotDistance,x.heading,x.gps?.lat,x.gps?.lon,x.gps?.accuracy].map(v=>'"'+String(v??'')+'"').join(',')));const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([rows.join('\\n')],{type:'text/csv'}));a.download='UiDo_Round.csv';a.click();};
  window.addEventListener('uidoNativeGps',e=>{if(e.detail&&e.detail.heading!=null&&e.detail.heading>=0){S.heading=e.detail.heading;$('orient').textContent='Heading '+Math.round(e.detail.heading)+'°';}});
  window.addEventListener('deviceorientationabsolute',e=>{if(e.alpha!=null&&!S.heading){S.heading=Math.round(e.alpha);$('orient').textContent='Heading '+Math.round(e.alpha)+'°';}});
  if(localStorage.getItem('uido_round')){try{const x=JSON.parse(localStorage.getItem('uido_round'));if(x?.shots)S.shots=x.shots;if(x?.pin)S.pin=x.pin;if(x?.strikeQuality)S.strikeQuality=x.strikeQuality;}catch(e){}}
})();
""";
}
