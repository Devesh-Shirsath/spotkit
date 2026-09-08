# Feature → metaphor

The hardest and most valuable step. Everything downstream is mechanical.

## The five questions

Answer these before drawing anything. In writing, briefly — they take a minute
and they prevent the most common failure, which is drawing the screen instead of
the idea.

1. **What is the primary object?** The noun the feature acts on. *User. Invoice.
   API. Guide. Key.*
2. **What happens to it?** The verb. *Grouped. Approved. Connected. Versioned.
   Packaged.*
3. **What is the relationship between objects?** Containment? Sequence?
   Mapping? Convergence? Hierarchy? This determines the archetype.
4. **What is the one interaction that matters?** If the user could do only one
   thing here, what is it?
5. **Which UI primitive naturally expresses that relationship?** Not "which
   primitive does the real product use" — which one *expresses the relationship*.

## The test

Cover the icon. Remove every label. Show it to someone who has never seen the
product.

If they can describe the *relationship* — "a bunch of things going into one
thing", "people with different levels of access", "something waiting to be
approved" — it works. If they can only say "a settings screen", start over.

## Relationship → shape

| Relationship | Shape that carries it |
|---|---|
| Containment | one panel enclosing several similar items |
| Convergence | several nodes, connectors, one central node |
| Sequence | cards in a receding stack, or two states and an arrow |
| Mapping | a matrix of rows × columns with filled/hollow cells |
| Hierarchy | one emphasized card above two recessive ones |
| Selection | a row of pills, exactly one filled |
| Transformation | two cards, before and after, one arrow between |
| Multiplicity | three rows, the third dissolving into the fade |
| Gating | a boundary line or shield between two groups |
| Accumulation | stacked, offset copies of one card |

## Catalog

Worked starting points. Adapt rather than copy — the wording of a specific
product's feature should shift the emphasis.

| Feature | Concept | Archetype | Key primitives |
|---|---|---|---|
| **Teams / Members** | people grouped and managed | C | group icon medallion, three avatar rows, edit affordance |
| **Roles & permissions** | who can do what | B | person rows × capability columns, filled/hollow dots |
| **Single sign-on** | one identity opening many doors | D | one key node, three service nodes, converging connectors |
| **Connectors / Integrations** | external services attached to the product | A | plug icon, logo tiles, service rows |
| **API gateway / Routing** | one entry point dispatching many ways | D | one central node, diverging arrows, endpoint rows |
| **API keys / Tokens** | credentials issued and revoked | A | key icon, rows with a state dot each |
| **Webhooks** | events pushed outward | D | central node, outbound dashed connectors, arrowheads |
| **Versioning** | one thing over time | C | clock icon, receding stack of identical cards |
| **Environments** | the same thing in parallel contexts | B | environment columns, config rows, cells |
| **Audit log** | a record of what happened | A | list rows, one state dot per row, no header controls |
| **Recipes / Workflows** | parts assembled into a reusable whole | C | book + braces icons, receding stack, one container |
| **Categories / Tags** | content grouped for navigation | A | tag icon, pill row with one selected, grouped cards |
| **Search** | many things narrowed to a few | A | search icon in a wide field, three result rows |
| **Documentation** | structured, navigable reference | A | book icon, section rows, one nested indent |
| **Pricing plans** | levels of access and value | B | two or three plan cards, feature rows, one emphasized |
| **Products / Packaging** | several capabilities sold as one | C | cube medallion, API cards collecting into a container |
| **Invoices / Billing** | records generated and tracked | A | document icon, amount bars right-aligned, state dots |
| **Usage / Quotas** | consumption against a limit | A | meter bar partially filled, rows with small meters |
| **App approval** | a submission reviewed and resolved | E | document card, arrow, checkmark |
| **Onboarding** | steps completed in order | E | two state cards, progress dots |
| **Notifications** | events routed to people | D | envelope icon, one node, recipient rows |
| **Partner groups** | outside organizations with shared access | B | building icon, org rows × resource columns |
| **Settings** | configurable options | A | gear medallion, toggle rows |
| **Analytics** | activity summarized | A | chart icon, a bar row, metric cards |

## Two examples in full

### "Teams is a tab with a table of all users in the organisation."

The literal reading is a table. The table is not the point.

- Object: people. Action: grouped. Relationship: containment.
- The interaction that matters: *managing* who is in the group.
- Archetype **C**: a group medallion above a receding stack of member rows, each
  row an avatar, a name bar, and a small edit affordance.

Reads as: *a place where an organisation's people are gathered and managed.*
Not as: *a table.*

### "Recipes are workflows made from guides and APIs clipped together."

- Objects: guides and APIs. Action: combined. Relationship: sequence into a whole.
- The interaction that matters: *assembling*.
- Archetype **C**: a medallion, then three cards receding — the first with a book
  icon, the second with braces, the third smaller and fading. Different icons on
  each card do the work of saying "different kinds of thing"; the stack does the
  work of saying "assembled into one."

No workflow editor. No canvas. No node graph. The relationship outranks the UI.

## When the feature is ambiguous

Offer **2–3 conceptual directions**, one line each, and let the user pick.

> "Partner Groups" could go three ways:
> **A. Grouping** — partner organizations gathered into containers.
> **B. Access** — a partner group meeting a boundary, with resources beyond it.
> **C. Sharing** — one group, several members, shared resources below.

These are different *ideas*, not different *styles*. Never offer "same concept,
three color treatments" — that is not a decision worth the user's time.

## Anti-patterns

- **Drawing the noun instead of the relationship.** "Invoices" is not a picture
  of an invoice; it is records being generated and tracked.
- **Literal-minded icon soup.** Three icons in a row is not a metaphor.
- **Reproducing navigation.** Sidebars and breadcrumbs describe an app, not a
  feature.
- **Metaphors from outside software.** No bridges, rockets, puzzle pieces,
  lightbulbs, handshakes. The vocabulary is interface, not allegory.
- **Encoding the feature's name rather than its behaviour.** If the feature were
  renamed tomorrow, the illustration should still be right.
