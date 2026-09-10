# SVG primitive library

Everything is built from these. Don't invent a new shape when one of these fits.

Every number below was derived by measuring a working illustration family, then
verified by rendering. They are **defaults that are known to work together**, not
laws — but change one and check the whole set, because they are tuned as a group.

## Coordinate system

Author on a **160 × 160 viewBox** whatever size it will display at. Identical
dimensions across a family are most of what makes it read as a family.

```
viewBox="0 0 160 160"
```

Three zones:

| Zone | Bounds | Holds |
|---|---|---|
| **Bleed** | outer ~10px | Shadow spill only. Never draw here. |
| **Card lane** | x 11 → 149 | The floating element, *wider* than the panel |
| **Panel lane** | x 21 → 139 | The base panel and its contents |

## The constants

```
STROKE    0.5, var(--il-line), on every stroked element -- no second width
PANEL     x 21   w 118   y 8    radius 10   (width varies 104-134 with content)
CARD      x 11   w 138   y 24   h 27        radius 8
MEDALLION cx 80  cy 33   r 14
PAD       10 content inset from the panel edge
CPAD      8 inside a card -- top and bottom equal
FADE      starts 70% of canvas height (y 112), complete at 82% (y 131)
SHADOW    dy 2 blur 2.6, or dy 4 blur 5 above ~2600 sq units; opacity 0.16
ICON      16 header card · 15 medallion · 12 chip · 10-13 inline -- filled, never stroked
BARS      h 6 primary · 5 secondary · 4.4 tertiary
ROW PITCH 20-24
```

These mirror `GEO` in `build.py`, which generated every example. If this file
and `build.py` ever disagree, `build.py` is right — and `python3 check.py --docs`
fails until the doc is fixed.

The **ratios** are the portable part — they survive a change of canvas size:

| Relationship | Ratio |
|---|---|
| panel width : canvas | 0.74 |
| card width : panel width | **1.17** |
| card overhang, each side | 10 units |
| medallion diameter : panel width | 0.24 |
| list-row height : panel width | 0.15 |
| visible panel height : panel width | ≈ 1.0 (it reads square) |

The 1.17 overhang is the single most important number here. It is what makes the
composition read as layered rather than nested. Equalize the two and the whole
effect collapses.

## Boilerplate

```svg
<svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="FEATURE">
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
    ...base panel + all panel content...
  </g>

  ...the one floating element, unmasked, on top...
</svg>
```

Five things about this scaffold:

- **Keep every `def`**, even one you think you are not using. The panel fill is
  `url(#panelG-ID)`; delete that gradient and the panel renders with no fill.

- **No background rect.** The illustration sits on the host page, and the fade
  dissolves into it. An opaque canvas rect turns every illustration into a tile.
- The floating element sits **outside** the mask. It never fades.
- **Suffix every id** per illustration (`fade-teams`, `lift-teams`). Several of
  these on one page with shared ids will cross-apply masks and filters, and the
  failure looks like a rendering bug rather than an id collision.
- Colors are `var(--il-*, literal)` so the file works standalone and still themes.

---

## Structural primitives

### Base panel

**The panel is not a fixed box.** Size it to the content it holds, centre it on
x=80, and pick an edge treatment. A panel that is 118 wide every time makes every
illustration the same shape before you have drawn anything.

**Width** — content width + 2 × PAD. In practice 104–134. Let the content decide:
a timeline is a column, so its frame should be narrow; a table of wide rows needs
a wide one.

**Edge treatment** — pick by *meaning*, not convenience:

| Mode | Shape | Says |
|---|---|---|
| `fade` | rounded top, open bottom, dissolves | there is more |
| `contained` | closed on four sides, height fits content | this is all of it |

A two-state approval flow is complete — contain it. A list of connectors implies
more — fade it. Using `fade` for everything is another kind of monotony.

```svg
<!-- fade -->
<path d="M21 18a10 10 0 0 1 10-10h98a10 10 0 0 1 10 10V160H21z"
      fill="url(#panelG-ID)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
<!-- contained -->
<rect x="22" y="30" width="116" height="100" rx="10"
      fill="url(#panelG-ID)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
```

