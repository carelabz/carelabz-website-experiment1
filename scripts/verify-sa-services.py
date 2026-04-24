"""Verify service field counts for each country."""
import json
import urllib.request

TOKEN = ""
with open(".env.local", encoding="utf-8") as f:
    for l in f:
        if l.startswith("STRAPI_API_TOKEN="):
            TOKEN = l.split("=", 1)[1].strip().strip('"').strip("'")
            break


def get(path):
    req = urllib.request.Request(
        "https://rational-cheese-8e8c4f80ea.strapiapp.com" + path,
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


for cc in ["br", "co", "cl", "ar", "pe"]:
    d = get(
        f"/api/service-pages?filters[region][$eq]={cc}&populate=*&pagination[pageSize]=20"
    )
    print(f"\n=== {cc.upper()} ===")
    for e in d.get("data", []):
        slug = e.get("slug")
        title = e.get("title")
        nf = len(e.get("features") or [])
        ns = len(e.get("processSteps") or [])
        nb = len(e.get("safetyBullets") or [])
        nq = len(e.get("faqs") or [])
        md = e.get("metaDescription") or ""
        dl = e.get("definitionalLede") or ""
        print(
            f"  {slug:<40} {title:<35} "
            f"f={nf} s={ns} sb={nb} q={nq}  "
            f"meta={len(md):>3}ch  lede={len(dl):>3}ch"
        )
