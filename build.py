#!/usr/bin/env python3
"""Generates the exemplar illustrations and the contact-sheet gallery.

Two layers:

  GEO + primitives   the visual language. Shared by every layout, never varied.
  LAYOUTS            twelve compositions. Varied per illustration, on purpose.

The split is the whole point. Monotony comes from reusing one *layout*; family
coherence comes from reusing the *language*. Change a constant in GEO and all
twelve move together.
"""
import os
from icons import PHOSPHOR

# ---------------------------------------------------------------- geometry --
GEO = dict(
    SIZE=160,
    PANEL_X=21, PANEL_W=118, PANEL_Y=8, PANEL_R=10,
    CARD_X=11,  CARD_W=138,  CARD_Y=24, CARD_H=27, CARD_R=8,
    MED_CX=80,  MED_CY=33,   MED_R=14,
    FADE_A=0.70, FADE_B=0.82,
    PAD=10,          # content inset from the panel edge
    SW=0.5,          # THE stroke width. Every stroke, everywhere. No exceptions.
    CPAD=8,          # breathing room inside a card, top AND bottom. Equal.
)
# The panel is NOT a fixed box. Each layout sizes it to its own content and
# picks an edge treatment. What stays constant is the language -- radius, stroke,
# padding, fade height -- not the rectangle.
G = GEO
PX, PW = G['PANEL_X'], G['PANEL_W']
IN_X = PX + G['PAD']                     # 31 -- content left edge
IN_R = PX + PW - G['PAD']                # 129 -- content right edge

SW    = GEO['SW']
LINE  = 'var(--il-line, #B9B1A4)'      # THE stroke colour. Every stroke, everywhere.
FILL  = 'var(--il-fill, #DCD6CE)'
FSOFT = 'var(--il-fill-soft, #E9E4DC)'
SOFT  = 'var(--il-stroke-soft, #9B948A)'
SURF  = 'var(--il-surface, #FFFFFF)'
GHOST = 'var(--il-ghost, #EAE7E2)'
ACC   = 'var(--il-accent, #3E9077)'
STRK  = 'var(--il-stroke, #35322D)'

# ------------------------------------------------------------------- icons --
def icon(name, x, y, size, color=STRK, weight='regular'):
    sc = size / 256.0
    return (f'<g transform="translate({x:.2f} {y:.2f}) scale({sc:.5f})" fill="{color}">'
            f'<path d="{PHOSPHOR[weight][name]}"/></g>')

def avatar(x, y, size, color=SOFT):
    return icon('user-circle', x, y, size, color)

# -------------------------------------------------------------- primitives --
def bar(x, y, w, h=5, fill=FILL):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.2f}" fill="{fill}"/>'

def barpair(x, y, w1, w2, h1=4.2, h2=5.2, gap=7.6):
    return bar(x, y, w1, h1) + bar(x, y + gap, w2, h2)

def dot(x, y, r, on=True, c=FILL):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>' if on else
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{LINE}" stroke-width="{SW}"/>')

def rule(x1, x2, y, op=0.8):
    """Separators are filled hairlines, not strokes -- that keeps the stroke
    inventory at exactly one width and one colour."""
    return f'<rect x="{x1}" y="{y}" width="{x2-x1}" height="{SW}" fill="{LINE}" opacity="{op}"/>'

def vrule(x, y1, y2, op=0.75):
    return f'<rect x="{x}" y="{y1}" width="{SW}" height="{y2-y1}" fill="{LINE}" opacity="{op}"/>'

