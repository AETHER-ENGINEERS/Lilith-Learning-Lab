package com.lilith.learninglab;

import android.content.Intent;
import android.net.Uri;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebView;

/** Lets <input type="file"> in the page open Android's file picker (used to import course JSON and .xdc apps). */
class FileChooser extends WebChromeClient {
    static final int REQ = 4201;
    private final MainActivity a;
    ValueCallback<Uri[]> pending;
    FileChooser(MainActivity a) { this.a = a; }

    @Override
    public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> cb, FileChooserParams params) {
        if (pending != null) pending.onReceiveValue(null);
        pending = cb;
        Intent i = new Intent(Intent.ACTION_GET_CONTENT);
        i.addCategory(Intent.CATEGORY_OPENABLE);
        i.setType("*/*");
        i.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
        try { a.startActivityForResult(Intent.createChooser(i, "Choose a course file"), REQ); }
        catch (Exception e) { pending = null; cb.onReceiveValue(null); return false; }
        return true;
    }

    void result(int code, Intent data) {
        if (pending == null) return;
        Uri[] out = null;
        if (code == MainActivity.RESULT_OK && data != null) {
            if (data.getClipData() != null) {
                int n = data.getClipData().getItemCount(); out = new Uri[n];
                for (int k = 0; k < n; k++) out[k] = data.getClipData().getItemAt(k).getUri();
            } else if (data.getData() != null) out = new Uri[] { data.getData() };
        }
        pending.onReceiveValue(out);
        pending = null;
    }
}
