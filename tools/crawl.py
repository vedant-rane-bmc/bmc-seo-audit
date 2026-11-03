#!/usr/bin/env python3
"""Small, dependency-free SEO crawler for the BookMyCharters agency.

Crawls a site from a start URL (plus URLs found in /sitemap.xml), stays on the allowed hosts, respects robots.txt,
and writes two CSVs:
  pages.csv  - one row per URL with the on-page signals the technical-seo agent checks
  issues.csv - one row per detected issue (url, issue code, detail)

Usage:
  python3 tools/crawl.py --start https://bookmycharters.com --max-pages 150 --out reports/2026-W46/crawl
"""
import argparse, csv, gzip, io, json, os, re, sys, time
import urllib.request, urllib.error, urllib.robotparser
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urldefrag

UA = "BMC-SEO-Agency-Crawler/1.0 (site owner audit)"
SKIP_EXT = re.compile(r"\.(jpg|jpeg|png|gif|webp|avif|svg|ico|pdf|zip|mp4|mov|webm|mp3|css|js|woff2?|ttf|xml)$", re.I)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self._in_title = "", False
        self.meta = {}             # name/property (lowercase) -> content
        self.links_canonical = []
        self.headings = []         # (level, text)
        self._hstack = None
        self.imgs = 0
        self.imgs_no_alt = 0       # alt missing or empty
        self.hrefs = []
        self.js_void = 0
        self._in_ldjson, self._ld_buf, self.ldjson = False, [], []
        self._skip = 0             # inside script/style/noscript/template
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or a.get("http-equiv") or "").lower()
            if key:
                self.meta.setdefault(key, a.get("content", ""))
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.links_canonical.append(a.get("href", ""))
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._hstack = [int(tag[1]), []]
        elif tag == "img":
            self.imgs += 1
            if not a.get("alt", "").strip():
                self.imgs_no_alt += 1
        elif tag == "a":
            href = a.get("href", "").strip()
            if href.lower().startswith("javascript:"):
                self.js_void += 1
            elif href:
                self.hrefs.append(href)
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in_ldjson, self._ld_buf = True, []
        if tag in ("script", "style", "noscript", "template"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._hstack:
            self.headings.append((self._hstack[0], " ".join("".join(self._hstack[1]).split())[:120]))
            self._hstack = None
        if tag == "script" and self._in_ldjson:
            self.ldjson.append("".join(self._ld_buf))
            self._in_ldjson = False
        if tag in ("script", "style", "noscript", "template") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ldjson:
            self._ld_buf.append(data)
            return
        if self._hstack is not None:
            self._hstack[1].append(data)
        if not self._skip:
            self.text_parts.append(data)


def fetch(url, timeout=20):
    """Return (status, final_url, headers, body_bytes, elapsed_ms, redirects)."""
    redirects = []

    class Track(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, hdrs, newurl):
            redirects.append((code, newurl))
            return super().redirect_request(req, fp, code, msg, hdrs, newurl)

    opener = urllib.request.build_opener(Track)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    t0 = time.time()
    try:
        with opener.open(req, timeout=timeout) as r:
            body = r.read()
            if (r.headers.get("Content-Encoding") or "").lower() == "gzip":
                body = gzip.decompress(body)
            return r.status, r.geturl(), {k.lower(): v for k, v in r.headers.items()}, body, int((time.time() - t0) * 1000), redirects
    except urllib.error.HTTPError as e:
        return e.code, url, {k.lower(): v for k, v in (e.headers or {}).items()}, b"", int((time.time() - t0) * 1000), redirects
    except Exception as e:  # network error
        return 0, url, {"error": str(e)}, b"", int((time.time() - t0) * 1000), redirects


def ld_types(blocks):
    types, errors = set(), 0
    def walk(o):
        if isinstance(o, dict):
            t = o.get("@type")
            if isinstance(t, list):
                types.update(map(str, t))
            elif t:
                types.add(str(t))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for b in blocks:
        try:
            walk(json.loads(b))
        except Exception:
            errors += 1
    return sorted(types), errors


def sitemap_urls(root, hosts, limit=5000):
    found, queue, seen = [], deque([urljoin(root, "/sitemap.xml")]), set()
    while queue and len(found) < limit:
        sm = queue.popleft()
        if sm in seen:
            continue
        seen.add(sm)
        status, _, _, body, _, _ = fetch(sm)
        if status != 200 or not body:
            continue
        if sm.endswith(".gz"):
            try:
                body = gzip.decompress(body)
            except Exception:
                pass
        text = body.decode("utf-8", "ignore")
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", text)
        if "<sitemapindex" in text:
            queue.extend(locs)
        else:
            found.extend(u for u in locs if urlparse(u).netloc in hosts)
    return found


def norm(u):
    u, _ = urldefrag(u)
    p = urlparse(u)
    path = p.path or "/"
    return f"{p.scheme}://{p.netloc}{path}" + (f"?{p.query}" if p.query else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)
    ap.add_argument("--max-pages", type=int, default=150)
    ap.add_argument("--out", required=True)
    ap.add_argument("--extra-host", action="append", default=[], help="other hosts to include, e.g. blog.bookmycharters.com")
    ap.add_argument("--delay", type=float, default=0.5)
    args = ap.parse_args()

    start = norm(args.start)
    host = urlparse(start).netloc
    hosts = {host, *args.extra_host}
    os.makedirs(args.out, exist_ok=True)

    rp = urllib.robotparser.RobotFileParser()
    rstatus, _, _, rbody, _, _ = fetch(urljoin(start, "/robots.txt"))
    rp.parse(rbody.decode("utf-8", "ignore").splitlines() if rstatus == 200 else [])

    in_sitemap = set(norm(u) for u in sitemap_urls(start, hosts))
    queue, seen, inlinks = deque([start, *sorted(in_sitemap)]), set(), {}
    pages, issues = [], []
    titles, descs = {}, {}

    def issue(url, code, detail=""):
        issues.append({"url": url, "issue": code, "detail": detail})

    if rstatus != 200:
        issue(urljoin(start, "/robots.txt"), "ROBOTS_TXT_UNAVAILABLE", f"status {rstatus}")
    if not in_sitemap:
        issue(urljoin(start, "/sitemap.xml"), "SITEMAP_EMPTY_OR_UNAVAILABLE")

    while queue and len(pages) < args.max_pages:
        url = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        if SKIP_EXT.search(urlparse(url).path):
            continue
        if not rp.can_fetch(UA, url):
            issue(url, "BLOCKED_BY_ROBOTS")
            continue
        status, final, headers, body, ms, redirects = fetch(url)
        time.sleep(args.delay)
        ctype = headers.get("content-type", "")
        row = {"url": url, "status": status, "final_url": final, "redirect_hops": len(redirects), "ms": ms,
               "in_sitemap": url in in_sitemap, "x_robots": headers.get("x-robots-tag", "")}
        if status == 0:
            issue(url, "FETCH_ERROR", headers.get("error", ""))
        elif status >= 400:
            issue(url, f"HTTP_{status}")
        if len(redirects) > 1:
            issue(url, "REDIRECT_CHAIN", " -> ".join(u for _, u in redirects))
        if status != 200 or "html" not in ctype.lower():
            pages.append(row)
            continue

        p = PageParser()
        try:
            p.feed(body.decode("utf-8", "ignore"))
        except Exception as e:
            issue(url, "HTML_PARSE_ERROR", str(e))
        title = " ".join(p.title.split())
        desc = p.meta.get("description", "").strip()
        canon = urljoin(final, p.links_canonical[0]) if p.links_canonical else ""
        h1s = [t for l, t in p.headings if l == 1]
        types, ld_err = ld_types(p.ldjson)
        words = len(" ".join(p.text_parts).split())
        viewport = p.meta.get("viewport", "")
        skips = sum(1 for (a, _), (b, _) in zip(p.headings, p.headings[1:]) if b > a + 1)

        row.update({
            "title": title, "title_len": len(title), "meta_description_len": len(desc),
            "canonical": canon, "canonical_count": len(p.links_canonical), "canonical_self": norm(canon) == norm(final) if canon else "",
            "meta_robots": p.meta.get("robots", ""), "h1_count": len(h1s), "h1": h1s[0] if h1s else "",
            "h2_count": sum(1 for l, _ in p.headings if l == 2), "heading_skips": skips,
            "imgs": p.imgs, "imgs_missing_alt": p.imgs_no_alt, "js_links": p.js_void,
            "jsonld_types": "|".join(types), "jsonld_errors": ld_err, "og_type": p.meta.get("og:type", ""),
            "og_url": p.meta.get("og:url", ""), "twitter_card": p.meta.get("twitter:card", ""),
            "viewport_blocks_zoom": ("user-scalable=no" in viewport.replace(" ", "")) or ("maximum-scale=1" in viewport.replace(" ", "")),
            "word_count": words,
        })
        pages.append(row)

        # issues
        if not title: issue(url, "TITLE_MISSING")
        elif len(title) > 60: issue(url, "TITLE_TOO_LONG", f"{len(title)} chars")
        if not desc: issue(url, "META_DESCRIPTION_MISSING")
        elif len(desc) > 160: issue(url, "META_DESCRIPTION_TOO_LONG", f"{len(desc)} chars")
        if not canon: issue(url, "CANONICAL_MISSING")
        elif len(p.links_canonical) > 1: issue(url, "CANONICAL_MULTIPLE", " | ".join(p.links_canonical))
        elif norm(canon) != norm(final): issue(url, "CANONICAL_NOT_SELF", canon)
        if "noindex" in (p.meta.get("robots", "") + row["x_robots"]).lower(): issue(url, "NOINDEX")
        if len(h1s) == 0: issue(url, "H1_MISSING")
        elif len(h1s) > 1: issue(url, "H1_MULTIPLE", " | ".join(h1s[:3]))
        elif h1s[0] == title: issue(url, "H1_EQUALS_TITLE")
        if skips: issue(url, "HEADING_LEVEL_SKIPS", str(skips))
        if p.imgs_no_alt: issue(url, "IMG_ALT_MISSING", f"{p.imgs_no_alt}/{p.imgs}")
        if p.js_void: issue(url, "JAVASCRIPT_LINKS", str(p.js_void))
        if not types: issue(url, "JSONLD_NONE")
        if ld_err: issue(url, "JSONLD_PARSE_ERROR", str(ld_err))
        if row["og_url"] and not row["og_url"].startswith("http"): issue(url, "OG_URL_RELATIVE", row["og_url"])
        if row["twitter_card"] and row["twitter_card"] not in ("summary", "summary_large_image", "app", "player"):
            issue(url, "TWITTER_CARD_INVALID", row["twitter_card"][:60])
        if row["viewport_blocks_zoom"]: issue(url, "VIEWPORT_BLOCKS_ZOOM", viewport)
        if words < 300: issue(url, "THIN_CONTENT", f"{words} words")
        if "This email id already exists" in body.decode("utf-8", "ignore"):
            issue(url, "STRAY_FORM_ERROR_TEXT")
        titles.setdefault(title, []).append(url)
        descs.setdefault(desc, []).append(url)

        for href in p.hrefs:
            nxt = norm(urljoin(final, href))
            if urlparse(nxt).scheme not in ("http", "https") or urlparse(nxt).netloc not in hosts:
                continue
            inlinks[nxt] = inlinks.get(nxt, 0) + 1
            if nxt not in seen:
                queue.append(nxt)

    for t, urls in titles.items():
        if t and len(urls) > 1:
            for u in urls: issue(u, "TITLE_DUPLICATE", f"{len(urls)} pages")
    for d, urls in descs.items():
        if d and len(urls) > 1:
            for u in urls: issue(u, "META_DESCRIPTION_DUPLICATE", f"{len(urls)} pages")
    for u in in_sitemap:
        if u not in inlinks and u != start:
            issue(u, "ORPHAN_IN_SITEMAP", "in sitemap, no internal links found in crawl")
    for r in pages:
        r["inlinks"] = inlinks.get(r["url"], 0)

    cols = sorted({k for r in pages for k in r}, key=lambda k: (k != "url", k))
    with open(os.path.join(args.out, "pages.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(pages)
    with open(os.path.join(args.out, "issues.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["url", "issue", "detail"]); w.writeheader(); w.writerows(issues)

    counts = {}
    for i in issues:
        counts[i["issue"]] = counts.get(i["issue"], 0) + 1
    print(f"Crawled {len(pages)} URLs ({len(in_sitemap)} in sitemap). Issues by type:")
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
