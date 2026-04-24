# Design Inspiration Analysis — Aleia · Nobl · Align Pilates · Pilates Collective

**Purpose:** Visual-design audit for the Carelabs Northern-Europe rebuild. 16 screenshots captured at 1440×900 with Playwright + Chromium, stored under [design-research/screenshots/](../design-research/screenshots/).

**Brand constraints for adaptation:** Navy `#0B1A2F` · Orange `#F97316` · Off-white `#F8FAFC` · Slate `#1E293B`.
**Existing font stack:** Barlow Condensed (display), Playfair Display italic (accent), Poppins (body) — already loaded via `src/app/layout.tsx`.

---

# 1. ALEIA — aleia.io

**Screenshots:** [hero](../design-research/screenshots/aleia-1-hero.png) · [nav-scrolled](../design-research/screenshots/aleia-2-nav-scrolled.png) · [full](../design-research/screenshots/aleia-3-full.png) · [footer](../design-research/screenshots/aleia-4-footer.png)

### A. Navigation bar
- Layout: bracketed text labels left-aligned: `[About] [Work] [Services] [Blog] [Contact]`. Small triangular "A" monochrome logo centred. On the right: circled `FR` language toggle, `SAY Bonjour 👋` bold sans with italic serif inline, black `LIFE @ ALEIA` pill.
- Background: transparent on a full-bleed hero video → stays transparent black-text-on-white when scrolled (no sticky colour change observed).
- Font: condensed sans for labels, **square brackets used as decoration**. All caps on the pill CTAs.
- Mobile menu not visible in viewport; likely hamburger.

### B. Hero section
- Background: **full-bleed looping video** of a neon "rave" scene with stylised animal-head characters. Sits behind the fold.
- Headline: enormous condensed geometric black sans (**"Serious Digital. Not So Serio…"** — truncating off-screen on purpose, scroll reveals rest). Font is grotesk-ultra-condensed, uppercase-ish lowercase but letterforms are aggressive.
- Font-mixing: yes — the brand wordmark uses both italic serif (`Bonjour`) and bold caps sans in the same line.
- Sub-copy: small sans label **"SCROLL ↓"** bottom-left, year stamp **"©2026"** bottom-right, tiny centered paragraph *"We craft brands, interfaces, and experiences that change brands' fortunes."*
- CTA: no visible primary button in hero — the entire section is the video statement.
- Decorative: aggressive cropping of the headline to imply more content below.

### C. Sections down the page
- **Section 2** bright cyan/electric blue `#2AF2FF`-ish with white text block *"We're Hiring — This Is Your Sign"* and white pill `SHOW DETAILS`.
- **Section 3** white with logo grid of past clients (sketchy, monochrome).
- **Section 4** hot pink `#FF33B5` with huge black display sans.
- **Section 5** white headline `Since 2019 — same goals, same mindset, better tools`.
- **Section 6** bold black block *"WE GAVE AI THE BLOG, GOOGLE INDEXING APPROVED*"* — huge white type on black.
- Spacing: very generous vertical rhythm, but sections stack abruptly — hard colour transitions with no gradient.

### D. Cards / components
- Minimal cards — content blocks are full-width colour bands with one statement each.
- Logos in a 5-column grid, monochrome.
- Client case study cards (further down) are black-and-white photo thumbnails with condensed uppercase labels.

### E. Colour palette
- **Primary:** black `#000` + white `#FFF`
- **Accent:** hot pink/magenta `~#FF33B5`
- **Secondary:** electric cyan `~#25F2FF`
- Overall feel: **bold, digital, editorial, loud**.

