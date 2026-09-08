# Working from a screenshot

When the user supplies a screenshot of the real product, it defines **structure**
— not appearance, and not content. The illustration is never a traced screenshot
at lower opacity.

Precedence when both are given:

1. The **feature description** defines the meaning.
2. The **screenshot** defines the underlying structure.
3. The **illustration language** defines everything visual.

A screenshot alone is the weakest input. If that is all you have, infer the
feature and *say what you inferred*, so the user can correct you before you draw.

## Six steps

### 1. Name the feature in one sentence

Not "a table of users with role dropdowns" — that describes a screen. Rather:
"give each member of an organisation a level of access."

### 2. Extract the primitives

List only what carries meaning. Usually 3–6 things:

> avatar per row · name per row · a role control per row · an add-member button ·
> a search field

### 3. Delete aggressively

Remove, without exception:

- every real name, email, URL, id, timestamp and number
- secondary and tertiary navigation, breadcrumbs, tabs you are not featuring
- toolbars, overflow menus, pagination, filters, sort controls
- all but 3–4 rows, all but 3–4 columns
- anything you would have to squint at when the illustration is 160px wide

A good abstraction throws away roughly **90%** of the interface.

### 4. Find the single interaction

What is this screen *for*? One verb. Assigning. Connecting. Approving.
Publishing. Comparing.

If the screen genuinely does several unrelated things, it needs several
illustrations rather than one crowded one. Say so rather than cramming.

### 5. Choose a metaphor, then check it against the screenshot

Pick the archetype from the *relationship* (see `archetypes.md`), then confirm
the screenshot does not contradict it. If the real UI is a matrix and your
metaphor is a stack, one of them is wrong — usually the metaphor should win, but
the mismatch is worth a sentence to the user.

### 6. Compose from primitives

Build with `primitives.md`. Nothing from the screenshot survives literally — not
proportions, not column widths, not the sidebar, not the color.

## Worked example

**Screenshot:** an admin page. Left sidebar, eight nav items. Header with
breadcrumb and search. A table with *Name, Email, Role, Status, Last active,
Actions*, twelve rows of real users, pagination, and a blue "Invite member"
button.

1. **Feature:** manage the people in an organisation and what each may do.
2. **Primitives:** person, name, role, status, invite.
3. **Delete:** sidebar, breadcrumb, search, pagination, four of six columns, nine
   of twelve rows, every real string, the button's blue.
4. **Interaction:** managing membership.
5. **Relationship:** containment, with a little mapping → archetype **C**, a group
   medallion over a receding stack of member rows. (Archetype **B** instead if the
   feature were specifically about *permissions* rather than *membership*.)
6. **Compose:** group icon in a flat medallion. Three member rows — avatar, name
   bar, small edit glyph — narrowing and fading downward, the first one elevated
   and overhanging. One plus cue for invite.

Twelve rows become three. Six columns become one bar. The result says *people,
grouped, managed* — which is what the screen was for.

## Common mistakes

- **Keeping the sidebar** because it was visually prominent. Navigation is
  product chrome; it says nothing about the feature.
- **Preserving column count** out of faithfulness. Four columns of dots read as
  permissions; six read as a spreadsheet.
- **Keeping the brand button color.** The real UI's primary button is not your
  accent budget.
- **Matching the screenshot's aspect ratio.** Format is chosen by where the
  illustration will be displayed, not by the shape of the source window.
- **Reproducing an empty or error state** that happened to be in the capture.

## Privacy

Product screenshots routinely contain customer names, emails, internal URLs and
account ids. None of it may survive — every string becomes a placeholder bar.
The style makes this easy, but check the output rather than assuming.
