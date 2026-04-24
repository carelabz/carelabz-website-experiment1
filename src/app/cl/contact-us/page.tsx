import type { Metadata } from "next";
import Link from "next/link";
import { headers } from "next/headers";
import { Phone, Mail, MapPin, Clock } from "lucide-react";
import { SAAnnouncementTicker } from "@/components/sa-announcement-ticker";
import { SANavbar } from "@/components/sa-navbar";
import { SAFooter } from "@/components/sa-footer";
import { COUNTRY_CONFIGS } from "@/lib/countries-config";
import { ContactForm } from "@/components/contact-form";
import { getContactPage } from "@/lib/strapi-pages";
import { getServicesByRegion } from "@/lib/strapi";
import { getCountryFromHeaders } from "@/lib/detect-country";
import {
  buildJsonLd,
  getRegionOrganizationSchema,
  getWebPageSchema,
  getBreadcrumbSchema,
} from "@/lib/jsonld";

export const dynamic = "force-dynamic";

const CC = "cl";
const COUNTRY_NAME = "Chile";
const HREFLANG = "en-CL";
const config = COUNTRY_CONFIGS[CC];

export async function generateMetadata(): Promise<Metadata> {
  const page = await getContactPage(CC);
  return {
    title: page?.metaTitle ?? `Contact Carelabs ${COUNTRY_NAME} | Get in Touch`,
    description:
      page?.metaDescription ??
      `Contact the Carelabs team for electrical safety testing, arc flash studies, and ${config.primaryStandard} compliance services across ${COUNTRY_NAME}.`,
    alternates: {
      canonical: `https://carelabz.com/${CC}/contact-us/`,
      languages: {
        [HREFLANG]: `https://carelabz.com/${CC}/contact-us/`,
        "x-default": `https://carelabz.com/${CC}/contact-us/`,
      },
    },
    openGraph: {
      title:
        page?.metaTitle ??
        `Contact Carelabs — Get a Free Consultation ${COUNTRY_NAME}`,
      description:
        page?.metaDescription ??
        `Get in touch for a free consultation on electrical safety services in ${COUNTRY_NAME}.`,
      url: `https://carelabz.com/${CC}/contact-us/`,
      siteName: "Carelabs",
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title:
        page?.metaTitle ??
        `Contact Carelabs — Get a Free Consultation ${COUNTRY_NAME}`,
      description:
        page?.metaDescription ??
        `Get in touch for a free consultation on electrical safety services in ${COUNTRY_NAME}.`,
    },
  };
}

