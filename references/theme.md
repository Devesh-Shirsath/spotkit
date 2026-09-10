# Theme, tokens and color

## Principle

The style is **grayscale-first**. Color is a guest, not a resident. Every
illustration must still read correctly with saturation set to zero — if removing
color destroys the meaning, the composition is doing too little work.

You supply the values. The skill defines the *slots* and the *relationships*
between them; it does not impose a palette.

## Token slots

Eleven colour slots, plus two for the shadow. Every primitive references these
and nothing else.

| Token | Role | Constraint |
|---|---|---|
| `--il-canvas` | Behind everything | Lightest surface in light mode, darkest in dark mode |
| `--il-ghost` | Plate behind the panel | Barely off `--il-canvas` |
| `--il-panel` | Base panel fill (gradient bottom) | Clearly above `--il-canvas` |
| `--il-panel-top` | Base panel fill (gradient top) | ~2% lighter than `--il-panel` |
| `--il-line` | **Every stroke in the system** | One colour for all line work — panels, cards, tiles, connectors, chrome |
| `--il-surface` | Floating cards | Highest contrast against `--il-panel`. This is what pops forward. |
| `--il-stroke` | Icon fill | Only genuinely dark value. Use sparingly. |
| `--il-stroke-soft` | Secondary icons, avatars, kebabs | ~50% toward the panel from `--il-stroke` |
| `--il-fill` | Placeholder bars | Neutral gray, deliberately *not* tinted like the surfaces |
| `--il-fill-soft` | Selected pills, the `+N` chip | ~40% lighter than `--il-fill` |
| `--il-accent` | Optional single accent | See rules below |

Plus two for the shadow, split so SVG `feDropShadow` can theme them:
`--il-shadow-c` (color) and `--il-shadow-o` (opacity).

## The relationships that actually matter

Get these right and almost any palette works:

1. `canvas` → `panel` must be **visible but quiet**. Earlier versions of this
   system made it a whisper, and the result was that nothing separated at
   display size. You should be able to see where the panel starts without
   looking for it.
2. `panel` → `surface` is the **only real step**. The floating card must read as
   lifted before the shadow is even applied.
3. `stroke` is the **only dark value**, and it appears in perhaps 3% of pixels.
4. `fill` (placeholder bars) is **neutral**, even when the surfaces are warm or
   cool. This deliberate mismatch is what makes the bars read as *content* rather
   than as *chrome*. It is a real technique, not an oversight.
5. **`--il-line` is a single value used by every stroke**, at width 0.5, always. It
   has to work on the canvas, on the panel *and* on a white card — pick it by
   testing all three, not just one. Differentiation between a panel edge and a
   card edge comes from the fills either side of the line, not from the line.

## The shipped preset

One preset ships today — the values `assets/illustration.css` uses.
It is a starting point, not a house style; the section below shows how to
derive your own without breaking the relationships above.

### Light
```css
  --il-canvas:       #EDEAE6;
  --il-ghost:        #EAE7E2;
  --il-panel:        #F7F5F2;
  --il-panel-top:    #FCFBF9;
  --il-line:         #B9B1A4;
  --il-surface:      #FFFFFF;
  --il-stroke:       #35322D;
  --il-stroke-soft:  #9B948A;
  --il-fill:         #DCD6CE;
  --il-fill-soft:    #E9E4DC;
  --il-accent:       #3E9077;
  --il-shadow-c:     #4A3F33;
  --il-shadow-o:     0.16;
```

### Dark
```css
  --il-canvas:       #1A1918;
  --il-ghost:        #1F1E1C;
  --il-panel:        #262523;
  --il-panel-top:    #2E2C29;
  --il-line:         #5C564D;
  --il-surface:      #322F2B;
  --il-stroke:       #DDD9D3;
  --il-stroke-soft:  #877F74;
  --il-fill:         #4A463E;
  --il-fill-soft:    #35322D;
  --il-accent:       #5FB694;
  --il-shadow-c:     #000000;
  --il-shadow-o:     0.55;
```

## Deriving a palette from a brand color

Do **not** tint the whole system with the brand hue. Instead:

1. Take the brand hue. Desaturate it to **4–8%** and use it for `canvas`,
   `panel`, and `surface` — enough to feel related, not enough to read as colored.
2. Keep `fill` fully neutral.
3. Use the brand color at **full saturation only for `--il-accent`**, and only if
   the accent rules below permit it.

## Dark mode is not an inversion

Flipping the values mechanically destroys the hierarchy. Two things change
character:

- **Surfaces get lighter as they come forward.** In light mode the floating card
  is brighter than the panel; in dark mode it is *also* brighter — lighter, not
  darker. Elevation always means "closer to light."
- **Warm darks go olive if you let them.** A warm near-black drifts toward yellow-green as it lightens. Keep the blue channel within a few points of the green one on every dark surface.
- **Shadows do less work; borders do more.** A soft shadow on near-black is
  nearly invisible, so `--il-line` has to carry more of the separation in dark
  mode. Raise shadow alpha and shrink its blur to compensate.

Placeholder bars must stay clearly *below* surface brightness in dark mode. A
common failure is bars that glow brighter than the card holding them.

## Accent rules

If an accent is used at all:

- **At most two elements** in a single illustration carry it.
- It marks exactly one of: success, selection, active state, a live connection,
  or the primary action. Never decoration.
- It never touches structure — no accent panels, borders, or backgrounds.
- Preferred carriers: a single state dot, one checkmark, one filled pill, one
  connector line, one small button.
- Convert the result to grayscale mentally. If two elements become
  indistinguishable, the accent was carrying meaning it should not have been.

**Third-party brand marks are exempt.** When an illustration depicts external
services (integrations, connectors, marketplaces), those logos keep their real
colors. That color belongs to the logos, not to the illustration system, and it
does not count against the accent budget.

## Multi-color is a smell

If you reach for a third color, the composition is compensating for a weak
metaphor. Go back to `references/metaphor.md`.

## More presets

The dial system this preset sits inside — elevation model, edge treatment,
overhang, corner language, stroke weight, icon style, density — is deliberately
open. Additional named directions (flat outline with no shadow, high-contrast
elevated cards, mono/blueprint) are a planned addition; a new preset is a new set
of token values plus a note on which dials it moves, and nothing in
`archetypes.md` or `metaphor.md` changes when one is added.
