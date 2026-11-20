# Builds the service pages (/home-nursing/, /home-lab/, ...) from index.html's header, footer and booking form.
# Run from the repo root after changing index.html's header/footer or the texts below:  python3 tools/build_service_pages.py
# Texts only repeat what the home page says about each service; a doctor reviews them before publishing.
import json, re

SITE = "https://madacare.sa"
src = open("index.html", encoding="utf-8").read()


def between(a, b):
    i = src.index(a)
    return src[i:src.index(b, i) + len(b)]


def fix(s):
    s = s.replace('src="assets/', 'src="/assets/').replace('href="#top"', 'href="/"')
    for k in ("about", "services", "blog", "download"):
        s = s.replace(f'href="#{k}"', f'href="/#{k}"')
    return s


GTM_HEAD = between("<!-- Google Tag Manager (standard snippet) -->", "<!-- End Google Tag Manager -->")
GTM_BODY = between("<!-- Google Tag Manager (noscript) -->", "<!-- End Google Tag Manager (noscript) -->")
SNAV = fix(between("<!-- Second Nav Header (DGA) -->", "</div>\n</div>\n"))
HEADER = fix(between("<!-- Nav Header -->", "</header>")).replace(' aria-current="page"', "")
FOOTER = fix(between("<!-- Footer -->", "</footer>"))
WA = fix(between('<a class="wa-float"', "</a>"))
BOOK = fix(between("<!-- Booking request (sent to the dashboard) -->", "</div>\n  </div>\n</div>"))

FAQ_STAFF = ("كيف أضمن كفاءة الفريق الطبي القادم لمنزلي؟", "جميع كوادرنا الطبية من أطباء وممرضين وفنيين مرخصين ومعتمدين من الهيئة السعودية للتخصصات الصحية، ويخضعون لتدريب مستمر على الجانب الطبي وعلى فن التعامل الإنساني، لتكون الزيارة مريحة وآمنة لأحبتكم.")
FAQ_AREA = ("هل الخدمة متوفرة في كل أحياء جدة؟", "نقدم خدماتنا داخل مدينة جدة. اترك عنوانك أو حيّك في ملاحظات الطلب، وسيؤكد لك فريقنا الموعد المناسب.")
FAQ_RELATIVE = ("هل أستطيع الحجز لأحد والديّ أو قريب لي؟", "نعم، يمكنك الحجز باسمك ورقم جوالك عن قريبك، واكتب في الملاحظات اسم المريض وحالته باختصار.")


def faq_book(cta):
    return ("كيف أحجز؟", f"اضغط «{cta}» واترك اسمك ورقم جوالك، وسيتواصل معك فريقنا لتأكيد الموعد. ويمكنك أيضاً الحجز من تطبيق مدى كير.")


