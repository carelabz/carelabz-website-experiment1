import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { marked } from "marked";
import {
  Shield,
  FileText,
  CheckCircle2,
  ChevronRight,
  Activity,
  BarChart2,
  Settings,
  Cpu,
  ClipboardList,
  ArrowRight,
} from "lucide-react";
import { SAAnnouncementTicker } from "@/components/sa-announcement-ticker";
import { SANavbar } from "@/components/sa-navbar";
import { SAFooter } from "@/components/sa-footer";
import { JsonLd } from "@/components/JsonLd";
import { getServicePageBySlug, ServicePage } from "@/lib/strapi";
import { getBlogPost, BlogPost } from "@/lib/strapi-blog";
import { COUNTRY_CONFIGS } from "@/lib/countries-config";

export const dynamic = "force-dynamic";

const CC = "br";
const COUNTRY_NAME = "Brazil";
const HREFLANG = "en-BR";
const config = COUNTRY_CONFIGS[CC];

interface PageProps {
  params: { slug: string };
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const pageUrl = `https://carelabz.com/${CC}/${params.slug}/`;
  const service = await getServicePageBySlug(`${params.slug}-${CC}`);
  if (service) {
    return {
      title: service.metaTitle || `${service.title} | Carelabs ${COUNTRY_NAME}`,
      description: service.metaDescription || undefined,
      keywords: service.seoKeywords?.join(", "),
      alternates: {
        canonical: pageUrl,
        languages: { [HREFLANG]: pageUrl, "x-default": pageUrl },
      },
      openGraph: {
        title: service.metaTitle || `${service.title} | Carelabs ${COUNTRY_NAME}`,
        description: service.metaDescription || undefined,
        url: pageUrl,
        type: "website",
      },
      twitter: {
        card: "summary_large_image",
        title: service.metaTitle || `${service.title} | Carelabs ${COUNTRY_NAME}`,
        description: service.metaDescription || undefined,
      },
    };
  }
  const post = await getBlogPost(CC, `${params.slug}-${CC}`);
  if (post) {
    return {
      title: post.metaTitle ?? `${post.title} | Carelabs ${COUNTRY_NAME}`,
      description: post.metaDescription ?? post.excerpt ?? undefined,
      keywords: post.seoKeywords ?? undefined,
      alternates: {
        canonical: pageUrl,
        languages: { [HREFLANG]: pageUrl, "x-default": pageUrl },
      },
      openGraph: {
        title: post.metaTitle ?? `${post.title} | Carelabs ${COUNTRY_NAME}`,
        description: post.metaDescription ?? post.excerpt ?? undefined,
        url: pageUrl,
        siteName: "Carelabs",
        type: "article",
      },
      twitter: {
        card: "summary_large_image",
        title: post.metaTitle ?? `${post.title} | Carelabs ${COUNTRY_NAME}`,
        description: post.metaDescription ?? post.excerpt ?? undefined,
      },
    };
  }
  return { title: `Not Found | Carelabs ${COUNTRY_NAME}` };
}

const STEP_ICONS = [ClipboardList, Cpu, BarChart2, Settings, Activity, Shield];

