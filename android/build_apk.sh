#!/bin/bash
# Build, sign and verify the APK with the plain Android SDK tools (no Gradle).
# Needs: JDK 17+, Android SDK with platforms;android-34 and build-tools;34.0.0 (set ANDROID_SDK_ROOT).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SDK="${ANDROID_SDK_ROOT:-/home/claude/android/sdk}"
BT="$SDK/build-tools/34.0.0"; AJ="$SDK/platforms/android-34/android.jar"
OUT="$HERE/out"; APK_NAME="${APK_NAME:-LilithLearningLab.apk}"
VERSION_NAME="${VERSION_NAME:-2.0.0}"; VERSION_CODE="${VERSION_CODE:-3}"
KS="$HERE/teacher-xavier.jks"; KS_PASS="${KS_PASS:-teacher-xavier}"

rm -rf "$OUT" "$HERE/assets" && mkdir -p "$OUT/classes" "$OUT/dex" "$HERE/assets"
python3 "$HERE/../build/build_web.py" --web "$HERE/assets"                       # tutorial -> index.html + avatar frames

"$BT/aapt2" compile --dir "$HERE/res" -o "$OUT/res.zip"
"$BT/aapt2" link -o "$OUT/base.apk" -I "$AJ" --manifest "$HERE/AndroidManifest.xml" \
  --min-sdk-version 24 --target-sdk-version 34 --version-code "$VERSION_CODE" --version-name "$VERSION_NAME" \
  -A "$HERE/assets" "$OUT/res.zip"
javac --release 8 -g:none -Xlint:-options -classpath "$AJ" -d "$OUT/classes" "$HERE"/src/com/lilith/learninglab/*.java
"$BT/d8" --lib "$AJ" --min-api 24 --output "$OUT/dex" $(find "$OUT/classes" -name '*.class')
(cd "$OUT/dex" && zip -q -j "$OUT/base.apk" classes.dex)
"$BT/zipalign" -f -p 4 "$OUT/base.apk" "$OUT/aligned.apk"
if [ ! -f "$KS" ]; then
  keytool -genkeypair -keystore "$KS" -storepass "$KS_PASS" -keypass "$KS_PASS" -alias teacher -keyalg RSA -keysize 2048 \
    -validity 36500 -dname "CN=Lilith Learning Lab, C=US" 2>/dev/null
fi
"$BT/apksigner" sign --ks "$KS" --ks-pass "pass:$KS_PASS" --key-pass "pass:$KS_PASS" --ks-key-alias teacher --out "$HERE/$APK_NAME" "$OUT/aligned.apk"
"$BT/apksigner" verify --verbose "$HERE/$APK_NAME"
"$BT/aapt2" dump badging "$HERE/$APK_NAME" | head -12
ls -l "$HERE/$APK_NAME"
