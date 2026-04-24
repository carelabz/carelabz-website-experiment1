"""Snapshot of current Strapi state for CO/CL/AR/PE: blogs + services + home."""
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


for cc in ["co", "cl", "ar", "pe"]:
    print(f"\n=== {cc.upper()} ===")
    # blog posts
    d = get(
        f"/api/blog-posts?filters[region][$eq]={cc}"
        "&fields[0]=documentId&fields[1]=slug&fields[2]=title"
        "&pagination[pageSize]=100"
    )
    blogs = d.get("data", [])
    print(f"  BLOGS ({len(blogs)}):")
    for e in blogs:
        t = (e.get("title") or "")[:70]
        print(f"    {e.get('documentId')}  {e.get('slug'):<55}  {t}")

    # service pages
    d = get(
        f"/api/service-pages?filters[region][$eq]={cc}"
        "&fields[0]=documentId&fields[1]=slug&fields[2]=title"
        "&pagination[pageSize]=20"
    )
    services = d.get("data", [])
    print(f"  SERVICES ({len(services)}):")
    for e in services:
        print(f"    {e.get('documentId')}  {e.get('slug'):<45}  {e.get('title')}")

    # home
    d = get(f"/api/home-pages?filters[region][$eq]={cc}&populate=*")
    home = d.get("data", [])
    if home:
        svc = home[0].get("services") or []
        print(f"  HOME.services ({len(svc)}):   documentId={home[0].get('documentId')}")
        for s in svc:
            print(f"    {s.get('title'):<40}  -> {s.get('href')}")
