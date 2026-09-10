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

REPEATS = 5
cards = ''
for pass_ in range(REPEATS):
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
     '<div class="split"><span data-theme="light">' + _mini('categories', 'g2a') +
     '</span><span class="half" data-theme="dark">' + _mini('categories', 'g2b') + '</span></div>'),
    ('Distinct, not filler',
     'Twelve layouts picked by meaning, with a budget on reuse, so a set never reads as one drawing repeated.',
     _mini('contributors', 'g3')),
    ('Free',
     'No signup, no API key, no per-image cost. It runs on the Claude you already pay for.',
     _mini('gateway', 'g4')),
]
gets = ''.join(
    f'<div class="get"><div class="orb">{ill}</div><h3>{h}</h3><p>{p}</p></div>'
    for h, p, ill in GETS)

LINKS = [('globe-simple', 'Portfolio', AUTHOR_URL), ('linkedin-logo', 'LinkedIn', LINKEDIN),
         ('github-logo', 'GitHub', GITHUB), ('instagram-logo', 'Instagram', INSTAGRAM)]
def _btn(ic, n, u):
    g = core.icon(ic, 0, 0, 18, 'currentColor')
    svg = ('<svg viewBox="0 0 18 18" width="18" height="18" aria-hidden="true">'
           + g + '</svg>')
    return f'<a class="dot" href="{u}" title="{n}" aria-label="{n}">{svg}</a>'

links = ''.join(_btn(ic, n, u) for ic, n, u in LINKS)

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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Geist:wght@300..700&display=swap" rel="stylesheet">
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
  --max:      1180px;
  --serif:    "Libre Baskerville", Georgia, "Times New Roman", serif;
  --sans:     "Geist", ui-sans-serif, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}}
html {{ scroll-behavior: smooth; }}
h1, h2, h3 {{ font-family: var(--serif); font-weight: 400; letter-spacing: -.04em; }}
body {{
  margin: 0; background: var(--page); color: var(--ink);
  font: 400 16px/1.65 var(--sans);
  -webkit-font-smoothing: antialiased;
  transition: background .35s ease, color .35s ease;
}}
.wrap {{ max-width: var(--max); margin: 0 auto; padding: 0 28px; }}

/* ---------- nav ---------- */
nav {{ display:flex; align-items:center; justify-content:space-between; padding:26px 0 0; }}
.brand {{ display:flex; align-items:center; gap:9px; font-weight:600; letter-spacing:-.02em; font-size:16.5px; }}
.brand i {{ width:15px; height:12px; border:1.4px solid var(--ink); border-radius:3.5px; display:block; }}
.navr {{ display:flex; align-items:center; gap:8px; }}
.ghost {{
  appearance:none; border:1px solid var(--line); background:transparent; color:var(--ink-soft);
  border-radius:999px; padding:7px 13px; font:inherit; font-size:13px; cursor:pointer;
  transition:color .2s, border-color .2s;
}}
.ghost:hover {{ color:var(--ink); border-color:var(--ink-soft); }}

/* ---------- hero: one full fold ---------- */
.fold {{ min-height: 100svh; display:flex; flex-direction:column; }}
header {{ padding: clamp(40px, 6.5vh, 78px) 0 0; max-width: 820px; margin: 0 auto; text-align: center; }}
h1 {{
  font-family: var(--serif); font-weight: 400;
  font-size: clamp(30px, 3.9vw, 46px); line-height: 1.24; letter-spacing: -.04em;
  margin: 0 0 22px; text-wrap: balance;
}}
h1 em {{ font-style: normal; color: var(--ink-soft); }}
.lede {{ font-size: 17px; color: var(--ink-soft); margin: 0 auto 26px; max-width: 620px; }}
.cta-row {{ display:flex; align-items:center; justify-content:center; gap:16px; flex-wrap:wrap; }}
.cta {{
  display:inline-flex; align-items:center; gap:9px; background: var(--ink); color: var(--page);
  text-decoration:none; padding: 13px 22px; border-radius: 999px; font-size:14.5px; font-weight:500;
  transition: transform .18s ease, opacity .18s ease;
}}
.cta:hover {{ transform: translateY(-1px); opacity:.9; }}
.meta {{ font-size:13.5px; color:var(--ink-soft); }}

