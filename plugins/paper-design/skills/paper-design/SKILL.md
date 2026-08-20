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
   ≤ 12 calls per artboard.
2. **Never re-query what a write already returned.** `write_html` returns every created
   node id — `scripts/p.py::write()` hands them back as a list. `get_tree_summary` /
   `get_computed_styles` are for inspecting designs *you didn't just write*.
3. **One screenshot per milestone** (section landed, artboard finished). Scale 1 or 0.5
   only — 0.6 returns a black image. Review against Paper's checklist, then move on.
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
9. **State the budget before starting** ("~40 calls: 3 screens × ~12 + 4 screenshots")
   and check Paper's usage meter before a long session.

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

- `layer-name` is the only naming hook in `write_html`; `id`/`title`/`aria-label` do nothing for the tree.

- `get_tree_summary` returns JSON; `json.loads(t)["summary"]` then regex.
- `backdrop-filter` blur, inline SVG with `var(--token)` fill/stroke, `radial-gradient`
  backgrounds, `letter-spacing` in em all render fine.
- A freshly replaced node can render blank in a capture taken the same instant; if you
  must verify, capture the artboard, not the (now re-ided) node.
- zsh: never `echo =====` in a shell command — `=` triggers `=cmd` expansion.
