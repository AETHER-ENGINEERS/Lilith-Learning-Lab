Jade Agent Kit 0.1.0 (https://github.com/lucky-edgelord/Jade-agent-kit, commit f1eba08), MIT.
jade-agent-kit.iife.js is src/index.js bundled by esbuild as an IIFE (global JadeKit) with
import.meta.url defined as "https://kit.local/dist/jade-agent-kit.js", so its assets resolve to https://kit.local/assets/,
a virtual host served from memory by build/src/net.js (works offline, including file:// in the Android WebView).
busybox.wasm / busybox.glue.js are the kit's assets (BusyBox is GPL-2.0; source: see THIRD_PARTY_NOTICES.md).
MicroPython is not duplicated: net.js serves the app's own copy (mp.js) to the kit.
SQLite (sqlite3.wasm) is not bundled; the agent is not given the sqlite tool.
Rebuild: in the kit repo, esbuild src/index.js --bundle --format=iife --global-name=JadeKit --minify --define:import.meta.url='"https://kit.local/dist/jade-agent-kit.js"'
