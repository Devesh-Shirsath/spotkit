# Spotkit spec — start here

This one file, plus [`references/icons.md`](references/icons.md) for icon paths,
is enough to draw an illustration that matches the rest of the family. The other
files in `references/` add depth — how to pick a metaphor, how to pick a layout,
how to build a set — but every number lives here.

Every value below was copied from `build.py`, which generated every example in
this repo, and `python3 check.py --docs` fails if this file drifts from it.
Don't improvise any of them: this style is sub-pixel geometry, and a stroke of 1
where the system uses 0.5 is visibly wrong.

## 0 · The standing rule: adapt, don't invent

**Pick the nearest of the twelve layouts in §7, start from its example file,
keep its geometry and change only the content** — the icon, what sits inside
the cards, how many rows within the layout's limit. Every tool that follows
this produces the same family; every tool that composes from scratch drifts.
Invent a new composition only when none of the twelve fits, and say so.

- **You can run Python in this repo:** copy that layout's `L*` function in
  `build.py`, edit its content, write the SVG out, run `python3 check.py out.svg`.
- **You can't run code:** fetch the layout's example file from §7, edit its
  content by hand, and go through §9 before you answer.
- **Write SVG code.** Never hand this to an image-generation model — it cannot
  hold a 0.5 stroke, and it will not match the family.

## 1 · Canvas

- `viewBox="0 0 160 160"`, whatever size it is shown at. No `width`/`height` on
  the root. **No background rect** — the fade dissolves into the host page.
- Lanes: outer **10** units are bleed (shadow spill only) · floating cards live in
  **x 11 → 149** · the panel lives in **x 21 → 139**.
- The fade runs from **y 112 to y 131** (70% → 82%). Nothing important below y 112.
- Centre of gravity on x 80, weighted to the upper two-thirds.

## 2 · The one stroke

**Every stroked element uses `stroke-width="0.5"` and
`stroke="var(--il-line, #B9B1A4)"`.** Panels, cards, backdrops, pills, hollow
dots, connectors — all of them. There is no second width and no second stroke
colour. Hierarchy comes from fills, opacity and the one shadow, never line weight.

- Separators are **filled rects 0.5 tall**, not strokes.
- Icons are **filled** Phosphor paths. Never `stroke` an icon, a tick or a plus.
- Placeholder bars are filled, fully rounded (`rx` = height / 2), never stroked.

## 3 · Tokens

Every colour is written `var(--il-token, #fallback)`, so the file works standalone
and still themes. Use the light value as the fallback.

| Token | Light | Dark | Used for |
|---|---|---|---|
| `--il-canvas` | `#EDEAE6` | `#1A1918` | the host page behind the illustration |
| `--il-ghost` | `#EAE7E2` | `#1F1E1C` | backdrop sheets |
| `--il-panel` | `#F7F5F2` | `#262523` | base panel, gradient bottom |
| `--il-panel-top` | `#FCFBF9` | `#2E2C29` | base panel, gradient top |
| `--il-line` | `#B9B1A4` | `#5C564D` | **every stroke** |
| `--il-surface` | `#FFFFFF` | `#322F2B` | floating cards, medallion |
| `--il-stroke` | `#35322D` | `#DDD9D3` | primary icons — the only dark value |
| `--il-stroke-soft` | `#9B948A` | `#877F74` | secondary icons, avatars, kebabs |
| `--il-fill` | `#DCD6CE` | `#4A463E` | placeholder bars, "yes" dots |
| `--il-fill-soft` | `#E9E4DC` | `#35322D` | selected pill, `+N` chip |
| `--il-accent` | `#3E9077` | `#5FB694` | **at most two elements**, one meaning |
| `--il-shadow-c` | `#4A3F33` | `#000000` | shadow colour |
| `--il-shadow-o` | `0.16` | `0.55` | shadow opacity |

Want your brand's colours? Tint canvas, panel and surface 4–8% toward the brand
hue, keep `--il-fill` neutral, and use the brand colour only as `--il-accent`.
Everything else in this file stays the same. (`references/theme.md`)

## 4 · Boilerplate

Replace `ID` with the illustration's name everywhere (`fade-audit`, `lift-audit`)
— two illustrations on one page with the same ids will swap masks. **Keep every
def**: the panel fill is `url(#panelG-ID)`.

