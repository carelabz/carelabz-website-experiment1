"""Seed CO / CL / AR / PE Strapi with parameterized content from the BR template.

Every country's WordPress source at www.carelabz.com/{cc}/ has the same
10 blog articles and 5 service pages, templated with country-name
substitutions. Carelabs' BR content has already been written to Strapi;
this script reuses those templates and applies per-country substitutions
for country name, adjective, primary/secondary standards, cities, etc.

Per country, this script:
  1. DELETEs WordPress artifacts (admin/uncategorized/404 pages)
  2. DELETEs bare-slug duplicates (keeps only -{cc} suffixed entries)
  3. PUTs unique titles + full content on the 5 service pages
  4. PUTs clean titles + meta + bodies on the legitimate blog posts
  5. PUTs the corrected HomePage.services array matching real slugs

Usage:  python scripts/seed-sa-content.py           # all 4 countries
        python scripts/seed-sa-content.py co        # single country
"""
from __future__ import annotations

import json
import sys
import urllib.request
import urllib.error

STRAPI = "https://rational-cheese-8e8c4f80ea.strapiapp.com"
TOKEN = ""
with open(".env.local", encoding="utf-8") as f:
    for line in f:
        if line.startswith("STRAPI_API_TOKEN="):
            TOKEN = line.split("=", 1)[1].strip().strip('"').strip("'")
            break
assert TOKEN, "STRAPI_API_TOKEN missing"


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


# ═══ Per-country configuration ═══════════════════════════════════════════

COUNTRIES = {
    "co": {
        "name": "Colombia",
        "adj": "Colombian",
        "primary": "RETIE",
        "secondary": "NTC 2050",
        "authority": "Ministerio de Minas y Energía",
        "cities": "Bogotá, Medellín, Cali, and Barranquilla",
        "home_doc_id": "t2wg8thwq1tqjcxqwjfdikfe",
    },
    "cl": {
        "name": "Chile",
        "adj": "Chilean",
        "primary": "NCh Elec. 4/2003",
        "secondary": "NSEG 5 En. 71",
        "authority": "SEC (Superintendencia de Electricidad y Combustibles)",
        "cities": "Santiago, Valparaíso, Antofagasta, and Concepción",
        "home_doc_id": "jabw21hk6nlgo95teix28lmj",
    },
    "ar": {
        "name": "Argentina",
        "adj": "Argentine",
        "primary": "AEA 90364",
        "secondary": "IRAM 2281",
        "authority": "ENRE",
        "cities": "Buenos Aires, Córdoba, Rosario, and Mendoza",
        "home_doc_id": "ss2pi7z36f6od5zdgz8i5nr8",
    },
    "pe": {
        "name": "Peru",
        "adj": "Peruvian",
        "primary": "RM 111-2013-MEM",
        "secondary": "CNE",
        "authority": "OSINERGMIN",
        "cities": "Lima, Arequipa, Trujillo, and Chiclayo",
        "home_doc_id": "jblvrpzicea6j22sn4lkm939",
    },
}

# Service documentIds per country (from Strapi query)
SERVICE_DOC_IDS = {
    "co": {
        "arc-flash-study": "ns1ihr8r7qpn9wfnlrizboqs",
        "harmonic-study-and-analysis": "ylbm7gsit54xslfziq1qpx4r",
        "motor-start-analysis": "v0o7u2tq68qyedwuck67qph3",
        "power-system-study-and-analysis": "g2gd5he8xuo7hzshn95b8qie",
        "power-quality-analysis": "j15tgqt8ax4lvk7lbohc39im",
    },
    "cl": {
        "arc-flash-study": "qbecghnj3enf7clb1sxza6ux",
        "harmonic-study-and-analysis": "hhwacnue0a3ldbu9zeog583h",
        "motor-start-analysis": "oxi8rmjwp712bcht08eyhh39",
        "power-system-study-and-analysis": "q1e9e20jpucukpoqk8h6m0rk",
        "power-quality-analysis": "f4i9mfkornfe45w714u8c41a",
    },
    "ar": {
        "arc-flash-study": "s20jebeelt2aumy4fgzub1sq",
        "harmonic-study-and-analysis": "ejsstlp46nhvktexup5lbq8m",
        "motor-start-analysis": "zw4plmfczdojvk2qvkc3o14r",
        "power-system-study-and-analysis": "lgwhcunbxffpcl03pvsfyh5u",
        "power-quality-analysis": "ta99eeai49me8rs65gwlhio3",
    },
    "pe": {
        "arc-flash-study": "t3c5dbrkmkx7lecouyeg2nfw",
        "harmonic-study-and-analysis": "xaz1j9n1gbc7bnk2a6tz9581",
        "motor-start-analysis": "o5md0pvcnoy0o5t3n9n30o3p",
        "power-system-study-and-analysis": "si5uque70csluuwcn4arubog",
        "power-quality-analysis": "iprb55gsx40n3yx356rymbyj",
    },
}