def backdrop(kind, x, w, y, h=None):
    """What sits behind the panel. Optional, and varied on purpose -- a fixed
    plate behind every illustration is the fastest way to make a set look
    mechanical."""
    r = G['PANEL_R'] + 6
    if kind == 'none':
        return ''
    if kind == 'plate':
        return (f'<rect x="{x-7}" y="{y+4}" width="{w+14}" height="{(h or 160-y)+6}" rx="{r}" '
                f'fill="{GHOST}" stroke="{LINE}" stroke-width="{SW}"/>')
    if kind == 'offset':                      # a second sheet, down and to the right
        return (f'<rect x="{x+8}" y="{y+8}" width="{w}" height="{(h or 160-y)}" rx="{G["PANEL_R"]}" '
                f'fill="{GHOST}" stroke="{LINE}" stroke-width="{SW}"/>')
    if kind == 'twin':                        # a stack seen edge-on
        # Every sheet steps DOWN from the one in front, and no two share a top
        # edge -- the front card has to read as the front card.
        return ''.join(
            f'<rect x="{x-d}" y="{y+d}" width="{w+2*d}" height="{(h or 160-y)}" rx="{G["PANEL_R"]+d//2}" '
            f'fill="{GHOST}" stroke="{LINE}" stroke-width="{SW}"/>'
            for d in (10, 5))
    raise ValueError(kind)


def panel(uid, x=21, w=118, y=8, h=None, mode='fade', chrome=False, back='plate'):
    """mode='fade'      -- open bottom, dissolves. Says: there is more.
       mode='contained' -- closed on all four sides. Says: this is all of it."""
    r = G['PANEL_R']
    s = backdrop(back, x, w, y, h)
    if mode == 'fade':
        p = (f"M{x} {y+r}a{r} {r} 0 0 1 {r} -{r}h{w-2*r}a{r} {r} 0 0 1 {r} {r}V160H{x}z")
        s += f'<path d="{p}" fill="url(#panelG-{uid})" stroke="{LINE}" stroke-width="{SW}"/>'
    else:
        s += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
              f'fill="url(#panelG-{uid})" stroke="{LINE}" stroke-width="{SW}"/>')
    if chrome:
        s += ''.join(dot(x + 10 + i * 5.5, y + 9, 1.7, True, LINE) for i in range(3))
        s += rule(x, x + w, y + 16, 0.55)
    return s


def head_strip(x, w, y, bw=30):
    """A titled top edge. Gives a panel something to hold when the floating
    element only covers one side of it -- otherwise the header reads as a hole."""
    return bar(x + G['PAD'], y, bw, 5) + rule(x, x + w, y + 13, 0.5)


def card(x, y, w, h, r, uid, lift=True, fill=SURF, stroke=LINE):
    # bigger objects sit further off the surface -- one shadow for everything
    # reads as a sticker sheet rather than a stack
    big = w * h > 2600
    f = (f' filter="url(#lift{"L" if big else ""}-{uid})"') if lift else ''
    return (f'<g{f}><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{SW}"/></g>')

def tile(x, y, s=16, r=5, fill=None):
    if fill:
        return f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{r}" fill="{fill}"/>'
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{r}" fill="none" '
            f'stroke="{LINE}" stroke-width="{SW}"/>' + dot(x + s / 2, y + s / 2, 2.4))


def kebab(x, y):
    return ''.join(dot(x, y + i * 3.6, 1.15, True, SOFT) for i in (-1, 0, 1))


def check(x, y, s=9, c=ACC):
    return icon('check', x, y, s, c)


def cursor(x, y, c=ACC):
    return f'<path d="M{x} {y}l4.6 11.4 1.8-4.6 4.6-1.8z" fill="{c}"/>'


def cluster(x, y, cols, extra=True, r=6.2):
    """A row of avatars plus a +N chip. Deliberately spaced rather than
    overlapped: an overlapping cluster needs a surface-coloured knockout ring to
    stay legible, and that would be a second stroke colour in a system that has
    exactly one."""
    gap = r * 2 + 2.4
    s = ''.join(f'<circle cx="{x + i * gap:.1f}" cy="{y}" r="{r}" fill="{c}" opacity="0.7"/>'
                for i, c in enumerate(cols))
    cx = x + len(cols) * gap
    s += f'<circle cx="{cx:.1f}" cy="{y}" r="{r}" fill="{FSOFT}"/>'
    return s + bar(cx - 3.2, y - 1.4, 6.4, 2.8, SOFT)