SERVICES = [
    dict(slug="home-doctor", svc="doctor", short="زيارة طبيب منزلية", h1="زيارة طبيب منزلية في جدة",
         title="طبيب منزلي في جدة | زيارة طبيب منزلية من مدى كير",
         desc="زيارة طبيب منزلية في جدة: كشف وتقييم الحالة وتشخيصها ومتابعتها داخل منزلك بأطباء مرخصين. احجز زيارة طبيب مع مدى كير بخطوات بسيطة.",
         schema_desc="رعاية طبية احترافية داخل منزلكم لتقييم الحالة وتشخيصها ومتابعتها.", stype="زيارة طبيب منزلية",
         lead="طبيب مرخص يزوركم في البيت لتقييم الحالة وتشخيصها ومتابعتها، بدل تعب المشاوير والانتظار في العيادات، وفي بيئة مريحة تحافظ على خصوصية المريض.",
         cta="احجز زيارة طبيب", inc_h="كشف طبي متكامل في بيتك",
         inc_p="يزوركم طبيب مرخص في الموعد اللي يناسبكم، ويفحص المريض ويقيّم حالته داخل منزله بكل احترام وخصوصية.",
         inc=[("كشف منزلي", "فحص المريض وتقييم حالته داخل المنزل."), ("التشخيص", "تشخيص الحالة على يد أطباء متخصصين."), ("المتابعة", "متابعة تطورات الحالة والتواصل معكم بعد الزيارة.")],
         who=[("كبار السن", "كشف في البيت يحفظ راحتهم بدون تعب المشاوير والانتظار."), ("من يصعب عليه التنقل", "الطبيب يوصل للمريض بدل ما يتنقل هو."), ("العائلات", "كشف لأفراد العائلة في بيتهم وفي وقت يناسبهم.")],
         faq_extra=[("هل يتابع الطبيب الحالة بعد الزيارة؟", "نعم، رعايتنا لا تنتهي بمغادرة المنزل؛ نلتزم بالتواصل معكم لمتابعة تطورات الحالة الصحية.")]),
    dict(slug="home-nursing", svc="nursing", short="التمريض المنزلي", h1="التمريض المنزلي في جدة",
         title="تمريض منزلي في جدة | مدى كير للرعاية الصحية المنزلية",
         desc="تمريض منزلي في جدة بطاقم مرخص: إعطاء الأدوية، غيار الجروح ورعاية يومية في بيتك. احجز ممرض منزلي مع مدى كير بخطوات بسيطة.",
         schema_desc="تمريض منزلي متكامل: إعطاء الأدوية، غيار الجروح، متابعة ورعاية يومية شاملة.", stype="تمريض منزلي",
         lead="ممرضون مرخصون يصلون إلى بيتك لإعطاء الأدوية، وغيار الجروح، والمتابعة والرعاية اليومية، في بيئة مريحة تحافظ على خصوصية المريض وتعفيه من عناء المستشفيات.",
         cta="احجز ممرض الآن", inc_h="رعاية تمريضية متكاملة في بيتك",
         inc_p="يزوركم ممرض مرخص ومدرّب في الموعد اللي يناسبكم، ويقدّم الرعاية اللي يحتاجها المريض داخل منزله بكل احترام وخصوصية.",
         inc=[("إعطاء الأدوية", "إعطاء الأدوية الموصوفة للمريض في مواعيدها داخل المنزل."), ("غيار الجروح", "تغيير ضمادات الجروح والعناية بها بطريقة آمنة ونظيفة."), ("متابعة ورعاية يومية", "زيارات منتظمة لمتابعة حالة المريض والاطمئنان على استقرارها.")],
         who=[("كبار السن", "رعاية تحفظ راحتهم وكرامتهم بدون تعب المشاوير والانتظار."), ("بعد الخروج من المستشفى", "استكمال الرعاية في البيت بين أهله."), ("من يصعب عليه التنقل", "ممرض يوصل للمريض بدل ما يتنقل هو.")],
         faq_extra=[("هل يمكن حجز رعاية تمريضية يومية؟", "نعم، نوفر متابعة ورعاية يومية حسب حالة المريض. اكتب احتياجك في ملاحظات الطلب، وسيتواصل معك فريقنا لترتيب الزيارات.")]),
    dict(slug="home-lab", svc="blood", short="المختبر المنزلي", h1="المختبر المنزلي في جدة: تحاليل في بيتك",
         title="تحاليل منزلية في جدة | المختبر المنزلي من مدى كير",
         desc="تحاليل منزلية في جدة: سحب العينات والتحاليل المخبرية داخل منزلك بسهولة وخصوصية، واستلام النتائج أونلاين. احجز مع مدى كير.",
         schema_desc="سحب العينات والتحاليل المخبرية داخل المنزل بسهولة وخصوصية واستلام النتائج أونلاين.", stype="تحاليل مخبرية منزلية",
         lead="نسحب العينات في بيتك ونجري التحاليل المخبرية بسهولة وخصوصية، وتستلم النتائج أونلاين بدون زحمة المختبرات والانتظار.",
         cta="احجز تحليل منزلي", inc_h="مختبر كامل يوصل لباب بيتك",
         inc_p="يزوركم فني مرخص في الموعد اللي يناسبكم لسحب العينات، وتوصلكم النتائج أونلاين.",
         inc=[("سحب العينات في المنزل", "سحب العينات داخل البيت بكل خصوصية وراحة."), ("التحاليل المخبرية", "تحليل العينات بدقة عالية."), ("النتائج أونلاين", "استلام نتائج التحاليل أونلاين بدون مشوار.")],
         who=[("كبار السن", "تحاليل في البيت بدون تعب المشاوير والانتظار."), ("التحاليل الدورية", "لمن يحتاج متابعة تحاليله بشكل منتظم."), ("من وقته ضيق", "تحاليل في بيتك وفي الوقت اللي يناسبك.")],
         faq_extra=[("كيف أستلم نتائج التحاليل؟", "تستلم نتائج تحاليلك أونلاين، بدون ما تحتاج تروح للمختبر.")]),
    dict(slug="iv-therapy", svc="iv", short="الفيتامينات الوريدية", h1="الفيتامينات الوريدية (IV Therapy) في جدة",
         title="فيتامينات وريدية في جدة | IV Therapy في بيتك من مدى كير",
         desc="جلسات فيتامينات وريدية (IV Therapy) في جدة داخل منزلك، بكادر طبي مرخص ومعتمد. احجز جلستك مع مدى كير بخطوات بسيطة.",
         schema_desc="جلسات فيتامينات وريدية لدعم الصحة العامة داخل المنزل.", stype="فيتامينات وريدية",
         lead="جلسات فيتامينات وريدية في بيتك يقدّمها كادر طبي مرخص ومعتمد، في بيئة مريحة وهادئة بدل الذهاب للعيادة.",
         cta="احجز جلسة", inc_h="جلستك في بيتك وبكل راحة",
         inc_p="يزوركم كادر طبي مرخص في الموعد اللي يناسبكم لتقديم الجلسة داخل منزلكم.",
         inc=[("جلسات في المنزل", "جلسة الفيتامينات الوريدية في بيتك بدل الذهاب للعيادة."), ("كادر طبي مرخص", "يقدّم الجلسة كادر مرخص ومعتمد."), ("متابعة بعد الجلسة", "نتواصل معكم بعد الجلسة للاطمئنان.")],
         who=None,
         faq_extra=[]),
    dict(slug="home-physiotherapy", svc="physio", short="العلاج الطبيعي المنزلي", h1="العلاج الطبيعي المنزلي في جدة",
         title="علاج طبيعي منزلي في جدة | مدى كير للرعاية الصحية المنزلية",
         desc="علاج طبيعي منزلي في جدة: جلسات علاج طبيعي داخل منزلك بأخصائيين مرخصين. احجز جلستك مع مدى كير بخطوات بسيطة.",
         schema_desc="جلسات علاج طبيعي داخل المنزل بأخصائيين مرخصين.", stype="علاج طبيعي منزلي",
         lead="جلسات علاج طبيعي في بيتك مع أخصائيين مرخصين، بدون تعب المشاوير، وفي بيئة مريحة تساعد المريض يلتزم بجلساته.",
         cta="احجز جلسة علاج طبيعي", inc_h="جلسات العلاج الطبيعي في بيتك",
         inc_p="يزوركم أخصائي علاج طبيعي مرخص في الموعد اللي يناسبكم، ويقدّم الجلسة داخل منزلكم.",
         inc=[("جلسات في المنزل", "جلسة العلاج الطبيعي في بيتك بدل الذهاب للمركز."), ("أخصائيون مرخصون", "يقدّم الجلسات أخصائيون مرخصون ومعتمدون."), ("متابعة الحالة", "متابعة تطور الحالة من جلسة لجلسة.")],
         who=[("كبار السن", "جلسات في البيت بدون تعب المشاوير."), ("بعد الخروج من المستشفى", "استكمال الجلسات في البيت بين أهله."), ("من يصعب عليه التنقل", "الأخصائي يوصل للمريض بدل ما يتنقل هو.")],
         faq_extra=[]),
]


