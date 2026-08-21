---
name: paper-design
description: Design in Paper Desktop (paper.design, the "paper" design MCP) under its weekly MCP call quota — code-to-design seeds, design-system boards, screen mockups, state variants, design-to-code reads. Use whenever the user mentions Paper, paper.design, the paper MCP, seeding a design system, or asks to mock up / diagram screens in Paper. Also use when the `paper` MCP tools are missing from the session (ships an HTTP bridge).
---

# Paper design — call-budgeted workflow

Paper Desktop serves its MCP at `http://127.0.0.1:29979/mcp` **from the app itself** and
meters usage **weekly**. On the free tier, naive per-element writing burns the whole
week's quota in one afternoon (~110 calls); Pro is higher but still finite. Every tool
call counts — so design sessions run on a **call budget**.

**Composes with Paper's official plugin** (`paper-desktop`, github.com/paper-design/agent-plugins).
Its two skills — `code-to-design` and `design-to-code` — are three-line intent briefs
("read the project's tokens/styles, build on the canvas" / "read the selected frame, emit
code in the project's conventions") plus a rule to make sure Paper Desktop is running. The
substantive guidance is served by the MCP itself: `get_guide(topic="paper-mcp-instructions")`
(design-quality checklist, review checkpoints, font rules; also `figma-import` and
`mobile-status-bar`). This skill layers on what neither covers: the **call budget**, the
**HTTP bridge**, and the verified **gotchas**. Use the official skill for intent, this one
for how to execute without burning the quota.

## The rules

1. **One `write_html` per section / row / card grid, not per element.** Paper's own
   "write small, write often" guide is UX advice; it costs 5–7× the calls. Target
   ≤ 12 calls per artboard. Each write also *returns every created node id* — via the
   `mcp__paper__*` tools that payload lands in the transcript and is resent with every
   later request, so a long seed is cheapest as one script run (bridge path, rule 6):
   fewer calls **and** one tool result instead of a hundred.
2. **Never re-query what a write already returned.** `write_html` returns every created
   node id — `scripts/p.py::write()` hands them back as a list. `get_tree_summary` /
   `get_computed_styles` are for inspecting designs *you didn't just write*.
3. **One screenshot per milestone** (section landed, artboard finished), captured at
   **scale 0.5** — image tokens scale with pixel *area*, so half scale is a quarter the
   context cost, and 1440×900 at 0.5 still reads for layout, hierarchy and breakage.
   Scale 1 only to judge fine type or hairline borders; 0.6 returns a black image.
   Reviewing several boards? Capture with `shot()`, stitch with
   `sheet([...], "review.jpg")`, and read the **one** contact sheet — 6 boards cost
   ~1.2k tokens as a sheet vs ~10k as six captures. Review it, then move on: never
   re-read a capture you have already reviewed, and never re-shoot a board to
   "double-check" — every image stays in context for the rest of the session.
4. **Zero fix-up calls.** Every write's root div sets `color` and `font-family`
   explicitly (text nodes do NOT inherit from the artboard). Create containers with
   their first child inline — an empty `<div>` becomes a Rectangle that cannot take
   children. `backgroundColor`, not `background`. Flex children that must not wrap get
   `flex-shrink:0; white-space:nowrap`. Tokens via `var(--…)` everywhere.
5. `duplicate_nodes` / `set_text_content` / `update_styles` are for **editing** existing
   nodes; for new content they cost more than one batched write. `write_html` in
   `replace` mode gives the node a **new id** — capture it from the result.
6. **Draft off-canvas.** Compose the HTML locally (f-strings / a scratch file), eyeball
   it in a browser if unsure, push only the final markup. Local is free; Paper isn't.
7. **Name every layer at write time.** Put `layer-name="…"` on every element you write
   (containers *and* leaves); Paper otherwise names everything "Frame", which makes the
   layer tree useless to a designer. It costs zero extra calls — `rename_nodes` after the
   fact does. Convention (kind · specifics, ≤ 50 chars):
   artboards `Foundations` / `Components` / `Screen · Dashboard · default|loading|empty|error|locked`;
   `Header`, `Section · Color`, `Row · Accent quartets`, `Panel · Backdrop mesh`,
   `Swatch · gold`, `Tile · radius bubble-md`, `Glass · card`, `Nav · Markets (active)`,
   `TickerCard · $PEPE (hot)`, `AgentCard · Momentum Scalper`, `PnLBadge · bull md`,
   `Table · Live feed`, `Row · $PEPE`, `Cell · price`, `Label · eyebrow`, `Icon · search`,
   `Chart · sparkline bull`. Text nodes take their content as name automatically — leave
   those. Name the state on state boards (`Skeleton · ticker grid`, `Empty · no agents`).
8. **Atomic structure — for every component.** Organize the canvas as
   `00 · Foundations` (tokens) → `01 · Atoms` (brand marks, badges, chips, icons, meters,
   inputs, buttons) → `02 · Molecules` (cards, nav items, search pills, stat tiles) →
   `03 · Organisms` (sidebar, header, tables, grids, sheets) → `Screen · …` boards.
   Every reusable bit is drawn **once**, on the lowest board it belongs to, as its own
   named node; anything larger is **composed by clone** (`<x-paper-clone node-id="…">`)
   rather than redrawn — so a badge fix on Atoms is the fix everywhere, and the layer
   tree of a screen reads as its component tree. Keep a local `ids` map (name → node id)
   so clones never need a tree lookup. Reorganize with `move_nodes` (ids survive), never
   delete + rewrite.
9. **Lay the canvas out as a grid, never a line.** `create_artboard` ignores `left`/`top`
   (Paper auto-places every new board in "the best empty spot" → a long single row).
   Collect every board id while building, then position ALL of them in **one**
   `update_styles` call at the end: system boards in a row on top
   (`00 · Foundations → 01 · Atoms → 02 · Molecules → 03 · Organisms`), screens below as a
   grid — **one column per route/flow, one row per state** (default, loading, empty, locked,
   error, dialogs), 120px gutters, ≤ 9 columns per band, a 400px gap between bands. Keep the
   layout map in code (route → column, state → row) so a re-run lands in the same place.
   Rows are canonical, **typed** states — never "Variant 1/2/3": Default · Loading · Empty ·
   Gated / not found · Error / filtered · Dialog / overlay · Secondary tab / view · Tertiary
   tab / view · Alternate tier / plan · Populated / in-flight — each row title carries a
   one-line descriptor of what belongs there ("skeletons · first fetch"), and **every
   section repeats its own row titles** on its left edge (only the rows it uses), so each
   block is self-contained at any zoom. Add
   **axis title frames**, with two deliberately different treatments so the axes never read
   alike: X (column) titles are short wide banners above each column (1440×160, card fill,
   route name at ≈96px/800 + a small "N boards" sub-line, 40px above the column); Y (row)
   titles are narrow quiet labels left of each band (≈360 wide, transparent, state name at
   ≈56px/700 in muted, a gold vertical rule on their right edge). Keep gutters tight (80px)
   and band gaps modest (≈360px) — big titles must not blow up the grid. Name them
   `Axis · column · <Route>` / `Axis · row · <State>` and position them in the same batched
   call as the boards.
10. **Light and dark are two whole parallel groups, not per-frame twins.** Paper tokens have
    no modes and there are no component instances, so: seed a parallel light token set
    (`--color-l-<name>` for every token whose value changes), keep ONE set of generators, and
    render the light set by mapping `var(--color-X)` → `var(--color-l-X)` (plus light mesh /
    shadows) on the way out. Build the light group as a complete mirror of the dark sections
    (same geometry, names prefixed `Light · `) placed to the right of the entire dark canvas;
    clone the title frames with `duplicate_nodes` and re-place them. A component fix = re-run
    the generator in both modes.
11. **State both budgets before starting** — MCP calls ("~40: 3 screens × ~12 + 4
   screenshots") *and* context ("~25k tokens: one generator, 4 half-scale captures as
   one sheet"). Check Paper's usage meter before a long session.
12. **Context is the other meter, and it compounds.** Everything in the transcript is
   resent on every subsequent request, so a seed that ends at 120k tokens of context
   costs 120k *per call* for the rest of the session — that is how a full seed burns a
   provider's weekly plan quota in one afternoon. Keep it out of context:
   - **Generators stay on disk.** Author with Write once, then **Edit in place** — never
     re-emit a whole file to change a section, and never paste generated HTML back into
     the conversation. Run them headless; `print()` only counts and the handful of ids
     you need next.
   - **Persist, don't echo.** Node ids → `ids.json` / `boards.jsonl` on disk. Never read
     those dumps back into context — query them with a one-liner that prints ≤ 20 lines.
   - **Captures**: rule 3.
   - Re-runs read the persisted ids file; they never re-derive state with
     `get_tree_summary` (rule 2 applies to your own writes too).

## Connecting

- Preferred: the `mcp__paper__*` tools, when they're registered in the session.
- If they're **not** (Paper wasn't running at session start — the tool list is frozen;
  only the user's `/mcp → paper → Reconnect` fixes it), use the bridge in `scripts/`
  beside this file: `from p import tool, write, art, shot, ids_of`. `mcp.py` does the
  streamable-HTTP handshake (`Accept: application/json, text/event-stream`, persisted
  `Mcp-Session-Id`). Run scripts with the skill's `scripts/` dir on `sys.path`.
- First calls of a session: `tool("get_basic_info")` (file, page, artboards, existing
  tokens) and `tool("get_guide", topic="paper-mcp-instructions")` once.
- If `get_basic_info` suddenly reports `artboards: []`, the user switched pages in Paper
  — don't "fix" it; wait or ask.
- If a call fails with "Weekly MCP limit reached", stop immediately, call
  `finish_working_on_nodes` (it still goes through), and write a resume script.

## Workflow for a code-to-design seed / screen set

1. Read the real source of truth first (theme CSS, tokens, component code, route files) —
   never generic defaults. Post the short design brief (mood, palette, type, direction).
2. **Tokens first, one call**: `create_tokens` with the full Tailwind-v4 namespaces
   (`--color-*`, `--font-*`, `--text-*`, `--font-weight-*`, `--tracking-*`, `--leading-*`,
   `--radius-*`, `--spacing-*`, `--container-*`, `--breakpoint-*`). Paper tokens have no
   light/dark modes — seed the canonical mode, document the other on a swatch row.
   Check fonts once with `get_font_family_info(familyNames=[…])` (Inter and Menlo are
   commonly available; SF Mono usually is not).
3. Artboards 1440×900 desktop (390×844 mobile), `height: fit-content` at the end.
   Flat token background for reference boards; put gradient meshes inside a contained
   panel when glass needs something to refract.
4. Build each artboard as a handful of big writes: header → section → section …
5. Screenshot once, run the review checklist (spacing, type hierarchy, contrast,
   lanes, clipping, repetition), fix with `update_styles` only if something is wrong.
6. `finish_working_on_nodes` when done. Record artboard ids + state somewhere durable.

## Screen boards (planning a product)

For each route: one artboard for the default state, plus compact state boards
(loading / empty / error / locked-tier) as separate artboards named
`Screen · <Route> · <state>`. Pull sections, copy and states from the route code —
`useQuery` branches, empty-state components, error boundaries, tier gates — so the
boards are buildable, not invented. Reuse a shared sidebar/header via
`<x-paper-clone node-id="…">` to save calls.

## Gotchas (verified against paper-desktop 0.5.4)

- `duplicate_nodes` takes `nodes: [{id}]` and returns source/new ids plus a `descendantIdMap`;
  duplicates keep their names, so they can also be mapped by second occurrence in the tree.
- `get_basic_info` lists at most ~100 artboards — for a full list use
  `get_tree_summary(rootNodeId, depth=1)`.
- SVG `<stop stop-color>` cannot take `var(--token)` (renders black) — use the literal hex of
  the token there; fills/strokes on shapes can take `var()`.
- `set_text_content` takes `updates: [{nodeId, textContent}]`.
- A build interrupted mid-run may still have created boards — dedupe by name before laying out.
- Board dumps get big fast (a full two-mode seed leaves ~200 KB of `boards*.jsonl` — reading
  both back is ~50k tokens). Grep them from a script; print only what you need.

- `create_artboard` accepts but ignores `left`/`top`; `update_styles` on the artboard is the only way to position it.
- `layer-name` is the only naming hook in `write_html`; `id`/`title`/`aria-label` do nothing for the tree.

- `get_tree_summary` returns JSON; `json.loads(t)["summary"]` then regex.
- `backdrop-filter` blur, inline SVG with `var(--token)` fill/stroke, `radial-gradient`
  backgrounds, `letter-spacing` in em all render fine.
- A freshly replaced node can render blank in a capture taken the same instant; if you
  must verify, capture the artboard, not the (now re-ided) node.
- zsh: never `echo =====` in a shell command — `=` triggers `=cmd` expansion.
