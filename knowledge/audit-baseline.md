# Audit baseline — findings to RE-VALIDATE (2 November 2026)

> These come from an external audit made with a fetcher that could not read `robots.txt`, `sitemap.xml`
> or `<script>` tags. **None of these is a confirmed current defect.** In the first sprint the technical-seo and
> content-director agents re-check each one against the live site and either open a register row
> (`proposed`, with fresh evidence) or mark it `not reproduced` in their report.
> After the first sprint, do not re-read this file except to check whether a new finding is a repeat.

## Technical (owner: technical-seo)

| Base ID | Finding to validate | Pages | Audit severity |
|---|---|---|---|
| B-T01 | Login/register/OTP/forgot-password modals server-rendered on every page; "This email id already exists!" ~10× in HTML | all | High |
| B-T02 | Country-code dropdown (~250 options) rendered 3× per page | all | High |
| B-T03 | `javascript:void(0)` used for content links: deal cards, destination cards, feature tabs; one malformed `javascript:void();` | /promotions, /private-jet, /wedding-charter, nav | High |
| B-T04 | Viewport `maximum-scale=1.0, user-scalable=no` blocks zoom | all | Medium |
| B-T05 | OG/Twitter: `og:type=article` on service pages; relative `og:url`; `twitter:card` holds page title; OG vs Twitter images differ; logo used as social image | all | Medium |
| B-T06 | `<title>` disagrees with `meta-title`/`og:title` | /fleet, /promotions, /wedding-charter | Medium |
| B-T07 | Non-standard meta: `meta-keywords`, `meta-revisit-after`, `meta-robots: All`; copyright meta typo "bookmychaters.com" | all | Low |
| B-T08 | Canonical seen as meta tag rather than `<link rel="canonical">` on /fleet | /fleet | Verify |
| B-T09 | /sitemap.html: all 21 fleet entries link to /fleet; link titles mismatched; .mp4 listed | /sitemap.html | Medium |
| B-T10 | Blog on subdomain; nav "Blog" link uses http:// | blog | Medium |
| B-T11 | Preloader video + "Your browser does not support the video tag" fallback text | home, /private-jet, /wedding-charter | Low |
| B-T12 | JSON-LD from `googleSchemaData.php` not confirmed on every template | all | Verify |
| B-T13 | Heading hierarchy: H1 = title tag copy on home and /private-jet; no H1 on /fleet; UI labels and form steps marked up as H3/H4 | home, /private-jet, /fleet, /wedding-charter | Medium |
| B-T14 | Empty alt on content images (10 deals on home, ~23 on /private-jet, all on /wedding-charter, blog thumbnails) | several | Medium |

## Content (owner: content-director)

| Base ID | Finding to validate | Pages |
|---|---|---|
| B-C01 | Helicopter/yacht "till we go live" placeholder copy | home |
| B-C02 | Feature blurbs printed twice in a row; empty headings ("Take off to a world of luxury…", 5× "Private Flying Experience") | home, /private-jet |
| B-C03 | All visible deals "Sold Out", dated Aug–Sep 2026; "Pay upto 80% less" vs listed discounts up to ~89% | home, /promotions |
| B-C04 | Delhi card lists The Taj Mahal Palace (Mumbai hotel); destination cards duplicated | /private-jet |
| B-C05 | Challenger 605: "8 Seater" vs "10–12 passengers"; cabin 6.1 vs 6.2 ft; $27m purchase price on charter page | /fleet/challenger-605 |
| B-C06 | ATR 72 called a jet; "Therange"; truncated Hawker 900XP text; "Gulfstream 200" naming | /wedding-charter, /fleet |
| B-C07 | Typos sitewide: recieve, charaters, atleast, incase, there by, wont, Aircrafts, Oneway, enroute, upto, Instragram | all |
| B-C08 | Password rule conflict: "8 to 15 alphanumeric" vs "at least 9 characters" | modal |
| B-C09 | Brand name inconsistency on /faq (Baron, Baron Eagle, Baron Luxury and Lifestyles…) | /faq |
| B-C10 | "149 airports in India" vs "30,000 airports worldwide" | /faq |
| B-C11 | Fleet pages ~200 words, no price range, conflicting specs | /fleet/* |
| B-C12 | /promotions ~150–200 words; no explanation of empty legs | /promotions |
| B-C13 | /wedding-charter ~500 words, no pricing, no FAQs | /wedding-charter |
| B-C14 | /faq: no payment, cancellation, GST, lead-time FAQs; thin cost answer | /faq |

## Opportunities (owners: search-intelligence, growth-recommender)

| Base ID | Opportunity | Blocked by |
|---|---|---|
| B-O01 | Price hub /private-jet-charter-cost-india with INR tables | price table in company-brief |
| B-O02 | Empty-leg system: hub + one URL per deal + Offer schema | dev effort |
| B-O03 | 10 city pages, then 20 | service/airport facts |
| B-O04 | 15 route pages, then 30 | flight times, price ranges |
| B-O05 | Enrich 21 fleet pages | spec sheet |
| B-O06 | Listicle inclusion (The Flying Engineer etc.) | — |
| B-O07 | Reclaim ~75 unlinked press mentions | list of clippings |
| B-O08 | Google Business Profile + review flow | — |
| B-O09 | Move blog to /blog/ with 301s | dev effort |
