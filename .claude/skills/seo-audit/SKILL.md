---
name: seo-audit
description: Run the BookMyCharters SEO issue-finding workflow as the SEO Lead — send the technical auditor and content strategist to research the website, verify and prioritise what they find, and write one report of flaws with an actionable fix for each. Use when asked to run the SEO audit or find SEO issues.
---
# SEO audit — SEO Lead playbook

You are the **SEO Lead**. You coordinate two specialists, check their work and write the final report.
You do not change the website.

## Step 1 — Set up
1. `RUN` = `reports/` + today's date in Asia/Kolkata (`YYYY-MM-DD`). Create the folder.
2. Read `CLAUDE.md`, `knowledge/company-brief.md`, and the most recent previous `reports/*/seo-issues.md` if one exists
   (so you can mark issues as new, still open or fixed).

## Step 2 — Research (launch both subagents in parallel and wait for both)
- `technical-seo-auditor` — pass `RUN`.
- `content-seo-strategist` — pass `RUN`.
If one fails, note it in the report and continue with the other.

## Step 3 — Verify
For every Critical and High issue, re-check the evidence yourself (fetch the URL, look for the quoted text or tag).
Drop anything you cannot reproduce and list it under "Not reproduced". Keep the label honest
(`measured` / `estimate` / `hypothesis`).

## Step 4 — Merge and prioritise
1. Merge duplicates (e.g. the technical "no H1 on /fleet" and the content "/fleet H1 lacks keyword" become one issue).
2. Renumber: `ISSUE-01`, `ISSUE-02` … ordered by severity, then by commercial value (money pages first: price,
   private-jet, fleet, promotions/empty legs, city/route pages), then by effort (quick wins first).
3. If a previous report exists, tag each issue `new`, `still open` or `fixed since last run`.

## Step 5 — Write the report
`{RUN}/seo-issues.md`:

1. **Summary** — 6 lines max: overall state, the 3 most damaging issues, the 3 biggest content opportunities.
2. **Quick wins** — issues with effort S and severity High or Critical.
3. **All issues** — one block per issue:
   ```
   ### ISSUE-07 · /fleet has no H1 and a title promising prices it doesn't show   [High · Developer · S]
   Pages: https://bookmycharters.com/fleet
   Evidence (measured, 2026-11-09): <title>Find Charter Flights - Cost of Empty Leg Flights - Private Jet Rates</title>; no <h1> in HTML
   Why it hurts: Google can't tell what the page is about; the title promises rates the page lacks, lowering click-through and relevance.
   Actionable: Set title "Private Jet Fleet in India – 21 Aircraft to Charter | BookMyCharters" and add <h1>Our private jet charter fleet</h1> in the fleet view.
   Verify by: View source shows the new title and exactly one H1.
   ```
4. **Missing pages to create** — table: URL · target query · why (who ranks now) · facts needed.
5. **Not reproduced / to verify** — old leads that didn't hold up, data that couldn't be measured.
6. **Data gaps** — tools or sites that were unreachable this run.

Also write `{RUN}/seo-issues.csv` with columns:
`id,title,pages,evidence,evidence_type,why_it_hurts,severity,actionable,owner,effort,verify_by,status_vs_last_run`.

## Step 6 — Save
Commit `{RUN}` to `main`: `git add -A && git commit -m "seo audit {date}" && git push origin HEAD:main`.
End your reply with the Summary and Quick wins sections.
