"""One-off: upload 4 missing services for MY + VN + backfill blog meta_desc pass 2."""
import os, json, re, copy, urllib.request, urllib.error

STRAPI = "https://rational-cheese-8e8c4f80ea.strapiapp.com"
TOKEN = ""
with open('.env.local', encoding='utf-8') as f:
    for line in f:
        if line.startswith('STRAPI_API_TOKEN='):
            TOKEN = line.split('=', 1)[1].strip().strip('"').strip("'")


def http(method, path, body=None):
    req_body = json.dumps({"data": body}).encode() if body else None
    headers = {"Authorization": f"Bearer {TOKEN}"}
    if req_body: headers["Content-Type"] = "application/json"
    req = urllib.request.Request(STRAPI + path, data=req_body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode('utf-8','replace')[:200]}"}


STRIP_TOP = {"id","documentId","createdAt","updatedAt","publishedAt","locale","localizations"}
def strip_meta(o):
    if isinstance(o, dict): return {k: strip_meta(v) for k,v in o.items() if k not in STRIP_TOP}
    if isinstance(o, list): return [strip_meta(i) for i in o]
    return o
def strip_ids(o):
    if isinstance(o, dict): return {k: strip_ids(v) for k,v in o.items() if k != "id"}
    if isinstance(o, list): return [strip_ids(i) for i in o]
    return o


COUNTRY_LOC = {
    'my': {'name': 'Malaysia', 'primary': 'MS IEC 60364', 'auth': 'DOSH',
           'phone': '+60 0 0000 0000', 'address': 'Kuala Lumpur, Malaysia',
           'localize': [
               (r'\bNFPA 70E\b', 'MS IEC 60364'),
               (r'\bOSHA\b', 'DOSH'),
               (r'\bNEC\b', 'MS IEC 60364'),
               (r'\b(USA|U\.S\.|United States)\b', 'Malaysia'),
               (r'\bAmerican\b', 'Malaysian'),
               (r'\bHouston, TX\b', 'Kuala Lumpur'),
               (r'\ben-US\b', 'en-MY'),
           ]},
    'vn': {'name': 'Vietnam', 'primary': 'TCVN 7447', 'auth': 'DOLISA',
           'phone': '+84 00 0000 0000', 'address': 'Ho Chi Minh City, Vietnam',
           'localize': [
               (r'\bNFPA 70E\b', 'TCVN 7447'),
               (r'\bOSHA\b', 'DOLISA'),
               (r'\bNEC\b', 'TCVN 7447'),
               (r'\b(USA|U\.S\.|United States)\b', 'Vietnam'),
               (r'\bAmerican\b', 'Vietnamese'),
               (r'\bHouston, TX\b', 'Ho Chi Minh City'),
               (r'\ben-US\b', 'en-VN'),
           ]},
}


def localize_recursive(obj, patterns):
    if isinstance(obj, str):
        out = obj
        for pat, rep in patterns:
            out = re.sub(pat, rep, out)
        out = re.sub(r'\bCare\s+Labs\b', 'Carelabs', out)
        out = re.sub(r'\bCareLabs\b', 'Carelabs', out)
        return out
    if isinstance(obj, dict): return {k: localize_recursive(v, patterns) for k, v in obj.items()}
    if isinstance(obj, list): return [localize_recursive(i, patterns) for i in obj]
    return obj


def rewrite_hrefs(obj, cc):
    if isinstance(obj, str):
        s = re.sub(r'/us/services/[^/]+/([^/]+)/', f'/{cc}/' + r'\1/', obj)
        s = re.sub(r'/us/blog/([^/]+)/', f'/{cc}/' + r'\1/', s)
        s = re.sub(r'/us/', f'/{cc}/', s)
        return s
    if isinstance(obj, dict): return {k: rewrite_hrefs(v, cc) for k, v in obj.items()}
    if isinstance(obj, list): return [rewrite_hrefs(i, cc) for i in obj]
    return obj