# Blog entries per country — sourced from Strapi snapshot.
# Format per entry:  (documentId, slug, action)
#   action = 'keep' -> update with parameterized content
#   action = 'delete' -> DELETE artifact / bare duplicate
BLOG_LEDGER = {
    "co": [
        # artifacts
        ("oyzagmesgpv3o1myxkhv253l", "404-page-co", "delete"),
        ("t2wju17ham4hl75mds3if6wh", "admin_co", "delete"),
        ("u4jqxfn12ukgxkuy4y3n3dba", "admin_co-co", "delete"),
        ("rs92ryc3w7plj4h22v7q3x3p", "uncategorized-co", "delete"),
        # bare-slug duplicates (no -co suffix)
        ("jh2gyii0ikzemqukkn08e1s2", "harmonic-analysis-of-the-colombian-power-system", "delete"),
        ("owzcim11o8y8h3d5weh4tpvc", "examine-and-confirm-electrical-motor-performance-in-compliance-with-colombian-regulations", "delete"),
        ("yapgsavfljztc12x67k9id5w", "principles-of-power-quality-work-in-colombia", "delete"),
        ("u6v6st2cx7yxivp8o3x6vv38", "how-to-perform-a-power-quality-analysis-in-colombia", "delete"),
        ("z9zxlqvdynikzdoqbwmkauay", "why-are-harmonic-analysis-and-study-important-for-businesses-in-colombia", "delete"),
        # legit -co entries
        ("u4vkki8skx5wbfnwgaw6xwa9", "arc-flash-analysis-in-colombia-a-detailed-guide-co", "keep:arc_flash_guide"),
        ("icmi3q8sbssc9irezuf1wtpf", "assessing-and-lowering-the-danger-of-an-arc-flash-is-crucial-co", "keep:arc_flash_assessing"),
        ("g902cqrqatjh32cffj4ljya4", "how-can-efficiency-and-reliability-of-commercial-motors-be-evaluated-co", "keep:motor_efficiency"),
        ("c58paj0nhj20vv717wvx8m35", "why-are-harmonic-analysis-and-study-important-for-businesses-in-colombia-co", "keep:harmonic_why"),
        ("wjjkj3gitc8p4efr1143g894", "harmonic-analysis-of-the-colombian-power-system-co", "keep:harmonic_system"),
        ("p4k92q553m97hxa01puupmjp", "principles-of-power-quality-work-in-colombia-co", "keep:power_quality_principles"),
        ("hpkdenmdbsa6e6shr9e5ip5f", "how-to-perform-a-power-quality-analysis-in-colombia-co", "keep:power_quality_howto"),
        ("jj6igr76yzl02329xcpgeb9r", "why-load-flow-and-short-circuit-analysis-important-for-colombian-business-co", "keep:load_flow_why"),
        ("fit43byj3bmuipqb2i0friqv", "load-flow-short-circuit-and-relay-coordination-in-power-system-analysis-co", "keep:load_flow_triad"),
        ("fxms1uh01iz9v8kp1e6qkf31", "examine-and-confirm-electrical-motor-performance-in-compliance-with-colombian-regulations-co", "keep:motor_compliance"),
    ],
    "cl": [
        ("bs9h9r0k1vdhfo27so2jw9nk", "404-page-cl", "delete"),
        ("cpwge5nfpxr0c6kn2vsc4584", "admin_cl", "delete"),
        ("g3cw3jam8fc6ph2887nplo2i", "admin_cl-cl", "delete"),
        ("jedyhl7kv496k7bfvdr9whae", "uncategorized-cl", "delete"),
        ("w93t9bjljdkzc0kaih6csxvp", "harmonic-analysis-of-the-chile-power-system", "delete"),
        ("uh0pwjtgwt9kztz3r9wxmfsr", "arc-flash-analysis-in-chile-a-detailed-guide", "delete"),
        ("mdl5l1n8oonwb0eiqaa6w3k8", "examine-and-confirm-electrical-motor-performance-in-compliance-with-chilean-regulations", "delete"),
        ("gki2emvl4p41l3r2605dahwi", "how-to-perform-a-power-quality-analysis-in-chile", "delete"),
        ("kgnr11fyyr40cps6j0zxyfkx", "principles-of-power-quality-work-in-chile", "delete"),
        ("kt7xdth5gozj6zoj2qnrmiqj", "why-are-harmonic-analysis-and-study-important-for-businesses-in-chile", "delete"),
        ("cwn2qk3yyzsbgjes8qg1pm1b", "why-load-flow-and-short-circuit-analysis-important-for-chilean-business", "delete"),
        ("jczjhsd6lq9mc9le1dj3n27j", "arc-flash-analysis-in-chile-a-detailed-guide-cl", "keep:arc_flash_guide"),
        ("kyzssnislaa75lq4tx67ptkj", "assessing-and-lowering-the-danger-of-an-arc-flash-is-crucial-cl", "keep:arc_flash_assessing"),
        ("r63q3q5k4td03oxoq5bvmjbe", "how-can-efficiency-and-reliability-of-commercial-motors-be-evaluated-cl", "keep:motor_efficiency"),
        ("wgfu3frqy1ibi8g6fjeiech1", "why-are-harmonic-analysis-and-study-important-for-businesses-in-chile-cl", "keep:harmonic_why"),
        ("iuw38jyxy40b6uxfv68abb5e", "harmonic-analysis-of-the-chile-power-system-cl", "keep:harmonic_system"),
        ("f171tk7kw5ntvtuhtkmecn9o", "principles-of-power-quality-work-in-chile-cl", "keep:power_quality_principles"),
        ("nvp3gtcegfxve9f5zz4t6i5e", "how-to-perform-a-power-quality-analysis-in-chile-cl", "keep:power_quality_howto"),
        ("wzlilnzagfzbya2klyiqftd1", "why-load-flow-and-short-circuit-analysis-important-for-chilean-business-cl", "keep:load_flow_why"),
        ("axa2o9nafbsqin0y1pqxdog7", "load-flow-short-circuit-and-relay-coordination-in-power-system-analysis-cl", "keep:load_flow_triad"),
        ("p5i4v9sbjp8cxvg4g8vdu4mx", "examine-and-confirm-electrical-motor-performance-in-compliance-with-chilean-regulations-cl", "keep:motor_compliance"),
    ],
    "ar": [
        ("bcw69g8m0ye6nrgevbtpk86j", "404-page-ar", "delete"),
        ("uay1fkiff78hfw5p42gjxfpb", "admin_ar", "delete"),
        ("cxzqzal0o2mroofeifen5d5s", "admin_ar-ar", "delete"),
        ("t4mg6h0edpgv71bv32qwvief", "uncategorized-ar", "delete"),
        ("fwzjpbval6x74akpa14p1g5o", "examine-and-confirm-electrical-motor-performance-in-compliance-with-argentine-regulations", "delete"),
        ("d5u9ur1cx4q2i2k8v0v8feuh", "harmonic-analysis-of-the-argentine-power-system", "delete"),
        ("e62e1ct6lss3asrtu27r7t4z", "how-to-perform-a-power-quality-analysis-in-argentina", "delete"),
        ("okhydyy9ryrevbs0mq5qnxtn", "principles-of-power-quality-work-in-argentina", "delete"),
        ("qvf9drmxzx2ec70rwwix1963", "why-are-harmonic-analysis-and-study-important-for-businesses-in-argentina", "delete"),
        ("wwcfx5guzcn2bb9urjljwteb", "arc-flash-analysis-in-argentina-a-detailed-guide-ar", "keep:arc_flash_guide"),
        ("u7oustoe2kcj84ccn1733i8x", "assessing-and-lowering-the-danger-of-an-arc-flash-is-crucial-ar", "keep:arc_flash_assessing"),
        ("jkyfyjun1cy7chwnteuvnn62", "how-can-efficiency-and-reliability-of-commercial-motors-be-evaluated-ar", "keep:motor_efficiency"),
        ("lkeos10g2n7ibh0estew4obq", "why-are-harmonic-analysis-and-study-important-for-businesses-in-argentina-ar", "keep:harmonic_why"),
        ("jowipdogv5kwd4rdgcrhq0ns", "harmonic-analysis-of-the-argentine-power-system-ar", "keep:harmonic_system"),
        ("nqfu3dbebosas2iyem3n6v5z", "principles-of-power-quality-work-in-argentina-ar", "keep:power_quality_principles"),
        ("l30unvkdrduiree2a8ctza8h", "how-to-perform-a-power-quality-analysis-in-argentina-ar", "keep:power_quality_howto"),
        ("cq3x4ho45bqmyi47jzhhdjji", "why-load-flow-and-short-circuit-analysis-important-for-argentine-business-ar", "keep:load_flow_why"),
        ("f0bnsiipnpe0m8c6v7dey91y", "load-flow-short-circuit-and-relay-coordination-in-power-system-analysis-ar", "keep:load_flow_triad"),
        ("g5zpzybsx2bugj278na2f9o5", "examine-and-confirm-electrical-motor-performance-in-compliance-with-argentine-regulations-ar", "keep:motor_compliance"),
    ],
    "pe": [
        ("wpwbhtspj6izf4stcpjd0we4", "404-page-pe", "delete"),
        ("s3o31jn3dbcjr7v31xfwk1zt", "admin_pe", "delete"),
        ("k5fypg5fna6tqh2je991kbl4", "admin_pe-pe", "delete"),
        ("j2z3hv3e8zovvk6q2ynoxiyv", "uncategorized-pe", "delete"),
        ("eedg3y8a6gxra0yt8tci6jm4", "examine-and-confirm-electrical-motor-performance-in-compliance-with-peruvian-regulations", "delete"),
        ("e6kw0w2iod252azl33m6saa6", "harmonic-analysis-of-the-peru-power-system", "delete"),
        ("j0z9sdiv8o7rzwemldyqye69", "how-to-perform-a-power-quality-analysis-in-peru", "delete"),
        ("bhhj9m8yk1ez34wht55l1iey", "principles-of-power-quality-work-in-peru", "delete"),
        ("e5fjubyikztputj1bizpk8d2", "why-are-harmonic-analysis-and-study-important-for-businesses-in-peru", "delete"),
        ("mwnx95zq8f358ipdx3fkgbo1", "arc-flash-analysis-in-peru-a-detailed-guide-pe", "keep:arc_flash_guide"),
        ("wnmthyergz3o8rrmpx4vb9q8", "assessing-and-lowering-the-danger-of-an-arc-flash-is-crucial-pe", "keep:arc_flash_assessing"),
        ("t0lv3uwq4x31e5sxzyu31l3b", "how-can-efficiency-and-reliability-of-commercial-motors-be-evaluated-pe", "keep:motor_efficiency"),
        ("h0rwa3dpru6upe95wjckozq9", "why-are-harmonic-analysis-and-study-important-for-businesses-in-peru-pe", "keep:harmonic_why"),
        ("b4ay4qtwzi0hpp8vwnjk43qg", "harmonic-analysis-of-the-peru-power-system-pe", "keep:harmonic_system"),
        ("fc8cu5v9cfq9uup9ew2z4a4h", "principles-of-power-quality-work-in-peru-pe", "keep:power_quality_principles"),
        ("wdq4kz7psv72orjruhdzm70g", "how-to-perform-a-power-quality-analysis-in-peru-pe", "keep:power_quality_howto"),
        ("d9zl8s8vh7gbeb1g3i3feber", "why-load-flow-and-short-circuit-analysis-important-for-peruvian-business-pe", "keep:load_flow_why"),
        ("w33zna99vrfyvd7kekoghio6", "load-flow-short-circuit-and-relay-coordination-in-power-system-analysis-pe", "keep:load_flow_triad"),
        ("qk0a7bd1qfvj17l4p0yy2qpa", "examine-and-confirm-electrical-motor-performance-in-compliance-with-peruvian-regulations-pe", "keep:motor_compliance"),
    ],
}

# ═══ Content templates ═══════════════════════════════════════════════════
# Use {country}, {adj}, {primary}, {secondary}, {authority}, {cities}, {cc} placeholders.
# Call render(template, ctx) to substitute.

def render(tpl: str, c: dict) -> str:
    return (
        tpl.replace("{country}", c["name"])
        .replace("{adj}", c["adj"])
        .replace("{primary}", c["primary"])
        .replace("{secondary}", c["secondary"])
        .replace("{authority}", c["authority"])
        .replace("{cities}", c["cities"])
        .replace("{cc}", c["cc"])
    )


def trust_badges(c: dict):
    return [
        {"label": c["primary"]},
        {"label": c["secondary"]},
        {"label": "IEEE 1584"},
        {"label": "ISO 9001:2008"},
    ]


# ───────── SERVICE PAGE TEMPLATES ───────────────────────────────────────

