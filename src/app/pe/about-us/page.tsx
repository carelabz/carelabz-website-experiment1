import type { Metadata } from "next";
import Link from "next/link";
import {
  ShieldCheck,
  Zap,
  Users,
  Star,
  Heart,
  Globe,
  Award,
  CheckCircle2,
  Wrench,
  BarChart2,
  Clock,
  Lightbulb,
  ArrowRight,
} from "lucide-react";
import { SAAnnouncementTicker } from "@/components/sa-announcement-ticker";
import { SANavbar } from "@/components/sa-navbar";
import { SAFooter } from "@/components/sa-footer";
import { COUNTRY_CONFIGS } from "@/lib/countries-config";
import { getAboutPage } from "@/lib/strapi-pages";
import {
  buildJsonLd,
  getRegionOrganizationSchema,
  getWebPageSchema,
  getBreadcrumbSchema,
} from "@/lib/jsonld";

export const dynamic = "force-dynamic";

const CC = "pe";
const COUNTRY_NAME = "Peru";
const HREFLANG = "en-PE";
const config = COUNTRY_CONFIGS[CC];

export async function generateMetadata(): Promise<Metadata> {
  const page = await getAboutPage(CC);
  return {
    title:
      page?.metaTitle ??
      `About Carelabs | ${COUNTRY_NAME} Electrical Safety Experts`,
    description:
      page?.metaDescription ??
      `Learn about Carelabs — our mission, values, and the team dedicated to electrical safety testing and ${config.primaryStandard} compliance across ${COUNTRY_NAME}.`,
    alternates: {
      canonical: `https://carelabz.com/${CC}/about-us/`,
      languages: {
        [HREFLANG]: `https://carelabz.com/${CC}/about-us/`,
        "x-default": `https://carelabz.com/${CC}/about-us/`,
      },
    },
    openGraph: {
      title:
        page?.metaTitle ??
        `About Carelabs — Power System Consultants ${COUNTRY_NAME}`,
      description:
        page?.metaDescription ??
        `Carelabs is a leading electrical safety engineering firm in ${COUNTRY_NAME}.`,
      url: `https://carelabz.com/${CC}/about-us/`,
      siteName: "Carelabs",
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title:
        page?.metaTitle ??
        `About Carelabs — Power System Consultants ${COUNTRY_NAME}`,
      description:
        page?.metaDescription ??
        `Carelabs is a leading electrical safety engineering firm in ${COUNTRY_NAME}.`,
    },
  };
}

const ICON_MAP: Record<string, React.ElementType> = {
  shield: ShieldCheck,
  zap: Zap,
  users: Users,
  star: Star,
  heart: Heart,
  globe: Globe,
  award: Award,
  check: CheckCircle2,
  wrench: Wrench,
  bar: BarChart2,
  clock: Clock,
  lightbulb: Lightbulb,
};

function resolveIcon(iconName: string | null | undefined): React.ElementType {
  if (!iconName) return Star;
  const key = iconName.toLowerCase().replace(/[^a-z]/g, "");
  return ICON_MAP[key] ?? Star;
}

