#!/usr/bin/env python3
"""Generates site/index.html — a single static file, no framework, no build step.

Illustrations are inlined rather than linked because CSS custom properties do
not cross into <img>, and the light/dark toggle is the point.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import illos
import build as core

REPO = 'https://github.com/Devesh-Shirsath/spotkit'
SITE = 'https://spotkit.vercel.app'
AUTHOR = 'Devesh Shirsath'
AUTHOR_URL = 'https://deveshshirsath.com'
LINKEDIN = 'https://www.linkedin.com/in/devesh-shirsath-644625172/'
GITHUB = 'https://github.com/Devesh-Shirsath'
INSTAGRAM = 'https://www.instagram.com/devesh.vs/'

items = [(title, sub, fn()) for title, sub, fn in illos.PROMPTS]
tokens = open(os.path.join(os.path.dirname(__file__), '..', 'assets', 'illustration.css')).read()
tokens = tokens[tokens.index(':root,'):]

panes = ''.join(
    f'<div class="illo" data-i="{i}"{"" if i == 0 else " aria-hidden=true"}>{doc}</div>'
    for i, (t, s, (uid, label, doc)) in enumerate(items))

chips = ''.join(
    f'<button class="chip{" on" if i == 0 else ""}" data-i="{i}" type="button">{t}</button>'
    for i, (t, s, _) in enumerate(items))

sheet = ''.join(
    '<div class="cell">' +
    doc.replace('-' + uid + '"', '-' + uid + '-s"').replace('-' + uid + ')', '-' + uid + '-s)') +
    '</div>'
    for uid, label, doc in [fn() for fn in core.SET])

prompts_js = ',\n      '.join(
    f'{{t:"{t}", s:"{s}"}}' for t, s, _ in items)

JSONLD = f'''{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Spotkit",
  "alternateName": "Spotkit illustration skill",
  "applicationCategory": "DesignApplication",
  "operatingSystem": "Any",
  "url": "{SITE}",
  "codeRepository": "{REPO}",
  "license": "https://opensource.org/licenses/MIT",
  "description": "Spotkit is a Claude Code skill that turns a feature description into a minimal, abstract product illustration, written as deterministic SVG rather than generated as an image.",
  "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
  "author": {{
    "@type": "Person",
    "name": "{AUTHOR}",
    "url": "{AUTHOR_URL}",
    "jobTitle": "Product Designer",
    "sameAs": ["{LINKEDIN}", "{GITHUB}", "{INSTAGRAM}"]
  }},
  "creator": {{
    "@type": "Person",
    "name": "{AUTHOR}",
    "url": "{AUTHOR_URL}"
  }}
}}'''

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spotkit — product illustrations from a sentence</title>
<meta name="description" content="Spotkit is a Claude Code skill that turns a feature description into a minimal, abstract SVG product illustration — one that belongs to the same family as every other illustration in your product.">
<meta name="author" content="{AUTHOR}">
<link rel="canonical" href="{SITE}">
<meta property="og:type" content="website">
<meta property="og:title" content="Spotkit — product illustrations from a sentence">
<meta property="og:description" content="Describe a feature. Get an SVG illustration that belongs to the same family as everything else you have made.">
<meta property="og:url" content="{SITE}">
<meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:creator" content="@deveshvs">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2224%22 fill=%22%23EDEAE6%22/><rect x=%2224%22 y=%2230%22 width=%2252%22 height=%2240%22 rx=%228%22 fill=%22none%22 stroke=%22%2335322D%22 stroke-width=%225%22/></svg>">
<script type="application/ld+json">{JSONLD}</script>
<style>
{tokens}

*,*::before,*::after {{ box-sizing: border-box; }}
:root {{
  --ink:      var(--il-stroke);
  --ink-soft: var(--il-stroke-soft);
  --page:     var(--il-canvas);
  --card:     var(--il-surface);
  --line:     var(--il-line);
  --radius:   14px;
  --max:      1120px;
}}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0; background: var(--page); color: var(--ink);
  font: 400 16px/1.6 ui-sans-serif, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  transition: background .35s ease, color .35s ease;
}}
.wrap {{ max-width: var(--max); margin: 0 auto; padding: 0 28px; }}

/* ---------- nav ---------- */
nav {{ display:flex; align-items:center; justify-content:space-between; padding:26px 0 0; }}
.brand {{ display:flex; align-items:center; gap:9px; font-weight:640; letter-spacing:-.01em; font-size:16px; }}
.brand i {{ width:15px; height:12px; border:1.4px solid var(--ink); border-radius:3.5px; display:block; }}
.navr {{ display:flex; align-items:center; gap:8px; }}
.ghost {{
  appearance:none; border:1px solid var(--line); background:transparent; color:var(--ink-soft);
  border-radius:999px; padding:7px 13px; font:inherit; font-size:13px; cursor:pointer;
  transition:color .2s, border-color .2s;
}}
.ghost:hover {{ color:var(--ink); border-color:var(--ink-soft); }}

/* ---------- hero ---------- */
header {{ padding: 90px 0 20px; max-width: 730px; }}
h1 {{
  font-size: clamp(31px, 4.3vw, 45px); line-height: 1.12; letter-spacing: -.026em;
  font-weight: 620; margin: 0 0 22px; text-wrap: balance;
}}
h1 em {{ font-style: normal; color: var(--ink-soft); }}
.lede {{ font-size: 17.5px; color: var(--ink-soft); margin: 0 0 30px; max-width: 540px; }}
.cta-row {{ display:flex; align-items:center; gap:14px; flex-wrap:wrap; }}
.cta {{
  display:inline-flex; align-items:center; gap:9px; background: var(--ink); color: var(--page);
  text-decoration:none; padding: 12px 20px; border-radius: 999px; font-size:14.5px; font-weight:560;
  transition: transform .18s ease, opacity .18s ease;
}}
.cta:hover {{ transform: translateY(-1px); opacity:.9; }}
.meta {{ font-size:13.5px; color:var(--ink-soft); }}

/* ---------- demo ---------- */
.demo {{ margin: 54px 0 0; }}
.stage {{
  display:grid; grid-template-columns: 1fr 390px; gap: 0;
  border:1px solid var(--line); border-radius: var(--radius); overflow:hidden;
  background: var(--card);
}}
.side {{ padding: 34px 36px; display:flex; flex-direction:column; justify-content:center; min-height: 320px; }}
.side + .side {{ border-left:1px solid var(--line); background: var(--il-panel); padding: 26px; }}
.tag {{
  font-size:11px; letter-spacing:.09em; text-transform:uppercase; color:var(--ink-soft);
  margin:0 0 14px; font-weight:600;
}}
.typed {{ font-size: 24px; line-height:1.4; letter-spacing:-.012em; margin:0; min-height: 2.7em; }}
.typed .sub {{ display:block; font-size:15px; color:var(--ink-soft); margin-top:7px; letter-spacing:0; }}
.caret {{ display:inline-block; width:2px; height:1em; background:var(--il-accent); vertical-align:-2px; margin-left:2px; animation:blink 1s steps(1) infinite; }}
@keyframes blink {{ 50% {{ opacity:0; }} }}
.illo {{ position:absolute; inset:0; display:grid; place-items:center; opacity:0; transition:opacity .45s ease; pointer-events:none; }}
.illo.on {{ opacity:1; }}
.illo svg {{ width:100%; height:auto; max-width:300px; display:block; }}
.frame {{ position:relative; width:100%; aspect-ratio:1/1; }}

.chips {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:26px; }}
.chip {{
  appearance:none; border:1px solid var(--line); background:transparent; color:var(--ink-soft);
  border-radius:999px; padding:7px 14px; font:inherit; font-size:13px; cursor:pointer;
  transition: all .2s ease;
}}
.chip:hover {{ color:var(--ink); border-color:var(--ink-soft); }}
.chip.on {{ background:var(--ink); border-color:var(--ink); color:var(--page); }}

/* ---------- argument ---------- */
.eyebrow {{
  font-size:11px; letter-spacing:.1em; text-transform:uppercase; color:var(--ink-soft);
  font-weight:640; margin:0 0 26px; padding-top:22px; border-top:1px solid var(--line);
}}
.why {{ margin: 92px 0 0; }}
.why-grid {{ display:grid; grid-template-columns: 1fr 1fr; gap:56px; align-items:start; }}
.why-grid h2 {{
  font-size: clamp(22px, 2.4vw, 28px); line-height:1.2; letter-spacing:-.02em;
  font-weight:620; margin:0; text-wrap: balance;
}}
.why-copy p {{ margin:0 0 15px; color:var(--ink-soft); font-size:15.5px; }}
.why-copy p:last-child {{ margin:0; }}
.why-copy em {{ font-style:normal; color:var(--ink); }}
.sheet {{
  display:grid; grid-template-columns:repeat(6,1fr); gap:10px; margin:46px 0 0;
  padding:20px 16px; border:1px solid var(--line); border-radius:var(--radius);
  background:var(--il-panel);
}}
.cell svg {{ width:100%; height:auto; display:block; }}
.sheet-note {{ margin:14px 0 0; font-size:13.5px; color:var(--ink-soft); }}

/* ---------- payoff ---------- */
.gets {{ margin: 92px 0 0; }}
.get-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:34px; }}
.get h3 {{ font-size:16px; font-weight:620; letter-spacing:-.012em; margin:0 0 8px; }}
.get p {{ margin:0; color:var(--ink-soft); font-size:14.5px; }}

/* ---------- install ---------- */
.install {{ margin: 92px 0 0; }}
.install h2, .foot h2 {{ font-size:19px; font-weight:620; letter-spacing:-.015em; margin:0 0 8px; }}
.install p {{ color:var(--ink-soft); margin:0 0 18px; font-size:15px; }}
.code {{
  display:flex; align-items:center; justify-content:space-between; gap:16px;
  border:1px solid var(--line); border-radius:11px; background:var(--card);
  padding:15px 16px; font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:13px;
  overflow-x:auto;
}}
.code span {{ white-space:nowrap; }}
.copy {{
  appearance:none; border:1px solid var(--line); background:transparent; color:var(--ink-soft);
  border-radius:7px; padding:5px 11px; font:inherit; font-size:12px; cursor:pointer; flex:none;
}}
.copy:hover {{ color:var(--ink); }}

/* ---------- footer ---------- */
.foot {{ margin: 92px 0 0; padding: 0 0 70px; }}
.foot p {{ color:var(--ink-soft); font-size:14.5px; margin:0 0 12px; max-width:520px; }}
.foot a {{ color:var(--ink); text-decoration:none; border-bottom:1px solid var(--line); }}
.foot a:hover {{ border-color:var(--ink-soft); }}
.links {{ display:flex; gap:18px; flex-wrap:wrap; font-size:14px; }}
.links a {{ color:var(--ink-soft); border:0; }}
.links a:hover {{ color:var(--ink); }}
.fine {{ margin-top:22px; font-size:12.5px; color:var(--ink-soft); opacity:.8; }}

@media (max-width: 900px) {{
  .why-grid {{ grid-template-columns:1fr; gap:22px; }}
  .get-grid {{ grid-template-columns:repeat(2,1fr); gap:28px; }}
  .sheet {{ grid-template-columns:repeat(4,1fr); }}
}}
@media (max-width: 760px) {{
  header {{ padding-top:58px; }}
  .sheet {{ grid-template-columns:repeat(3,1fr); gap:10px; padding:18px 14px; }}
  .get-grid {{ grid-template-columns:1fr; gap:24px; }}
  .stage {{ grid-template-columns: 1fr; }}
  .side + .side {{ border-left:0; border-top:1px solid var(--line); }}
  .side {{ min-height:auto; }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation-duration:.001ms !important; transition-duration:.001ms !important; }}
}}
</style>
</head>
<body>
<div class="wrap">

<nav>
  <div class="brand"><i></i> spotkit</div>
  <div class="navr">
    <button class="ghost" id="theme" type="button" aria-label="Switch theme">Dark</button>
    <a class="ghost" href="{REPO}" style="text-decoration:none">GitHub</a>
  </div>
</nav>

<header>
  <h1>Every feature wants an illustration.<br><em>Drawing twenty isn't your job.</em></h1>
  <p class="lede">Spotkit is an illustration system that runs inside Claude Code.
  Describe a feature in a sentence and get a clean, distinct SVG that belongs with
  everything else you've made — light and dark from one file, yours to edit, free.</p>
  <div class="cta-row">
    <a class="cta" href="{REPO}">Get it on GitHub →</a>
    <span class="meta">MIT · runs on the Claude you already have</span>
  </div>
</header>

<section class="demo">
  <div class="stage">
    <div class="side">
      <p class="tag">You write</p>
      <p class="typed" id="typed"><span id="tt"></span><span class="caret"></span><span class="sub" id="ts"></span></p>
      <div class="chips" id="chips">{chips}</div>
    </div>
    <div class="side">
      <p class="tag">Spotkit draws</p>
      <div class="frame">{panes}</div>
    </div>
  </div>
</section>

<section class="why">
  <p class="eyebrow">The hard part</p>
  <div class="why-grid">
    <h2>Drawing one is easy.<br>Drawing twenty that match is the job.</h2>
    <div class="why-copy">
      <p>You draw the first three and they look good. By the tenth the corner
      radius has drifted, the stroke weight is slightly off, and the set reads as
      assembled rather than designed. That is the part that quietly fails, and it
      is why most products end up with three good illustrations and stock art
      everywhere else.</p>
      <p>Spotkit is a system rather than a generator. Twelve layouts chosen by
      what a feature <em>means</em>, one stroke width and one colour across every
      file, and guards that refuse the geometry mistakes you only notice once
      someone sees a single illustration at full size.</p>
    </div>
  </div>
  <div class="sheet">{sheet}</div>
  <p class="sheet-note">Twelve features, twelve different layouts, one set of rules.
  Same twelve files in both themes.</p>
</section>

<section class="gets">
  <p class="eyebrow">What you get</p>
  <div class="get-grid">
    <div class="get">
      <h3>Real SVG</h3>
      <p>Edit it, paste it into Figma, review it in a pull request. Not a PNG you
      have to ask someone to change.</p>
    </div>
    <div class="get">
      <h3>Light and dark</h3>
      <p>Twelve CSS variables. One file serves both themes, and retheming the
      whole set is a three-value edit.</p>
    </div>
    <div class="get">
      <h3>Distinct, not filler</h3>
      <p>Twelve layouts picked by meaning, with a budget on reuse, so a set never
      reads as one drawing repeated.</p>
    </div>
    <div class="get">
      <h3>Free</h3>
      <p>MIT licensed. No signup, no API key, no per-image cost. It runs on the
      Claude you already pay for.</p>
    </div>
  </div>
</section>

<section class="install">
  <p class="eyebrow">Install</p>
  <h2>Two lines and it's yours</h2>
  <p>Drop it into your skills folder and ask. Python 3 only, and only if you want to regenerate.</p>
  <div class="code">
    <span id="cmd">git clone {REPO}.git ~/.claude/skills/spotkit</span>
    <button class="copy" id="copy" type="button">Copy</button>
  </div>
</section>

<footer class="foot">
  <p class="eyebrow">Who made this</p>
  <p>Spotkit was built by <a href="{AUTHOR_URL}">{AUTHOR}</a>, a product designer
  working on developer tools and API documentation.</p>
  <div class="links">
    <a href="{AUTHOR_URL}">Portfolio</a>
    <a href="{LINKEDIN}">LinkedIn</a>
    <a href="{GITHUB}">GitHub</a>
    <a href="{INSTAGRAM}">Instagram</a>
  </div>
  <p class="fine">MIT licensed. Icons by Phosphor.</p>
</footer>

</div>
<script>
(function () {{
  var P = [
      {prompts_js}
  ];
  var tt = document.getElementById('tt'), ts = document.getElementById('ts');
  var illos = [].slice.call(document.querySelectorAll('.illo'));
  var chips = [].slice.call(document.querySelectorAll('.chip'));
  var i = -1, timer = null, typer = null, auto = true;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function show(n) {{
    clearTimeout(timer); clearInterval(typer);
    i = n;
    illos.forEach(function (el, k) {{
      el.classList.toggle('on', k === n);
      el.setAttribute('aria-hidden', k === n ? 'false' : 'true');
    }});
    chips.forEach(function (c, k) {{ c.classList.toggle('on', k === n); }});
    ts.textContent = '';
    var full = P[n].t, j = 0;
    if (reduce) {{ tt.textContent = full; ts.textContent = P[n].s; queue(); return; }}
    tt.textContent = '';
    typer = setInterval(function () {{
      tt.textContent = full.slice(0, ++j);
      if (j >= full.length) {{ clearInterval(typer); ts.textContent = P[n].s; queue(); }}
    }}, 42);
  }}
  function queue() {{ if (auto) timer = setTimeout(function () {{ show((i + 1) % P.length); }}, 3200); }}

  chips.forEach(function (c) {{
    c.addEventListener('click', function () {{ auto = false; show(+c.dataset.i); }});
  }});
  show(0);

  // theme
  var btn = document.getElementById('theme');
  var root = document.documentElement;
  var dark = matchMedia('(prefers-color-scheme: dark)').matches;
  function paint() {{
    root.setAttribute('data-theme', dark ? 'dark' : 'light');
    btn.textContent = dark ? 'Light' : 'Dark';
  }}
  btn.addEventListener('click', function () {{ dark = !dark; paint(); }});
  paint();

  // copy
  var copy = document.getElementById('copy');
  copy.addEventListener('click', function () {{
    navigator.clipboard.writeText(document.getElementById('cmd').textContent).then(function () {{
      copy.textContent = 'Copied'; setTimeout(function () {{ copy.textContent = 'Copy'; }}, 1600);
    }});
  }});
}})();
</script>
</body>
</html>
'''
open(os.path.join(os.path.dirname(__file__), 'index.html'), 'w').write(html)
print('site/index.html —', len(html) // 1024, 'KB')
