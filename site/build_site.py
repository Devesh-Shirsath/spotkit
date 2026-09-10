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
LOGO = open(os.path.join(os.path.dirname(__file__), '.logo_inline.html')).read().strip()
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
     '<div class="stack2"><span class="back" data-theme="dark">' + _mini('categories', 'g2b') +
     '</span><span class="front" data-theme="light">' + _mini('categories', 'g2a') + '</span></div>'),
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

def _svg(name, size=17):
    g = core.icon(name, 0, 0, size, 'currentColor')
    return f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" aria-hidden="true">{g}</svg>'

moon   = f'<span class="only-light">{_svg("moon")}</span>'
sun    = f'<span class="only-dark">{_svg("sun")}</span>'
ghmark = _svg('github-logo', 16)
STARS  = 53

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
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{JSONLD}</script>
<style>
{tokens}

@font-face {{
  font-family: "Geist Pixel";
  src: url('fonts/geist-pixel.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}}
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
  --pixel:    "Geist Pixel", ui-monospace, SFMono-Regular, Menlo, monospace;
  --sans:     "Geist", ui-sans-serif, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}}
html {{ scroll-behavior: smooth; }}

/* Content settles in as it comes into view. The hero is deliberately excluded —
   the first thing anyone sees should already be there. */
.reveal {{
  opacity: 0;
  transform: translateY(22px);
  transition: opacity .85s cubic-bezier(.16,1,.3,1), transform .85s cubic-bezier(.16,1,.3,1);
  transition-delay: var(--d, 0ms);
  will-change: opacity, transform;
}}
.reveal.in {{ opacity: 1; transform: none; }}
h1, h2, h3 {{ font-family: var(--serif); font-weight: 400; letter-spacing: -.04em; }}
body {{
  margin: 0; background: var(--page); color: var(--ink);
  font: 400 16px/1.65 var(--sans);
  -webkit-font-smoothing: antialiased;
  transition: background .35s ease, color .35s ease;
}}
.wrap {{ width: 100%; max-width: var(--max); margin: 0 auto; padding: 0 28px; }}

/* ---------- nav ---------- */
nav {{ display:flex; align-items:center; justify-content:space-between; padding:26px 0 0; flex:0 0 auto; }}
.brand {{ display:flex; align-items:center; line-height:0; color: var(--ink); }}
.brand .logo {{ height:36px; width:auto; display:block; }}
.navr {{ display:flex; align-items:center; gap:8px; }}
.ico {{
  appearance:none; border:1px solid var(--line); background:transparent; color:var(--ink-soft);
  width:38px; height:38px; border-radius:999px; padding:0; cursor:pointer;
  display:inline-grid; place-items:center; text-decoration:none;
  transition:color .2s, border-color .2s;
}}
.ico:hover {{ color:var(--ink); border-color:var(--ink-soft); }}
.ico.wide {{
  width:auto; padding:0 14px; gap:7px; grid-auto-flow:column; align-items:center;
  font:inherit; font-size:13px; font-variant-numeric:tabular-nums;
}}
.ico span {{ line-height:0; }}
.ico svg {{ display:block; }}
.only-light {{ display:block; }}
.only-dark  {{ display:none; }}
[data-theme="dark"] .only-light {{ display:none; }}
[data-theme="dark"] .only-dark  {{ display:block; }}

/* ---------- hero: one full fold ---------- */
.fold {{ min-height: 100svh; display:flex; flex-direction:column; }}
.hero-body {{
  flex: 1 1 auto; display:flex; flex-direction:column; justify-content:center;
  min-height: 0; padding: clamp(20px, 4vh, 44px) 0 0;
}}
header {{ padding: 0; max-width: 820px; margin: 0 auto; text-align: center; }}
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
  flex: 0 0 auto; padding: 0; min-height: 0;
}}
.rail {{ overflow:hidden; padding: 84px 0 14px; }}   /* room for the scaled-up centre card */
/* Cards are placed by JS, not by flex: each one is centred on the rail and then
   pushed out by a measured offset, so the visual gap between neighbours is the
   same at every tier. A flex row cannot do that — its pitch is the unscaled box
   width, so a card at .44 leaves half a box of dead air on both sides. */
