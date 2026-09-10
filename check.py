#!/usr/bin/env python3
"""Lint Spotkit illustrations -- and the docs that describe them.

    python3 check.py my-feature.svg [more.svg ...]    lint illustrations
    python3 check.py --flat examples/flat/light/*.svg  literal colours allowed
    python3 check.py --docs                            docs agree with build.py

It checks the rules that fail silently: a second stroke width, a second stroke
colour, more than one shadow, a background rect, text, unsuffixed ids, a moved
fade line. Errors exit non-zero; warnings are judgement calls to look at.

--docs exists because the written spec once drifted from build.py -- snippets
said stroke-width 1 while every shipped file used 0.5, and any model copying
the snippets drew the wrong thing. It fails when a doc disagrees with the code.

Standard library only.
"""
import glob, math, os, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.abspath(__file__))
NS = '{http://www.w3.org/2000/svg}'

FADE = (0.70, 0.82)                       # must match build.GEO FADE_A / FADE_B
SHADOWS = {(2.0, 2.6), (4.0, 5.0)}        # (dy, stdDeviation): lift, liftL
SW = 0.5                                  # THE stroke width, on a 160 canvas
ACCENT_MAX = 2


def tag(el):
    return el.tag.replace(NS, '')


def props(el):
    """Presentation attributes plus anything in style=""."""
    p = dict(el.attrib)
    for decl in p.pop('style', '').split(';'):
        if ':' in decl:
            k, v = decl.split(':', 1)
            p[k.strip()] = v.strip()
    return p


def num(s, default=0.0):
    try:
        return float(re.sub(r'[a-z%]+$', '', str(s).strip()))
    except ValueError:
        return default


def light_tokens():
    css = open(os.path.join(ROOT, 'assets', 'illustration.css')).read()
    blocks = re.findall(r'\{([^{}]*)\}', css)
    out = []
    for b in blocks:
        d = dict(re.findall(r'(--il-[\w-]+):\s*([^;]+);', b))
        if d:
            out.append({k: v.strip().upper() for k, v in d.items()})
    return out[0], out[1]                 # light, dark


