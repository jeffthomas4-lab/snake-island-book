#!/usr/bin/env python3
"""
Build index.html (the live snakeisland.coachjeffthomas.com book) directly from
manuscript.md, the launched text of The Old Roar. Run after any manuscript edit:

    python build_index.py

The manuscript is the single source of truth. This script parses its 85 passages
into a single-file choose-your-own-adventure engine, keeping every passage's text,
image, and navigation faithful to the printed book.
"""
import re, html, pathlib, json

ROOT = pathlib.Path(__file__).parent
SRC = (ROOT / "manuscript.md").read_text(encoding="utf-8")

# ---- maps the engine needs (book structure) -------------------------------
ARRIVAL = {110:"madison",120:"chayten",130:"carson",140:"reid",
           150:"kellen",160:"kiera",170:"ella",180:"aiden"}
BEAT_COUSIN = {510:"madison",520:"chayten",530:"carson",540:"reid",
               560:"kellen",570:"kiera",580:"ella",590:"aiden"}
EXITS = {116,126,136,146,156,166,176,186}
AIDEN_DEEP = {184,185}          # Crown-depth choices
COUSIN_LABEL = {
 "madison":"Madison — the Quiet Pool","carson":"Carson — the Coulee Plains",
 "reid":"Reid — Old Speak's Wood","chayten":"Chayten — the Driftwood Stage",
 "kellen":"Kellen — Skip-Stone Lake","kiera":"Kiera — the Painted Cliff",
 "ella":"Ella — the Bright Water Court","aiden":"Aiden — the Unicorn Meadow"}
COUSIN_ARRIVAL = {v:k for k,v in ARRIVAL.items()}

# ---- regexes ---------------------------------------------------------------
HEADER   = re.compile(r'^## Passage (\d+)\s*[—-]\s*(.*)$')
SECTION  = re.compile(r'^#{1,2}\s')
IMG      = re.compile(r'^!\[\]\(images/([\w\-]+)\.png\)\s*$')
TURN     = re.compile(r'^>\s*\*\*Turn to Passage (\d+)', re.I)
CHOICE   = re.compile(r'^>\s*\*\*If (.*?),?\s*turn to passage (\d+)\.?\s*\*\*\s*$', re.I)
EXITLINE = re.compile(r"^>\s*\*\*[\w][\w']*'s chapter ends here", re.I)
DEPTH    = re.compile(r'^>\s*\*This is .*?(SILVER|CROWN) ending', re.I)
B_PLAYED = re.compile(r'^###\s*\(if you played', re.I)
B_SKIP   = re.compile(r'^###\s*\(if you skipped', re.I)
READVER  = re.compile(r'^\*Read the version below', re.I)
READIF   = re.compile(r'^\*Read this if', re.I)

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    return t

def img_html(name, alt):
    return (f'<figure class="illus"><img src="images/{name}.webp" '
            f'alt="{html.escape(alt)}" loading="lazy"></figure>')

# ---- split manuscript into passages ---------------------------------------
passages, order, cur = {}, [], None
for line in SRC.split("\n"):
    m = HEADER.match(line)
    if m:
        cur = int(m.group(1))
        passages[cur] = {"title": m.group(2).strip(), "lines": []}
        order.append(cur)
        continue
    if SECTION.match(line):
        cur = None
        continue
    if cur is not None:
        passages[cur]["lines"].append(line)

