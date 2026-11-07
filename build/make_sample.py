#!/usr/bin/env python3
"""Write a small sample course on a different subject (percentages) to show the JSON format works for any topic."""
import json, sys

APP_HTML = '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font:16px system-ui;margin:0;padding:16px;background:#150d27;color:#f1ebff}.bar{height:36px;border-radius:8px;background:#261b3b;overflow:hidden;margin:12px 0}.bar i{display:block;height:100%;background:#b26bff;width:0}input{width:100%}#t{font-size:22px}</style></head><body><div id="t"></div><div class="bar"><i id="f"></i></div><input id="s" type="range" min="0" max="100" value="10"><p>Slide to 35% to complete.</p><script>var s=document.getElementById("s"),f=document.getElementById("f"),t=document.getElementById("t"),d=false;function u(v){f.style.width=v+"%";t.textContent=v+"% = "+(v/100)+" = "+v+"/100";if(+v===35&&!d){d=true;lilith.complete()}}s.oninput=function(){u(+s.value);webxdc.sendUpdate({payload:{v:+s.value}},"")};webxdc.setUpdateListener(function(x){if(x.payload&&x.payload.v!==undefined){s.value=x.payload.v;u(x.payload.v)}},0);u(+s.value);</script></body></html>'''


def course():
    return {
      "format": "lilith-course", "version": 1, "id": "everyday-percentages", "title": "Everyday Math: Percentages",
      "subtitle": "A tiny sample course in a different subject", "author": "Lilith Learning Lab",
      "description": "Two short chapters on percentages. It exists to show that any subject can be taught with the same format: maps, summaries, glossary, quiz and practice labs of every type.",
      "chapters": [
        {"id": "p1", "title": "What a percent means",
         "maps": [{"title": "Percent basics", "links": [
            "Percent | means | Per hundred",
            "Percent | is written as | Fraction",
            "Percent | is written as | Decimal",
            "Fraction | has denominator | 100",
            "Decimal | is | Percent divided by 100",
            "50 percent | equals | One half [ch2]"]}],
         "summary": ["A percent is a number out of one hundred. Fifty percent means fifty out of every hundred, which is one half.", "You can write the same amount as a percent, a fraction or a decimal, and switching between them is just moving the decimal point."],
         "glossary": [{"term": "Percent", "def": "A number expressed as parts per hundred, written with the % sign."}, {"term": "Decimal", "def": "A number written with a decimal point, such as 0.25."}, {"term": "Fraction", "def": "A number written as one whole number over another, such as 1/4."}],
         "keyPoints": ["Percent means per hundred.", "To turn a percent into a decimal, divide by 100.", "To turn a decimal into a percent, multiply by 100.", "25% = 0.25 = 1/4."],
         "lesson": [{"type": "text", "items": ["Think of a percent as a recipe for slicing a whole into 100 equal pieces.", "So 30% is 30 of those pieces, or 0.30 of the whole."]}, {"type": "code", "lang": "text", "code": "50%  = 0.50 = 1/2\n25%  = 0.25 = 1/4\n10%  = 0.10 = 1/10\n100% = 1.00 = the whole thing"}],
         "quiz": [{"q": "What is 25% as a decimal?", "options": ["2.5", "0.25", "0.025", "25"], "answer": 1, "explain": "Divide by 100: 25 / 100 = 0.25."},
                  {"q": "Which fraction equals 50%?", "options": ["1/4", "1/3", "1/2", "2/3"], "answer": 2, "explain": "Fifty out of one hundred is one half."},
                  {"q": "How do you turn 0.4 into a percent?", "options": ["Divide by 100", "Multiply by 100", "Add 100", "Subtract 100"], "answer": 1, "explain": "0.4 times 100 = 40%."}],
         "cards": [{"q": "What does percent mean?", "a": "Per hundred."}, {"q": "10% as a decimal?", "a": "0.10"}],
         "practice": [
            {"type": "fill", "title": "Fill the blanks", "text": "Percent means per {{hundred|100}}. So 75% as a decimal is {{0.75|.75}}."},
            {"type": "match", "title": "Match the forms", "intro": "Match each percent to its fraction.", "pairs": [["50%", "1/2"], ["25%", "1/4"], ["10%", "1/10"], ["100%", "1"]]},
            {"type": "order", "title": "Percent to decimal", "intro": "Put the steps in order.", "items": ["Look at the percent, for example 35%", "Drop the % sign", "Divide by 100", "Read the decimal: 0.35"]}]},
        {"id": "p2", "number": 2, "title": "Finding a percent of a number",
         "maps": [{"title": "Percent of a number", "links": [
            "Percent of a number | needs | The percent",
            "Percent of a number | needs | The whole",
            "The percent | becomes | A decimal [ch1]",
            "A decimal | is multiplied by | The whole",
            "Product | is | The answer",
            "Tip 10% | is | Move the decimal one place"]}],
         "summary": ["To find a percent of a number, turn the percent into a decimal and multiply. So 20% of 80 is 0.20 times 80, which is 16."],
         "glossary": [{"term": "Whole", "def": "The full amount you are taking a percent of."}, {"term": "Product", "def": "The result of multiplying two numbers."}],
         "keyPoints": ["Percent of a number = (percent / 100) x number.", "10% of a number: move the decimal point one place left.", "50% is half; 25% is a quarter."],
         "lesson": [{"type": "text", "items": ["Worked example: 15% of 60. Step one: 15 / 100 = 0.15. Step two: 0.15 x 60 = 9."]}, {"type": "code", "lang": "javascript", "code": "function percentOf(p, whole) {\n  return p / 100 * whole;\n}\npercentOf(15, 60); // 9"}],
         "quiz": [{"q": "What is 20% of 80?", "options": ["8", "16", "20", "64"], "answer": 1, "explain": "0.20 x 80 = 16."},
                  {"q": "What is 10% of 350?", "options": ["3.5", "350", "35", "10"], "answer": 2, "explain": "Move the decimal point one place left: 35."}],
         "cards": [{"q": "Formula for p% of w?", "a": "p / 100 x w"}],
         "practice": [
            {"type": "code", "title": "Write percentOf", "intro": "Write percentOf(p, whole): p percent of whole.", "fn": "percentOf", "starter": "function percentOf(p, whole) {\n  // your code\n}", "tests": [{"args": [20, 80], "expect": 16}, {"args": [50, 10], "expect": 5}, {"args": [15, 60], "expect": 9}, {"args": [0, 99], "expect": 0}], "hint": "Divide p by 100, then multiply by whole.", "solution": "function percentOf(p, whole) {\n  return p / 100 * whole;\n}"},
            {"type": "write", "title": "Say it with numbers", "prompt": "Write the multiplication that finds 30% of 200 (use 0.3 or 0.30).", "checks": [{"re": "0?\\.30?", "msg": "uses 0.3"}, {"re": "200", "msg": "uses 200"}, {"re": "[x*]", "msg": "multiplies"}], "solution": "0.3 * 200 = 60"},
            {"type": "webxdc", "title": "Percent slider", "intro": "An interactive app inside the course file. Slide to 35% to finish.", "height": 300, "html": APP_HTML},
            {"type": "terminal", "title": "Percent calculator", "intro": "A tiny calculator shell: try  calc 20 of 80", "prompt": "calc>", "chips": ["calc 20 of 80", "calc 50 of 10", "calc 10 of 350"],
             "commands": [{"re": "^calc 20 of 80$", "out": ["16"]}, {"re": "^calc 50 of 10$", "out": ["5"]}, {"re": "^calc 10 of 350$", "out": ["35"]}, {"re": "^calc ", "out": ["Try: calc 20 of 80, calc 50 of 10 or calc 10 of 350"], "cls": "warn"}],
             "tasks": [{"text": "Find 20% of 80", "cmd": "^calc 20 of 80$"}, {"text": "Find 10% of 350", "cmd": "^calc 10 of 350$"}]}]}
      ],
      "sandbox": {"type": "terminal", "title": "Calculator", "prompt": "calc>", "intro": "Try: calc 20 of 80", "chips": ["calc 20 of 80"], "commands": [{"re": "^calc 20 of 80$", "out": ["16"]}]}
    }

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "sample.course.json"
    json.dump(course(), open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out)