MISSING_SERVICES = ['arc-flash-study', 'short-circuit-analysis', 'load-flow-analysis', 'relay-coordination-study']

print("=== Uploading missing MY + VN services ===")
for cc in ['my', 'vn']:
    loc = COUNTRY_LOC[cc]
    for base in MISSING_SERVICES:
        r = http('GET', f'/api/service-pages?filters[slug][$eq]={base}-{cc}')
        if r.get('data'):
            print(f'  [{cc}] {base}-{cc} exists')
            continue
        ref_path = f'data/strapi-refs/{base}-us.json'
        if not os.path.exists(ref_path):
            print(f'  [{cc}] NO TEMPLATE for {base}')
            continue
        with open(ref_path, encoding='utf-8') as f:
            tmpl = json.load(f).get('data', [])
        if not tmpl:
            continue
        tmpl = tmpl[0]
        payload = strip_meta(copy.deepcopy(tmpl))
        payload = localize_recursive(payload, loc['localize'])
        payload = rewrite_hrefs(payload, cc)
        payload['region'] = cc
        payload['slug'] = f'{base}-{cc}'
        payload['ctaPrimaryHref'] = f'/{cc}/contact-us/'
        payload['ctaSecondaryHref'] = f'/{cc}/our-services/'
        payload['ctaBannerPrimaryHref'] = f'/{cc}/contact-us/'
        payload['ctaBannerSecondaryHref'] = f'/{cc}/our-services/'
        payload['footerPhone'] = loc['phone']
        payload['footerAddress'] = loc['address']
        kw = list(payload.get('seoKeywords') or [])
        for k in (loc['primary'], 'IEEE 1584', 'IEC 60909', 'ETAP', f"Carelabs {loc['name']}"):
            if k not in kw: kw.append(k)
        payload['seoKeywords'] = kw
        payload = strip_ids(payload)
        r = http('POST', '/api/service-pages', payload)
        ok = 'error' not in r
        print(f'  [{cc}] {"OK" if ok else "ERR"} {base}-{cc}' + ('' if ok else f' :: {r["error"][:100]}'))

print()
print("=== Meta_desc backfill pass 2 ===")
CNAME = {'my': 'Malaysia', 'vn': 'Vietnam', 'cz': 'Czech Republic', 'de': 'Germany',
         'jp': 'Japan', 'ro': 'Romania', 'sk': 'Slovakia', 'ua': 'Ukraine',
         'za': 'South Africa', 'nz': 'New Zealand', 'th': 'Thailand',
         'us': 'USA', 'ca': 'Canada'}

page = 1
ok = skip = fail = 0
while True:
    r = http('GET', f'/api/blog-posts?pagination[page]={page}&pagination[pageSize]=100&populate=*')
    entries = r.get('data', [])
    if not entries:
        break
    for e in entries:
        md = e.get('metaDescription') or ''
        if md and len(md) >= 30:
            skip += 1
            continue
        excerpt = e.get('excerpt') or ''
        body = e.get('body') or ''
        title = e.get('title') or ''
        cc = (e.get('region') or '').lower()
        cname = CNAME.get(cc, cc.upper())
        src = excerpt if len(excerpt) > 30 else body[:300]
        new_md = re.sub(r'\s+', ' ', src).strip()[:160] if src else ''
        if len(new_md) < 30:
            new_md = (title + ' - Carelabs ' + cname +
                      ' insights on electrical safety, arc flash analysis, and power system engineering.')[:160]
        payload = {k: v for k, v in e.items() if k not in STRIP_TOP}
        payload['metaDescription'] = new_md
        payload = strip_ids(payload)
        r2 = http('PUT', f'/api/blog-posts/{e["documentId"]}', payload)
        if 'error' in r2:
            fail += 1
        else:
            ok += 1
    if len(entries) < 100:
        break
    page += 1

print(f'meta_desc pass 2: {ok} updated, {skip} already had meta, {fail} failed')