**Content must fit.** If rows spill past the panel on both sides it reads as a
bug, not as depth. Exactly one element — the designated float — may break the
bounds, and it should break them decisively (8–15 units), not by two.

### Backdrop

What sits behind the panel. **Optional**, and varied on purpose — an identical
plate behind every illustration is the fastest way to make a set look mechanical.

| Kind | What it is | Use when |
|---|---|---|
| `none` | nothing | the composition is already layered (fanned cards, a matrix) |
| `plate` | a larger rounded rect, inset −7 / +4 | the panel needs a floor |
| `offset` | a second sheet down and to the right | you want "there are more of these" |
| `twin` | two sheets stepping down and out | a stack seen edge-on |

For a panel at `x 21 w 118 y 8` (all inside the fade mask, drawn before the panel):

```svg
<!-- plate: x-7, y+4, w+14, radius 16 -->
<rect x="14" y="12" width="132" height="158" rx="16"
      fill="var(--il-ghost, #EAE7E2)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
<!-- offset: x+8, y+8, same width, radius 10 -->
<rect x="29" y="16" width="118" height="152" rx="10"
      fill="var(--il-ghost, #EAE7E2)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
<!-- twin: two sheets, 10 then 5 down and out, radius 15 then 12 -->
<rect x="11" y="18" width="138" height="152" rx="15"
      fill="var(--il-ghost, #EAE7E2)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
<rect x="16" y="13" width="128" height="152" rx="12"
      fill="var(--il-ghost, #EAE7E2)" stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
```

**No two sheets may share a top edge, and the panel is always the highest.** A
backdrop level with the panel does not read as depth — it reads as a mistake.
Each sheet steps down from the one in front (5, then 10) and widens to match, so
the front card is unambiguously the front card.

Keep any backdrop barely separated from the canvas. If you notice it before you
notice the panel, it is too strong.

### Window chrome and the balanced header

Three dots and a rule turn the panel into a recognizable surface, which in turn
licenses content that overflows its right edge.

Separately: **when the floating element covers only one side of the panel's top
edge, answer it on the other side.** A chip floating over the top-left of an
otherwise empty header leaves a visible hole. A short bar and a kebab at the
right closes it. This is the difference between a composition and an
arrangement.

This applies to **every** layout with a one-sided float, not just the ones where
it looks obviously wrong. Measure it: if the band between the float's far edge
and the panel's far edge is more than about **25 units**, it is a dead zone and
needs something in it.

Equally, **a float with a large empty band beneath it is too small or too high.**
If there is more than ~12 units of nothing between a medallion and the content it
introduces, grow the medallion and push it down. Empty space is structural in
this style, but only when it is doing something.

### Floating header card

```svg
<!-- 138 x 27 = 3726 sq units, so it takes the deeper shadow, liftL -->
<g filter="url(#liftL-ID)">
  <rect x="11" y="24" width="138" height="27" rx="8"
        fill="var(--il-surface, #FFFFFF)"
        stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
</g>
<!-- 16px icon, centred: 5.5 above and below -->
<g transform="translate(27 29.5) scale(0.0625)" fill="var(--il-stroke, #35322D)"><path d="…"/></g>
<!-- short bar over long bar, centred: 6.3 above and below -->
<rect x="52" y="30.3" width="29" height="4.8" rx="2.4" fill="var(--il-fill, #DCD6CE)"/>
<rect x="52" y="38.7" width="58" height="6"   rx="3"   fill="var(--il-fill, #DCD6CE)"/>
```

The short-over-long bar pair is the workhorse of the system. It reads as "title
and description" without a character of text. Vary the two widths — equal bars
read as a loading skeleton.

### Medallion

Alternative to the header card, for features about a *thing* rather than a
*record*.

