function getStrapiUrl(): string {
  const raw = process.env.NEXT_PUBLIC_STRAPI_URL || "http://localhost:1337";
  if (raw.startsWith("http://") || raw.startsWith("https://")) return raw;
  return `https://${raw}`;
}

const STRAPI_URL = getStrapiUrl();

export interface FaqItem {
  id: number;
  question: string;
  answer: string;
}

export interface ServicePage {
  id: number;
  documentId: string;
  title: string;
  slug: string;
  body: string;
  metaTitle: string;
  metaDescription: string;
  faqs: FaqItem[];
  createdAt: string;
  updatedAt: string;
  publishedAt: string;
}

interface StrapiResponse<T> {
  data: T;
  meta: Record<string, unknown>;
}

export async function getServicePageBySlug(
  slug: string
): Promise<ServicePage | null> {
  const res = await fetch(
    `${STRAPI_URL}/api/service-pages?filters[slug][$eq]=${slug}&populate=faqs`,
    {
      headers: {
        Authorization: `Bearer ${process.env.STRAPI_API_TOKEN}`,
      },
      next: { revalidate: 60 },
    }
  );

  if (!res.ok) return null;

  const json: StrapiResponse<ServicePage[]> = await res.json();

  if (!json.data || json.data.length === 0) return null;

  return json.data[0];
}
