# Embedding and configuring the lab

`build.py` turns a JSON config into one HTML file. The config is read at start-up by `QWL.mount(element, config)`.

```json
{
  "title": "Bell pair", "intro": "HTML allowed",
  "qubits": 2, "steps": 6, "maxQubits": 5, "maxSteps": 14,
  "start": "H-X#0\nI-X#1",
  "startQasm": "...", 
  "palette": ["h","x","cx"],
  "results": ["chances","shots","inspect"],
  "code": ["python","qasm","text","ascii"], "codeOpen": false,
  "console": true, "chips": ["h 0","cx 0 1","run"], "python": true,
  "complete": "all | run | shots", "seed": 1, "shots": 1024,
  "levels": [ { "title": "...", "intro": "...", "start": "I-I-I", "goal": { }, "hint": "...", "solution": "H-I-I", "after": "..." } ]
}
```

| key | meaning |
|---|---|
| `qubits`, `steps` | size of the starting grid. `start`/`startQasm` override the qubit count |
| `palette` | gates in the palette, in order (names from the gate list in the README). Empty array hides nothing: pass the gates you want |
| `results` | which result tabs to show |
| `code` | which code tabs to show. Leave out `"python"` to hide the Python tab |
| `python` | `false` leaves MicroPython out of the build (smaller file) |
| `codeTab`, `resultsTab` | which code tab / result tab is shown first |
| `complete` | when to call `lilith.complete()`: `"all"` (every level solved, default with levels), `"run"` (as soon as the circuit has a gate), `"shots"` (when the console runs shots) |

## Levels and goals

`goal` is data, so a course can be written in JSON:

```json
{ "probs": [ {"state": "11", "min": 0.99}, {"state": "0", "approx": 0.5, "tol": 0.02}, {"state": "1", "max": 0.1} ],
  "gates": { "min": 2, "max": 6, "only": ["h","z"], "require": ["cx"], "forbid": ["x"], "count": {"h": {"min": 2}} },
  "linked": true, "via": "python" }
```

* `state` is a prefix of the result written with qubit 0 on the left, so `"1"` means "qubit 0 is 1" (a marginal) and `"110"` is a full state.
* `linked` is true when a multi-qubit gate (CNOT, CZ, SWAP, CCX) is required, false when none is allowed.
* Gate names are lower case: `h x y z s t cx cz swap ...`.
* `via` (`"python"`, `"qasm"` or `"text"`) means the circuit must have been made by running/applying code in that tab, so a level can teach the code panel.
* `start` uses the Q text notation. `solutionCode` (optional) is shown instead of `solution` and is pasted into the code editor for `via` levels. `solution` is shown by the *Show a solution* button.

## JavaScript API

```js
var lab = QWL.mount(el, config);       // lab.circuit(), lab.setCircuit(c), lab.runCommand("h 0")
var c = QWL.fromText("H-X#0\nI-X#1");  // also QWL.fromQasm(text)
var r = QWL.simulate(c);               // r.probs (qubit 0 is the leftmost digit of the index), r.re, r.im
QWL.toQasm(c, 3); QWL.toPython(c); QWL.toDiagram(c, {unicode:true}); QWL.toText(c);
QWL.sample(c, r, 1000, seed);          // seeded counts
QWL.check(goal, c, r);                 // {ok, why}
```

## Theming

Every colour is a CSS variable on `.qwl` (`--qb-bg`, `--qb-panel`, `--qb-acc`, ...). Override them in your page to restyle the lab. The defaults match the Lilith Learning Lab.

## Hosting

* **webxdc**: `python3 build.py --xdc lab.xdc --config lab.json --out lab.html`.
* **Lilith course**: put the built HTML into a lab: `{"type":"webxdc","title":"...","html":"<built html>"}`.
* **Web page**: iframe the file, or serve it as it is.
