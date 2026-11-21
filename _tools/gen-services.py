#!/usr/bin/env python3
# Builds services/<slug>/index.html for every service in services.py, and sitemap.xml.
import os, sys, json, html
sys.path.insert(0, os.path.dirname(__file__))
from services import SERVICES
from sectors import SECTORS
SEC_LINKS = "".join(f'<a href="/sectors/{x["slug"]}/">{html.escape(x["name"])}</a>' for x in SECTORS)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://b2b.madacare.sa"
e = html.escape

HEADER = """<header class="nav">
  <div class="nav-in">
    <div class="nav-main">
      <a class="logo bx-logo" href="/" aria-label="مدى كير للأعمال"><img class="lg-svg" src="/assets/logo.svg" alt="" width="140" height="40"><span class="bx-biz">للأعمال</span></a>
      <nav class="menu" id="menu" aria-label="القائمة الرئيسية">
        <a href="/#services" aria-current="page">خدماتنا</a>
        <a href="/#why">لماذا مدى كير؟</a>
        <a href="/#how">آلية التعاون</a>
        <a href="/#faq">الأسئلة الشائعة</a>
        <a class="btn btn-primary m-app" href="{quote}">اطلب عرض سعر</a>
      </nav>
    </div>
    <div class="nav-acts">
      <a class="bx-home" href="https://madacare.sa/">موقع مدى كير</a>
      <span class="nav-div" aria-hidden="true"></span>
      <a class="btn btn-primary" href="{quote}"><span>اطلب عرض سعر</span></a>
    </div>
    <button type="button" class="burger" id="burger" aria-label="القائمة" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  </div>
</header>"""

FOOTER = """<footer class="foot">
  <span class="foot-deco" aria-hidden="true"></span>
  <div class="foot-in">
    <div class="foot-cols">
      <div class="fg-brand">
        <span class="logo logo-f" role="img" aria-label="مدى كير"><img class="lg-svg" src="/assets/logo-white.svg" alt="" width="183" height="52" loading="lazy"></span>
        <div class="fg-text">
          <p>رعاية أقرب. اهتمام أكبر. وشراكة تدوم.</p>
          <div class="social">
            <a class="so" data-mail href="mailto:digital@madacare.sa" aria-label="البريد الإلكتروني"><img src="/assets/so-5.svg" alt="" width="20" height="20" loading="lazy"></a>
          </div>
        </div>
        <div class="legal-ids"><p class="li-h">بيانات الشركة</p><p>شركة المستقبل الذكية للخدمات الطبية</p><p>السجل التجاري: 7017170502</p><p>الرقم الضريبي: 310803930400003</p><p>المملكة العربية السعودية</p></div>
      </div>
      <div class="fg-links">
        <div class="fg-grid">
          <div class="fg-col"><p class="fg-label">خدماتنا للشركات</p>{svc_links}</div>
          <div class="fg-col"><p class="fg-label">القطاعات</p>{sec_links}</div>
          <div class="fg-col"><p class="fg-label">مدى كير</p><a href="/#how">آلية التعاون</a><a href="/#quote">اطلب عرض سعر</a><a href="https://madacare.sa/">الرعاية الصحية المنزلية</a><a href="https://madacare.sa/about/">من نحن</a><a href="https://madacare.sa/privacy-policy/">سياسة الخصوصية</a></div>
        </div>
      </div>
    </div>
    <div class="legal">
      <p>مدى كير — نرعاكم كأهلنا · جميع الحقوق محفوظة © 2026</p>
    </div>
  </div>
</footer>

<a class="wa-float" id="waFloat" href="{quote}" aria-label="تواصل معنا على واتساب"><img src="/assets/wa-float.svg" alt="" width="80" height="80" loading="lazy" decoding="async"></a>

<script src="/b2b-config.js"></script>
<script src="/b2b.js"></script>
</body>
</html>
"""

