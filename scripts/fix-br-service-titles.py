"""One-off: fix duplicate BR service titles in Strapi."""
import json
import os
import urllib.request

STRAPI = "https://rational-cheese-8e8c4f80ea.strapiapp.com"

TOKEN = ""
with open(".env.local", encoding="utf-8") as f:
    for line in f:
        if line.startswith("STRAPI_API_TOKEN="):
            TOKEN = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

assert TOKEN, "STRAPI_API_TOKEN not found"


def http(method: str, path: str, body=None):
    req_body = json.dumps({"data": body}).encode() if body else None
    headers = {"Authorization": f"Bearer {TOKEN}"}
    if req_body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        STRAPI + path, data=req_body, headers=headers, method=method
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


# Mapping: slug substring -> correct title
TITLE_MAP = [
    ("arc-flash", "Arc Flash Study"),
    ("harmonic", "Harmonic Study & Analysis"),
    ("motor-start", "Motor Start Analysis"),
    ("power-system-study", "Power System Study & Analysis"),
    ("power-quality", "Power Quality Analysis"),
]


def correct_title(slug: str):
    for sub, title in TITLE_MAP:
        if sub in slug:
            return title
    return None


def main():
    qs = (
        "filters[region][$eq]=br"
        "&fields[0]=title&fields[1]=slug&fields[2]=documentId"
        "&pagination[pageSize]=100"
    )
    data = http("GET", f"/api/service-pages?{qs}")
    entries = data.get("data", [])
    print(f"Found {len(entries)} BR service pages.\n")

    updated = skipped = failed = 0
    for e in entries:
        doc_id = e.get("documentId")
        slug = e.get("slug") or ""
        current_title = e.get("title") or ""
        new_title = correct_title(slug)

        if not new_title:
            print(f"  [?] {slug}: no title mapping, skipping")
            skipped += 1
            continue

        if current_title == new_title:
            print(f"  [=] {slug}: already \"{new_title}\"")
            skipped += 1
            continue

        try:
            http("PUT", f"/api/service-pages/{doc_id}", {"title": new_title})
            print(f"  [OK] {slug}: \"{current_title}\" -> \"{new_title}\"")
            updated += 1
        except Exception as exc:
            print(f"  [ERR] {slug}: {exc}")
            failed += 1

    print(f"\nSummary: {updated} updated, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
