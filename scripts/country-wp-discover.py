#!/usr/bin/env python3
"""Discover all blog + service WP URLs for one country.

Strategy: prefer the Yoast per-country sitemap (carelabz.com/{cc}/sitemap.xml)
which authoritatively classifies URLs as pages (services) vs. posts (blogs).
Fall back to crawling the blog/service index pages if sitemap is missing.

Usage:
  python3 scripts/country-wp-discover.py {cc}

Output:
  data/{cc}/wp-blog-urls.txt
  data/{cc}/wp-service-urls.txt
"""

import os, sys, re, json, time, subprocess
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "--break-system-packages", "-q"])
    import requests
    from bs4 import BeautifulSoup

WP = "https://carelabz.com"
UA = {"User-Agent": "Mozilla/5.0 (compatible; CarelabsMigration/1.0)"}

EXCLUDE_SLUGS = {
    "", "404-page", "about-us", "about", "blogs", "blog", "our-blogs",
    "contact-us", "contact", "services", "service", "our-services",
    "careers", "registration", "login",
}


def fetch_xml(url: str) -> str | None:
    try:
        r = requests.get(url, headers=UA, timeout=20)
        if r.status_code == 200:
            return r.text
    except Exception:
        pass
    return None


def extract_locs(xml: str) -> list[str]:
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def classify_via_sitemap(cc: str) -> tuple[list[str] | None, list[str] | None]:
    """Return (services, blogs) lists if sitemap is parseable; else (None, None)."""
    idx = fetch_xml(f"{WP}/{cc}/sitemap.xml")
    if not idx:
        return None, None
    sub = extract_locs(idx)
    page_xml = post_xml = None
    for s in sub:
        if s.endswith(f"/{cc}/page-sitemap.xml"):
            page_xml = fetch_xml(s)
        elif s.endswith(f"/{cc}/post-sitemap.xml"):
            post_xml = fetch_xml(s)
    if not page_xml and not post_xml:
        return None, None

    def is_country_url(u: str) -> bool:
        return u.startswith(f"{WP}/{cc}/")

    def slug(u: str) -> str:
        rel = u.replace(f"{WP}/{cc}/", "")
        return rel.rstrip("/").split("/")[-1]

    def cleaned(urls: list[str]) -> list[str]:
        out = []
        for u in urls:
            if not is_country_url(u):
                continue
            s = slug(u)
            if s in EXCLUDE_SLUGS:
                continue
            out.append(u.rstrip("/") + "/")
        return sorted(set(out))

    services = cleaned(extract_locs(page_xml)) if page_xml else []
    blogs = cleaned(extract_locs(post_xml)) if post_xml else []
    return services, blogs


def crawl_paginated(start_url: str, cc: str, max_pages: int = 30) -> list[str]:
    """Fallback crawler — used when the sitemap is unavailable."""
    found: set[str] = set()
    visited: set[str] = set()
    queue: list[str] = [start_url]

    EXCLUDE_PATTERNS = [
        r"/about(?:-us)?/?$",
        r"/contact(?:-us)?/?$",
        r"/blogs?/?$",
        r"/our-blogs/?$",
        r"/services?/?$",
        r"/our-services/?$",
        r"/feed/?$",
        r"/comments/feed/?$",
        r"/page/\d+/?$",
        r"/category/",
        r"/tag/",
        r"/author/",
        r"/wp-content/",
        r"/wp-login",
        r"/wp-admin",
        r"/registration/?$",
        r"/login/?$",
        r"/careers/?$",
        r"#",
    ]

    iteration = 0
    while queue and iteration < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        iteration += 1
        try:
            r = requests.get(url, headers=UA, timeout=20)
            if r.status_code != 200:
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if not href.startswith(f"{WP}/{cc}/"):
                    continue
                clean = href.split("#")[0].split("?")[0].rstrip("/") + "/"
                if any(re.search(p, clean) for p in EXCLUDE_PATTERNS):
                    continue
                if re.search(r"/page/\d+/?$", clean):
                    if clean not in visited:
                        queue.append(clean)
                    continue
                rel = clean[len(f"{WP}/{cc}/"):]
                seg_count = rel.count("/")
                if seg_count == 1 and len(rel) > 1:
                    found.add(clean)
                elif seg_count == 2:
                    first = rel.split("/", 1)[0]
                    if first in {"service", "services", "our-services",
                                 "blog", "blogs", "our-blogs", "insights"}:
                        found.add(clean)
        except Exception as e:
            print(f"  WARN crawl {url}: {e}")
        time.sleep(0.3)

    return sorted(found)


def main():
    if len(sys.argv) < 2:
        print("Usage: country-wp-discover.py {cc}")
        sys.exit(1)
    cc = sys.argv[1]

    out_dir = Path(f"data/{cc}")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Country: {cc}")
    services, blogs = classify_via_sitemap(cc)

    if services is not None or blogs is not None:
        services = services or []
        blogs = blogs or []
        print(f"  via sitemap: services={len(services)} blogs={len(blogs)}")
    else:
        # Fallback to legacy crawler
        audits = json.loads(Path("data/wp-country-availability.json").read_text(encoding="utf-8"))["audits"]
        info = audits.get(cc) or {}
        s = info.get("summary", {})
        blog_path = s.get("blog")
        service_path = s.get("services")
        print(f"  (no sitemap — falling back to crawl)")
        print(f"  Blog index:    /{cc}/{blog_path or '(none)'}")
        print(f"  Service index: /{cc}/{service_path or '(none)'}")
        blogs = crawl_paginated(f"{WP}/{cc}/{blog_path}", cc) if blog_path else []
        services = crawl_paginated(f"{WP}/{cc}/{service_path}", cc) if service_path else []

    Path(f"data/{cc}/wp-blog-urls.txt").write_text("\n".join(blogs), encoding="utf-8")
    Path(f"data/{cc}/wp-service-urls.txt").write_text("\n".join(services), encoding="utf-8")
    print(f"  Blog posts:    {len(blogs)}")
    print(f"  Service pages: {len(services)}")


if __name__ == "__main__":
    main()
