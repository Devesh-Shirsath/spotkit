# Spotkit — notes for AI agents

This repository is an illustration skill: it turns a feature description into a
minimal SVG product illustration that matches a fixed visual system.

## To make an illustration

1. Read **`SPEC.md`**. It is self-contained — every number, the SVG template,
   the building blocks, the twelve layouts and a complete example.
2. Take icon paths from **`references/icons.md`**. Never draw your own glyph.
3. Follow the workflow in `SKILL.md` (feature → metaphor → layout → SVG → check).
   Open another file in `references/` only when a step needs it.
4. If you can run Python: build with the primitives in `build.py`
   (`from build import *`) and run `python3 check.py your.svg` before answering.

## Don't read these — large, and not needed to draw

- `site/` — the landing page (its `index.html` alone is ~190 KB)
- `examples/gallery.html`, `examples/contact-*.svg`, `examples/flat/`
- `icons.py` — the same paths as `references/icons.md`, in Python

## Reading from a link, without cloning

Fetch the raw files, not the GitHub pages around them:

- https://raw.githubusercontent.com/Devesh-Shirsath/spotkit/main/SPEC.md
- https://raw.githubusercontent.com/Devesh-Shirsath/spotkit/main/references/icons.md

Those two are enough.

## Changing the skill itself

`build.py` is the source of truth — it generated every example. After changing
it or any doc:

```bash
python3 build.py && python3 flatten.py && python3 check.py --docs
```

`check.py --docs` fails if a doc's numbers, colours or snippets disagree with
`build.py` and `assets/illustration.css`.
