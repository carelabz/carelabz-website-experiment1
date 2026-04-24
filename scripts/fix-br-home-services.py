"""Fix BR HomePage.services array so every href matches a real ServicePage."""
import json
import urllib.request
import urllib.error

STRAPI = "https://rational-cheese-8e8c4f80ea.strapiapp.com"
TOKEN = ""
with open(".env.local", encoding="utf-8") as f:
    for line in f:
        if line.startswith("STRAPI_API_TOKEN="):
            TOKEN = line.split("=", 1)[1].strip().strip('"').strip("'")
            break


def http(method, path, body=None):
    req_body = json.dumps({"data": body}).encode() if body else None
    headers = {"Authorization": f"Bearer {TOKEN}"}
    if req_body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        STRAPI + path, data=req_body, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        return {"__error": f"HTTP {e.code}: {e.read().decode('utf-8','replace')[:300]}"}


DOCUMENT_ID = "w4i3qphytvq32dmbi92vpblz"

# Match the 5 real ServicePage entries under region=br
NEW_SERVICES = [
    {
        "title": "Arc Flash Study",
        "description": "IEEE 1584 arc flash hazard analysis with incident-energy calculations, PPE category labels, and NR-10-aligned mitigation for every bus.",
        "icon": "zap",
        "href": "/br/arc-flash-study/",
    },
    {
        "title": "Harmonic Study & Analysis",
        "description": "Identify harmonic distortion, locate resonance risks, and size passive or active filters to bring your facility back inside the limits.",
        "icon": "bar-chart",
        "href": "/br/harmonic-study-and-analysis/",
    },
    {
        "title": "Motor Start Analysis",
        "description": "Predict the voltage dip, torque profile, and breaker response before you start a large motor — avoid nuisance trips and stalled loads.",
        "icon": "settings",
        "href": "/br/motor-start-analysis/",
    },
    {
        "title": "Power System Study & Analysis",
        "description": "Load flow, short circuit, protection coordination, and transient analysis in a single ETAP-based study with digital deliverables.",
        "icon": "search",
        "href": "/br/power-system-study-and-analysis/",
    },
    {
        "title": "Power Quality Analysis",
        "description": "Measure voltage stability, sags, transients, and harmonics; pinpoint the source of equipment failures; deliver ranked remediation.",
        "icon": "thermometer",
        "href": "/br/power-quality-analysis/",
    },
]


def main():
    r = http("PUT", f"/api/home-pages/{DOCUMENT_ID}", {"services": NEW_SERVICES})
    if "__error" in r:
        print(f"ERR: {r['__error']}")
        return
    print("Updated BR HomePage.services:")
    for s in NEW_SERVICES:
        print(f"  {s['title']:<32} -> {s['href']}")


if __name__ == "__main__":
    main()
