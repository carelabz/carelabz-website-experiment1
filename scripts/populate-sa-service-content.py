"""Populate all 25 SA service pages (5 countries × 5 services) with full AEO
content — features (6), processSteps (4), safetyBullets (5), faqs (5),
definitionalLede, metaTitle, and metaDescription.

Overwrites prior content from seed-sa-content.py with a richer, more
specific content set per the Step 2 content template in the feature spec.

Usage:
  python scripts/populate-sa-service-content.py          # all 5 countries
  python scripts/populate-sa-service-content.py co       # single country

The script is idempotent and re-runnable. Existing ServicePage documentIds
are resolved via the /api/service-pages endpoint, so running against a
freshly reseeded Strapi will still target the right entries.
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


# ─── Country variable map (from the feature spec) ────────────────────────

COUNTRIES = {
    "br": {
        "country": "Brazil",
        "adj": "Brazilian",
        "cities": "São Paulo, Rio de Janeiro, Brasília, and Salvador",
        "primary": "NR-10",
        "secondary": "ABNT NBR 5410",
        "authority": "Ministério do Trabalho",
    },
    "co": {
        "country": "Colombia",
        "adj": "Colombian",
        "cities": "Bogotá, Medellín, Cali, and Barranquilla",
        "primary": "RETIE",
        "secondary": "NTC 2050",
        "authority": "Ministerio de Minas y Energía",
    },
    "cl": {
        "country": "Chile",
        "adj": "Chilean",
        "cities": "Santiago, Valparaíso, Concepción, and Viña del Mar",
        "primary": "NCh Elec. 4/2003",
        "secondary": "NSEG 5 En. 71",
        "authority": "SEC",
    },
    "ar": {
        "country": "Argentina",
        "adj": "Argentine",
        "cities": "Buenos Aires, Córdoba, Rosario, and Mendoza",
        "primary": "AEA 90364",
        "secondary": "IRAM 2281",
        "authority": "ENRE",
    },
    "pe": {
        "country": "Peru",
        "adj": "Peruvian",
        "cities": "Lima, Arequipa, Trujillo, and Chiclayo",
        "primary": "RM 111-2013-MEM",
        "secondary": "CNE",
        "authority": "OSINERGMIN",
    },
}


def render(tpl: str, ctx: dict) -> str:
    """Replace {country}, {adj}, {primary}, {secondary}, {authority}, {cities} tokens."""
    out = tpl
    for k, v in ctx.items():
        out = out.replace("{" + k + "}", v)
    return out


def trust_badges(ctx: dict):
    return [
        {"label": ctx["primary"]},
        {"label": ctx["secondary"]},
        {"label": "IEEE 1584"},
        {"label": "ISO 9001:2008"},
    ]


# ═══ Service content templates ═══════════════════════════════════════════

# Service 1 — ARC FLASH STUDY (from feature spec)
ARC_FLASH = {
    "title": "Arc Flash Study",
    "eyebrow": "Electrical Safety",
    "metaTitle_tpl": "Arc Flash Study in {country} | {primary} Compliant | Carelabs",
    "metaDescription_tpl": "IEEE 1584-compliant arc flash study services in {country}. Incident energy calculations, PPE labeling, and {primary} compliance for {adj} facilities.",
    "definitionalLede": "An arc flash study is a systematic engineering analysis that calculates incident energy levels at each point in an electrical system, determining the arc flash boundary and required PPE categories to protect workers from electrical arc hazards.",
    "seoKeywords_tpl": [
        "arc flash study {country}",
        "IEEE 1584 arc flash",
        "{primary} compliance",
        "incident energy analysis",
        "PPE category labels",
    ],
    "featuresHeading": "Key Challenges We Solve",
    "featuresSubtext_tpl": "Carelabs delivers IEEE 1584 arc flash studies for {adj} industrial facilities — from incident-energy calculation to printed equipment labels and {primary}-aligned mitigation plans.",
    "features": [
        ("Incident Energy Calculations", "IEEE 1584-based calculations at every bus and panel to determine arc flash boundaries and energy levels."),
        ("PPE Category Labeling", "Equipment labels specifying required PPE category, incident energy, and flash protection boundary per {primary}."),
        ("Short Circuit Integration", "Coordinated with short circuit analysis to ensure accurate fault current data feeds the arc flash model."),
        ("Hazard Risk Assessment", "Systematic evaluation of each work location to classify hazard severity and determine safe approach distances."),
        ("Mitigation Recommendations", "Engineering controls to reduce incident energy — relay settings, bus differential protection, and zone-selective interlocking."),
        ("Compliance Documentation", "Complete report package meeting {primary}, IEEE 1584, and NFPA 70E requirements for regulatory audits."),
    ],
    "safetyEyebrow": "Worker Safety",
    "safetyHeading": "Protect Your Team from Arc Flash Hazards",
    "safetyBody": "Arc flash exceeds 19,000 °C — enough to vaporise copper and cause severe burns at distance. A study quantifies that risk and specifies how to reduce it.",
    "safetyBullets": [
        "Reduces arc flash incident energy by up to 80% through engineering controls",
        "Equipment labels meet {primary} and NFPA 70E marking requirements",
        "Identifies highest-risk panels and switchgear for priority mitigation",
        "Establishes safe approach distances and PPE categories for every work location",
        "Provides audit-ready documentation for {authority} inspections",
    ],
    "reportsEyebrow": "Deliverables",
    "reportsHeading": "What You Receive",
    "reportsBody": "Every arc flash engagement ends with a complete package aligned with IEEE 1584 and {primary}.",
    "reportsBullets": [
        "Updated single-line diagrams and equipment inventory",
        "Short-circuit, coordination, and incident-energy results bus-by-bus",
        "Printed labels for every panel and piece of switchgear",
        "Ranked mitigation plan with estimated cost and incident-energy reduction",
        "Executive summary plus a full technical appendix for engineering review",
    ],
    "processSteps": [
        ("Data Collection", "On-site survey of switchgear, transformers, cable runs, and protective device settings across your {adj} facility."),
        ("System Modeling", "Build the electrical model in ETAP with verified utility fault contribution, impedance data, and device coordination curves."),
        ("Analysis & Calculation", "Run IEEE 1584 arc flash calculations at every bus to determine incident energy, arc flash boundary, and PPE requirements."),
        ("Report & Labeling", "Deliver the final report with equipment labels, one-line diagrams, and {primary} compliance documentation."),
    ],
    "faqs": [
        ("What is an arc flash study?", "An arc flash study calculates the incident energy — measured in cal/cm² — at every point in your electrical system where workers might be exposed. The study determines PPE requirements, arc flash boundaries, and equipment labeling needs. It follows IEEE 1584 methodology and is required under {primary} for facilities in {country}."),
        ("How often should an arc flash study be updated?", "Arc flash studies should be updated every 5 years or whenever significant changes occur — new equipment installations, utility fault current changes, protective device modifications, or facility expansions. {primary} requires current studies. An outdated study may understate hazards, leaving workers inadequately protected."),
        ("How long does an arc flash study take?", "A typical arc flash study for a medium-sized {adj} facility takes 4 to 8 weeks from initial data collection to final report delivery. Larger industrial complexes with multiple substations may require 10 to 12 weeks. The timeline depends on system complexity, number of buses, and data availability."),
        ("What PPE is required after an arc flash study?", "PPE requirements are determined by the incident energy level at each work location. Category 1 (4 cal/cm²) requires arc-rated shirt and pants. Category 2 (8 cal/cm²) adds a face shield. Category 3 (25 cal/cm²) requires a flash suit hood. Category 4 (40 cal/cm²) requires a full flash suit."),
        ("Is an arc flash study required by {primary}?", "{primary} requires employers to assess arc flash hazards at electrical equipment where workers perform energized work. This assessment must include incident energy calculations, PPE determination, and equipment labeling. Carelabs delivers studies that meet {primary}, IEEE 1584, and NFPA 70E requirements."),
    ],
    "ctaBannerHeading": "Ready to Schedule Your Arc Flash Study?",
    "ctaBannerBody_tpl": "Our ISO 9001:2008-accredited engineers deliver IEEE 1584 studies across {cities} Fast turnaround, clear reports, full {primary} compliance support.",
}


# Service 2 — HARMONIC STUDY & ANALYSIS
HARMONIC = {
    "title": "Harmonic Study & Analysis",
    "eyebrow": "Power Quality",
    "metaTitle_tpl": "Harmonic Study & Analysis in {country} | IEEE 519 | Carelabs",
    "metaDescription_tpl": "IEEE 519-compliant harmonic studies in {country}. THD measurement, filter design, and resonance analysis for {adj} facilities with nonlinear loads.",
    "definitionalLede": "A harmonic study measures and models non-sinusoidal distortions in voltage and current waveforms caused by nonlinear loads, then designs mitigation — passive or active filters, reactors, or capacitor bank adjustments — to bring total harmonic distortion within IEEE 519 limits.",
    "seoKeywords_tpl": [
        "harmonic study {country}",
        "harmonic analysis",
        "IEEE 519",
        "total harmonic distortion THD",
        "power quality filter",
    ],
    "featuresHeading": "What a Harmonic Study Reveals",
    "featuresSubtext_tpl": "Harmonics from variable-speed drives, UPS systems, and LED lighting disrupt more than power quality — they overheat transformers, fail capacitors, and misoperate relays in {adj} facilities.",
    "features": [
        ("THD Measurement Campaign", "Class A IEC 61000-4-30 power quality analysers deployed at the PCC and critical buses for a 7-14 day harmonic data capture."),
        ("Harmonic Source Identification", "Waveform analysis to identify dominant harmonic orders and trace them back to VFDs, rectifiers, UPS systems, or arc furnaces."),
        ("Filter Sizing & Design", "Passive tuned filters or active filter selection sized to site THD targets and economic optimum per IEEE 519."),
        ("Resonance & Capacitor Analysis", "Frequency scan to detect parallel or series resonance between capacitor banks and system inductance before they damage equipment."),
        ("Power Factor Impact", "Quantify displacement and distortion power factor; size reactive compensation that holds PF at utility-penalty-free levels."),
        ("Compliance Documentation", "Report delivers IEEE 519 compliance status per voltage level with bus-by-bus THD tabulation and filter commissioning plan."),
    ],
    "safetyEyebrow": "Equipment Protection",
    "safetyHeading": "Catch Harmonic Damage Before It Shows Up",
    "safetyBody": "Harmonic distortion silently overheats transformers, trips breakers, and ages motors faster. Annual monitoring catches it early.",
    "safetyBullets": [
        "Prevents transformer overheating caused by harmonic current components",
        "Extends capacitor bank life by eliminating resonance amplification",
        "Reduces neutral conductor overload on systems with 3rd and 9th harmonics",
        "Eliminates nuisance breaker trips from distorted current waveforms",
        "Reduces utility penalty charges for poor distortion power factor",
    ],
    "reportsEyebrow": "Deliverables",
    "reportsHeading": "What's in Your Harmonic Report",
    "reportsBody": "Every Carelabs harmonic report includes measured data, ETAP simulation results, and a sized mitigation plan — digital PDF plus raw measurement files.",
    "reportsBullets": [
        "Individual and total harmonic distortion (THD) at every measured bus",
        "Harmonic frequency spectrum plots with dominant orders flagged",
        "Resonance sweep showing parallel/series risk across the audible range",
        "Mitigation design — filter rating, placement, and expected post-install THD",
        "Compliance gap analysis against IEEE 519 limits",
    ],
    "processSteps": [
        ("Measurement Campaign", "Deploy class A PQ analysers at the PCC and sensitive buses for a representative 7-14 day recording window."),
        ("Harmonic Modeling", "Build the ETAP harmonic model with measured data and conduct frequency-domain sweeps bus-by-bus."),
        ("Filter Design", "Size and place passive or active filters that bring THD within IEEE 519 limits at the PCC."),
        ("Verification", "Re-run the model with mitigation in place; deliver commissioning plan and expected post-install THD."),
    ],
    "faqs": [
        ("What are power system harmonics?", "Harmonics are voltage or current waveform components at integer multiples of the fundamental frequency (50 Hz in {country}). They appear when nonlinear loads — variable-speed drives, UPS systems, LED lighting, rectifiers — draw current in short pulses rather than smooth sinusoids. The resulting distortion propagates through the network and causes heating, resonance, and equipment failure."),
        ("What causes harmonics in industrial facilities?", "Primary sources in {adj} industrial plants are variable-frequency drives (6-pulse and 12-pulse), switched-mode power supplies, UPS systems, LED lighting ballasts, induction furnaces, and arc welders. These loads draw current in pulses rather than sinusoidally. Each nonlinear load type produces a characteristic harmonic spectrum that a harmonic study identifies and quantifies."),
        ("What THD level is acceptable?", "IEEE 519 specifies voltage THD limits at the point of common coupling — 5% for systems under 1 kV and 2.5% for medium-voltage feeders. Current THD limits depend on the short-circuit ratio at your connection. Exceeding these limits risks equipment damage and may trigger utility penalties. Carelabs reports flag every bus above the threshold."),
        ("How do harmonics damage equipment?", "Harmonic currents cause additional I²R losses in cables and transformers, overheating insulation. Motors suffer torque pulsations and bearing stress. Capacitor banks can resonate at specific harmonic orders, generating overvoltages that destroy capacitors. Neutral conductors on three-phase systems overload on triplen harmonics. Over time, these effects halve equipment lifespan."),
        ("Does {primary} require harmonic analysis?", "{primary} addresses electrical installation safety in {country} but does not specifically mandate harmonic studies. However, IEEE 519 is the internationally recognized reference for harmonic limits and is adopted by major {adj} utilities. Harmonic studies are required by utility connection agreements for industrial facilities and are good practice under any electrical safety regime."),
    ],
    "ctaBannerHeading": "Bring Your Facility Back Within Harmonic Limits",
    "ctaBannerBody_tpl": "Carelabs engineers deliver ETAP-based harmonic studies across {cities} Digital reports, ranked mitigation, IEEE 519 compliance.",
}


# Service 3 — MOTOR START ANALYSIS
MOTOR_START = {
    "title": "Motor Start Analysis",
    "eyebrow": "Power System Engineering",
    "metaTitle_tpl": "Motor Start Analysis in {country} | Voltage Dip Studies | Carelabs",
    "metaDescription_tpl": "Motor starting studies for {adj} industrial facilities. ETAP dynamic simulation to size soft starters, VFDs, and verify {primary} compliance.",
    "definitionalLede": "A motor start analysis simulates the transient electrical behaviour during large motor starting — calculating voltage dip, acceleration time, and breaker coordination — to ensure the motor can start without tripping protection, stalling under load, or disrupting sensitive equipment on the same bus.",
    "seoKeywords_tpl": [
        "motor start analysis {country}",
        "motor starting study",
        "voltage dip",
        "ETAP transient analysis",
        "soft starter sizing",
    ],
    "featuresHeading": "Questions a Motor Start Study Answers",
    "featuresSubtext_tpl": "Motor starting is the single most disruptive event a {adj} facility's electrical system sees. Knowing the outcome in advance saves you from nuisance trips, stalled loads, and commissioning delays.",
    "features": [
        ("Voltage Dip Calculation", "Time-domain simulation of terminal voltage during starting, verified against the 80% nameplate floor and bus-level limits for sensitive loads."),
        ("Starting Method Comparison", "DOL vs reduced-voltage autotransformer vs soft starter vs VFD, each modelled in ETAP with cost and voltage-impact tradeoffs."),
        ("Generator Impact Analysis", "Transient simulation of motor start on generator-only supplies where motor kVA exceeds 10-15% of genset rating."),
        ("Protection Coordination", "Verify upstream breakers ride through starting inrush (5-7× FLA for DOL) without nuisance tripping."),
        ("Cable Sizing Verification", "Check cable thermal ratings under starting current and voltage drop compliance per {primary} installation codes."),
        ("Recommendation Report", "Selected starting method with relay settings tuned to ride through transient, plus commissioning procedure."),
    ],
    "safetyEyebrow": "Equipment Protection",
    "safetyHeading": "Protect Downstream Loads From Motor-Start Transients",
    "safetyBody": "Voltage drops during motor starts affect everything on the bus — lighting, PLCs, drives, instrumentation. Modelling the transient protects the whole plant.",
    "safetyBullets": [
        "Prevents motor stall and thermal damage from undersized supply",
        "Verifies 80% nameplate terminal voltage minimum during acceleration",
        "Eliminates nuisance upstream breaker trips during motor start",
        "Confirms sensitive bus voltage rides through within PLC and drive tolerances",
        "Provides {authority}-ready documentation for motor installation approval",
    ],
    "reportsEyebrow": "Deliverables",
    "reportsHeading": "Motor Start Report Contents",
    "reportsBody": "Every motor start report includes time-domain simulations, starting-current curves, voltage-recovery plots, and a clear go/no-go recommendation for direct-on-line start.",
    "reportsBullets": [
        "Voltage vs time at motor terminals and every sensitive bus",
        "Current vs time from inrush through steady-state",
        "Motor and load torque-speed curves with acceleration margin",
        "Starter sizing and settings when DOL is not viable",
        "Recommendations for bus configuration during start",
    ],
    "processSteps": [
        ("Motor Data Collection", "Gather motor nameplate, starting impedance, load inertia, and supply short-circuit data."),
        ("Load Flow Modeling", "Build the ETAP model with current bus loading and utility fault contribution to represent real starting conditions."),
        ("Starting Simulation", "Run time-domain simulation of direct-on-line start; iterate through soft starter, VFD, and reduced-voltage options if DOL violates limits."),
        ("Recommendation", "Deliver sizing, settings, and commissioning plan with expected voltage dip and acceleration time per scenario."),
    ],
    "faqs": [
        ("What is a motor start analysis?", "A motor start analysis is a time-domain simulation that predicts the transient electrical behaviour when a large motor is energized — voltage dip at terminals and across the bus, inrush current magnitude and duration, acceleration time to rated speed, and protection device response. The study determines whether the motor can start safely and what starting method is required."),
        ("Why do motors cause voltage dips?", "Induction motors draw 5-7 times their full-load current during starting because the rotor slip is 100%. This inrush current flows through source impedance — transformer, cables, generator — causing voltage drop at the motor terminals and every bus upstream. In {adj} industrial facilities with weak supplies, the dip can exceed 20% and trip sensitive equipment."),
        ("When is a motor start study required?", "Before commissioning any motor larger than 30% of supply transformer kVA, before adding any motor to a generator-only supply where motor kVA exceeds 10-15% of generator rating, or whenever multiple motors start simultaneously. {primary} requires that motor installations meet voltage tolerance limits, which a starting study verifies."),
        ("What is an acceptable voltage dip?", "Terminal voltage must stay at or above 80% of rated during motor acceleration — below this the motor develops insufficient torque to reach speed. Bus voltage should stay above 90% for sensitive loads like PLCs, VFDs, and contactors. Utility codes in {country} often limit voltage dip at the PCC to 3-5% for large motor starts."),
        ("How does a VFD help with motor starting?", "A variable-frequency drive ramps the motor up from low frequency, limiting inrush to near full-load current regardless of motor size. The VFD also controls acceleration time and torque profile. For motors where direct-on-line starting violates voltage dip limits, a VFD or soft starter is typically the most economical solution after a Carelabs study confirms the sizing."),
    ],
    "ctaBannerHeading": "Model Your Motor Start Before You Commission",
    "ctaBannerBody_tpl": "Carelabs engineers deliver ETAP-based motor starting studies for industrial facilities across {cities}",
}


# Service 4 — POWER SYSTEM STUDY & ANALYSIS
POWER_SYSTEM = {
    "title": "Power System Study & Analysis",
    "eyebrow": "Engineering Studies",
    "metaTitle_tpl": "Power System Study in {country} | Load Flow & Short Circuit | Carelabs",
    "metaDescription_tpl": "Integrated power system studies for {adj} facilities — load flow, short circuit, protection coordination, and {primary} compliance in one engagement.",
    "definitionalLede": "A power system study is an integrated set of engineering analyses — load flow, short circuit, protection coordination, arc flash, and transient stability — that together quantify how your electrical network performs under normal load, fault conditions, and switching events.",
    "seoKeywords_tpl": [
        "power system study {country}",
        "load flow analysis",
        "short circuit study",
        "protection coordination",
        "IEC 60909",
    ],
    "featuresHeading": "Four Studies, One Integrated Engagement",
    "featuresSubtext_tpl": "Every real-world power system analysis combines multiple studies. Running them together in a single ETAP model produces results you can act on across your {adj} operations.",
    "features": [
        ("Load Flow Analysis", "Steady-state voltage and current calculations at every bus under normal and contingency operating conditions."),
        ("Short Circuit Calculations", "IEC 60909 fault current computations for 3-phase, L-G, L-L, and L-L-G faults at every switchgear location."),
        ("Protection Coordination", "Time-current curves for every relay, fuse, and breaker to ensure selectivity and verify ratings against calculated fault current."),
        ("Voltage Regulation", "Identifies tap-changer settings, capacitor placement, and voltage profile improvements that keep every bus within ±5% limits."),
        ("Power Factor Correction", "Sizes and places capacitor banks to reach 0.95+ PF at the utility meter without exciting harmonic resonance."),
        ("System Capacity Evaluation", "Quantifies available capacity at each substation for future loads, identifying bottlenecks before you commit to an expansion."),
    ],
    "safetyEyebrow": "System Reliability",
    "safetyHeading": "Prove Your Power System Can Survive Its Worst Day",
    "safetyBody": "A power system that works on a normal afternoon may not survive a motor start at shift change or a fault at a remote feeder. Analysis shows you where the margins are.",
    "safetyBullets": [
        "Verifies every breaker interrupting rating against calculated fault current",
        "Ensures voltage regulation stays within ±5% at every critical bus",
        "Confirms protection coordination is selective across all fault types",
        "Documents the electrical baseline for {primary} audits and insurance",
        "Identifies equipment nearing thermal or interrupting capacity limits",
    ],
    "reportsEyebrow": "Deliverables",
    "reportsHeading": "Power System Report Contents",
    "reportsBody": "One engagement, one report, everything you need for insurer audits, regulatory filings, and internal engineering review.",
    "reportsBullets": [
        "Updated single-line diagram with every component modelled",
        "Load flow results bus-by-bus under normal and contingency scenarios",
        "Short-circuit fault currents and breaker-duty comparisons",
        "Protection coordination curves with every device plotted",
        "Ranked list of findings with proposed remediation and estimated cost",
    ],
    "processSteps": [
        ("Single-Line Review", "Collect existing single-line diagrams, nameplate data, relay settings, and utility fault data."),
        ("System Modeling", "Build the complete ETAP model with verified impedances and protective device characteristics."),
        ("Multi-Study Analysis", "Run load flow, short circuit, and coordination studies in sequence on the same model for consistent results."),
        ("Integrated Report", "Deliver a single report package with findings ranked by severity plus recommended relay settings."),
    ],
    "faqs": [
        ("What is a power system study?", "A power system study is an engineering analysis of an electrical network that combines load flow, short circuit, and protection coordination into a single integrated assessment. The study quantifies how the system performs under normal operation, fault conditions, and switching events. It provides the technical baseline for capacity planning, protection upgrades, and {primary} compliance."),
        ("What's included in a Carelabs power system study?", "Every Carelabs power system study includes a load flow analysis at normal and contingency conditions, short circuit calculations per IEC 60909, protection coordination with time-current curves, voltage regulation assessment, and a ranked findings list. We build the model in ETAP and deliver a single integrated report rather than separate deliverables."),
        ("How often should a power system study be updated?", "Refresh the study every 5 years or immediately after any material change — new transformer, new generation source, significant load addition, or upstream utility upgrade. Stale studies are a common audit finding under {primary}. The {adj} electrical code requires that protective devices match current system conditions, which only a current study can verify."),
        ("What software is used for the analysis?", "Carelabs engineers use ETAP (Electrical Transient Analyser Program) — the industry-standard power system analysis platform. ETAP handles load flow, short circuit, protection coordination, arc flash, transient stability, and harmonic studies in a single environment. The output includes one-line diagrams, time-current curves, and compliance reports."),
        ("Is a power system study required by {primary}?", "{primary} requires employers to ensure electrical installations are safe, properly rated, and coordinated with protective devices. A power system study is the engineering document that proves compliance. {authority} auditors typically request the most recent study during inspections. Carelabs delivers studies that meet {primary} and international best practices."),
    ],
    "ctaBannerHeading": "Get a Baseline Your Operations Team Can Build On",
    "ctaBannerBody_tpl": "Carelabs engineers deliver full power system studies across {cities} Load flow + short circuit + coordination + transients in one engagement.",
}


# Service 5 — POWER QUALITY ANALYSIS
POWER_QUALITY = {
    "title": "Power Quality Analysis",
    "eyebrow": "Power Quality",
    "metaTitle_tpl": "Power Quality Analysis in {country} | IEEE 1159 | Carelabs",
    "metaDescription_tpl": "IEEE 1159-compliant power quality monitoring for {adj} facilities. Voltage sag/swell analysis, transient capture, and remediation planning.",
    "definitionalLede": "Power quality analysis measures voltage and current disturbances — sags, swells, transients, harmonics, imbalance, flicker — at the point where sensitive equipment connects to the grid, using IEEE 1159 classification methodology to diagnose recurring failures and design targeted mitigation.",
    "seoKeywords_tpl": [
        "power quality analysis {country}",
        "voltage sag",
        "IEEE 1159",
        "transient analysis",
        "power quality survey",
    ],
    "featuresHeading": "Power Quality Issues We Track",
    "featuresSubtext_tpl": "Most equipment in a modern {adj} facility is more sensitive to supply anomalies than the equipment it replaced. Measuring what's actually on the bus is the first step to fixing what's breaking.",
    "features": [
        ("Power Quality Monitoring", "Class A IEC 61000-4-30 analysers deployed for 7-30 day continuous recording at the PCC and sensitive buses."),
        ("Voltage Event Classification", "Every sag, swell, interruption, and transient classified per IEEE 1159 with magnitude, duration, and waveform capture."),
        ("Harmonic Spectrum Analysis", "Individual harmonic orders measured and plotted against IEEE 519 limits at voltage and current level."),
        ("Transient Capture", "High-speed sampling captures sub-cycle events — capacitor switching, lightning-induced surges, fast transient bursts."),
        ("Grounding Assessment", "Neutral-to-ground voltage measurement and ground-loop analysis for installations where sensitive electronics misbehave."),
        ("PQ Improvement Recommendations", "Ranked remediation — UPS, isolation transformer, SPD, filter, or supply reconfiguration — with estimated ROI per mitigation."),
    ],
    "safetyEyebrow": "Equipment Protection",
    "safetyHeading": "Prevent the Failures You Can't Explain",
    "safetyBody": "Poor power quality degrades equipment silently. Motors age faster on unbalanced voltage. Capacitors fail when they resonate. Drives trip on transients.",
    "safetyBullets": [
        "Identifies voltage sags that cause intermittent PLC and VFD dropout",
        "Detects high-frequency transients that damage power electronics",
        "Distinguishes utility-side problems from facility-internal sources",
        "Quantifies power quality cost — lost production, equipment replacement",
        "Provides evidence for utility service quality disputes under {country} regulations",
    ],
    "reportsEyebrow": "Deliverables",
    "reportsHeading": "Power Quality Report Contents",
    "reportsBody": "A complete digital report plus the raw measurement files so your engineering team can reopen the data anytime. Aligned with IEEE 519, IEC 61000-4-30, and IEEE 1159.",
    "reportsBullets": [
        "Event log: every sag, swell, interruption, and transient time-stamped",
        "Voltage and current trends over the measurement window",
        "THD and individual harmonic spectrum at each measurement point",
        "Flicker measurements (Pst, Plt) where relevant",
        "Ranked remediation — source identification, proposed fix, estimated cost",
    ],
    "processSteps": [
        ("PQ Meter Deployment", "Install class A analysers at the PCC and 2-4 critical distribution boards identified with operations."),
        ("Monitoring Period", "Continuous recording for 7-30 days to capture all shifts, weekend/weekday differences, and rare events."),
        ("Data Analysis", "Correlate measured events with production logs; separate utility-source issues from internal-source issues."),
        ("Corrective Actions", "Deliver ranked remediation plan with estimated ROI and implementation sequence."),
    ],
    "faqs": [
        ("What is a power quality analysis?", "Power quality analysis is the measurement and classification of voltage and current disturbances — voltage sags, swells, transients, harmonics, imbalance, flicker, and interruptions — at a facility's connection to the grid. Using IEEE 1159 methodology, the study identifies recurring problems, their sources, and designs targeted mitigation that matches the specific disturbances observed."),
        ("What causes poor power quality?", "Power quality problems come from two directions. Utility-side: lightning strikes, remote faults, switching operations, and motor starts on neighbouring facilities. Facility-internal: large motor starts, welders, arc furnaces, harmonic-generating drives, and poorly grounded electronics. A Carelabs study separates the two, which matters because the fix is different for each source."),
        ("How long does power quality monitoring take?", "A representative power quality survey requires 7 to 30 days of continuous class A monitoring at the PCC and 2-4 critical buses. Seven days captures one full production cycle including weekday/weekend variation. Thirty days adds rare-event coverage — storm transients, maintenance switching, and shift-change motor starts. For {adj} industrial facilities, 14 days is typical."),
        ("What equipment is used for power quality measurement?", "Carelabs uses class A power quality analysers certified to IEC 61000-4-30 — the international standard for PQ measurement methodology. Class A instruments capture every sub-cycle event, calculate true RMS voltage and current, measure harmonic spectrum to the 50th order, and classify voltage events per IEEE 1159. Data is time-stamped to ±20 ms accuracy."),
        ("Does {primary} address power quality?", "{primary} focuses on electrical installation safety rather than power quality specifically. However, utility connection agreements in {country} typically reference IEEE 519 for harmonics and IEEE 1159 for voltage events. Power quality problems that cause equipment failures or production loss may be addressable through utility service quality disputes under {country} regulatory frameworks."),
    ],
    "ctaBannerHeading": "Measure It, Then Fix It",
    "ctaBannerBody_tpl": "Carelabs delivers class-A power quality surveys across {cities} IEC 61000-4-30 measurement, IEEE 519 evaluation, ranked remediation.",
}


SERVICE_TEMPLATES = {
    "arc-flash-study": ARC_FLASH,
    "harmonic-study-and-analysis": HARMONIC,
    "motor-start-analysis": MOTOR_START,
    "power-system-study-and-analysis": POWER_SYSTEM,
    "power-quality-analysis": POWER_QUALITY,
}


def build_payload(slug_key: str, ctx: dict) -> dict:
    t = SERVICE_TEMPLATES[slug_key]
    return {
        "title": t["title"],
        "eyebrow": t["eyebrow"],
        "metaTitle": render(t["metaTitle_tpl"], ctx),
        "metaDescription": render(t["metaDescription_tpl"], ctx),
        "definitionalLede": render(t["definitionalLede"], ctx),
        "seoKeywords": [render(k, ctx) for k in t["seoKeywords_tpl"]],
        "trustBadges": trust_badges(ctx),
        "featuresHeading": t["featuresHeading"],
        "featuresSubtext": render(t["featuresSubtext_tpl"], ctx),
        "features": [
            {"title": title, "description": render(desc, ctx)}
            for (title, desc) in t["features"]
        ],
        "safetyEyebrow": t["safetyEyebrow"],
        "safetyHeading": t["safetyHeading"],
        "safetyBody": render(t["safetyBody"], ctx),
        "safetyBullets": [render(b, ctx) for b in t["safetyBullets"]],
        "reportsEyebrow": t["reportsEyebrow"],
        "reportsHeading": t["reportsHeading"],
        "reportsBody": render(t["reportsBody"], ctx),
        "reportsBullets": [render(b, ctx) for b in t["reportsBullets"]],
        "processHeading": "Our Process",
        "processSteps": [
            {"number": i + 1, "title": title, "description": render(desc, ctx)}
            for i, (title, desc) in enumerate(t["processSteps"])
        ],
        "faqs": [
            {"question": render(q, ctx), "answer": render(a, ctx)}
            for (q, a) in t["faqs"]
        ],
        "faqSectionHeading": "Frequently Asked Questions",
        "ctaBannerHeading": t["ctaBannerHeading"],
        "ctaBannerBody": render(t["ctaBannerBody_tpl"], ctx),
        "ctaBannerPrimaryText": "Request a Free Quote",
        "ctaBannerPrimaryHref": f"/{ctx['cc']}/contact-us/",
        "ctaBannerSecondaryText": "Explore All Services",
        "ctaBannerSecondaryHref": f"/{ctx['cc']}/services/",
    }


def get_service_doc_ids(cc: str) -> dict:
    """Map service slug root -> documentId for the given country."""
    qs = (
        f"filters[region][$eq]={cc}"
        "&fields[0]=documentId&fields[1]=slug&pagination[pageSize]=20"
    )
    r = http("GET", f"/api/service-pages?{qs}")
    if "__error" in r:
        raise RuntimeError(f"query {cc}: {r['__error']}")
    out = {}
    for e in r.get("data", []):
        slug = e.get("slug") or ""
        # Strip "-{cc}" suffix to get the slug key
        suffix = f"-{cc}"
        key = slug[: -len(suffix)] if slug.endswith(suffix) else slug
        if key in SERVICE_TEMPLATES:
            out[key] = e.get("documentId")
    return out


def run_country(cc: str) -> dict:
    ctx = dict(COUNTRIES[cc])
    ctx["cc"] = cc
    print(f"\n{'=' * 72}")
    print(f"  {cc.upper()}  -  {ctx['country']}")
    print('=' * 72)

    doc_ids = get_service_doc_ids(cc)
    missing = set(SERVICE_TEMPLATES.keys()) - set(doc_ids.keys())
    if missing:
        print(f"  [WARN] missing documentIds for: {', '.join(missing)}")

    stats = {"ok": 0, "fail": 0}
    for slug_key, doc_id in doc_ids.items():
        payload = build_payload(slug_key, ctx)
        r = http("PUT", f"/api/service-pages/{doc_id}", payload)
        if "__error" in r:
            print(f"  [ERR] {slug_key}: {r['__error'][:150]}")
            stats["fail"] += 1
        else:
            nf = len(payload["features"])
            ns = len(payload["processSteps"])
            nb = len(payload["safetyBullets"])
            nq = len(payload["faqs"])
            print(
                f"  [OK ] {slug_key:<35} features={nf} steps={ns} "
                f"safety={nb} faqs={nq}"
            )
            stats["ok"] += 1
    return stats


def main():
    ccs = [sys.argv[1]] if len(sys.argv) > 1 else list(COUNTRIES.keys())
    totals = {}
    for cc in ccs:
        totals[cc] = run_country(cc)

    print()
    print("=" * 72)
    print("  FINAL SUMMARY")
    print("=" * 72)
    total_ok = total_fail = 0
    for cc, s in totals.items():
        print(f"  {cc.upper()}  updated={s['ok']:>2}  failed={s['fail']:>2}")
        total_ok += s["ok"]
        total_fail += s["fail"]
    print(f"\n  TOTAL: {total_ok} services updated, {total_fail} failed")


if __name__ == "__main__":
    main()