```svg
<circle cx="80" cy="33" r="14"
        fill="var(--il-surface, #FFFFFF)"
        stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>
<g transform="translate(72.5 25.5) scale(0.05859)" fill="var(--il-stroke, #35322D)"><path d="…15px icon…"/></g>
```

A medallion and a header card are mutually exclusive.

**The medallion is usually flat.** When a composition has a medallion *and* a
prominent first row, the elevation belongs to the row, not the circle — the row
is the thing being acted on. Give the medallion a border only and let the row
carry the shadow and the overhang. Getting this backwards is a common and
surprisingly visible mistake.

### Ghost plate

A faint bordered plate behind the panel, drawn first and inside the fade mask —
the `plate` backdrop above.

Borrowed from bento layouts. It gives the composition a floor to sit on, which is
most of why those designs read as deep rather than flat. It needs **both** a fill
and a hairline — fill alone reads as a flat slab rather than a surface, and the
edge is what makes it intentional.

Keep it barely separated from the canvas. If you notice it before you notice the
panel, it is too strong.

---

## Three defects that ship silently

All three were found by people using the output, not by looking at it. They share
a property: the eye skims past them at 160px and they only become obvious once
someone stares at one illustration at full size. Check them by **arithmetic**.

`build.py` provides guards that raise at build time rather than let these
through — use them instead of trusting a coordinate.

### 1 · A glyph between two elements must fit inside the gap

An arrow between two cards, a plus between two panels, a divider between two
tiles. If the glyph is wider than the gap it crosses the neighbours' strokes,
and that reads as a rendering bug rather than a design choice.

```python
x = fits(left_card_right, right_card_left, glyph_size, 'flow arrow')
```

`fits()` returns the centred x and **raises** if the glyph needs more room than
the gap has, with clearance of 2 units each side. A real failure:

```
flow arrow is 12 wide and needs 16.0 of room,
but the gap 76..84 is only 8. Widen the gap or shrink the glyph.
```

The fix is nearly always to widen the gap, not shrink the glyph — a glyph small
enough to squeeze into 8 units is too small to read.

### 2 · A rail is capped by its first node

A timeline rail that starts above its first dot leaves a 2-unit stub poking out
of the top. Two units. Invisible in a contact sheet, obvious at full size, and it
makes the whole thing look unfinished.

```python
b += rail(x, [56, 80, 104])      # starts at the first node's centre
```

The rail **may** run past the last node — that tail says "and more" and is the
point of the fade. Only the top end is capped. Asymmetric on purpose.

### 3 · Content must not touch a card's bottom edge

See below. `padded(card_y, card_h, content_top, content_bottom)` raises on both
overflow and lopsided padding.

## Padding inside a card

**Top and bottom padding must be equal.** This is the single most common defect
in this system and it is invisible until you look for it: content is laid out
from the top of a card downward, the last element lands on or past the bottom
edge, and the card reads as broken even though nothing is obviously wrong.

Use `CPAD` (8) top and bottom. Audit it arithmetically rather than by eye:

```python
top = content_top - card_y
bot = (card_y + card_h) - content_bottom     # must be > 0 and ~= top
```

Real numbers from a version of this set that shipped looking fine:

| | top | bottom |
|---|---|---|
| fanned side card | 6.5 | **−0.2** — content hung outside the card |
| split state card | 10.0 | **3.0** |
| referral card | 6.5 | **0.3** |

When you add an element to a card, grow the card. Do not absorb it into the
bottom padding.

## Elevation

**Two shadow levels, not one.** A 58×21 chip and a 50×58 raised card carrying the
same shadow reads as a sticker sheet rather than a stack.

```svg
<filter id="lift-ID">   <feDropShadow dx="0" dy="2" stdDeviation="2.6" …/></filter>
<filter id="liftL-ID">  <feDropShadow dx="0" dy="4" stdDeviation="5"   …/></filter>
```

Objects over roughly 2600 square units take the deeper one — the 138 × 27 header
card is 3726, so it is `liftL`; a 62 × 22 chip is 1364, so it is `lift`. Still
only **one element per illustration** casts any shadow (the corner-chip pair in
L5 counts as one) — the two levels exist so that element is lit correctly for
its size, not so you can light several.