SERVICE_TEMPLATES = {
    "arc-flash-study": {
        "title": "Arc Flash Study",
        "eyebrow": "Electrical Safety",
        "metaTitle_tpl": "Arc Flash Study Services in {country} | Carelabs",
        "metaDescription_tpl": "IEEE 1584 arc flash studies, incident-energy calculations, and {primary}-aligned PPE labelling for {adj} facilities. ISO 9001:2008 accredited.",
        "definitionalLede_tpl": "An arc flash study quantifies the incident energy at every piece of electrical equipment, sets safe approach boundaries, and specifies the PPE category workers must wear. Carelabs delivers IEEE 1584-aligned studies with {primary} mitigation recommendations and ready-to-apply equipment labels.",
        "seoKeywords_tpl": ["arc flash study {country}", "IEEE 1584 arc flash", "{primary} compliance", "incident energy analysis", "PPE category labels"],
        "featuresHeading": "Key Challenges We Solve",
        "featuresSubtext_tpl": "Our engineers identify and resolve arc flash risks before they become costly incidents — with ETAP-based modelling, short-circuit analysis, and protection coordination rolled into every engagement across {country}.",
        "features": [
            ("Incident Energy Calculation", "IEEE 1584 calculations at every relevant bus, with clearing-time sensitivity so you see exactly where faster protection would cut exposure."),
            ("Equipment Labels Ready to Apply", "Printed {primary} / IEEE 1584 labels per panel with incident energy, arc-flash boundary, and required PPE category."),
            ("Short Circuit & Coordination", "Full three-phase, L-G, L-L, and L-L-G fault analysis with protective-device coordination curves."),
            ("Prioritised Mitigation Plan", "Ranked recommendations with cost and incident-energy impact for each option."),
        ],
        "safetyEyebrow": "Worker Safety",
        "safetyHeading": "Protect Your Team from the Most Dangerous Electrical Hazard",
        "safetyBody_tpl": "Arc flash exceeds 19,000 °C — enough to vaporise copper and cause severe burns at distance. Every {adj} facility with switchgear, MCCs, or panelboards has exposure.",
        "safetyBullets": [
            "Eliminate energised work wherever possible; document exceptions",
            "Install remote racking and arc-flash detection where exposure is high",
            "Train every qualified worker annually and audit the training",
            "Match PPE category to the calculated incident energy at each task",
            "Keep labels current — re-study after any system change",
        ],
        "reportsEyebrow": "Deliverables",
        "reportsHeading": "Comprehensive Report Package",
        "reportsBody_tpl": "Every arc flash engagement ends with a digital report package aligned with IEEE 1584 and {primary}. Your team gets everything they need for compliance audits and daily operations.",
        "reportsBullets": [
            "Updated single-line diagrams and equipment inventory",
            "Short-circuit, coordination, and incident-energy results bus-by-bus",
            "Printed labels for every panel and piece of switchgear",
            "Ranked mitigation plan with estimated cost and incident-energy reduction",
            "Executive summary plus a full technical appendix for engineering review",
        ],
        "processSteps": [
            ("Data Collection", "On-site walkdown to capture single-line diagrams, nameplate data, cable lengths, and existing protection settings."),
            ("ETAP Modelling", "Build the power system model in ETAP, run short-circuit analysis, and coordinate protection devices."),
            ("Arc Flash Calculation", "IEEE 1584 incident-energy calculations, arc-flash boundary determination, and PPE category selection."),
            ("Labels & Report", "Print equipment labels, document findings, rank mitigation options, and deliver the final report package."),
        ],
        "faqs": [
            ("What is an arc flash study?", "An arc flash study calculates the incident energy available at every piece of energised electrical equipment in your facility. The results define safe approach boundaries and the PPE category workers must wear, as required by {primary} and IEEE 1584."),
            ("How often should an arc flash study be updated?", "Every five years at minimum, and immediately after any change that affects fault current — new transformer, new generation source, significant load addition, or upstream utility upgrade."),
            ("Which standard does Carelabs follow for arc flash analysis in {country}?", "IEEE 1584 for the calculation method and {primary} for the {adj} regulatory framework. Our reports are accepted by {authority} and major utility clients."),
            ("Can arc flash risk be eliminated?", "Not eliminated, but reduced dramatically. Faster protection clearing times, arc-resistant switchgear, remote racking, and bus segmentation can cut incident energy by an order of magnitude."),
            ("How long does a typical arc flash study take?", "For a mid-size industrial plant, expect 3–6 weeks from site visit to final report — faster if drawings are current and protection-relay settings are documented."),
        ],
        "ctaBannerHeading": "Ready to Schedule Your Arc Flash Study?",
        "ctaBannerBody_tpl": "Our ISO 9001:2008-accredited engineers deliver IEEE 1584 studies across {cities} Fast turnaround, clear reports, full {primary} compliance support.",
    },
    "harmonic-study-and-analysis": {
        "title": "Harmonic Study & Analysis",
        "eyebrow": "Power Quality",
        "metaTitle_tpl": "Harmonic Study & Analysis in {country} | Carelabs",
        "metaDescription_tpl": "Identify harmonic distortion, locate resonance risks, and size mitigation with ETAP-based harmonic studies for {adj} facilities.",
        "definitionalLede_tpl": "Harmonic distortion shortens equipment life, raises energy bills, and increases the risk of nuisance tripping. A Carelabs harmonic study measures distortion at the point of common coupling, models your system in ETAP, and sizes the mitigation that brings you back within limits.",
        "seoKeywords_tpl": ["harmonic study {country}", "harmonic analysis", "IEEE 519", "total harmonic distortion THD", "power quality filter"],
        "featuresHeading": "What a Harmonic Study Reveals",
        "featuresSubtext_tpl": "Harmonics from variable-speed drives, UPS systems, and LED lighting disrupt more than just power quality — they drive transformer overheating, capacitor failures, and relay misoperation in {adj} facilities.",
        "features": [
            ("Point of Common Coupling Measurement", "Measure voltage and current THD at the PCC using calibrated analysers and benchmark against IEEE 519."),
            ("Resonance Risk Detection", "Identify parallel and series resonance points where capacitor banks amplify specific harmonic orders."),
            ("Load-by-Load Spectrum", "Characterise every nonlinear load — VFDs, rectifiers, UPS — so mitigation is sized correctly."),
            ("Mitigation Sizing", "Passive filter, active filter, or drive-side reactor: we model each option in ETAP and show you which hits your target for the lowest capex."),
        ],
        "safetyEyebrow": "Equipment Protection",
        "safetyHeading": "Catch Harmonic Damage Before It Shows Up",
        "safetyBody_tpl": "Harmonic distortion silently overheats transformers, trips breakers, and ages motors faster. Annual monitoring catches it early.",
        "safetyBullets": [
            "Neutral conductors overload on 3rd and 9th harmonics — detect early",
            "Capacitor banks fail prematurely when they resonate with system inductance",
            "Motors run hotter and lose efficiency as THD rises above 8%",
            "Protective relays misoperate when waveforms distort beyond rated limits",
            "Energy bills climb as reactive power and losses compound",
        ],
        "reportsEyebrow": "Deliverables",
        "reportsHeading": "What's in Your Harmonic Report",
        "reportsBody_tpl": "Every Carelabs harmonic report includes measured data, ETAP simulation results, and a sized mitigation plan — digital PDF plus raw measurement files.",
        "reportsBullets": [
            "Individual and total harmonic distortion (THD) at every measured bus",
            "Harmonic frequency spectrum plots with dominant orders flagged",
            "Resonance sweep showing parallel/series risk across the audible range",
            "Mitigation design — filter rating, placement, and expected post-install THD",
            "Compliance gap analysis against IEEE 519 limits",
        ],
        "processSteps": [
            ("Single-Line Review", "Mark every nonlinear load, capacitor bank, and long medium-voltage cable on the drawing."),
            ("On-site Measurement", "Connect power-quality analysers at the PCC and sensitive buses for a 7–14 day recording window."),
            ("ETAP Modelling", "Build the harmonic model, run frequency-domain analysis, and calculate THD per bus."),
            ("Mitigation Design", "Size the filter or reactor, re-run the model with mitigation in place, and verify compliance."),
        ],
        "faqs": [
            ("When does a {adj} facility need a harmonic study?", "When nonlinear load exceeds 15% of total bus load, when you're adding VFDs or UPS capacity, when a new capacitor bank is planned, or when equipment is failing without an obvious cause."),
            ("What are the harmonic limits in {country}?", "IEEE 519 guidance is widely adopted — typically 5% voltage THD for systems below 1 kV and 3% for medium-voltage. Current THD limits depend on the short-circuit ratio at your connection point."),
            ("Passive filter or active filter — which is right for my site?", "Passive filters are cheaper and handle a single dominant harmonic order well. Active filters handle wider spectra and changing load conditions. Our study tells you which matches your actual load profile."),
            ("How long does a harmonic study take?", "Two to four weeks end-to-end: measurement window is the bottleneck, usually 7–14 days of continuous recording."),
            ("Will a harmonic study shut down my plant?", "No. Measurements are taken non-intrusively at existing metering points. The only disruption is when we install temporary analysers."),
        ],
        "ctaBannerHeading": "Bring Your Facility Back Within Harmonic Limits",
        "ctaBannerBody_tpl": "Carelabs engineers deliver ETAP-based harmonic studies across {cities} Digital reports, ranked mitigation, IEEE 519 compliance.",
    },
    "motor-start-analysis": {
        "title": "Motor Start Analysis",
        "eyebrow": "Power System Engineering",
        "metaTitle_tpl": "Motor Start Analysis in {country} | Carelabs",
        "metaDescription_tpl": "Predict voltage dip, torque profile, and breaker response before starting a large motor. ETAP-based motor starting studies for {adj} industrial facilities.",
        "definitionalLede_tpl": "Starting a large motor on a weak bus can drop terminal voltage below 80% of nameplate, stall connected loads, and trip upstream breakers. A Carelabs motor start analysis models the event in ETAP and tells you — before you hit the button — what will happen.",
        "seoKeywords_tpl": ["motor start analysis {country}", "motor starting study", "voltage dip", "ETAP transient analysis", "soft starter sizing"],
        "featuresHeading": "Questions a Motor Start Study Answers",
        "featuresSubtext_tpl": "Motor starting is the single most disruptive event a {adj} facility's electrical system sees. Knowing the outcome in advance saves you from nuisance trips, stalled loads, and commissioning delays.",
        "features": [
            ("Can the Supply Start the Motor?", "Calculate voltage dip at the motor terminals and every sensitive bus — check that terminal voltage stays above 80% of rated as the motor accelerates."),
            ("Will the Motor Reach Full Speed?", "Compare motor torque-speed curve against load torque-speed curve. If they cross before synchronous speed, the motor will stall."),
            ("What Breaker Will Trip?", "Check protective-device coordination through the starting transient — inrush peaks should ride through without tripping upstream."),
            ("Do You Need a Soft Starter?", "If direct-on-line starting violates limits, we size the soft starter, VFD, or autotransformer that restores compliance."),
        ],
        "safetyEyebrow": "Equipment Protection",
        "safetyHeading": "Protect Downstream Loads From Motor-Start Transients",
        "safetyBody_tpl": "Voltage drops during motor starts affect everything on the bus — lighting, PLCs, drives, instrumentation. Modelling the transient protects the whole plant.",
        "safetyBullets": [
            "Terminal voltage must stay at or above 80% of rated during acceleration",
            "Starting current typically 5–7× full-load amps for direct-on-line starts",
            "Supply transformer trips if motor exceeds 30% of base kVA on DOL start",
            "Generator-only supplies need the motor to stay below 10–15% of kVA rating",
            "Sensitive electronics on the same bus need voltage-ride-through verified",
        ],
        "reportsEyebrow": "Deliverables",
        "reportsHeading": "Motor Start Report Contents",
        "reportsBody_tpl": "Every motor start report includes time-domain simulations, starting-current curves, voltage-recovery plots, and a clear go/no-go recommendation for direct-on-line start.",
        "reportsBullets": [
            "Voltage vs time at motor terminals and every sensitive bus",
            "Current vs time from inrush through steady-state",
            "Motor and load torque-speed curves with acceleration margin",
            "Starter sizing and settings when DOL is not viable",
            "Recommendations for bus configuration during start",
        ],
        "processSteps": [
            ("Data Collection", "Motor nameplate, starting impedance, load inertia, and supply short-circuit data."),
            ("Baseline Simulation", "Model direct-on-line start in ETAP and evaluate voltage dip, acceleration time, and breaker behaviour."),
            ("Starter Evaluation", "If DOL fails, simulate soft starter, VFD, autotransformer options until you have one that meets limits."),
            ("Report & Settings", "Deliver the report plus recommended protective-relay settings tuned for the start transient."),
        ],
        "faqs": [
            ("When is a motor start analysis needed?", "Before commissioning a motor larger than 30% of your supply transformer's kVA rating, before adding a motor on a generator-only supply, or any time multiple motors start simultaneously."),
            ("What minimum voltage does the motor need during start?", "At least 80% of rated voltage at the terminals throughout acceleration. Lower voltages reduce starting torque and can cause the motor to stall before reaching rated speed."),
            ("Do you need dynamic motor data for the simulation?", "Detailed dynamic models produce the most accurate results, but when manufacturer data is unavailable we use measured starting impedance and standard induction-machine models."),
            ("Will a soft starter solve every motor-start problem?", "Usually — but not always. For high-inertia loads or weak supplies, a VFD or autotransformer may be the only way to start within limits."),
            ("How long does a motor start analysis take?", "One to three weeks depending on how many scenarios you want modelled."),
        ],
        "ctaBannerHeading": "Model Your Motor Start Before You Commission",
        "ctaBannerBody_tpl": "Carelabs engineers deliver ETAP-based motor starting studies for industrial facilities across {cities}",
    },
    "power-system-study-and-analysis": {
        "title": "Power System Study & Analysis",
        "eyebrow": "Engineering Studies",
        "metaTitle_tpl": "Power System Study & Analysis in {country} | Carelabs",
        "metaDescription_tpl": "Load flow, short circuit, protection coordination, and transient studies in a single ETAP-based engagement for {adj} facilities.",
        "definitionalLede_tpl": "A power system study answers the three questions every industrial facility needs answered: can the network carry the load, survive a fault, and clear it selectively? Carelabs delivers load flow, short circuit, and protection coordination as one integrated engagement.",
        "seoKeywords_tpl": ["power system study {country}", "load flow analysis", "short circuit study", "protection coordination", "IEC 60909"],
        "featuresHeading": "Four Studies, One Integrated Engagement",
        "featuresSubtext_tpl": "Every real-world power system analysis combines multiple studies. Running them together — in a single ETAP model — produces results you can act on across your {adj} operations.",
        "features": [
            ("Load Flow Analysis", "Voltage, current, power factor, and losses at every bus under normal operating conditions."),
            ("Short Circuit Study", "IEC 60909 fault calculations for three-phase, L-G, L-L, and L-L-G faults."),
            ("Protection Coordination", "Time-current curves for every relay, fuse, and breaker to confirm the nearest device trips first."),
            ("Transient Analysis", "Lightning, switching, and capacitor-energisation transients for surge arrester sizing."),
        ],
        "safetyEyebrow": "System Reliability",
        "safetyHeading": "Prove Your Power System Can Survive Its Worst Day",
        "safetyBody_tpl": "A power system that works on a normal afternoon may not survive a motor start at shift change or a fault at a remote feeder. Analysis shows you where the margins are.",
        "safetyBullets": [
            "Confirm breaker interrupting ratings against calculated fault current",
            "Validate transformer ratings against peak operating load",
            "Check voltage regulation stays within ±5% at every bus",
            "Verify protection coordination is selective across all fault types",
            "Document the baseline — future upgrades get built on solid ground",
        ],
        "reportsEyebrow": "Deliverables",
        "reportsHeading": "Power System Report Contents",
        "reportsBody_tpl": "One engagement, one report, everything you need for insurer audits, regulatory filings, and internal engineering review.",
        "reportsBullets": [
            "Updated single-line diagram with every component modelled",
            "Load flow results bus-by-bus under normal and contingency scenarios",
            "Short-circuit fault currents and breaker-duty comparisons",
            "Protection coordination curves with every device plotted",
            "Ranked list of findings with proposed remediation and estimated cost",
        ],
        "processSteps": [
            ("Data Collection", "Single-line, nameplate, cable, and relay-setting data. Meeting with operations."),
            ("System Modelling", "Build the full ETAP model with every transformer, cable, breaker, relay, motor, and generator."),
            ("Run the Studies", "Load flow, short circuit, coordination, and transient analyses on the same model."),
            ("Report & Review", "Deliver the report, walk operations through findings, provide updated relay setting sheets."),
        ],
        "faqs": [
            ("How often should a power system study be refreshed?", "Every five years at minimum, and immediately after any material change — new transformer, new generation, large load addition, or upstream utility upgrade."),
            ("What calculation method does Carelabs use for short circuit?", "IEC 60909 for initial symmetrical short-circuit current, peak current, and breaking current."),
            ("Do I need all four studies or can I pick and choose?", "You can scope to any subset. Running all four together typically costs 25–40% less than running them separately and ensures results are internally consistent."),
            ("Will Carelabs update our relay settings as part of the study?", "Yes. The coordination study produces recommended settings per device, ready for your relay engineer to load."),
            ("Does the study cover renewable integration or just conventional loads?", "Both. Solar PV, battery energy storage, and cogeneration are modelled in the same ETAP environment."),
        ],
        "ctaBannerHeading": "Get a Baseline Your Operations Team Can Build On",
        "ctaBannerBody_tpl": "Carelabs engineers deliver full power system studies across {cities} Load flow + short circuit + coordination + transients in one engagement.",
    },
    "power-quality-analysis": {
        "title": "Power Quality Analysis",
        "eyebrow": "Power Quality",
        "metaTitle_tpl": "Power Quality Analysis in {country} | Carelabs",
        "metaDescription_tpl": "Measure voltage stability, sags, transients, and harmonics to pinpoint equipment-failure causes in {adj} facilities. Ranked remediation from Carelabs engineers.",
        "definitionalLede_tpl": "Power quality problems — voltage dips, sags, harmonics, transients — cause most 'unexplained' equipment failures in industrial facilities. A Carelabs power quality analysis measures the supply over two weeks, separates utility-side from facility-side issues, and delivers ranked remediation.",
        "seoKeywords_tpl": ["power quality analysis {country}", "voltage sag", "voltage imbalance", "transient analysis", "IEEE 519"],
        "featuresHeading": "Power Quality Issues We Track",
        "featuresSubtext_tpl": "Most equipment in a modern {adj} facility is more sensitive to supply anomalies than the equipment it replaced. Measuring what's actually on the bus is the first step to fixing what's breaking.",
        "features": [
            ("Voltage Stability & Imbalance", "Long-duration over-/under-voltage plus three-phase imbalance — both silently kill motors."),
            ("Sags, Swells, and Interruptions", "Fast RMS fluctuations that dropout relays, reset PLCs, and cost production."),
            ("Harmonics and Flicker", "Waveform distortion from nonlinear loads and fast-changing loads like welders and arc furnaces."),
            ("Transients and Surges", "Sub-cycle events from switching, lightning, and capacitor energisation."),
        ],
        "safetyEyebrow": "Equipment Protection",
        "safetyHeading": "Prevent the Failures You Can't Explain",
        "safetyBody_tpl": "Poor power quality degrades equipment silently. Motors age faster on unbalanced voltage. Capacitors fail when they resonate. Drives trip on transients.",
        "safetyBullets": [
            "Sags longer than 0.5 cycles can trip sensitive controls",
            "Imbalance above 2% significantly reduces motor life",
            "Voltage THD above 5% causes measurable equipment heating",
            "Transients above 2 kV damage electronic power supplies",
            "Flicker above 0.8 Pst causes measurable productivity loss",
        ],
        "reportsEyebrow": "Deliverables",
        "reportsHeading": "Power Quality Report Contents",
        "reportsBody_tpl": "A complete digital report plus the raw measurement files so your engineering team can reopen the data anytime. Aligned with IEEE 519 and IEC 61000-4-30.",
        "reportsBullets": [
            "Event log: every sag, swell, interruption, and transient time-stamped",
            "Voltage and current trends over the measurement window",
            "THD and individual harmonic spectrum at each measurement point",
            "Flicker measurements (Pst, Plt) where relevant",
            "Ranked remediation — source identification, proposed fix, estimated cost",
        ],
        "processSteps": [
            ("Scope & Single-Line Review", "Agree on measurement points with operations — usually the PCC plus 2–4 critical distribution boards."),
            ("Instrumentation", "Install class-A power quality analysers at each point. Typical measurement window is 7–14 days."),
            ("Data Analysis", "Correlate events with production logs. Separate utility-source issues from internal-source issues."),
            ("Report and Remediation", "Deliver findings, rank recommended fixes by ROI, and walk operations through the report."),
        ],
        "faqs": [
            ("When should a power quality survey be run?", "After unexplained equipment failures, before qualifying new sensitive equipment, when the utility changes its feed, and as a routine baseline every 3–5 years on critical installations."),
            ("How long is the measurement window?", "Seven to fourteen days minimum. That's what it takes to capture all shifts, weekday/weekend differences, and rare events."),
            ("Can you identify whether the problem is utility or internal?", "Yes — that's the core of the analysis. By measuring simultaneously at the PCC and at internal buses, we can tell whether disturbances originated upstream or inside the facility."),
            ("What standard do your measurements follow?", "IEC 61000-4-30 class A for measurement methodology and IEEE 519 for harmonic evaluation."),
            ("Do you also install mitigation equipment?", "We design and specify mitigation — filters, UPS, isolation transformers, arresters — and work with your preferred contractor for installation."),
        ],
        "ctaBannerHeading": "Measure It, Then Fix It",
        "ctaBannerBody_tpl": "Carelabs delivers class-A power quality surveys across {cities} IEC 61000-4-30 measurement, IEEE 519 evaluation, ranked remediation.",
    },
}

