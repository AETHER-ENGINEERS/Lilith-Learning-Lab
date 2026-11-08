MicroPython WebAssembly port, from the npm package @micropython/micropython-webassembly-pyscript 1.29.0-6.
MicroPython is MIT licensed (https://micropython.org, https://github.com/micropython/micropython).
Files: micropython.mjs (loader) and micropython.wasm (interpreter, ~450 KB).
build_web.py packs them into mp.js, which the app loads with a script tag so no file fetch is needed.
The loader is turned into a classic script at build time; the wasm bytes are handed to the Worker and loaded from a blob URL.