def cards(items, link=False):
    if link:
        return "\n".join(f'      <a class="fact" href="{h}"><b>{b}</b><small>{s}</small></a>' for b, s, h in items)
    return "\n".join(f'      <div class="fact"><b>{b}</b><small>{s}</small></div>' for b, s in items)


def page(sv):
    url = f"{SITE}/{sv['slug']}/"
    faq = [FAQ_STAFF, faq_book(sv["cta"]), *sv["faq_extra"], FAQ_AREA, FAQ_RELATIVE]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalBusiness", "@id": SITE + "/#org", "name": "مدى كير", "url": SITE + "/", "logo": SITE + "/assets/mada-logo.png"},
        {"@type": "Service", "@id": url + "#service", "name": sv["h1"].split(":")[0], "serviceType": sv["stype"], "description": sv["schema_desc"], "url": url,
         "provider": {"@id": SITE + "/#org"}, "areaServed": {"@type": "City", "name": "جدة"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "خدماتنا", "item": SITE + "/#services"},
            {"@type": "ListItem", "position": 3, "name": sv["short"], "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    qa = "".join(f'''      <div class="qa{' open' if i == 0 else ''}"><button type="button" class="qa-h" aria-expanded="{'true' if i == 0 else 'false'}"><span>{q}</span><img class="i-minus" src="/assets/ic-minus.svg" alt="" width="24" height="24" loading="lazy" decoding="async"><img class="i-plus" src="/assets/ic-plus.svg" alt="" width="24" height="24" loading="lazy" decoding="async"></button>
        <div class="qa-b"><p>{a}</p></div></div>
''' for i, (q, a) in enumerate(faq))
    others = [(o["short"], o["schema_desc"], f"/{o['slug']}/") for o in SERVICES if o is not sv]
    who = "" if not sv["who"] else f'''
<section class="tint" id="who">
  <div class="pat pat-02" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap stack32">
    <div class="sec-head">
      <p class="eyebrow">لمين الخدمة</p>
      <h2 class="h2">لمن يحتاج الخدمة وهو في بيته</h2>
    </div>
    <div class="facts">
{cards(sv["who"])}
    </div>
  </div>
</section>
'''
    book = BOOK.replace(f'<option value="{sv["svc"]}">', f'<option value="{sv["svc"]}" selected>')
    title, desc = sv["title"], sv["desc"]
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
{GTM_HEAD}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="مدى كير">
<meta property="og:locale" content="ar_SA">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/og-image.jpg">
<link rel="icon" type="image/png" href="/assets/mada-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="/fonts/thmanyahsans-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"></noscript>
<link rel="stylesheet" href="/site.css">
<!-- Structured data for Google: this service, breadcrumb and the FAQ shown on the page. Built by tools/build_service_pages.py. -->
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
{GTM_BODY}
<a class="skip" href="#main">تخطي إلى المحتوى</a>

{SNAV}
{HEADER}

<main id="main">
<section class="hero pg-hero" id="top">
  <div class="pat pat-10" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="pg-hero-in">
      <nav class="crumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">›</span><a href="/#services">خدماتنا</a><span aria-hidden="true">›</span><span aria-current="page">{sv["short"]}</span></nav>
      <h1 class="display">{sv["h1"]}</h1>
      <p class="lead">{sv["lead"]}</p>
      <div class="tags">
        <span class="tag-oc"><span>طواقم طبية مرخصة من وزارة الصحة</span><img src="/assets/ic-usercheck.svg" alt="" width="18" height="18"></span>
        <span class="tag-oc"><span>داخل مدينة جدة</span><img src="/assets/ic-location.svg" alt="" width="18" height="18" style="filter:brightness(0) invert(1)"></span>
      </div>
      <div class="hero-acts">
        <a class="btn btn-white" href="#book" data-book data-svc="{sv["svc"]}"><span>{sv["cta"]}</span><img src="/assets/ic-whatsapp-btn.svg" alt="" width="32" height="32"></a>
      </div>
    </div>
  </div>
</section>

<section class="svc" id="includes">
  <div class="wrap stack32">
    <div class="sec-head">
      <p class="eyebrow">وش تشمل الخدمة</p>
      <h2 class="h2">{sv["inc_h"]}</h2>
      <p class="p16 w800">{sv["inc_p"]}</p>
    </div>
    <div class="facts">
{cards(sv["inc"])}
    </div>
  </div>
</section>
{who}
<section class="svc" id="how">
  <div class="wrap stack32">
    <div class="sec-head">
      <p class="eyebrow">كيف تحجز</p>
      <h2 class="h2">ثلاث خطوات وتوصلك الرعاية</h2>
    </div>
    <div class="facts">
      <div class="fact"><small>الخطوة 1</small><b>اطلب الخدمة</b><small>اضغط «{sv["cta"]}» واترك اسمك ورقم جوالك، أو احجز من تطبيق مدى كير.</small></div>
      <div class="fact"><small>الخطوة 2</small><b>نأكد معك الموعد</b><small>يتواصل معك فريقنا لمعرفة الحالة وتحديد الموعد المناسب.</small></div>
      <div class="fact"><small>الخطوة 3</small><b>نوصل لبيتك</b><small>يصل فريقنا إلى منزلك ويقدّم الخدمة، ونتابع معك بعد الزيارة.</small></div>
    </div>
  </div>
</section>

<section class="tint" id="why">
  <div class="pat pat-02" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap stack56">
    <div class="sec-head center"><p class="eyebrow">ليش مدى كير</p><h2 class="h2">لماذا يختارنا أهــل جدة</h2></div>
    <div class="cards4">
      <div class="sc why"><span class="fi"><img src="/assets/why-ic4.svg" alt="" width="32" height="32" loading="lazy" decoding="async"></span><div class="sc-t"><b>الثقة المطلقة</b><p>طاقم طبي مرخص ومعتمد وفق أعلى المعايير الصحية المحلية والعالمية</p></div></div>
      <div class="sc why"><span class="fi"><img src="/assets/why-ic3.svg" alt="" width="32" height="32" loading="lazy" decoding="async"></span><div class="sc-t"><b>السرعة الذكية</b><p>نظام استجابة سريع يضمن وصول الفريق الطبي في وقت قياسي إلى منزلك</p></div></div>
      <div class="sc why"><span class="fi"><img src="/assets/why-ic2.svg" alt="" width="32" height="32" loading="lazy" decoding="async"></span><div class="sc-t"><b>الخصوصية التامة</b><p>نحترم خصوصية المنزل ونقدم خدماتنا في بيئة آمنة وهادئة للمريض</p></div></div>
      <div class="sc why"><span class="fi"><img src="/assets/why-ic1.svg" alt="" width="32" height="32" loading="lazy" decoding="async"></span><div class="sc-t"><b>التعامل الإنساني</b><p>شعارنا "نرعاكم كأهلُنا" ليس مجرد كلمات، بل منهج عمل يومي</p></div></div>
    </div>
  </div>
</section>

<section class="faq" id="help">
  <div class="faq-in">
    <div class="faq-text">
      <h2 class="h2">أسئلة شائعة عن {sv["short"]}</h2>
      <p class="p16">جمعنا لكم أكثر الأسئلة اللي تجينا عن خدمة {sv["short"]} في جدة.</p>
      <div class="faq-btns"><a class="btn btn-primary" href="#book" data-book data-svc="{sv["svc"]}"><span>{sv["cta"]}</span></a><a class="btn btn-neutral" href="#help" data-help>تحتاج لمساعدة؟</a></div>
    </div>
    <div class="faq-list" id="faq">
{qa}    </div>
  <a class="btn btn-neutral faq-help-m" href="#help" data-help>تحتاج لمساعدة؟</a>
  </div>
</section>

<section class="tint" id="more">
  <div class="wrap stack32">
    <div class="sec-head center"><p class="eyebrow">خدمات أخرى</p><h2 class="h2">رعاية متكاملة لكل العائلة</h2></div>
    <div class="cards4">
{cards(others, link=True)}
    </div>
  </div>
</section>
</main>

{FOOTER}

{WA}

{book}

<script src="/site-config.js"></script>
<script src="/site.js"></script>
</body>
</html>
'''


import os
for sv in SERVICES:
    os.makedirs(sv["slug"], exist_ok=True)
    open(f"{sv['slug']}/index.html", "w", encoding="utf-8").write(page(sv))
    print("wrote", sv["slug"])

RIGHTS = [
    ("تلقي العلاج والرعاية", "يجب أن يحصل المريض على العلاج والرعاية الضرورية لاسترداد صحته أو الحفاظ عليها، دون اعتبار للعرق أو الدين أو الجنس أو الحالة الاجتماعية أو الأصل أو العمر أو الإعاقة أو مصدر دفع تكلفة العلاج.", None),
    ("الاحترام والخصوصية", "يتمتع المريض بحق المعاملة باحترام والحفاظ على خصوصيته وكرامته، ويجب توفير خصوصية بصرية وسمعية خلال الأنشطة الشخصية مثل النظافة والإجراءات السريرية.", None),
    ("الرعاية من مقدمي الرعاية المؤهلين", "يجب أن يحصل المريض على الرعاية من مقدمي الرعاية الصحية المؤهلين، ممن لديهم التعليم والخبرة اللازمة لتقديم الخدمة بكفاءة.", None),
    ("تطبيق قواعد مكافحة العدوى", "يجب على مقدمي الرعاية الصحية اتباع قواعد مكافحة العدوى التي تحددها وزارة الصحة لحماية المرضى من الإصابة بالعدوى.", None),
    ("الالتزام بالقيم وحماية الحقوق", "يجب على مقدمي الرعاية الصحية احترام قيم المرضى ومعتقداتهم، وحماية حقوقهم، والإبلاغ عن أي حالات عنف جسدي أو نفسي.", None),
    ("تعيين وصي قانوني", "إذا كان المريض غير قادر على اتخاذ قرارات حول العلاج، يجب تعيين وصي قانوني للتوقيع نيابة عنه، مع التأكد من هوية الوصي أو ولي الأمر.", None),
    ("المشاركة في الرعاية الصحية", "يحق للمريض وذويه:", [
        "التواصل مع الفريق العلاجي للحصول على معلومات كاملة ومحدثة حول التشخيص والعلاج وفوائده والنتائج المتوقعة.",
        "معرفة البدائل الطبية والمخاطر ونسبة نجاح العلاج.",
        "التعرف على إمكانيات الرعاية المتاحة واسم الطبيب المسؤول.",
        "رفض العلاج أو عدم إكماله وفقاً للأنظمة المعمول بها، مع إبلاغه بمسؤولياته والخيارات البديلة.",
        "الاستفسار عن أي جزء من العلاج أو الخدمة المقدمة."]),
    ("توفير بيئة آمنة", "يجب توفير بيئة آمنة أثناء الجلسات العلاجية، وحماية المريض من أي نوع من الإساءة الجنسية أو اللفظية أو الإهمال وسوء المعاملة.", None),
    ("معلومات تكلفة العلاج", "يجب تزويد المريض بمعلومات مسبقة عن تكلفة العلاج، ويشمل ذلك تفسير الفاتورة والخدمات المقدمة.", None),
    ("رفض التوقيع", "يحق للمريض رفض التوقيع على أي مستند إن لم يُشرح له بطريقة واضحة.", None),
    ("تقديم الشكاوى", "يمكن للمريض إبلاغ موظفي تجربة العميل بأي شكوى أو مشكلة تتعلق برعايته أو حقوقه أو سلامته.", None),
]


def rights_page():
    url = f"{SITE}/patient-rights/"
    title = "حقوق المرضى | مدى كير للرعاية الصحية المنزلية"
    desc = "حقوق المريض في مدى كير: الرعاية دون تمييز، الخصوصية والكرامة، الرعاية من كوادر مؤهلة، معرفة تكلفة العلاج، والمشاركة في القرار وتقديم الشكاوى."
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalBusiness", "@id": SITE + "/#org", "name": "مدى كير", "url": SITE + "/", "logo": SITE + "/assets/mada-logo.png"},
        {"@type": "WebPage", "@id": url, "url": url, "name": "حقوق المرضى", "description": desc, "inLanguage": "ar", "publisher": {"@id": SITE + "/#org"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "حقوق المرضى", "item": url}]}]}
    items = ""
    for i, (h, t, sub) in enumerate(RIGHTS, 1):
        ul = "" if not sub else '<ul>' + "".join(f"<li>{x}</li>" for x in sub) + "</ul>"
        items += f'      <li class="rt{" rt-wide" if sub else ""}"><span class="rt-n" aria-hidden="true">{i}</span><div><h3>{h}</h3><p>{t}</p>{ul}</div></li>\n'
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
{GTM_HEAD}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="مدى كير">
<meta property="og:locale" content="ar_SA">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/assets/mada-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="/fonts/thmanyahsans-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"></noscript>
<link rel="stylesheet" href="/site.css">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
{GTM_BODY}
<a class="skip" href="#main">تخطي إلى المحتوى</a>