PLUS = '<img class="i-minus" src="/assets/ic-minus.svg" alt="" width="24" height="24"><img class="i-plus" src="/assets/ic-plus.svg" alt="" width="24" height="24">'


def head(title, meta, url, ld):
    s = {"meta": meta}
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(s['meta'])}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="مدى كير للأعمال">
<meta property="og:locale" content="ar_SA">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(s['meta'])}">
<meta property="og:image" content="{SITE}/assets/og-b2b-2.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(s['meta'])}">
<meta name="twitter:image" content="{SITE}/assets/og-b2b-2.jpg">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="/assets/mada-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="/fonts/thmanyahsans-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"></noscript>
<link rel="stylesheet" href="/site.css">
<link rel="stylesheet" href="/b2b.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
"""


def page(s):
    url = f"{SITE}/services/{s['slug']}/"
    quote = f"/?service={s['form']}#quote"
    title = f"{s['title']} | مدى كير للأعمال"
    ld = [
        {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "description": s["meta"], "url": url,
         "serviceType": s["name"], "areaServed": {"@type": "Country", "name": "المملكة العربية السعودية"},
         "audience": {"@type": "BusinessAudience", "name": "الشركات والمنشآت"},
         "provider": {"@type": "MedicalBusiness", "name": "مدى كير للأعمال", "url": SITE + "/"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "مدى كير للأعمال", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "خدماتنا", "item": SITE + "/#services"},
            {"@type": "ListItem", "position": 3, "name": s["name"], "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]]},
    ]
    inc = "\n".join(f'      <li class="sv-item"><span class="sv-tick" aria-hidden="true">✓</span><div><b>{e(t)}</b><p>{e(d)}</p></div></li>' for t, d in s["includes"])
    steps = "\n".join(f'      <li class="bx-step"><span class="bx-dot">{i}</span><b>{e(t)}</b><p>{e(d)}</p></li>' for i, (t, d) in enumerate(s["steps"], 1))
    gains = "\n".join(f'      <div class="sv-gain"><span class="sv-gn">{i:02d}</span><b>{e(t)}</b><p>{e(d)}</p></div>' for i, (t, d) in enumerate(s["gains"], 1))
    fit = "".join(f"<li>{e(x)}</li>" for x in s["fit"])
    faq = "\n".join(
        f'      <div class="qa{" open" if i == 0 else ""}"><button type="button" class="qa-h" aria-expanded="{"true" if i == 0 else "false"}"><span>{e(q)}</span>{PLUS}</button>\n        <div class="qa-b"><p>{e(a)}</p></div></div>'
        for i, (q, a) in enumerate(s["faq"]))
    others = "\n".join(
        f'      <a class="sv-other" href="/services/{o["slug"]}/" style="--ac:{o["ac"]};--bg:{o["bg"]}"><span class="bx-ic">{o["ic"]}</span><b>{e(o["name"])}</b><span class="sv-go" aria-hidden="true">←</span></a>'
        for o in SERVICES if o is not s)
    svc_links = "".join(f'<a href="/services/{o["slug"]}/">{e(o["name"])}</a>' for o in SERVICES)
    intro = "\n".join(f'      <p class="{"p20" if i == 0 else "p16"}">{e(p)}</p>' for i, p in enumerate(s["intro"]))

    return head(title, s["meta"], url, ld) + f"""<body class="sv-page" style="--ac:{s['ac']};--bg:{s['bg']}">
<a class="skip" href="#main">تخطي إلى المحتوى</a>

{HEADER.format(quote=quote)}

<main id="main">

