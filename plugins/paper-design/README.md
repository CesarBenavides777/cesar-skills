# paper-design

Design in [Paper Desktop](https://paper.design) under its weekly MCP call quota.

Paper's official `paper-desktop` plugin gives Claude the canvas; this plugin teaches it
how to use the canvas **without burning the week's quota**: one write per section instead
of one per element, never re-querying nodes a write already returned, one screenshot per
milestone, and the handful of rendering gotchas that otherwise cost fix-up calls. It also
ships a tiny HTTP bridge (`skills/paper-design/scripts/`) for sessions where the `paper`
MCP tools never registered because the app wasn't running at startup.

## Install

```
/plugin marketplace add CesarBenavides777/claude-plugins
/plugin install paper-design@cesar-ai
```

Then just ask: "seed our design system into Paper", "mock up the settings page in Paper",
"draw the empty and error states for /agents". The skill composes with the official
`paper-desktop:code-to-design` / `design-to-code` skills — use those for intent, this one
for execution.

## What's inside

- `skills/paper-design/SKILL.md` — the rules, the workflow, the gotchas.
- `skills/paper-design/scripts/mcp.py` — minimal streamable-HTTP MCP client for
  `http://127.0.0.1:29979/mcp`.
- `skills/paper-design/scripts/p.py` — `tool()`, `write()` (returns created ids),
  `art()`, `shot()`.

MIT.
