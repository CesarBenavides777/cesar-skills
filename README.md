# Cesar Skills

Claude Code plugins by [Cesar Benavides](https://github.com/CesarBenavides777), published
as the **`cesar-skills`** marketplace. This repo is a generated mirror of `plugins/` in the
Cesar-AI monorepo — open issues here, but changes land upstream and sync on merge.

## Install

```
/plugin marketplace add CesarBenavides777/cesar-skills
/plugin install paper-design@cesar-skills
```

## Plugins

| Plugin | What it does |
| ------ | ------------ |
| [`paper-design`](plugins/paper-design) | Design in [Paper Desktop](https://paper.design) under its weekly MCP call quota — batched code-to-design seeds, design-system boards, screen + state mockups, and an HTTP bridge for when the `paper` MCP tools aren't registered in the session. Composes with Paper's official `paper-desktop` plugin. |

Skills are also emitted flat under `skills/` for clients that discover `skills/<name>/SKILL.md`.

MIT — see [LICENSE](LICENSE).
