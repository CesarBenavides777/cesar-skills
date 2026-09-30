---
name: simple-html-recap
description: A "super simple" single-file HTML format for recaps, summaries, and shipped-work lists, with tone, writing conventions and theme adjustable per user or project through a recap-style.md file. Use when asked for a recap, summary, changelog or shipped list "in html", or when delivering weekly-recap output as HTML instead of markdown or chat.
---

# Simple HTML recap

One self-contained HTML file. No frameworks, no external requests, no build step. The
whole page fits in about 2 screens.

## 1. Load the style overrides first

Before writing, look for a style file and read every one that exists:

1. `.claude/recap-style.md` in the current project
2. `~/.claude/recap-style.md` for the user

Each file is optional and so is every section inside it (`Tone`, `Conventions`, `Theme`,
`Links`, `Delivery`). Resolve each section on its own: an instruction in the request
beats the project file, the project file beats the user file, and the user file beats the
defaults below. A section a file leaves out falls through to the next level. A starter
file with every section is in `style-template.md` next to this skill.

## 2. Structure

1. `<h1>` title and one `.meta` line: project, date range, data sources.
2. One `<h2>` per theme, 5-7 at most. Biggest launch first, then Fixes, then "In flight" last.
3. A plain `<ul>` under each heading, 2-5 bullets.
4. One `.links` row per section: 1-4 small links at most (ticket, PR or commit, live page,
   chat permalink), each prefixed with an 11px icon.

## 3. Default tone

Written for a non-technical reader. Each bullet says what changed and why it matters to
the people using it, in plain words. Not commit messages, not file names, not the
implementation. One idea per bullet, one or two short sentences.

## 4. Default conventions

- Sentence case for the title and headings.
- Link labels name the thing ("Loyalty launch PR", "PR #123"), never "here" or a bare URL.
- `&middot;` between links in a `.links` row.
- Numerals for counts and ranges ("3 fixes", "1-5 min").
- Dates in the `.meta` line as the reader would say them ("Jul 7-11, 2026").

## 5. Default theme (copy verbatim)

```css
body {
  font-family: -apple-system, Helvetica, Arial, sans-serif;
  max-width: 720px;
  margin: 40px auto;
  padding: 0 20px;
  line-height: 1.5;
  color: #222;
}
h1 {
  font-size: 1.4rem;
}
h2 {
  font-size: 1.05rem;
  margin-top: 1.8em;
  border-bottom: 1px solid #ddd;
  padding-bottom: 4px;
}
ul {
  padding-left: 1.2em;
}
li {
  margin: 6px 0;
}
.meta {
  color: #777;
  font-size: 0.9rem;
}
.links {
  font-size: 0.85rem;
  color: #999;
  margin-top: 2px;
}
.links a {
  color: #6b7cbf;
  text-decoration: none;
}
.links a:hover {
  text-decoration: underline;
}
.ic {
  fill: currentColor;
  width: 11px;
  height: 11px;
  vertical-align: -1px;
  margin-right: 3px;
}
@media (prefers-color-scheme: dark) {
  body {
    background: #111;
    color: #ddd;
  }
  h2 {
    border-color: #333;
  }
  .meta {
    color: #999;
  }
  .links a {
    color: #8fa0e0;
  }
}
```

A `Theme` section in a style file replaces this whole block, dark-mode rule included. A
theme that commits to one dark or light ground must paint `body`'s background explicitly,
or the host page's colours show through.

## 6. Links row

```html
<p class="links">
  <svg class="ic"><use href="#i-gh" /></svg
  ><a href="https://github.com/org/repo/pull/123">PR #123</a> &middot;
  <svg class="ic"><use href="#i-ticket" /></svg
  ><a href="https://tracker.example.com/ABC-42">ABC-42</a>
</p>
```

Icons live in one inline `<svg style="display:none">` sprite of `<symbol id="i-…">`
elements at the top of `<body>`. Never hotlink an icon. Brand marks can come from
[Simple Icons](https://simpleicons.org) (CC0); a generic link glyph is fine when there is no
brand.

## 7. Gathering link targets

Unless a `Links` section says otherwise:

- GitHub base URL: `gh repo view --json url --jq .url`.
- PRs and commits: `gh pr list --state merged --search "merged:>=YYYY-MM-DD"`, `git log --since`.
- Before linking a page on a live site, confirm the route exists in the app.
- Leave a link out rather than guess one.

## 8. Delivery

Default: write the file (e.g. `recap-YYYY-MM-DD.html`) and hand it over. In Claude Code,
send it with `SendUserFile` and `display: render` so it renders inline. A `Delivery`
section can switch this, for example to a published page when the readers are a team
who won't open a local file.

## Optional: tabs

For a recap with more than about 5 sections, a tab row above them lets readers jump to
their own. One tab per section plus "Everything" as the default. Keep it plain:
`role="tablist"`, buttons carrying `aria-selected`, sections toggled with the `hidden`
property, arrow-key navigation, and the selected tab remembered in `localStorage` inside
a `try/catch`.
