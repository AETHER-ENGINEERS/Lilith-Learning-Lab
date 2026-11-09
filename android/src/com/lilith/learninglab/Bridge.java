package com.lilith.learninglab;

import android.speech.tts.TextToSpeech;
import android.webkit.JavascriptInterface;

/** JavaScript bridge: window.AndroidTTS.speak(text, rate, id) / stop() / isReady() / copy(text) / share(title, text) / fetchUrl(url, id). Runs on a WebView background thread. */
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

    /** Downloads a text file over HTTPS from raw.githubusercontent.com only (course catalog and course files). Result goes to window.__netDone(id, ok, text). */
    @JavascriptInterface
    public void fetchUrl(final String url, final int id) {
        new Thread(() -> {
            String text; boolean ok = false;
            try {
                java.net.URL u = new java.net.URL(url);
                if (!"https".equals(u.getProtocol()) || !"raw.githubusercontent.com".equals(u.getHost())) throw new java.io.IOException("Only raw.githubusercontent.com is allowed");
                java.net.HttpURLConnection c = (java.net.HttpURLConnection) u.openConnection();
                c.setConnectTimeout(15000); c.setReadTimeout(30000); c.setInstanceFollowRedirects(true);
                c.setRequestProperty("User-Agent", "LilithLearningLab");
                int code = c.getResponseCode();
                if (code != 200) throw new java.io.IOException("HTTP " + code);
                java.io.InputStream in = c.getInputStream();
                java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
                byte[] buf = new byte[16384]; int n; long total = 0;
                while ((n = in.read(buf)) > 0) { total += n; if (total > 20L * 1024 * 1024) throw new java.io.IOException("File too large"); out.write(buf, 0, n); }
                in.close();
                text = out.toString("UTF-8"); ok = true;
            } catch (Exception e) {
                text = String.valueOf(e.getMessage() == null ? e.toString() : e.getMessage());
            }
            final String q = org.json.JSONObject.quote(text); final boolean fok = ok;
            a.runOnUiThread(() -> a.web.evaluateJavascript("window.__netDone&&window.__netDone(" + id + "," + fok + "," + q + ")", null));
        }).start();
    }
}
