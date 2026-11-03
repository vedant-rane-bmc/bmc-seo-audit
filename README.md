# BookMyCharters SEO Issue Finder — setup (phase 1)

Three agents, one command, one report. Research only — nothing on the website is changed.

```
/seo-audit  →  SEO Lead
                ├─ technical-seo-auditor   (crawl, indexing, meta, headings, schema, speed)
                └─ content-seo-strategist  (content quality, keywords, missing pages, competitor & AI gaps)
             →  Lead verifies, merges, prioritises
             →  reports/YYYY-MM-DD/seo-issues.md + seo-issues.csv
```

## 1. Before the first run (≈1 hour)
- Fill in `knowledge/company-brief.md` — at least which services are live (jet / helicopter / yacht / empty legs).
  The content agent only proposes pages for live services and never invents prices or specs.

## 2. Try it once by hand (recommended first)
Option A — Claude Code on your computer: open this folder in Claude Code and type `/seo-audit`.
Option B — Claude Code on the web: push this folder to a private GitHub repo (`bmc-seo-audit`), open it at
claude.ai/code, and type `/seo-audit`.

Read `reports/<date>/seo-issues.md`. If an agent's output is off, edit its file in `.claude/agents/` (plain English) and run again.

## 3. Make it run on its own
- **Cloud** (runs with your laptop closed): claude.ai/code/routines → New scheduled task →
  repository `bmc-seo-audit`, schedule weekly (e.g. Monday 09:00), prompt: `Run /seo-audit.`
  In the task's cloud environment set **Network access → Custom** and allow `bookmycharters.com`,
  `blog.bookmycharters.com`, `www.googleapis.com` (+ default list). Add network secret `PSI_API_KEY` for page speed.
- **Desktop** (runs on your computer): Claude Desktop → Code → Scheduled → New task → Only on this computer →
  this folder → weekly → prompt `Run /seo-audit.`

Each run compares with the previous report and marks issues as new, still open or fixed.

## Optional connectors (claude.ai → Customize → Connectors)
- Windsor.ai (Search Console + GA4) — lets agents use real click/impression data. Not required in phase 1.
- Ahrefs — keyword volumes and competitor data. Not required in phase 1; without it, demand is judged from live search results.

## Next phase
When the issue list looks right, add an approval step and an implementer (see the full kit).
