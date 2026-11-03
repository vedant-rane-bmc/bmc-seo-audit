#!/usr/bin/env python3
"""PageSpeed Insights check (mobile by default). Needs env PSI_API_KEY (Google Cloud API key with PSI API enabled).

Usage:
  python3 tools/psi.py https://bookmycharters.com/ https://bookmycharters.com/private-jet --out reports/2026-W46/psi.csv
"""
import argparse, csv, json, os, sys, urllib.parse, urllib.request

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
DEFAULT = ["https://bookmycharters.com/", "https://bookmycharters.com/private-jet",
           "https://bookmycharters.com/fleet/challenger-605", "https://bookmycharters.com/promotions"]


def run(url, key, strategy):
    q = urllib.parse.urlencode({"url": url, "key": key, "strategy": strategy, "category": "performance"})
    with urllib.request.urlopen(f"{API}?{q}", timeout=120) as r:
        d = json.load(r)
    lh = d.get("lighthouseResult", {})
    audits = lh.get("audits", {})
    field = d.get("loadingExperience", {}).get("metrics", {})
    fv = lambda k: field.get(k, {}).get("percentile", "")
    return {
        "url": url, "strategy": strategy,
        "lab_performance_score": round(lh.get("categories", {}).get("performance", {}).get("score", 0) * 100),
        "lab_lcp_s": round(audits.get("largest-contentful-paint", {}).get("numericValue", 0) / 1000, 2),
        "lab_cls": round(audits.get("cumulative-layout-shift", {}).get("numericValue", 0), 3),
        "lab_tbt_ms": round(audits.get("total-blocking-time", {}).get("numericValue", 0)),
        "lab_dom_size": audits.get("dom-size", {}).get("numericValue", ""),
        "field_lcp_ms_p75": fv("LARGEST_CONTENTFUL_PAINT_MS"),
        "field_inp_ms_p75": fv("INTERACTION_TO_NEXT_PAINT"),
        "field_cls_p75": fv("CUMULATIVE_LAYOUT_SHIFT_SCORE"),
        "field_overall": d.get("loadingExperience", {}).get("overall_category", "no field data"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*", default=DEFAULT)
    ap.add_argument("--strategy", default="mobile", choices=["mobile", "desktop"])
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    key = os.environ.get("PSI_API_KEY")
    if not key:
        print("PSI_API_KEY not set - performance not measured this run.")
        sys.exit(0)
    rows = []
    for u in a.urls:
        try:
            rows.append(run(u, key, a.strategy))
        except Exception as e:
            rows.append({"url": u, "strategy": a.strategy, "field_overall": f"ERROR {e}"})
    for r in rows:
        print(json.dumps(r))
    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        with open(a.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=sorted({k for r in rows for k in r}))
            w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main()
