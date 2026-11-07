package com.lilith.learninglab;

import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/** Fully offline: never navigate away from the bundled page. */
class OfflineClient extends WebViewClient {
    @Override
    public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
        return !request.getUrl().toString().startsWith("file:///android_asset/");
    }
}
