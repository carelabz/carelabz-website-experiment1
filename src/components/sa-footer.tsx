import Image from "next/image";
import Link from "next/link";
import type { CountryConfig } from "@/lib/countries-config";

interface SAFooterProps {
  config: CountryConfig;
  phone?: string | null;
  email?: string | null;
  address?: string | null;
  description?: string | null;
}

export function SAFooter({
  config,
  phone,
  email,
  address,
  description,
}: SAFooterProps) {
  const resolvedPhone = phone ?? config.phone;
  const resolvedEmail = email ?? config.email;
  const resolvedAddress = address ?? config.address;
  const resolvedDescription = description ?? config.footerDescription;

  const companyLinks = [
    { label: "About Us", href: config.aboutPath },
    ...(config.caseStudyPath
      ? [{ label: "Case Studies", href: config.caseStudyPath }]
      : []),
    { label: "Blog", href: config.blogIndexPath },
    { label: "Contact", href: config.contactPath },
  ];

  return (
    <footer className="bg-[#094d76] relative overflow-hidden">
      <div className="absolute bottom-0 left-0 right-0 pointer-events-none select-none overflow-hidden">
        <span
          className="font-serif font-black text-[20vw] text-white/5 leading-none whitespace-nowrap block -mb-[5vw]"
          aria-hidden="true"
        >
          CARELABS
        </span>
      </div>

      <div className="relative max-w-[1400px] mx-auto px-6 lg:px-12 py-20 lg:py-28">
        <div className="grid lg:grid-cols-4 gap-12 lg:gap-8">
          <div>
            <Link
              href={`/${config.cc}/`}
              className="inline-block mb-6"
              aria-label={`Carelabs ${config.countryName} home`}
            >
              <Image
                src="/images/logo/carelabs-logo.svg"
                alt="Carelabs"
                width={866}
                height={288}
                className="h-10 w-auto"
                style={{ filter: "brightness(0) invert(1)" }}
              />
            </Link>
            <p className="text-white/60 text-sm leading-relaxed font-sans max-w-xs">
              {resolvedDescription}
            </p>
          </div>

          <div>
            <h4 className="font-serif font-bold text-[#F15C30] text-sm uppercase tracking-widest mb-6">
              Services
            </h4>
            <ul className="space-y-3">
              {config.services.map((s) => (
                <li key={s.href}>
                  <Link
                    href={s.href}
                    className="text-white/70 hover:text-white transition-colors text-sm font-sans"
                  >
                    {s.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-serif font-bold text-[#F15C30] text-sm uppercase tracking-widest mb-6">
              Company
            </h4>
            <ul className="space-y-3">
              {companyLinks.map((c) => (
                <li key={c.href}>
                  <Link
                    href={c.href}
                    className="text-white/70 hover:text-white transition-colors text-sm font-sans"
                  >
                    {c.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-serif font-bold text-[#F15C30] text-sm uppercase tracking-widest mb-6">
              Contact
            </h4>
            <ul className="space-y-3">
              <li>
                <a
                  href={`mailto:${resolvedEmail}`}
                  className="text-white/70 hover:text-white transition-colors text-sm font-sans"
                >
                  {resolvedEmail}
                </a>
              </li>
              <li>
                <a
                  href={`tel:${resolvedPhone.replace(/\s/g, "")}`}
                  className="text-white/70 hover:text-white transition-colors text-sm font-sans"
                >
                  {resolvedPhone}
                </a>
              </li>
              <li>
                <span className="text-white/70 text-sm font-sans whitespace-pre-line">
                  {resolvedAddress}
                </span>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-16 pt-8 border-t border-white/10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <p className="text-white/50 text-sm font-sans">
            © {new Date().getFullYear()} Carelabs {config.countryName}. All
            rights reserved.
          </p>
          <div className="flex gap-6">
            <Link
              href="/privacy/"
              className="text-white/50 hover:text-white text-sm transition-colors font-sans"
            >
              Privacy Policy
            </Link>
            <Link
              href="/terms/"
              className="text-white/50 hover:text-white text-sm transition-colors font-sans"
            >
              Terms of Service
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
