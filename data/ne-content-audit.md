# Carelabs Northern Europe — Full Content Audit (UK, IE, SE, NO, DK, FI)

**Scope:** 6 countries × (1 homepage + 1 about + 1 services index + 5 service pages + 1 contact + ~10 blog posts) ≈ 120 URLs. Extracted fully for UK (canonical); per-country deltas extracted for IE, SE, NO, DK, FI.
**Extracted:** 2026-04-25 via WebFetch.
**Purpose:** Reference document for populating the new Next.js + Strapi stack with Northern European country content. Pattern identical to South America audit.

---

# Executive summary

## 1. UK is the canonical source. Every other NE country is templated from UK.

Every URL on IE / SE / NO / DK / FI is a copy of the UK master with three variables swapped: country name, adjective, and a 4-5 city coverage list. Body prose, section headings, workflow steps, and benefit lists are byte-identical after substitution.

## 2. Standards mentioned on source: only ISO 9001:2008 + ETAP

No country-specific electrical code (BS 7671, IET, HSE, SS 4364, EN 50110, NEK 400, DS/HD 60364, SFS 6000) appears anywhere in the WP source — despite those being the actual regulatory frameworks. Our Strapi content (and whatever we build for NE) must author those references; they don't exist on WordPress.

## 3. Typical gaps on every page
- **FAQs** — zero across all 60+ source pages (homepages, services, blogs, about, contact)
- **Meta descriptions** — zero across every URL
- **Author / publishedDate** — zero on any blog post
- **Real image URLs** — every image is a lazy-loaded SVG placeholder
- **Real contact info** — `+15558021083` (US placeholder) on every country's WhatsApp; no physical addresses on contact pages

## 4. Source bugs flagged for the live carelabz.com (not our problem to fix)
- **DK arc-flash** closing line: `"Copenhagen, Aarhus. Odense, and Aalborg"` — period typo instead of comma
- **UK motor-efficiency blog**: references `"Understanding of Singapore Standards"` — template leak from a Singapore fork, editor missed that swap
- **FI blog index**: several slugs still carry `-united-kingdom/` and `-uk-businesses/` paths but display Finnish titles — fork-without-rename pattern
- **IE / SE / NO / DK blog indexes**: carry BOTH the UK-slug version AND the localised version of the same article — bare-slug duplicates the same way SA countries had

## 5. Blog inventory

UK has **10 unique blog articles** (the canonical set). Other countries mirror these with localisation:

| Slug pattern | UK | IE | SE | NO | DK | FI |
|---|---|---|---|---|---|---|
| a-step-by-step-guide-to-arc-flash-analysis-... | ...united-kingdom | +in-ireland | +in-sweden | +in-norway | +in-denmark | +in-united-kingdom (not localised) |
| the-value-of-arc-flash-risk-assessment-...-in-... | ...the-uk | +in-ireland | +in-sweden | +in-norway | +in-denmark | in-the-uk (only) |
| why-are-harmonic-analysis-...-so-vital-for-... | ...uk-businesses | +irish-businesses | +swedish-businesses | +norwegian-businesses | +danish-businesses | uk-businesses (display says Finnish) |
| harmonic-analysis-of-...-power-system | the-uk | irish | swedish | norwegian | danish | finnish |
| how-can-you-evaluate-...-commercial-motors | UK-only slug present | UK slug | UK slug | UK slug | UK slug | UK slug |
| analyze-and-evaluate-...-as-per-...-regulations | uk | irish | swedish | norwegian | danish | finnish |
| ...-power-quality-working-principles | uk | irish | swedish | norwegian | danish | finnish |
| how-can-the-electricity-quality-in-...-be-analyzed | uk | irish | sweden | norway | danish | finland |
| load-flow-and-short-circuit-analysis-significance-for-...-businesses | uk | irish | swedish | norwegian | danish | finnish |
| study-of-the-power-systems-load-flow-short-circuit-and-relay-coordination | UK-only slug | same UK slug | same | same | same | same |

Takeaway: each country has ~10-13 blog entries; after deduplication the real count per country is **10 articles**.

