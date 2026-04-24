"""Clone redesigned BR pages to CO/CL/AR/PE.

New BR files are parametric: CC / COUNTRY_NAME / HREFLANG are defined as
top-level consts and the rest of the file uses template literals +
`${COUNTRY_CONFIGS[CC]}` lookups. Almost all tokens follow from those 3 consts,
so the clone is small.
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BR_DIR = os.path.join(ROOT, "src", "app", "br")

COUNTRIES = {
    "co": {
        "name": "Colombia",
        "upper": "CO",
        "hreflang": "en-CO",
    },
    "cl": {
        "name": "Chile",
        "upper": "CL",
        "hreflang": "en-CL",
    },
    "ar": {
        "name": "Argentina",
        "upper": "AR",
        "hreflang": "en-AR",
    },
    "pe": {
        "name": "Peru",
        "upper": "PE",
        "hreflang": "en-PE",
    },
}


def transform(text: str, cc: str) -> str:
    c = COUNTRIES[cc]
    name = c["name"]
    upper = c["upper"]
    hreflang = c["hreflang"]

    subs = [
        # Top-level consts (the only literal refs to "br"/"Brazil"/"en-BR")
        (r'const CC = "br";', f'const CC = "{cc}";'),
        (r'const COUNTRY_NAME = "Brazil";', f'const COUNTRY_NAME = "{name}";'),
        (r'const HREFLANG = "en-BR";', f'const HREFLANG = "{hreflang}";'),
        # Function names
        (r"\bBRHomePage\b", f"{upper}HomePage"),
        (r"\bBRServicesIndexPage\b", f"{upper}ServicesIndexPage"),
        (r"\bBRBlogIndexPage\b", f"{upper}BlogIndexPage"),
        (r"\bBRAboutPage\b", f"{upper}AboutPage"),
        (r"\bBRContactPage\b", f"{upper}ContactPage"),
    ]

    out = text
    for pat, rep in subs:
        out = re.sub(pat, rep, out)
    return out


FILES = [
    "page.tsx",
    "services/page.tsx",
    "blogs/page.tsx",
    "about-us/page.tsx",
    "contact-us/page.tsx",
    "[slug]/page.tsx",
]


def clone():
    for cc in COUNTRIES:
        dest_base = os.path.join(ROOT, "src", "app", cc)
        for rel in FILES:
            src = os.path.join(BR_DIR, rel)
            dst = os.path.join(dest_base, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            out = transform(content, cc)
            with open(dst, "w", encoding="utf-8", newline="\n") as f:
                f.write(out)
            print(f"[{cc}] wrote {rel}")


if __name__ == "__main__":
    clone()
    print("\nDone.")