function buildServiceData(service: ServicePage) {
  return {
    title: service.title,
    eyebrow: service.eyebrow || "Electrical Safety",
    definitionalLede: service.definitionalLede || service.metaDescription || "",
    trustBadges:
      service.trustBadges ||
      config.standards.slice(0, 4).map((s) => ({ label: s })),
    featuresHeading: service.featuresHeading || "Key Challenges We Solve",
    featuresSubtext:
      service.featuresSubtext ||
      "Our engineers identify and resolve electrical safety risks before they become costly incidents.",
    features: service.features || [],
    safetyEyebrow: service.safetyEyebrow || "Worker Safety",
    safetyHeading: service.safetyHeading || "Protecting Your Team",
    safetyBody:
      service.safetyBody ||
      `Electrical hazards are among the leading causes of workplace injuries in ${COUNTRY_NAME} facilities.`,
    safetyBullets: service.safetyBullets || [],
    reportsEyebrow: service.reportsEyebrow || "Deliverables",
    reportsHeading: service.reportsHeading || "Comprehensive Report Package",
    reportsBody:
      service.reportsBody ||
      `Every engagement concludes with a ${config.primaryStandard}-aligned report package.`,
    reportsBullets: service.reportsBullets || [],
    processHeading: service.processHeading || "Our Process",
    processSteps: service.processSteps || [],
    faqs: service.faqs || [],
    faqSectionHeading: service.faqSectionHeading || "Frequently Asked Questions",
    ctaBannerHeading:
      service.ctaBannerHeading || "Ready to Schedule Your Study?",
    ctaBannerBody:
      service.ctaBannerBody ||
      "Our certified engineers deliver fast turnaround, clear reports, and full compliance support.",
    ctaBannerPrimaryText: service.ctaBannerPrimaryText || "Get a Free Quote",
    ctaBannerPrimaryHref:
      service.ctaBannerPrimaryHref || config.contactPath,
    ctaBannerSecondaryText:
      service.ctaBannerSecondaryText || "View All Services",
    ctaBannerSecondaryHref:
      service.ctaBannerSecondaryHref || config.servicesIndexPath,
  };
}

function CTASplit({
  leadText,
  tailText,
  buttonText,
  buttonHref,
}: {
  leadText: string;
  tailText: string;
  buttonText: string;
  buttonHref: string;
}) {
  return (
    <section className="relative">
      <div className="flex flex-col lg:flex-row">
        <div className="flex-1 bg-[#F15C30] py-20 lg:py-32 px-6 lg:px-12 flex items-center justify-center lg:justify-end">
          <h2 className="font-serif font-black text-4xl sm:text-5xl lg:text-6xl text-white text-center lg:text-right lg:pr-8">
            {leadText}
          </h2>
        </div>
        <div className="flex-1 bg-[#094d76] py-20 lg:py-32 px-6 lg:px-12 flex items-center justify-center lg:justify-start">
          <h2 className="font-serif font-black text-4xl sm:text-5xl lg:text-6xl text-white text-center lg:text-left lg:pl-8">
            {tailText}
          </h2>
        </div>
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
          <Link
            href={buttonHref}
            className="inline-flex items-center gap-3 bg-white text-[#094d76] font-serif font-bold px-10 py-5 rounded-full shadow-2xl hover:scale-105 transition-transform text-lg"
          >
            {buttonText}
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </div>
    </section>
  );
}

