import { MetadataRoute } from "next";
import { getBlogPosts } from "@/lib/strapi-blog";

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

  const staticPages: MetadataRoute.Sitemap = [
    { url: `${baseUrl}/`, priority: 1.0, changeFrequency: "monthly" },
    { url: `${baseUrl}/us/`, priority: 1.0, changeFrequency: "weekly" },
    { url: `${baseUrl}/us/services/`, priority: 0.9, changeFrequency: "weekly" },
    { url: `${baseUrl}/us/about/`, priority: 0.7, changeFrequency: "monthly" },
    { url: `${baseUrl}/us/contact/`, priority: 0.8, changeFrequency: "monthly" },
    { url: `${baseUrl}/us/blog/`, priority: 0.8, changeFrequency: "daily" },
    { url: `${baseUrl}/us/case-studies/`, priority: 0.7, changeFrequency: "weekly" },
  ];

  const servicePages: MetadataRoute.Sitemap = serviceSlugs.map((slug) => ({
    url: `${baseUrl}/us/services/${slug}/`,
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

  return [...staticPages, ...servicePages, ...blogPages];
}
