"""Diagnose BR homepage service cards vs ServicePage entries."""
import json
import urllib.request

STRAPI = "https://rational-cheese-8e8c4f80ea.strapiapp.com"
TOKEN = ""
with open(".env.local", encoding="utf-8") as f:
    for line in f:
        if line.startswith("STRAPI_API_TOKEN="):
            TOKEN = line.split("=", 1)[1].strip().strip('"').strip("'")
            break


def get(path):
    req = urllib.request.Request(
        STRAPI + path, headers={"Authorization": f"Bearer {TOKEN}"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


home = get("/api/home-pages?filters[region][$eq]=br&populate=*")
print("=== HomePage.services array ===")
entries = home.get("data", [])
if entries:
    svc = entries[0].get("services") or []
    for s in svc:
        print(f"  {s.get('title'):<40}  href={s.get('href')}  icon={s.get('icon')}")
    print(f"\n  documentId: {entries[0].get('documentId')}")
else:
    print("  (no BR HomePage found)")

print()
print("=== ServicePage entries for BR ===")
pages = get(
    "/api/service-pages?filters[region][$eq]=br&fields[0]=title"
    "&fields[1]=slug&fields[2]=documentId&pagination[pageSize]=100"
)
for p in pages.get("data", []):
    print(f"  {p.get('slug'):<45}  title={p.get('title')}")