<section class="hero bx-hero sv-hero" id="top">
  <div class="pat pat-10" aria-hidden="true"></div>
  <div class="bx-orb o1" aria-hidden="true"></div><div class="bx-orb o2" aria-hidden="true"></div>
  <div class="wrap bx-hero-in">
    <div class="bx-hero-text">
      <nav class="sv-crumbs bx-up" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">›</span><a href="/#services">خدماتنا</a><span aria-hidden="true">›</span><span aria-current="page">{e(s['name'])}</span></nav>
      <h1 class="display bx-up" style="--d:.12s">{e(s['title'])}</h1>
      <p class="sv-hl bx-up" style="--d:.24s">{e(s['hl'])}</p>
      <p class="bx-sub bx-up" style="--d:.36s">{e(s['lead'])}</p>
      <div class="bx-acts bx-up" style="--d:.48s">
        <a class="btn btn-white bx-cta" href="{quote}"><span>اطلب عرض سعر لهذه الخدمة</span><span class="bx-arr" aria-hidden="true">←</span></a>
        <a class="bx-ghost" href="#includes">ماذا تشمل الخدمة؟</a>
      </div>
    </div>
    <div class="bx-hero-vis sv-vis" aria-hidden="true">
      <div class="bx-core">
        <span class="bx-ring r1"></span><span class="bx-ring r2"></span><span class="bx-ring r3"></span>
        <span class="bx-core-in sv-core"><i>{s['ic']}</i></span>
      </div>
    </div>
  </div>
</section>

<section class="bx-about sv-intro">
  <div class="wrap bx-about-in">
    <div class="bx-about-text rv-up">
      <span class="bx-eyebrow">نظرة على الخدمة</span>
      <h2 class="h2">لماذا تحتاج منشأتك هذه الخدمة؟</h2>
{intro}
    </div>
    <aside class="sv-fit rv-up" style="--d:.15s">
      <b>تناسب بشكل خاص</b>
      <ul>{fit}</ul>
      <a class="btn btn-primary" href="{quote}">اطلب عرض سعر</a>
    </aside>
  </div>
</section>

<section class="tint sv-inc" id="includes">
  <div class="pat pat-02" aria-hidden="true"></div>
  <div class="wrap stack56">
    <div class="sec-head center bx-head rv-up">
      <span class="bx-eyebrow">تفاصيل الخدمة</span>
      <h2 class="h2">ماذا تشمل الخدمة؟</h2>
      <p class="p16 bx-head-p">يُحدد النطاق النهائي للخدمة في الاتفاقية بحسب احتياج منشأتك.</p>
    </div>
    <ul class="sv-items">
{inc}
    </ul>
  </div>
</section>

<section class="bx-how sv-how" id="how">
  <div class="wrap stack56">
    <div class="sec-head center bx-head rv-up">
      <span class="bx-eyebrow">كيف نقدم الخدمة</span>
      <h2 class="h2">أربع خطوات واضحة من الطلب إلى المتابعة</h2>
    </div>
    <ol class="bx-steps" id="steps">
{steps}
    </ol>
  </div>
</section>

<section class="sv-gains">
  <div class="wrap stack56">
    <div class="sec-head center bx-head rv-up">
      <span class="bx-eyebrow light">ماذا تكسب منشأتك</span>
      <h2 class="h2">أثر يلمسه موظفوك… وتلمسه أعمالك</h2>
    </div>
    <div class="sv-gain-grid">
{gains}
    </div>
  </div>
</section>

<section class="faq" id="faq">
  <div class="faq-in">
    <div class="faq-text">
      <h2 class="h2">أسئلة عن {e(s['name'])}</h2>
      <p class="p16">إذا عندك سؤال ما لقيت إجابته هنا، فريقنا جاهز يساعدك.</p>
      <div class="faq-btns"><a class="btn btn-primary" href="{quote}">اطلب عرض سعر</a><a class="btn btn-neutral" data-mail href="mailto:digital@madacare.sa">راسلنا بالإيميل</a></div>
    </div>
    <div class="faq-list">
{faq}
    </div>
  </div>
</section>

<section class="sv-cta">
  <div class="wrap">
    <div class="sv-cta-box rv-up">
      <div>
        <h2>جاهز تبدأ مع {e(s['name'])}؟</h2>
        <p>أرسل لنا طلبك في أقل من دقيقة، ويتواصل معك فريق مدى كير للأعمال بعرض يناسب منشأتك.</p>
      </div>
      <a class="btn btn-white bx-cta" href="{quote}"><span>اطلب عرض سعر</span><span class="bx-arr" aria-hidden="true">←</span></a>
    </div>
  </div>