```svg
<svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="FEATURE NAME">
  <defs>
    <linearGradient id="fadeG-ID" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0.7" stop-color="#fff"/><stop offset="0.82" stop-color="#000"/>
    </linearGradient>
    <mask id="fade-ID"><rect width="160" height="160" fill="url(#fadeG-ID)"/></mask>
    <linearGradient id="panelG-ID" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="var(--il-panel-top, #FCFBF9)"/>
      <stop offset="1" stop-color="var(--il-panel, #F7F5F2)"/>
    </linearGradient>
    <filter id="lift-ID" x="-60%" y="-60%" width="220%" height="220%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.6"
        flood-color="var(--il-shadow-c, #4A3F33)" flood-opacity="var(--il-shadow-o, 0.16)"/>
    </filter>
    <filter id="liftL-ID" x="-60%" y="-60%" width="220%" height="220%">
      <feDropShadow dx="0" dy="4" stdDeviation="5"
        flood-color="var(--il-shadow-c, #4A3F33)" flood-opacity="var(--il-shadow-o, 0.16)"/>
    </filter>
  </defs>
  <g mask="url(#fade-ID)">
    <!-- backdrop, base panel and all panel content: these fade -->
  </g>
  <!-- the one floating element: outside the mask, never fades -->
</svg>
```

## 5 · Building blocks

Coordinates are for the default panel (`x 21 w 118 y 8`); move them with it.

```svg
<!-- base panel, fade: rounded top, open bottom. Width 104-134, sized to content. -->
<path d="M21 18a10 10 0 0 1 10-10h98a10 10 0 0 1 10 10V160H21z"
      fill="url(#panelG-ID)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
<!-- base panel, contained: closed, height fits content ("this is all of it") -->
<rect x="22" y="30" width="116" height="100" rx="10"
      fill="url(#panelG-ID)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>

<!-- backdrop (optional; vary it across a set). plate: x-7, y+4, w+14, rx 16 -->
<rect x="14" y="12" width="132" height="158" rx="16"
      fill="var(--il-ghost, #EAE7E2)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
<!-- offset: x+8, y+8, same w, rx 10. twin: two sheets, (x-10, y+10, w+20, rx 15)
     behind (x-5, y+5, w+10, rx 12). The panel is always the highest sheet. -->

<!-- floating card: surface fill, the line, the shadow. Area > 2600 takes liftL. -->
<g filter="url(#liftL-ID)">
  <rect x="11" y="24" width="138" height="27" rx="8"
        fill="var(--il-surface, #FFFFFF)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
</g>
<!-- header-card contents: 16px icon + short bar over long bar, both centred -->
<g transform="translate(27 29.5) scale(0.0625)" fill="var(--il-stroke, #35322D)"><path d="…"/></g>
<rect x="52" y="30.3" width="29" height="4.8" rx="2.4" fill="var(--il-fill, #DCD6CE)"/>
<rect x="52" y="38.7" width="58" height="6" rx="3" fill="var(--il-fill, #DCD6CE)"/>

<!-- chip: a small float (62-74 x 22, rx 8, lift) holding a 12px icon and one bar -->
<g filter="url(#lift-ID)">
  <rect x="18" y="14" width="74" height="22" rx="8"
        fill="var(--il-surface, #FFFFFF)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
</g>
<g transform="translate(27 19) scale(0.04688)" fill="var(--il-stroke, #35322D)"><path d="…"/></g>
<rect x="44" y="22.4" width="34" height="4.6" rx="2.3" fill="var(--il-fill, #DCD6CE)"/>

<!-- medallion: for a feature that is a *thing*. Flat by default; 15px icon. -->
<circle cx="80" cy="33" r="14"
        fill="var(--il-surface, #FFFFFF)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
<g transform="translate(72.5 25.5) scale(0.05859)" fill="var(--il-stroke, #35322D)"><path d="…"/></g>

<!-- list row: leader, then a bar pair. Pitch 20-22. -->
<g transform="translate(33 60) scale(0.05859)" fill="var(--il-stroke-soft, #9B948A)"><path d="…user-circle…"/></g>
<rect x="57" y="60.5" width="28" height="4.2" rx="2.1" fill="var(--il-fill, #DCD6CE)"/>
<rect x="57" y="67.9" width="52" height="5.2" rx="2.6" fill="var(--il-fill, #DCD6CE)"/>

<!-- separators are filled hairlines -->
<rect x="30" y="66" width="102" height="0.5" fill="var(--il-line, #B9B1A4)" opacity="0.8"/>
<rect x="84" y="48" width="0.5" height="76" fill="var(--il-line, #B9B1A4)" opacity="0.55"/>

<!-- dots: filled = yes / active, hollow = no -->
<circle cx="92" cy="76" r="3" fill="var(--il-fill, #DCD6CE)"/>
<circle cx="108" cy="76" r="3" fill="none" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>

<!-- tile: outlined with a centre dot, or filled with a third-party brand colour -->
<rect x="28" y="34" width="16" height="16" rx="5" fill="none"
      stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
<circle cx="36" cy="42" r="2.4" fill="var(--il-fill, #DCD6CE)"/>

<!-- pills: exactly one selected (a fill, no stroke); the rest outlined -->
<rect x="40" y="30.5" width="22" height="11" rx="5.5" fill="var(--il-fill-soft, #E9E4DC)"/>
<rect x="66" y="30.5" width="26" height="11" rx="5.5" fill="none"
      stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>

<!-- kebab: three dots r 1.15, 3.6 apart -->
<circle cx="124" cy="20.9" r="1.15" fill="var(--il-stroke-soft, #9B948A)"/>
<circle cx="124" cy="24.5" r="1.15" fill="var(--il-stroke-soft, #9B948A)"/>
<circle cx="124" cy="28.1" r="1.15" fill="var(--il-stroke-soft, #9B948A)"/>

<!-- rail: starts AT the first node's centre, may run past the last -->
<rect x="44" y="56" width="0.5" height="70" fill="var(--il-line, #B9B1A4)" opacity="0.7"/>
<circle cx="44" cy="56" r="3.6" fill="var(--il-accent, #3E9077)"/>
<circle cx="44" cy="80" r="3.6" fill="var(--il-fill, #DCD6CE)"/>

<!-- connector: the same stroke; dashed = configurable. Edge to edge, never under a card. -->
<path d="M44 42C53.5 42 53.5 63 63 63" fill="none"
      stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"
      stroke-dasharray="2.4 3" stroke-linecap="round"/>

<!-- cues (one per illustration): the Phosphor check or plus at 9, filled; or a cursor -->
<g transform="translate(X Y) scale(0.03516)" fill="var(--il-accent, #3E9077)"><path d="…check…"/></g>
<path d="M0 0l4.6 11.4 1.8-4.6 4.6-1.8z" fill="var(--il-accent, #3E9077)"/>
```