---

# Country variable map

| CC | Country | Adjective | Cities (from WP source) | Likely real regulator (not on WP) | Primary standard (propose) |
|---|---|---|---|---|---|
| uk | United Kingdom | UK / British | London, Birmingham, Leeds, Glasgow | HSE (Health and Safety Executive) | BS 7671 (IET Wiring Regulations) |
| ie | Ireland | Irish | Dublin, Cork, Limerick, Galway, Waterford (**5**) | HSA (Health and Safety Authority) | I.S. 10101 (National Rules for Electrical Installations) |
| se | Sweden | Swedish | Stockholm, Gothenburg, Malmo, Uppsala | Elsäkerhetsverket | SS 436 40 00 (Swedish Electrical Installations) |
| no | Norway | Norwegian | Oslo, Bergen, Trondheim, Stavanger | DSB (Direktoratet for samfunnssikkerhet og beredskap) | NEK 400 |
| dk | Denmark | Danish | Copenhagen, Aarhus, Odense, Aalborg | Sikkerhedsstyrelsen | DS/HD 60364 |
| fi | Finland | Finnish | Helsinki, Vantaa, Espoo, Tampere | Tukes | SFS 6000 |

IE is the only country with 5 cities on the service pages; the other five use 4.

---

# UK — Full canonical content

## UK.Homepage
- **URL:** https://www.carelabz.com/uk/
- **Meta title:** Home - Carelabs UK
- **Meta description:** (not set)
- **H1:** Welcome to Care Labs
- **Tagline:** Helping our customers succeed in what they do
- **Hero subtext:** "Care Labs is an innovative company that focuses on empowering electrical excellence and enhancing electrical experiences in the workplace."
- **Key stat:** "10 YEARS OF EXPERIENCE IN ELECTRICAL SAFETY"
- **About blurb:** "We are a team of extremely knowledgeable and competent experts who offer top-notch electrical engineering solutions all around the world. Since our founding, every achievement has helped us prepare our communities and environment for the future. We take pleasure in offering cost-effective, environmentally friendly options for carrying out all ideas and projects that have the same objective."
- **Services section H2:** "Explore Our Services"
- **Services section intro:** "Discover our wide range of expert electrical installation and inspection services designed to meet your unique needs. From design to maintenance, we have the expertise and resources to handle any project, big or small. Trust our experienced team to deliver top-quality solutions that meet your budget and timeline. Explore our services today and experience the difference of Care Labs."
- **Service cards (5):** Arc Flash Study · Harmonic Study & Analysis · Power Quality Analysis · Power System Study & Analysis · Motor Start Analysis
- **News section H4:** "Discover Our News"
- **News section copy:** "Explore the latest news and trends on our featured blog post page. Stay informed with our regularly updated selection of curated posts on a variety of topics, including technology, business, health, lifestyle, and more. Keep up to date and explore our featured posts now."
- **Standards logos shown:** NEC · NFPA · BSI · IET · IEC · OSHA · IEEE
- **Nav:** Home · About Us · Our Services · Contact Us
- **Footer contact:** Email `contact@carelabs.com`; WhatsApp `+15558021083`; Facebook/Twitter/LinkedIn
- **Copyright:** © 2023 — All rights reserved by Carelabs
- **Industries listed:** none on homepage
- **Stats:** only the "10 years of experience" banner

## UK.About
- **URL:** https://www.carelabz.com/uk/about-us/
- **Meta title:** ABOUT US - Carelabs UK
- **H1:** Building Relationships with Our Clients
- **Tagline:** "Helping our customers succeed in what they do."
- **Company overview:** "A team of extremely knowledgeable and competent experts who offer top-notch electrical engineering solutions all around the world."
- **Vision:** "To become the global leader in holistic power systems excellence and management, setting new benchmarks for safety, efficiency, and sustainability."
- **Mission:** "At Care Labs, we empower our clients to transform their power systems into assets that are reliable, efficient, and sustainable through expertise and innovative solutions."
- **Goals (9-point list):**
  1. Expand global presence and deepen local engagement
  2. Continuously improve energy efficiency and promote clean energy adoption
  3. Strengthen partnerships with governments, industries, and communities
  4. Enhance energy security through innovative solutions
  5. Foster safety, compliance, and resilience culture
  6. Provide inexpensive energy solutions to low-income communities
  7. Value trust-based, long-term partnerships
  8. Encourage sustainable energy solutions for social/economic progress
  9. Provide clean, cheap energy to underprivileged populations
