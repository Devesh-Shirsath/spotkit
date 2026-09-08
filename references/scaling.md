# Scaling beyond the square

The 160×160 square is the default and the reference format. It is a **spot
illustration** — for feature cards, docs sidebars, settings navigation, changelog
entries, empty states.

Other canvases need more than a resize. Density has to change with area, or the
illustration either looks empty or looks busy.

## The density budget

Count **content blocks**: a list row, a stack card, a matrix, a node, a state
card, a pill row. Structural elements (panel, floating card, medallion) do not
count.

| Canvas | Use for | Blocks | Floating elements | Rule |
|---|---|---|---|---|
| 96 × 96 | dense nav, inline | 2 | 1 | Drop the bar pair to a single bar. Icons only, no matrices. |
| **160 × 160** | **default spot** | **3** | **1** | The reference format. |
| 320 × 320 | feature cards | 4–5 | 1 (+1 small) | May add a second, much smaller floating chip. |
| 480 × 320 | wide feature blocks | 5–6 | 2 | Panel becomes landscape. Content may split into two columns. |
| 720 × 420 | landing hero | 6–8 | 2 | Panel becomes a window. A nav rail is permitted. |

Hard ceilings at every size: **never more than two floating elements**, **never
more than three distinct content patterns**, **never any text**.

## Scaling up correctly

Growing the canvas is not permission to add detail everywhere. Spend the extra
area in this order, stopping as soon as the composition feels resolved:

1. **More whitespace first.** Often a 320px illustration is a 160px illustration
   with more air, and that is the right answer.
2. **More instances** of a block you already have — a fourth list row before a
   new kind of element.
3. **One secondary floating element** — a small chip, a state badge, an inline
   callout. Much smaller than the primary, with a lighter shadow.
4. **One additional relationship** — a connector, a selection cue.
5. Only at 720px: a structural addition like a nav rail or a second column.

**The 0.5 stroke has a floor.** Below roughly 96px display width it drops under
half a device pixel and antialiases away to nothing. At those sizes either raise
the stroke to 0.75 for that size only — and say so, because it is a deliberate
break from the one-stroke rule — or drop the hairlines entirely and let fills
carry the whole composition. The second is usually better.

Stroke weights, corner radii and bar heights **scale proportionally** with the
canvas. An illustration at 320 uses 2.8px strokes where the 160 used 1.4. Do not
keep hairlines hairline as you scale up; the family will fracture.

The one exception: the **shadow does not scale linearly**. Increase blur by
roughly the square root of the scale factor. A 4× canvas gets a 2× blur, not 4×.

## Landscape

At 480×320 and wider, the panel turns from portrait to landscape and the bottom
fade weakens — a wide panel that dissolves looks broken rather than quiet.

- Reduce the fade to the bottom **12%** instead of 40%, or replace it with a
  bottom edge that simply runs off the canvas.
- The floating element still overhangs horizontally, but proportionally less:
  **1.08×** the panel width rather than 1.17×.
- Content may occupy two columns. Keep them unequal — roughly 60/40 — so the
  composition still has a subject.
- Center of gravity stays left of center; the right third stays quieter.

## Hero format

At 720×420 the illustration is doing marketing work, and the temptation is to
make it a product screenshot. Resist it — the fidelity ceiling does not rise with
the canvas. A hero in this style is a **spot illustration with more room**, not a
denser one.

Permitted only at this size:
- A vertical nav rail: a narrow strip of 4–5 dots or short bars, no labels.
- A second floating element on the opposite side of the primary.
- One large content region (a matrix, a stack, a graph) rather than several small
  ones.

Still forbidden: text, realistic data, secondary navigation, more than one accent.

## Non-square aspect ratios

Keep the **panel** proportional to the canvas, not fixed. The panel occupies
roughly **74% of canvas width** and starts **7.5% down** from the top in every
format. The floating element's vertical band stays at **12% → 40%** of canvas
height. Holding these three proportions is what keeps a 96px icon and a 720px
hero recognizably related.

## Export

Author once at 160×160 (or the format's native size) and scale with CSS or
`width`/`height` attributes. Because everything is vector and token-driven, one
file serves every display size and both themes.

For raster export, render at 3× and downsample. Hairlines at 1px will alias badly
if rasterized at 1×.