**Icons:** `<g transform="translate(X Y) scale(size/256)" fill="…"><path d="…"/></g>`
with a path from [`references/icons.md`](references/icons.md). Sizes: 16 header
card · 15 medallion · 12 chip · 10–13 inline. Never draw your own glyph.

**Padding inside every card is equal top and bottom** — about 8 in a content
card; a chip's 12px icon sits 5 from each edge. Check it with arithmetic:
`top = content_top - card_y`, `bottom = card_y + card_h - content_bottom`.

## 6 · Depth

- **At most one element casts a shadow** — the floating element. (L5's two
  diagonal chips count as one; a flat medallion layout may have none.)
- `lift` (dy 2, blur 2.6) for anything under ~2600 sq units, `liftL` (dy 4,
  blur 5) above. Opacity comes from `--il-shadow-o` — 16% in light. If you can
  see a dark edge under the card at display size, it is too strong.
- **Every card has the 0.5 line as well as its fill.** A shadow alone does not
  separate white from near-white at 160px.
- The float **overhangs** the panel decisively, 8–15 units, or not at all.
- One gradient only: the panel's. No blur, glow, gloss, bevel, perspective.

## 7 · Layouts

Pick by the feature's **relationship**, then by how many elements it needs
(1–2: L7 L8 L12 · 3–4: L1 L2 L3 L5 L11 · 4–6: L4 L6 L9 L10). In a set, no
layout more than twice in twelve, and at most two full-width header cards.

**Then open the example file and edit it.** Each is a finished, checked
illustration of its layout — all twelve are also in `references/examples.md`,
one file — or fetch one raw: `https://raw.githubusercontent.com/Devesh-Shirsath/spotkit/main/examples/<file>.svg`. Keep every coordinate of the
panel, backdrop, float and cards; rename the ids (`-approval` → `-yourname`);
swap the icon and the contents.

