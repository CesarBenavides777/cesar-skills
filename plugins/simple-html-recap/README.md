# simple-html-recap

Recaps, summaries and shipped-work lists as one plain HTML file: a title, 5-7 themed sections of short bullets written for a non-technical reader, and a tiny row of links under each. No framework, no external requests, fits in about 2 screens, follows the viewer's light or dark setting.

## Install

```
/plugin marketplace add CesarBenavides777/cesar-skills
/plugin install simple-html-recap@cesar-skills
```

Or for any agent: `npx skills add CesarBenavides777/cesar-skills --skill simple-html-recap`.

Then ask for "this week's recap in html" or "a simple shipped list".

## Make it yours

The defaults stay put until you override them. Drop a `recap-style.md` in `~/.claude/` (everywhere) or `.claude/` (one project) with any of these sections: `Tone`, `Conventions`, `Theme`, `Links`, `Delivery`. Leave a section out and the default applies. A request can still override both for a single recap ("make this one casual").

`skills/simple-html-recap/style-template.md` is a starter with every section filled in.

MIT.
