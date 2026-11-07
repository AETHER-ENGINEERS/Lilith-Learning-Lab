#!/usr/bin/env python3
"""Build the Reinforcement Learning with Python course (Gymnasium + Stable-Baselines3).
Usage: python3 make_rl_course.py <out.json>"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "rl"))
import part1, part2, part3  # noqa: E402

PAGE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font:15px system-ui,Roboto,sans-serif;margin:0;padding:12px;background:#150d27;color:#f1ebff}
button{font:inherit;border:0;border-radius:20px;padding:8px 14px;background:#b26bff;color:#1b0b33;font-weight:600;margin:3px 3px 3px 0}
button.t{background:#2d2046;color:#e7d9ff}.row{display:flex;flex-wrap:wrap;align-items:center;gap:4px}
.bar{height:10px;border-radius:5px;background:#261b3b;overflow:hidden}.bar i{display:block;height:100%;background:#b26bff;width:0}
small,.m{color:#c9b8e8}input[type=range]{width:140px}%STYLE%</style></head><body>%BODY%<script>
function done(){try{if(window.lilith)lilith.complete()}catch(e){}}
%SCRIPT%</script></body></html>"""

BANDIT = PAGE.replace("%STYLE%", ".arm button{white-space:nowrap}.arm{display:grid;grid-template-columns:84px 1fr 78px;gap:8px;align-items:center;margin:6px 0}").replace("%BODY%", """
<div class="m">Five slot machines with hidden average payouts. Pull to learn. The bars are your running estimates.</div>
<div id="arms"></div>
<div class="row"><label class="m">epsilon <input id="e" type="range" min="0" max="100" value="10"> <b id="ev">0.10</b></label>
<button id="auto" class="t">Auto pull x10 (epsilon-greedy)</button><button id="rst" class="t">New machines</button></div>
<div class="m" id="st"></div><div class="bar"><i id="pg"></i></div><div class="m">Make 40 pulls to finish.</div>""").replace("%SCRIPT%", """
var N=5,mu,Q,C,total,pulls;
function init(){mu=[];for(var i=0;i<N;i++)mu.push(Math.random());Q=Array(N).fill(0);C=Array(N).fill(0);total=0;pulls=0;draw()}
function gauss(){return (Math.random()+Math.random()+Math.random()-1.5)/0.5}
function pull(a){var r=mu[a]+0.25*gauss();C[a]++;Q[a]+=(r-Q[a])/C[a];total+=r;pulls++;draw();if(pulls>=40)done()}
function greedy(){var b=0;for(var i=1;i<N;i++)if(Q[i]>Q[b])b=i;return b}
function eps(){return +document.getElementById('e').value/100}
function draw(){var h='';for(var i=0;i<N;i++){var w=Math.max(0,Math.min(100,Q[i]*100));h+='<div class="arm"><button data-a="'+i+'">Arm '+(i+1)+'</button><div class="bar"><i style="width:'+w+'%"></i></div><small>'+Q[i].toFixed(2)+' ('+C[i]+')</small></div>'}
document.getElementById('arms').innerHTML=h;document.getElementById('ev').textContent=eps().toFixed(2);
var best=0;for(var j=1;j<N;j++)if(mu[j]>mu[best])best=j;
document.getElementById('st').textContent='Pulls: '+pulls+'   total reward: '+total.toFixed(1)+(pulls>=8?'   (the truly best arm is Arm '+(best+1)+' when you want to check)':'');
document.getElementById('pg').style.width=Math.min(100,pulls/40*100)+'%';
Array.prototype.forEach.call(document.querySelectorAll('[data-a]'),function(b){b.onclick=function(){pull(+b.dataset.a)}})}
document.getElementById('e').oninput=draw;
document.getElementById('auto').onclick=function(){for(var k=0;k<10;k++){pull(Math.random()<eps()?Math.floor(Math.random()*N):greedy())}};
document.getElementById('rst').onclick=init;init();""")