| | Layout | Start from | Panel (x, w, edge, backdrop) | Float | Content |
|---|---|---|---|---|---|
| L1 | Header + rows | `billing.svg` | 21, 118, fade, twin | header card 11,24 138×27 | 3 rows at y 60/81/102: 15px avatar + bar pair |
| L2 | Cascade | `teams.svg` | 25, 110, fade, offset | raised row 13,56 134×21 r7 + flat medallion | 2 receding rows, opacity .70 / .40 |
| L3 | Tab bar | `categories.svg` | 24, 112, fade, plate | card 11,24 138×24: icon + 4 pills | 3 rows at y 62/84/106 |
| L4 | Toolbar | `workspace.svg` | 22, 116, fade, none | card 11,24 138×26: 4 brand tiles + search | avatar cluster, rule, 3 rows with checks |
| L5 | Corner chips | `docs.svg` | 28, 104, fade, offset | chips 13,12 and 91,94, 58×21 | header bar + kebab, 4 rows |
| L6 | Window | `connectors.svg` | 13, 134, fade, chrome, twin | none — first row raised | 3 row cards 118×18 at y 34/56/78 |
| L7 | Fanned | `contributors.svg` | 16, 128, contained y44 h92, none | middle card 55,32 50×60 r11 | 2 flat side cards 46×50 |
| L8 | Notifications | `notifications.svg` | 26, 108, contained y30 h100, offset | card 16,44 112×34 r10 | 1 flat card behind, 92×32 |
| L9 | Constellation | `gateway.svg` | 21, 118, fade, plate | hub 63,46 34×34 r11, 18px icon | 4 tiles, dashed connectors to the hub |
| L10 | Matrix | `roles.svg` | 21, 118, fade, none | corner chip 13,16 62×22 | 3 icon columns × 4 avatar rows of dots |
| L11 | Timeline | `audit.svg` | 28, 104, fade, offset | column chip 18,14 74×22 | rail at x 44, nodes y 56/80/104 |
| L12 | Split | `approval.svg` | 22, 116, contained y30 h100, plate | flat medallion 80,37 r17 | 2 state cards 44×44, arrow in the gap |

A float that covers only one side of the panel's top edge gets answered on the
other side — a short bar and a kebab (L5, L11). Full detail: `references/archetypes.md`.

## 8 · A complete example

`examples/audit.svg` — L11, a timeline for an audit log. Copy its structure.

