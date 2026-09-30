# Skills

Each directory is one agent skill (`SKILL.md` plus any scripts it ships). Generated from the
Cesar-AI monorepo — edit upstream, not here.

### [`paper-design`](./paper-design/SKILL.md)

Design in Paper Desktop (paper.design, the "paper" design MCP) under its weekly MCP call quota — code-to-design seeds, design-system boards, screen mockups, state variants, design-to-code reads. Use whenever the user mentions Paper, paper.design, the paper MCP, seeding a design system, or asks to mock up / diagram screens in Paper. Also use when the `paper` MCP tools are missing from the session (ships an HTTP bridge).

```
npx skills add CesarBenavides777/cesar-skills --skill paper-design
npx shadcn@latest add https://raw.githubusercontent.com/CesarBenavides777/cesar-skills/main/r/paper-design.json
```

### [`simple-html-recap`](./simple-html-recap/SKILL.md)

A "super simple" single-file HTML format for recaps, summaries, and shipped-work lists, with tone, writing conventions and theme adjustable per user or project through a recap-style.md file. Use when asked for a recap, summary, changelog or shipped list "in html", or when delivering weekly-recap output as HTML instead of markdown or chat.

```
npx skills add CesarBenavides777/cesar-skills --skill simple-html-recap
npx shadcn@latest add https://raw.githubusercontent.com/CesarBenavides777/cesar-skills/main/r/simple-html-recap.json
```