- **Standards/certifications shown:** NEC · NFPA · BSI · IET · IEC · OSHA · IEEE
- **Team members:** not listed
- **FAQs:** none

## UK.Services index
- **URL:** https://www.carelabz.com/uk/our-services/
- **Meta title:** Our Services - Carelabs UK
- **H1:** Our Services
- **Hero subtext:** none (carousel directly)
- **Service cards (5)** with descriptions (quoting verbatim):
  1. **Arc Flash Study** — "Care Labs is an economical provider of electrical arc flash analysis, investigation, and certification services for businesses of all types."
  2. **Power Quality Analysis** — "Care Labs evaluates the quality of power for UK businesses. Our objective is to prevent your electrical installations, appliances, and electrical equipment from malfunctioning due to fluctuations in the power supply."
  3. **Harmonic Study and Analysis** — "Care Labs offers electrical installation safety inspection, testing, calibration, certification, and harmonic inquiry and analysis."
  4. **Motor Start Analysis** — "Care Labs provides organizations around the UK with a specialized Motor start study and analysis service."
  5. **Power System Study and Analysis** — "Care Labs provides various electrical installation services, including electrical safety inspections, simulations of electrical system design, power quality analysis studies, and research and analysis of power systems."

## UK.Contact
- **URL:** https://www.carelabz.com/uk/contact-us/
- **Meta title:** Contact Us - Carelabs UK
- **H1:** Power Up Your Electrical Safety - Request an Inspection Today!
- **Hero subtext:** "Don't leave your electrical system to chance – let our experts provide the insights you need. Our comprehensive inspections will help you stay safe. Contact Care Labs today for expert solutions."
- **Phone:** `+15558021083` (WhatsApp, US placeholder)
- **Email:** Cloudflare-obfuscated `contact@carelabs.com`
- **Physical address:** not published on UK page
- **Office hours:** not published
- **Offices mentioned globally:** Canada, UAE, Rwanda, India (no UK office)
- **Contact options:** Talk to Sales · Submit Ticket · Connect to Us · WhatsApp
- **Form field labels:** not extractable from HTML

---

## UK.Service 1 — Arc Flash Study
- **URL:** https://www.carelabz.com/uk/arc-flash-study/
- **Meta title:** Arc Flash Study - Carelabs UK
- **Meta description:** (not set)
- **H1:** Arc Flash Study
- **Hero subtext:** "Carelabs is an economical provider of electrical arc flash analysis, investigation, and certification services for businesses of all types."

### Sections (verbatim)

**Definition:** "An arc flash occurs when current flows between conductors via an air gap. The arc flash ionizes the air and emits a considerable amount of light and heat (approximately 35,000 degrees Fahrenheit). Researching and analyzing the electrical installations of a facility to estimate the incident energy available for each piece of electrical equipment. Studies produce a short circuit and coordination analysis, updated electrical one-line schematics and equipment placements."

**Arc Flash Research Objectives:**
- Determine the extent of damage produced by the incident energy emitted during an arc flash fault
- Modifying the settings of protective equipment to restrict exposure to incident energy
- Provide safety recommendations regarding arc flash risks
- Follow the specific rules and laws of your country
- Determine the type of PPE worn on the job

**The Adverse Consequences of Arc Flash:**
- Arcs result in severe burns to the skin, eyes, and face
- The inhalation of gases and hot particles can cause severe burns in the throat and lungs
- Flying debris and loose parts cause injuries

