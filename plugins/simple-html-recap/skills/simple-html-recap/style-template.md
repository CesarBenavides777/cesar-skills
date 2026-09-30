# Recap style

Copy to `~/.claude/recap-style.md` (applies everywhere) or `.claude/recap-style.md` (one
project). Keep only the sections you want to change; anything left out uses the skill's
defaults.

## Tone

- Audience: the whole team, including sales and support.
- Voice: first person plural ("we shipped"), friendly, no hype.
- Bullets: one sentence each.

## Conventions

- No em or en dashes.
- Never use these words: robust, seamless, leverage.
- Numerals for every number ("3", not "three").
- Title case for headings.

## Theme

Replaces the default CSS block entirely.

```css
:root {
  --bg: #0f1115;
  --fg: #e8e8e8;
  --muted: #9aa0a6;
  --line: #2a2e35;
  --brand: #7aa2f7;
}
body {
  font-family: system-ui, sans-serif;
  max-width: 720px;
  margin: 40px auto;
  padding: 0 20px;
  line-height: 1.5;
  color: var(--fg);
  background: var(--bg);
}
h1 {
  font-size: 1.4rem;
}
h2 {
  font-size: 1.05rem;
  margin-top: 1.8em;
  border-bottom: 1px solid var(--line);
  padding-bottom: 4px;
}
ul {
  padding-left: 1.2em;
}
li {
  margin: 6px 0;
}
.meta {
  color: var(--muted);
  font-size: 0.9rem;
}
.links {
  font-size: 0.85rem;
  color: var(--muted);
  margin-top: 2px;
}
.links a {
  color: var(--brand);
  text-decoration: none;
}
.links a:hover {
  text-decoration: underline;
}
.ic {
  width: 11px;
  height: 11px;
  vertical-align: -1px;
  margin-right: 3px;
}
```

## Links

- Tickets: Linear, `https://linear.app/acme/issue/<ID>`.
- Chat: Slack permalinks from the search results.

## Delivery

- Publish as a shareable page and hand over the link.