def pill(x, y, w, h=11, sel=False):
    """Selected pills are a fill; unselected are an outline. One stroke spec."""
    edge = '' if sel else f' stroke="{LINE}" stroke-width="{SW}"'
    fill = FSOFT if sel else 'none'
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" '
            f'fill="{fill}"{edge}/>')


def svg(uid, label, faded, floating=''):
    return f'''<svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" class="il">
  <defs>
    <linearGradient id="fadeG-{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="{G['FADE_A']}" stop-color="#fff"/><stop offset="{G['FADE_B']}" stop-color="#000"/>
    </linearGradient>
    <mask id="fade-{uid}"><rect width="160" height="160" fill="url(#fadeG-{uid})"/></mask>
    <linearGradient id="panelG-{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="var(--il-panel-top, #FCFBF9)"/>
      <stop offset="1" stop-color="var(--il-panel, #F7F5F2)"/>
    </linearGradient>
    <filter id="lift-{uid}" x="-60%" y="-60%" width="220%" height="220%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.6"
        flood-color="var(--il-shadow-c, #4A3F33)" flood-opacity="var(--il-shadow-o, 0.16)"/>
    </filter>
    <filter id="liftL-{uid}" x="-60%" y="-60%" width="220%" height="220%">
      <feDropShadow dx="0" dy="4" stdDeviation="5"
        flood-color="var(--il-shadow-c, #4A3F33)" flood-opacity="var(--il-shadow-o, 0.16)"/>
    </filter>
  </defs>
  <g mask="url(#fade-{uid})">
{faded}
  </g>
{floating}
</svg>
'''


def header_card(uid, ic, x=11, w=138, y=None, h=None):
    y = G['CARD_Y'] if y is None else y
    h = G['CARD_H'] if h is None else h
    return (card(x, y, w, h, G['CARD_R'], uid)
            + icon(ic, x + 16, y + (h - 16) / 2, 16)
            + barpair(x + 41, y + (h - 19) / 2, 29, 58, 4.8, 6, 8.4))


def medallion(uid, ic, cx=80, cy=None, r=None, lift=False):
    cy = G['MED_CY'] if cy is None else cy
    r = G['MED_R'] if r is None else r
    f = f' filter="url(#lift-{uid})"' if lift else ''
    return (f'<g{f}><circle cx="{cx}" cy="{cy}" r="{r}" fill="{SURF}" '
            f'stroke="{LINE}" stroke-width="{SW}"/></g>'
            + icon(ic, cx - 7.5, cy - 7.5, 15))


# =========================================================== L A Y O U T S ==
# Each layout sizes its own panel to its own content and picks an edge
# treatment. Only the language is shared.

BRAND = ['#C25E3E', '#2F9468', '#5C82CE', '#B08A3E', '#8A6BC0']


def L1_header_rows(uid, label, ic):
    b = panel(uid, 21, 118, 8, back='twin')
    for i in range(3):
        y = 60 + i * 21
        b += avatar(33, y, 15)
        b += barpair(57, y + 0.5, 28, 52, 4.2, 5.2, 7.4)
    return uid, label, svg(uid, label, b, header_card(uid, ic))


def L2_cascade(uid, label, ic):
    """Narrow panel, wide raised row. The float is the widest thing here."""
    b = panel(uid, 25, 110, 8, back='offset')
    for i, (x, w, h, op) in enumerate([(35, 90, 16, 0.70), (45, 70, 13, 0.40)]):
        y = 84 + i * 22
        sc = w / 134.0
        b += f'<g opacity="{op}">' + card(x, y, w, h, 6.5, uid, lift=False)
        b += avatar(x + 7, y + h / 2 - 5, 10)
        b += bar(x + 21, y + h / 2 - 2.1, w - 38, 4.2)
        b += icon('pencil-simple', x + w - 15, y + h / 2 - 4.2, 8.5, SOFT) + '</g>'
    top = card(13, 56, 134, 21, 7, uid)
    top += avatar(24, 61.5, 11) + bar(41, 64.7, 62, 4.6)
    top += icon('pencil-simple', 129, 61.5, 10, SOFT)
    return uid, label, svg(uid, label, b, medallion(uid, ic) + top)


