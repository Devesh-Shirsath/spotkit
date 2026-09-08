# Image-model prompts (fallback path)

Use this **only** when the user explicitly asks for a prompt for an external
image model, or wants something SVG genuinely cannot express.

## Say this once, plainly

Diffusion models are weak at exactly what defines this style: hairline borders,
exact corner radii, repeated placeholder bars, uniform stroke weight, and above
all **consistency across a set**. Twenty illustrations generated this way will
not look like one family, and any text the model invents will be garbled.

One sentence of that when handing over a prompt. Don't belabour it.

## Structure

Order matters — image models weight early tokens more heavily.

```
[SUBJECT + METAPHOR]
[COMPOSITION AND LAYERING]
[2-5 UI PRIMITIVES, CONCRETE]
[STYLE AND FIDELITY]
[COLOR]
[THEME]
[NEGATIVE CONSTRAINTS]
```

Write it as instructions to a renderer, not prose to a person. No "this
illustration represents…" — just the description.

## Template

> Minimal abstract UI illustration of [CONCEPT]. A large rounded rectangular
> panel with a thin light-gray border and softly rounded top corners, its lower
> portion fading gently into the background with no bottom edge. One white card
> floats over the panel's upper area, slightly wider than the panel and
> overlapping both its left and right edges, casting a single soft shadow; the
> card holds a small line icon of [ICON] and two rounded gray placeholder bars,
> one short above one long. Below, inside the panel, [CONTENT: e.g. three list
> rows, each a small rounded-square tile beside two gray placeholder bars], the
> lowest row dissolving into the fade. Flat vector, low fidelity, geometric,
> generous whitespace, hairline strokes of uniform weight, depth from layering
> only. Warm off-white background, white surfaces, medium-gray borders,
> dark-gray icon strokes, light neutral-gray placeholder bars. Grayscale, no
> accent color. Light mode. Square composition, centered, weighted to the upper
> two thirds.
>
> Negative: text, letters, numbers, words, realistic data, screenshot, dashboard,
> photorealism, 3D render, isometric, glossy, gradients, glassmorphism, neon,
> saturated colors, shadows on multiple elements, people, faces, hands,
> characters, mascots, stock illustration, decorative background, clutter.

## Adapting it

- **Dark mode:** swap the color sentence for "near-black background, dark
  charcoal surfaces, mid-gray borders, light-gray icon strokes, muted gray
  placeholder bars", and end with "Dark mode." Keep the *hierarchy* words — the
  card is still described as lighter than the panel.
- **Accent:** append one clause naming exactly one element: "a single muted mint
  checkmark on the right-hand card, the only color present."
- **Other archetypes:** replace the floating-card sentence with a medallion ("a
  thin-outlined circle centered on the panel's upper area containing a small line
  icon of […]"), and the content sentence with the archetype's own description
  from `archetypes.md`.

## Consistency across a set

If the user insists on generating a family this way:

- Keep the style, color, theme and negative sections **byte-identical** across
  every prompt. Change only the subject, icon and content sentences.
- Fix the seed where the model supports it.
- Generate one, approve it, then use it as a style reference image (`--sref`, an
  image prompt, or a reference-image input) for the rest.
- Budget several attempts per illustration.

Even done carefully this is worse than the SVG path for a set. Offer to switch.