The shadow is soft on purpose: 16% opacity, warm, a few units of blur. If you can
see a dark edge under the card at display size, it is too strong.

## One stroke

Every stroke in every illustration is `stroke-width="0.5"` and
`stroke="var(--il-line)"`. There is no second width and no second colour.

```bash
grep -oh 'stroke-width="[^"]*"' examples/*.svg | sort -u   # must be one line
grep -oh 'stroke="[^"]*"'       examples/*.svg | sort -u   # must be one line
```

**The line is darker than a UI border would be, on purpose.** At half a unit it
antialiases to roughly half its own value at typical display sizes, so a border
colour picked by eye against a solid swatch will vanish once drawn. Pick it by
looking at the rendered illustration, not at the hex.

Below about 96px display width, 0.5 becomes unreliable — see `scaling.md`.

Hierarchy comes from **fills, opacity and elevation** — never from line weight.
A set with five stroke widths looks hand-assembled however good the individual
pieces are, and it is the single fastest way to lose the "custom made" quality.

Three consequences worth knowing:

- **Separators are fills, not strokes.** A `<rect>` of the same 0.5 height, with
  a fill, gives a hairline without adding a second stroke spec. Opacity does the
  softening a thinner line would.
- **Not everything needs an outline.** A selected pill is a fill. A logo tile is
  a fill. An avatar is an icon. Strokes are for *structure* — panels, cards,
  containers, connectors — and nothing else. If you are stroking something
  merely to make it visible, give it a fill instead.
- **Avatar clusters are spaced, not overlapped.** An overlapping cluster needs a
  surface-coloured knockout ring to stay legible, and that ring is a second
  stroke colour. Spacing them costs nothing and keeps the rule intact.

## Contrast

The single most common failure in this style is making everything so quiet that
nothing separates — especially in light mode.

An illustration at 160px has **no text to carry hierarchy**, so the surfaces have
to do it alone. The steps between canvas → ghost → panel → surface are therefore
deliberately wider here than a real product UI would use. Three rules:

1. **Every card gets a hairline.** In light mode a soft shadow alone does not
   separate white-on-near-white at this scale. The border is what makes the edge
   legible; the shadow only says which way is up.
2. **Placeholder bars must be clearly darker than the card holding them** — in
   both themes. Bars that glow brighter than their card is the classic dark-mode
   failure.
3. **Squint at it.** If the composition collapses into one flat shape, raise the
   steps before you add anything.

---

## Content primitives

### Placeholder bar

The only way text is ever represented.

```svg
<rect x="X" y="Y" width="W" height="5" rx="2.5" fill="var(--il-fill, #DCD6CE)"/>
```

Radius is always half the height — bars are fully rounded.

### List row

Leader glyph, then a bar pair. Row pitch 20–21, leader 15×15.

```svg
<rect x="33" y="60" width="15" height="15" rx="5" fill="#C25E3E"/>   <!-- logo tile -->
<rect x="57" y="60.5" width="28" height="4.2" rx="2.1" fill="var(--il-fill, #DCD6CE)"/>
<rect x="57" y="67.9" width="52" height="5.2" rx="2.6" fill="var(--il-fill, #DCD6CE)"/>
```

Leader variants: a **logo tile** (rounded square, the one place real brand color
is allowed) for external services; an **avatar** — the Phosphor `user-circle`
icon at 15, in `--il-stroke-soft` — for people; a **line icon** for records.

### Receding stack

Cards marching down and back. For features about *assembling* or *collecting*.

| Card | Width | Height | Opacity |
|---|---|---|---|
| 1 (front) | 138 | 18–27 | 1.00 |
| 2 | 99 | 15–22 | 0.70–0.85 |
| 3 | 77 | 12–16 | 0.45–0.50 |

All centered on x=80. Scale the contents by `width / 138` — a full-size icon in
card 3 destroys the illusion instantly.