# ---- build a scene per passage --------------------------------------------
scenes = {}
for num in order:
    P = passages[num]
    mode = "main"
    buckets = {"main": [], "played": [], "skipped": []}
    bq = []                       # pending blockquote (banner) lines
    choices, nav, depth, is_exit = [], None, None, False

    def flush_bq():
        if bq:
            buckets[mode].append('<blockquote class="banner">'
                                  + "<br>".join(inline(x) for x in bq)
                                  + "</blockquote>")
            bq.clear()

    for raw in P["lines"]:
        line = raw.rstrip()
        if not line.strip():
            flush_bq(); continue
        if line.strip() == "---":          # markdown passage separator, not content
            flush_bq(); continue
        if IMG.match(line):
            flush_bq()
            name = IMG.match(line).group(1)
            buckets[mode].append(img_html(name, P["title"]))
            continue
        if B_PLAYED.match(line):  flush_bq(); mode = "played";  continue
        if B_SKIP.match(line):    flush_bq(); mode = "skipped"; continue
        if READVER.match(line) or READIF.match(line): continue
        if EXITLINE.match(line):  is_exit = True; continue
        if is_exit:               continue          # drop cousin-list tail
        if DEPTH.match(line):     depth = DEPTH.match(line).group(1).upper(); continue
        cm = CHOICE.match(line)
        if cm:
            flush_bq()
            label = cm.group(1).strip()
            label = re.sub(r'^you\s+', '', label, flags=re.I)
            label = label[:1].upper() + label[1:]
            choices.append({"label": label, "target": int(cm.group(2))})
            continue
        tm = TURN.match(line)
        if tm:
            flush_bq(); nav = int(tm.group(1)); continue
        if num == 597 and line.startswith(">"):
            continue                                # final-choice routing handled in engine
        if line.startswith(">"):
            bq.append(re.sub(r'^>\s?', '', line)); continue
        flush_bq()
        buckets[mode].append("<p>" + inline(line) + "</p>")
    flush_bq()

    sc = {"id": num, "title": P["title"]}
    if num in BEAT_COUSIN:
        sc["beat"] = BEAT_COUSIN[num]
        sc["played"] = "".join(buckets["played"])
        sc["skipped"] = "".join(buckets["skipped"])
        sc["html"] = "".join(buckets["main"])
        sc["next"] = nav
    else:
        sc["html"] = "".join(buckets["main"])
        if choices: sc["choices"] = choices
        if nav is not None: sc["next"] = nav
    if depth: sc["depth"] = depth
    if num in EXITS: sc["exit"] = True
    if num in ARRIVAL: sc["arrival"] = ARRIVAL[num]
    if num in AIDEN_DEEP: sc["aidenDeep"] = True
    if num == 597: sc["finalChoice"] = True
    if num in (601, 602): sc["ending"] = True
    scenes[num] = sc

# manual structural overrides faithful to the print navigation
scenes[11]["next"] = "hub"          # Harbor Keeper -> pick a cousin
for n in EXITS: scenes[n]["next"] = "hub"