### F. Typography
- Display: ultra-condensed grotesk (possibly **Akzidenz Grotesk** / **Haffer**/**Editorial**-family style).
- Body: neutral sans (Inter-like).
- Mixing: italic serif word ("Bonjour") dropped into sans UI.
- Line heights: very tight on display, generous on body.
- Letter-spacing: tight on display, tracked-out on small caps.

### G. CTA sections
- The "We're Hiring" block is the CTA. White pill button `SHOW DETAILS` with black text, rounded full.

### H. Footer
- Obscured in capture by cookie banner — based on the full-page screenshot, it's a classic dark band with minimal links and wordmark bottom-right.

### I. Animations / interactions
- Looping hero video
- Per the HTML, scroll-triggered fade-ins on section blocks (cannot verify without interactive)
- Ticker-style large-type cropping (headline "Blink and You'll" continues off-canvas, suggesting marquee or scroll reveal)

### J. Overall feel
- **Adjectives:** bold · editorial · playful-digital
- **Most memorable:** the bracketed `[About] [Work]` nav and the hot-pink "This Is Your Sign" block
- **Premium cue:** confidence to use large type, aggressive cropping, and whole-viewport colour blocks instead of timid imagery

---

# 2. NOBL — nobl.io

**Screenshots:** [hero](../design-research/screenshots/nobl-1-hero.png) · [nav-scrolled](../design-research/screenshots/nobl-2-nav-scrolled.png) · [full](../design-research/screenshots/nobl-3-full.png) · [footer](../design-research/screenshots/nobl-4-footer.png)

### A. Navigation bar
- Layout: thin dividing line under nav. Left cluster `CAPABILITIES · METHODOLOGY · ABOUT NOBL`, centred wordmark `NOBL` in custom display serif, right cluster `TODAY'S CHANGEMAKER` plus search icon and hamburger.
- Background: cream `#F3EAD4` — matches page. No colour shift on scroll.
- Font: all caps condensed sans for nav labels (likely **Founders Grotesk** or similar), tracked wide. Logo in bold heavy display serif with a stylised `L`.

### B. Hero section
- Background: flat cream `#F3EAD4`.
- Headline: **"Bold ambitions demand collaboration."** — massive heavy ultra-black display serif in black, centred, two lines. This is the anchor of the whole brand.
- Font mixing: none in the headline; serif throughout. But mixed against sans nav.
- Sub-copy: *"But truly working in sync takes effort."* in gray sans, below headline, centre.
- CTA: none inline — the hero is a statement. Scroll reveals a circular line-art illustration (a pendulum / figures on a circle).

### C. Sections down the page
- **Hero** cream serif statement.
- **Section 2** deep red `~#E8351C` block, white heavy serif text *"We're NOBL. We help organizations do incredible things together."*
- **Section 3** cream "Propel Your Transformation" with dark panels listing methodology.
- **Section 4** black section titled "Methodology" with yellow accents.
- **Section 5** yellow `~#FDDC33` Today's Changemaker card.
- **Section 6** cream "Let's Talk." CTA.
- Spacing: confident, wide, cream-first with punch blocks of red/black/yellow.

### D. Cards / components
- Minimal — sections of solid colour containing a single statement and optional caption.
- Small rounded 8-12 px cards where they appear.
- Illustrations are bold hand-drawn line art in black on cream.

### E. Colour palette
- **Primary:** cream `#F3EAD4`
- **Ink:** black `#1A1A1A`
- **Brand red:** `#E8351C`
- **Brand yellow:** `#FDDC33`
- **Accent muted grey** for body copy
- Feel: **editorial, confident, warm-neutral with jewel-tone punches**.

### F. Typography
- Display: ultra-bold old-style serif (think **Canela**, **Flecha**, or **Relative Faces Noe**). Extremely heavy black weight.
- Body: neutral sans.
- Nav: tracked uppercase sans.
- Line-height: tight on display (headlines sit at line-height ~0.95), loose on body.
- No italic accent; all serif.

### G. CTA sections
- Final "Let's Talk." section in cream with dark red capsule button `CONTACT US →`. Simple, confident.
- Rounded pill button, white text, small right-pointing chevron inside.

### H. Footer
- Background: pure black `#000`.
- Left: white heavy serif statement *"NOBL is the modern change and transformation partner."* + red pill `CONTACT US →`.
- Right: three columns of simple sans links (*About NOBL · Careers · Capabilities · Contact · Methodology · Today's Changemaker · Newsletter*).
- Bottom-left: circular LinkedIn icon.
- Typography: white serif statement + sans links in tracked uppercase labels.
- Very minimal, lots of breathing room.

### I. Animations / interactions
- Line-drawing animation on the circular pendulum illustration (SVG path-draw on scroll based on visible residue)
- Section colour-bands arrive as hard cuts (no parallax)
- Cookie banner as yellow sticky panel — treated as a design element, not an afterthought

### J. Overall feel
- **Adjectives:** editorial · confident · humanistic
- **Most memorable:** the ultra-heavy serif statement on cream + the jewel-red block that follows
- **Premium cue:** willingness to let a single sentence own an entire viewport, backed by photography-quality display type

---

# 3. ALIGN PILATES STUDIO — alignpilatesstudio.com.au

**Screenshots:** [hero](../design-research/screenshots/align-pilates-1-hero.png) · [nav-scrolled](../design-research/screenshots/align-pilates-2-nav-scrolled.png) · [full](../design-research/screenshots/align-pilates-3-full.png) · [footer](../design-research/screenshots/align-pilates-4-footer.png)

### A. Navigation bar
- Layout: small rounded-rectangle logo box top-left ("ALIGN" two-line wordmark), sparse nav right-aligned with thin serif labels (*Book · Classes · Our Team · Pricing · Contact · On Demand · Staff*).
- Background: transparent over the hero photograph, becomes solid white after scroll.
- Font: very thin/light serif for nav labels, tracked-out, uppercase-sentence-case mix.
- Mobile menu not visible at this breakpoint.

### B. Hero section
- Background: full-bleed warm interior photo of the studio (Reformer machine, woman walking, pendant light, plants).
- Headline: *"ALIGN PILATES STUDIO"* in **thin Didone-style serif, stacked on two lines, white**, centred-left.
- Font mixing: just the serif; nav matches.
- Sub-copy: none — the image + the white pill CTA carry it.
- CTA: white pill `BOOK IN` with fine serif black text, subtle shadow. High-contrast against warm photo.
- Decorative: nothing beyond the photography.

### C. Sections down the page
- **Section 2** alternating `THE GROUP CLASS EXPERIENCE` + `THE PERSONALISED EXPERIENCE` columns, each with cream background, small-caps tracked label, large serif heading, price, description.
- **Section 3** `Our Studio` with centred serif heading and body paragraph, cream.
- **Section 4** 2×3 photo grid of class types (Reformer Pilates, Clinical Pilates, Barre Pilates, Tripod & Chair, Tower & Chair, Private Sessions) — square warm-toned photos with serif captions underneath.
- **Section 5** testimonials carousel with reviewer cards.
- **Section 6** Mindbody-powered review list (5-star + name + date).
- Spacing: very generous vertical rhythm, alternating cream and pure white.

### D. Cards / components
- Square photography cards with serif titles below. No rounded corners; clean photo edges.
- Reviewer cards are flat text rows with star icons — no heavy containers.
- No drop shadows, no borders — relies on whitespace.

### E. Colour palette
- **Cream** `~#E8DFD1`
- **Off-white** `~#F6F0E7`
- **Warm grey / taupe** `~#A89F92` (footer)
- **Deep gold stars** for ratings
- **Black** body text
- Feel: **warm, neutral, calming, lifestyle-premium**.

### F. Typography
- Headings: thin Didone-serif (think **Didot** or **Playfair Display Light**)
- Labels: tracked-out small caps in condensed sans
- Body: very light-weight neutral sans
- Line-heights: generous (1.6+) on body, slightly tighter on display
- Letter-spacing: heavily tracked on labels (+200 units)

### G. CTA sections
- White pill `SIGN UP` in footer newsletter module
- `APPLY NOW` underlined link (not a button)
- `BOOK IN` white pill in hero
- All lean into minimal outlined or pill affordances

### H. Footer
- Background: warm grey `~#A89F92`
- 4 columns: `FOLLOW US · STAY CONNECTED · WORK WITH US · GET IN TOUCH`
- All column headings in **tracked-out white caps serif** with a thin underline
- Links: underlined white text
- Newsletter signup module with "Email Address" input + white-outline `SIGN UP` button
- Address, email, phone listed simply at right

### I. Animations / interactions
- Nav fades from transparent to white on scroll (inferred from hero-vs-scrolled screenshots)
- Photo cards likely fade-in on scroll
- No marquee; minimal motion

### J. Overall feel
- **Adjectives:** calm · warm · premium-lifestyle
- **Most memorable:** the alternating cream-and-white sections with small-caps eyebrow + large serif heading rhythm
- **Premium cue:** high-quality photography, restraint, generous whitespace, Didone serif

---

# 4. PILATES COLLECTIVE — pilatescollective.studio

**Screenshots:** [hero](../design-research/screenshots/pilates-collective-1-hero.png) · [nav-scrolled](../design-research/screenshots/pilates-collective-2-nav-scrolled.png) · [full](../design-research/screenshots/pilates-collective-3-full.png) · [footer](../design-research/screenshots/pilates-collective-4-footer.png)

### A. Navigation bar
- Layout: small bold uppercase `PILATES COLLECTIVE` wordmark top-left, centre-right sparse nav (*About · Class Schedule · Services · Pricing · Retreats · Blog*), dark pill `BOOK NOW` CTA far right.
- Background: transparent on hero (black-and-white photo) — looks white-text-on-photo.
- Font: condensed medium sans, uppercase for links.
- Mobile menu: not in viewport.

### B. Hero section
- Background: **full-bleed black-and-white photograph** of the studio with a person on a Reformer. Dramatic, cinematic.
- Headline: **"REFORMER PILATES FOR WHIDBEY ISLAND."** white condensed sans, all caps, bold. Left-aligned.
- Font mixing: none in hero. The headline is a single typeface.
- Sub-copy: *"A PREMIER BOUTIQUE STUDIO EXPERIENCE — NO FERRY REQUIRED."* — smaller caps, thinner weight, below headline.
- CTA: dark transparent outlined pill `EXPLORE NEW CLIENT DEALS →`.
- Decorative: a floating live-chat bubble ("Hi there, have a question?") — not part of the static design.
- Scrolling reveals a massive `GOOD. DO PILATES.` marquee in white bold condensed caps on black.

### C. Sections down the page
- **Section 2** cream-bg with 3 circular photo cards (classes) + short serif captions.
- **Section 3** black-and-white photo hero block `BOOK A PRIVATE OR SEMI-PRIVATE SESSION`.
- **Section 4** cream block with contact form for teacher training.
- **Section 5** cream "GET TO KNOW US" text block with the studio's philosophy.
- **Section 6** grey "FOLLOW US ON SOCIAL" block.
- **Section 7** black block with form (Name / Email / Message).
- **Section 8** cream footer with the circular P/C logo.

### D. Cards / components
- **Circular photo frames** for the three class cards — full circles, warm sepia-tone imagery.
- Rounded-rectangle form inputs (very rounded, almost pill).
- Pill buttons — large radius, neutral grey.

### E. Colour palette
- **Cream / sand** `~#E8D7C2`
- **Black** `#000`
- **White** `#FFF`
- **Cool grey** `~#B4B8BA` (one section)
- Feel: **earthy, cinematic, coastal-premium**.

### F. Typography
- Display: bold condensed sans for all CAPS headings (Barlow Condensed / Oswald style)
- Logo: italic didone serif `P C`
- Body: neutral sans (Work Sans / Inter)
- Very tight letter-spacing on the big caps headlines
- Mix: serif only on the logo; UI is sans

### G. CTA sections
- Pill buttons throughout, outlined or filled
- Centred Send button on black form section (`SEND` in light-grey pill)
- The `BOOK NOW` nav CTA is the hero call

### H. Footer
- Background: warm cream/sand `~#E8D7C2`
- Left: big circular **PC monogram logo** — two letters inside a yin-yang-style curved oval, with "PILATES COLLECTIVE" in a serif+sans mix beneath. Beautiful.
- Right: 3 columns `Explore · Follow us · Locations`, each with tiny semi-serif heading + underlined sans links.
- Floating chat bubble fixed right.
- Very minimal, confident.

### I. Animations / interactions
- Giant horizontal marquee text ("GOOD. DO PILATES.") visible as you scroll past the hero — likely auto-scrolls or parallaxes
- Chat widget is persistent
- No other heavy motion observed

### J. Overall feel
- **Adjectives:** earthy · cinematic · boutique-minimal
- **Most memorable:** the circular PC monogram and the B&W photography carrying the brand
- **Premium cue:** restraint + high-quality monochrome imagery + a genuinely beautiful logomark

---

# BEST-OF — and how to adapt for Carelabs

## Best hero section — **Nobl**
Nobl's hero wins because of its **confidence**: a single heavy-serif statement on cream, no image, no CTA. It makes the headline the product.

**Carelabs adaptation:** Full-viewport navy `#0B1A2F` hero. Giant **Barlow Condensed Extrabold uppercase** statement — *"ELECTRICAL SAFETY DEMANDS CERTAINTY."* — centred, ~8–10 rem at desktop. Below: one-line white/70 sub-copy in Poppins. One orange pill CTA `REQUEST A STUDY`. Subtle grid-dot texture overlay at 4% opacity (we already have this pattern in BR). No hero imagery — the words are the product. This matches Nobl's boldness while reading as engineering instead of consulting.

## Best navigation — **Nobl** (with bracket riff from Aleia)
Nobl's centred wordmark + clean tracked-caps nav is elegant. Aleia's bracketed labels `[About] [Work]` are memorable but probably too loud for a safety-engineering brand.

**Carelabs adaptation:** Keep the existing fixed navy navbar. Swap the current mixed serif+sans links for **tracked-out Barlow Condensed uppercase** labels at 0.15em letter-spacing, 13 px. Centred logo unchanged. Right-side CTA stays orange pill. Add a subtle 1-px rule under the nav on scroll (Nobl's thin under-line trick). No brackets.

## Best typography system — **Nobl**
Nobl's typography — one heavy display serif doing all the emotional work, against a neutral sans — is the cleanest system.

**Carelabs adaptation:** We already have the right three fonts loaded (Barlow Condensed, Playfair Display, Poppins). Use them as:
- **Hero + section headings:** Barlow Condensed 800 uppercase (our "display" role) — matches Pilates Collective's marquee and Aleia's aggression.
- **Accent word inside headings:** Playfair Display italic (our "accent" role) for the country name or key phrase — adds the Nobl editorial warmth.
- **Body / nav / labels:** Poppins 400 / 500. Tracked-out 500 for eyebrows.
Stick to 5 type roles maximum — avoid Aleia's "every paragraph is a different style" trap.

## Best colour palette approach — **Align Pilates**
Align's cream-alternating sections with photography doing the lifting is the calmest, most premium rhythm of the four. But warm cream clashes with safety-engineering authority.

**Carelabs adaptation:** Use **navy `#0B1A2F` and off-white `#F8FAFC` as alternating section backgrounds** the same way Align alternates cream and white. Keep orange `#F97316` for every CTA + eyebrow. One slate `#1E293B` section per page maximum (Align uses warm grey the same way). Photography where possible — industrial electrical panels shot in warm tungsten, not stock imagery.

## Best card / component design — **Align Pilates**
Align's photo-grid cards — square photograph, small-caps eyebrow, fine serif title, no border, no shadow — are the most premium. Pilates Collective's circular photo cards are tempting but too stylised for engineering.

**Carelabs adaptation:** For service cards on `/services/` and homepage, use:
- **16:10 photography top** (real photos of switchgear / labs / engineers at work)
- **Small-caps Barlow Condensed eyebrow** (e.g., `ARC FLASH · IEEE 1584`)
- **Barlow Condensed Bold uppercase title** (our existing style)
- **Poppins 400 body** below, 3-line max
- No borders. No shadows. Just whitespace and photography.
- Hover: image crop 5% zoom + eyebrow shifts to orange. No card lift.

## Best CTA section — **Nobl**
Nobl's "Let's Talk." cream section with one red pill button wins. No gradient, no split, no overlap. A single sentence plus a single button.

**Carelabs adaptation:** Replace the current gradient orange→navy CTA with a **single-colour navy CTA section**. Huge Barlow Condensed heading *"READY TO SCHEDULE A STUDY?"*, Playfair italic on the last word. One orange pill below. No sub-copy, no decorative elements. The contrast of a simple section against the alternating nav/off-white page IS the emphasis.

## Best footer — **Align Pilates**
Align's warm-grey footer with tracked caps column headings and underlined links is the most elegant. Pilates Collective's circular logo is beautiful but too specific.

**Carelabs adaptation:** Our current orange-on-navy-band footer is too loud. Switch to:
- Background: navy `#0B1A2F`
- 4 columns with **tracked-caps Barlow Condensed 14 px** headings (`NAVIGATE · SERVICES · CONTACT · LEGAL`), thin rule under each heading
- Links: **Poppins, underlined on hover**, no underline default — Align's exact treatment
- Newsletter signup module (optional), white-outline pill submit
- Big white `CARELABS` wordmark in the bottom band (our existing watermark pattern from the BR footer works here). Keep it.

## Best overall animation / motion — **Pilates Collective** (marquee) + **Nobl** (line-art draw)
Pilates Collective's giant `GOOD. DO PILATES.` marquee scrolling past the hero is cinematic. Nobl's animated line-art pendulum is warm and humanistic.

**Carelabs adaptation:** We already ship the announcement ticker — that's our Pilates Collective marquee equivalent (standards list cycling). For a Nobl-style moment, add **one animated SVG line-art electrical waveform / sine wave** that draws itself on scroll into the Manifesto section of the homepage. Single decorative element, thin orange stroke (1.5 px), draws in over 2 s. Nothing else needs motion.

---

# Synthesis — what the Carelabs NE site should feel like

- **Tone from Nobl:** big serious statements, confidence to let one sentence own a viewport, cream-or-navy colour bands, jewel-tone accent punch (orange)
- **Rhythm from Align:** alternating background sections, tracked caps eyebrow + serif accent + fine body, photography-first feature grids, elegant warm footer
- **Density from Pilates Collective:** cinematic B&W-ish photography, pill buttons, giant marquee word, circular decorative element as brand mark
- **Boldness from Aleia:** willingness to go huge on type, colour-block sections instead of timid gradients

**Avoid:**
- Aleia's chaos palette (hot pink + electric cyan + yellow) — wrong for electrical safety
- Pilates Collective's circular photos — too stylised for industrial B2B
- Nobl's jewel red as primary — too consumer; we use navy/orange instead

**Design moves to ship on NE rebuild:**
1. Hero: navy-only, condensed-caps headline + Playfair italic accent word + one orange pill (Nobl-confidence)
2. Services section: alternating navy/off-white bands, photography-led cards, no shadows (Align-rhythm)
3. Industries: full-width marquee of client sectors in huge condensed caps (Pilates Collective-marquee)
4. Manifesto: single orange-stroke SVG line animation on scroll (Nobl-humanism)
5. CTA: one navy block, one sentence, one orange pill (Nobl-restraint)
6. Footer: navy, 4-col tracked caps, underlined links, CARELABS watermark (Align-elegance)

---

*Screenshots captured 2026-04-25 via Playwright 1.47.0 + Chromium at 1440×900. Viewport/full-page/footer/scrolled-nav for each of 4 sites. All assets under [design-research/screenshots/](../design-research/screenshots/) for reference.*