# ───────── BLOG TEMPLATES (keyed to the 'keep:X' markers in BLOG_LEDGER) ────

BLOG_TEMPLATES = {
    "arc_flash_guide": {
        "title_tpl": "Arc Flash Analysis in {country}: A Detailed Guide",
        "metaTitle_tpl": "Arc Flash Analysis in {country}: Complete Guide | Carelabs",
        "metaDescription_tpl": "Arc flash analysis identifies electrical hazards and defines PPE requirements. Learn the 5-step risk mitigation process for {adj} facilities.",
        "category": "Arc Flash Study",
        "excerpt_tpl": "Arc flash events can produce temperatures above 19,000 °C and cause severe burns, toxic fumes, and blast injuries. Here is the five-step framework Carelabs engineers use to identify, control, and mitigate arc flash risk in {adj} facilities.",
        "seoKeywords_tpl": ["arc flash analysis {country}", "{primary} compliance", "IEEE 1584", "arc flash hazard assessment", "PPE selection arc flash"],
        "body_tpl": """## What is an arc flash?

An arc flash is the light and heat produced when current jumps between conductors through an air gap. The discharge ionises the surrounding air, making it conductive and sustaining the arc. Temperatures at the arc can exceed 19,000 °C — hot enough to vaporise copper, ignite clothing, and cause third-degree burns at distance.

## Why arc flash analysis matters

Arc flash incidents create three categories of harm:

- **Human injury** — severe burns, hearing loss, eye damage, and respiratory injury from inhaled hot gases.
- **Equipment damage** — switchgear destruction, panel rupture, and downtime during rebuilds.
- **Commercial loss** — medical costs, worker's compensation, litigation, fines, and reputational damage that can cost far more than the incident itself.

An arc flash study quantifies the incident energy available at every piece of electrical equipment, sets safe approach boundaries, and defines the PPE category workers must wear.

## Common causes

- Failed conductor insulation
- Dust, moisture, or corrosion inside enclosures
- Dropped tools or fasteners bridging live parts
- Poor maintenance of breakers, switches, and relays
- Mis-rated or defective equipment
- Human error during testing or racking

## The five-step arc flash risk framework

### Step 1 — Identify the hazard

Build a detailed electrical model of the facility. This requires data collection, single-line diagrams, short-circuit analysis, protective-device coordination, and incident-energy calculations — typically in software such as ETAP.

### Step 2 — Manage exposure

Work on de-energised equipment wherever possible. Replace manual racking with remote-operated systems. Install physical barriers between workers and live parts.

### Step 3 — Engineering controls

Reduce incident energy at the source: lower short-circuit current, install arc-flash detection and suppression, upgrade switchboards, add bus insulation, and tune protective-device settings so faults clear faster.

### Step 4 — Administrative controls

Apply incident-energy labels to every piece of equipment. Define arc-flash boundaries. Publish electrical work permits. Train personnel annually. Document every study in your safety program.

### Step 5 — Personal protective equipment

PPE is the last line of defence, not the first. Select arc-rated clothing, face shields, gloves, and hearing protection based on the calculated incident energy for each task.

## What Carelabs delivers

Every Carelabs arc flash study ships with:

- Power-system model built in ETAP
- Short-circuit and overcurrent coordination analysis
- Incident-energy calculations at every relevant bus
- Equipment labels ready to apply
- One-line diagrams updated to current state
- Mitigation recommendations with cost-benefit ranking
- A final report aligned with IEEE 1584 and {primary}

Our engineers are ISO 9001:2008-accredited and serve {cities} and every other major industrial centre in {country}. [Request a free arc flash study quote](/{cc}/contact-us/) or [explore our arc flash service page](/{cc}/arc-flash-study/).
""",
    },
    "arc_flash_assessing": {
        "title_tpl": "Assessing and Lowering the Danger of an Arc Flash",
        "metaTitle_tpl": "How to Assess and Reduce Arc Flash Risk | Carelabs {country}",
        "metaDescription_tpl": "Arc flash events can reach 20,000 °C. Learn how to identify hazards, apply engineering controls, and protect your workforce in {adj} facilities.",
        "category": "Arc Flash Study",
        "excerpt_tpl": "Arc flash incidents damage lives, equipment, and reputations. This guide walks through the costs of an arc flash and the five practical steps a {adj} facility can take to bring the risk down.",
        "seoKeywords_tpl": ["arc flash risk assessment", "arc flash mitigation", "{primary}", "electrical safety program", "arc-resistant switchgear"],
        "body_tpl": """## Why arc flash risk deserves board-level attention

Electrical arcs form when voltage across a gap ionises the air between two conductors. Once the air turns conductive, current flows through the plasma and generates extreme heat — typically up to 20,000 °C at the arc. The light, pressure wave, and flying molten metal make arc flash one of the most dangerous failure modes in industrial electrical systems.

## The real cost of an arc flash incident

### Direct costs

- Medical care and rehabilitation for injured workers
- Worker's compensation claims
- Accident investigation and production downtime

### Indirect costs

- Legal fees, settlements, and regulatory fines
- Higher insurance premiums
- Equipment replacement and rebuild time
- Contract-worker costs during recovery

### Reputational costs

A visible safety incident damages employer brand, customer trust, and — in worst cases — leads to the suspension of an electrical contractor's license.

## What causes most arc flash incidents

- Testing or racking on the wrong surface or with the wrong probe
- Inappropriate equipment ratings or improper installation
- Damaged insulation, conductor gaps, or panel obstructions
- Accumulated dust, rust, or moisture inside enclosures
- Poor circuit-breaker and switch maintenance
- Frayed connections or energised components left exposed

## Five mitigation strategies that work

### 1. De-energise whenever possible

The single most effective step. Avoid energised work. When re-energising, test first with remote tools and observe approach boundaries.

### 2. Adopt low-risk technology

Remote racking systems, arc-flash detection relays, and infrared inspection windows keep operators outside the arc-flash boundary during routine tasks.

### 3. Redesign the system for lower incident energy

Configure protective devices for faster clearing times. Use current-limiting breakers. Segment the bus. Ensure PPE categories are matched to the actual hazard level of each task.

### 4. Reduce available fault current

Non-current-limiting breakers, bus segmentation during maintenance, and current-limiting reactors all reduce the energy available to feed an arc.

### 5. Deploy arc-resistant switchgear

Arc-resistant designs use sealed joints, top-mounted pressure-relief vents, and reinforced hinges to channel arc energy away from personnel through ducts to a safe area.

## How Carelabs runs an assessment

Our engineers assess the current state of your safety program, model the system in ETAP, calculate incident energy at every bus, and recommend mitigation ranked by cost and impact. Carelabs is ISO 9001:2008-accredited and delivers arc flash assessments across {cities} and every other major {adj} industrial region.

[Book a free consultation](/{cc}/contact-us/) or [read more about our arc flash service](/{cc}/arc-flash-study/).
""",
    },
    "motor_efficiency": {
        "title_tpl": "How to Evaluate Commercial Motor Efficiency and Reliability",
        "metaTitle_tpl": "Motor Efficiency & Reliability Evaluation | Carelabs {country}",
        "metaDescription_tpl": "Motors use 46% of industrial electricity. Learn the four factors that govern motor performance and the audit process Carelabs uses in {adj} plants.",
        "category": "Motor Analysis",
        "excerpt_tpl": "Industrial motors consume nearly half of all electricity used in manufacturing. Small gains in motor efficiency translate directly to lower bills and higher reliability in {adj} facilities. Here is how Carelabs audits commercial motors.",
        "seoKeywords_tpl": ["motor efficiency audit", "commercial motor reliability", "motor performance {country}", "energy efficiency industrial motors"],
        "body_tpl": """## Why motor efficiency is a bottom-line issue

In industrial plants, motors draw **46% of total electricity** and **69% of total energy** consumed. Peak efficiency sits around 75% of rated load, and efficiency drops off as motors age. Poor motor design and operation — oversized motors, unmatched loads, power-quality problems — are among the fastest drivers of rising energy bills.

The upside: an audit that cuts losses by even a few percentage points pays for itself within a year on most production lines.

## Four factors that govern motor performance

### 1. Power quality

Transients, voltage imbalance, sags, swells, and harmonics create heating, torque pulsation, and insulation stress. Poor power quality is often the hidden cause of "mystery" motor failures.

### 2. Torque characteristics

A motor's torque–speed curve determines whether it can start the load, hold speed under disturbance, and ride through voltage dips. Measured torque is one of the clearest indicators of motor health.

### 3. Load matching and operating point

Motors overloaded mechanically stress bearings, couplings, and insulation. Motors lightly loaded run below their efficiency sweet spot and waste energy.

### 4. Maintenance baseline

Predictive maintenance starts with baseline efficiency data. Without a reference point, you cannot tell whether a motor is drifting toward failure.

## The failure statistics you should know

- **75% of industrial motor failures cause 1–6 days of plant downtime per year.**
- 90% of motor breakdowns show warning signs less than a month in advance.
- 36% of breakdowns progress from first symptom to failure in under 24 hours.

Regular inspection, inline testing, and corrective analysis cut this downtime dramatically.

## The Carelabs motor audit process

1. **Document review** — collect drawings, nameplate data, and service history.
2. **Single-line diagram and checklist** — build a current-state reference.
3. **On-site inspection** — walk the installation and complete the checklist.
4. **Testing** — electrical and mechanical testing under representative load.
5. **Data capture** — record voltage, current, power factor, vibration, temperature.
6. **Cross-check against load flow and power quality** — confirm supply is healthy.
7. **Corrective recommendations** — any issue found is scoped with a fix.
8. **Compliance check** — verify efficiency meets {adj} national standards.
9. **Digital report** — delivered with prioritised action list and safe-work notes.

## Why work with Carelabs

- Accountable engineering — we own the outcome.
- Familiarity with {adj} standards and local utility conventions.
- Digital, audit-ready reports.
- Coverage across {cities} and every other major industrial region in {country}.

[Request a motor efficiency audit](/{cc}/contact-us/) or [see our motor start analysis service](/{cc}/motor-start-analysis/).
""",
    },
    "harmonic_why": {
        "title_tpl": "Why Harmonic Analysis Matters for {adj} Businesses",
        "metaTitle_tpl": "Why Harmonic Analysis Matters in {country} | Carelabs",
        "metaDescription_tpl": "Harmonic distortion cuts equipment lifespan and raises utility costs. Learn when to measure harmonics in {adj} facilities.",
        "category": "Harmonic Analysis",
        "excerpt_tpl": "Harmonic distortion shortens equipment life, raises energy bills, and increases the risk of equipment failure in {adj} facilities. Here is when to measure harmonics and how Carelabs engineers bring distortion back within limits.",
        "seoKeywords_tpl": ["harmonic analysis {country}", "power quality", "THD limits", "point of common coupling", "ETAP harmonic study"],
        "body_tpl": """## What harmonics do to your power system

An ideal supply delivers a clean sinusoidal voltage. In real facilities, nonlinear loads — variable-speed drives, switched-mode power supplies, LED lighting, UPS systems — pull current in short bursts that distort the waveform. That distortion is measured as **total harmonic distortion (THD)**.

Persistent harmonic distortion above the limits causes:

- Additional Joule-effect losses inside conductors, transformers, and motors
- Higher subscribed-power billing from the utility
- Equipment that must be oversized to stay within thermal limits
- Component lifespan reductions once distortion reaches ~10% THD
- Peak currents that trip protective devices and idle production

## When to run a harmonic study

Most facilities stay safe with up to **15% nonlinear load** on the bus. Above that threshold, distortion rises fast. Order a harmonic study when any of these is true:

- Nonlinear load exceeds 15% of total bus load
- You are about to add a variable-speed drive, UPS, or rectifier system
- A capacitor bank is being added or resized
- Equipment is overheating without an obvious cause
- Protective devices are tripping with no upstream fault

## The Carelabs harmonic analysis workflow

1. **Collect the single-line diagram.** Mark every nonlinear load, capacitor bank, and long medium-voltage cable.
2. **Identify the point of common coupling (PCC).**
3. **Flag sensitive buses** — distribution boards feeding precision equipment.
4. **Gather harmonic data** for every nonlinear load.
5. **Pull utility data** at the PCC — short-circuit fault levels, allowable limits.
6. **Model the network in ETAP** and run the harmonic analysis.
7. **Calculate individual and total distortion** at each bus and the PCC.
8. **Plot the spectrum** to identify dominant harmonic orders.
9. **Design mitigation** — passive filter, active filter, or drive-side reactor.
10. **Re-run the analysis** with mitigation modelled to verify compliance.

## What changes after mitigation

- Lower conductor and transformer heating
- Higher effective power factor and smaller reactive-power bills
- Extended capacitor-bank, motor, and transformer service life
- Fewer nuisance breaker trips
- Cleaner supply for sensitive equipment

## Why {adj} facilities work with Carelabs

ISO 9001:2008-accredited engineers, ETAP-based modelling, and coverage across {cities} and every other major industrial region.

[Request a harmonic study quote](/{cc}/contact-us/) or [learn more about our harmonic service](/{cc}/harmonic-study-and-analysis/).
""",
    },
    "harmonic_system": {
        "title_tpl": "Harmonic Analysis of the {country} Power System",
        "metaTitle_tpl": "Harmonic Analysis of {country} Power Systems | Carelabs",
        "metaDescription_tpl": "Harmonics raise RMS current, overheat transformers, and damage sensitive equipment in {adj} facilities. Here is how harmonic analysis works.",
        "category": "Harmonic Analysis",
        "excerpt_tpl": "Harmonics raise the RMS current on every cable, transformer, and motor they pass through. The effects — overheating, nuisance tripping, shortened lifespan — are often mistaken for normal ageing in {adj} plants.",
        "seoKeywords_tpl": ["harmonic distortion", "power system analysis {country}", "nonlinear loads", "ETAP", "capacitor bank harmonics"],
        "body_tpl": """## Why harmonics deserve their own study

Every modern facility runs on electricity, and most modern loads — computers, LED lighting, variable-speed drives, rectifiers, UPS systems — are nonlinear. Nonlinear loads distort the supply waveform and inject harmonic currents back into the network. Those harmonics raise the RMS current on every cable, transformer, and motor between the load and the utility transformer.

The effects can be subtle at first: slightly elevated transformer temperature, a breaker that trips unexpectedly, a motor that ages faster than its twin on the next line. Over time, these add up to real losses.

## What harmonic distortion actually is

Harmonic distortion is a non-sinusoidal deviation in the voltage or current waveform. It is caused by loads that draw current in pulses — switched-mode power supplies, drives, UPS equipment, fluorescent and LED lighting, and electronically-controlled motors.

Once distortion exists, it propagates through the power system and affects every piece of equipment downstream.

## Why harmonic analysis matters

A harmonic study quantifies distortion, identifies the dominant orders, and tells you whether your facility is within the 5–8% THD ceilings specified by international standards such as **IEEE 519**. Without the study, you are guessing.

## When to run a study

- Nonlinear load exceeds 25% of any circuit or bus
- You are diagnosing unexplained equipment damage or breaker trips
- The plant is being expanded with new drives, rectifiers, or UPS
- A capacitor bank is being added — capacitors can resonate with system inductance at specific harmonic frequencies

## How harmonics affect different equipment

| Equipment | Harmonic effect |
|-----------|-----------------|
| Rotating machines | Increased cable resistance, rotor losses, overheating, torque pulsation |
| Transformers and cables | Overheating, neutral-conductor overload, higher losses |
| Capacitor banks | High circulating currents, insulation breakdown, resonance |
| Power electronics | Reduced efficiency, component failure |
| Protective relays | Misoperation and nuisance tripping |

## The benefits of mitigation

- Lower conductor, switchgear, and transformer losses — directly reducing energy bills
- Lower RMS current means smaller cables, switchgear, and busbars on future upgrades
- Less overheating means longer life for motors, capacitors, and transformers
- Fewer unplanned shutdowns and fewer missed-production incidents

## The Carelabs workflow

1. Obtain the single-line diagram and mark nonlinear loads.
2. Locate the point of common coupling (PCC).
3. Highlight sensitive plant buses.
4. Collect harmonic data for every nonlinear load plus utility background levels.
5. Model the system in ETAP.
6. Measure voltage and current distortion at each bus.
7. If distortion exceeds limits, design a mitigation strategy — passive filter, active filter, or drive-side reactor.
8. Re-run the analysis to verify compliance.

Carelabs equips engineers with ETAP and modern instrumentation to deliver risk-free harmonic assessments across {country}. [Request a quote](/{cc}/contact-us/) or [see our harmonic service page](/{cc}/harmonic-study-and-analysis/).
""",
    },
    "power_quality_principles": {
        "title_tpl": "Principles of Power Quality Work in {country}",
        "metaTitle_tpl": "Power Quality Principles in {country} | Carelabs",
        "metaDescription_tpl": "Voltage stability, imbalance, harmonics, and sags are the four pillars of power quality. How Carelabs engineers measure and fix each in {adj} facilities.",
        "category": "Power Quality",
        "excerpt_tpl": "Power quality issues — voltage dips, imbalance, harmonics, flicker — cause equipment damage, production loss, and safety incidents in {adj} facilities. This guide explains the categories and how Carelabs measures and mitigates each.",
        "seoKeywords_tpl": ["power quality {country}", "voltage imbalance", "voltage sag analysis", "current harmonics"],
        "body_tpl": """## Why power quality matters

The quality of the power supply directly determines whether the equipment connected to it performs as designed and lives out its rated lifespan. A network with clean, stable voltage keeps production running. A network with poor power quality slowly degrades every motor, drive, and sensitive electronic controller on the floor — often without an obvious culprit.

Unlike **reliability** (which measures long-duration outages), power-quality disturbances can be silent. Equipment may degrade for years before anyone notices.

## The business cost of poor power quality

### Direct economic impact

- Lost production
- Process-restart costs
- Equipment damage and repair
- Breakdowns and delays
- Safety and health concerns
- Contract penalties for missed deliveries
- Environmental fines when processes escape control

### Indirect economic impact

- Delayed revenue recognition
- Market-share loss to competitors with better reliability
- Brand-value damage after repeated incidents

## The five power-quality issues every facility should track

### 1. Voltage stability

Steady-state voltage magnitude sustained for minutes or hours. Over- and under-voltage drive equipment failure, higher energy consumption, and system malfunction.

### 2. Voltage imbalance

Unequal voltages across three phases. Causes:

- Reverse torque in induction motors
- Stator and rotor overheating
- Reduced cable capacity
- Extra losses on the neutral conductor
- Higher cable energy losses

### 3. Current harmonics

Nonlinear loads inject harmonic currents back into the supply. Computers, variable-speed drives, and discharge lamps are the main culprits.

### 4. Voltage flicker

Envelope modulation of the voltage waveform — typically from arc furnaces, welders, or large intermittent loads.

### 5. Voltage dips and interruptions

Short-term RMS decreases lasting half a cycle to a full minute. Most equipment rides through short dips, but longer interruptions drop production.

## How Carelabs fixes power-quality problems

- **Load flow analysis** — magnitudes of power flow, voltage levels, power factor, and losses.
- **Harmonic analysis** — identify, predict, and mitigate harmonic issues.
- **Surge and transient analysis** — locate the source of fast events.
- **Voltage analysis** — track sags, swells, imbalance over time.
- **Reactive power study** — size capacitor banks at load and distribution ends.

Every study uses ETAP for system modelling and is delivered as a digital report with prioritised recommendations. Carelabs serves {cities} and every other major {adj} industrial region.

[Schedule a power quality assessment](/{cc}/contact-us/) or [see our power quality service](/{cc}/power-quality-analysis/).
""",
    },
    "power_quality_howto": {
        "title_tpl": "How to Perform a Power Quality Analysis in {country}",
        "metaTitle_tpl": "How to Run a Power Quality Analysis in {country} | Carelabs",
        "metaDescription_tpl": "Step-by-step guide to running a power quality analysis on {adj} industrial facilities — from survey scope to final report.",
        "category": "Power Quality",
        "excerpt_tpl": "A power quality analysis measures voltage stability, frequency, harmonics, and transients to identify the supply issues that drive equipment failure. Here is the five-step process Carelabs engineers follow on every {adj} assessment.",
        "seoKeywords_tpl": ["power quality analysis", "voltage stability {country}", "harmonic deformation", "power analyzer"],
        "body_tpl": """## What power quality really measures

Power quality is the ability of connected equipment to use the energy delivered to it. When power quality is poor, you see:

- High energy consumption per unit of production
- Rising maintenance cost on motors and electronics
- Unplanned downtime
- Equipment instability
- Higher failure rates on sensitive controllers

A proper power quality analysis identifies which of those symptoms is caused by the supply — and which is caused by the load — so fixes go in the right place.

## The two categories of power-quality variation

### Disruptions

Irregularities in voltage or current. Transient voltages exceed peak magnitude thresholds. RMS fluctuations — sags, surges, interruptions — cross predetermined limits.

### Steady-state variations

Continuous conditions: RMS voltage shifts, sustained imbalance, and harmonic wave distortion. Measured over time and characterised statistically.

## What a power quality analysis examines

- **Voltage stability** — steady-state level and slow variation
- **Supply frequency** — alternation rate of the voltage waveform
- **Voltage dips and swells** — fast RMS changes
- **Voltage spikes and transients** — sub-cycle peak events
- **Harmonic deformation** — waveform distortion from nonlinear loads
- **Radio-frequency interference** — high-frequency noise riding on the supply

Most of these require specialised test equipment and a certified technician to capture and interpret correctly.

## The Carelabs five-step procedure

### Step 1 — Define the scope

Agree on the objectives of the survey with the plant team. Which buses? Which loads? What symptoms are you trying to explain?

### Step 2 — Draw the single-line schematic

Capture the complete electrical system from the utility point of supply to the critical loads. Mark transformers, major breakers, capacitor banks, and VSDs.

### Step 3 — Instrument the system

Connect power-quality analysers at the PCC and at every critical distribution board. Capture voltage, current, power factor, THD, and transients for a representative period — typically 7 to 14 days.

### Step 4 — Analyse the data

Correlate events with production logs. A sag at 02:14 on Tuesday night has a specific cause; finding that cause is the job. Compare measurements against IEEE 519 limits.

### Step 5 — Deliver the report

A power-quality report tells three stories: what the measurements show, which problems those measurements explain, and what it will cost to fix them — ranked by ROI.

## Why work with Carelabs

Carelabs engineers are trained to separate utility-side problems from facility-side problems, which matters because the fix is different for each. We deliver power-quality assessments across {cities} and every other major {adj} industrial region.

[Book a power quality survey](/{cc}/contact-us/) or [see our power quality service](/{cc}/power-quality-analysis/).
""",
    },
    "load_flow_why": {
        "title_tpl": "Why Load Flow and Short Circuit Analysis Matter in {country}",
        "metaTitle_tpl": "Load Flow & Short Circuit Analysis in {country} | Carelabs",
        "metaDescription_tpl": "Load flow and short circuit analysis prove your power system can survive full load and fault conditions. Why every {adj} facility needs both.",
        "category": "Power System Analysis",
        "excerpt_tpl": "A load flow study shows whether your power system can carry full load. A short circuit study shows whether it can survive a fault. {adj} industrial facilities need both.",
        "seoKeywords_tpl": ["load flow analysis {country}", "short circuit study", "power system analysis", "breaker interrupting capacity"],
        "body_tpl": """## Two studies, two very different questions

A **load flow analysis** answers: "Can the system carry the load I plan to put on it?" It calculates voltage, current, power factor, and losses at every node under normal operation.

A **short circuit study** answers: "Can the system survive a fault without catastrophic damage?" It quantifies the fault current at every point and checks that every breaker can interrupt that current safely.

Every industrial or commercial facility in {country} should have both on file — and should refresh them whenever the load mix, transformer, or generation scheme changes.

## What a short circuit can do

Without proper analysis, a short circuit can produce:

- Equipment damage from through-fault currents that exceed rated withstand
- Overheating of cables, busbars, and transformers
- Fire or explosion at the fault point
- Extended downtime while the system is rebuilt
- Severe injury to nearby personnel

## Three common short-circuit causes

### Insulation defects

Current finds a path through failed or contaminated insulation. Neutral wires carrying current they were not sized for overheat and fail.

### Loose connections

Slack wiring allows current to leak into grounded or neutral components.

### Faulty outlets or receptacles

Downstream equipment plugged into damaged receptacles short out the feeder.

## How Carelabs uses load flow and short circuit analysis

Carelabs engineers build an ETAP model of the facility and run both studies together. Load flow identifies bottlenecks — overloaded transformers, overloaded feeders, voltages outside ±5% limits. Short circuit identifies breakers operating above their interrupting rating, bus-bracing problems, and protection-coordination gaps.

The output is a single, actionable report: ranked list of issues, recommended fixes, and documentation you can hand to insurers and auditors.

## What you get from Carelabs

- Transparent pricing with no size-based hidden fees
- ETAP-based simulations that match real-world measurements
- Digital reports with engineer commentary
- Follow-up support for every issue we identify
- Pre-commissioning verification before systems are energised
- Fast response on new enquiries

We serve {cities} and every other major industrial region in {country}.

[Request a quote](/{cc}/contact-us/) or [read about our power system service](/{cc}/power-system-study-and-analysis/).
""",
    },
    "load_flow_triad": {
        "title_tpl": "Load Flow, Short Circuit & Relay Coordination in Power System Analysis",
        "metaTitle_tpl": "Load Flow, Short Circuit & Relay Coordination | Carelabs {country}",
        "metaDescription_tpl": "Three studies, one system: load flow, short circuit, and relay coordination together prove your {adj} power system is safe, selective, and dependable.",
        "category": "Power System Analysis",
        "excerpt_tpl": "Load flow, short circuit, and relay coordination studies together answer three questions every {adj} facility needs answered: can it carry the load, survive a fault, and clear that fault selectively?",
        "seoKeywords_tpl": ["power system analysis {country}", "relay coordination", "Gauss-Seidel", "Newton-Raphson", "ETAP load flow"],
        "body_tpl": """## The three questions every plant needs answered

A complete power system analysis combines three separate studies that each answer a different question:

- **Load flow** — can the system carry the load it is asked to carry?
- **Short circuit** — can the system survive a fault without catastrophic damage?
- **Relay coordination** — when a fault happens, does the nearest breaker open *first*?

Get all three right and you have a power system that is safe in normal operation, survivable under fault, and selective when things go wrong.

## Load flow study and analysis

A load flow study calculates:

- Active and reactive power generated at every source
- Real and reactive losses on every line and transformer
- Voltage magnitude and angle at every bus
- Power factor at every major load
- Line currents and loading percentages

### The three common numerical methods

**Gauss-Seidel** — simple to implement, low memory, but slow to converge on large systems.

**Newton-Raphson** — more complex code, but quadratic convergence and high accuracy. Requires more memory.

**Fast Decoupled Load Flow (FDLF)** — lowest memory footprint, roughly five times faster than Newton-Raphson. Preferred for real-time grid operations.

## Short circuit study and analysis

A short circuit study evaluates four fault types:

- **Line-to-line** — two phases shorted
- **Single line-to-ground** — one phase to earth
- **Double line-to-ground** — two phases and ground together
- **Three-phase** — all three phases faulted

The engineer builds an impedance diagram from the single-line drawing and calculates the short-circuit current, transformer multiplier, and full-load amps at every point. Those numbers are compared against breaker interrupting ratings.

## Relay coordination analysis

Relay coordination is the art of making sure the breaker *nearest* the fault trips before any upstream breaker. Coordination lets the rest of the plant keep running during a fault and isolates damage to the smallest possible zone.

The workflow:

1. Run the short-circuit analysis first.
2. Model every protective device with its time–current characteristic curve.
3. Plot curves together and check for overlap or crossed coordination.
4. Adjust pickup, time dial, and definite-time settings until every pair is selective.
5. Document final settings and issue relay setting sheets.

## The benefits

- Higher grid reliability
- Correctly rated equipment
- Quantified safety margins on incident energy and fault current
- Compliance with {primary} and international standards
- A documented baseline for every future upgrade

## Why work with Carelabs

Carelabs delivers load flow, short circuit, and relay coordination as a single engagement on {adj} industrial sites. Our engineers use ETAP, provide digital reports, and respond within 24 hours.

[Get a quote](/{cc}/contact-us/) or [see our power system service](/{cc}/power-system-study-and-analysis/).
""",
    },
    "motor_compliance": {
        "title_tpl": "Testing Electrical Motor Performance per {adj} Regulations",
        "metaTitle_tpl": "Motor Performance Compliance in {country} | Carelabs",
        "metaDescription_tpl": "IEEE 112 and IEC 60034 testing methods for motor efficiency compliance in {adj} facilities. How Carelabs verifies and reports motor performance.",
        "category": "Motor Analysis",
        "excerpt_tpl": "Motors drive 70% of industrial energy use. Verifying efficiency against IEEE 112 and IEC 60034 standards is how {adj} facilities hit energy targets and avoid regulatory exposure.",
        "seoKeywords_tpl": ["motor efficiency testing {country}", "IEEE 112", "IEC 60034-2-1", "motor compliance {adj}"],
        "body_tpl": """## Why motor efficiency compliance matters

Industrial electric motors power a wide variety of applications in the global economy. According to the International Energy Agency, the industrial sector accounts for up to **70% of all energy** used in industrial settings and **45% of global electricity production**.

Motors are responsible for approximately **15% (4.3 billion tons)** of the world's annual 26 billion tons of CO₂ emissions. Improving industrial motor energy efficiency by 20–30% typically pays back within three years — a cost-effective, low-risk lever for both operational and environmental goals.

## Why use efficient motors

- Lower operating costs
- Quieter, cooler operation
- Increased motor durability and reliability
- Reduced greenhouse gas emissions
- Compliance with evolving {adj} energy regulations

## Where motor energy losses come from

Energy is lost in electric motors through:

- **Friction and windage** — fixed overhead regardless of load
- **Stator losses** — scale with the square of current
- **Rotor losses** — scale with slip
- **Core losses** — scale with magnetic flux density
- **Stray-load losses** — hard to measure, often ignored

Selecting the right testing methodology determines how accurately these losses are captured — and thus how confidently you can claim a motor meets its rated efficiency.

## Internationally recognised test methods

Three standards dominate commercial motor testing:

### IEEE 112-2004

Ten test methods for polyphase motors and generators. The primary methods Carelabs uses:

- Simple input–output testing
- Loss-separated input–output testing
- Back-to-back testing with loss separation
- Load-loss calculation from smoothed residual losses
- Eh-star method

### IEC 60034-2-1 (2014)

Three categories for loss measurement:

- Single-machine input–output power measurement
- Back-to-back dual-machine testing
- Single-machine loss measurement

### JEC 37 (Japan)

Specific to Japanese induction machines; excludes stray-load loss entirely. Used less in {country} but worth citing when working with {adj} subsidiaries of Japanese OEMs.

## What Carelabs delivers

Every motor compliance audit from Carelabs ends with:

- Test plan aligned to the appropriate IEEE or IEC method
- On-site electrical and mechanical measurements
- Efficiency curve across the operating range
- Compliance gap analysis against {adj} and international standards
- Recommendations ranked by energy-saving impact

Carelabs serves {cities} and every other major industrial centre in {country}. [Request a motor compliance audit](/{cc}/contact-us/) or [see our motor start analysis service](/{cc}/motor-start-analysis/).
""",
    },
}


