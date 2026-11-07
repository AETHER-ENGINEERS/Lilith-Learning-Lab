package com.lilith.learninglab;

import android.speech.tts.TextToSpeech;
import android.webkit.JavascriptInterface;

/** JavaScript bridge: window.AndroidTTS.speak(text, rate, id) / stop() / isReady() / copy(text) / share(title, text). Runs on a WebView background thread. */
class Bridge {
    private final MainActivity a;
    Bridge(MainActivity a) { this.a = a; }

    @JavascriptInterface
    public void speak(String text, float rate, int id) {
        if (!a.ttsReady) { a.event("u" + id, "error"); return; }
        float r = Math.max(0.5f, Math.min(2.5f, rate));
        a.tts.setSpeechRate(r);
        int res = a.tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "u" + id);
        if (res != TextToSpeech.SUCCESS) a.event("u" + id, "error");
    }

    @JavascriptInterface
    public void stop() { if (a.tts != null) a.tts.stop(); }

    @JavascriptInterface
    public boolean isReady() { return a.ttsReady; }

    @JavascriptInterface
    public void copy(final String text) {
        a.runOnUiThread(() -> {
            android.content.ClipboardManager cm = (android.content.ClipboardManager) a.getSystemService(android.content.Context.CLIPBOARD_SERVICE);
            if (cm != null) cm.setPrimaryClip(android.content.ClipData.newPlainText("Lilith Learning Lab", text));
        });
    }

    @JavascriptInterface
    public void share(final String title, final String text) {
        a.runOnUiThread(() -> {
            android.content.Intent i = new android.content.Intent(android.content.Intent.ACTION_SEND);
            i.setType("text/plain");
            i.putExtra(android.content.Intent.EXTRA_SUBJECT, title);
            i.putExtra(android.content.Intent.EXTRA_TEXT, text);
            try { a.startActivity(android.content.Intent.createChooser(i, title)); } catch (Exception e) { /* no share target */ }
        });
    }
}
