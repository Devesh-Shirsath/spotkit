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

# the marquee runs two copies of the set so the loop is seamless
def _card(i, t, doc, dup):
    return (f'<div class="card" data-i="{i}" data-t="{t}"'
            f'{" aria-hidden=true" if dup else ""}>'
            + doc.replace('-' + f'c{i}' + '"', '"') + '</div>')

cards = ''
for pass_ in (0, 1):
    for i, (t, sub, (uid, label, doc)) in enumerate(items):
        tag = f'{uid}-m{pass_}'
        d = doc.replace('-' + uid + '"', '-' + tag + '"').replace('-' + uid + ')', '-' + tag + ')')
        cards += (f'<div class="card" data-i="{i}"'
                  f'{" aria-hidden=true" if pass_ else ""}>{d}</div>')

# one illustration per payoff claim, borrowed from the main set
core_by_uid = {u: (l, d) for u, l, d in [fn() for fn in core.SET]}
def _mini(uid, tag):
    l, d = core_by_uid[uid]
    return d.replace('-' + uid + '"', '-' + tag + '"').replace('-' + uid + ')', '-' + tag + ')')

GETS = [
    ('Real SVG',
     'Edit it, paste it into Figma, review it in a pull request. Not a PNG you have to ask someone to change.',
     _mini('connectors', 'g1')),
    ('Light and dark',
     'Twelve CSS variables. One file serves both themes, and retheming the whole set is a three-value edit.',
     '<div class="duo"><div data-theme="light">' + _mini('categories', 'g2a') +
     '</div><div data-theme="dark">' + _mini('categories', 'g2b') + '</div></div>'),
    ('Distinct, not filler',
     'Twelve layouts picked by meaning, with a budget on reuse, so a set never reads as one drawing repeated.',
     _mini('contributors', 'g3')),
    ('Free',
     'MIT licensed. No signup, no API key, no per-image cost. It runs on the Claude you already pay for.',
     _mini('gateway', 'g4')),
]
gets = ''.join(
    f'<div class="get"><h3>{h}</h3><p>{p}</p><div class="get-illo">{ill}</div></div>'
    for h, p, ill in GETS)

LINKS = [('globe-simple', 'Portfolio', AUTHOR_URL), ('linkedin-logo', 'LinkedIn', LINKEDIN),
         ('github-logo', 'GitHub', GITHUB), ('instagram-logo', 'Instagram', INSTAGRAM)]
links = ''.join(
    f'<a href="{u}">{core.icon(ic, 0, 0, 16, "currentColor").replace("<g ", chr(60) + "svg viewBox=" + chr(34) + "0 0 16 16" + chr(34) + " width=" + chr(34) + "16" + chr(34) + " height=" + chr(34) + "16" + chr(34) + " aria-hidden=" + chr(34) + "true" + chr(34) + "><g ").replace("</g>", "</g></svg>")}<span>{n}</span></a>'
    for ic, n, u in LINKS)

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
header {{ padding: 96px 0 0; max-width: 780px; margin: 0 auto; text-align: center; }}
h1 {{
  font-size: clamp(31px, 4.3vw, 45px); line-height: 1.14; letter-spacing: -.026em;
  font-weight: 620; margin: 0 0 20px; text-wrap: balance;
}}
h1 em {{ font-style: normal; color: var(--ink-soft); }}
.lede {{ font-size: 17px; color: var(--ink-soft); margin: 0 auto 28px; max-width: 560px; }}
.cta-row {{ display:flex; align-items:center; justify-content:center; gap:14px; flex-wrap:wrap; }}
.cta {{
  display:inline-flex; align-items:center; gap:9px; background: var(--ink); color: var(--page);
  text-decoration:none; padding: 12px 20px; border-radius: 999px; font-size:14.5px; font-weight:560;
  transition: transform .18s ease, opacity .18s ease;
}}
.cta:hover {{ transform: translateY(-1px); opacity:.9; }}
.meta {{ font-size:13.5px; color:var(--ink-soft); }}

