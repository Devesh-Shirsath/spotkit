#!/usr/bin/env python3
"""Open Graph card: 1200x630, five illustrations plus the wordmark."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import illos
from flatten import theme_vars, flatten, suffix_ids

v = theme_vars('light')
W, H = 1200, 630
cell, gap = 176, 22
picks = [illos.PROMPTS[i][2]() for i in (0, 2, 4, 5, 3)]
gw = len(picks) * cell + (len(picks) - 1) * gap
ox, oy = (W - gw) // 2, 300

body = f'<rect width="{W}" height="{H}" fill="{v["--il-canvas"]}"/>'
for i, (uid, label, doc) in enumerate(picks):
    inner = flatten(suffix_ids(doc, f'og{i}'), v)
    inner = inner[inner.index('>', inner.index('<svg')) + 1: inner.rindex('</svg>')]
    body += (f'<svg x="{ox + i*(cell+gap)}" y="{oy}" width="{cell}" height="{cell}" '
             f'viewBox="0 0 160 160">{inner}</svg>')

F = 'ui-sans-serif,-apple-system,Helvetica,Arial,sans-serif'
body += f'''
<text x="{W/2}" y="150" font-family="{F}" font-size="64" font-weight="640"
      fill="{v["--il-stroke"]}" text-anchor="middle" letter-spacing="-1.6">spotkit</text>
<text x="{W/2}" y="205" font-family="{F}" font-size="27"
      fill="{v["--il-stroke-soft"]}" text-anchor="middle">Spot illustrations for your whole product</text>
<text x="{W/2}" y="{oy+cell+62}" font-family="{F}" font-size="20"
      fill="{v["--il-stroke-soft"]}" text-anchor="middle" opacity="0.85">A Claude Code skill · MIT</text>'''

open(os.path.join(os.path.dirname(__file__), 'og.svg'), 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{body}</svg>')
print(f'og.svg {W}x{H}')