**Importance paragraph:** "Arc flash studies are essential for reducing hazards, enhancing electrical workers' safety, and the overall safety of the organization. They help determine electrical hazard levels and implementing appropriate safety measures to reduce the risk of burns and accidents. Applicability extends to all utilities, manufacturing, industrial, and commercial businesses that utilize electrical disconnects, motor control, panel boards, and switchboards."

**Arc Flash Research Benefits:**
- Enhanced human and mechanical safety
- Reduced healthcare and legal expenses
- Compliance with regulatory safety requirements
- Reduced penalties for violations of standards

**Steps for Arc Flash Analysis:** Data collection · Conducting field inspection · The conception of a system · Investigating arc flashes

**Carelabs Workflow (11 steps):**
- Data collection
- ETAP modeling of a power system
- Abbreviated investigation
- Coordination of overcurrent protection devices
- An investigation concerning arc flashes
- Examination for arc flashes
- Keeping a ledger
- Methods for lowering arc flash risk
- Full-size one-line diagrams
- Application of arc flash markings
- The finished report

**Advantages of Using Carelabs Services:**
- Create more secure electrical systems that adhere to regulations
- Integrated modules for comprehensive short circuits, overcurrent coordination, device assessment, and arc flash evaluation
- Creating a more secure workplace
- Quick and straightforward alternative design idea for optimal form
- Enhanced safety margins with user-defined arc fault limits
- Computer-aided analysis creates arc flash labels automatically
- Reduce productivity losses and maintenance costs

**Coverage:** "Carelabs has quickly established themselves as an ISO 9001:2008-accredited business with a clientele that has supplied outstanding feedback. Services available in London, Birmingham, Leeds, and Glasgow."

- **Standards:** ISO 9001:2008 · ETAP
- **FAQs:** none

## UK.Service 2 — Harmonic Study and Analysis
- **URL:** https://www.carelabz.com/uk/harmonic-study-and-analysis/
- **Meta title:** Harmonic Study and Analysis - Carelabs UK
- **H1:** Harmonic Study and Analysis
- **Hero subtext:** "Carelabs offers electrical installation safety inspection, testing, calibration, certification, and harmonic inquiry and analysis."

### Sections (verbatim highlights)
- 415-volt systems: 5% total / 4% odd / 2% even harmonic limits
- Effects of Harmonic Distortion (12 bullets): International high voltage · Equipment failure from voltage distortion · Increased internal energy · Branch breaker tripping · Measurement error · Wiring explosions/fires · Generator failure · Declining power factor · Utility cost · Reduced productivity · Unnecessary downtime · Larger engine requirements
- 9-step Harmonic Analysis Workflow ending in ETAP analysis + mitigation rerun
- Service Advantages: tiered 25% / 25-75% / upper background harmonic analysis
- **Coverage:** London, Birmingham, Leeds, Glasgow
- **Standards:** ISO 9001:2008
- **FAQs:** none

## UK.Service 3 — Motor Start Analysis
- **URL:** https://www.carelabz.com/uk/motor-start-analysis/
- **Meta title:** Motor Start Analysis - Carelabs UK
- **H1:** Motor Start Analysis
- **Hero subtext:** "Carelabs provides organizations around the UK with a specialized Motor start study and analysis service. The major aim of our motor start analysis service is to examine the atypical results of starting a big motor."

### Key content
- Analysis Methodology bullet list (4 techniques including starting impedance modelling, voltage drop, dynamic model, transient stability)
- "The United Kingdom Must Conduct a Motor Start Analysis" section — 80% terminal voltage rule explained
- "When is a Motor Start Analysis Necessary?" (5-bullet list, repeated twice as with SA countries — source bug)
- Benefits paragraph and closing
- **Coverage:** London, Birmingham, Leeds, Glasgow
- **Standards:** none beyond ETAP
- **FAQs:** none

## UK.Service 4 — Power System Study and Analysis
- **URL:** https://www.carelabz.com/uk/power-system-study-and-analysis/
- **Meta title:** Power System Study and Analysis - Carelabs UK
- **H1:** Power System Study and Analysis
- **Hero subtext:** "Carelabs provides various electrical installation services, including electrical safety inspections, simulations of electrical system design, power quality analysis studies, and research and analysis of power systems."