def build_service_payload(slug_key: str, c: dict) -> dict:
    """Render a service page payload for a given country context."""
    t = SERVICE_TEMPLATES[slug_key]
    return {
        "title": t["title"],
        "eyebrow": t["eyebrow"],
        "metaTitle": render(t["metaTitle_tpl"], c),
        "metaDescription": render(t["metaDescription_tpl"], c),
        "definitionalLede": render(t["definitionalLede_tpl"], c),
        "seoKeywords": [render(k, c) for k in t["seoKeywords_tpl"]],
        "trustBadges": trust_badges(c),
        "featuresHeading": t["featuresHeading"],
        "featuresSubtext": render(t["featuresSubtext_tpl"], c),
        "features": [
            {"title": title, "description": render(desc, c)}
            for (title, desc) in t["features"]
        ],
        "safetyEyebrow": t["safetyEyebrow"],
        "safetyHeading": t["safetyHeading"],
        "safetyBody": render(t["safetyBody_tpl"], c),
        "safetyBullets": t["safetyBullets"],
        "reportsEyebrow": t["reportsEyebrow"],
        "reportsHeading": t["reportsHeading"],
        "reportsBody": render(t["reportsBody_tpl"], c),
        "reportsBullets": t["reportsBullets"],
        "processHeading": "Our Process",
        "processSteps": [
            {"number": i + 1, "title": title, "description": desc}
            for i, (title, desc) in enumerate(t["processSteps"])
        ],
        "faqs": [
            {"question": render(q, c), "answer": render(a, c)}
            for (q, a) in t["faqs"]
        ],
        "faqSectionHeading": "Frequently Asked Questions",
        "ctaBannerHeading": t["ctaBannerHeading"],
        "ctaBannerBody": render(t["ctaBannerBody_tpl"], c),
        "ctaBannerPrimaryText": "Request a Free Quote",
        "ctaBannerPrimaryHref": f"/{c['cc']}/contact-us/",
        "ctaBannerSecondaryText": "Explore All Services",
        "ctaBannerSecondaryHref": f"/{c['cc']}/services/",
    }


