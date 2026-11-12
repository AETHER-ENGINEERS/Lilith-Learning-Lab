# Quantum Web Lab

A phone-friendly quantum circuit lab that runs entirely in the browser, offline, in one HTML file.
Built for courses: configure it with a small JSON file (levels, gates, start circuits) and drop it into any page or webxdc app.

* **Composer** in the spirit of IBM Quantum Composer: colour-coded gate palette, tap-to-place circuit grid, a probability dial on every wire, chances, shots with a seed, and an *Inspect* view with amplitudes, phase dials and Bloch discs. Made for thumbs.
* **Code, both ways.** Edit the circuit or edit the code, and the other side follows:
  * **MicroQiskit** (Python, runs on MicroPython compiled to WebAssembly) , see [docs/microqiskit.md](docs/microqiskit.md)
  * **micro QASM** (OpenQASM 3 and 2 subset) , see [docs/microqasm.md](docs/microqasm.md)
  * **Q text**, the compact `H-X#0` notation from [Q.js](https://github.com/stewdio/q.js)
  * **ASCII diagram** of the circuit, Q.js style, unicode or plain
* **Q Console**, a forgiving command line for beginners and kids: `h 0`, `cx 0 1`, `run`, `explain`.
* **Levels**: declarative goals in JSON, so a course can ship challenges without writing code.
* **No dependencies, no network.** Own state-vector simulator (up to 12 qubits), own parsers. MicroPython (MIT) is bundled as WebAssembly for the Python tab.

## Quick start

```sh
python3 build.py                      # dist/quantum-web-lab.html and dist/quantum-web-lab.xdc
python3 build.py --config lab.json --out lab.html   # your own lab
python3 build.py --no-python          # leave MicroPython out (about 90 KB instead of 390 KB)
```

Open the HTML file in a browser. The `.xdc` is a [webxdc](https://webxdc.org) app for Delta Chat and compatible hosts.

## For course authors

```python
import build
html = build.build_html({"title": "Make a Bell pair", "qubits": 2, "levels": [...]}, python=True)
```

The config format, the goal language and the JavaScript API are in [docs/embedding.md](docs/embedding.md).
The lab calls `window.lilith.complete()` (if present) when the learner finishes, which is how the Lilith Learning Lab marks a lab as done.

## Conventions

* The composer and the Q text put **qubit 0 on top and on the left** of a result like `01` (Q.js style). Qiskit and MicroQiskit put qubit 0 on the **right**. A button above the chart flips the labels, and the Python tab says so.
* Gates: `i h x y z s sdg t tdg sx sxdg rx ry rz p cx cy cz ch cp ccx ccz swap measure`.

## Tests

```sh
node tests/core.test.js                  # simulator, text, ASCII, QASM, goals
node tests/microqiskit.test.mjs          # MicroQiskit on real MicroPython/WASM, cross-checked with the JS core
python3 tests/ui_test.py                 # Playwright: tapping, code round trips, Python run, console, levels
```

## Licence and credits

MIT. See [LICENSE](LICENSE). The Q text notation and the ASCII diagram style follow [Q.js](https://github.com/stewdio/q.js) by Stewart Smith (MIT, [docs/Q.js-LICENSE.md](docs/Q.js-LICENSE.md)); no Q.js code is used.
The look of the composer takes ideas from IBM Quantum Composer. MicroPython is MIT licensed (`vendor/micropython`).
