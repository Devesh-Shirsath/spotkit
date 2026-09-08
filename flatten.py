#!/usr/bin/env python3
"""Flat exports: literal colours baked in, no CSS custom properties.

Two uses:
  1. GitHub README images -- <img> and <object> never resolve var(), so a themed
     SVG always shows its fallback. A per-theme flat file plus <picture> fixes it.
  2. Figma -- Figma's SVG importer does not run CSS either, so pasting a themed
     file gives you black shapes. These paste correctly.

Writes examples/flat/<theme>/*.svg and a contact sheet per theme.
"""
import os, re, build

def theme_vars(name):
    css = open('assets/illustration.css').read()
    marker = ':root,\n[data-theme="light"] {' if name == 'light' else '[data-theme="dark"] {'
    i = css.index(marker); j = css.index('}', i)
    return dict(re.findall(r'(--il-[\w-]+):\s*([^;]+);', css[i:j]))

def flatten(doc, vars_):
    def sub(m):
        return vars_.get(m.group(1), m.group(2)).strip()
    return re.sub(r'var\((--il-[\w-]+),\s*([^)]+)\)', sub, doc)

def suffix_ids(doc, tag):
    for base in ('fadeG', 'fade', 'panelG', 'lift', 'liftL'):
        doc = doc.replace(f'"{base}-', f'"{base}-{tag}-').replace(f'(#{base}-', f'(#{base}-{tag}-')
    return doc

items = [f() for f in build.SET]

for theme in ('light', 'dark'):
    v = theme_vars(theme)
    out = f'examples/flat/{theme}'
    os.makedirs(out, exist_ok=True)
    for uid, label, doc in items:
        open(f'{out}/{uid}.svg', 'w').write(flatten(doc, v))

    # contact sheet: 6 x 2 grid of 160px cells, 20px gutter, on the theme canvas
    cell, gap, pad = 160, 18, 22
    cols, rows = 6, 2
    W = pad * 2 + cols * cell + (cols - 1) * gap
    H = pad * 2 + rows * cell + (rows - 1) * gap
    body = f'<rect width="{W}" height="{H}" fill="{v["--il-canvas"]}"/>'
    for i, (uid, label, doc) in enumerate(items):
        x = pad + (i % cols) * (cell + gap)
        y = pad + (i // cols) * (cell + gap)
        inner = flatten(suffix_ids(doc, f's{i}'), v)
        inner = inner[inner.index('>', inner.index('<svg')) + 1: inner.rindex('</svg>')]
        body += f'<svg x="{x}" y="{y}" width="{cell}" height="{cell}" viewBox="0 0 160 160">{inner}</svg>'
    open(f'examples/contact-{theme}.svg', 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{body}</svg>')

print('flat exports + contact sheets written')