def build_blog_payload(key: str, c: dict) -> dict:
    """Render a blog post payload for a given country context."""
    t = BLOG_TEMPLATES[key]
    return {
        "title": render(t["title_tpl"], c),
        "metaTitle": render(t["metaTitle_tpl"], c),
        "metaDescription": render(t["metaDescription_tpl"], c),
        "category": t["category"],
        "excerpt": render(t["excerpt_tpl"], c),
        "seoKeywords": [render(k, c) for k in t["seoKeywords_tpl"]],
        "body": render(t["body_tpl"], c),
    }


def home_services(c: dict):
    """The 5 real service cards for the HomePage."""
    return [
        {
            "title": "Arc Flash Study",
            "description": "IEEE 1584 arc flash hazard analysis with incident-energy calculations, PPE labels, and mitigation ranked by cost and impact.",
            "icon": "zap",
            "href": f"/{c['cc']}/arc-flash-study/",
        },
        {
            "title": "Harmonic Study & Analysis",
            "description": "Identify harmonic distortion, locate resonance risks, and size filter mitigation to bring your facility back within limits.",
            "icon": "bar-chart",
            "href": f"/{c['cc']}/harmonic-study-and-analysis/",
        },
        {
            "title": "Motor Start Analysis",
            "description": "Predict the voltage dip, torque profile, and breaker response before you start a large motor — avoid nuisance trips.",
            "icon": "settings",
            "href": f"/{c['cc']}/motor-start-analysis/",
        },
        {
            "title": "Power System Study & Analysis",
            "description": "Load flow, short circuit, protection coordination, and transients in a single ETAP-based engagement with digital deliverables.",
            "icon": "search",
            "href": f"/{c['cc']}/power-system-study-and-analysis/",
        },
        {
            "title": "Power Quality Analysis",
            "description": "Measure voltage stability, sags, transients, and harmonics; pinpoint equipment-failure sources; deliver ranked remediation.",
            "icon": "thermometer",
            "href": f"/{c['cc']}/power-quality-analysis/",
        },
    ]