function ServiceView({ service, slug }: { service: ServicePage; slug: string }) {
  const data = buildServiceData(service);
  const pageUrl = `https://carelabz.com/${CC}/${slug}/`;
  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebPage",
        "@id": pageUrl,
        url: pageUrl,
        name: service.metaTitle || `${service.title} | Carelabs ${COUNTRY_NAME}`,
        description: service.metaDescription || undefined,
        inLanguage: HREFLANG,
        isPartOf: { "@id": "https://carelabz.com/#website" },
      },
      {
        "@type": "Service",
        name: service.title,
        serviceType: "Electrical Safety Engineering",
        description: data.definitionalLede || service.metaDescription || undefined,
        url: pageUrl,
        provider: {
          "@type": "LocalBusiness",
          name: "Carelabs",
          url: "https://carelabz.com",
          telephone: config.phone,
          email: config.email,
          address: {
            "@type": "PostalAddress",
            addressLocality: config.address,
            addressCountry: CC.toUpperCase(),
          },
        },
        areaServed: { "@type": "Country", name: COUNTRY_NAME },
      },
      ...(data.faqs.length > 0
        ? [
            {
              "@type": "FAQPage",
              mainEntity: data.faqs.map((faq) => ({
                "@type": "Question",
                name: faq.question,
                acceptedAnswer: { "@type": "Answer", text: faq.answer },
              })),
            },
          ]
        : []),
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          {
            "@type": "ListItem",
            position: 1,
            name: "Home",
            item: `https://carelabz.com/${CC}/`,
          },
          {
            "@type": "ListItem",
            position: 2,
            name: "Services",
            item: `https://carelabz.com${config.servicesIndexPath}`,
          },
          {
            "@type": "ListItem",
            position: 3,
            name: service.title,
            item: pageUrl,
          },
        ],
      },
    ],
  };

  return (
    <main className="bg-white font-sans">
      <JsonLd data={jsonLd} />
      <SAAnnouncementTicker
        countryName={COUNTRY_NAME}
        standards={config.standards}
      />
      <SANavbar config={config} />

      {/* HERO — dark blue gradient */}
      <section
        className="relative overflow-hidden py-24 lg:py-32"
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
        <div className="absolute top-16 right-[8%] w-64 h-64 border-[3px] border-white/10 rounded-full pointer-events-none" />
        <div className="absolute top-32 right-[14%] w-40 h-40 bg-[#F15C30]/15 rounded-full pointer-events-none" />

        <div className="relative max-w-[1400px] mx-auto px-6 lg:px-12">
          <nav aria-label="Breadcrumb" className="mb-10">
            <ol className="flex flex-wrap items-center gap-2 text-sm text-white/70 font-sans">
              <li>
                <Link
                  href={`/${CC}/`}
                  className="hover:text-[#F15C30] transition-colors"
                >
                  Home
                </Link>
              </li>
              <li>
                <ChevronRight className="h-3 w-3" />
              </li>
              <li>
                <Link
                  href={config.servicesIndexPath}
                  className="hover:text-[#F15C30] transition-colors"
                >
                  Services
                </Link>
              </li>
              <li>
                <ChevronRight className="h-3 w-3" />
              </li>
              <li className="text-white">{service.title}</li>
            </ol>
          </nav>

          <div className="max-w-3xl">
            <span className="text-[#F15C30] text-sm uppercase tracking-widest font-semibold font-serif">
              {data.eyebrow}
            </span>
            <h1 className="font-serif font-black text-4xl sm:text-5xl lg:text-7xl text-white mt-6 tracking-tight leading-[1.05]">
              {service.title}
            </h1>
            {data.definitionalLede && (
              <p className="mt-8 text-lg text-white/75 leading-relaxed max-w-2xl font-sans">
                {data.definitionalLede}
              </p>
            )}
            <div className="mt-10 flex flex-wrap gap-4">
              <Link
                href={data.ctaBannerPrimaryHref}
                className="inline-flex items-center gap-3 bg-[#F15C30] text-white font-sans font-semibold px-8 py-4 rounded-full hover:bg-[#c44a1f] transition-colors"
              >
                Free Consultation
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                href={config.servicesIndexPath}
                className="inline-flex items-center gap-3 border-2 border-white/50 text-white font-sans font-semibold px-8 py-4 rounded-full hover:bg-white hover:text-[#094d76] transition-colors"
              >
                All Services
              </Link>
            </div>
            {data.trustBadges.length > 0 && (
              <div className="flex flex-wrap gap-3 mt-10">
                {data.trustBadges.map((badge, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center gap-2 rounded-full bg-white/10 border border-white/20 px-4 py-2 text-sm text-white font-sans backdrop-blur-sm"
                  >
                    <Shield className="h-3.5 w-3.5 text-[#F15C30]" />
                    {badge.label}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* FEATURES INTRO */}
      <section className="py-20 lg:py-28 bg-white">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="max-w-3xl">
            <span className="text-[#F15C30] text-sm uppercase tracking-widest font-semibold font-serif">
              Challenges We Solve
            </span>
            <h2 className="font-serif font-black text-4xl sm:text-5xl lg:text-6xl text-[#094d76] mt-4 tracking-tight">
              {data.featuresHeading}
            </h2>
            {data.featuresSubtext && (
              <p className="mt-8 text-lg text-[#9c9b9a] leading-relaxed font-sans">
                {data.featuresSubtext}
              </p>
            )}
          </div>
        </div>
      </section>

      {/* FEATURES LIST */}
      {data.features.length > 0 && (
        <section className="py-20 lg:py-28 bg-[#f2f2f4]">
          <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
            <h2 className="font-serif font-black text-3xl sm:text-4xl lg:text-5xl text-[#094d76] tracking-tight mb-16">
              What We Deliver
            </h2>
            <div className="grid gap-6 md:grid-cols-2">
              {data.features.map((feature, i) => (
                <div
                  key={i}
                  className="bg-white rounded-3xl p-8 lg:p-10 hover:shadow-2xl transition-shadow"
                >
                  <div className="w-14 h-14 bg-[#e8f4fd] rounded-2xl flex items-center justify-center mb-6">
                    <span className="font-serif font-black text-[#2575B6] text-xl">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                  </div>
                  <h3 className="font-serif font-bold text-xl lg:text-2xl text-[#094d76] mb-4">
                    {feature.title}
                  </h3>
                  <p className="text-[#9c9b9a] leading-relaxed font-sans">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* SAFETY SECTION */}
      <section className="py-20 lg:py-28 bg-white">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
            <div>
              <span className="text-[#F15C30] text-sm uppercase tracking-widest font-semibold font-serif">
                {data.safetyEyebrow}
              </span>
              <h2 className="font-serif font-black text-3xl sm:text-4xl lg:text-5xl text-[#094d76] mt-4 tracking-tight">
                {data.safetyHeading}
              </h2>
              <p className="mt-8 text-[#9c9b9a] leading-relaxed font-sans">
                {data.safetyBody}
              </p>
              {data.safetyBullets.length > 0 && (
                <ul className="mt-8 space-y-3">
                  {data.safetyBullets.map((bullet, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <CheckCircle2 className="w-5 h-5 text-[#F15C30] mt-0.5 shrink-0" />
                      <span className="text-[#094d76] font-sans">{bullet}</span>
                    </li>
                  ))}
                </ul>
              )}
              <Link
                href={config.contactPath}
                className="mt-10 inline-flex items-center gap-3 bg-[#F15C30] text-white font-sans font-semibold px-8 py-4 rounded-full hover:bg-[#c44a1f] transition-colors"
              >
                Contact Us
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
            <div
              className="relative rounded-3xl aspect-[4/3] flex items-center justify-center overflow-hidden"
              style={{
                background:
                  "linear-gradient(135deg, #e8f4fd 0%, rgba(37,117,182,0.25) 100%)",
              }}
            >
              <Shield className="w-32 h-32 text-[#094d76]/20" />
            </div>
          </div>
        </div>
      </section>

      {/* REPORTS */}
      <section className="py-20 lg:py-28 bg-[#f2f2f4]">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
            <div
              className="relative rounded-3xl aspect-[4/3] flex items-center justify-center bg-white order-2 lg:order-1"
            >
              <FileText className="w-32 h-32 text-[#094d76]/15" />
            </div>
            <div className="order-1 lg:order-2">
              <span className="text-[#F15C30] text-sm uppercase tracking-widest font-semibold font-serif">
                {data.reportsEyebrow}
              </span>
              <h2 className="font-serif font-black text-3xl sm:text-4xl lg:text-5xl text-[#094d76] mt-4 tracking-tight">
                {data.reportsHeading}
              </h2>
              <p className="mt-8 text-[#9c9b9a] leading-relaxed font-sans">
                {data.reportsBody}
              </p>
              {data.reportsBullets.length > 0 && (
                <ol className="mt-8 space-y-4">
                  {data.reportsBullets.map((bullet, i) => (
                    <li key={i} className="flex items-start gap-4">
                      <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-[#F15C30] text-white font-serif font-black text-sm shrink-0">
                        {i + 1}
                      </span>
                      <span className="text-[#094d76] font-sans pt-1">
                        {bullet}
                      </span>
                    </li>
                  ))}
                </ol>
              )}
              <Link
                href={config.contactPath}
                className="mt-10 inline-flex items-center gap-3 bg-[#094d76] text-white font-sans font-semibold px-8 py-4 rounded-full hover:bg-[#2575B6] transition-colors"
              >
                Reach Out
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* PROCESS */}
      {data.processSteps.length > 0 && (
        <section className="py-20 lg:py-28 bg-white">
          <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
            <div className="mb-16 text-center">
              <span className="text-[#F15C30] text-sm uppercase tracking-widest font-semibold font-serif">
                How We Work
              </span>
              <h2 className="font-serif font-black text-4xl sm:text-5xl lg:text-6xl text-[#094d76] mt-4 tracking-tight">
                {data.processHeading}
              </h2>
            </div>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {data.processSteps.map((step, idx) => {
                const Icon = STEP_ICONS[idx % STEP_ICONS.length];
                const stepNum = step.number ?? idx + 1;
                return (
                  <div
                    key={stepNum}
                    className="relative bg-[#f2f2f4] rounded-3xl p-8 lg:p-10 hover:bg-[#e8f4fd] transition-colors"
                  >
                    <span className="absolute top-6 right-8 font-serif font-black text-6xl text-[#094d76]/10 leading-none">
                      {String(stepNum).padStart(2, "0")}
                    </span>
                    <div className="w-14 h-14 bg-white rounded-2xl flex items-center justify-center mb-6">
                      <Icon className="w-7 h-7 text-[#2575B6]" />
                    </div>
                    <h3 className="font-serif font-bold text-xl text-[#094d76] mb-3">
                      {step.title}
                    </h3>
                    <p className="text-[#9c9b9a] leading-relaxed font-sans text-sm">
                      {step.description}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        </section>
      )}

      {/* FAQ */}
      {data.faqs.length > 0 && (
        <section className="py-24 lg:py-28 bg-[#f2f2f4]">
          <div className="max-w-3xl mx-auto px-6 lg:px-12">
            <div className="mb-12 text-center">
              <span className="text-[#F15C30] text-sm uppercase tracking-widest font-semibold font-serif">
                FAQ
              </span>
              <h2 className="font-serif font-black text-4xl sm:text-5xl text-[#094d76] mt-4 tracking-tight">
                {data.faqSectionHeading}
              </h2>
            </div>
            <div className="space-y-4">
              {data.faqs.map((faq, i) => (
                <details
                  key={i}
                  className="group bg-white rounded-2xl p-6 open:shadow-lg transition-shadow"
                >
                  <summary className="flex items-center justify-between cursor-pointer list-none">
                    <span className="font-serif font-bold text-[#094d76] text-lg pr-6">
                      {faq.question}
                    </span>
                    <span className="text-[#F15C30] text-2xl transition-transform group-open:rotate-45 shrink-0">
                      +
                    </span>
                  </summary>
                  <p className="mt-4 text-[#9c9b9a] font-sans leading-relaxed">
                    {faq.answer}
                  </p>
                </details>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA SPLIT */}
      <CTASplit
        leadText="Ready to"
        tailText="Get Started?"
        buttonText={data.ctaBannerPrimaryText}
        buttonHref={data.ctaBannerPrimaryHref}
      />

      <SAFooter config={config} />
    </main>
  );
}

function formatDate(s: string | null): string {
  if (!s) return "";
  try {
    return new Date(s).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  } catch {
    return s;
  }
}

function BlogView({ post }: { post: BlogPost }) {
  const articleJsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: post.title,
    description: post.metaDescription ?? post.excerpt ?? "",
    inLanguage: HREFLANG,
    author: {
      "@type": "Person",
      name: post.author ?? "Carelabs Engineering Team",
    },
    datePublished: post.publishedDate ?? post.publishedAt,
    dateModified: post.updatedAt,
    publisher: {
      "@type": "Organization",
      name: "Carelabs",
      url: "https://carelabz.com",
    },
    ...(post.heroImage
      ? { image: `https://carelabz.com${post.heroImage}` }
      : {}),
    url: `https://carelabz.com/${CC}/${post.slug}/`,
  };

  return (
    <main className="bg-white font-sans">
      <JsonLd data={articleJsonLd} />
      <SAAnnouncementTicker
        countryName={COUNTRY_NAME}
        standards={config.standards}
      />
      <SANavbar config={config} />

      {/* HERO */}
      <section
        className="relative overflow-hidden py-20 lg:py-28"
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
        <div className="relative max-w-[1000px] mx-auto px-6 lg:px-12">
          <nav
            aria-label="Breadcrumb"
            className="flex items-center gap-2 text-sm text-white/70 mb-8 flex-wrap font-sans"
          >
            <Link
              href={`/${CC}/`}
              className="hover:text-[#F15C30] transition-colors"
            >
              Home
            </Link>
            <span aria-hidden="true">/</span>
            <Link
              href={config.blogIndexPath}
              className="hover:text-[#F15C30] transition-colors"
            >
              Blog
            </Link>
            <span aria-hidden="true">/</span>
            <span className="text-white line-clamp-1">{post.title}</span>
          </nav>
          {post.category && (
            <span className="inline-block px-4 py-1.5 rounded-full bg-[#F15C30]/20 text-[#F15C30] text-xs uppercase tracking-wider font-serif font-semibold">
              {post.category}
            </span>
          )}
          <h1 className="mt-6 font-serif font-black text-4xl sm:text-5xl lg:text-6xl text-white leading-[1.05] tracking-tight">
            {post.title}
          </h1>
          <div className="mt-8 flex flex-wrap items-center gap-4 text-sm text-white/75 font-sans">
            {post.author && (
              <span>
                By <span className="text-white font-medium">{post.author}</span>
              </span>
            )}
            {post.publishedDate && (
              <time dateTime={post.publishedDate}>
                {formatDate(post.publishedDate)}
              </time>
            )}
          </div>
          {post.heroImage && post.heroImage.startsWith("http") && (
            <div className="mt-10 relative aspect-[16/9] rounded-3xl overflow-hidden shadow-2xl">
              <Image
                src={post.heroImage}
                alt={post.heroImageAlt ?? post.title}
                fill
                priority
                className="object-cover"
                sizes="(max-width: 1000px) 100vw, 1000px"
              />
            </div>
          )}
        </div>
      </section>

      {/* BODY */}
      <section className="py-16 lg:py-24 bg-white">
        <div className="max-w-3xl mx-auto px-6 lg:px-12">
          <article
            className="prose prose-lg max-w-none prose-headings:font-serif prose-headings:font-black prose-headings:text-[#094d76] prose-p:text-[#5a5d66] prose-p:font-sans prose-li:text-[#5a5d66] prose-li:font-sans prose-strong:text-[#094d76] prose-a:text-[#F15C30] prose-a:no-underline hover:prose-a:underline"
            dangerouslySetInnerHTML={{
              __html: marked(post.body || "") as string,
            }}
          />
          {post.tags && post.tags.length > 0 && (
            <div className="mt-10 flex flex-wrap gap-2">
              {post.tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-[#f2f2f4] px-4 py-1.5 text-xs font-medium text-[#094d76] font-sans"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* FAQ */}
      {post.faqs && post.faqs.length > 0 && (
        <section className="py-20 bg-[#f2f2f4]">
          <div className="max-w-3xl mx-auto px-6 lg:px-12">
            <h2 className="font-serif font-black text-3xl sm:text-4xl text-[#094d76] mb-8 text-center">
              Frequently Asked Questions
            </h2>
            <div className="space-y-4">
              {post.faqs.map((faq, i) => (
                <details
                  key={i}
                  className="group bg-white rounded-2xl p-6 open:shadow-lg transition-shadow"
                >
                  <summary className="flex items-center justify-between cursor-pointer list-none">
                    <span className="font-serif font-bold text-[#094d76] pr-6">
                      {faq.question}
                    </span>
                    <span className="text-[#F15C30] text-2xl transition-transform group-open:rotate-45 shrink-0">
                      +
                    </span>
                  </summary>
                  <p className="mt-4 text-[#9c9b9a] font-sans leading-relaxed">
                    {faq.answer}
                  </p>
                </details>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA SPLIT */}
      <CTASplit
        leadText="Need expert"
        tailText="help?"
        buttonText="Contact Us"
        buttonHref={config.contactPath}
      />

      <SAFooter config={config} />
    </main>
  );
}

export default async function Page({ params }: PageProps) {
  const service = await getServicePageBySlug(`${params.slug}-${CC}`);
  if (service) return <ServiceView service={service} slug={params.slug} />;
  const post = await getBlogPost(CC, `${params.slug}-${CC}`);
  if (post) return <BlogView post={post} />;
  notFound();
}