/* ---------- reel: holds, then steps ---------- */
.reel {{
  flex: 1 1 auto; display:flex; flex-direction:column; justify-content:center;
  overflow:hidden; padding: 0 0 clamp(18px, 3.5vh, 36px); min-height: 0;
}}
.rail {{ overflow:hidden; }}
.track {{
  display:flex; align-items:center; gap: 40px; width: max-content;
  will-change: transform;
  transition: transform 900ms cubic-bezier(.22,.61,.36,1);
}}
.card {{
  width: 350px; flex: none;
  transform: scale(.46); opacity: .28;
  transition: transform 900ms cubic-bezier(.22,.61,.36,1), opacity 900ms ease;
}}
.card.n1 {{ transform: scale(.7); opacity: .5; }}
.card.n0 {{ transform: scale(1); opacity: 1; }}
.card svg {{ width:100%; height:auto; display:block; }}
.prompt {{
  text-align:center; margin: clamp(10px, 2vh, 22px) 0 0; font-size: 18px;
  letter-spacing:-.01em; color: var(--ink); min-height: 1.6em;
}}
.prompt span::before {{ content:'“'; color:var(--ink-soft); }}
.prompt span::after  {{ content:'”'; color:var(--ink-soft); }}

/* ---------- argument ---------- */
.why {{ margin: clamp(62px, 9vh, 104px) 0 0; }}
.why-grid {{ display:grid; grid-template-columns: 1fr 1fr; gap:88px; align-items:start; }}
.why-copy p {{ margin:0 0 18px; color:var(--ink-soft); font-size:18px; line-height:1.6; }}
.why-copy p:last-child {{ margin:0; }}
.why-copy em {{ font-style:normal; color:var(--ink); }}
.sheets {{
  display:grid; gap:22px; margin: clamp(40px, 6vh, 64px) 0 0;
  width: min(1400px, calc(100vw - 56px)); margin-left:50%; transform:translateX(-50%);
}}
.sheets img {{
  width:100%; height:auto; display:block; border-radius:16px;
  border:1px solid var(--line);
}}
.sheet-note {{ margin:24px 0 0; font-size:14px; color:var(--ink-soft); text-align:center; }}

/* ---------- payoff ---------- */
.gets {{ margin: clamp(62px, 9vh, 104px) 0 0; }}
.get-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap: 56px 64px; }}
.get {{ text-align:center; }}
.orb {{
  width: 250px; height: 250px; margin: 0 auto 14px; display:grid; place-items:center;
}}
.orb svg {{ width:100%; height:auto; display:block; }}
.split {{ position:relative; width:100%; }}
.split span {{ display:block; background:var(--il-canvas); border-radius:12px; overflow:hidden; }}
.split .half {{ position:absolute; inset:0; clip-path: polygon(100% 0, 100% 100%, 0 100%); }}
.get h3 {{ font-family:var(--serif); font-weight:400; font-size:19px; letter-spacing:-.04em; margin:0 0 12px; }}
.get p {{ margin:0 auto; color:var(--ink-soft); font-size:15px; max-width:340px; }}

/* ---------- install ---------- */
.install {{ margin: clamp(62px, 9vh, 104px) 0 0; text-align:center; }}
.install h2, .foot h2 {{ font-family:var(--serif); font-weight:400; font-size:21px; letter-spacing:-.04em; margin:0 0 10px; }}
.install p {{ color:var(--ink-soft); margin:0 0 22px; font-size:15px; }}
.code {{
  display:flex; align-items:center; justify-content:space-between; gap:16px;
  border:1px solid var(--line); border-radius:12px; background:var(--card);
  padding:16px 18px; max-width:640px; margin:0 auto; text-align:left; font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:13px;
  overflow-x:auto;
}}
.code span {{ white-space:nowrap; }}
.copy {{
  appearance:none; border:1px solid var(--line); background:transparent; color:var(--ink-soft);
  border-radius:7px; padding:5px 11px; font:inherit; font-size:12px; cursor:pointer; flex:none;
}}
.copy:hover {{ color:var(--ink); }}