.track {{ position: relative; height: 340px; }}
.card {{
  position:absolute; bottom:0; left:50%; width: 340px;
  transform-origin: 50% 100%;                  /* one baseline for the whole reel */
  transform: translateX(-50%) scale(.44); opacity: .14;
  transition: transform 900ms cubic-bezier(.22,.61,.36,1), opacity 900ms ease;
}}
.card svg {{ width:100%; height:auto; display:block; }}
.prompt {{
  text-align:center; margin: 0;
  font-family: var(--pixel); font-size: 16px; letter-spacing: 0;
  color: var(--ink-soft); min-height: 1.7em;
}}
.prompt .q {{ color: var(--ink-soft); opacity: 0; transition: opacity .25s ease; }}
.prompt.started .q {{ opacity: 1; }}   /* no empty “” frame between cycles */
.prompt .caret {{
  display:inline-block; width:.5em; height:1.05em; background: var(--cursor);
  vertical-align:-3px; margin:0 1px 0 3px; border-radius:1px;
}}
.prompt.typing .caret {{ opacity:1; }}                 /* solid while it types */
.prompt.done .caret {{ animation: blink 1.05s steps(1) infinite; }}
@keyframes blink {{ 50% {{ opacity:0; }} }}

/* ---------- argument ---------- */
.why {{ margin: clamp(120px, 20vh, 220px) 0 0; }}
.band {{ max-width: 730px; margin: 0 auto; text-align: center; }}
.band h2 {{ font-size: 32px; line-height: 1.34; margin: 0 0 18px; }}
.band p {{ color: var(--ink-soft); font-size: 17px; margin: 0 auto; max-width: 640px; }}
.band em {{ font-style: normal; color: var(--ink); }}
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
.gets {{ margin: clamp(120px, 20vh, 220px) 0 0; }}
.get-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap: 26px 40px; margin-top: clamp(34px, 5vh, 54px); max-width: 900px; margin-left:auto; margin-right:auto; }}
.get {{ text-align:center; }}
.orb {{
  width: 230px; height: 230px; margin: 0 auto 8px; display:grid; place-items:center;
}}
.orb svg {{ width:100%; height:auto; display:block; }}
.stack2 {{ position:relative; width:88%; margin:0 auto; }}
.stack2 span {{
  display:block; border-radius:15px; overflow:hidden;
  background:var(--il-canvas); border:1px solid var(--il-line);
}}
.stack2 .back {{ position:absolute; inset:0; transform: translate(11%, -9%); }}
.stack2 .front {{ position:relative; }}
.get h3 {{ font-family:var(--serif); font-weight:400; font-size:19px; letter-spacing:-.04em; margin:0 0 12px; }}
.get p {{ margin:0 auto; color:var(--ink-soft); font-size:15px; max-width:340px; }}

/* ---------- install ---------- */
.install {{ margin: clamp(120px, 20vh, 220px) 0 0; text-align:center; }}
.install h2, .foot h2 {{ font-family:var(--serif); font-weight:400; font-size:21px; letter-spacing:-.04em; margin:0 0 10px; }}
.install p {{ color:var(--ink-soft); margin:0 0 22px; font-size:15px; }}
.code {{
  display:flex; align-items:center; gap:14px;
  border:1px solid var(--line); border-radius:12px; background:var(--card);
  padding:16px 18px; max-width:780px; margin:0 auto; text-align:left;
  font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:13px;
  overflow:hidden;
}}
.code span#cmd {{ white-space:nowrap; overflow-x:auto; flex:1 1 auto; min-width:0; }}
.copy {{
  appearance:none; border:1px solid var(--line); background:transparent; color:var(--ink-soft);
  border-radius:7px; padding:5px 11px; font:inherit; font-size:12px; cursor:pointer; flex:none;
}}
.copy:hover {{ color:var(--ink); }}