GRID = PAGE.replace("%STYLE%", "table{border-collapse:collapse;margin:8px 0}td{width:52px;height:52px;border:1px solid #3a2a5c;text-align:center;font-size:24px;padding:0}.g{background:#2c4a1f}.p{background:#5a1a2a}.s{background:#2a1f4a}.path{outline:2px solid #b26bff;outline-offset:-3px}").replace("%BODY%", """
<div class="m">Start is S, goal is the star, the pit is the red cell. Arrows show the best action learned so far.</div>
<table id="t"></table>
<div class="row"><button id="b1">Train 20 episodes</button><button id="b2">Train 300</button><button id="b3" class="t">Reset</button></div>
<div class="m" id="st"></div>""").replace("%SCRIPT%", """
var R=5,Cc=5,A=4,goal=[4,4],pit=[2,2],wall=[[1,1],[3,2]],Q,ep,rng=Math.random;
var DX=[-1,0,1,0],DY=[0,1,0,-1],AR=['\\u2190','\\u2193','\\u2192','\\u2191'];
function id(r,c){return r*Cc+c}function isWall(r,c){return wall.some(function(w){return w[0]===r&&w[1]===c})}
function reset(){Q=[];for(var i=0;i<R*Cc;i++)Q.push([0,0,0,0]);ep=0;draw([])}
function step(r,c,a){var nr=r+DY[a],nc=c+DX[a];if(nr<0||nr>=R||nc<0||nc>=Cc||isWall(nr,nc)){nr=r;nc=c}
var rew=-0.01,fin=false;if(nr===goal[0]&&nc===goal[1]){rew=1;fin=true}else if(nr===pit[0]&&nc===pit[1]){rew=-1;fin=true}return [nr,nc,rew,fin]}
function best(s){var b=0;for(var i=1;i<A;i++)if(Q[s][i]>Q[s][b])b=i;return b}
function train(n){var alpha=0.5,gamma=0.95,eps=0.2;for(var e=0;e<n;e++){var r=0,c=0;for(var t=0;t<60;t++){var s=id(r,c),a=rng()<eps?Math.floor(rng()*A):best(s);
var o=step(r,c,a),s2=id(o[0],o[1]);var tgt=o[3]?o[2]:o[2]+gamma*Math.max.apply(null,Q[s2]);Q[s][a]+=alpha*(tgt-Q[s][a]);r=o[0];c=o[1];if(o[3])break}ep++}
var p=greedyPath();draw(p.cells);var ok=p.ok;document.getElementById('st').textContent='Episodes: '+ep+(ok?'   Greedy path reaches the goal in '+p.cells.length+' cells.':'   Greedy path does not reach the goal yet.');if(ok)done()}
function greedyPath(){var r=0,c=0,cells=[[0,0]];for(var t=0;t<30;t++){var o=step(r,c,best(id(r,c)));r=o[0];c=o[1];cells.push([r,c]);if(o[3])return {cells:cells,ok:r===goal[0]&&c===goal[1]}}return {cells:cells,ok:false}}
function draw(path){var h='';for(var r=0;r<R;r++){h+='<tr>';for(var c=0;c<Cc;c++){var cl='',tx='';var onp=path.some(function(p){return p[0]===r&&p[1]===c});
if(r===goal[0]&&c===goal[1]){cl='g';tx='\\u2605'}else if(r===pit[0]&&c===pit[1]){cl='p'}else if(isWall(r,c)){cl='s';tx='\\u25A0'}
else if(r===0&&c===0&&ep===0){cl='s';tx='S'}else if(ep>0){tx=AR[best(id(r,c))]}else tx='\\u00B7';
h+='<td class="'+cl+(onp?' path':'')+'">'+tx+'</td>'}h+='</tr>'}document.getElementById('t').innerHTML=h;if(!ep)document.getElementById('st').textContent='Episodes: 0'}
document.getElementById('b1').onclick=function(){train(20)};document.getElementById('b2').onclick=function(){train(300)};document.getElementById('b3').onclick=reset;reset();""")