export default async function CLContactPage() {
  const headersList = headers();
  const iso2 = getCountryFromHeaders(headersList, CC.toUpperCase());
  const countryName = COUNTRY_NAME;

  const [page, services] = await Promise.all([
    getContactPage(CC),
    getServicesByRegion(CC),
  ]);

  const serviceOptions = services.map((s) => ({
    title: s.title,
    slug: s.slug,
  }));

  const headline = page?.heroHeadline ?? "Get in Touch";
  const subtext =
    page?.heroSubtext ??
    `Have a question or ready to start a project? Our ${COUNTRY_NAME} team is here to help.`;

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
      `https://carelabz.com/${CC}/contact-us/`,
      page?.metaTitle ??
        `Contact Carelabs — Get a Free Consultation ${COUNTRY_NAME}`,
      page?.metaDescription ??
        `Get in touch for a free consultation on electrical safety services in ${COUNTRY_NAME}.`,
      HREFLANG
    ),
    getBreadcrumbSchema([
      { name: "Home", url: `https://carelabz.com/${CC}/` },
      { name: "Contact", url: `https://carelabz.com/${CC}/contact-us/` },
    ]),
  ]);

  const contactRow = (
    Icon: React.ElementType,
    label: string,
    value: React.ReactNode
  ) => (
    <div className="flex items-start gap-5">
      <div className="w-12 h-12 bg-[#F15C30] rounded-xl flex items-center justify-center shrink-0">
        <Icon className="w-5 h-5 text-white" />
      </div>
      <div>
        <p className="font-serif font-bold text-[#094d76] uppercase tracking-widest text-xs mb-1">
          {label}
        </p>
        <div className="text-[#5a5d66] font-sans">{value}</div>
      </div>
    </div>
  );

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
          <h1 className="mx-auto max-w-4xl font-serif font-black text-5xl sm:text-6xl lg:text-7xl text-white tracking-tight leading-[1.05]">
            {headline}
          </h1>
          <p className="mx-auto mt-8 max-w-2xl text-lg text-white/80 leading-relaxed font-sans">
            {subtext}
          </p>
          <span className="inline-flex items-center gap-2 mt-8 px-4 py-2 rounded-full bg-white/10 border border-white/25 text-white text-sm font-sans backdrop-blur-sm">
            <MapPin className="w-4 h-4" />
            Showing services available in {countryName}
          </span>
        </div>
      </section>

      {/* FORM + CONTACT */}
      <section className="py-20 lg:py-28 bg-[#f2f2f4]">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="grid lg:grid-cols-2 gap-10 items-start">
            <div className="bg-white rounded-3xl p-8 lg:p-12 shadow-xl">
              <h2 className="font-serif font-black text-3xl text-[#094d76] mb-3">
                {page?.formHeading ?? "Send Us a Message"}
              </h2>
              <p className="text-[#9c9b9a] mb-8 font-sans">
                {page?.formSubtext ??
                  "Fill in the form below and we will get back to you within one business day."}
              </p>
              <ContactForm
                services={serviceOptions}
                defaultIso2={iso2}
                countryName={countryName}
              />
            </div>

            <div className="space-y-8">
              {page?.phone &&
                contactRow(
                  Phone,
                  "Phone",
                  <a
                    href={`tel:${page.phone.replace(/\s/g, "")}`}
                    className="hover:text-[#F15C30] transition-colors"
                  >
                    {page.phone}
                  </a>
                )}
              {page?.email &&
                contactRow(
                  Mail,
                  "Email",
                  <a
                    href={`mailto:${page.email}`}
                    className="hover:text-[#F15C30] transition-colors"
                  >
                    {page.email}
                  </a>
                )}
              {page?.address &&
                contactRow(
                  MapPin,
                  "Address",
                  <p className="whitespace-pre-line">{page.address}</p>
                )}
              {page?.officeHours &&
                contactRow(
                  Clock,
                  "Office Hours",
                  <p className="whitespace-pre-line">{page.officeHours}</p>
                )}

              {!page?.phone &&
                !page?.email &&
                !page?.address &&
                !page?.officeHours && (
                  <>
                    {contactRow(Phone, "Phone", <p>{config.phone}</p>)}
                    {contactRow(Mail, "Email", <p>{config.email}</p>)}
                    {contactRow(MapPin, "Address", <p>{config.address}</p>)}
                    {contactRow(
                      Clock,
                      "Office Hours",
                      <p>Monday – Friday, 9 AM – 5 PM</p>
                    )}
                  </>
                )}

              {page?.mapEmbedUrl && (
                <div className="rounded-3xl overflow-hidden border border-[#094d76]/10">
                  <iframe
                    src={page.mapEmbedUrl}
                    width="100%"
                    height="280"
                    style={{ border: 0 }}
                    allowFullScreen
                    loading="lazy"
                    referrerPolicy="no-referrer-when-downgrade"
                    title={`Carelabs ${COUNTRY_NAME} Office Location`}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* CTA SPLIT */}
      <section className="relative">
        <div className="flex flex-col lg:flex-row">
          <div className="flex-1 bg-[#F15C30] py-24 lg:py-32 px-6 lg:px-12 flex items-center justify-center lg:justify-end">
            <h2 className="font-serif font-black text-5xl lg:text-6xl text-white text-center lg:text-right lg:pr-8">
              Need
            </h2>
          </div>
          <div className="flex-1 bg-[#094d76] py-24 lg:py-32 px-6 lg:px-12 flex items-center justify-center lg:justify-start">
            <h2 className="font-serif font-black text-5xl lg:text-6xl text-white text-center lg:text-left lg:pl-8">
              urgent help?
            </h2>
          </div>
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
            <Link
              href={`tel:${config.phone.replace(/\s/g, "")}`}
              className="inline-flex items-center gap-3 bg-white text-[#094d76] font-serif font-bold px-10 py-5 rounded-full shadow-2xl hover:scale-105 transition-transform text-lg"
            >
              <Phone className="w-5 h-5" />
              Call Now
            </Link>
          </div>
        </div>
      </section>

      <SAFooter config={config} />
    </main>
  );
}