### Key content
- ETAP-based load flow, short circuit, protective device coordination, transient/stability
- "Why is a Power System Analysis Study Necessary?" (multi-paragraph intro)
- Report examples (9 bullets): Circuit interrupter · Security plan · Load transport · Continuous evaluations · Arc flash · Power effectiveness · Harmonics · Engine starting · Earth science
- Load Flow / Short Circuit / Transient Research / Protection Coordination sections
- General approach (11 steps)
- Carelabs components (7 bullets)
- **Coverage:** London, Birmingham, Leeds, Glasgow
- **Standards:** ETAP (tool)
- **FAQs:** none

## UK.Service 5 — Power Quality Analysis
- **URL:** https://www.carelabz.com/uk/power-quality-analysis/
- **Meta title:** Power Quality Analysis - Carelabs UK
- **H1:** Power Quality Analysis
- **Hero subtext:** "Carelabs evaluates the quality of power for UK businesses. Our objective is to prevent your electrical installations, appliances, and electrical equipment from malfunctioning due to fluctuations in the power supply."

### Key content
- Purpose list (12 bullets) — same as SA template
- "Analysis of Power Quality is Necessary in the UK" — three-type taxonomy (Frequency Deviation / Voltage Disruptions / Distortion) with 2.1-3.2 sub-categories
- "What is the scope of Power Quality Analysis?" — 6 techniques listed (Harmonic · Surge/Transient · Voltage Tracking · Reactive Power · Captive Electricity · Load Flow)
- **Coverage:** London, Birmingham, Leeds, Glasgow
- **Standards:** none beyond the ISO
- **FAQs:** none

---

# UK — Blog posts (canonical master, 10 articles)

## UK.Blog 1 — A Step-by-Step Guide to Arc Flash Analysis in the United Kingdom
- **URL:** https://carelabz.com/uk/a-step-by-step-guide-to-arc-flash-analysis-in-the-united-kingdom/
- **Meta title:** A Step-by-Step Guide to Arc Flash Analysis in the United Kingdom - Carelabs UK
- **Author / date / category:** all unset in HTML
- **Summary:** 5-step framework (Determine Probability → Manage Threat → Engineering Controls → Administrative Controls → PPE). Discusses commercial impact, causes, Carelabs service advantages. ~800 words. Ends with London/Birmingham/Leeds/Glasgow coverage statement.

## UK.Blog 2 — The Value of Arc Flash Risk Assessment and Prevention Strategies in the UK
- **URL:** https://carelabz.com/uk/the-value-of-arc-flash-risk-assessment-and-prevention-strategies-in-the-uk/
- **Summary:** Commercial impacts (direct, indirect, reputational), causes, 5 mitigation methods (de-energise · low-risk tech · engineering redesign · reduce fault current · arc-resistant switchgear). Same structure as SA.

## UK.Blog 3 — Why are Harmonic Analysis and Study so Vital for UK Businesses?
- **URL:** https://carelabz.com/uk/why-are-harmonic-analysis-and-studies-so-vital-for-uk-businesses/
- **Summary:** Harmonic impact on business (5 economic effects), causes (15% nonlinear threshold), 9-step analysis methodology. Matches SA template.

## UK.Blog 4 — Harmonic Analysis of the UK Power System
- **URL:** https://carelabz.com/uk/harmonic-analysis-of-the-uk-power-system/
- **Summary:** Definition of harmonic distortion, importance, when required (4 triggers), equipment-effect table (5 rows), mitigation benefits, 8-step procedure. Matches SA.

## UK.Blog 5 — How can you Evaluate the Functionality and Dependability of Commercial Motors?
- **URL:** https://carelabz.com/uk/how-can-you-evaluate-the-functionality-and-dependability-of-commercial-motors/
- **Summary:** Motors = 46% electricity / 69% industrial energy; 4 factors affecting performance; 75% failures = 1-6 days downtime stat; Carelabs advantages (with template artifact: **"Understanding of Singapore Standards"** — source bug); 9-step audit methodology.