PRONOUNCE = {
    "Gymnasium": "jim nay zee um", "PPO": "P P O", "DQN": "D Q N", "A2C": "A 2 C", "SAC": "sack", "TD3": "T D 3", "DDPG": "D D P G",
    "TRPO": "T R P O", "SB3": "S B 3", "MDP": "M D P", "RL": "R L", "RLHF": "R L H F", "GAE": "G A E", "KL": "K L",
    "MlpPolicy": "M L P policy", "CnnPolicy": "C N N policy", "numpy": "num pie", "NumPy": "num pie", "PyTorch": "pie torch",
    "TensorBoard": "tensor board", "VecNormalize": "vec normalize", "CartPole": "cart pole", "FrozenLake": "frozen lake",
    "LineWorld": "line world", "MuJoCo": "mew jo co", "env": "environment", "venv": "V env", "gamma": "gamma", "Atari": "a tarry",
    "VecFrameStack": "vec frame stack", "DummyVecEnv": "dummy vec environment", "SubprocVecEnv": "sub process vec environment",
    "EvalCallback": "eval callback", "sb3-contrib": "S B 3 contrib", "pip": "pip", "Q-learning": "Q learning", "Q-table": "Q table",
}

SANDBOX = {
    "type": "terminal", "title": "Algorithm cheat sheet", "prompt": "rl>",
    "intro": "A scripted lookup tool, not a real Python shell. Try: algo ppo, compare, defaults ppo, spaces",
    "chips": ["algo ppo", "algo dqn", "algo sac", "compare", "defaults ppo", "spaces", "help"],
    "commands": [
        {"re": "^help$", "out": ["algo <ppo|a2c|dqn|sac|td3|ddpg>   what it is and when to use it", "compare                          table of action spaces and data use", "defaults ppo                     main PPO defaults in SB3", "spaces                           Gymnasium spaces cheat sheet"]},
        {"re": "^algo ppo$", "out": ["PPO: on-policy actor-critic with a clipped objective.", "Actions: discrete or continuous. Use as a strong default.", "Tip: use several parallel envs (make_vec_env)."]},
        {"re": "^algo a2c$", "out": ["A2C: on-policy actor-critic, synchronous advantage updates.", "Actions: discrete or continuous. Simple and fast, often noisier than PPO."]},
        {"re": "^algo dqn$", "out": ["DQN: off-policy value-based with replay buffer and target network.", "Actions: discrete only. Good for games and image inputs."]},
        {"re": "^algo sac$", "out": ["SAC: off-policy actor-critic with an entropy bonus.", "Actions: continuous only. Sample efficient and robust for control."]},
        {"re": "^algo td3$", "out": ["TD3: off-policy deterministic actor-critic with twin critics.", "Actions: continuous only."]},
        {"re": "^algo ddpg$", "out": ["DDPG: off-policy deterministic actor-critic, an ancestor of TD3.", "Actions: continuous only. Sensitive to settings."]},
        {"re": "^algo ", "out": ["Unknown algorithm. Try: ppo a2c dqn sac td3 ddpg"], "cls": "warn"},
        {"re": "^compare$", "out": ["algo  actions            data", "PPO   discrete+continuous on-policy", "A2C   discrete+continuous on-policy", "DQN   discrete            off-policy", "SAC   continuous          off-policy", "TD3   continuous          off-policy", "DDPG  continuous          off-policy"]},
        {"re": "^defaults ppo$", "out": ["learning_rate 3e-4", "n_steps 2048 (per env)", "batch_size 64", "n_epochs 10", "gamma 0.99", "gae_lambda 0.95", "clip_range 0.2", "(check your SB3 version's docs to confirm)"]},
        {"re": "^spaces$", "out": ["Discrete(n)            integers 0..n-1", "Box(low, high, shape)  real arrays", "MultiDiscrete([a, b])  several discrete choices", "MultiBinary(n)         n on/off flags", "Dict({...})            named spaces, use MultiInputPolicy"]},
        {"re": ".", "out": ["Unknown command. Type help."], "cls": "warn"}],
    "tasks": []
}

