"""Append Canada electrical-safety standards to existing CA Strapi SEO fields.

Never overwrites existing values. Only appends:
- seoKeywords on home-page + 4 service-pages
- definitionalLede on service-pages (if present)

Idempotent: skips values already in seoKeywords; skips sentence already in lede.
"""
from __future__ import annotations

import copy
import json
import urllib.error
import urllib.request

STRAPI_URL = "https://rational-cheese-8e8c4f80ea.strapiapp.com"

NEW_KEYWORDS = [
    "CSA Z462",
    "IEEE 1584",
    "Canadian Electrical Code",
    "P.Eng Certified",
    "ETAP Certified",
    "CSA Z462 compliance Canada",
    "Canadian electrical standards",
]

SERVICE_KEYWORDS = [
    "CSA Z462",
    "IEEE 1584",
    "Canadian Electrical Code",
    "ETAP",
    "P.Eng",
]

STANDARDS_SENTENCE = (
    " Our work follows CSA Z462, IEEE 1584, and the Canadian Electrical Code "
    "to ensure full compliance for your facility."
)

SERVICE_SLUGS = [
    "arc-flash-study-ca",
    "short-circuit-analysis-ca",
    "load-flow-analysis-ca",
    "relay-coordination-study-ca",
]


def load_token() -> str:
    with open(".env.local", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("STRAPI_API_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("STRAPI_API_TOKEN missing")


def http(method: str, path: str, token: str, body: dict | None = None) -> dict:
    req_body = json.dumps({"data": body}).encode("utf-8") if body is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if req_body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        f"{STRAPI_URL}{path}", data=req_body, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}: {err[:400]}"}


def deep_strip_id(obj):
    if isinstance(obj, dict):
        return {k: deep_strip_id(v) for k, v in obj.items() if k != "id"}
    if isinstance(obj, list):
        return [deep_strip_id(i) for i in obj]
    return obj


def put_entry(collection: str, doc_id: str, payload: dict, token: str) -> dict:
    STRIP_TOP = {"id", "documentId", "createdAt", "updatedAt", "publishedAt", "locale", "localizations"}
    clean_top = {k: v for k, v in payload.items() if k not in STRIP_TOP}
    return http("PUT", f"/api/{collection}/{doc_id}", token, deep_strip_id(clean_top))


def merge_keywords(existing, additions):
    existing = list(existing or [])
    lower_existing = {k.lower() for k in existing if isinstance(k, str)}
    added = []
    for a in additions:
        if a.lower() not in lower_existing:
            existing.append(a)
            added.append(a)
            lower_existing.add(a.lower())
    return existing, added


def append_sentence(existing_text: str, sentence: str) -> tuple[str, bool]:
    if not existing_text:
        return existing_text, False
    if sentence.strip() in existing_text:
        return existing_text, False
    trimmed = existing_text.rstrip()
    joiner = "" if trimmed.endswith((".", "!", "?")) else "."
    return f"{trimmed}{joiner}{sentence}", True


def run():
    token = load_token()

    # 1. HOME PAGE (CA)
    print("=== CA home-page ===")
    r = http("GET", "/api/home-pages?filters[region][$eq]=ca&populate=*&pagination[pageSize]=1", token)
    entries = r.get("data", [])
    if not entries:
        print("  no CA home found")
    else:
        e = entries[0]
        before = list(e.get("seoKeywords") or [])
        updated = copy.deepcopy(e)
        new_kw, added = merge_keywords(before, NEW_KEYWORDS)
        updated["seoKeywords"] = new_kw
        # home has no definitionalLede; skip sentence
        if added:
            r2 = put_entry("home-pages", e["documentId"], updated, token)
            ok = "error" not in r2
            print(f"  {'OK' if ok else 'ERR'} docId={e['documentId']} kw_added={len(added)}")
            for a in added:
                print(f"      + {a}")
            if not ok: print(f"      !! {r2['error']}")
        else:
            print("  clean — all keywords already present")

    # 2. SERVICE PAGES (CA)
    for slug in SERVICE_SLUGS:
        print(f"\n=== CA service-pages / {slug} ===")
        r = http("GET", f"/api/service-pages?filters[slug][$eq]={slug}&populate=*", token)
        entries = r.get("data", [])
        if not entries:
            print("  not found")
            continue
        e = entries[0]
        updated = copy.deepcopy(e)
        before_kw = list(e.get("seoKeywords") or [])
        new_kw, added_kw = merge_keywords(before_kw, SERVICE_KEYWORDS)
        updated["seoKeywords"] = new_kw

        lede_change = False
        if e.get("definitionalLede"):
            new_lede, lede_change = append_sentence(e["definitionalLede"], STANDARDS_SENTENCE)
            if lede_change:
                updated["definitionalLede"] = new_lede

        if added_kw or lede_change:
            r2 = put_entry("service-pages", e["documentId"], updated, token)
            ok = "error" not in r2
            print(f"  {'OK' if ok else 'ERR'} kw_added={len(added_kw)} lede_appended={lede_change}")
            for a in added_kw:
                print(f"      + keyword: {a}")
            if lede_change:
                print(f"      + lede sentence appended")
            if not ok: print(f"      !! {r2['error']}")
        else:
            print("  clean — keywords already present, lede already contains sentence")


if __name__ == "__main__":
    run()