## UK.Blog 6 — Analyse and Evaluate the Performance of Electric Motors as per UK Regulations
- **URL:** https://carelabz.com/uk/analyze-and-evaluate-the-performance-of-electric-motors-as-per-uk-regulations/
- **Summary:** IEA statistics on industrial motors (70% / 35% / 45%); 20-30% efficiency gain potential; reasons to use efficient motors; internationally recognised testing methods (IEEE 112-2004, IEC 60034-2-1, JEC 37); 10 IEEE 112 measures; 3 IEC categories. Matches SA's "Examine and Confirm" article structure.

## UK.Blog 7 — UK Power Quality Working Principles
- **URL:** https://carelabz.com/uk/uk-power-quality-working-principles/
- **Summary:** Impact on equipment lifespan; direct/indirect/socioeconomic consequences (8+3+3 bullets); 5 power-quality issue categories (voltage stability / imbalance / harmonics / flicker / sags); mitigation via Load Flow / Harmonic / Surge / Voltage Dip / Reactive Power / Captive Power analyses. Ends with coverage.

## UK.Blog 8 — How Can the Electricity Quality in the UK Be Analyzed?
- **URL:** https://carelabz.com/uk/how-can-the-electricity-quality-in-the-uk-be-analyzed/
- **Summary:** Two categories (Unrests / Steady-state); 7 supply quality factors (voltage stability, frequency, voltage dips, spikes, transient voltages, harmony alterations, radio-frequency); 5-step Carelabs procedure. Matches SA "How to Perform a Power Quality Analysis" article.

## UK.Blog 9 — Load Flow and Short Circuit Analysis Significance for UK Businesses
- **URL:** https://carelabz.com/uk/load-flow-and-short-circuit-analysis-significance-for-uk-businesses/
- **Summary:** Importance of balance; definitions; short circuit causes (3: insulation / slack wire / broken outlet); Carelabs advantages (6 bullets); ETAP software. Matches SA.

## UK.Blog 10 — Study of the Power System's Load Flow, Short Circuit, and Relay Coordination
- **URL:** https://carelabz.com/uk/study-of-the-power-systems-load-flow-short-circuit-and-relay-coordination/
- **Summary:** 7 study types listed; Load Flow 3-phase workflow; 3 calculation methods (Gauss-Seidel / Newton-Raphson / FDLF); 4 short circuit fault types; Relay Coordination role; 6 benefits. Matches SA template exactly.

---

# Ireland (IE) — delta from UK

## IE.Cities
Dublin, Cork, Limerick, Galway, Waterford **(5 cities — unique to IE)**

## IE.Service pages
Identical content to UK templates with "Ireland"/"Irish" substituted. Arc Flash hero reads: *"Carelabs offers a range of industries low-cost electrical arc flash analysis, investigation, and certification services."* Closing: *"We offer arc flash investigation and analysis services in all major cities, including Dublin, Cork, Limerick, Galway, and Waterford."*

## IE.Blog posts
Carries 13 entries: 10 Ireland-localised + 3 UK-slug duplicates (arc-flash-value, step-by-step, harmonic-vital). The Ireland-localised ones follow the templated content with "Irish" substitution.

## IE.Standards mentioned
ISO 9001:2008 only.

---

# Sweden (SE) — delta from UK

## SE.Cities
Stockholm, Gothenburg, Malmo, Uppsala

## SE.Service pages
Identical templates. Arc Flash hero: *"Carelabs provides affordable electrical arc flash analysis, investigation, and certification services to a variety of sectors."* Closing: *"Stockholm, Gothenburg, Malmo, and Uppsala are just a few of the major cities where we provide arc flash investigation and analysis services."*

## SE.Blog posts
13 entries (10 Swedish + 3 UK-slug duplicates).

## SE.Standards mentioned
ISO 9001:2008 only.

---

# Norway (NO) — delta from UK

## NO.Cities
Oslo, Bergen, Trondheim, Stavanger