EXAM = [
    ("In the RL loop, who produces the reward?", ["The agent", "The environment", "The optimizer", "The dataset"], 1, "The environment sends the reward and the next observation."),
    ("What does step() return in Gymnasium?", ["obs, reward, done", "obs, reward, terminated, truncated, info", "obs, info", "reward, info"], 1, "Gymnasium uses terminated and truncated instead of one done flag."),
    ("An episode ends at the 500-step limit in CartPole. Which flag is true?", ["terminated", "truncated", "neither", "both"], 1, "A time limit is truncation."),
    ("With gamma = 0.5, what is the return of [2, 2, 2]?", ["6", "3.5", "4", "1.5"], 1, "2 + 1 + 0.5 = 3.5."),
    ("Which expression is the Bellman target for Q(s, a) with reward r and next state s'?", ["r", "r + gamma * max Q(s', a')", "Q(s, a)", "gamma * r"], 1, "Reward plus the discounted best next value."),
    ("Why do agents need to explore?", ["To save memory", "Otherwise they may never find better actions", "To reduce reward", "To avoid terminal states"], 1, "Without exploring, the agent can lock onto a poor action."),
    ("In Q-learning, what does alpha control?", ["Discounting", "How far each update moves toward the target", "The number of states", "Exploration probability"], 1, "Alpha is the learning rate."),
    ("Which method learns about the greedy policy while behaving with an exploring one?", ["Q-learning", "Random search", "REINFORCE only", "Supervised learning"], 0, "That is what off-policy means."),
    ("What must a custom Gymnasium environment define?", ["Observation and action spaces, reset and step", "A loss function", "A GPU", "A replay buffer"], 0, "Those are the required parts."),
    ("Which tool validates a custom environment for SB3?", ["check_env", "evaluate_policy", "Monitor", "VecNormalize"], 0, "stable_baselines3.common.env_checker.check_env."),
    ("What two ideas stabilize DQN?", ["Dropout and batch norm", "Replay buffer and target network", "Entropy and clipping", "Wrappers and callbacks"], 1, "Replay decorrelates samples; the target network stabilizes targets."),
    ("Which algorithm cannot handle continuous actions?", ["PPO", "SAC", "DQN", "A2C"], 2, "DQN needs a discrete action set."),
    ("What does PPO's clipping limit?", ["Reward size", "How far the new policy moves from the old one", "Episode length", "Buffer size"], 1, "It limits the probability ratio."),
    ("Which call trains an SB3 model?", ["model.fit()", "model.learn(total_timesteps=...)", "model.run()", "model.train()"], 1, "learn with a timestep budget."),
    ("Why use a separate evaluation environment?", ["It is required by Python", "To measure the policy without training noise", "To save memory", "To use more CPUs"], 1, "Evaluation should be clean and repeatable."),
    ("What is reward hacking?", ["Stealing rewards", "Exploiting a loophole in the reward to score high without the real task", "Clipping rewards", "Shaping rewards with potentials"], 1, "The agent optimizes what you wrote, not what you meant."),
]


def build():
    chapters = part1.CH + part2.CH + part3.CH
    html = {"__BANDIT__": BANDIT, "__GRID__": GRID}
    for ch in chapters:
        for lab in ch["practice"]:
            if lab["type"] == "webxdc" and lab["html"] in html:
                lab["html"] = html[lab["html"]]
    return {
        "format": "lilith-course", "version": 1, "id": "rl-python-gymnasium-sb3",
        "title": "Reinforcement Learning with Python",
        "subtitle": "From the basics to Gymnasium and Stable-Baselines3",
        "author": "Lilith Learning Lab",
        "description": "A beginner-friendly course on reinforcement learning: the core ideas, tabular Q-learning, DQN and PPO, then practical work with Gymnasium environments and Stable-Baselines3. Written for the current Gymnasium (1.x) API and recent Stable-Baselines3 2.x releases; check the library docs for your installed versions.",
        "pronounce": PRONOUNCE,
        "chapters": chapters,
        "finalExam": {"title": "Final exam: Reinforcement Learning", "passMark": 70, "size": 16,
                      "questions": [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in EXAM]},
        "sandbox": SANDBOX,
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "rl.course.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=1)
    print("wrote", out)
