import { MetadataRoute } from "next";
import { getBlogPosts } from "@/lib/strapi-blog";
import { getServicesByRegion } from "@/lib/strapi";
import { getCaseStudies } from "@/lib/strapi-pages";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = "https://carelabz.com";

  const serviceSlugs = [
    "study-analysis/arc-flash-study",
    "study-analysis/short-circuit-analysis",
    "study-analysis/load-flow-analysis",
    "study-analysis/relay-coordination-study",
    "study-analysis/harmonic-study",
    "study-analysis/power-quality-analysis",
    "study-analysis/motor-start-analysis",
    "study-analysis/power-system-study",
    "inspection/electrical-safety-inspection",
  ];

  const caServiceSlugs = [
    "arc-flash-study",
    "short-circuit-analysis",
    "load-flow-analysis",
    "relay-coordination-study",
  ];

  const staticPages: MetadataRoute.Sitemap = [
    { url: `${baseUrl}/`, priority: 1.0, changeFrequency: "monthly" },
    { url: `${baseUrl}/us/`, priority: 1.0, changeFrequency: "weekly" },
    { url: `${baseUrl}/us/services/`, priority: 0.9, changeFrequency: "weekly" },
    { url: `${baseUrl}/us/about/`, priority: 0.7, changeFrequency: "monthly" },
    { url: `${baseUrl}/us/contact/`, priority: 0.8, changeFrequency: "monthly" },
    { url: `${baseUrl}/us/blog/`, priority: 0.8, changeFrequency: "daily" },
    { url: `${baseUrl}/us/case-studies/`, priority: 0.7, changeFrequency: "weekly" },
    { url: `${baseUrl}/ca/`, priority: 1.0, changeFrequency: "weekly" },
    { url: `${baseUrl}/ca/service/`, priority: 0.9, changeFrequency: "weekly" },
    { url: `${baseUrl}/ca/about-us/`, priority: 0.7, changeFrequency: "monthly" },
    { url: `${baseUrl}/ca/contact/`, priority: 0.8, changeFrequency: "monthly" },
    { url: `${baseUrl}/ca/blogs/`, priority: 0.8, changeFrequency: "daily" },
    { url: `${baseUrl}/ca/case-study/`, priority: 0.7, changeFrequency: "weekly" },
    { url: `${baseUrl}/mx/`, priority: 1.0, changeFrequency: "weekly" },
    { url: `${baseUrl}/mx/service/`, priority: 0.9, changeFrequency: "weekly" },
    { url: `${baseUrl}/mx/about-us/`, priority: 0.7, changeFrequency: "monthly" },
    { url: `${baseUrl}/mx/contact-us/`, priority: 0.8, changeFrequency: "monthly" },
    { url: `${baseUrl}/mx/blogs/`, priority: 0.8, changeFrequency: "daily" },
    { url: `${baseUrl}/mx/arc-flash-study/`, priority: 0.9, changeFrequency: "monthly" },
    { url: `${baseUrl}/mx/short-circuit-analysis/`, priority: 0.9, changeFrequency: "monthly" },
    { url: `${baseUrl}/mx/load-flow-analysis/`, priority: 0.9, changeFrequency: "monthly" },
    { url: `${baseUrl}/mx/relay-coordination-study/`, priority: 0.9, changeFrequency: "monthly" },
  ];

  // Helper: per-country static + service page entries (post-CA countries use shared pattern)
  const LATAM_EU_SERVICE_SLUGS = [
    "arc-flash-study",
    "harmonic-study-and-analysis",
    "motor-start-analysis",
    "power-system-study-and-analysis",
    "power-quality-analysis",
  ];

  const multiCountryStatic: MetadataRoute.Sitemap = [];
  const multiCountryServices: MetadataRoute.Sitemap = [];
  for (const { cc, servicesIdx } of [
    { cc: "br", servicesIdx: "services" },
    { cc: "co", servicesIdx: "services" },
    { cc: "cl", servicesIdx: "services" },
    { cc: "ar", servicesIdx: "services" },
    { cc: "pe", servicesIdx: "services" },
    { cc: "uk", servicesIdx: "our-services" },
  ]) {
    multiCountryStatic.push(
      { url: `${baseUrl}/${cc}/`, priority: 1.0, changeFrequency: "weekly" },
      { url: `${baseUrl}/${cc}/${servicesIdx}/`, priority: 0.9, changeFrequency: "weekly" },
      { url: `${baseUrl}/${cc}/about-us/`, priority: 0.7, changeFrequency: "monthly" },
      { url: `${baseUrl}/${cc}/contact-us/`, priority: 0.8, changeFrequency: "monthly" },
      { url: `${baseUrl}/${cc}/blogs/`, priority: 0.8, changeFrequency: "daily" },
    );
    for (const slug of LATAM_EU_SERVICE_SLUGS) {
      multiCountryServices.push({
        url: `${baseUrl}/${cc}/${slug}/`,
        lastModified: new Date(),
        priority: 0.9,
        changeFrequency: "monthly",
      });
    }
  }
  staticPages.push(...multiCountryStatic);

  const servicePages: MetadataRoute.Sitemap = serviceSlugs.map((slug) => ({
    url: `${baseUrl}/us/services/${slug}/`,
    lastModified: new Date(),
    priority: 0.9,
    changeFrequency: "monthly",
  }));

  const caServicePages: MetadataRoute.Sitemap = caServiceSlugs.map((slug) => ({
    url: `${baseUrl}/ca/services/${slug}/`,
    lastModified: new Date(),
    priority: 0.9,
    changeFrequency: "monthly",
  }));

  let blogPages: MetadataRoute.Sitemap = [];
  try {
    const posts = await getBlogPosts("us");
    blogPages = posts.map((post) => ({
      url: `${baseUrl}/us/blog/${post.slug}/`,
      lastModified: new Date(post.updatedAt || post.publishedAt),
      priority: 0.6,
      changeFrequency: "monthly" as const,
    }));
  } catch {
    // Strapi unavailable — skip blog posts in sitemap
  }

  let caBlogPages: MetadataRoute.Sitemap = [];
  try {
    const posts = await getBlogPosts("ca");
    caBlogPages = posts.map((post) => ({
      url: `${baseUrl}/ca/${post.slug}/`,
      lastModified: new Date(post.updatedAt || post.publishedAt),
      priority: 0.6,
      changeFrequency: "monthly" as const,
    }));
  } catch {
    // Strapi unavailable — skip CA blog posts in sitemap
  }

  // ── UAE (ae) ───────────────────────────────────────────────
  const aeStatic: MetadataRoute.Sitemap = [
    { url: `${baseUrl}/ae/`, priority: 1.0, changeFrequency: "weekly" },
    { url: `${baseUrl}/ae/services/`, priority: 0.9, changeFrequency: "weekly" },
    { url: `${baseUrl}/ae/about/`, priority: 0.7, changeFrequency: "monthly" },
    { url: `${baseUrl}/ae/contact/`, priority: 0.8, changeFrequency: "monthly" },
    { url: `${baseUrl}/ae/blog/`, priority: 0.8, changeFrequency: "daily" },
    { url: `${baseUrl}/ae/case-studies/`, priority: 0.7, changeFrequency: "weekly" },
  ];

  let aeServicePages: MetadataRoute.Sitemap = [];
  try {
    const svc = await getServicesByRegion("ae");
    aeServicePages = svc.map((s) => {
      const slug = s.slug.endsWith("-ae") ? s.slug.slice(0, -3) : s.slug;
      return {
        url: `${baseUrl}/ae/services/${slug}/`,
        lastModified: new Date(s.updatedAt || s.publishedAt),
        priority: 0.9,
        changeFrequency: "monthly" as const,
      };
    });
  } catch {
    // Strapi unavailable — skip AE service pages
  }

  let aeBlogPages: MetadataRoute.Sitemap = [];
  try {
    const posts = await getBlogPosts("ae");
    aeBlogPages = posts.map((p) => {
      const slug = p.slug.endsWith("-ae") ? p.slug.slice(0, -3) : p.slug;
      return {
        url: `${baseUrl}/ae/blog/${slug}/`,
        lastModified: new Date(p.updatedAt || p.publishedAt),
        priority: 0.6,
        changeFrequency: "monthly" as const,
      };
    });
  } catch {
    // Strapi unavailable — skip AE blog posts
  }

  let aeCaseStudyPages: MetadataRoute.Sitemap = [];
  try {
    const studies = await getCaseStudies("ae");
    aeCaseStudyPages = studies.map((s) => {
      const slug = s.slug.endsWith("-ae") ? s.slug.slice(0, -3) : s.slug;
      return {
        url: `${baseUrl}/ae/case-studies/${slug}/`,
        lastModified: new Date(s.updatedAt || s.publishedAt),
        priority: 0.7,
        changeFrequency: "monthly" as const,
      };
    });
  } catch {
    // Strapi unavailable — skip AE case studies
  }

  return [
    ...staticPages,
    ...servicePages,
    ...caServicePages,
    ...multiCountryServices,
    ...blogPages,
    ...caBlogPages,
    ...aeStatic,
    ...aeServicePages,
    ...aeBlogPages,
    ...aeCaseStudyPages,
  ];
}