/* ---------- footer ---------- */
.foot {{
  margin: clamp(120px, 20vh, 220px) 0 0; background: var(--il-panel); overflow: hidden;
}}
.foot-inner {{
  max-width: var(--max); margin: 0 auto; padding: 0 28px;
  display: grid; grid-template-columns: 1fr auto; gap: 48px; align-items: center;
}}
.foot h2 {{ font-size: 22px; margin: 0 0 12px; }}
.foot p {{ color: var(--ink-soft); font-size: 15px; margin: 0; max-width: 380px; }}
.foot a {{ color: var(--ink); text-decoration: none; border-bottom: 1px solid var(--line); }}
.foot .fine {{ margin-top: 18px; font-size: 12.5px; opacity: .75; }}
.foot-left {{ padding: 0; }}
.foot-portrait {{
  width: 340px; height: 284px; align-self: end; margin-top: 56px;
  background: url('devesh.png') center top / 340px auto no-repeat;
}}
.foot .links {{ display:flex; flex-wrap:wrap; gap:12px; margin-top:24px; justify-content:flex-start; }}
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
  .foot-inner {{ grid-template-columns:1fr; gap:28px; text-align:center; justify-items:center; }}
  .foot p {{ margin:0 auto; }}
  .foot .links {{ justify-content:center; }}
  .foot-portrait {{ order:-1; width:230px; height:180px; background-size:230px auto; }}
  .foot-left {{ padding-bottom:0; }}
}}
@media (max-width: 700px) {{
  header {{ padding-top:60px; }}
  .get-grid {{ grid-template-columns:1fr; gap:34px; }}
  .card {{ width:150px; }}
  .rail {{ padding: 42px 0 10px; }}
  .prompt {{ font-size:16.5px; }}
}}
@media (prefers-reduced-motion: reduce) {{
  html {{ scroll-behavior:auto; }}
  .reveal {{ opacity:1 !important; transform:none !important; }}
  *, *::before, *::after {{ animation-duration:.001ms !important; transition-duration:.001ms !important; }}
}}
</style>
</head>
<body>
<div class="fold">
<div class="wrap">
<nav>
  <a class="brand" href="#" aria-label="Spotkit">{LOGO}</a>
  <div class="navr">
    <button class="ico" id="theme" type="button" aria-label="Switch theme">{moon}{sun}</button>
    <a class="ico wide" href="{REPO}" aria-label="Spotkit on GitHub">{ghmark}<span id="stars">{STARS}</span></a>
  </div>
</nav>
</div>

<div class="hero-body">
<div class="wrap">
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
  <p class="prompt" id="prompt"><span class="q">“</span><span id="ptxt"></span><span class="caret" aria-hidden="true"></span><span class="q">”</span></p>
</section>
</div>
</div>

<div class="wrap">

<section class="why">
  <div class="band">
    <h2>Drawing one is easy.<br>Drawing twenty that match is the job.</h2>
    <p>Spotkit is a system, not a generator — twelve layouts chosen by what a
    feature <em>means</em>, one stroke width and one colour throughout.</p>
  </div>
  <div class="sheets">
    <img src="sheet-light.svg" alt="Twelve Spotkit illustrations in light mode" loading="lazy" width="1116" height="376">
    <img src="sheet-dark.svg" alt="The same twelve illustrations in dark mode" loading="lazy" width="1116" height="376">
  </div>
</section>

