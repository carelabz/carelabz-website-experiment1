"""One-shot: replace "CareLabs" with "Carelabs" in ALL Strapi entries (us + ca).

Preserves protected tokens:
- carelabz.com (domain)
- carelabs-logo.svg (logo filename)
- linkedin.com/company/carelabs, twitter.com/carelabz, facebook.com/carelabz
- any @carelabz.* email
"""
from __future__ import annotations

import copy
import json
import re
import urllib.error
import urllib.request

STRAPI_URL = "https://rational-cheese-8e8c4f80ea.strapiapp.com"


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


def fix_string(s: str) -> str:
    if not isinstance(s, str):
        return s
    placeholder_map = {}
    protected = re.compile(
        r"(https?://[^\s\"'<>]*carelab[zs][^\s\"'<>]*|"
        r"[a-zA-Z0-9._%+-]+@carelab[zs]\.[a-zA-Z]+|"
        r"carelabs-logo\.[a-zA-Z]+|"
        r"/carelab[zs]/|"
        r"carelab[zs]\.com)"
    )
    def _protect(m):
        k = f"\x00P{len(placeholder_map)}\x00"
        placeholder_map[k] = m.group(0)
        return k
    out = protected.sub(_protect, s)
    # Primary fix: CareLabs -> Carelabs
    out = re.sub(r"\bCareLabs\b", "Carelabs", out)
    # Also catch other known bad casings
    out = re.sub(r"\bCARELABS\b", "Carelabs", out)
    out = re.sub(r"\bCareLAbz\b", "Carelabs", out)
    out = re.sub(r"\bCare Labs\b", "Carelabs", out)
    for k, v in placeholder_map.items():
        out = out.replace(k, v)
    return out


def deep_fix(obj):
    if isinstance(obj, str):
        return fix_string(obj)
    if isinstance(obj, dict):
        return {k: deep_fix(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [deep_fix(i) for i in obj]
    return obj


def count_carelabs(obj) -> int:
    text = json.dumps(obj, ensure_ascii=False)
    text = re.sub(r"https?://[^\s\"'<>]*carelab[zs][^\s\"'<>]*", "", text)
    text = re.sub(r"@carelab[zs]\.[a-zA-Z]+", "", text)
    text = re.sub(r"carelab[zs]\.com", "", text)
    text = re.sub(r"carelabs-logo\.[a-zA-Z]+", "", text)
    text = re.sub(r"/carelab[zs]/", "", text)
    return len(re.findall(r"\bCareLabs\b", text))


def put_entry(collection: str, doc_id: str, payload: dict, token: str) -> dict:
    STRIP_TOP = {"id", "documentId", "createdAt", "updatedAt", "publishedAt", "locale", "localizations"}

    def deep_strip_id(obj):
        if isinstance(obj, dict):
            return {k: deep_strip_id(v) for k, v in obj.items() if k != "id"}
        if isinstance(obj, list):
            return [deep_strip_id(i) for i in obj]
        return obj

    clean_top = {k: v for k, v in payload.items() if k not in STRIP_TOP}
    return http("PUT", f"/api/{collection}/{doc_id}", token, deep_strip_id(clean_top))


def list_all(collection: str, region: str, token: str) -> list:
    out = []
    page = 1
    while True:
        path = f"/api/{collection}?filters[region][$eq]={region}&pagination[page]={page}&pagination[pageSize]=100&populate=*"
        r = http("GET", path, token)
        data = r.get("data", []) or []
        out.extend(data)
        meta = r.get("meta", {}).get("pagination", {})
        if page >= meta.get("pageCount", 1):
            break
        page += 1
    return out


def run():
    token = load_token()
    total_updates = 0
    total_fails = 0
    per_collection = {}

    COLLECTIONS = ["service-pages", "home-pages", "blog-posts", "about-pages", "contact-pages"]

    for region in ("ca", "us"):
        print(f"\n========== REGION = {region} ==========")
        for collection in COLLECTIONS:
            entries = list_all(collection, region, token)
            print(f"\n  {collection} ({len(entries)} entries)")
            ok_ct = 0
            clean_ct = 0
            fail_ct = 0
            for e in entries:
                before_count = count_carelabs(e)
                if before_count == 0:
                    clean_ct += 1
                    continue
                fixed = deep_fix(copy.deepcopy(e))
                r = put_entry(collection, e["documentId"], fixed, token)
                if "error" in r:
                    fail_ct += 1
                    print(f"    ERR {e.get('slug','?'):50s} found={before_count} :: {r['error'][:120]}")
                else:
                    ok_ct += 1
                    print(f"    OK  {e.get('slug','?'):50s} fixed={before_count}")
            per_collection[f"{region}/{collection}"] = {"ok": ok_ct, "clean": clean_ct, "fail": fail_ct}
            total_updates += ok_ct
            total_fails += fail_ct

    print()
    print(f"DONE. Updated {total_updates} entries, {total_fails} failures.")
    for k, v in per_collection.items():
        if v["ok"] or v["fail"]:
            print(f"  {k}: {v}")
    with open("data/strapi-payloads/spelling-fix-report.json", "w", encoding="utf-8") as f:
        json.dump({"updates": total_updates, "failures": total_fails, "per_collection": per_collection}, f, indent=2)


if __name__ == "__main__":
    run()