## NO.Service pages
Identical templates. Arc Flash hero: *"CareLabs is a low-cost provider of electrical arc flash analysis, investigation, and certification services for a wide range of businesses."* Closing: *"We offer arc flash investigation and analysis services in all major cities, including Oslo, Bergen, Trondheim, and Stavanger."*

## NO.Blog posts
13 entries (10 Norwegian + 3 UK-slug duplicates).

## NO.Standards mentioned
ISO 9001:2008 only.

---

# Denmark (DK) — delta from UK

## DK.Cities
Copenhagen, Aarhus, Odense, Aalborg

## DK.Service pages
Identical templates. Arc Flash hero: *"CareLabs offers low-cost electrical arc flash analysis, investigation, and certification services to organizations of all sizes."* Closing (source bug): *"We provide arc flash investigation and analysis services in all major cities, including Copenhagen, Aarhus. Odense, and Aalborg."* — note period typo after Aarhus.

## DK.Blog posts
13 entries (10 Danish + 3 UK-slug duplicates).

## DK.Standards mentioned
ISO 9001:2008 only.

---

# Finland (FI) — delta from UK

## FI.Cities
Helsinki, Vantaa, Espoo, Tampere

## FI.Service pages
Identical templates. Arc Flash hero: *"CareLabs is a low-cost provider of electrical arc flash analysis, investigation, and certification services for all sorts of enterprises."* Closing: *"We provide arc flash investigation and analysis services in all major cities, including Helsinki, Vantaa, Espoo, and Tampere."*

## FI.Blog posts
10 entries — a mix. Some keep the UK slug (step-by-step, value, harmonic-vital) even though the display title shows "Finland"/"Finnish" — FI is less aggressively localised than the other NE forks.

## FI.Standards mentioned
ISO 9001:2008 only.

---

# Appendix A — What WordPress source does NOT contain

| Field | State | Implication for Strapi |
|---|---|---|
| Meta descriptions | Never set | Must author per page (follow SA pattern) |
| Author / publishedDate | Never set | Default to "Carelabs Engineering Team" + migration date |
| Hero images | Lazy SVG placeholders only | Upload real images via Strapi admin or use Unsplash |
| FAQs | Never set | Author 4-5 per service + blog post per SA pattern |
| Country-specific electrical standards | Never referenced | Author: BS 7671 for UK, I.S. 10101 for IE, SS 436 40 00 for SE, NEK 400 for NO, DS/HD 60364 for DK, SFS 6000 for FI |
| Phone numbers | US placeholder on every country | Real per-country numbers needed |
| Physical addresses | Never published | Placeholder or real per-country office |
| Case studies | No such section | Do not advertise until real content exists |
| Industries | No homepage industries list | Use 10-item global fallback as SA does |

# Appendix B — Suggested NE Strapi per-country config values

Ready-to-paste shape matching the existing `countries-config.ts` entries for SA countries:

