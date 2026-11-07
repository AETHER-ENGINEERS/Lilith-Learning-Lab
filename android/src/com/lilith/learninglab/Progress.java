package com.lilith.learninglab;

import android.speech.tts.UtteranceProgressListener;

/** Forwards text-to-speech events to the page (window.__ttsEvent). */
class Progress extends UtteranceProgressListener {
    private final MainActivity a;
    Progress(MainActivity a) { this.a = a; }
    @Override public void onStart(String id) { a.event(id, "start"); a.keepAwake(true); }
    @Override public void onDone(String id) { a.event(id, "done"); a.keepAwake(false); }
    @Override public void onError(String id) { a.event(id, "error"); a.keepAwake(false); }
    @Override public void onStop(String id, boolean interrupted) { a.keepAwake(false); }
    @Override public void onRangeStart(String id, int start, int end, int frame) { a.event(id, "range"); }
}