def L3_tabbar(uid, label, ic, sel=1):
    b = panel(uid, 24, 112, 8, back='plate')
    for i in range(3):
        y = 62 + i * 22
        b += icon('book-open', 34, y, 13, SOFT)
        b += barpair(54, y - 0.5, 30, 54, 4.2, 5.2, 7.4)
    y = G['CARD_Y']
    f = card(11, y, 138, 24, 8, uid) + icon(ic, 21, y + 5.5, 13, SOFT)
    for i, (x, w) in enumerate(zip([40, 66, 96, 120], [22, 26, 20, 18])):
        f += pill(x, y + 6.5, w, 11, i == sel)
        f += bar(x + 5, y + 10.6, w - 10, 2.8, SOFT if i == sel else FILL)
    return uid, label, svg(uid, label, b, f)


def L4_toolbar(uid, label):
    b = panel(uid, 22, 116, 8, back='none')
    b += cluster(41, 66, BRAND[:4], True)
    b += rule(22, 138, 82)
    for i in range(3):
        y = 90 + i * 16
        b += avatar(32, y - 5.5, 11)
        b += bar(48, y - 2.2, 54, 4.4)
        b += check(119, y - 4.5, 9, ACC if i == 0 else FILL)
    y = G['CARD_Y']
    f = card(11, y, 138, 26, 9, uid)
    for i, c in enumerate(BRAND[:4]):
        f += tile(26 + i * 23, y + 7.5, 12, 4, c)
    f += vrule(119, y + 7, y + 19, 0.8) + icon('magnifying-glass', 128, y + 8, 10, SOFT)
    return uid, label, svg(uid, label, b, f)


def L5_corner_chips(uid, label, ic):
    """Narrow panel with a real header, chips on the diagonal."""
    b = panel(uid, 28, 104, 8, back='offset')
    b += bar(96, 20, 18, 4.6) + kebab(124, 22.5)     # answers the chip on the left
    b += rule(28, 132, 34, 0.5)
    for i in range(4):
        y = 46 + i * 19
        b += icon('book-open', 38, y, 12, SOFT)
        b += barpair(56, y - 0.5, 24, 52, 4, 5, 7.2)
    a = card(13, 12, 58, 21, 8, uid) + icon(ic, 22, 17, 12) + bar(39, 20.4, 24, 4.6)
    c = card(91, 94, 58, 21, 8, uid) + icon('stack', 100, 99, 12, SOFT) + bar(117, 102.4, 24, 4.6)
    return uid, label, svg(uid, label, b, a + c)


def L6_window(uid, label):
    """Wide panel sized to hold its rows -- nothing spills."""
    b = panel(uid, 13, 134, 8, chrome=True, back='twin')
    for i in range(3):
        y = 34 + i * 22
        b += card(21, y, 118, 18, 6, uid, lift=(i == 0))
        b += tile(26, y + 3, 12, 4, BRAND[i])
        b += bar(44, y + 6.6, 22, 4.4)
        b += vrule(73, y + 4, y + 14, 0.7)
        b += bar(80, y + 6.6, 24, 4.4)
        b += vrule(110, y + 4, y + 14, 0.7)
        b += bar(117, y + 6.6, 12, 4.4)
        b += kebab(134, y + 9)
    return uid, label, svg(uid, label, b)


