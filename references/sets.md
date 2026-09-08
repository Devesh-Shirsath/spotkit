# Producing a family

One illustration is easy. Twenty that look like one system is the actual problem.

## Lock the spec after the first one

Once the first illustration is approved, write down what it decided and treat it
as fixed:

```
canvas       160 x 160
panel        x 21 w 118, top y 8, radius 10, hairline 1
float        138 wide (1.17x panel), y 24, h 27, radius 8, shadow dy 3 blur 3.4
medallion    cx 80 cy 33 r 14, flat unless it is the only element
icon         15 in card / 14 in medallion / 10-12 inline, stroke 1.4, round caps
bars         6 / 5 / 4.4, always short-over-long, never equal widths
row pitch    20-24
fade         69% -> 80% of canvas height
palette      <token values>
accent       <color or none>, meaning: <one meaning>
```

Restate it to yourself before each new illustration. Drift is gradual and
invisible until you see all twenty together, at which point it is expensive.

## Vary concept, never style

**Must not change** across a family:

stroke weight · corner radii · shadow · panel geometry · bar heights · row pitch ·
fade depth · icon size and weight · palette · accent meaning · abstraction level

**Should change:**

archetype · icon · content pattern · which relationship is shown · whether a cue
appears

**This is where sets go wrong.** Every piece individually fine, and the set
reads as one image repeated, because everything landed on the easiest layout —
header card, then rows.

Budget it: **no layout more than about twice in twelve**. If you have reached for
L1 a third time, the feature's relationship probably is not "many of one thing";
you defaulted. Go back to `metaphor.md`.

Neighbours matter most. Two features adjacent in the product's navigation must
get different layouts even when one would fit both — adjacency is where
repetition is actually noticed.

## Order the work

1. Draw the **two or three hardest** features first — the ones whose metaphors
   are least obvious. They stress the system and expose missing primitives while
   changing it is still cheap.
2. Get those approved.
3. Batch the rest; most will be straightforward.
4. Review the whole set together, both themes, at true display size.

Do not start with the easy ones. A system tuned on easy features breaks on hard
ones.

## The contact sheet

Before delivering, render everything in one grid, light and dark, at real display
size. This is not optional — it is the only view where family problems show up.

Look for:

- One illustration noticeably **darker or busier**. Usually too many strokes.
- **Optical weight clustering.** Two matrices side by side look heavier than two
  list illustrations; separate them in the ordering.
- **Repeated icons.** Two features sharing an icon means one metaphor is
  underdeveloped.
- **Accent drift.** The accent should appear in a minority of the set and always
  mean the same thing. If it is everywhere, it means nothing.
- **A wandering fade line.** Every bottom should dissolve at the same height.
- **Inconsistent overhang.** All floating elements at 1.17x, or none.

`examples/gallery.html` is a working contact sheet; copy its structure.

## Adding to an existing family

When extending a set drawn earlier, possibly by someone else:

1. **Measure before drawing.** Open two or three existing files and read off the
   real geometry and token values. Do not assume they match this skill's
   defaults — the family's own conventions win.
2. Note which archetypes are already used, and how often.
3. Note the icon inventory so you do not repeat one.
4. Draw the new illustration.
5. Place it in the contact sheet **between two existing ones** and confirm it does
   not stand out.

If the existing set breaks one of this skill's rules — two accents, no fade,
whatever — follow the existing set. Internal consistency beats conformance to
this document.

## Naming and delivery

Name files after the feature, kebab-case, no theme suffix:
`role-permissions.svg`, not `role-permissions-light-v2-final.svg`.

**Themes come from tokens on one file, not from two files.** Shipping
`x-light.svg` and `x-dark.svg` doubles maintenance and guarantees they drift.
Ship one file and let the CSS theme it.

## Generating a set programmatically

For a family beyond about eight illustrations, write a small generator rather
than hand-authoring each SVG — one script holding the constants, with a function
per illustration. `build.py` in this skill is a working example.

The payoff is not typing speed. It is that changing one constant moves the whole
family together, which is exactly the operation you will want repeatedly and the
one that is most error-prone by hand.
