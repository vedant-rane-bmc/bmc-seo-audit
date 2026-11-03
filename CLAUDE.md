# BookMyCharters — SEO Issue Finder (phase 1)

This repo runs a **research-only** SEO workflow for https://bookmycharters.com (blog: https://blog.bookmycharters.com).
Goal of this phase: find every flaw that holds back Google rankings and AI-assistant recommendations, and give one
clear, actionable fix for each. **Nothing is changed on the website.** No code, no publishing.

## Agents

| Role | Where | Finds |
|---|---|---|
| SEO Lead | main session, via `/seo-audit` | Coordinates, verifies, de-duplicates, prioritises, writes the report |
| `technical-seo-auditor` | `.claude/agents/` | Crawl, indexing, metadata, headings, schema, links, speed, mobile |
| `content-seo-strategist` | `.claude/agents/` | Content quality, keyword targeting, missing pages, competitor gaps, AI-answer readiness |

## Rules for every agent

1. **Evidence or it didn't happen.** Every issue cites the URL, what was seen (quoted HTML, crawl row, search result)
   and the date checked. If you can't reproduce it today, it is not an issue — at most a "to verify" note.
2. **Label every number**: `measured` (crawl, PSI, live page), `estimate` (third-party tool), `hypothesis`.
3. **Never invent facts** — prices, aircraft specs, services, airport counts come only from `knowledge/company-brief.md`.
   If a fix needs a fact that isn't there, write `[TEAM TO CONFIRM: …]` in the actionable.
4. **Old findings are leads, not proof.** `knowledge/audit-baseline.md` lists items from an earlier audit to re-check.
5. **Be specific.** "Improve meta descriptions" is not an actionable. "Replace the /fleet title
   `Find Charter Flights - Cost of Empty Leg Flights - Private Jet Rates` with `Private Jet Fleet in India – 21 Aircraft to Charter`" is.
6. **One issue = one root cause.** If the same template causes the problem on 30 pages, it is one issue listing the pages.
7. If a tool or site is unreachable, say so in the report and carry on with what you can reach.

## Issue format (used by all agents)

| Field | Meaning |
|---|---|
| id | `TECH-01`, `CONT-01` … (the Lead renumbers in the final report) |
| title | One line naming the flaw |
| pages | URLs or "all pages (template)" |
| evidence | What was observed, quoted, with date and source |
| why_it_hurts | How it lowers rankings, click-through or AI recommendation — one or two sentences |
| severity | Critical / High / Medium / Low (see below) |
| actionable | Exact change to make: what, where, example of the corrected version |
| owner | Developer / Content / Marketing |
| effort | S (< 2 h) / M (< 2 days) / L (more) |
| verify_by | How to check the fix worked |

**Severity guide**
- Critical — stops pages being crawled/indexed or shows wrong information to users or Google.
- High — directly weakens ranking or AI citation for commercial queries (price, city, route, empty leg, aircraft).
- Medium — weakens quality signals across many pages (headings, alt text, thin content, duplicate meta).
- Low — polish (typos in non-critical spots, deprecated tags).

## Output

`reports/YYYY-MM-DD/` with `seo-issues.md` (the report you read), `seo-issues.csv` (same issues as a table) and the
specialists' working notes. Commit to `main` when finished.
