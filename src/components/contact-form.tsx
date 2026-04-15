"use client";

import { useState } from "react";
import { CheckCircle, Loader2 } from "lucide-react";
import { ALL_COUNTRIES, getCountryByIso2 } from "@/lib/all-countries";

interface ContactFormProps {
  services: { title: string; slug: string }[];
  defaultIso2: string;
  countryName: string;
}

const HEAR_ABOUT_OPTIONS = [
  "Google Search",
  "LinkedIn",
  "Referral",
  "Industry Event",
  "Trade Publication",
  "Word of Mouth",
  "Other",
];

export function ContactForm({
  services,
  defaultIso2,
}: ContactFormProps) {
  const defaultCountry = getCountryByIso2(defaultIso2);
  const [selectedDialCode, setSelectedDialCode] = useState(
    defaultCountry.dialCode
  );
  const [status, setStatus] = useState<"idle" | "submitting" | "submitted">(
    "idle"
  );

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("submitting");
    // Visual-only submit — simulate async
    await new Promise((resolve) => setTimeout(resolve, 800));
    setStatus("submitted");
  }

  if (status === "submitted") {
    return (
      <div className="bg-green-50 border border-green-200 rounded-2xl p-10 text-center">
        <div className="flex justify-center mb-4">
          <CheckCircle className="w-16 h-16 text-green-500" />
        </div>
        <h3 className="text-2xl font-bold text-[#1A2538] mb-2">
          Message Sent Successfully!
        </h3>
        <p className="text-[#374151]">
          Thank you for reaching out. Our team will contact you within 24
          hours.
        </p>
      </div>
    );
  }

  const inputClass =
    "w-full bg-white border border-slate-200 rounded-xl px-4 h-[50px] focus:border-[#0050B3] focus:ring-2 focus:ring-[#0050B3]/20 outline-none transition-all text-[#1A2538] placeholder-slate-400 text-sm";
  const labelClass =
    "text-sm font-semibold text-[#1A2538] mb-2 block";

  return (
    <form
      onSubmit={handleSubmit}
      className="grid grid-cols-1 md:grid-cols-2 gap-6"
    >
      {/* Full Name */}
      <div>
        <label htmlFor="name" className={labelClass}>
          Full Name <span className="text-red-500">*</span>
        </label>
        <input
          id="name"
          name="name"
          type="text"
          required
          placeholder="Jane Smith"
          className={inputClass}
        />
      </div>

      {/* Company Name */}
      <div>
        <label htmlFor="company" className={labelClass}>
          Company Name
        </label>
        <input
          id="company"
          name="company"
          type="text"
          placeholder="Acme Corp"
          className={inputClass}
        />
      </div>

      {/* Email */}
      <div>
        <label htmlFor="email" className={labelClass}>
          Email Address <span className="text-red-500">*</span>
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          placeholder="jane@company.com"
          className={inputClass}
        />
      </div>

      {/* Phone Number */}
      <div>
        <label htmlFor="phone" className={labelClass}>
          Phone Number
        </label>
        <div className="flex">
          <select
            aria-label="Country dial code"
            value={selectedDialCode}
            onChange={(e) => setSelectedDialCode(e.target.value)}
            className="min-w-[130px] bg-white border border-slate-200 border-r-0 rounded-l-xl h-[50px] px-3 text-[#1A2538] focus:outline-none focus:border-[#0050B3] cursor-pointer text-sm"
          >
            {ALL_COUNTRIES.map((c) => (
              <option key={c.iso2} value={c.dialCode}>
                {c.flag} {c.dialCode}
              </option>
            ))}
          </select>
          <input
            id="phone"
            name="phone"
            type="tel"
            placeholder="(555) 000-0000"
            className="bg-white border border-slate-200 rounded-r-xl px-4 h-[50px] flex-1 focus:border-[#0050B3] focus:ring-2 focus:ring-[#0050B3]/20 outline-none text-[#1A2538] placeholder-slate-400 text-sm transition-all"
          />
        </div>
      </div>

      {/* Service */}
      <div className="md:col-span-2">
        <label htmlFor="service" className={labelClass}>
          Service of Interest
        </label>
        <select
          id="service"
          name="service"
          defaultValue=""
          className={`${inputClass} cursor-pointer`}
        >
          <option value="" disabled>
            Select a service...
          </option>
          {services.map((s) => (
            <option key={s.slug} value={s.slug}>
              {s.title}
            </option>
          ))}
          <option value="other">Other / General Enquiry</option>
        </select>
      </div>

      {/* Message */}
      <div className="md:col-span-2">
        <label htmlFor="message" className={labelClass}>
          Message <span className="text-red-500">*</span>
        </label>
        <textarea
          id="message"
          name="message"
          required
          placeholder="Tell us about your project or requirements..."
          className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 min-h-[140px] focus:border-[#0050B3] focus:ring-2 focus:ring-[#0050B3]/20 outline-none transition-all text-[#1A2538] placeholder-slate-400 text-sm resize-y"
        />
      </div>

      {/* How did you hear */}
      <div className="md:col-span-2">
        <label htmlFor="referral" className={labelClass}>
          How did you hear about us?
        </label>
        <select
          id="referral"
          name="referral"
          defaultValue=""
          className={`${inputClass} cursor-pointer`}
        >
          <option value="" disabled>
            Please select...
          </option>
          {HEAR_ABOUT_OPTIONS.map((opt) => (
            <option key={opt} value={opt}>
              {opt}
            </option>
          ))}
        </select>
      </div>

      {/* Submit */}
      <div className="md:col-span-2">
        <button
          type="submit"
          disabled={status === "submitting"}
          className="w-full bg-[#FF6633] text-white rounded-[50px] h-[50px] font-semibold hover:bg-[#e55729] transition-all shadow-sm disabled:opacity-60 disabled:cursor-not-allowed inline-flex items-center justify-center gap-2"
        >
          {status === "submitting" ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Sending...
            </>
          ) : (
            <>Send Message →</>
          )}
        </button>
      </div>
    </form>
  );
}