Whether card 1 is the *floating* element or just the first stacked card is a real
choice: float it when the feature is about acting on one item, keep it flat when
the feature is about the collection.

### Matrix

Permissions, capability grids, plan comparisons. Column headers are 10px icons;
cells are dots — **filled means yes, hollow means no**.

```svg
<!-- column rules and the header rule are filled hairlines, not strokes -->
<rect x="84" y="48" width="0.5" height="76" fill="var(--il-line, #B9B1A4)" opacity="0.55"/>
<rect x="30" y="66" width="102" height="0.5" fill="var(--il-line, #B9B1A4)" opacity="0.8"/>
<circle cx="92" cy="76" r="3" fill="var(--il-fill, #DCD6CE)"/>              <!-- yes -->
<circle cx="108" cy="76" r="3" fill="none"
        stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>              <!-- no -->
```

Column rules at x 84 / 100 / 116 / 132, cells at x 92 / 108 / 124, column-head
icons at 11 in `--il-stroke-soft`, rows from y=76 at pitch 13. **Max 4 × 4** — beyond
that it stops being a metaphor and becomes a spreadsheet.

Make the fill pattern look *deliberate*. A viewer should sense a rule: give one
row visibly more filled dots than the others so it reads as levels of access.
Random-looking cells read as noise.

### Connector

Relationships between nodes. Dashed for configurable, solid for established.
A connector is structure, so it uses **the** stroke — same width, same colour —
like everything else.

```svg
<path d="M44 42C53.5 42 53.5 63 63 63" fill="none"
      stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"
      stroke-dasharray="2.4 3" stroke-linecap="round"/>
```

A single gentle cubic reads better than orthogonal elbows at this scale. Start
and end it at the edges of the two things it joins — it never runs under a card
or across a row. Never cross two connectors. More than four and the metaphor is
too literal.

### Pill / tab

```svg
<rect x="40" y="30.5" width="22" height="11" rx="5.5"
      fill="var(--il-fill-soft, #E9E4DC)"/>                                  <!-- selected -->
<rect x="66" y="30.5" width="26" height="11" rx="5.5" fill="none"
      stroke="var(--il-line, #B9B1A4)" stroke-width="0.5"/>                  <!-- the rest -->
```

The selected pill is a **fill with no stroke**; unselected ones are an outline at
the single stroke spec. Exactly one selected per strip — that is the whole point
of a tab bar. Inside each, a 2.8-tall bar: `--il-stroke-soft` in the selected
one, `--il-fill` in the others.

### Avatar cluster

A row of circles with a `+N` chip. Reads as "a group" faster than any icon.

```svg
<circle cx="41" cy="66" r="6.2" fill="#C25E3E" opacity="0.7"/>
<!-- next at cx + 14.8 (2r + 2.4), then a --il-fill-soft circle holding a
     6.4 x 2.8 --il-stroke-soft bar for the count -->
```

Spaced, not overlapped — see **One stroke** above for why. Keep the fills at
~0.7 opacity so four of them do not out-shout the composition.

### Window chrome

Three dots and a rule at the top of the panel. Turns the panel from an abstract
container into a recognizable surface — which in turn licenses content that
overflows past its right edge.

```svg
<!-- panel at x 13 w 134 y 8: dots at panel x + 10, then + 5.5 and + 11 -->
<circle cx="23" cy="17" r="1.7" fill="var(--il-line, #B9B1A4)"/>
<rect x="13" y="24" width="134" height="0.5" fill="var(--il-line, #B9B1A4)" opacity="0.55"/>
```

### Kebab menu

```svg
<!-- three 1.15r dots, 3.6 apart, in --il-stroke-soft -->
```

Cheap and effective at the right edge of a row: it says "each of these has
actions" without drawing any.

### Interaction cues

At most **one** per illustration.

Cues are **filled shapes**, never strokes — a stroked plus or tick is a second
stroke width and immediately looks hand-drawn next to the Phosphor glyphs.