```svg
<svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Audit log" class="il">
  <defs>
    <linearGradient id="fadeG-audit" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0.7" stop-color="#fff"/><stop offset="0.82" stop-color="#000"/>
    </linearGradient>
    <mask id="fade-audit"><rect width="160" height="160" fill="url(#fadeG-audit)"/></mask>
    <linearGradient id="panelG-audit" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="var(--il-panel-top, #FCFBF9)"/>
      <stop offset="1" stop-color="var(--il-panel, #F7F5F2)"/>
    </linearGradient>
    <filter id="lift-audit" x="-60%" y="-60%" width="220%" height="220%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.6"
        flood-color="var(--il-shadow-c, #4A3F33)" flood-opacity="var(--il-shadow-o, 0.16)"/>
    </filter>
    <filter id="liftL-audit" x="-60%" y="-60%" width="220%" height="220%">
      <feDropShadow dx="0" dy="4" stdDeviation="5"
        flood-color="var(--il-shadow-c, #4A3F33)" flood-opacity="var(--il-shadow-o, 0.16)"/>
    </filter>
  </defs>
  <g mask="url(#fade-audit)">
    <!-- offset backdrop, then a narrow 104-wide panel: a timeline is a column -->
    <rect x="36" y="16" width="104" height="152" rx="10" fill="var(--il-ghost, #EAE7E2)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
    <path d="M28 18a10 10 0 0 1 10 -10h84a10 10 0 0 1 10 10V160H28z" fill="url(#panelG-audit)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
    <!-- rail from the first node down past the last; newest event accented -->
    <rect x="44" y="56" width="0.5" height="70" fill="var(--il-line, #B9B1A4)" opacity="0.7"/>
    <circle cx="44.0" cy="56.0" r="3.6" fill="var(--il-accent, #3E9077)"/>
    <circle cx="44.0" cy="80.0" r="3.6" fill="var(--il-fill, #DCD6CE)"/>
    <circle cx="44.0" cy="104.0" r="3.6" fill="var(--il-fill, #DCD6CE)"/>
    <!-- a short-over-long bar pair per event -->
    <rect x="58.0" y="49.0" width="22.0" height="4.2" rx="2.10" fill="var(--il-fill, #DCD6CE)"/>
    <rect x="58.0" y="56.4" width="50.0" height="5.2" rx="2.60" fill="var(--il-fill, #DCD6CE)"/>
    <rect x="58.0" y="73.0" width="22.0" height="4.2" rx="2.10" fill="var(--il-fill, #DCD6CE)"/>
    <rect x="58.0" y="80.4" width="50.0" height="5.2" rx="2.60" fill="var(--il-fill, #DCD6CE)"/>
    <rect x="58.0" y="97.0" width="22.0" height="4.2" rx="2.10" fill="var(--il-fill, #DCD6CE)"/>
    <rect x="58.0" y="104.4" width="50.0" height="5.2" rx="2.60" fill="var(--il-fill, #DCD6CE)"/>
    <!-- the chip covers the left of the top edge, so a bar and kebab answer it on the right -->
    <rect x="102.0" y="22.0" width="18.0" height="4.6" rx="2.30" fill="var(--il-fill, #DCD6CE)"/>
    <circle cx="124.0" cy="20.9" r="1.15" fill="var(--il-stroke-soft, #9B948A)"/>
    <circle cx="124.0" cy="24.5" r="1.15" fill="var(--il-stroke-soft, #9B948A)"/>
    <circle cx="124.0" cy="28.1" r="1.15" fill="var(--il-stroke-soft, #9B948A)"/>
  </g>
  <!-- the one float: a column chip, small shadow, 12px icon, one bar -->
  <g filter="url(#lift-audit)"><rect x="18.0" y="14.0" width="74.0" height="22.0" rx="8.0" fill="var(--il-surface, #FFFFFF)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/></g>
  <g transform="translate(27.00 19.00) scale(0.04688)" fill="var(--il-stroke, #35322D)"><path d="M136,80v43.47l36.12,21.67a8,8,0,0,1-8.24,13.72l-40-24A8,8,0,0,1,120,128V80a8,8,0,0,1,16,0Zm-8-48A95.44,95.44,0,0,0,60.08,60.15C52.81,67.51,46.35,74.59,40,82V64a8,8,0,0,0-16,0v40a8,8,0,0,0,8,8H72a8,8,0,0,0,0-16H49c7.15-8.42,14.27-16.35,22.39-24.57a80,80,0,1,1,1.66,114.75,8,8,0,1,0-11,11.64A96,96,0,1,0,128,32Z"/></g>
  <rect x="44.0" y="22.4" width="34.0" height="4.6" rx="2.30" fill="var(--il-fill, #DCD6CE)"/>
</svg>
```

## 9 · Before you answer

If you can run code, `python3 check.py your.svg` checks most of these. If not,
go through them yourself — each one is a failure people have actually shipped.

1. Every `stroke-width` is `0.5`; every `stroke` is `var(--il-line, #B9B1A4)`.
2. No icon, tick or plus is stroked. Icons are Phosphor paths from `icons.md`.
3. At most one element has a `filter` (L5's chip pair aside), and it uses
   `lift`/`liftL` unchanged.
4. No background rect, no `<text>`, no second gradient, no blur.
5. Every id carries the same `-name` suffix.
6. The fade stops are exactly `0.7` and `0.82`.
7. Every card's top padding equals its bottom padding, and bottom > 0.
8. Nothing crosses what it sits between: a glyph in a gap clears both sides by
   2+; a connector ends at the edges it joins; a rail starts at its first node.
9. The float overhangs 8–15 units or not at all; only the float breaks the panel.
   The composition is centred on x=80 and fills the square.
10. At most two accent-coloured elements. It still reads in grayscale.
11. Bars are short-over-long, never equal. Fewer than six content blocks.
    Nothing that carries meaning is under 9 units.
12. It reads as the feature with every label removed — and would never be
    mistaken for a screenshot.

## 10 · Other sizes and themes

- **Any display size:** keep the 160 viewBox and scale with CSS. Only author a
  bigger viewBox if you must, and then multiply every number by `size / 160`
  (a 320 viewBox has 1.0 strokes) and shadow blur by its square root.
  Wide and hero formats change the density — `references/scaling.md`.
- **Dark mode:** one file. Inline the SVG in the page and the tokens switch it.
  An SVG in `<img>` or Figma can't read CSS variables and shows the fallbacks —
  use the flat exports in `examples/flat/` there.

## 11 · Delivering

> **Feature interpretation** — one line on what it actually does.
> **Metaphor** — one line: the relationship shown.
> **Layout** — which of the twelve it adapts (or why none fit).
> **Primitives** — the 2–5 used.
> **The SVG.**

Don't pad it with explanation nobody asked for.