# ═══ Per-country runner ═══════════════════════════════════════════════════

def run_country(cc: str):
    c = dict(COUNTRIES[cc])
    c["cc"] = cc
    print(f"\n{'=' * 72}")
    print(f"  {cc.upper()}  —  {c['name']}")
    print('=' * 72)

    # 1. Delete artifacts + duplicates
    print("\n--DELETE artifacts + bare-slug duplicates")
    deleted = 0
    for doc_id, slug, action in BLOG_LEDGER[cc]:
        if action != "delete":
            continue
        r = http("DELETE", f"/api/blog-posts/{doc_id}")
        if "__error" in r:
            print(f"  [ERR] {slug}: {r['__error'][:100]}")
        else:
            print(f"  [OK ] deleted {slug}")
            deleted += 1
    print(f"  Total deleted: {deleted}")

    # 2. Update legitimate blog posts
    print("\n--UPDATE 10 legitimate blog posts")
    updated_blog = 0
    for doc_id, slug, action in BLOG_LEDGER[cc]:
        if not action.startswith("keep:"):
            continue
        key = action[len("keep:"):]
        payload = build_blog_payload(key, c)
        r = http("PUT", f"/api/blog-posts/{doc_id}", payload)
        if "__error" in r:
            print(f"  [ERR] {slug}: {r['__error'][:100]}")
        else:
            print(f"  [OK ] {slug}  ->  {payload['title']}")
            updated_blog += 1
    print(f"  Total blog updated: {updated_blog}")

    # 3. Update service pages
    print("\n--UPDATE 5 service pages")
    updated_svc = 0
    for slug_key, doc_id in SERVICE_DOC_IDS[cc].items():
        payload = build_service_payload(slug_key, c)
        r = http("PUT", f"/api/service-pages/{doc_id}", payload)
        if "__error" in r:
            print(f"  [ERR] {slug_key}: {r['__error'][:100]}")
        else:
            print(f"  [OK ] {slug_key:<35}  ->  {payload['title']}")
            updated_svc += 1
    print(f"  Total services updated: {updated_svc}")

    # 4. Fix HomePage.services array
    print("\n--PUT HomePage.services with correct hrefs")
    r = http(
        "PUT",
        f"/api/home-pages/{c['home_doc_id']}",
        {"services": home_services(c)},
    )
    if "__error" in r:
        print(f"  [ERR] {r['__error'][:200]}")
    else:
        print(f"  [OK ] 5 service cards set on HomePage")

    return {"deleted": deleted, "blog_updated": updated_blog, "svc_updated": updated_svc}


def main():
    ccs = [sys.argv[1]] if len(sys.argv) > 1 else list(COUNTRIES.keys())
    totals = {}
    for cc in ccs:
        totals[cc] = run_country(cc)
    print()
    print("=" * 72)
    print("  FINAL SUMMARY")
    print("=" * 72)
    for cc, stats in totals.items():
        print(
            f"  {cc.upper()}  deleted={stats['deleted']:>2}  "
            f"blog_updated={stats['blog_updated']:>2}  "
            f"svc_updated={stats['svc_updated']:>2}"
        )


if __name__ == "__main__":
    main()
