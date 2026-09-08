# Layouts

The most common failure of this style is **monotony** — every illustration
becomes "wide header card, then rows." The visual language is fine; the
composition is the same twelve times and the set reads as one image repeated.

Variety comes from composition, never from styling. Same radii, same strokes,
same tokens, same fade — different arrangement.

## The four choices

Every layout is a combination of four independent decisions. They multiply, so
the space is much larger than the twelve named layouts below.

**1 · Where the floating element sits**

top-centre overhanging · top-left overhanging · two at opposite corners ·
inline (a content row raised out of the stack) · none at all

**2 · What the floating element is**

header card (icon + bar pair) · pill / tab strip · icon toolbar ·
small chip (icon + one bar) · medallion · search field · a raised content row ·
a raised card among peers

**3 · How content is arranged**

centred rows · cascade (stepping inward, fading) · right overflow (rows wider
than the panel) · fanned (three side by side, middle raised) · stacked offset ·
constellation (satellites around a hub) · matrix · timeline rail · split pair ·
ascending columns

**4 · Panel treatment**

plain · window chrome (three dots and a rule) · nested inner panel

**5 · Frame and backdrop**

The panel is sized to its content, not fixed — 104 wide for a timeline, 134 for a
table of rows. Its edge is either `fade` (open bottom: *there is more*) or
`contained` (closed: *this is all of it*). Behind it sits `none`, a `plate`, an
`offset` sheet, or a `twin` stack.

These are not decoration. A narrow contained panel and a wide fading one read as
different objects before any content is drawn, which is most of the perceived
variety in a set.

`L1` is choice 1=top-centre, 2=header card, 3=centred rows, 4=plain. That is one
cell of the grid, and the reason sets look repetitive is that it is the easiest
cell to land in.

## The twelve

| | Layout | Float | Panel | Backdrop | Reads as |
|---|---|---|---|---|---|
| **L1** | Header + rows | header card | 118 fade | twin | many of one thing |
| **L2** | Cascade | raised row + flat medallion | 110 fade | offset | a group, receding |
| **L3** | Tab bar | pill strip | 112 fade | plate | one option among several |
| **L4** | Toolbar | icon strip | 116 fade | none | tools and the people using them |
| **L5** | Corner chips | two chips, diagonal | 104 fade | offset | a thing with parts attached |
| **L6** | Window | none | 134 fade, chrome | twin | a real surface, more off-screen |
| **L7** | Fanned | middle card, raised | 128 **contained** | none | a set with one chosen |
| **L8** | Notifications | top card | 108 **contained** | offset | events arriving |
| **L9** | Constellation | header card | 118 fade | plate | systems converging |
| **L10** | Matrix | header card | 118 fade | none | who can do what |
| **L11** | Timeline | header card | 104 fade | offset | sequence, newest first |
| **L12** | Split | medallion | 116 **contained** | plate | moving through stages |

Four panel widths, two edge treatments, four backdrops. That spread is doing as
much work as the content arrangements.

## Choosing the float

This is the decision most often defaulted, and defaulting it is what makes a set
look repetitive even when the content arrangements all differ. There are eight
treatments. The full-width header card is **one of them, not the default.**

| Treatment | Width | Use when |
|---|---|---|
| header card | full | the feature is a list of records that needs naming |
| pill / tab strip | full | the feature is a choice among options |
| icon toolbar | full | the feature is about a set of tools |
| corner chip | ~60 | the header band is already occupied by something else |
| column chip | ~74 | the content is a single column |
| medallion | 28 | the feature is a *thing* rather than a record |
| a raised content element | varies | the subject **is** one of the content items |
| none | — | the panel itself is the subject |

**Budget: at most two illustrations in twelve may use the full-width header
card.** It is the easiest choice and it will quietly take over a set — an earlier
version of this system had it on 7 of 12 before anyone counted.

You have defaulted if any of these is true:

- the float says nothing the content does not already say
- you could swap the floats between two illustrations and neither would change
- the float is full width because the *panel* is, not because the content is
- three layouts in a row have an identical icon-plus-two-bars strip at `y=24`

The fix is almost always to ask what the *subject* of the feature is. If it is a
hub, raise the hub. If it is a column, put a chip at the head of the column. If
it is the surface itself, drop the float entirely.

## Choosing

**First, by meaning.** The relationship decides — see `metaphor.md`.

**Then, by element count.** How many things does the idea actually need?

| Elements | Layouts that fit |
|---|---|
| 1–2 | L8, L12, L7 |
| 3–4 | L1, L2, L3, L5, L11 |
| 4–6 | L4, L6, L9, L10 |

Forcing four elements into L8 leaves it empty; forcing two into L10 leaves it
looking broken. Match the layout to the count before you start drawing.

**Then, by neighbour.** If the illustration next to this one in the product's
navigation uses the same layout, pick your second choice. Adjacency is where
monotony is actually noticed.

**Distribution across a set:** no layout should appear more than about twice in
twelve. If you have used L1 three times, the third one is lazy — re-examine
whether that feature's relationship is really "many of one thing," or whether you
just defaulted.

## What stays fixed

However the composition varies, these never do:

- the panel *radius, padding and hairline* — though not its width or height
- the fade height, wherever a panel fades
- the fade, at the same height every time
- stroke weights, bar heights, corner radii
- the icon family and its sizes
- the token palette
- exactly one element carrying the shadow
- the outer ~10px kept clear

A set built this way looks like twelve views of one product rather than twelve
copies of one drawing.

## Balance

- Centre of gravity on **x=80**, weighted to the upper two thirds. The fade owns
  the bottom.
- Content lives roughly `y=44 → y=120`. The fade begins at `y=112`, so **check
  that nothing important lands below it** — cards dissolving mid-content is the
  most common geometry bug in this system.
- The last block *should* sit inside the fade and half-dissolve. That is the
  device that says "and more."
- If the panel is more than ~60% covered, remove something.

## Inventing a thirteenth

Allowed, and expected — the four choices above generate far more than twelve.
Two rules:

1. Change only choices 1–4. If you find yourself changing a radius, a stroke
   weight or a token to make it work, stop: you are leaving the family.
2. Build it as a function alongside the others in `build.py`, so it inherits
   every constant rather than restating them.
