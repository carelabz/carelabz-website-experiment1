"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Menu, X, ChevronDown } from "lucide-react";
import type { CountryConfig } from "@/lib/countries-config";

interface SANavbarProps {
  config: CountryConfig;
}

export function SANavbar({ config }: SANavbarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [servicesOpen, setServicesOpen] = useState(false);

  const navLinks = [
    { name: "About", href: config.aboutPath },
    { name: "Industries", href: `/${config.cc}/#industries` },
    { name: "Insights", href: config.blogIndexPath },
  ];

  return (
    <nav className="bg-white py-4 border-b border-[#094d76]/5">
      <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
        <div className="flex items-center justify-between">
          <Link
            href={`/${config.cc}/`}
            aria-label={`Carelabs ${config.countryName} home`}
          >
            <Image
              src="/images/logo/carelabs-logo.svg"
              alt="Carelabs"
              width={866}
              height={288}
              priority
              className="h-10 w-auto"
            />
          </Link>

          <div className="hidden lg:flex items-center gap-10">
            <div
              className="relative"
              onMouseEnter={() => setServicesOpen(true)}
              onMouseLeave={() => setServicesOpen(false)}
            >
              <button
                type="button"
                className="text-[#094d76] font-serif font-semibold text-sm hover:text-[#F15C30] transition-colors inline-flex items-center gap-1"
                aria-expanded={servicesOpen}
                aria-haspopup="true"
              >
                Services
                <ChevronDown
                  className={`w-4 h-4 transition-transform ${
                    servicesOpen ? "rotate-180" : ""
                  }`}
                />
              </button>

              {servicesOpen && (
                <div className="absolute left-1/2 -translate-x-1/2 top-full pt-3 z-50">
                  <div className="bg-white rounded-2xl shadow-xl border border-[#094d76]/10 p-4 min-w-[320px]">
                    <ul className="grid gap-1">
                      {config.services.map((s) => (
                        <li key={s.href}>
                          <Link
                            href={s.href}
                            className="block px-3 py-2.5 rounded-xl text-sm font-medium text-[#094d76] hover:bg-[#e8f4fd] hover:text-[#2575B6] transition-colors font-sans"
                          >
                            {s.label}
                          </Link>
                        </li>
                      ))}
                    </ul>
                    <div className="border-t border-[#094d76]/10 mt-3 pt-3">
                      <Link
                        href={config.servicesIndexPath}
                        className="flex items-center justify-between px-3 py-2 text-sm font-serif font-semibold text-[#F15C30] hover:text-[#2575B6] transition-colors"
                      >
                        View All Services →
                      </Link>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {navLinks.map((link) => (
              <Link
                key={link.name}
                href={link.href}
                className="text-[#094d76] font-serif font-semibold text-sm hover:text-[#F15C30] transition-colors"
              >
                {link.name}
              </Link>
            ))}
          </div>

          <div className="hidden lg:block">
            <Link
              href={config.contactPath}
              className="inline-flex items-center gap-2 bg-[#F15C30] text-white font-sans font-semibold px-6 py-3 rounded-full hover:bg-[#c44a1f] transition-colors"
            >
              Get a Quote
            </Link>
          </div>

          <button
            type="button"
            className="lg:hidden p-2 text-[#094d76]"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? (
              <X className="w-6 h-6" />
            ) : (
              <Menu className="w-6 h-6" />
            )}
          </button>
        </div>
      </div>

      {mobileMenuOpen && (
        <div className="lg:hidden bg-white border-t border-[#094d76]/10 mt-4 py-6">
          <div className="max-w-[1400px] mx-auto px-6 space-y-2">
            <div className="py-2">
              <p className="text-[#094d76]/60 font-serif text-xs uppercase tracking-widest mb-3">
                Services
              </p>
              <ul className="space-y-2">
                {config.services.map((s) => (
                  <li key={s.href}>
                    <Link
                      href={s.href}
                      className="block text-[#094d76] font-sans font-medium py-1.5"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      {s.label}
                    </Link>
                  </li>
                ))}
                <li>
                  <Link
                    href={config.servicesIndexPath}
                    className="block text-[#F15C30] font-serif font-semibold py-1.5"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    View All Services →
                  </Link>
                </li>
              </ul>
            </div>
            {navLinks.map((link) => (
              <Link
                key={link.name}
                href={link.href}
                className="block text-[#094d76] font-serif font-semibold py-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                {link.name}
              </Link>
            ))}
            <Link
              href={config.contactPath}
              className="inline-flex items-center gap-2 bg-[#F15C30] text-white font-sans font-semibold px-6 py-3 rounded-full w-full justify-center mt-4"
              onClick={() => setMobileMenuOpen(false)}
            >
              Get a Quote
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}