export default async function PEAboutPage() {
  const page = await getAboutPage(CC);

  const headline = page?.heroHeadline ?? "Who We Are";
  const subtext =
    page?.heroSubtext ??
    `Carelabs is a trusted partner for electrical safety testing, calibration, inspection, and certification services across ${COUNTRY_NAME}.`;

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
      `https://carelabz.com/${CC}/about-us/`,
      page?.metaTitle ??
        `About Carelabs — Power System Consultants ${COUNTRY_NAME}`,
      page?.metaDescription ??
        `Carelabs is a leading electrical safety engineering firm in ${COUNTRY_NAME}.`,
      HREFLANG
    ),
    getBreadcrumbSchema([
      { name: "Home", url: `https://carelabz.com/${CC}/` },
      { name: "About", url: `https://carelabz.com/${CC}/about-us/` },
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
        <div className="relative max-w-[1400px] mx-auto px-6 lg:px-12 text-center">
          <h1 className="mx-auto max-w-4xl font-serif font-black text-5xl sm:text-6xl lg:text-7xl text-white tracking-tight leading-[1.05]">
            {headline}
          </h1>
          <p className="mx-auto mt-8 max-w-2xl text-lg text-white/80 leading-relaxed font-sans">
            {subtext}
          </p>
        </div>
      </section>

      {/* MISSION */}
      {(page?.missionHeading || page?.missionBody) && (
        <section className="py-20 lg:py-28 bg-white">
          <div className="max-w-3xl mx-auto px-6 lg:px-12 text-center">
            <div className="w-1 h-16 bg-[#F15C30] mx-auto mb-8" />
            {page?.missionHeading && (
              <h2 className="font-serif font-black text-3xl sm:text-4xl lg:text-5xl text-[#094d76] mb-8 tracking-tight">
                {page.missionHeading}
              </h2>
            )}
            {page?.missionBody && (
              <p className="text-lg text-[#9c9b9a] leading-relaxed font-sans">
                {page.missionBody}
              </p>
            )}
          </div>
        </section>
      )}

      {/* VALUES */}
      {page?.values && page.values.length > 0 && (
        <section className="py-20 lg:py-28 bg-[#f2f2f4]">
          <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
            <div className="mb-16 text-center">
              <span className="text-[#F15C30] text-sm uppercase tracking-widest font-semibold font-serif">
                Our Values
              </span>
              {page?.valuesHeading && (
                <h2 className="font-serif font-black text-3xl sm:text-4xl lg:text-5xl text-[#094d76] mt-4 tracking-tight">
                  {page.valuesHeading}
                </h2>
              )}
            </div>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {page.values.map((value, idx) => {
                const Icon = resolveIcon(value.icon);
                return (
                  <div
                    key={idx}
                    className="bg-white rounded-3xl p-8 hover:shadow-2xl transition-shadow"
                  >
                    <div className="w-14 h-14 bg-[#e8f4fd] rounded-2xl flex items-center justify-center mb-6">
                      <Icon className="w-7 h-7 text-[#2575B6]" />
                    </div>
                    <h3 className="font-serif font-bold text-xl text-[#094d76] mb-3">
                      {value.title}
                    </h3>
                    <p className="text-[#9c9b9a] text-sm leading-relaxed font-sans">
                      {value.description}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        </section>
      )}

      {/* CERTIFICATIONS */}
      {page?.certifications && page.certifications.length > 0 && (
        <section className="py-20 bg-white">
          <div className="max-w-5xl mx-auto px-6 lg:px-12">
            <h2 className="font-serif font-black text-3xl sm:text-4xl text-[#094d76] mb-10 text-center tracking-tight">
              Standards We Follow
            </h2>
            <div className="flex flex-wrap justify-center gap-3">
              {page.certifications.map((cert, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-2 bg-[#e8f4fd] border border-[#2575B6]/20 rounded-full px-5 py-3"
                >
                  <Award className="w-4 h-4 text-[#F15C30] shrink-0" />
                  <span className="text-sm font-medium text-[#094d76] font-sans">
                    {cert}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA SPLIT */}
      <section className="relative">
        <div className="flex flex-col lg:flex-row">
          <div className="flex-1 bg-[#F15C30] py-24 lg:py-32 px-6 lg:px-12 flex items-center justify-center lg:justify-end">
            <h2 className="font-serif font-black text-5xl lg:text-6xl text-white text-center lg:text-right lg:pr-8">
              {page?.ctaBannerHeading ?? "Partner"}
            </h2>
          </div>
          <div className="flex-1 bg-[#094d76] py-24 lg:py-32 px-6 lg:px-12 flex items-center justify-center lg:justify-start">
            <h2 className="font-serif font-black text-5xl lg:text-6xl text-white text-center lg:text-left lg:pl-8">
              with Carelabs
            </h2>
          </div>
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
            <Link
              href={page?.ctaBannerPrimaryHref ?? config.contactPath}
              className="inline-flex items-center gap-3 bg-white text-[#094d76] font-serif font-bold px-10 py-5 rounded-full shadow-2xl hover:scale-105 transition-transform text-lg"
            >
              {page?.ctaBannerPrimaryText ?? "Get in Touch"}
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      <SAFooter config={config} />
    </main>
  );
}