{SNAV}
{HEADER}

<main id="main">
<section class="hero pg-hero" id="top">
  <div class="pat pat-10" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="pg-hero-in">
      <nav class="crumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">›</span><span aria-current="page">حقوق المرضى</span></nav>
      <h1 class="display">حقوق المرضى</h1>
      <p class="lead">في مدى كير نرعاكم كأهلنا، ونلتزم بحقوق كل مريض نخدمه في بيته. هذي حقوقك وحقوق أهلك معنا.</p>
    </div>
  </div>
</section>

<section class="svc" id="rights">
  <div class="wrap stack32">
    <ol class="rights">
{items}    </ol>
  </div>
</section>

<section class="tint" id="complaint">
  <div class="pat pat-02" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="rt-cta">
      <div><h2 class="h2">عندك شكوى أو استفسار؟</h2><p class="p16">فريق تجربة العميل يسمعك ويتابع معك، وكل الشكاوى نتعامل معها بسرية.</p></div>
      <a class="btn btn-primary" href="#help" data-help><span>تواصل معنا</span></a>
    </div>
  </div>
</section>
</main>

{FOOTER}

{WA}

{BOOK}

<script src="/site-config.js"></script>
<script src="/site.js"></script>
</body>
</html>
'''


os.makedirs("patient-rights", exist_ok=True)
open("patient-rights/index.html", "w", encoding="utf-8").write(rights_page())
print("wrote patient-rights")

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for path in [""] + [s["slug"] + "/" for s in SERVICES] + ["patient-rights/"]:
    sm += f"  <url>\n    <loc>{SITE}/{path}</loc>\n    <lastmod>2026-11-19</lastmod>\n  </url>\n"
open("sitemap.xml", "w").write(sm + "</urlset>\n")