</section>

<section class="sv-more">
  <div class="wrap stack56">
    <div class="sec-head center bx-head rv-up">
      <span class="bx-eyebrow">خدمات أخرى</span>
      <h2 class="h2">اكتشف بقية خدماتنا للشركات</h2>
    </div>
    <div class="sv-others">
{others}
    </div>
  </div>
</section>

</main>

{FOOTER.format(quote=quote, svc_links=svc_links, sec_links=SEC_LINKS)}"""


def sector_page(x):
    url = f"{SITE}/sectors/{x['slug']}/"
    quote = "/#quote"
    title = f"{x['title']} | مدى كير للأعمال"
    by = {o["slug"]: o for o in SERVICES}
    ld = [
        {"@context": "https://schema.org", "@type": "WebPage", "name": x["title"], "description": x["meta"], "url": url,
         "about": {"@type": "MedicalBusiness", "name": "مدى كير للأعمال", "url": SITE + "/"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "مدى كير للأعمال", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "القطاعات", "item": SITE + "/#sectors"},
            {"@type": "ListItem", "position": 3, "name": x["name"], "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in x["faq"]]},
    ]
    needs = "\n".join(f'      <li class="sv-item"><span class="sv-tick" aria-hidden="true">!</span><div><b>{e(t)}</b><p>{e(d)}</p></div></li>' for t, d in x["needs"])
    svcs = "\n".join(
        f'      <article class="bx-card" style="--ac:{by[k]["ac"]};--bg:{by[k]["bg"]}"><span class="bx-ic">{by[k]["ic"]}</span><h3>{e(by[k]["name"])}</h3><p>{e(why)}</p><a class="bx-more" href="/services/{k}/">اعرف أكثر عن الخدمة <span aria-hidden="true">←</span></a></article>'
        for k, why in x["services"])
    faq = "\n".join(
        f'      <div class="qa{" open" if i == 0 else ""}"><button type="button" class="qa-h" aria-expanded="{"true" if i == 0 else "false"}"><span>{e(q)}</span>{PLUS}</button>\n        <div class="qa-b"><p>{e(a)}</p></div></div>'
        for i, (q, a) in enumerate(x["faq"]))
    others = "\n".join(
        f'      <a class="sv-other" href="/sectors/{o["slug"]}/" style="--ac:{o["ac"]};--bg:{o["bg"]}"><span class="bx-ic">{o["ic"]}</span><b>{e(o["name"])}</b><span class="sv-go" aria-hidden="true">←</span></a>'
        for o in SECTORS if o is not x)
    svc_links = "".join(f'<a href="/services/{o["slug"]}/">{e(o["name"])}</a>' for o in SERVICES)
    return head(title, x["meta"], url, ld) + f"""<body class="sv-page" style="--ac:{x['ac']};--bg:{x['bg']}">
<a class="skip" href="#main">تخطي إلى المحتوى</a>

{HEADER.format(quote=quote)}

<main id="main">

<section class="hero bx-hero sv-hero" id="top">
  <div class="pat pat-10" aria-hidden="true"></div>
  <div class="bx-orb o1" aria-hidden="true"></div><div class="bx-orb o2" aria-hidden="true"></div>
  <div class="wrap bx-hero-in">
    <div class="bx-hero-text">
      <nav class="sv-crumbs bx-up" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">›</span><a href="/#sectors">القطاعات</a><span aria-hidden="true">›</span><span aria-current="page">{e(x['name'])}</span></nav>
      <h1 class="display bx-up" style="--d:.12s">{e(x['title'])}</h1>
      <p class="sv-hl bx-up" style="--d:.24s">{e(x['hl'])}</p>
      <p class="bx-sub bx-up" style="--d:.36s">{e(x['lead'])}</p>
      <div class="bx-acts bx-up" style="--d:.48s">
        <a class="btn btn-white bx-cta" href="{quote}"><span>اطلب عرض سعر لمنشأتك</span><span class="bx-arr" aria-hidden="true">←</span></a>
        <a class="bx-ghost" href="#solutions">الحلول المناسبة لقطاعك</a>
      </div>
    </div>
    <div class="bx-hero-vis sv-vis" aria-hidden="true">
      <div class="bx-core">
        <span class="bx-ring r1"></span><span class="bx-ring r2"></span><span class="bx-ring r3"></span>
        <span class="bx-core-in sv-core"><i>{x['ic']}</i></span>
      </div>
    </div>
  </div>
