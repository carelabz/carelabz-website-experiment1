/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: true,
  images: {
    dangerouslyAllowSVG: true,
    contentDispositionType: "attachment",
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
    remotePatterns: [
      {
        protocol: "https",
        hostname: "rational-cheese-8e8c4f80ea.strapiapp.com",
      },
      {
        protocol: "https",
        hostname: "**.strapiapp.com",
      },
      {
        protocol: "https",
        hostname: "images.unsplash.com",
      },
    ],
  },
  async redirects() {
    /** Helper: creates both trailing-slash and non-trailing-slash source variants */
    function pair(source, destination) {
      const clean = source.replace(/\/+$/, "");
      return [
        { source: clean, destination, permanent: true },
        { source: clean + "/", destination, permanent: true },
      ];
    }

    return [
      /* ============================================================ */
      /*  US — Core pages                                             */
      /* ============================================================ */
      ...pair("/us/about-us", "/us/about/"),
      ...pair("/us/contact-us", "/us/contact/"),
      ...pair("/us/case-study", "/us/case-studies/"),
      ...pair("/us/privacy-policy", "/privacy/"),
      ...pair("/us/terms-and-conditions", "/terms/"),
      ...pair("/company/privacy-policy", "/privacy/"),
      ...pair("/company/terms-and-conditions", "/terms/"),

      /* ============================================================ */
      /*  US — Service pages                                          */
      /* ============================================================ */
      ...pair("/us/service/arc-flash-study-in-usa", "/us/services/study-analysis/arc-flash-study/"),
      ...pair("/us/service/short-circuit-analysis", "/us/services/study-analysis/short-circuit-analysis/"),
      ...pair("/us/service/load-flow-analysis-us", "/us/services/study-analysis/load-flow-analysis/"),
      ...pair("/us/service/relay-coordination-study-in-usa", "/us/services/study-analysis/relay-coordination-study/"),
      ...pair("/us/harmonic-study-and-analysis-in-usa", "/us/services/study-analysis/harmonic-study/"),
      ...pair("/us/power-quality-analysis-in-usa", "/us/services/study-analysis/power-quality-analysis/"),
      ...pair("/us/motor-start-analysis-in-usa", "/us/services/study-analysis/motor-start-analysis/"),
      ...pair("/us/power-system-study-and-analysis-in-usa", "/us/services/study-analysis/power-system-study/"),
      ...pair("/us/electrical-safety-inspection-in-usa", "/us/services/inspection/electrical-safety-inspection/"),

      /* ============================================================ */
      /*  US — Blog posts                                             */
      /* ============================================================ */
      ...pair("/us/step-by-step-guide-to-perform-arc-flash-analysis-in-the-us", "/us/blog/step-by-step-guide-to-perform-arc-flash-analysis-in-the-us/"),
      ...pair("/us/working-principles-of-power-quality-analysis-in-the-us", "/us/blog/working-principles-of-power-quality-analysis-in-the-us/"),
      ...pair("/us/harmonic-analysis-in-power-system-in-the-us", "/us/blog/harmonic-analysis-in-power-system-in-the-us/"),
      ...pair("/us/arc-flash-at-turkey-point-2017", "/us/blog/arc-flash-at-turkey-point-2017/"),
      ...pair("/us/priest-rapids-dam-arc-flash-explosion-2014", "/us/blog/priest-rapids-dam-arc-flash-explosion-2014/"),
      ...pair("/us/checklist-for-electrical-safety-audit-in-the-usa", "/us/blog/checklist-for-electrical-safety-audit-in-the-usa/"),
      ...pair("/us/mgm-grand-hotel-fire-1980", "/us/blog/mgm-grand-hotel-fire-1980/"),
      ...pair("/us/test-and-verify-efficiency-of-electrical-motor-as-per-national-international-standards", "/us/blog/test-and-verify-efficiency-of-electrical-motor/"),
      ...pair("/us/resolving-safety-issues-with-arc-flash-and-lockout-tagout-services-at-a-leading-medical-company", "/us/blog/resolving-safety-issues-arc-flash-lockout-tagout/"),
      ...pair("/us/which-of-these-facts-about-arc-flashes-are-true", "/us/blog/which-of-these-facts-about-arc-flashes-are-true/"),
      ...pair("/us/the-importance-of-relay-coordination-in-power-system", "/us/blog/the-importance-of-relay-coordination-in-power-system/"),
      ...pair("/us/upgrading-your-power-system-dont-ignore-the-short-circuit-analysis", "/us/blog/upgrading-your-power-system-short-circuit-analysis/"),
      ...pair("/us/what-are-the-key-insights-obtained-from-load-flow-analysis", "/us/blog/key-insights-from-load-flow-analysis/"),
      ...pair("/us/improving-reliability-through-electrical-safety-audit-at-a-retail-company", "/us/blog/improving-reliability-electrical-safety-audit-retail/"),
      ...pair("/us/commercial-electrical-safety-inspection-checklist-for-the-united-states", "/us/blog/commercial-electrical-safety-inspection-checklist-usa/"),
      ...pair("/us/prioritizing-a-safe-work-environment-at-a-multinational-technology-company", "/us/blog/safe-work-environment-multinational-technology-company/"),
      ...pair("/us/energy-conservation-by-auditing-power-quality", "/us/blog/energy-conservation-by-auditing-power-quality/"),
      ...pair("/us/three-mile-island-blast-1979", "/us/blog/three-mile-island-blast-1979/"),
      ...pair("/us/how-to-do-an-electrical-switchgear-risk-assessment-in-usa", "/us/blog/electrical-switchgear-risk-assessment-usa/"),
      ...pair("/us/arc-flash-study-a-grandeur-or-mandate", "/us/blog/arc-flash-study-a-grandeur-or-mandate/"),
      ...pair("/us/electrical-condition-installation-report-by-third-party-company-in-the-usa", "/us/blog/electrical-condition-installation-report-usa/"),
      ...pair("/us/why-is-harmonic-study-and-analysis-important-for-companies-in-the-united-states", "/us/blog/why-harmonic-study-analysis-important-usa/"),
      ...pair("/us/need-or-necessity-electrical-switchgear-risk-assessment-in-the-usa", "/us/blog/need-electrical-switchgear-risk-assessment-usa/"),
      ...pair("/us/importance-of-electrical-safety-inspection-in-usa", "/us/blog/upgrading-your-power-system-short-circuit-analysis/"),
      ...pair("/us/blog/importance-of-electrical-safety-inspection-usa", "/us/blog/upgrading-your-power-system-short-circuit-analysis/"),
      ...pair("/us/importance-of-electrical-safety-audit-for-companies-in-the-usa", "/us/blog/importance-of-electrical-safety-audit-usa/"),
      ...pair("/us/importance-of-electrical-installation-condition-report-ecir-in-the-us", "/us/blog/importance-electrical-installation-condition-report-ecir/"),
      ...pair("/us/importance-of-arc-flash-hazard-analysis-and-mitigation-in-the-united-states", "/us/blog/which-of-these-facts-about-arc-flashes-are-true/"),
      ...pair("/us/blog/importance-arc-flash-hazard-analysis-mitigation-usa", "/us/blog/which-of-these-facts-about-arc-flashes-are-true/"),
      ...pair("/us/how-to-perform-power-system-study-and-analysis-for-load-flow-short-circuit-and-relay-coordination-for-a-company-in-the-us", "/us/blog/power-system-study-load-flow-short-circuit-relay-coordination/"),
      ...pair("/us/how-to-audit-electric-motor-efficiency-and-reliability-for-commercial-use", "/us/blog/audit-electric-motor-efficiency-reliability/"),
      ...pair("/us/guide-to-perform-power-quality-analysis-in-the-united-states", "/us/blog/guide-power-quality-analysis-united-states/"),

      /* ============================================================ */
      /*  CA — Legacy WP cruft + typo redirects                       */
      /* ============================================================ */
      ...pair("/ca/services-arch-flash-analysis", "/ca/services/arc-flash-study/"),
      ...pair("/ca/services-old", "/ca/service/"),
      ...pair("/ca/home", "/ca/"),

      /* ============================================================ */
      /*  LATAM + UK — WP junk/legacy redirects                        */
      /* ============================================================ */
      ...pair("/mx/404-page", "/mx/"),
      ...pair("/mx/home", "/mx/"),
      ...pair("/mx/services-old", "/mx/service/"),
      ...pair("/br/404-page", "/br/"),
      ...pair("/co/404-page", "/co/"),
      ...pair("/cl/404-page", "/cl/"),
      ...pair("/ar/404-page", "/ar/"),
      ...pair("/pe/404-page", "/pe/"),
      ...pair("/uk/home-demo", "/uk/"),
      ...pair("/uk/ss", "/uk/"),
      ...pair("/uk/404-page", "/uk/"),
      // UK services index is at /our-services/, not /services/
      ...pair("/uk/services", "/uk/our-services/"),
      ...pair("/uk/service", "/uk/our-services/"),

      /* ============================================================ */
      /*  NZ — WP legacy 'carelabz-com-nz-*' slugs cleaned up          */
      /*  Old WP URL preserved via 301 to new clean URL                */
      /* ============================================================ */
      ...pair(
        "/nz/carelabz-com-nz-arc-flash-study-and-analysis-in-new-zealand",
        "/nz/arc-flash-study-in-new-zealand/"
      ),
      ...pair(
        "/nz/carelabz-com-nz-harmonic-study-and-analysis-in-new-zealand",
        "/nz/harmonic-study-in-new-zealand/"
      ),
      ...pair(
        "/nz/carelabz-com-nz-power-system-study-and-analysis-in-new-zealand",
        "/nz/power-system-study-in-new-zealand/"
      ),
      ...pair(
        "/nz/carelabz-com-nz-power-quality-analysis-in-new-zealand",
        "/nz/power-quality-analysis-in-new-zealand/"
      ),

      /* ============================================================ */
      /*  DE — nested-service country not in the flat batch.          */
      /*  WP serves /de/blog/ (we use /de/blogs/), /de/case-study/    */
      /*  (we don't have one), /de/service/:slug/ (we use /services/).*/
      /* ============================================================ */
      ...pair("/de/blog", "/de/blogs/"),
      ...pair("/de/case-study", "/de/"),
      { source: "/de/service/:slug", destination: "/de/services/:slug/", permanent: true },
      { source: "/de/service/:slug/", destination: "/de/services/:slug/", permanent: true },

      /* ============================================================ */
      /*  MY + VN — WP uses "-in-malaysia" / "-in-vietnam" suffix AND */
      /*  swaps "arc-flash-analysis" where our slug is "arc-flash-    */
      /*  study". Must come BEFORE the generic /xx/service/:slug/     */
      /*  rule so specific mappings win.                               */
      /* ============================================================ */
      ...pair("/my/arc-flash-study-in-malaysia", "/my/arc-flash-study/"),
      ...pair("/my/service/arc-flash-analysis-in-malaysia", "/my/arc-flash-study/"),
      ...pair("/my/service/short-circuit-analysis-in-malaysia", "/my/short-circuit-analysis/"),
      ...pair("/my/service/load-flow-analysis-in-malaysia", "/my/load-flow-analysis/"),
      ...pair("/my/service/relay-coordination-study-in-malaysia", "/my/relay-coordination-study/"),
      ...pair("/vn/arc-flash-study-in-vietnam", "/vn/arc-flash-study/"),
      ...pair("/vn/service/arc-flash-analysis-in-vietnam", "/vn/arc-flash-study/"),
      ...pair("/vn/service/short-circuit-analysis-in-vietnam", "/vn/short-circuit-analysis/"),
      ...pair("/vn/service/load-flow-analysis-in-vietnam", "/vn/load-flow-analysis/"),
      ...pair("/vn/service/relay-coordination-study-in-vietnam", "/vn/relay-coordination-study/"),

      /* ============================================================ */
      /*  Flat-service countries — WP serves duplicate URLs at         */
      /*  /xx/services/slug/ and /xx/services/ that don't map to our  */
      /*  flat routes. Redirect them to the canonical flat location.  */
      /* ============================================================ */
      // Note: se/no/dk/fi/uk/ie removed from the generic /xx/case-study → /xx/
      // redirect below because they now have real /case-studies/ placeholder
      // pages. Those 4 country-specific case-study redirects are handled
      // separately below the main list.
      ...[
        "at", "be", "ch", "nl", "au",
        "es", "pt", "gr", "fr", "ru", "pl", "hu", "cz", "ro", "sk", "ua",
        "cn", "jp", "kr", "hk", "tw", "my", "sg", "th", "vn", "id", "ph",
        "nz", "sa", "tr", "za", "eg", "it",
      ].flatMap((cc) => [
        // /xx/services/ → /xx/our-services/ (for countries using our-services)
        ...pair(`/${cc}/services`, `/${cc}/our-services/`),
        // /xx/services/SLUG/ → /xx/SLUG/ (flat redirect)
        { source: `/${cc}/services/:slug`, destination: `/${cc}/:slug/`, permanent: true },
        { source: `/${cc}/services/:slug/`, destination: `/${cc}/:slug/`, permanent: true },
        // Some WP installs use singular /service/ — same flat target
        { source: `/${cc}/service/:slug`, destination: `/${cc}/:slug/`, permanent: true },
        { source: `/${cc}/service/:slug/`, destination: `/${cc}/:slug/`, permanent: true },
        // /xx/case-study/ → /xx/ (countries without case-study page)
        ...pair(`/${cc}/case-study`, `/${cc}/`),
        // /xx/home-2/ → /xx/ (WP junk homepage duplicates)
        ...pair(`/${cc}/home-2`, `/${cc}/`),
      ]),

      /* ============================================================ */
      /*  Blog-index slug variants across countries                    */
      /* ============================================================ */
      // MY, VN, TH, SG, ID, PH use /our-blogs/ on WP but our index is /blogs/
      ...["my", "vn", "th", "sg", "id", "ph"].flatMap((cc) => pair(`/${cc}/our-blogs`, `/${cc}/blogs/`)),
      // NZ uses /blog/ singular on WP but our index is /blogs/
      ...pair("/nz/blog", "/nz/blogs/"),

      // BR/CO/CL/AR/PE use /services/ plural as their real index, not redirect
      // (handled separately — not in the list above).
      // IN uses /our-services/ and /our-blogs/ — blog index already correct.

      /* ============================================================ */
      /*  NE case-study → case-studies (UK/IE/SE/NO/DK/FI now have    */
      /*  real placeholder pages, so /case-study/ redirects to those) */
      /* ============================================================ */
      ...["uk", "ie", "se", "no", "dk", "fi"].flatMap((cc) => [
        ...pair(`/${cc}/case-study`, `/${cc}/case-studies/`),
      ]),

      /* ============================================================ */
      /*  UAE — root-level legacy WP URLs -> /ae/...                  */
      /*  Live WP serves these at carelabz.com root; new site nests   */
      /*  everything under /ae/. These 301s preserve all backlinks +  */
      /*  Search Console rankings on cutover.                         */
      /* ============================================================ */
      ...pair("/about-carelabs", "/ae/about/"),
      ...pair("/contact-us", "/ae/contact/"),

      // 77 legacy service URLs -> /ae/services/
      ...pair("/arc-flash-study", "/ae/services/arc-flash-study/"),
      ...pair("/arc-flash-study-analysis", "/ae/services/arc-flash-study-analysis/"),
      ...pair("/automatic-transfer-switch-testing-service", "/ae/services/automatic-transfer-switch-testing-service/"),
      ...pair("/bain-marie-calibration", "/ae/services/bain-marie-calibration/"),
      ...pair("/battery-testing-services-dubai-uae", "/ae/services/battery-testing-services-dubai-uae/"),
      ...pair("/biomedical-equipment-safety-inspection-services", "/ae/services/biomedical-equipment-safety-inspection-services/"),
      ...pair("/biomedical-equipment-safety-testing-services", "/ae/services/biomedical-equipment-safety-testing-services/"),
      ...pair("/blast-chiller-calibration", "/ae/services/blast-chiller-calibration/"),
      ...pair("/blast-freezer-calibration", "/ae/services/blast-freezer-calibration/"),
      ...pair("/building-envelope-infrared-thermography-inspection-service", "/ae/services/building-envelope-infrared-thermography-inspection-service/"),
      ...pair("/cable-testing", "/ae/services/cable-testing/"),
      ...pair("/calibrator-calibration", "/ae/services/calibrator-calibration/"),
      ...pair("/capacitor-bank-test", "/ae/services/capacitor-bank-test/"),
      ...pair("/chiller-calibration", "/ae/services/chiller-calibration/"),
      ...pair("/circuit-breaker-testing", "/ae/services/circuit-breaker-testing/"),
      ...pair("/commercial-electrical-inspection-services-dubai-uae", "/ae/services/commercial-electrical-inspection-services-dubai-uae/"),
      ...pair("/commercial-electrical-testing", "/ae/services/commercial-electrical-testing/"),
      ...pair("/contact-resistance-testing-service", "/ae/services/contact-resistance-testing-service/"),
      ...pair("/continuity-testing", "/ae/services/continuity-testing/"),
      ...pair("/digital-thermometer-calibration", "/ae/services/digital-thermometer-calibration/"),
      ...pair("/earth-fault-loop-impedence-test", "/ae/services/earth-fault-loop-impedence-test/"),
      ...pair("/earth-ground-testing-service", "/ae/services/earth-ground-testing-service/"),
      ...pair("/electric-motor-testing", "/ae/services/electric-motor-testing/"),
      ...pair("/electric-switchgear-testing-services", "/ae/services/electric-switchgear-testing-services/"),
      ...pair("/electrical-calibration", "/ae/services/electrical-calibration/"),
      ...pair("/electrical-compliance-inspection", "/ae/services/electrical-compliance-inspection/"),
      ...pair("/electrical-installations-certification-service", "/ae/services/electrical-installations-certification-service/"),
      ...pair("/electrical-safety-audit-service", "/ae/services/electrical-safety-audit-service/"),
      ...pair("/electrical-safety-auditing-inspection-service", "/ae/services/electrical-safety-auditing-inspection-service/"),
      ...pair("/electrical-safety-testing", "/ae/services/electrical-safety-testing/"),
      ...pair("/electrical-switchgear-risk-assessment-study-hazard-analysis-service", "/ae/services/electrical-switchgear-risk-assessment-study-hazard-analysis-service/"),
      ...pair("/electrical-switchgear-safety-inspection-services", "/ae/services/electrical-switchgear-safety-inspection-services/"),
      ...pair("/electrical-thermography-inspection", "/ae/services/electrical-thermography-inspection/"),
      ...pair("/energy-auditing-service", "/ae/services/energy-auditing-service/"),
      ...pair("/factory-acceptance-testing-services", "/ae/services/factory-acceptance-testing-services/"),
      ...pair("/fixed-electrical-testing", "/ae/services/fixed-electrical-testing/"),
      ...pair("/fixed-wire-testing", "/ae/services/fixed-wire-testing/"),
      ...pair("/frequency-stability-analysis", "/ae/services/frequency-stability-analysis/"),
      ...pair("/generator-load-bank-testing", "/ae/services/generator-load-bank-testing/"),
      ...pair("/gfci-standard-inspection-service", "/ae/services/gfci-standard-inspection-service/"),
      ...pair("/ground-fault-testing", "/ae/services/ground-fault-testing/"),
      ...pair("/grounding-grid-study-analysis", "/ae/services/grounding-grid-study-analysis/"),
      ...pair("/grounding-system-design-and-planning", "/ae/services/grounding-system-design-and-planning/"),
      ...pair("/harmonic-study-analysis", "/ae/services/harmonic-study-analysis/"),
      ...pair("/insulation-resistance-test-service", "/ae/services/insulation-resistance-test-service/"),
      ...pair("/leakage-current-measurement", "/ae/services/leakage-current-measurement/"),
      ...pair("/lightning-arrester-testing", "/ae/services/lightning-arrester-testing/"),
      ...pair("/lightning-arrester-testing-service", "/ae/services/lightning-arrester-testing-service/"),
      ...pair("/live-testing", "/ae/services/live-testing/"),
      ...pair("/load-flow-analysis", "/ae/services/load-flow-analysis/"),
      ...pair("/mcc-panel-operation-testing", "/ae/services/mcc-panel-operation-testing/"),
      ...pair("/megger-test", "/ae/services/megger-test/"),
      ...pair("/motor-acceleration-study-analysis", "/ae/services/motor-acceleration-study-analysis/"),
      ...pair("/pfc-psc-test", "/ae/services/pfc-psc-test/"),
      ...pair("/polarity-test-service", "/ae/services/polarity-test-service/"),
      ...pair("/portable-appliance-testing-dubai-uae", "/ae/services/portable-appliance-testing-dubai-uae/"),
      ...pair("/power-quality-study-analysis", "/ae/services/power-quality-study-analysis/"),
      ...pair("/power-restoration-optimization", "/ae/services/power-restoration-optimization/"),
      ...pair("/power-system-study-analysis", "/ae/services/power-system-study-analysis/"),
      ...pair("/primary-current-injection-test", "/ae/services/primary-current-injection-test/"),
      ...pair("/prospective-short-circuit-test-prospective-fault-current-test", "/ae/services/prospective-short-circuit-test-prospective-fault-current-test/"),
      ...pair("/protection-relay-testing-services", "/ae/services/protection-relay-testing-services/"),
      ...pair("/protective-devices-testing-services", "/ae/services/protective-devices-testing-services/"),
      ...pair("/relay-coordination-study-and-analysis", "/ae/services/relay-coordination-study-and-analysis/"),
      ...pair("/residual-current-device-testing-safety", "/ae/services/residual-current-device-testing-safety/"),
      ...pair("/residual-current-device-testing-safety-2", "/ae/services/residual-current-device-testing-safety-2/"),
      ...pair("/secondary-current-injection-test", "/ae/services/secondary-current-injection-test/"),
      ...pair("/short-circuit-study-analysis", "/ae/services/short-circuit-study-analysis/"),
      ...pair("/soil-resistivity-test", "/ae/services/soil-resistivity-test/"),
      ...pair("/third-party-electrical-certification", "/ae/services/third-party-electrical-certification/"),
      ...pair("/third-party-electrical-inspection-company-uae", "/ae/services/third-party-electrical-inspection-company-uae/"),
      ...pair("/third-party-inspection-electrical-installation", "/ae/services/third-party-inspection-electrical-installation/"),
      ...pair("/torque-test", "/ae/services/torque-test/"),
      ...pair("/unbalanced-load-flow-study-analysis", "/ae/services/unbalanced-load-flow-study-analysis/"),
      ...pair("/vibration-study-and-analysis", "/ae/services/vibration-study-and-analysis/"),
      ...pair("/voltage-drop-study-analysis", "/ae/services/voltage-drop-study-analysis/"),
      ...pair("/voltage-imbalance-study", "/ae/services/voltage-imbalance-study/"),

      // 38 legacy blog URLs -> /ae/blog/
      ...pair("/about-earth-fault-loop-impedence-test", "/ae/blog/about-earth-fault-loop-impedence-test/"),
      ...pair("/electrical-infrared-thermography-inspection-important", "/ae/blog/electrical-infrared-thermography-inspection-important/"),
      ...pair("/electrical-installation-inspection-fulfilling-trakhees-guidelines-to-procure-operation-fitness-certificate-ofc", "/ae/blog/electrical-installation-inspection-fulfilling-trakhees-guidelines-to-procure-operation-fitness-certificate-ofc/"),
      ...pair("/how-what-why-generator-load-bank-testing-done", "/ae/blog/how-what-why-generator-load-bank-testing-done/"),
      ...pair("/learn-about-residual-current-device-testing-safety", "/ae/blog/learn-about-residual-current-device-testing-safety/"),
      ...pair("/learn-continuity-testing-what-how", "/ae/blog/learn-continuity-testing-what-how/"),
      ...pair("/learn-how-insulation-resistance-test-done", "/ae/blog/learn-how-insulation-resistance-test-done/"),
      ...pair("/learn-what-is-earth-ground-test-why-and-how-is-it-done", "/ae/blog/learn-what-is-earth-ground-test-why-and-how-is-it-done/"),
      ...pair("/megger-test-performed", "/ae/blog/megger-test-performed/"),
      ...pair("/need-conduct-electrical-safety-testing", "/ae/blog/need-conduct-electrical-safety-testing/"),
      ...pair("/protecting-electrical-systems", "/ae/blog/protecting-electrical-systems/"),
      ...pair("/purpose-lightning-arrester-testing-necessary", "/ae/blog/purpose-lightning-arrester-testing-necessary/"),
      ...pair("/thermography-test-of-electrical-panels", "/ae/blog/thermography-test-of-electrical-panels/"),
      ...pair("/thermography-testing-of-electrical-equipment", "/ae/blog/thermography-testing-of-electrical-equipment/"),
      ...pair("/what-automatic-transfer-switch-testing-how-automatic-transfer-switch-testing-done", "/ae/blog/what-automatic-transfer-switch-testing-how-automatic-transfer-switch-testing-done/"),
      ...pair("/what-cable-testing-how-cable-testing-done", "/ae/blog/what-cable-testing-how-cable-testing-done/"),
      ...pair("/what-capacitor-bank-testing-why-capacitor-bank-testing-done", "/ae/blog/what-capacitor-bank-testing-why-capacitor-bank-testing-done/"),
      ...pair("/what-circuit-breaker-testing-how-circuit-breaker-testing-done", "/ae/blog/what-circuit-breaker-testing-how-circuit-breaker-testing-done/"),
      ...pair("/what-contact-resistance-test-why-contact-resistance-testing-done", "/ae/blog/what-contact-resistance-test-why-contact-resistance-testing-done/"),
      ...pair("/what-earth-grounding", "/ae/blog/what-earth-grounding/"),
      ...pair("/what-factory-acceptance-testing-how-fat-done", "/ae/blog/what-factory-acceptance-testing-how-fat-done/"),
      ...pair("/what-ground-fault-testing-why-ground-fault-testing-important", "/ae/blog/what-ground-fault-testing-why-ground-fault-testing-important/"),
      ...pair("/what-how-grounding-design-planning", "/ae/blog/what-how-grounding-design-planning/"),
      ...pair("/what-how-harmonic-study-analysis-done", "/ae/blog/what-how-harmonic-study-analysis-done/"),
      ...pair("/what-is-electric-motor-testing-and-why-is-it-done", "/ae/blog/what-is-electric-motor-testing-and-why-is-it-done/"),
      ...pair("/what-is-soil-resistivity-test-how-is-soil-resistivity-testing-done", "/ae/blog/what-is-soil-resistivity-test-how-is-soil-resistivity-testing-done/"),
      ...pair("/what-is-torque-testing-how-is-torque-testing-done", "/ae/blog/what-is-torque-testing-how-is-torque-testing-done/"),
      ...pair("/what-leakage-current-testing-measuring-how-leakage-current-testing-measuring-done", "/ae/blog/what-leakage-current-testing-measuring-how-leakage-current-testing-measuring-done/"),
      ...pair("/what-motor-acceleration-study-analysis", "/ae/blog/what-motor-acceleration-study-analysis/"),
      ...pair("/what-pat-test-why-pat-test-done", "/ae/blog/what-pat-test-why-pat-test-done/"),
      ...pair("/what-polarity-test-why-conduct-polarity-test", "/ae/blog/what-polarity-test-why-conduct-polarity-test/"),
      ...pair("/what-protective-device-testing-how-done", "/ae/blog/what-protective-device-testing-how-done/"),
      ...pair("/what-short-circuit-analysis-done-why", "/ae/blog/what-short-circuit-analysis-done-why/"),
      ...pair("/what-voltage-drop-study-analysis", "/ae/blog/what-voltage-drop-study-analysis/"),
      ...pair("/what-why-load-flow-analysis-power-flow-analysis-done", "/ae/blog/what-why-load-flow-analysis-power-flow-analysis-done/"),
      ...pair("/what-you-need-to-know-about-arc-flash", "/ae/blog/what-you-need-to-know-about-arc-flash/"),
      ...pair("/what-you-need-to-know-about-arc-flash-hazard-study-and-analysis", "/ae/blog/what-you-need-to-know-about-arc-flash-hazard-study-and-analysis/"),
      ...pair("/why-how-what-automatic-transfer-switch-testing-done", "/ae/blog/why-how-what-automatic-transfer-switch-testing-done/"),

      // 8 Search Console top-traffic alias slugs (WP slug != Strapi slug)
      ...pair("/polarity-test", "/ae/services/polarity-test-service/"),
      ...pair("/insulation-resistance-test", "/ae/services/insulation-resistance-test-service/"),
      ...pair("/arc-flash-analysis", "/ae/services/arc-flash-study-analysis/"),
      ...pair("/motor-testing-services", "/ae/services/electric-motor-testing/"),
      ...pair("/short-circuit-analysis-study", "/ae/services/short-circuit-study-analysis/"),
      ...pair("/cable-testing-services", "/ae/services/cable-testing/"),
      ...pair("/breaker-testing-services", "/ae/services/circuit-breaker-testing/"),
      ...pair("/power-system-protection-coordination-study", "/ae/services/relay-coordination-study-and-analysis/"),
    ];
  },
};

export default nextConfig;
