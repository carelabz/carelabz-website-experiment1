import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowRight, BookOpen } from "lucide-react";
import { SAAnnouncementTicker } from "@/components/sa-announcement-ticker";
import { SANavbar } from "@/components/sa-navbar";
import { SAFooter } from "@/components/sa-footer";
import { COUNTRY_CONFIGS } from "@/lib/countries-config";
import { getBlogPosts, type BlogPost } from "@/lib/strapi-blog";
import {
  buildJsonLd,
  getRegionOrganizationSchema,
  getWebPageSchema,
  getBreadcrumbSchema,
} from "@/lib/jsonld";

export const dynamic = "force-dynamic";

const CC = "ar";
const COUNTRY_NAME = "Argentina";
const HREFLANG = "en-AR";
const config = COUNTRY_CONFIGS[CC];

export const metadata: Metadata = {
  title: `Electrical Safety Blog: Power System Studies & Analysis | Carelabs ${COUNTRY_NAME}`,
  description: `Expert insights on electrical safety, power system studies, arc flash analysis, and ${config.primaryStandard} compliance for ${COUNTRY_NAME} facilities. Stay informed with Carelabs.`,
  alternates: {
    canonical: `https://carelabz.com/${CC}/blogs/`,
    languages: {
      [HREFLANG]: `https://carelabz.com/${CC}/blogs/`,
      "x-default": `https://carelabz.com/${CC}/blogs/`,
    },
  },
  openGraph: {
    title: `Electrical Safety Blog & Industry Insights | Carelabs ${COUNTRY_NAME}`,
    description: `Expert insights on arc flash analysis, power system engineering, and electrical safety compliance in ${COUNTRY_NAME}.`,
    url: `https://carelabz.com/${CC}/blogs/`,
    siteName: "Carelabs",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: `Electrical Safety Blog & Industry Insights | Carelabs ${COUNTRY_NAME}`,
    description: `Expert insights on arc flash analysis, power system engineering, and electrical safety compliance in ${COUNTRY_NAME}.`,
  },
};

function postDate(post: BlogPost): string {
  return post.publishedDate ?? post.publishedAt;
}

