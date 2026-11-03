# Keyword map (seed — owned by search-intelligence)

> Starting clusters from the 2 November 2026 audit. Search volumes were **not** measured in that audit.
> The search-intelligence agent replaces "volume: unknown" with `estimate` (Ahrefs) or `measured` (GSC) values
> and adds/removes clusters as evidence comes in. Keep this file under ~150 lines; move detail to weekly reports.

| Cluster | Seed queries | Intent | Current page | Target page | Status |
|---|---|---|---|---|---|
| Price / cost | private jet price India; private jet price per hour India; private jet price in rupees; charter flight cost India 2026 | Commercial research | none (titles claim it; pages don't answer) | NEW /private-jet-charter-cost-india | proposed |
| Route | Mumbai to Goa private jet; Delhi to Goa private jet; Mumbai to Delhi charter flight; Mumbai to Udaipur private jet | Transactional | none | NEW /private-jet/{from}-to-{to} | proposed |
| City | private jet charter Mumbai; private jet Delhi; private jet Bangalore; best private jet services in Mumbai | Commercial | unlinked cards on /private-jet | NEW /private-jet/{city} | proposed |
| Empty leg | empty leg flights India; empty leg Mumbai; empty leg private jet deals | Transactional | /promotions (no per-deal URLs) | /empty-leg-flights + per-deal URLs | proposed |
| Helicopter | helicopter charter Mumbai price; helicopter rental India; Mumbai to Pune helicopter; Char Dham helicopter | Commercial | placeholder | NEW /helicopter-charter (only if service is live) | blocked: service status |
| Yacht | yacht charter Mumbai; yacht rental Mumbai price; Goa yacht party | Commercial (local) | placeholder | NEW /yacht-charter/{city} (only if live) | blocked: service status |
| Occasion | wedding charter flight India; destination wedding private jet; corporate jet charter | Commercial | /wedding-charter (thin) | expand /wedding-charter; NEW /corporate-charter | proposed |
| Aircraft | Challenger 605 charter price; King Air B200 charter India; Phenom 100 price per hour | Commercial | /fleet/{model} (thin, no price) | enrich existing 21 pages | proposed |
| Brand / comparison | bookmycharters; bookmycharters reviews; best private jet charter company in India | Navigational / shortlist | home, /why-us | off-page + /why-us | monitoring |

## Rules

- Do not target a keyword the business cannot satisfy (see service table in `company-brief.md`).
- One primary keyword per URL. Flag cannibalisation in the register.
- Homepage targets "private jet charter India" + brand, not broad global terms like "private jets".