<section class="gets">
  <div class="band">
    <h2>What you actually get.</h2>
    <p>An editable file rather than a picture, both themes out of one source,
    twelve layouts that keep a set from repeating itself — and nothing to pay for.</p>
  </div>
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
      <h2>Meet the creator</h2>
      <p>Spotkit was built by <a href="{AUTHOR_URL}">{AUTHOR}</a>, a product
      designer working on developer tools and API documentation.</p>
      <div class="links">{links}</div>
    </div>
    <div class="foot-portrait" role="img" aria-label="{AUTHOR}"></div>
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
  var prompt = document.getElementById('prompt');
  var typer  = null;

  function type(n) {{
    clearInterval(typer);
    var full = P[n].t + ' — ' + P[n].s, i = 0;
    if (reduce) {{ ptxt.textContent = full; prompt.className = 'prompt done started'; return; }}
    ptxt.textContent = '';
    prompt.className = 'prompt typing';
    typer = setInterval(function () {{
      ptxt.textContent = full.slice(0, ++i);
      if (i === 1) prompt.classList.add('started');
      if (i >= full.length) {{
        clearInterval(typer);
        prompt.className = 'prompt done started';
      }}
    }}, 26);
  }}

  // Scale and opacity by distance from the centre; anything further out is
  // pinned to the last tier. The centre offsets are cumulative half-widths plus
  // one constant gap, so every neighbour sits the same distance from the last —
  // which a fixed flex pitch cannot give you once the cards are scaled.
  var SCALE = [1.22, .80, .58, .44];
  var OPAC  = [1, .52, .28, .14];
  var CEN = null, W = 0;
  function sc(d) {{ return SCALE[Math.min(d, SCALE.length - 1)]; }}
  function op(d) {{ return OPAC[Math.min(d, OPAC.length - 1)]; }}

  function measure() {{
    W = cards[0].offsetWidth;
    track.style.height = W + 'px';          // svgs are square
    var gap = W * 0.053;
    CEN = [0];
    for (var k = 1; k < cards.length; k++)
      CEN[k] = CEN[k - 1] + W * sc(k - 1) / 2 + gap + W * sc(k) / 2;
  }}

  function place(animate) {{
    if (!CEN || cards[0].offsetWidth !== W) measure();
    for (var i = 0; i < cards.length; i++) {{
      var d = i - at, ad = Math.abs(d), c = cards[i];
      if (!animate) c.style.transition = 'none';
      c.style.transform = 'translateX(calc(-50% + ' + (d < 0 ? -CEN[ad] : CEN[ad]) +
                          'px)) scale(' + sc(ad) + ')';
      c.style.opacity = op(ad);
    }}
    type(at % N);
    if (!animate) {{
      track.offsetHeight;                   // flush before re-enabling
      for (var j = 0; j < cards.length; j++) cards[j].style.transition = '';
    }}
  }}
  addEventListener('resize', function () {{ measure(); place(false); }});

  function step() {{
    at++;
    place(true);
    if (at >= (SETS - 1) * N) {{
      setTimeout(function () {{ at -= N; place(false); }}, 950);
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
  function paint() {{ root.setAttribute('data-theme', dark ? 'dark' : 'light'); }}
  btn.addEventListener('click', function () {{ dark = !dark; paint(); }});
  paint();

  // Reveal on scroll. Groups stagger by index so a row of four arrives as a
  // wave rather than all at once.
  var groups = [
    ['.band', 0], ['.sheets img', 110], ['.get', 90],
    ['.install h2, .install p, .code', 70], ['.foot-left, .foot-portrait', 90]
  ];
  if (!reduce && 'IntersectionObserver' in window) {{
    var io = new IntersectionObserver(function (entries) {{
      entries.forEach(function (e) {{
        if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }}
      }});
    }}, {{ rootMargin: '0px 0px -12% 0px', threshold: 0.12 }});

    var watched = [];
    groups.forEach(function (g) {{
      [].slice.call(document.querySelectorAll(g[0])).forEach(function (el, i) {{
        el.classList.add('reveal');
        el.style.setProperty('--d', (i * g[1]) + 'ms');
        io.observe(el);
        watched.push(el);
      }});
    }});

    // Safety net: anything already on screen shows immediately, and after three
    // seconds everything gives up and shows regardless. Content must never be
    // left invisible because an observer did not fire.
    function showIfVisible() {{
      watched.forEach(function (el) {{
        var r = el.getBoundingClientRect();
        if (r.top < innerHeight && r.bottom > 0) el.classList.add('in');
      }});
    }}
    requestAnimationFrame(showIfVisible);
    setTimeout(function () {{
      watched.forEach(function (el) {{ el.classList.add('in'); }});
    }}, 3000);
  }}

  // live star count, falling back to whatever was baked in at build time
  fetch('https://api.github.com/repos/Devesh-Shirsath/spotkit')
    .then(function (r) {{ return r.ok ? r.json() : null; }})
    .then(function (d) {{
      if (d && typeof d.stargazers_count === 'number') {{
        document.getElementById('stars').textContent = d.stargazers_count;
      }}
    }})
    .catch(function () {{}});

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