function formatDate(v: string | null): string {
  if (!v) return "";
  try {
    return new Date(v).toLocaleDateString("en-US", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  } catch {
    return "";
  }
}

function slugPath(post: BlogPost): string {
  const slug = post.slug.endsWith(`-${CC}`) ? post.slug.slice(0, -3) : post.slug;
  return `/${CC}/${slug}/`;
}

export default async function ARBlogIndexPage() {
  const allPosts = await getBlogPosts(CC);
  const sorted = [...allPosts].sort(
    (a, b) => new Date(postDate(b)).getTime() - new Date(postDate(a)).getTime()
  );
  const featured = sorted.slice(0, 3);
  const older = sorted.slice(3);
  const featuredPost = featured[0];
  const sideFeatured = featured.slice(1, 3);

  const jsonLd = buildJsonLd([
    getRegionOrganizationSchema({
      cc: CC,
      countryName: COUNTRY_NAME,
      countryIso2: CC.toUpperCase(),
      phone: config.phone,
      email: config.email,
      addressLocality: config.address,
    }),
    getWebPageSchema(
      `https://carelabz.com/${CC}/blogs/`,
      `Electrical Safety Blog & Industry Insights | Carelabs ${COUNTRY_NAME}`,
      `Expert insights on arc flash analysis, power system engineering, and electrical safety compliance in ${COUNTRY_NAME}.`,
      HREFLANG
    ),
    getBreadcrumbSchema([
      { name: "Home", url: `https://carelabz.com/${CC}/` },
      { name: "Blog", url: `https://carelabz.com/${CC}/blogs/` },
    ]),
  ]);

  return (
    <main className="bg-white font-sans">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <SAAnnouncementTicker
        countryName={COUNTRY_NAME}
        standards={config.standards}
      />
      <SANavbar config={config} />

      {/* HERO */}
      <section
        className="relative overflow-hidden py-24 lg:py-28"
        style={{
          background: "linear-gradient(135deg, #094d76 0%, #2575B6 100%)",
        }}
      >
        <div
          className="absolute inset-0 opacity-[0.08] pointer-events-none"
          style={{
            backgroundImage:
              "radial-gradient(circle at 2px 2px, white 1px, transparent 0)",
            backgroundSize: "32px 32px",
          }}
          aria-hidden="true"
        />
        <div className="relative max-w-[1400px] mx-auto px-6 lg:px-12 text-center">
          <span className="text-[#F15C30] text-sm uppercase tracking-widest font-semibold font-serif">
            Power Systems Knowledge Hub
          </span>
          <h1 className="mt-6 mx-auto max-w-3xl font-serif font-black text-5xl sm:text-6xl lg:text-7xl text-white tracking-tight leading-[1.05]">
            Power up your Knowledge
          </h1>
          <p className="mx-auto mt-8 max-w-2xl text-lg text-white/75 leading-relaxed font-sans">
            Stay ahead of {config.primaryStandard}, IEEE 1584, and international
            compliance requirements. Expert knowledge from the Carelabs
            engineering team.
          </p>
        </div>
      </section>

      {/* FEATURED + SIDE */}
      {featuredPost && (
        <section className="py-16 lg:py-24 bg-white">
          <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
            <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-8 mb-12">
              <div>
                <span className="text-[#F15C30] text-sm uppercase tracking-widest font-semibold font-serif">
                  Latest Articles
                </span>
                <h2 className="font-serif font-black text-3xl sm:text-4xl lg:text-5xl text-[#094d76] mt-4 tracking-tight">
                  Featured Insights
                </h2>
              </div>
            </div>

            <div className="grid lg:grid-cols-2 gap-8">
              {/* Featured dark card */}
              <Link
                href={slugPath(featuredPost)}
                className="group bg-[#094d76] rounded-3xl p-10 lg:p-14 flex flex-col justify-end min-h-[500px] relative overflow-hidden"
              >
                {featuredPost.heroImage &&
                featuredPost.heroImage.startsWith("http") ? (
                  <Image
                    src={featuredPost.heroImage}
                    alt={featuredPost.heroImageAlt ?? featuredPost.title}
                    fill
                    className="object-cover opacity-30 group-hover:opacity-40 transition-opacity"
                    sizes="(max-width: 1024px) 100vw, 50vw"
                  />
                ) : (
                  <div
                    className="absolute inset-0 opacity-10"
                    style={{
                      backgroundImage:
                        "radial-gradient(circle at 2px 2px, white 1px, transparent 0)",
                      backgroundSize: "32px 32px",
                    }}
                    aria-hidden="true"
                  />
                )}
                <div
                  className="absolute inset-0 pointer-events-none"
                  style={{
                    background:
                      "linear-gradient(135deg, rgba(241,92,48,0.08) 0%, transparent 60%)",
                  }}
                  aria-hidden="true"
                />
                <div className="relative">
                  {featuredPost.category && (
                    <span className="text-[#F15C30] text-sm font-semibold uppercase tracking-wider font-serif">
                      {featuredPost.category}
                    </span>
                  )}
                  <h3 className="font-serif font-bold text-3xl lg:text-4xl text-white mt-4 mb-6 group-hover:text-[#F15C30] transition-colors">
                    {featuredPost.title}
                  </h3>
                  {featuredPost.excerpt && (
                    <p className="text-white/75 leading-relaxed mb-6 font-sans">
                      {featuredPost.excerpt.length > 160
                        ? featuredPost.excerpt.slice(0, 157) + "…"
                        : featuredPost.excerpt}
                    </p>
                  )}
                  <div className="flex items-center justify-between">
                    <span className="text-white/60 text-sm font-sans">
                      {formatDate(postDate(featuredPost))}
                    </span>
                    <ArrowRight className="w-5 h-5 text-white group-hover:translate-x-2 transition-transform" />
                  </div>
                </div>
              </Link>

              {/* Side cards */}
              <div className="space-y-6">
                {sideFeatured.map((post) => (
                  <Link
                    key={post.id}
                    href={slugPath(post)}
                    className="group block p-8 lg:p-10 border border-[#094d76]/10 rounded-3xl hover:border-[#094d76]/30 transition-colors"
                  >
                    {post.category && (
                      <span className="text-[#F15C30] text-sm font-semibold uppercase tracking-wider font-serif">
                        {post.category}
                      </span>
                    )}
                    <h3 className="font-serif font-bold text-2xl text-[#094d76] mt-3 mb-4 group-hover:text-[#2575B6] transition-colors">
                      {post.title}
                    </h3>
                    {post.excerpt && (
                      <p className="text-[#9c9b9a] leading-relaxed mb-4 font-sans">
                        {post.excerpt.length > 140
                          ? post.excerpt.slice(0, 137) + "…"
                          : post.excerpt}
                      </p>
                    )}
                    <div className="flex items-center justify-between">
                      <span className="text-[#9c9b9a] text-sm font-sans">
                        {formatDate(postDate(post))}
                      </span>
                      <ArrowRight className="w-5 h-5 text-[#094d76] group-hover:translate-x-2 transition-transform" />
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* MORE ARTICLES */}
      {older.length > 0 && (
        <section className="py-16 lg:py-24 bg-[#f2f2f4]">
          <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
            <h2 className="font-serif font-black text-3xl lg:text-4xl text-[#094d76] mb-10 tracking-tight">
              More Articles
            </h2>
            <div className="bg-white rounded-3xl overflow-hidden">
              <ul className="divide-y divide-[#094d76]/10">
                {older.map((post) => (
                  <li key={post.id}>
                    <Link
                      href={slugPath(post)}
                      className="group block px-8 lg:px-10 py-6 hover:bg-[#e8f4fd] transition-colors border-l-4 border-transparent hover:border-[#F15C30]"
                    >
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                        <div className="flex-1 min-w-0">
                          {post.category && (
                            <span className="text-[#F15C30] text-xs uppercase tracking-widest font-serif font-semibold">
                              {post.category}
                            </span>
                          )}
                          <h3 className="font-serif font-bold text-lg lg:text-xl text-[#094d76] group-hover:text-[#2575B6] transition-colors mt-1 line-clamp-1">
                            {post.title}
                          </h3>
                        </div>
                        <div className="flex items-center gap-6 shrink-0">
                          <span className="text-[#9c9b9a] text-sm font-sans">
                            {formatDate(postDate(post))}
                          </span>
                          <ArrowRight className="w-5 h-5 text-[#094d76] group-hover:translate-x-1 transition-transform" />
                        </div>
                      </div>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>
      )}

      {sorted.length === 0 && (
        <section className="py-32 bg-[#f2f2f4]">
          <div className="max-w-2xl mx-auto px-6 text-center">
            <BookOpen className="w-12 h-12 text-[#094d76]/30 mx-auto mb-6" />
            <p className="text-[#9c9b9a] font-sans text-lg">
              No articles yet. Check back soon.
            </p>
          </div>
        </section>
      )}

      {/* CTA SPLIT */}
      <section className="relative">
        <div className="flex flex-col lg:flex-row">
          <div className="flex-1 bg-[#F15C30] py-24 lg:py-32 px-6 lg:px-12 flex items-center justify-center lg:justify-end">
            <h2 className="font-serif font-black text-5xl lg:text-6xl text-white text-center lg:text-right lg:pr-8">
              Ready to
            </h2>
          </div>
          <div className="flex-1 bg-[#094d76] py-24 lg:py-32 px-6 lg:px-12 flex items-center justify-center lg:justify-start">
            <h2 className="font-serif font-black text-5xl lg:text-6xl text-white text-center lg:text-left lg:pl-8">
              Get Started?
            </h2>
          </div>
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
            <Link
              href={config.contactPath}
              className="inline-flex items-center gap-3 bg-white text-[#094d76] font-serif font-bold px-10 py-5 rounded-full shadow-2xl hover:scale-105 transition-transform text-lg"
            >
              Contact Us
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      <SAFooter config={config} />
    </main>
  );
}