DATA = json.dumps(scenes, ensure_ascii=False)
HUBS = json.dumps(COUSIN_LABEL, ensure_ascii=False)
ARR  = json.dumps(COUSIN_ARRIVAL, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Old Roar, A Sun Lakes Story</title>
<style>
  :root { --paper:#faf6ed; --ink:#2b2419; --warm:#c97a3f; --water:#4a7d8c; --green:#6b8e4e; --gold:#c9a23f; --rule:rgba(43,36,25,.15); }
  * { box-sizing:border-box; margin:0; padding:0; }
  html,body { background:var(--paper); color:var(--ink); font-family:'Charter','Georgia',serif; line-height:1.7; font-size:18px; min-height:100vh; }
  .container { max-width:720px; margin:0 auto; padding:28px 24px 80px; }
  header { border-bottom:2px solid var(--ink); padding-bottom:16px; margin-bottom:24px; }
  header .title-row { display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:12px; }
  header h1 { font-size:28px; font-weight:normal; font-style:italic; letter-spacing:.5px; }
  header .sub { font-size:12px; text-transform:uppercase; letter-spacing:1.5px; color:var(--warm); margin-top:4px; }
  .controls button { background:none; border:1px solid var(--ink); color:var(--ink); padding:5px 12px; cursor:pointer; font-family:inherit; font-size:12px; border-radius:3px; margin-left:6px; }
  .controls button:hover { background:var(--ink); color:var(--paper); }
  .progress-strip { background:rgba(107,142,78,.08); border:1px dashed var(--green); padding:9px 14px; margin:0 0 24px; font-size:12px; border-radius:3px; }
  .progress-strip strong { color:var(--green); }
  .progress-strip .tag { display:inline-block; background:rgba(107,142,78,.15); padding:2px 7px; border-radius:3px; margin:0 3px 3px 0; font-size:11px; }
  .scene-meta { font-size:12px; text-transform:uppercase; letter-spacing:1.5px; color:var(--water); margin-bottom:6px; font-style:italic; }
  .scene-title { font-size:30px; font-weight:normal; margin-bottom:20px; font-style:italic; line-height:1.25; }
  .scene-text { font-size:17px; }
  .scene-text p { margin-bottom:14px; }
  .scene-text blockquote.banner { border:1.5px solid var(--ink); border-radius:5px; padding:12px 16px; margin:0 0 16px; text-align:center; font-variant:small-caps; letter-spacing:1px; font-size:15px; background:rgba(201,162,63,.08); }
  .choices { display:flex; flex-direction:column; gap:12px; margin-top:32px; padding-top:22px; border-top:1px solid var(--rule); }
  .choices button, .choices a.btn { background:var(--paper); border:1.5px solid var(--ink); padding:14px 18px; text-align:left; cursor:pointer; font-family:inherit; font-size:16px; color:var(--ink); border-radius:5px; transition:all .15s ease; line-height:1.4; text-decoration:none; display:block; width:100%; }
  .choices button:hover, .choices a.btn:hover { background:var(--ink); color:var(--paper); transform:translateX(4px); }
  .choices button .sub, .choices a.btn .sub { display:block; font-size:13px; color:var(--warm); margin-top:4px; font-style:italic; }
  .choices button:hover .sub { color:#f5c587; }
  figure.illus { margin:0 0 28px; }
  figure.illus img { width:100%; height:auto; display:block; border-radius:4px; box-shadow:0 6px 24px rgba(43,36,25,.18); }
  .hub-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
  @media (max-width:540px){ .hub-grid { grid-template-columns:1fr; } }
  .hub-grid button { font-size:15px; padding:12px 14px; }
  .hub-grid button.played { background:rgba(107,142,78,.12); border-color:var(--green); }
  .hub-grid button.played::after { content:" \\2713"; color:var(--green); }
  .dock-btn { background:var(--ink)!important; color:var(--paper)!important; border-color:var(--ink)!important; }
  .dock-btn .sub { color:#f5c587!important; }
  .small { font-size:14px; color:rgba(43,36,25,.6); font-style:italic; margin-top:10px; }
  .endcap { text-align:center; font-style:italic; color:var(--warm); letter-spacing:3px; margin:30px 0 10px; font-size:18px; }
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="title-row">
      <div>
        <h1>The Old Roar</h1>
        <div class="sub">A Sun Lakes Story &middot; For the eight cousins</div>
      </div>
      <div class="controls"><button onclick="restart()">Start over</button></div>
    </div>
  </header>
  <div id="progress"></div>
  <main id="main"></main>
</div>
<script>
const SCENES = __DATA__;
const COUSINS = __HUBS__;
const ARRIVAL = __ARR__;          // cousin -> arrival passage number
const ORDER = ["madison","carson","reid","chayten","kellen","kiera","ella","aiden"];

let state;
function fresh(){ return { current:"cover", visited:[], played:{}, aidenCrown:false }; }
function save(){ try{ localStorage.setItem("old-roar", JSON.stringify(state)); }catch(e){} }
function load(){ try{ const s=localStorage.getItem("old-roar"); state = s?JSON.parse(s):fresh(); }catch(e){ state=fresh(); } if(!state.played) state.played={}; }
function restart(){ state=fresh(); save(); render(); }

function go(t){
  state.current = t;
  const n = parseInt(t,10);
  if(SCENES[n] && SCENES[n].arrival){ state.played[SCENES[n].arrival]=true; }
  if(SCENES[n] && SCENES[n].aidenDeep){ state.aidenCrown=true; }
  if(!state.visited.includes(t)) state.visited.push(t);
  save(); window.scrollTo(0,0); render();
}

function playedCount(){ return ORDER.filter(c=>state.played[c]).length; }

function renderProgress(){
  if(state.current==="cover") return "";
  const pc = playedCount();
  let h = '<div class="progress-strip"><strong>Cousins visited:</strong> '+pc+' of 8 ';
  h += ORDER.filter(c=>state.played[c]).map(c=>'<span class="tag">'+c.charAt(0).toUpperCase()+c.slice(1)+'</span>').join('');
  h += '</div>';
  return h;
}

function btn(target,label,sub,cls){
  return '<button class="'+(cls||'')+'" onclick="go(\\''+target+'\\')">'+label+(sub?'<span class="sub">'+sub+'</span>':'')+'</button>';
}

function renderCover(){
  return '<figure class="illus"><img src="images/cover.webp" alt="The Old Roar, book cover"></figure>'
    + '<div class="scene-text">'
    + '<p>Eight cousins. One cove. A man with clipboards who wants to drain the lake and build a data center on the dry bed.</p>'
    + '<p>Read the opening straight through. Then follow the cousins into <em>The Old Roar</em>, the world that lives under the lake, in any order you like. When you have walked as many of their paths as you want, everyone meets again at the dock.</p>'
    + '</div>'
    + '<div class="choices">'
    + btn("1","Begin reading \\u25B8","Passage 1 \\u2014 the synchronized jump")
    + '</div>';
}

function renderHub(){
  const pc = playedCount();
  let h = '<figure class="illus"><img src="images/table.webp" alt="The eight cousins gathered"></figure>'
    + '<div class="scene-text">'
    + '<p>The Harbor Keeper steps aside. Eight paths lead away from the meadow, one shaped for each cousin.</p>'
    + '<p>Follow any cousin into their region. Read them in any order, as many as you like. When you are ready, bring everyone home to the dock for the showdown.</p>'
    + '</div><div class="choices"><div class="hub-grid">';
  ORDER.forEach(c=>{
    const pl = state.played[c] ? 'played' : '';
    h += btn(String(ARRIVAL[c]), COUSINS[c], '', 'hub-grid-btn '+pl).replace('class="hub-grid-btn '+pl+'"','class="'+pl+'"');
  });
  h += '</div>';
  const sub = pc<8 ? 'Best after you have visited everyone, but you can go whenever you like.' : 'All eight visited. Go finish it.';
  h += btn("400","Bring everyone home to the dock \\u25B8", sub, "dock-btn");
  h += '</div>';
  return h;
}

function sceneBody(sc){
  let body = sc.html || "";
  if(sc.beat){
    body += state.played[sc.beat] ? sc.played : sc.skipped;
  }
  return body;
}

function render(){
  const m = document.getElementById("main");
  document.getElementById("progress").innerHTML = renderProgress();

  if(state.current==="cover"){ m.innerHTML = renderCover(); return; }
  if(state.current==="hub"){ m.innerHTML = renderHub(); return; }

  const num = parseInt(state.current,10);
  const sc = SCENES[num];
  if(!sc){ m.innerHTML = "<p>Lost the path. <button onclick=\\"restart()\\">Start over</button></p>"; return; }

  let h = '<div class="scene-meta">Passage '+num+'</div>';
  h += '<div class="scene-title">'+sc.title+'</div>';
  h += '<div class="scene-text">'+sceneBody(sc)+'</div>';
  h += '<div class="choices">';

  if(sc.choices){
    sc.choices.forEach(c=> h += btn(String(c.target), c.label));
  } else if(sc.finalChoice){
    const crown = state.played["aiden"] && state.aidenCrown;
    h += btn(crown?"598":"599","Turn the page \\u25B8","See how it ends");
  } else if(sc.ending){
    h += '</div><div class="endcap">\\u2726 The End \\u2726</div><div class="choices">';
    h += btn("cover","Read it again \\u25B8");
  } else if(sc.exit){
    h += btn("hub","Back to the meadow \\u25B8","Pick another cousin, or head to the dock");
  } else if(sc.next!==undefined && sc.next!==null){
    h += btn(String(sc.next),"Continue \\u25B8");
  }
  h += '</div>';
  m.innerHTML = h;
}

load(); render();
</script>
</body>
</html>
"""

HTML = (HTML.replace("__DATA__", DATA).replace("__HUBS__", HUBS).replace("__ARR__", ARR))
(ROOT / "index.html").write_text(HTML, encoding="utf-8")

# ---- report ----------------------------------------------------------------
print(f"passages parsed : {len(scenes)}")
beats = [n for n in scenes if 'beat' in scenes[n]]
print(f"showdown beats  : {len(beats)} {beats}")
# integrity: every referenced target exists
targets=set()
for n,sc in scenes.items():
    if sc.get('next') and sc['next']!='hub': targets.add(int(sc['next']))
    for c in sc.get('choices',[]): targets.add(int(c['target']))
    if sc.get('beat') and sc.get('next'): targets.add(int(sc['next']))
missing=[t for t in targets if t not in scenes]
print(f"missing targets : {missing}")
dead=[n for n,sc in scenes.items() if not any(k in sc for k in ('next','choices','finalChoice','ending','exit'))]
print(f"dead-ends       : {dead}")
print(f"index.html bytes: {(ROOT/'index.html').stat().st_size}")
