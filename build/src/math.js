/* LaTeX math support for Lilith Learning Lab (no DOM needed except through katex when present).
   Delimiters inside any course text:   $inline$   $$display$$   \(inline\)   \[display\]   and \$ for a literal dollar sign.
   Backtick code spans are never treated as math. A "$" only opens math when the next character is not a space, and only closes
   when the previous character is not a space and the next is not a digit, so prices and shell prompts stay plain text.
   Exports: split, render (HTML), caption (readable unicode), speech (words for the voice), hasMath. */
(function (root) {
  'use strict';

  var RX = /(\\\$)|(`[^`\n]*`)|(\$\$[\s\S]+?\$\$)|(\\\[[\s\S]+?\\\])|(\\\([\s\S]+?\\\))|(\$(?![\s$])(?:[^$\\\n]|\\[\s\S])+?(?<![\s\\])\$(?!\d))/g;

  /* split a string into [{t:'text'|'code'|'math', v, display}] */
  function split(s) {
    s = String(s == null ? '' : s);
    var out = [], last = 0, m;
    RX.lastIndex = 0;
    while ((m = RX.exec(s))) {
      if (m.index > last) out.push({ t: 'text', v: s.slice(last, m.index) });
      if (m[1]) out.push({ t: 'text', v: '$' });
      else if (m[2]) out.push({ t: 'code', v: m[2] });
      else if (m[3]) out.push({ t: 'math', v: m[3].slice(2, -2).trim(), display: true });
      else if (m[4]) out.push({ t: 'math', v: m[4].slice(2, -2).trim(), display: true });
      else if (m[5]) out.push({ t: 'math', v: m[5].slice(2, -2).trim(), display: false });
      else out.push({ t: 'math', v: m[6].slice(1, -1).trim(), display: false });
      last = RX.lastIndex;
    }
    if (last < s.length) out.push({ t: 'text', v: s.slice(last) });
    return out;
  }
  function hasMath(s) { return split(s).some(function (p) { return p.t === 'math'; }); }

  var MACROS = { '\\N': '\\mathbb{N}', '\\Z': '\\mathbb{Z}', '\\R': '\\mathbb{R}', '\\Q': '\\mathbb{Q}', '\\Hom': '\\mathrm{Hom}', '\\Set': '\\mathbf{Set}', '\\Type': '\\mathsf{Type}', '\\Prop': '\\mathsf{Prop}' };
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/[<]/g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

  /* HTML: escape text, **bold**, `code`, and typeset math with KaTeX (falls back to the raw TeX if KaTeX is missing) */
  function render(s) {
    var parts = split(s), hold = [], buf = '';
    parts.forEach(function (p) {
      if (p.t === 'text') buf += p.v;
      else if (p.t === 'code') buf += p.v;
      else { hold.push(p); buf += '' + (hold.length - 1) + ''; }
    });
    var h = esc(buf).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
    return h.replace(/(\d+)/g, function (_, i) {
      var p = hold[+i], k = root.katex;
      if (k && k.renderToString) {
        try { return k.renderToString(p.v, { displayMode: p.display, throwOnError: false, strict: false, trust: false, macros: Object.assign({}, MACROS) }); } catch (e) { /* fall through */ }
      }
      return '<code>' + esc(p.v) + '</code>';
    });
  }

  /* ---------- LaTeX to unicode / spoken words ---------- */
  var SYM = {   // name: [unicode, spoken]
    alpha: ['α', 'alpha'], beta: ['β', 'beta'], gamma: ['γ', 'gamma'], delta: ['δ', 'delta'], epsilon: ['ε', 'epsilon'], varepsilon: ['ε', 'epsilon'], zeta: ['ζ', 'zeta'], eta: ['η', 'eta'], theta: ['θ', 'theta'],
    iota: ['ι', 'iota'], kappa: ['κ', 'kappa'], lambda: ['λ', 'lambda'], mu: ['μ', 'mu'], nu: ['ν', 'nu'], xi: ['ξ', 'xi'], pi: ['π', 'pi'], rho: ['ρ', 'rho'], sigma: ['σ', 'sigma'], tau: ['τ', 'tau'],
    upsilon: ['υ', 'upsilon'], phi: ['φ', 'phi'], varphi: ['φ', 'phi'], chi: ['χ', 'chi'], psi: ['ψ', 'psi'], omega: ['ω', 'omega'],
    Gamma: ['Γ', 'capital gamma'], Delta: ['Δ', 'capital delta'], Theta: ['Θ', 'capital theta'], Lambda: ['Λ', 'capital lambda'], Xi: ['Ξ', 'capital xi'], Pi: ['Π', 'capital pi'], Sigma: ['Σ', 'capital sigma'], Phi: ['Φ', 'capital phi'], Psi: ['Ψ', 'capital psi'], Omega: ['Ω', 'capital omega'],
    to: ['→', ' to '], rightarrow: ['→', ' to '], longrightarrow: ['⟶', ' to '], Rightarrow: ['⇒', ' implies '], Longrightarrow: ['⟹', ' implies '], implies: ['⟹', ' implies '], leftarrow: ['←', ' from '], Leftarrow: ['⇐', ' is implied by '],
    leftrightarrow: ['↔', ' if and only if '], Leftrightarrow: ['⇔', ' if and only if '], iff: ['⟺', ' if and only if '], mapsto: ['↦', ' maps to '], hookrightarrow: ['↪', ' embeds in '], twoheadrightarrow: ['↠', ' onto '], rightsquigarrow: ['⇝', ' leads to '],
    Downarrow: ['⇓', ' reduces to '], uparrow: ['↑', ' up '], downarrow: ['↓', ' down '],
    land: ['∧', ' and '], wedge: ['∧', ' and '], lor: ['∨', ' or '], vee: ['∨', ' or '], neg: ['¬', ' not '], lnot: ['¬', ' not '], forall: ['∀', ' for all '], exists: ['∃', ' there exists '], nexists: ['∄', ' there is no '],
    vdash: ['⊢', ' proves '], models: ['⊨', ' models '], top: ['⊤', ' top '], bot: ['⊥', ' bottom '], perp: ['⊥', ' perp '], dashv: ['⊣', ' is right adjoint to the left adjoint '], mid: ['∣', ' such that '],
    equiv: ['≡', ' is equivalent to '], cong: ['≅', ' is isomorphic to '], simeq: ['≃', ' is equivalent to '], approx: ['≈', ' is about '], sim: ['∼', ' is similar to '], neq: ['≠', ' is not equal to '], ne: ['≠', ' is not equal to '],
    leq: ['≤', ' is at most '], le: ['≤', ' is at most '], geq: ['≥', ' is at least '], ge: ['≥', ' is at least '], lt: ['<', ' is less than '], gt: ['>', ' is greater than '], prec: ['≺', ' precedes '], succ: ['≻', ' succeeds '],
    in: ['∈', ' in '], notin: ['∉', ' not in '], subset: ['⊂', ' is a subset of '], subseteq: ['⊆', ' is a subset of '], supset: ['⊃', ' contains '], cup: ['∪', ' union '], cap: ['∩', ' intersection '], emptyset: ['∅', ' the empty set '], varnothing: ['∅', ' the empty set '],
    times: ['×', ' times '], otimes: ['⊗', ' tensor '], oplus: ['⊕', ' plus '], circ: ['∘', ' composed with '], cdot: ['·', ' dot '], bullet: ['•', ' '], star: ['⋆', ' star '], ast: ['∗', ' star '],
    ldots: ['…', ' dot dot dot '], cdots: ['⋯', ' dot dot dot '], dots: ['…', ' dot dot dot '], infty: ['∞', ' infinity '], sum: ['∑', ' the sum '], prod: ['∏', ' the product '], int: ['∫', ' the integral '], partial: ['∂', ' partial '], nabla: ['∇', ' nabla '],
    langle: ['⟨', ' pair '], rangle: ['⟩', ' '], lbrace: ['{', ' '], rbrace: ['}', ' '], colon: [':', ' colon '], pm: ['±', ' plus or minus '], mp: ['∓', ' minus or plus '], div: ['÷', ' divided by '], min: ['min', ' min '], max: ['max', ' max '],
    sin: ['sin', ' sine '], cos: ['cos', ' cosine '], log: ['log', ' log '], ln: ['ln', ' natural log '], exp: ['exp', ' exp '], lim: ['lim', ' the limit '], det: ['det', ' determinant '], dim: ['dim', ' dimension '], ker: ['ker', ' kernel '],
    sqrt: ['√', ' square root of '], prime: ['′', ' prime '], hbar: ['ℏ', ' h bar '], ell: ['ℓ', ' ell '], Re: ['ℜ', ' real part of '], Im: ['ℑ', ' imaginary part of '], aleph: ['ℵ', ' aleph '], quad: [' ', ' '], qquad: ['  ', ' ']
  };
  var DROP = /^(left|right|big|Big|bigg|Bigg|bigl|bigr|Bigl|Bigr|displaystyle|textstyle|limits|nolimits|,|;|:|!|>|<|quad|qquad|mathstrut|vphantom|hphantom|phantom|scriptstyle)$/;
  var SUP = { '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾', 'n': 'ⁿ', 'i': 'ⁱ', '*': '*' };
  var SUB = { '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉', '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎', 'a': 'ₐ', 'e': 'ₑ', 'i': 'ᵢ', 'j': 'ⱼ', 'k': 'ₖ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ', 'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'x': 'ₓ' };

  /* tiny recursive converter. mode 'u' = unicode caption, 's' = speech */
  function conv(t, mode) {
    var i = 0, n = t.length;
    function group() {      // read {...} or one token; returns the raw inner string
      while (i < n && t[i] === ' ') i++;
      if (t[i] === '{') {
        var d = 1, j = i + 1;
        while (j < n && d > 0) { if (t[j] === '{') d++; else if (t[j] === '}') d--; j++; }
        var inner = t.slice(i + 1, j - 1); i = j; return inner;
      }
      if (t[i] === '\\') { var m = /^\\([A-Za-z]+|.)/.exec(t.slice(i)); i += m[0].length; return m[0]; }
      return t[i++] || '';
    }
    function word() {
      var m = /^[A-Za-z]+/.exec(t.slice(i + 1));
      if (m) { i += 1 + m[0].length; return m[0]; }
      var c = t[i + 1] || ''; i += 2; return c;
    }
    var out = '';
    while (i < n) {
      var c = t[i];
      if (c === '\\') {
        var name = word();
        if (name === 'frac' || name === 'dfrac' || name === 'tfrac') { var a = conv(group(), mode), b = conv(group(), mode); out += mode === 's' ? (' ' + a + ' over ' + b + ' ') : ('(' + a + ')/(' + b + ')'); }
        else if (name === 'sqrt') { var r = conv(group(), mode); out += mode === 's' ? (' square root of ' + r + ' ') : ('√(' + r + ')'); }
        else if (/^(text|mathrm|mathsf|mathbf|mathit|mathtt|mathcal|mathfrak|mathscr|operatorname|textbf|textit|mbox|boldsymbol|bm)$/.test(name)) { var g = group(); out += mode === 's' ? (' ' + conv(g, mode) + ' ') : conv(g, mode); }
        else if (name === 'mathbb') { var l = group(); out += mode === 's' ? (' ' + l + ' ') : ({ N: 'ℕ', Z: 'ℤ', Q: 'ℚ', R: 'ℝ', C: 'ℂ', B: '𝔹', P: 'ℙ' }[l] || l); }
        else if (name === 'xrightarrow' || name === 'xlongrightarrow') { var lab = conv(group(), mode); out += mode === 's' ? (' to via ' + lab + ' ') : ('→[' + lab + ']'); }
        else if (name === 'begin' || name === 'end') { group(); }
        else if (name === '\\') out += mode === 's' ? ' , ' : ' ; ';
        else if (name === '{' || name === '}') out += mode === 's' ? ' ' : name;
        else if (name === ' ' || name === ',' || name === ';' || name === ':' || name === '!' || name === '>') out += ' ';
        else if (name === '&') out += ' ';
        else if (name === '|') out += mode === 's' ? ' norm ' : '‖';
        else if (name === 'lvert' || name === 'rvert') out += mode === 's' ? ' absolute value ' : '|';
        else if (name === 'lVert' || name === 'rVert') out += mode === 's' ? ' norm ' : '‖';
        else if (name === 'lceil' || name === 'rceil' || name === 'lfloor' || name === 'rfloor') out += mode === 's' ? ' ' : { lceil: '⌈', rceil: '⌉', lfloor: '⌊', rfloor: '⌋' }[name];
        else if (DROP.test(name)) { if (name === 'left' || name === 'right' || /^big/i.test(name)) { /* the following delimiter is kept */ } }
        else if (SYM[name]) {
          out += SYM[name][mode === 's' ? 1 : 0];
          if (mode === 'u' && /^[α-ωΑ-Ω]$/.test(SYM[name][0]) && t[i] === ' ' && /[A-Za-z0-9]/.test(t[i + 1] || '')) i++;   // \lambda x -> λx
        }
        else out += mode === 's' ? (' ' + name + ' ') : name;
      } else if (c === '^' || c === '_') {
        i++;
        var arg = group(), isSup = c === '^', raw = conv(arg, mode);
        if (mode === 's') {
          if (isSup) out += ({ '2': ' squared ', '3': ' cubed ', '-1': ' inverse ', '*': ' star ', "'": ' prime ' }[arg.trim()] || (' to the ' + raw + ' '));
          else out += ' sub ' + raw + ' ';
        } else {
          var map = isSup ? SUP : SUB, ok = raw.length > 0 && raw.split('').every(function (ch) { return map[ch]; });
          out += ok ? raw.split('').map(function (ch) { return map[ch]; }).join('') : (isSup ? '^(' + raw + ')' : '_(' + raw + ')');
        }
      } else if (c === '{' || c === '}') { i++; }
      else if (c === '~') { out += ' '; i++; }
      else if (c === '&') { out += mode === 's' ? ' ' : ' '; i++; }
      else if (c === '=' && mode === 's') { out += ' equals '; i++; }
      else if (c === '+' && mode === 's') { out += ' plus '; i++; }
      else if (c === '<' && mode === 's') { out += ' less than '; i++; }
      else if (c === '>' && mode === 's') { out += ' greater than '; i++; }
      else if (c === '|' && mode === 's') { out += ' such that '; i++; }
      else if (c === '-' && mode === 's') { out += ' minus '; i++; }
      else if (c === '*' && mode === 's') { out += ' star '; i++; }
      else if (c === ',' && mode === 's') { out += ', '; i++; }
      else if (c === '(' && mode === 's') { out += ' '; i++; }
      else if (c === ')' && mode === 's') { out += ' '; i++; }
      else { out += c; i++; }
    }
    if (mode === 's') out = out.replace(/([A-Za-z])\s*\(/g, '$1 (').replace(/\s+/g, ' ');
    return out.replace(/\s+/g, ' ').trim();
  }

  function mapText(s, mode, wrapDisplay) {
    return split(s).map(function (p) {
      if (p.t !== 'math') return p.v;
      var r = conv(p.v, mode);
      return mode === 's' ? (p.display && wrapDisplay ? ' The formula: ' + r + '. ' : ' ' + r + ' ') : r;
    }).join('');
  }
  function caption(s) { return mapText(s, 'u', false); }
  function speech(s) { return mapText(s, 's', true); }

  var api = { split: split, hasMath: hasMath, render: render, caption: caption, speech: speech, esc: esc };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LilithMath = api;
})(typeof window !== 'undefined' ? window : globalThis);