# ------------------------------------------------------------- illustrations --
def lint(path, text=None, flat=False):
    errors, warns = [], []
    E, W = errors.append, warns.append
    try:
        root = ET.fromstring(text if text is not None else open(path).read())
    except ET.ParseError as e:
        return [f'not valid XML: {e}'], []

    if tag(root) != 'svg':
        return ['root element is not <svg>'], []

    vb = root.get('viewBox')
    scale = 1.0
    if not vb:
        E('no viewBox -- author on viewBox="0 0 160 160"')
    else:
        w = num(vb.split()[2]) if len(vb.split()) == 4 else 160
        scale = w / 160.0
        if vb.split() != ['0', '0', '160', '160']:
            W(f'viewBox is "{vb}", not "0 0 160 160" -- fine for another canvas '
              f'(see references/scaling.md); expecting strokes of {SW * scale:g}')
    for a in ('width', 'height'):
        if root.get(a):
            E(f'root <svg> has a baked-in {a}= -- drop it and size with CSS')
    if root.get('role') != 'img' or not root.get('aria-label'):
        W('add role="img" and a meaningful aria-label to the root <svg>')

    # parent map, and which elements live inside <defs>/<mask>
    parent = {c: p for p in root.iter() for c in p}

    def inside(el, names):
        while el in parent:
            el = parent[el]
            if tag(el) in names:
                return True
        return False

    drawn = [el for el in root.iter() if not inside(el, ('defs', 'mask'))
             and tag(el) not in ('defs', 'mask')]

    # -- the one stroke ---------------------------------------------------------
    widths, colours = {}, {}
    for el in drawn:
        p = props(el)
        s = p.get('stroke')
        if not s or s == 'none':
            continue
        colours.setdefault(s, 0)
        colours[s] += 1
        wv = p.get('stroke-width')
        if wv is None:
            E(f'<{tag(el)}> has stroke= but no stroke-width -- it defaults to 1, '
              f'double the system width')
            continue
        widths.setdefault(num(wv), 0)
        widths[num(wv)] += 1
    want = round(SW * scale, 4)
    bad = sorted(w for w in widths if abs(w - want) > 1e-6)
    if bad:
        E(f'stroke widths {sorted(widths)} -- every stroke is {want:g}, no exceptions '
          f'(icons are filled, separators are filled rects {want:g} tall)')
    if len(colours) > 1:
        E(f'{len(colours)} stroke colours {sorted(colours)} -- every stroke uses '
          f'var(--il-line, ...) and nothing else')
    elif colours and not flat and '--il-line' not in next(iter(colours)):
        E(f'stroke colour {next(iter(colours))} -- use var(--il-line, #B9B1A4)')

    # -- shadows ----------------------------------------------------------------
    lifted = [el for el in drawn if props(el).get('filter', 'none') != 'none']
    if len(lifted) > 2:
        E(f'{len(lifted)} elements cast a shadow -- at most one does')
    elif len(lifted) == 2:
        W('two elements cast a shadow -- only right for the corner-chip pair (L5); '
          'otherwise exactly one')
    for f in root.iter(NS + 'filter'):
        kids = [tag(k) for k in f]
        if any(k not in ('feDropShadow',) for k in kids):
            E(f'filter #{f.get("id")} uses {kids} -- the only effect is one feDropShadow')
        for d in f.iter(NS + 'feDropShadow'):
            pair = (num(d.get('dy')) / scale, num(d.get('stdDeviation')) / math.sqrt(scale))
            if not any(abs(pair[0] - a) < .01 and abs(pair[1] - b) < .01 for a, b in SHADOWS):
                E(f'shadow dy={d.get("dy")} stdDeviation={d.get("stdDeviation")} -- '
                  f'the system uses dy 2 / blur 2.6 (small) or dy 4 / blur 5 (large)')
            op = d.get('flood-opacity', '1')
            if '--il-shadow-o' not in op and num(op, 1) > 0.2 and not flat:
                E(f'shadow opacity {op} -- use var(--il-shadow-o, 0.16)')

    # -- things that never appear -----------------------------------------------
    for el in drawn:
        t = tag(el)
        if t in ('text', 'tspan', 'foreignObject'):
            E('contains text -- placeholder bars only, never words')
        if t == 'image':
            E('contains an <image> -- the illustration is geometry only')
        if t == 'rect':
            p = props(el)
            if (num(p.get('x')) <= 1 and num(p.get('y')) <= 1
                    and num(p.get('width')) >= 150 * scale and num(p.get('height')) >= 150 * scale
                    and 'url(#' not in p.get('fill', '')):
                E('full-canvas background rect -- delete it; the fade dissolves into the host page')
            x, w = num(p.get('x')), num(p.get('width'))
            if w and not inside(el, ('g',)) and (x < 10 * scale - .01 or x + w > 150 * scale + .01):
                W(f'rect at x={x:g} w={w:g} reaches into the outer 10-unit bleed')

    grads = [g for g in root.iter() if tag(g) in ('linearGradient', 'radialGradient')]
    masked = set()
    for m in root.iter(NS + 'mask'):
        for el in m.iter():
            masked |= set(re.findall(r'url\(#([^)]+)\)', el.get('fill', '')))
    structural = [g for g in grads if g.get('id') not in masked]
    if len(structural) > 1:
        E(f'{len(structural)} gradients -- one only, the base panel\'s vertical gradient')

    # -- the fade ---------------------------------------------------------------
    overlays = [el for el in drawn if tag(el) == 'rect' and 'url(#' in props(el).get('fill', '')
                and num(props(el).get('width')) >= 150 * scale]
    if overlays:
        E('a full-width gradient rect is painted over the art -- that fade only works '
          'on one background colour. Fade with the mask in the boilerplate instead')
    elif not list(root.iter(NS + 'mask')):
        W('no fade mask -- right only for a contained panel (closed on all four sides)')
    for g in grads:
        if g.get('id') in masked:
            offs = sorted(num(s.get('offset')) for s in g.iter(NS + 'stop'))
            if len(offs) == 2 and (abs(offs[0] - FADE[0]) > .005 or abs(offs[1] - FADE[1]) > .005):
                E(f'fade runs {offs[0]:g} -> {offs[1]:g}; every sibling fades '
                  f'{FADE[0]:g} -> {FADE[1]:g}')

    # -- ids --------------------------------------------------------------------
    ids = [el.get('id') for el in root.iter() if el.get('id')]
    suffixes = {i.split('-', 1)[1] if '-' in i else None for i in ids}
    if None in suffixes or len(suffixes) > 1:
        E(f'ids {ids} -- suffix every id with one illustration name '
          f'(fade-teams, lift-teams) or masks cross-apply on a shared page')

    # -- colour -----------------------------------------------------------------
    blob = text if text is not None else open(path).read()
    acc = blob.count('--il-accent')
    if acc > ACCENT_MAX:
        E(f'{acc} accent-coloured elements -- at most {ACCENT_MAX}, ideally one')
    if not flat:
        loose = []
        for el in root.iter():
            if inside(el, ('mask',)) or (tag(el) == 'stop' and parent[el].get('id') in masked):
                continue
            for a in ('fill', 'stroke', 'stop-color', 'flood-color'):
                v = props(el).get(a, '')
                if v.startswith('#'):
                    loose.append(v)
        if loose:
            W(f'{len(loose)} literal colours ({", ".join(sorted(set(loose))[:5])}) will not '
              f'theme -- fine for third-party logo tiles, otherwise var(--il-*, #hex)')

    return errors, warns