</section>

<section class="tint sv-inc">
  <div class="pat pat-02" aria-hidden="true"></div>
  <div class="wrap stack56">
    <div class="sec-head center bx-head rv-up">
      <span class="bx-eyebrow">نفهم قطاعك</span>
      <h2 class="h2">تحديات صحية يعرفها {e(x['name'])}</h2>
      <p class="p16 bx-head-p">{e(x['intro'])}</p>
    </div>
    <ul class="sv-items sv-needs">
{needs}
    </ul>
  </div>
</section>

<section class="bx-svc sv-sol" id="solutions">
  <div class="wrap stack56">
    <div class="sec-head center bx-head rv-up">
      <span class="bx-eyebrow">الحلول المناسبة</span>
      <h2 class="h2">خدمات تناسب {e(x['name'])}</h2>
      <p class="p16 bx-head-p">ويمكن جمعها في برنامج واحد مصمم لمنشأتك.</p>
    </div>
    <div class="bx-grid sv-sol-grid">
{svcs}
    </div>
  </div>
</section>

<section class="faq" id="faq">
  <div class="faq-in">
    <div class="faq-text">
      <h2 class="h2">أسئلة من {e(x['name'])}</h2>
      <p class="p16">إذا عندك سؤال ما لقيت إجابته هنا، فريقنا جاهز يساعدك.</p>
      <div class="faq-btns"><a class="btn btn-primary" href="{quote}">اطلب عرض سعر</a><a class="btn btn-neutral" data-mail href="mailto:digital@madacare.sa">راسلنا بالإيميل</a></div>
    </div>
    <div class="faq-list">
{faq}
    </div>
  </div>
</section>

<section class="sv-cta">
  <div class="wrap">
    <div class="sv-cta-box rv-up">
      <div>
        <h2>خلنا نصمم الحل الصحي المناسب لمنشأتك</h2>
        <p>أرسل لنا طلبك في أقل من دقيقة، ويتواصل معك فريق مدى كير للأعمال بعرض يناسب طبيعة عملك.</p>
      </div>
      <a class="btn btn-white bx-cta" href="{quote}"><span>اطلب عرض سعر</span><span class="bx-arr" aria-hidden="true">←</span></a>
    </div>
  </div>
</section>

<section class="sv-more">
  <div class="wrap stack56">
    <div class="sec-head center bx-head rv-up">
      <span class="bx-eyebrow">قطاعات أخرى</span>
      <h2 class="h2">نخدم مختلف القطاعات</h2>
    </div>
    <div class="sv-others">
{others}
    </div>
  </div>
</section>

</main>

{FOOTER.format(quote=quote, svc_links=svc_links, sec_links=SEC_LINKS)}"""


for s in SERVICES:
    d = os.path.join(ROOT, "services", s["slug"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(page(s))

for x in SECTORS:
    d = os.path.join(ROOT, "sectors", x["slug"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(sector_page(x))

urls = [SITE + "/"] + [f"{SITE}/services/{s['slug']}/" for s in SERVICES] + [f"{SITE}/sectors/{x['slug']}/" for x in SECTORS]
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    f.write("".join(f"  <url><loc>{u}</loc></url>\n" for u in urls))
    f.write("</urlset>\n")
print("built", len(SERVICES), "service pages and", len(SECTORS), "sector pages")