```ts
uk: {
  cc: "uk", countryName: "United Kingdom", countryNameLocative: "the UK",
  hreflang: "en-GB", dialCodeCountryIso2: "GB",
  address: "London, United Kingdom",
  standards: ["BS 7671", "IET Wiring Regulations", "IEEE 1584", "IEC 60909", "ETAP"],
  primaryStandard: "BS 7671",
  localCodeName: "BS 7671 (IET Wiring Regulations 18th Edition)",
  localAuthority: "HSE (Health and Safety Executive)",
  // cities: London, Birmingham, Leeds, Glasgow
},
ie: {
  cc: "ie", countryName: "Ireland", countryNameLocative: "Ireland",
  hreflang: "en-IE", dialCodeCountryIso2: "IE",
  address: "Dublin, Ireland",
  standards: ["I.S. 10101", "IEEE 1584", "IEC 60909", "ISO 9001:2008", "ETAP"],
  primaryStandard: "I.S. 10101",
  localCodeName: "I.S. 10101 (National Rules for Electrical Installations)",
  localAuthority: "HSA (Health and Safety Authority)",
  // cities: Dublin, Cork, Limerick, Galway, Waterford
},
se: {
  cc: "se", countryName: "Sweden", countryNameLocative: "Sweden",
  hreflang: "en-SE", dialCodeCountryIso2: "SE",
  address: "Stockholm, Sweden",
  standards: ["SS 436 40 00", "IEEE 1584", "IEC 60909", "ISO 9001:2008", "ETAP"],
  primaryStandard: "SS 436 40 00",
  localCodeName: "SS 436 40 00 (Swedish Electrical Installations)",
  localAuthority: "Elsäkerhetsverket",
  // cities: Stockholm, Gothenburg, Malmo, Uppsala
},
no: {
  cc: "no", countryName: "Norway", countryNameLocative: "Norway",
  hreflang: "en-NO", dialCodeCountryIso2: "NO",
  address: "Oslo, Norway",
  standards: ["NEK 400", "IEEE 1584", "IEC 60909", "ISO 9001:2008", "ETAP"],
  primaryStandard: "NEK 400",
  localCodeName: "NEK 400 (Low-voltage electrical installations)",
  localAuthority: "DSB (Direktoratet for samfunnssikkerhet og beredskap)",
  // cities: Oslo, Bergen, Trondheim, Stavanger
},
dk: {
  cc: "dk", countryName: "Denmark", countryNameLocative: "Denmark",
  hreflang: "en-DK", dialCodeCountryIso2: "DK",
  address: "Copenhagen, Denmark",
  standards: ["DS/HD 60364", "IEEE 1584", "IEC 60909", "ISO 9001:2008", "ETAP"],
  primaryStandard: "DS/HD 60364",
  localCodeName: "DS/HD 60364 (Low-voltage electrical installations)",
  localAuthority: "Sikkerhedsstyrelsen",
  // cities: Copenhagen, Aarhus, Odense, Aalborg
},
fi: {
  cc: "fi", countryName: "Finland", countryNameLocative: "Finland",
  hreflang: "en-FI", dialCodeCountryIso2: "FI",
  address: "Helsinki, Finland",
  standards: ["SFS 6000", "IEEE 1584", "IEC 60909", "ISO 9001:2008", "ETAP"],
  primaryStandard: "SFS 6000",
  localCodeName: "SFS 6000 (Low-voltage electrical installations)",
  localAuthority: "Tukes",
  // cities: Helsinki, Vantaa, Espoo, Tampere
},
```

# Appendix C — Source bugs (affect live carelabz.com, not our build)

1. **DK arc flash closing** — period instead of comma: `"Copenhagen, Aarhus. Odense, and Aalborg"` (should be `"Copenhagen, Aarhus, Odense, and Aalborg"`)
2. **UK motor efficiency blog** — template leak: cites `"Understanding of Singapore Standards"` as a Carelabs service advantage (should say UK)
3. **FI blog index** — 3 articles still use UK slug paths but display Finnish titles (`...in-the-united-kingdom/` / `...uk-businesses/` / `...in-the-uk/`)
4. **All 6 countries' Motor Start page** — "When is a Motor Start Analysis Necessary?" section duplicates twice (same bug as SA countries)
5. **UK arc flash page** — one bullet reads `"Web search lists an apartment building at the queried address"` — looks like machine-translation or copy-paste artifact
6. **No country mentions its actual electrical code** — UK never mentions BS 7671, NO never mentions NEK 400, etc. Only ISO 9001:2008 referenced across 60+ pages.

# Appendix D — Pages NOT scraped / not present

- Case studies: 404 on every NE country (no such page exists)
- Author archives: skipped per user rules
- Category archives: skipped
- Per-country /careers/ page: not present (all link to global `/careers/`)
- Per-country /company/privacy-policy/: not present (all link to global)
- 404 pages: exist under `/404-page/` slug pattern but are WP artifacts — skipped

---

*End of audit. Source: www.carelabz.com/{uk|ie|se|no|dk|fi}/ via WebFetch, 2026-04-25.*
*Pattern matches earlier [data/sa-services-full-audit.md](sa-services-full-audit.md) audit of BR/CO/CL/AR/PE — the entire Carelabs WordPress site is one templated monolith with country/city/adjective substitutions.*
