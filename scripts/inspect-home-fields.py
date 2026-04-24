"""Inspect key HomePage fields for all 5 SA countries."""
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
    d = get(f"/api/home-pages?filters[region][$eq]={cc}&populate=*")
    if not d.get("data"):
        continue
    h = d["data"][0]
    doc = h.get("documentId")
    sh = h.get("servicesHeading")
    ss = h.get("servicesSubtext")
    ih = h.get("insightsHeading")
    ind = h.get("industries") or []
    print(f"=== {cc.upper()} === {doc}")
    print(f"  servicesHeading: {sh!r}")
    print(f"  servicesSubtext: {ss!r}")
    print(f"  insightsHeading: {ih!r}")
    print(f"  industries: {len(ind)} items -> {[i.get('name') for i in ind[:5]]}")
    print()
