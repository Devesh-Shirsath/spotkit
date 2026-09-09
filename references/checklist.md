# Quality checklist

Run this before delivering. Anything that fails gets simplified — the fix is
almost always removal.

## Concept

- [ ] Can a stranger describe the *relationship* from the image alone?
- [ ] Is there exactly **one** visual idea, not two competing?
- [ ] Would it still be correct if the feature were renamed tomorrow?
- [ ] Is the metaphor stronger than a literal reproduction would be?
- [ ] Does it avoid non-software allegory — no bridges, rockets, lightbulbs?

## Restraint

- [ ] **Zero text.** No labels, no numbers, no realistic copy.
- [ ] At most **one** interaction cue.
- [ ] At most **two** accent-colored elements — ideally one, often zero.
- [ ] Fewer than **six** content blocks.
- [ ] At most **two** distinct icons, excluding third-party logos.
- [ ] Panel no more than ~60% covered.

## Visual language

- [ ] **One stroke width (0.5) and one stroke colour in the whole file.** Verify:
      `grep -oh 'stroke-width="[^"]*"' *.svg | sort -u` returns one line,
      and the same for `stroke="…"`.
- [ ] Separators are filled hairlines, not strokes.
- [ ] Nothing is stroked merely to make it visible — that is a fill's job.
- [ ] One corner-radius language.
- [ ] Exactly **one** element casts a shadow, at the elevation matching its size.
- [ ] The panel has **no bottom edge**; contents fade downward with it.
- [ ] Only the designated float breaks the panel bounds — content does not spill.
- [ ] Where the float breaks out, it does so decisively (8–15 units), not by two.
- [ ] If the float covers one side of the panel's top edge, something answers it on the other side.
- [ ] The elevation is on the right element — usually the record being acted on,
      not the decorative circle above it.
- [ ] At most one gradient, structural, on the base panel only.
- [ ] No gloss, bevel, 3D, or glassmorphism.
- [ ] Every card has a hairline, not just a shadow.
- [ ] **Nothing placed in a gap crosses its neighbours' strokes.** Use `fits()`.
- [ ] **No rail, connector or line protrudes past its first node.** Use `rail()`.
- [ ] No dead band wider than ~25 units beside a one-sided float.
- [ ] No empty band deeper than ~12 units under a medallion.
- [ ] Outer ~10px empty except for shadow spill.

## Color

- [ ] Convert to grayscale mentally. Does it still read?
- [ ] Squint at it. Does it collapse into one flat shape?
- [ ] Are placeholder bars neutral rather than tinted like the surfaces?
- [ ] Is the floating surface clearly brighter than the panel in **both** themes?
- [ ] In dark mode, are bars clearly darker than the card containing them?
- [ ] Does the accent carry exactly one meaning?

## Fidelity

- [ ] Roughly 20–40% of the real UI's detail. No more.
- [ ] No sidebar, breadcrumb, pagination, toolbar, or overflow menu.
- [ ] No more than 4 rows and 4 columns anywhere.
- [ ] Nothing so small it vanishes at final display size.
- [ ] Nothing important sits below `y=112` — the fade eats it.

## Family

- [ ] Geometry identical to its siblings.
- [ ] Layout differs from its immediate neighbours.
- [ ] Panel is sized to its content, not defaulted to the same width again.
- [ ] **Every card: top padding == bottom padding, and bottom padding > 0.**
      Check by arithmetic, not by eye — this fails silently and constantly.
- [ ] No backdrop sheet shares a top edge with the panel; the panel is highest.
- [ ] Backdrop varies across the set — not the same plate twelve times.
- [ ] Edge treatment chosen by meaning: `fade` = there is more, `contained` = this is all of it.
- [ ] No layout used more than twice in a set of a dozen.
- [ ] **No more than two full-width header cards in twelve.** Count them.
- [ ] The float earns its place — it says something the content does not.
- [ ] Layout matches the element count — not 2 things in a matrix, not 6 in a two-card split.
- [ ] Icon not already used elsewhere in the set.
- [ ] Optical weight comparable to the rest.
- [ ] Fade line at the same height as every sibling.

## Technical

- [ ] `viewBox` present; no baked-in `width`/`height`.
- [ ] All colors are `var(--il-*, literal)`.
- [ ] Every `id` suffixed per illustration — shared ids cross-apply masks and
      filters between illustrations on the same page.
- [ ] No opaque background rect.
- [ ] Icons are Phosphor **regular**, filled not stroked.
- [ ] If it must theme, it is **inlined** — `<img>` and `<object>` render fallbacks only and will never follow dark mode.
- [ ] `role="img"` and a meaningful `aria-label`.
- [ ] Checked at the **smallest** intended size, not just zoomed in.

## The two that matter most

> Does someone understand what this feature does?

> Would someone mistake this for a screenshot?

The first must be yes. The second must be no.
