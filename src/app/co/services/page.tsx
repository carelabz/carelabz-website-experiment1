import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SAAnnouncementTicker } from "@/components/sa-announcement-ticker";
import { SANavbar } from "@/components/sa-navbar";
import { SAFooter } from "@/components/sa-footer";
import { COUNTRY_CONFIGS } from "@/lib/countries-config";
import { getServicesByRegion, ServicePage } from "@/lib/strapi";
import {
  buildJsonLd,
  getRegionOrganizationSchema,
  getWebPageSchema,
  getBreadcrumbSchema,
} from "@/lib/jsonld";

export const dynamic = "force-dynamic";

const CC = "co";
const COUNTRY_NAME = "Colombia";
const HREFLANG = "en-CO";
const config = COUNTRY_CONFIGS[CC];

export const metadata: Metadata = {
  title: `Electrical Safety Services ${COUNTRY_NAME} | Carelabs`,
  description: `Discover Carelabs' ${COUNTRY_NAME} electrical safety services — arc flash studies, short circuit analysis, load flow analysis, and relay coordination aligned with ${config.primaryStandard}.`,
  alternates: {
    canonical: `https://carelabz.com/${CC}/service/`,
    languages: {
      [HREFLANG]: `https://carelabz.com/${CC}/service/`,
      "x-default": `https://carelabz.com/${CC}/service/`,
    },
  },
  openGraph: {
    title: `Power System Engineering Services in ${COUNTRY_NAME} | Carelabs`,
    description: `Professional electrical safety services including arc flash studies, short circuit analysis, and power system engineering across ${COUNTRY_NAME}.`,
    url: `https://carelabz.com/${CC}/service/`,
    siteName: "Carelabs",
    type: "website",
    locale: HREFLANG.replace("-", "_"),
  },
  twitter: {
    card: "summary_large_image",
    title: `Power System Engineering Services in ${COUNTRY_NAME} | Carelabs`,
    description: `Professional electrical safety services including arc flash studies, short circuit analysis, and power system engineering across ${COUNTRY_NAME}.`,
  },
};

function getServiceHref(service: ServicePage): string {
  const slug = service.slug;
  const urlSlug = slug.endsWith(`-${CC}`) ? slug.slice(0, -3) : slug;
  return `/${CC}/${urlSlug}/`;
}

export default async function COServicesIndexPage() {
  const services = await getServicesByRegion(CC);

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
      `https://carelabz.com/${CC}/service/`,
      `Power System Engineering Services in ${COUNTRY_NAME} | Carelabs`,
      `Professional electrical safety services including arc flash studies, short circuit analysis, and power system engineering across ${COUNTRY_NAME}.`,
      HREFLANG
    ),
    getBreadcrumbSchema([
      { name: "Home", url: `https://carelabz.com/${CC}/` },
      { name: "Services", url: `https://carelabz.com/${CC}/service/` },
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
        <div className="absolute top-12 right-[8%] w-56 h-56 border-[3px] border-white/10 rounded-full pointer-events-none" />
        <div className="absolute top-24 right-[14%] w-36 h-36 bg-[#F15C30]/15 rounded-full pointer-events-none" />

        <div className="relative max-w-[1400px] mx-auto px-6 lg:px-12 text-center">
          <span className="text-[#F15C30] text-sm uppercase tracking-widest font-semibold font-serif">
            {COUNTRY_NAME} Electrical Engineering
          </span>
          <h1 className="mt-6 mx-auto max-w-4xl font-serif font-black text-5xl sm:text-6xl lg:text-7xl text-white tracking-tight leading-[1.05]">
            Power System Analysis for Your Specific Needs
          </h1>
          <p className="mx-auto mt-8 max-w-2xl text-lg text-white/75 leading-relaxed font-sans">
            Comprehensive electrical safety services designed to keep your
            facilities compliant with {config.primaryStandard}, your workers
            protected, and your operations running smoothly — delivered by
            certified engineers across {COUNTRY_NAME}.
          </p>
        </div>
      </section>

      {/* SERVICES GRID */}
      <section className="py-20 lg:py-28 bg-[#f2f2f4]">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          {services.length === 0 ? (
            <p className="text-center py-12 text-[#9c9b9a] font-sans">
              Services are currently being loaded. Please check back shortly.
            </p>
          ) : (
            <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {services.map((service, index) => (
                <article
                  key={service.id}
                  className="bg-white rounded-3xl p-8 lg:p-10 hover:shadow-2xl transition-shadow group"
                >
                  <span className="font-serif font-black text-5xl text-[#f2f2f4] group-hover:text-[#e8f4fd] transition-colors block mb-6">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <h2 className="font-serif font-bold text-2xl text-[#094d76] mb-4">
                    {service.title}
                  </h2>
                  {service.metaDescription && (
                    <p className="text-[#9c9b9a] leading-relaxed font-sans line-clamp-4 mb-8">
                      {service.metaDescription.length > 200
                        ? service.metaDescription.slice(0, 197) + "…"
                        : service.metaDescription}
                    </p>
                  )}
                  <Link
                    href={getServiceHref(service)}
                    className="inline-flex items-center gap-2 text-[#F15C30] font-serif font-semibold text-sm hover:text-[#2575B6] transition-colors"
                  >
                    Learn more
                    <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
                  </Link>
                </article>
              ))}
            </div>
          )}
        </div>
      </section>

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