# --------------------------------------------------------------------- docs --
DOCS = ['SKILL.md', 'SPEC.md', 'README.md', 'AGENTS.md', 'references/*.md']


def docs():
    import build
    problems = 0
    if (build.GEO['FADE_A'], build.GEO['FADE_B']) != FADE or build.GEO['SW'] != SW:
        print('check.py FADE/SW constants disagree with build.GEO -- update check.py')
        problems += 1
    light, dark = light_tokens()
    files = sorted({f for pat in DOCS for f in glob.glob(os.path.join(ROOT, pat))})
    for f in files:
        rel = os.path.relpath(f, ROOT)
        md = open(f).read()
        for m in re.finditer(r'```(\w*)\n(.*?)```', md, re.S):
            lang, body = m.group(1), m.group(2)
            line0 = md[:m.start()].count('\n') + 2
            for i, ln in enumerate(body.split('\n')):
                where = f'{rel}:{line0 + i}'
                if '<!-- wrong' in ln:
                    continue
                for w in re.findall(r'stroke-width="([\d.]+)"', ln):
                    if w != '0.5':
                        print(f'{where}: stroke-width="{w}" -- the system has one width, 0.5')
                        problems += 1
                for tok, hexv in re.findall(r'var\((--il-[\w-]+),\s*(#[0-9A-Fa-f]{3,6})\)', ln):
                    if tok in light and light[tok] != hexv.upper():
                        print(f'{where}: {tok} fallback {hexv} -- assets/illustration.css says {light[tok]}')
                        problems += 1
                if lang == 'css':
                    for tok, v in re.findall(r'(--il-[\w-]+):\s*([^;]+);', ln):
                        v = v.strip().upper()
                        if tok in light and v not in (light[tok], dark[tok]):
                            print(f'{where}: {tok}: {v} -- assets/illustration.css has '
                                  f'{light[tok]} (light) / {dark[tok]} (dark)')
                            problems += 1
                for dy, sd in re.findall(r'<feDropShadow[^>]*dy="([\d.]+)"\s+stdDeviation="([\d.]+)"', ln):
                    if (float(dy), float(sd)) not in SHADOWS:
                        print(f'{where}: shadow dy {dy} blur {sd} -- system uses 2/2.6 and 4/5')
                        problems += 1
            fade = re.findall(r'<stop offset="([\d.]+)" stop-color="#(?:fff|000)"', body)
            if len(fade) == 2 and tuple(map(float, fade)) != FADE:
                print(f'{rel}:{line0}: fade stops {fade} -- build.py uses {list(FADE)}')
                problems += 1
            if lang == 'svg' and body.lstrip().startswith('<svg'):
                errs, _ = lint(rel, body)
                for e in errs:
                    print(f'{rel}:{line0}: example SVG: {e}')
                problems += len(errs)
    print(f'docs: {len(files)} files, {problems} problem{"s" * (problems != 1)}')
    return problems


# --------------------------------------------------------------------- main --
def main(argv):
    if '--docs' in argv:
        return 1 if docs() else 0
    flat = '--flat' in argv
    paths = [a for a in argv if not a.startswith('--')]
    if not paths:
        print(__doc__.strip().split('\n\n')[1])
        return 2
    failed = 0
    for p in paths:
        errs, warns = lint(p, flat=flat)
        status = 'FAIL' if errs else ('ok, with notes' if warns else 'ok')
        print(f'{p}: {status}')
        for e in errs:
            print(f'  error  {e}')
        for w in warns:
            print(f'  note   {w}')
        failed += bool(errs)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
