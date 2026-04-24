import { chromium } from "playwright";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { mkdirSync } from "node:fs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = join(__dirname, "..", "screenshots");
mkdirSync(OUT, { recursive: true });

const SITES = [
  { name: "aleia", url: "https://www.aleia.io" },
  { name: "nobl", url: "https://nobl.io" },
  { name: "align-pilates", url: "https://www.alignpilatesstudio.com.au" },
  { name: "pilates-collective", url: "https://pilatescollective.studio" },
];

async function shoot(site) {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " +
      "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
  });
  const page = await context.newPage();
  try {
    await page.goto(site.url, { waitUntil: "networkidle", timeout: 45000 });
  } catch (e) {
    try {
      await page.goto(site.url, { waitUntil: "domcontentloaded", timeout: 30000 });
    } catch (e2) {
      console.error(`  [ERR] ${site.name}: ${e2.message}`);
      await browser.close();
      return;
    }
  }
  // wait a moment for lazy content
  await page.waitForTimeout(2500);

  // hero / above-the-fold (1440×900)
  await page.screenshot({
    path: join(OUT, `${site.name}-1-hero.png`),
    fullPage: false,
  });
  console.log(`  [OK] ${site.name}-1-hero.png`);

  // scroll ~400px to capture any change in navbar on scroll
  await page.evaluate(() => window.scrollTo(0, 400));
  await page.waitForTimeout(600);
  await page.screenshot({
    path: join(OUT, `${site.name}-2-nav-scrolled.png`),
    fullPage: false,
  });
  console.log(`  [OK] ${site.name}-2-nav-scrolled.png`);

  // full-page
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(400);
  await page.screenshot({
    path: join(OUT, `${site.name}-3-full.png`),
    fullPage: true,
  });
  console.log(`  [OK] ${site.name}-3-full.png`);

  // footer-only: scroll to bottom
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(800);
  await page.screenshot({
    path: join(OUT, `${site.name}-4-footer.png`),
    fullPage: false,
  });
  console.log(`  [OK] ${site.name}-4-footer.png`);

  await browser.close();
}

(async () => {
  for (const site of SITES) {
    console.log(`\n=== ${site.name} (${site.url}) ===`);
    await shoot(site);
  }
  console.log("\nAll done.");
})();