```svg
<!-- check: the Phosphor `check` icon at 9, in the accent -->
<g transform="translate(X Y) scale(0.03516)" fill="var(--il-accent, #3E9077)"><path d="…check…"/></g>
<!-- plus: the Phosphor `plus` icon, same treatment, in --il-stroke -->
<g transform="translate(X Y) scale(0.03516)" fill="var(--il-stroke, #35322D)"><path d="…plus…"/></g>
<!-- cursor: a filled arrow -->
<path d="M0 0l4.6 11.4 1.8-4.6 4.6-1.8z" fill="var(--il-accent, #3E9077)"/>
```

A cue in the accent counts against the accent budget (two elements, at most).

---

## Icons

Icons come from **[Phosphor](https://phosphoricons.com)** (MIT). Two things about
using them here differ from normal web usage:

- **They are filled paths on a 256 grid, not strokes.** Set `fill`, never
  `stroke`. Scale by `size / 256`.
- **Use the `regular` weight** (16/256). Bold reads heavy against 0.5-unit
  structural strokes — the icons end up shouting over the panels and cards they
  sit on. Regular sits at roughly the same optical weight as the rest of the
  line work, which is the point.

```svg
<g transform="translate(27 29.5) scale(0.0625)" fill="var(--il-stroke, #35322D)">
  <path d="…phosphor regular path…"/>
</g>
```

Sizes: **16** in a header card · **15** in a medallion · **12** in a chip ·
**10–13** inline in rows and matrix headers.

**`references/icons.md` has paste-ready paths for 54 icons** (generated from
`icons.py`). Copy the path; never redraw a glyph. For anything missing, take
the regular-weight SVG from phosphoricons.com, or:

```
https://cdn.jsdelivr.net/npm/@phosphor-icons/core@2.1.1/assets/regular/<name>.svg
```

| Concept | Phosphor name |
|---|---|
| Docs / guides | `book-open` |
| Code / API | `brackets-curly` |
| Integration | `plugs-connected` |
| Security | `shield-check` |
| Access / permissions | `lock-key` |
| Person / avatar | `user-circle` |
| Group / team | `users-three` |
| Package / product | `cube` |
| Organization | `buildings` |
| Category / tag | `tag` |
| Layers / collections | `stack` |
| Notification | `bell` |
| Billing | `receipt` |
| Routing / gateway | `tree-structure` |
| Record / document | `file-text` |
| Edit | `pencil-simple` |
| Search | `magnifying-glass` |
| Versions / history | `clock-counter-clockwise` |
| Approved | `check-circle` |
| Add | `plus` |
| Inventory / shipment | `package` · `truck` · `barcode` |
| Store / marketplace | `storefront` |
| Payments / money | `currency-circle-dollar` · `bank` |
| Data / storage | `database` |
| Settings | `gear` |
| Filter / segment | `funnel` |
| Workflow / pipeline | `path` · `arrows-clockwise` |
| Web / region | `globe` |
| Messages / comments | `chat-circle` |
| Tickets / support | `ticket` |

Using one icon family across the whole set is most of what makes a family cohere.
Don't mix Phosphor with hand-drawn glyphs.

## Theming caveat — inline the SVG

CSS custom properties **do not cross document boundaries**. An SVG loaded through
`<img src="x.svg">`, `<object>`, or `background-image` renders in its own document
and will only ever show the literal fallback values — it will not follow your
theme, and it will not switch to dark mode.

To theme an illustration, **inline the SVG markup** into the page. That is why
`examples/gallery.html` inlines rather than links, and why every `id` has to be
suffixed per illustration.

If you must use `<img>` (a README, an email, a CMS field), accept that you are
shipping the fallback palette and generate a separate file per theme for that
surface only.

## What never appears

Gloss. Bevels. Blur beyond the one shadow. Perspective. Isometric grids. Shadows
on more than one element. Text. Realistic data. Decorative particles. More than
one accent hue.

**Gradients:** exactly one is permitted — the structural vertical gradient on the
base panel, spanning about 2% of lightness. Never on content, never on a card,
never more than one per illustration.