/* ---------- footer ---------- */
.foot {{
  margin: clamp(62px, 9vh, 104px) 0 0; background: var(--il-panel); overflow: hidden;
}}
.foot-inner {{
  max-width: var(--max); margin: 0 auto; padding: 46px 28px 0;
  display: grid; grid-template-columns: 1fr auto 1fr; gap: 40px; align-items: end;
}}
.foot-left {{ padding-bottom: 46px; }}
.foot h2 {{ font-size: 22px; margin: 0 0 12px; }}
.foot p {{ color: var(--ink-soft); font-size: 15px; margin: 0; max-width: 380px; }}
.foot a {{ color: var(--ink); text-decoration: none; border-bottom: 1px solid var(--line); }}
.foot .fine {{ margin-top: 18px; font-size: 12.5px; opacity: .75; }}
.foot-mid {{
  width: 260px; height: 232px; align-self: end;
  background: url('devesh.png') center bottom / contain no-repeat;
}}
.foot-right {{ display:flex; gap:12px; justify-content:flex-end; padding-bottom: 46px; }}
.foot .dot {{
  width: 46px; height: 46px; border-radius: 50%; border: 0; border-bottom: 0;
  background: var(--ink); color: var(--page);
  display: grid; place-items: center; transition: opacity .18s ease, transform .18s ease;
}}
.foot .dot:hover {{ opacity: .85; transform: translateY(-1px); }}

@media (max-width: 900px) {{
  .why-grid {{ grid-template-columns:1fr; gap:24px; }}
}}
@media (max-width: 820px) {{
  .foot-inner {{ grid-template-columns:1fr; gap:22px; text-align:center; justify-items:center; }}
  .foot-left {{ padding-bottom:0; }}
  .foot p {{ margin:0 auto; }}
  .foot-right {{ justify-content:center; padding-bottom:30px; }}
  .foot-mid {{ order:-1; width:200px; height:180px; }}
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
<div class="fold">
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
    <a class="cta" href="{REPO}">Get it on GitHub</a>
  </div>
</header>
</div>

<section class="reel" aria-label="Example illustrations">
  <div class="rail"><div class="track" id="track">{cards}</div></div>
  <p class="prompt" id="prompt"><span id="ptxt"></span></p>
</section>
</div>

<div class="wrap">

<section class="why">
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
</section>

<section class="gets">
  <div class="get-grid">{gets}</div>
</section>

<section class="install">
  <h2>Two lines and it's yours</h2>
  <p>Drop it into your skills folder and ask. Python 3 only, and only if you want to regenerate.</p>
  <div class="code">
    <span id="cmd">git clone {REPO}.git ~/.claude/skills/spotkit</span>
    <button class="copy" id="copy" type="button">Copy</button>
  </div>
</section>

</div>

<footer class="foot">
  <div class="foot-inner">
    <div class="foot-left">
      <h2>Who made this</h2>
      <p>Spotkit was built by <a href="{AUTHOR_URL}">{AUTHOR}</a>, a product
      designer working on developer tools and API documentation.</p>
      <p class="fine">MIT licensed. Icons by Phosphor.</p>
    </div>
    <div class="foot-mid" role="img" aria-label="{AUTHOR}"></div>
    <div class="foot-right">{links}</div>
  </div>
</footer>
<script>
(function () {{
  var P = [
      {prompts_js}
  ];
  var N = P.length;

  // Holds on one illustration, then steps to the next. The track is the set
  // repeated, so advancing never runs out; when it gets far enough along it
  // snaps back by one set with the transition off, which is invisible because
  // the content is identical.
  var track = document.getElementById('track');
  var ptxt  = document.getElementById('ptxt');
  var cards = [].slice.call(track.querySelectorAll('.card'));
  var SETS  = cards.length / N;
  var at    = N;                       // start one set in, so there is room either side
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function place(animate) {{
    track.style.transition = animate ? '' : 'none';
    var slot = cards[0].offsetWidth + parseFloat(getComputedStyle(track).gap || 40);
    var x = track.parentNode.clientWidth / 2 - cards[0].offsetWidth / 2 - at * slot;
    track.style.transform = 'translateX(' + x + 'px)';
    for (var i = 0; i < cards.length; i++) {{
      var d = Math.abs(i - at);
      cards[i].className = 'card' + (d === 0 ? ' n0' : d === 1 ? ' n1' : '');
    }}
    var n = at % N;
    ptxt.textContent = P[n].t + ' — ' + P[n].s;
    if (!animate) track.offsetHeight;   // flush before re-enabling
  }}

  function step() {{
    at++;
    place(true);
    if (at >= (SETS - 1) * N) {{
      setTimeout(function () {{ at -= N; place(false); track.style.transition = ''; }}, 950);
    }}
  }}

  place(false);
  track.style.transition = '';
  if (!reduce) setInterval(step, 3400);
  addEventListener('resize', function () {{ place(false); track.style.transition = ''; }});

  // theme
  var btn = document.getElementById('theme');
  var root = document.documentElement;
  var dark = false;   // the illustrations were designed light-first
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
