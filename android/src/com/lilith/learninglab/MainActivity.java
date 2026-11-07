package com.lilith.learninglab;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.view.View;
import android.view.Window;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.util.Locale;

/**
 * Lilith Learning Lab: a standalone, offline Android app.
 * Courses are imported as JSON files; lectures, concept maps, quizzes and practice labs run as a local web page (assets/index.html) in a WebView.
 * Teacher's voice uses Android's built-in text-to-speech engine through the AndroidTTS bridge below.
 */
public class MainActivity extends Activity implements TextToSpeech.OnInitListener {
    private WebView web;
    private FileChooser chooser;
    TextToSpeech tts;
    volatile boolean ttsReady = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Window w = getWindow();
        w.setStatusBarColor(Color.parseColor("#0F0B18"));
        w.setNavigationBarColor(Color.parseColor("#0F0B18"));

        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#0F0B18"));
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);                    // progress and settings are kept with localStorage
        s.setAllowFileAccess(true);                      // loads the bundled assets
        s.setAllowContentAccess(false);
        s.setAllowFileAccessFromFileURLs(false);
        s.setAllowUniversalAccessFromFileURLs(false);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setCacheMode(WebSettings.LOAD_NO_CACHE);
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);
        chooser = new FileChooser(this);
        web.setWebChromeClient(chooser);
        web.setWebViewClient(new OfflineClient());
        web.addJavascriptInterface(new Bridge(this), "AndroidTTS");
        setContentView(web);

        tts = new TextToSpeech(this, this);
        web.loadUrl("file:///android_asset/index.html");
    }

    @Override
    protected void onActivityResult(int req, int code, android.content.Intent data) {
        if (req == FileChooser.REQ && chooser != null) chooser.result(code, data); else super.onActivityResult(req, code, data);
    }

    @Override
    public void onInit(int status) {
        if (status != TextToSpeech.SUCCESS) { ttsReady = false; return; }
        int r = tts.setLanguage(Locale.US);
        if (r == TextToSpeech.LANG_MISSING_DATA || r == TextToSpeech.LANG_NOT_SUPPORTED) tts.setLanguage(Locale.getDefault());
        tts.setPitch(1.05f);
        tts.setOnUtteranceProgressListener(new Progress(this));
        ttsReady = true;
    }

    void keepAwake(final boolean on) {
        runOnUiThread(() -> web.setKeepScreenOn(on));
    }

    void event(String utteranceId, final String type) {
        final String id = utteranceId.startsWith("u") ? utteranceId.substring(1) : utteranceId;
        runOnUiThread(() -> web.evaluateJavascript("window.__ttsEvent&&window.__ttsEvent(" + id + ",'" + type + "')", null));
    }

    @Override
    public void onBackPressed() {
        web.evaluateJavascript("(function(){return window.__onBack ? window.__onBack() : false;})()", value -> { if (value == null || !value.equals("true")) leave(); });
    }

    private void leave() { super.onBackPressed(); }

    @Override
    protected void onDestroy() {
        if (tts != null) { tts.stop(); tts.shutdown(); }
        if (web != null) { web.destroy(); }
        super.onDestroy();
    }
}
