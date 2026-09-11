# Spotkit — notes for AI agents

This repository is an illustration skill: it turns a feature description into a
minimal SVG product illustration that matches a fixed visual system.

## To make an illustration

1. Read **`SPEC.md`**. It is self-contained — every number, the SVG template,
   the building blocks, the twelve layouts and a complete example.
2. **Adapt, don't invent.** Pick the nearest of the twelve layouts (`SPEC.md`
   §7), start from its example file in `examples/`, keep its geometry and change
   only the content. Invent a composition only if none fits, and say so.
3. Take icon paths from **`references/icons.md`**. Never draw your own glyph.
4. If you can run Python: copy the layout's `L*` function from `build.py`, edit
   its content, and run `python3 check.py your.svg` before answering.
5. Write SVG code. Never use an image-generation model for this.

## Don't read these — large, and not needed to draw

- `site/` — the landing page (its `index.html` alone is ~190 KB)
- `examples/gallery.html`, `examples/contact-*.svg`, `examples/flat/`
- `icons.py` — the same paths as `references/icons.md`, in Python

## Reading from a link, without cloning

Fetch the raw files, not the GitHub pages around them:

- https://raw.githubusercontent.com/Devesh-Shirsath/spotkit/main/SPEC.md
- https://raw.githubusercontent.com/Devesh-Shirsath/spotkit/main/references/icons.md
- https://raw.githubusercontent.com/Devesh-Shirsath/spotkit/main/references/examples.md (all twelve layouts, to adapt)

## Changing the skill itself

`build.py` is the source of truth — it generated every example. After changing
it or any doc:

```bash
python3 build.py && python3 flatten.py && python3 check.py --docs
```

`check.py --docs` fails if a doc's numbers, colours or snippets disagree with
`build.py` and `assets/illustration.css`.