def L7_fanned(uid, label):
    """Contained panel. The raised card breaks its top edge."""
    b = panel(uid, 16, 128, 44, h=92, mode='contained', back='none')
    for i, x in enumerate((22, 92)):
        b += card(x, 54, 46, 50, 9, uid, lift=False)      # 54..104
        b += (f'<circle cx="{x+23}" cy="70" r="9.5" fill="{BRAND[i+1]}" opacity="0.3"/>')
        b += icon('user-circle', x + 17, 64, 12, SOFT)
        b += bar(x + 11, 86, 24, 4.2) + bar(x + 8, 93, 30, 4.2)   # ends 97.2
    b += bar(48, 112, 64, 5) + bar(58, 121, 44, 4.4)
    mid = card(55, 32, 50, 60, 11, uid)                   # 32..92
    mid += f'<circle cx="80" cy="52" r="12" fill="{ACC}" opacity="0.14"/>'
    mid += icon('user-circle', 72.5, 44.5, 15, ACC)
    mid += bar(65, 70, 30, 4.8) + bar(61, 78.5, 38, 4.8)  # ends 83.3
    return uid, label, svg(uid, label, b, mid)


def L8_notifications(uid, label):
    """Contained, almost no chrome. The cards are the whole idea."""
    b = panel(uid, 26, 108, 30, h=100, mode='contained', back='offset')
    b += card(38, 80, 92, 32, 10, uid, lift=False)
    b += f'<circle cx="53" cy="96" r="9.5" fill="{BRAND[1]}" opacity="0.8"/>'
    b += bar(69, 89, 34, 4.8) + bar(69, 98.5, 50, 5.4)
    f = card(16, 44, 112, 34, 10, uid)
    f += f'<circle cx="33" cy="61" r="10" fill="{BRAND[0]}" opacity="0.8"/>'
    f += bar(50, 53, 40, 5) + bar(50, 63, 62, 5.6)
    return uid, label, svg(uid, label, b, f)


def L9_constellation(uid, label, ic):
    """No header. The hub is the floating element -- when a feature is about one
    thing everything else connects to, a title bar above it is noise."""
    b = panel(uid, 21, 118, 8, back='plate')
    for x, y in [(28, 34), (28, 82), (112, 34), (112, 82)]:
        sx, ex = (44, 63) if x < 80 else (112, 97)
        cx = (sx + ex) / 2
        b += (f'<path d="M{sx if x<80 else x} {y+8}C{cx} {y+8} {cx} 63 {ex if x<80 else 97} 63" '
              f'fill="none" stroke="{LINE}" stroke-width="{SW}" stroke-dasharray="2.4 3" '
              f'stroke-linecap="round"/>')
        b += tile(x, y)
    b += bar(52, 104, 56, 5) + bar(62, 114, 36, 4.4)
    hub = card(63, 46, 34, 34, 11, uid) + icon(ic, 71, 54, 18)
    return uid, label, svg(uid, label, b, hub)


def L10_matrix(uid, label, ic):
    """A corner chip, not a title bar. The column icons already occupy the right
    of the header band, so a full-width float would fight them."""
    b = panel(uid, 21, 118, 8, back='none')
    cols = [92, 108, 124]
    for x in (84, 100, 116, 132):
        b += vrule(x, 48, 124, 0.55)
    for i, x in enumerate(cols):
        b += icon(['book-open', 'brackets-curly', 'shield-check'][i], x - 5.5, 50, 11, SOFT)
    b += rule(30, 132, 66)
    for r, cells in enumerate([[1, 1, 1], [1, 1, 0], [1, 0, 0], [0, 1, 0]]):
        y = 76 + r * 13
        b += avatar(31, y - 6.5, 13) + bar(48, y - 2.5, 26, 5)
        for x, on in zip(cols, cells):
            b += dot(x, y, 3, on)
    chip = card(13, 16, 62, 22, 8, uid) + icon(ic, 22, 21, 12) + bar(39, 24.4, 26, 4.6)
    return uid, label, svg(uid, label, b, chip)