/* ---------- moving reel ---------- */
.reel {{ margin: 54px 0 0; overflow: hidden; }}
.track {{
  display:flex; gap: 26px; width: max-content; padding: 8px 0;
  animation: drift 64s linear infinite;
}}
.track:hover {{ animation-play-state: paused; }}
@keyframes drift {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
.card {{
  width: 186px; flex: none; border-radius: 13px; padding: 8px;
  background: var(--il-panel); border: 1px solid var(--line);
  opacity: .5; transform: scale(.92);
  transition: opacity .5s ease, transform .5s ease;
}}
.card.active {{ opacity: 1; transform: scale(1.08); border-color: var(--ink-soft); }}
.card svg {{ width:100%; height:auto; display:block; }}
.prompt {{
  text-align:center; margin: 26px 0 0; font-size: 19px; letter-spacing:-.012em;
  color: var(--ink); min-height: 1.6em;
}}
.prompt span::before {{ content:'“'; color:var(--ink-soft); }}
.prompt span::after  {{ content:'”'; color:var(--ink-soft); }}

/* ---------- argument ---------- */
.eyebrow {{
  font-size:11px; letter-spacing:.1em; text-transform:uppercase; color:var(--ink-soft);
  font-weight:640; margin:0 0 26px; padding-top:22px; border-top:1px solid var(--line);
}}
.why {{ margin: 96px 0 0; }}
.why-grid {{ display:grid; grid-template-columns: 0.85fr 1.15fr; gap:52px; align-items:start; }}
.why-grid h2 {{
  font-size: clamp(22px, 2.4vw, 28px); line-height:1.2; letter-spacing:-.02em;
  font-weight:620; margin:0; text-wrap: balance;
}}
.why-copy p {{ margin:0 0 15px; color:var(--ink-soft); font-size:15.5px; }}
.why-copy p:last-child {{ margin:0; }}
.why-copy em {{ font-style:normal; color:var(--ink); }}
.sheets {{ display:grid; gap:14px; }}
.sheets img {{
  width:100%; height:auto; display:block; border-radius:11px; border:1px solid var(--line);
}}
.sheet-note {{ margin:14px 0 0; font-size:13.5px; color:var(--ink-soft); }}

/* ---------- payoff ---------- */
.gets {{ margin: 92px 0 0; }}
.get-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:40px 46px; }}
.get-illo {{
  margin-top:16px; padding:14px; border:1px solid var(--line); border-radius:12px;
  background:var(--il-panel);
}}
.get-illo svg {{ width:100%; height:auto; display:block; max-width:158px; margin:0 auto; }}
.duo {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.duo > div {{ border-radius:8px; padding:6px; background:var(--il-canvas); }}
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
.links {{ display:flex; gap:20px; flex-wrap:wrap; font-size:14px; }}
.links a {{ color:var(--ink-soft); border:0; display:inline-flex; align-items:center; gap:7px; }}
.links a svg {{ flex:none; opacity:.85; }}
.links a:hover {{ color:var(--ink); }}
.fine {{ margin-top:22px; font-size:12.5px; color:var(--ink-soft); opacity:.8; }}

@media (max-width: 900px) {{
  .why-grid {{ grid-template-columns:1fr; gap:24px; }}
}}
@media (max-width: 700px) {{
  header {{ padding-top:60px; }}
  .get-grid {{ grid-template-columns:1fr; gap:34px; }}
  .card {{ width:150px; }}
  .prompt {{ font-size:16.5px; }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation-duration:.001ms !important; transition-duration:.001ms !important; }}
  .track {{ animation:none; transform:none; }}
  .reel {{ overflow-x:auto; }}
  .card {{ opacity:1; transform:none; }}
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
  everything else you've made.</p>
  <div class="cta-row">
    <a class="cta" href="{REPO}">Get it on GitHub →</a>
    <span class="meta">MIT · runs on the Claude you already have</span>
  </div>
</header>
</div>

<section class="reel" aria-label="Example illustrations">
  <div class="track" id="track">{cards}</div>
  <p class="prompt" id="prompt"><span id="ptxt"></span></p>
</section>

<div class="wrap">

<section class="why">
  <p class="eyebrow">The hard part</p>
  <div class="why-grid">
    <h2>Drawing one is easy.<br>Drawing twenty that match is the job.</h2>
    <div class="why-copy">
      <p>By the tenth, the corner radius has drifted and the set reads as
      assembled rather than designed.</p>
      <p>Spotkit is a system, not a generator — twelve layouts chosen by what a
      feature <em>means</em>, one stroke width and one colour throughout.</p>
    </div>
  </div>
  <div class="sheets">
    <img src="sheet-light.svg" alt="Twelve Spotkit illustrations in light mode" loading="lazy" width="1116" height="376">
    <img src="sheet-dark.svg" alt="The same twelve illustrations in dark mode" loading="lazy" width="1116" height="376">
  </div>
  <p class="sheet-note">Twelve features, twelve layouts, one set of rules — and the
  same twelve files in both themes.</p>
</section>

<section class="gets">
  <p class="eyebrow">What you get</p>
  <div class="get-grid">{gets}</div>
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
  <div class="links">{links}</div>
  <p class="fine">MIT licensed. Icons by Phosphor.</p>
</footer>

</div>
<script>
(function () {{
  var P = [
      {prompts_js}
  ];

  // The caption follows whichever card is nearest the middle of the screen,
  // rather than a timer — so it can never drift out of step with the marquee.
  var track  = document.getElementById('track');
  var ptxt   = document.getElementById('ptxt');
  var cards  = [].slice.call(track.querySelectorAll('.card'));
  var last   = -1, queued = false;

  function sync() {{
    queued = false;
    var mid = innerWidth / 2, best = null, bestD = Infinity;
    for (var i = 0; i < cards.length; i++) {{
      var r = cards[i].getBoundingClientRect();
      if (r.right < -200 || r.left > innerWidth + 200) continue;
      var d = Math.abs(r.left + r.width / 2 - mid);
      if (d < bestD) {{ bestD = d; best = cards[i]; }}
    }}
    if (!best) return;
    cards.forEach(function (c) {{ c.classList.toggle('active', c === best); }});
    var n = +best.dataset.i;
    if (n !== last) {{ last = n; ptxt.textContent = P[n].t + ' — ' + P[n].s; }}
  }}
  function loop() {{ if (!queued) {{ queued = true; requestAnimationFrame(sync); }} requestAnimationFrame(loop); }}
  requestAnimationFrame(loop);
  addEventListener('resize', sync);

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
