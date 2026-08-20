# Cesar Skills

Cesar Skills — Claude Code plugins, agent skills and a shadcn registry by Cesar Benavides. This repo is a **generated mirror** of the Cesar-AI monorepo —
open issues here, but changes land upstream and sync on merge. Nothing in this tree is
hand-edited.

## Install

**Claude Code plugin marketplace** (managed, auto-updating):

```
/plugin marketplace add CesarBenavides777/cesar-skills
/plugin install paper-design@cesar-skills
```

**Any agent, via [skills.sh](https://skills.sh)** (copies `skills/<name>/` into the agent's
skills dir; `-g` for user-global, `--skill <name>` to pick one):

```
npx skills add CesarBenavides777/cesar-skills
npx skills add CesarBenavides777/cesar-skills --skill paper-design -g
```

**shadcn CLI** (skills, UI primitives, moneytrees components and themes — project-scoped):

```
npx shadcn@latest add https://raw.githubusercontent.com/CesarBenavides777/cesar-skills/main/r/paper-design.json
npx shadcn@latest add https://raw.githubusercontent.com/CesarBenavides777/cesar-skills/main/r/pnl-badge.json
```

or register the namespace once in `components.json` and use `@cesar/<name>`:

```json
{ "registries": { "@cesar": "https://raw.githubusercontent.com/CesarBenavides777/cesar-skills/main/r/{name}.json" } }
```

```
npx shadcn@latest add @cesar/paper-design @cesar/moneytrees-ui
```

## Plugins

| Plugin | What it does |
| ------ | ------------ |
| [`paper-design`](plugins/paper-design) | Design in Paper Desktop (paper.design) under its weekly MCP call quota: batched code-to-design seeds, design-system boards, screen mockups and state variants, plus an HTTP bridge for when the paper MCP tools aren't registered in the session. |

## Skills

Flat `skills/<name>/SKILL.md` layout (what skills.sh and most agents discover); the same
skills are also inside their plugin and in the registry. See [skills/README.md](skills/README.md).

| Skill | Description |
| ----- | ----------- |
| [`paper-design`](skills/paper-design/SKILL.md) | Design in Paper Desktop (paper.design, the "paper" design MCP) under its weekly MCP call quota — code-to-design seeds, design-system boards, screen mockups, state variants, design-to-code reads. Use whenever the user mentions Paper, paper.design, the paper MCP, seeding a design system, or asks to mock up / diagram screens in Paper. Also use when the `paper` MCP tools are missing from the session (ships an HTTP bridge). |

## shadcn registry

`registry.json` is the index; `r/<name>.json` are the installable items (every file inlined,
so raw GitHub serves them as-is). 92 items:

- **Agent skills** (1): `paper-design`
- **UI primitives (shadcn/Radix family → `components/ui/`)** (37): `accordion`, `alert`, `alert-dialog`, `avatar`, `badge`, `button`, `button-group`, `card`, `card-skeleton`, `carousel`, `chart`, `collapsible`, `command`, `dialog`, `dropdown-menu`, `empty-state`, `hover-card`, `input`, `input-group`, `label`, `popover`, `progress`, `scroll-area`, `section-error`, `select`, `separator`, `sheet`, `sidebar`, `skeleton`, `slider`, `sonner`, `spinner`, `switch`, `table`, `tabs`, `textarea`, `tooltip`
- **UI primitives (React Aria family → `components/aria/`)** (36): `aria-accordion`, `aria-alert`, `aria-alert-dialog`, `aria-avatar`, `aria-badge`, `aria-button`, `aria-button-group`, `aria-card`, `aria-checkbox`, `aria-collapsible`, `aria-command`, `aria-dialog`, `aria-dropdown-menu`, `aria-empty`, `aria-field`, `aria-input`, `aria-input-group`, `aria-label`, `aria-popover`, `aria-progress`, `aria-scroll-area`, `aria-select`, `aria-separator`, `aria-sheet`, `aria-sidebar`, `aria-skeleton`, `aria-slider`, `aria-sonner`, `aria-spinner`, `aria-switch`, `aria-table`, `aria-tabs`, `aria-textarea`, `aria-toggle`, `aria-toggle-group`, `aria-tooltip`
- **Shared lib/hooks** (2): `use-mobile`, `utils`
- **Themes** (2): `moneytrees-theme`, `theme`
- **moneytrees (→ `components/moneytrees/`)** (14): `agent-card`, `bending-sidebar`, `data-table-v2`, `liquid-surface`, `live-feed-table`, `moneytrees-logo`, `moneytrees-ui`, `onboarding-tour`, `pnl-badge`, `sentiment-meter`, `theme-provider`, `ticker-card`, `ticker-chart`, `usage-meter`

Items reference each other by absolute `https://raw.githubusercontent.com/CesarBenavides777/cesar-skills/main/r/<name>.json` URLs, so a single `add` pulls
its whole dependency chain. `utils` (`cn`) is assumed to exist from `shadcn init`.

MIT — see [LICENSE](LICENSE).