def L11_timeline(uid, label, ic):
    """Narrow panel, narrow float. A full-width bar over a single column of
    events reads as a header bolted onto the wrong shape."""
    b = panel(uid, 28, 104, 8, back='offset')
    b += vrule(44, 50, 126, 0.7)
    for i, y in enumerate([56, 80, 104]):
        b += dot(44, y, 3.6, True, ACC if i == 0 else FILL)
        b += barpair(58, y - 7, 22, 50, 4.2, 5.2, 7.4)
    chip = card(18, 14, 74, 22, 8, uid) + icon(ic, 27, 19, 12) + bar(44, 22.4, 34, 4.6)
    return uid, label, svg(uid, label, b, chip)


def L12_split(uid, label, ic):
    b = panel(uid, 22, 116, 30, h=100, mode='contained', back='plate')
    for x, done in ((30, False), (84, True)):
        b += card(x, 62, 46, 44, 8, uid, lift=False)      # 62..106
        b += bar(x + 8, 71, 28, 4.6) + bar(x + 8, 80, 20, 4.6)
        b += (check(x + 7, 89) if done else dot(x + 10.5, 93.5, 3.2, False))
    b += icon('arrow-right', 74, 78, 12, SOFT)
    b += bar(56, 116, 48, 4.6)
    return uid, label, svg(uid, label, b, medallion(uid, ic, cy=30))


SET = [
    lambda: L2_cascade('teams', 'Teams', 'users-three'),
    lambda: L3_tabbar('categories', 'Categories', 'tag'),
    lambda: L4_toolbar('workspace', 'Workspace access'),
    lambda: L5_corner_chips('docs', 'Documentation', 'book-open'),
    lambda: L6_window('connectors', 'Connectors'),
    lambda: L7_fanned('contributors', 'Contributors'),
    lambda: L8_notifications('notifications', 'Notifications'),
    lambda: L9_constellation('gateway', 'API gateway', 'tree-structure'),
    lambda: L10_matrix('roles', 'Roles &amp; access', 'lock-key'),
    lambda: L11_timeline('audit', 'Audit log', 'clock-counter-clockwise'),
    lambda: L12_split('approval', 'App approval', 'file-text'),
    lambda: L1_header_rows('billing', 'Invoices', 'receipt'),
]

if __name__ == '__main__':
    os.makedirs('examples', exist_ok=True)
    items = [f() for f in SET]
    for uid, label, doc in items:
        open(f'examples/{uid}.svg', 'w').write(doc)

    def grid(t):
        out = ''
        for uid, label, doc in items:
            d = doc.replace('-' + uid + '"', '-' + uid + t + '"')
            d = d.replace('-' + uid + ')', '-' + uid + t + ')')
            out += '<figure>' + d + '<figcaption>' + label + '</figcaption></figure>'
        return out

    open('examples/gallery.html', 'w').write(f'''<!doctype html><meta charset="utf-8">
<title>Illustration contact sheet</title>
<style>
{open('assets/illustration.css').read()}
  body {{ margin:0; font:13px/1.5 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif; }}
  .pane {{ padding:26px 22px; }}
  .light {{ background:#EDEAE6; color:#7a736a; }}
  .dark  {{ background:#1A1918; color:#877f74; }}
  h2 {{ font-size:10px; letter-spacing:.1em; text-transform:uppercase; font-weight:600;
       margin:0 0 16px; opacity:.6; }}
  .g {{ display:grid; grid-template-columns:repeat(6,1fr); gap:16px; align-items:start; }}
  figure {{ margin:0; }} .g svg {{ width:100%; display:block; }}
  figcaption {{ margin-top:7px; font-size:10.5px; opacity:.75; text-align:center; }}
</style>
<div class="pane light" data-theme="light"><h2>Light</h2><div class="g">{grid('l')}</div></div>
<div class="pane dark" data-theme="dark"><h2>Dark</h2><div class="g">{grid('d')}</div></div>
''')
    print('wrote', len(items), 'svgs + gallery')
