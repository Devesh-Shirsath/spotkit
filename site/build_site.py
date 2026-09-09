#!/usr/bin/env python3
"""Generates site/index.html — a single static file, no framework, no build step.

Illustrations are inlined rather than linked because CSS custom properties do
not cross into <img>, and the light/dark toggle is the point.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import illos

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
  --max:      1080px;
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
header {{ padding: 86px 0 20px; max-width: 660px; }}
h1 {{
  font-size: clamp(34px, 5.2vw, 52px); line-height: 1.08; letter-spacing: -.028em;
  font-weight: 620; margin: 0 0 20px;
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

/* ---------- install ---------- */
.install {{ margin: 66px 0 0; }}
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
.foot {{ margin: 76px 0 0; border-top:1px solid var(--line); padding: 30px 0 60px; }}
.foot p {{ color:var(--ink-soft); font-size:14.5px; margin:0 0 12px; max-width:520px; }}
.foot a {{ color:var(--ink); text-decoration:none; border-bottom:1px solid var(--line); }}
.foot a:hover {{ border-color:var(--ink-soft); }}
.links {{ display:flex; gap:18px; flex-wrap:wrap; font-size:14px; }}
.links a {{ color:var(--ink-soft); border:0; }}
.links a:hover {{ color:var(--ink); }}
.fine {{ margin-top:22px; font-size:12.5px; color:var(--ink-soft); opacity:.8; }}

@media (max-width: 760px) {{
  header {{ padding-top:58px; }}
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
  <h1>Spot illustrations for<br>your whole product. <em>Not one at a time.</em></h1>
  <p class="lede">Spotkit is a Claude Code skill. Describe a feature in a sentence
  and get an SVG illustration that belongs to the same family as every other one
  you have made — same geometry, same stroke, light and dark from one file.</p>
  <div class="cta-row">
    <a class="cta" href="{REPO}">Get it on GitHub →</a>
    <span class="meta">MIT · no dependencies</span>
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

<section class="install">
  <h2>Install</h2>
  <p>Drop it into your skills folder and ask. Python 3 only, and only if you want to regenerate.</p>
  <div class="code">
    <span id="cmd">git clone {REPO}.git ~/.claude/skills/spotkit</span>
    <button class="copy" id="copy" type="button">Copy</button>
  </div>
</section>

<footer class="foot">
  <h2>Who made this</h2>
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
