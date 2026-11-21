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
            {"@type": "ListItem", "position": 2, "name": "خدماتنا", "item": SITE + "/services/"},
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
      <nav class="crumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">›</span><a href="/services/">خدماتنا</a><span aria-hidden="true">›</span><span aria-current="page">{sv["short"]}</span></nav>
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


def policy_page(slug, name, title, desc, lead, body, hero=None, tail=None, book=None, crumbs=None):
    url = f"{SITE}/{slug}/"
    if hero is None:
        hero = f'''<section class="hero pg-hero" id="top">
  <div class="pat pat-10" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="pg-hero-in">
      <nav class="crumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">›</span><span aria-current="page">{name}</span></nav>
      <h1 class="display">{name}</h1>
      <p class="lead">{lead}</p>
    </div>
  </div>
</section>'''
    if tail is None:
        tail = '''<section class="tint" id="complaint">
  <div class="pat pat-02" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="rt-cta">
      <div><h2 class="h2">عندك شكوى أو استفسار؟</h2><p class="p16">فريق تجربة العميل يسمعك ويتابع معك، وكل الشكاوى نتعامل معها بسرية.</p></div>
      <a class="btn btn-primary" href="#help" data-help><span>تواصل معنا</span></a>
    </div>
  </div>
</section>'''
    if book is None:
        book = BOOK
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalBusiness", "@id": SITE + "/#org", "name": "مدى كير", "url": SITE + "/", "logo": SITE + "/assets/mada-logo.png"},
        {"@type": "WebPage", "@id": url, "url": url, "name": name, "description": desc, "inLanguage": "ar", "publisher": {"@id": SITE + "/#org"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": SITE + "/"},
            *[{"@type": "ListItem", "position": i, "name": n, "item": u} for i, (n, u) in enumerate(crumbs or [(name, url)], 2)]]}]}
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
{hero}

{body}
{tail}
</main>

{FOOTER}

{WA}

{book}

<script src="/site-config.js"></script>
<script src="/site.js"></script>
</body>
</html>
'''




def rights_page():
    items = ""
    for i, (h, t, sub) in enumerate(RIGHTS, 1):
        ul = "" if not sub else '<ul>' + "".join(f"<li>{x}</li>" for x in sub) + "</ul>"
        items += f'      <li class="rt{" rt-wide" if sub else ""}"><span class="rt-n" aria-hidden="true">{i}</span><div><h3>{h}</h3><p>{t}</p>{ul}</div></li>\n'
    body = f'''<section class="svc" id="rights">
  <div class="wrap stack32">
    <ol class="rights">
{items}    </ol>
  </div>
</section>
'''
    return policy_page("patient-rights", "حقوق المرضى", "حقوق المرضى | مدى كير للرعاية الصحية المنزلية",
                       "حقوق المريض في مدى كير: الرعاية دون تمييز، الخصوصية والكرامة، الرعاية من كوادر مؤهلة، معرفة تكلفة العلاج، والمشاركة في القرار وتقديم الشكاوى.",
                       "في مدى كير نرعاكم كأهلنا، ونلتزم بحقوق كل مريض نخدمه في بيته. هذي حقوقك وحقوق أهلك معنا.", body)


CANCEL = [
    ("إعادة جدولة الزيارة", [
        "يمكن إعادة جدولة الموعد <b>مجاناً</b> بالتواصل معنا قبل <b>أكثر من 24 ساعة</b> من الموعد المحدد.",
        "خلال آخر <b>24 ساعة</b> قبل الموعد لا تتم إعادة الجدولة."]),
    ("إلغاء الزيارة", [
        "إذا تم الإلغاء قبل <b>أكثر من 24 ساعة</b> من الموعد، يُحتفظ بـ <b>75%</b> من قيمة الخدمة كرصيد في حساب العميل لاستخدامه في خدمات أخرى.",
        "إذا تم الإلغاء خلال <b>أقل من 24 ساعة</b> من الموعد، يُحتفظ بـ <b>50%</b> من قيمة الخدمة كرصيد في حساب العميل لاستخدامه في خدمات أخرى."]),
    ("عدم التواجد في المنزل", [
        "في حال عدم التواجد في المنزل بعد <b>15 دقيقة</b> من الموعد المحدد، سيتم اعتبار الجلسة <b>ملغاة</b> ولن يكون هناك أي استرداد للمبلغ."]),
    ("الاستثناءات", [
        "في الحالات الطارئة، يمكن التواصل مع فريق الدعم في مدى كير لبحث إمكانية تقديم استثناءات وفقاً للظروف الخاصة."]),
]
CANCEL_TABLE = [
    ("إعادة جدولة الزيارة قبل أكثر من 24 ساعة من الموعد.", "تتم إعادة الجدولة مجاناً", "ok"),
    ("إلغاء الزيارة قبل أكثر من 24 ساعة من الموعد.", "الاحتفاظ بـ 75% من المبلغ كرصيد للعميل", "mid"),
    ("إلغاء الزيارة خلال أقل من 24 ساعة من الموعد.", "الاحتفاظ بـ 50% من المبلغ كرصيد للعميل", "mid"),
    ("عدم التواجد في المنزل بعد أكثر من 15 دقيقة من موعد الجلسة.", "تُلغى الجلسة دون رد المبلغ أو منح رصيد", "no"),
    ("الحالات الطارئة.", "تواصل مع فريق الدعم لبحث الاستثناء", "ok"),
]


def cancel_page():
    items = ""
    for i, (h, sub) in enumerate(CANCEL, 1):
        items += f'      <li class="rt"><span class="rt-n" aria-hidden="true">{i}</span><div><h3>{h}</h3><ul>' + "".join(f"<li>{x}</li>" for x in sub) + '</ul></div></li>\n'
    rows = "".join(f'        <tr><td>{c}</td><td><span class="pol-r pol-{k}">{r}</span></td></tr>\n' for c, r, k in CANCEL_TABLE)
    body = f'''<section class="svc" id="policy">
  <div class="wrap stack32">
    <ol class="rights">
{items}    </ol>
    <div class="sec-head"><p class="eyebrow">ملخص السياسة</p><h2 class="h2">وش يصير في كل حالة؟</h2></div>
    <div class="pol-tbl"><table>
      <thead><tr><th scope="col">الحالة</th><th scope="col">الإجراء المتّبع</th></tr></thead>
      <tbody>
{rows}      </tbody>
    </table></div>
    <p class="p16">نُقدّر تعاونكم في الالتزام بهذه السياسة لضمان سير العمل بشكل فعّال وتقديم أفضل تجربة لجميع عملائنا.</p>
  </div>
</section>
'''
    return policy_page("cancellation-policy", "سياسة الإلغاء وإعادة الجدولة وعدم التواجد في المنزل", "سياسة الإلغاء وإعادة الجدولة وعدم التواجد في المنزل | مدى كير",
                       "سياسة مدى كير لإلغاء المواعيد وإعادة جدولتها وعدم التواجد في المنزل: مهلة 24 ساعة، الرصيد في حساب العميل، والاستثناءات في الحالات الطارئة.",
                       "نسعى دائماً لتقديم خدمة عالية الجودة لعملائنا، وأي تغيير أو تأخير في الموعد قد يؤثر على خدمة بقية العملاء. لذا نضع بين أيديكم سياسة واضحة للإلغاء وإعادة الجدولة وعدم التواجد في المنزل.", body)


PRIVACY = [
    ("المبادئ العامة لحماية البيانات الشخصية", ["تسعى «مدى كير» دائماً إلى حماية خصوصية المعلومات وسرية البيانات التي يتم جمعها من مستخدمي منصتها. لذلك، تُعتبر هذه السياسة جزءاً من شروط استخدام الموقع والتطبيق الخاص بـ«مدى كير»."], None),
    ("جمع المعلومات الشخصية", ["عند زيارة الموقع أو التطبيق، لا يتم جمع أي معلومات شخصية إلا إذا اخترت طواعية تقديمها. بالإضافة إلى ذلك، تُستخدم المعلومات التي تقدمها فقط لإنجاز طلباتك وتقديم الخدمات المطلوبة بكفاءة."], None),
    ("استخدام المعلومات الشخصية", ["تلتزم «مدى كير» بعدم مشاركة بياناتك الشخصية مع أي جهة غير حكومية إلا في حالات خاصة تتطلبها الأنظمة السعودية. وبالتالي، يمكنك الاطمئنان بأن بياناتك الشخصية تُعالج بسرية تامة."], None),
    ("ملفات الكوكيز (Cookies)", ["يتم استخدام ملفات «الكوكيز» لتسهيل تجربة المستخدم، مثل تذكر كلمة المرور أو إعدادات الصفحة. ويمكنك تعديل إعدادات الكوكيز أو تعطيلها في أي وقت."], None),
    ("تحديثات سياسة الخصوصية", ["تقوم «مدى كير» بتحديث سياسة الخصوصية بانتظام، لذلك نوصي المستخدمين بمراجعة السياسة بشكل دوري للبقاء على اطلاع على أي تغييرات."], None),
    ("حماية البيانات الشخصية", ["<b>التدابير الأمنية:</b> تطبق «مدى كير» تدابير صارمة لحماية المعلومات الشخصية من أي دخول غير مصرح به أو إساءة استخدام، ويتم تحديث إجراءات الحماية بانتظام لضمان توافقها مع المعايير القياسية.",
                                "<b>تدريب الموظفين:</b> يتم تدريب الموظفين باستمرار على التعامل بسرية تامة مع المعلومات الشخصية للعملاء، وذلك لضمان حماية وأمان البيانات بشكل كامل."], None),
    ("حقوق المستخدمين", ["للمستخدم الحق في:"], ["الاطلاع على أي معلومات عامة غير محمية.", "معرفة سبب رفض أي طلب للحصول على المعلومات.", "تقديم تظلم في حال رفض طلب الاطلاع على المعلومات."]),
]


def privacy_page():
    items = ""
    for i, (h, ps, sub) in enumerate(PRIVACY, 1):
        ul = "" if not sub else '<ul>' + "".join(f"<li>{x}</li>" for x in sub) + "</ul>"
        items += f'      <li class="rt rt-wide"><span class="rt-n" aria-hidden="true">{i}</span><div><h3>{h}</h3>' + "".join(f"<p>{x}</p>" for x in ps) + f'{ul}</div></li>\n'
    body = f'''<section class="svc" id="privacy">
  <div class="wrap stack32">
    <ol class="rights rights-1">
{items}    </ol>
  </div>
</section>
'''
    return policy_page("privacy-policy", "سياسة الخصوصية", "سياسة الخصوصية | مدى كير",
                       "سياسة الخصوصية في مدى كير: كيف نجمع بياناتك الشخصية ونستخدمها ونحميها، وملفات الكوكيز، وحقوقك كمستخدم.",
                       "خصوصيتك وبياناتك الصحية أمانة عندنا. هنا نوضح كيف نجمع معلوماتك ونستخدمها ونحميها.", body)


REVIEWS = [
    ("ريم القحطاني", "sa", "أكثر شيء أعجبني إنهم يهتمون براحة المريض نفسيًا قبل أي شيء. الخدمة إنسانية جدًا وتحس فعلًا إنهم يهتمون."),
    ("أبو عبدالله – جدة", "sa", "بدل تعب المشاوير والانتظار بالمستشفى، الطبيب زارنا في البيت بكل احترافية. الخدمة مريحة جدًا خصوصًا لكبار السن. شكرًا مدى كير."),
    ("Rajesh – Jeddah", "in", "Booking was easy, the medical staff arrived on time, and the service quality exceeded expectations. Highly recommended."),
    ("أم خالد – جدة", "sa", "صراحة التجربة فاقت توقعاتي، الممرضة كانت راقية جدًا بالتعامل وحسّتنا فعلًا إن الوالدة بين أيدٍ أمينة. أكثر شيء ريّحنا سرعة الاستجابة والاهتمام بالتفاصيل."),
    ("أحمد – جدة", "eg", "الخدمة ممتازة والتنظيم احترافي جدًا، المختبر وصل للبيت بموعده والنتائج وصلت بسرعة. وفروا علينا وقت ومجهود كبير."),
    ("Maria – Jeddah", "ph", "The nurse was very kind and professional. My mother felt comfortable during the entire visit. Thank you Mada Care for the excellent home healthcare service."),
    ("سارة الحربي", "sa", "جربت خدمة الفيتامينات الوريدية وكانت تجربة ممتازة جدًا، الفريق محترف والتعامل راقٍ والمواعيد دقيقة. أكيد مو آخر مرة."),
    ("محمد – جدة", "sd", "تعامل محترم جدًا واهتمام حقيقي بالمريض، خصوصًا المتابعة بعد الزيارة. هذا الشيء نادر اليوم."),
    ("نوف العتيبي", "sa", "كنت متخوفة بالبداية بالتعامل مع شركات رعاية منزلية مرة ثانية، لكن بعد أول زيارة عرفت الفرق فعلًا. مستوى الخدمة ممتاز ويستحق الثقة."),
    ("Khalid – Jeddah", "pk", "Very fast response and professional medical team. The home visit experience was smooth and comfortable for my family."),
]
FLAGS = {"sa": ("flag-sa.webp", "السعودية"), "eg": ("flag-eg.svg", "مصر"), "ph": ("flag-ph.svg", "الفلبين"), "in": ("flag-in.svg", "الهند"), "sd": ("flag-sd.svg", "السودان"), "pk": ("flag-pk.svg", "باكستان")}
AV = ["7,148,85", "128,81,159", "220,104,3", "21,112,239", "217,45,32"]
BOOK_FAQ = [
    ("كيف أضمن كفاءة الفريق الطبي القادم لمنزلي؟", "في مدى كير، لا نختار إلا الأفضل. جميع كوادرنا الطبية (أطباء، ممرضين، وفنيين) مرخصين ومعتمدين من الهيئة السعودية للتخصصات الصحية، ويخضعون لتدريب مستمر ليس فقط على الجانب الطبي، بل على «فن التعامل الإنساني» لضمان أن تكون الزيارة تجربة مريحة وآمنة لأحبتكم."),
    ("ما هي سرعة الاستجابة عند طلب الخدمة؟", "نحن ندرك أن الوقت هو أغلى ما نملكه في ظروف المرض. لذلك، صممنا نظام استجابة ذكي يجعل متوسط وقت الرد لدينا لا يتجاوز دقيقة واحدة. بمجرد تأكيد طلبك، ستحصل على إشعار بتفاصيل الفريق وتوقيت وصوله المتوقع إلى باب منزلك."),
    ("هل تتوفر لديكم خدمات طارئة؟", "مدى كير تقدم رعاية منزلية تخصصية ومجدولة مع وجود إمكانية لاستقبال الحالات الطارئة، وإذا كانت الحالة تستدعي تدخلاً طارئاً وفورياً (مثل صعوبات التنفس الحادة أو الحوادث) يمكننا نقل الحالة بسيارة إسعاف إلى أقرب مستشفى أو الهلال الأحمر."),
    ("هل يمكنني متابعة موقع الطبيب وهو في طريقه إليّ؟", "بالتأكيد! هذا هو جوهر التزامنا بالشفافية والراحة. من خلال تطبيق «مدى كير»، يمكنك تتبع مسار الفريق الطبي مباشرة على الخريطة ومعرفة الوقت المتبقي لوصولهم بدقة، تماماً كما تتابع رحلتك المفضلة، وأيضاً يمكنك التحدث مباشرة من خلال شات مخصص مع الفريق الطبي أثناء قدومه لمنزلك."),
    ("ماذا لو احتجت إلى متابعة حالتي بعد مغادرة الفريق الطبي؟", "علاقتنا لا تنتهي بمغادرة باب المنزل. نحن نقدم خدمة «المتابعة بعد الزيارة»، حيث يظل فريقنا على تواصل للاطمئنان على استقرار الحالة، ويمكنك الوصول لسجلك الطبي الكامل، نتائج تحاليلك، وخططك العلاجية في أي وقت ومن أي مكان عبر التطبيق."),
    ("هل خدماتكم تشمل جميع أحياء مدينة جدة؟", "نعم، نحن نغطي كافة أنحاء مدينة جدة، ونسعى دائماً لتوسيع نطاق تغطيتنا لضمان وصول «مدى كير» لكل منزل يحتاج إلى رعاية إنسانية واحترافية."),
    ("كيف يمكنني استلام نتائج الفحوصات المخبرية؟", "كل شيء رقمي وسهل، ستصلك نتائج تحاليلك المخبرية مباشرة عبر التطبيق فور صدورها، مع شرح مبسط للنتائج لضمان أن تكون الصورة واضحة أمامكم دائماً."),
]


def book_page():
    reviews = ""
    for i, (n, f, q) in enumerate(REVIEWS):
        img, alt = FLAGS[f]
        en = q[0].isascii()
        bq = f'<blockquote class="en"><p dir="ltr">{q}</p><span class="qm">”</span></blockquote>' if en else f'<blockquote><span class="qm">”</span><p>{q}</p></blockquote>'
        reviews += f'    <figure class="qc"><div class="qc-in"><div class="qc-top"><span class="av" style="--av:rgba({AV[i % 5]},.1);--ac:rgb({AV[i % 5]})"><i></i></span><b>{n}</b><img class="flag" src="/assets/{img}" alt="{alt}" width="24" height="18" loading="lazy" decoding="async"></div>\n      {bq}</div></figure>\n'
    qa = "".join(f'''      <div class="qa{' open' if i == 0 else ''}"><button type="button" class="qa-h" aria-expanded="{'true' if i == 0 else 'false'}"><span>{q}</span><img class="i-minus" src="/assets/ic-minus.svg" alt="" width="24" height="24" loading="lazy" decoding="async"><img class="i-plus" src="/assets/ic-plus.svg" alt="" width="24" height="24" loading="lazy" decoding="async"></button>
        <div class="qa-b"><p>{a}</p></div></div>
''' for i, (q, a) in enumerate(BOOK_FAQ))
    form = BOOK.replace('<div class="ov" id="bookOv" hidden>', '<div class="ov ov-inline" id="bookOv">').replace('<div class="dlg" role="dialog" aria-modal="true" aria-labelledby="bkT">', '<div class="dlg" role="region" aria-labelledby="bkT">')
    form = re.sub(r'\s*<button type="button" class="dlg-x"[^>]*>×</button>', "", form).replace('<h2 id="bkT">احجز موعدك</h2>', '<h2 id="bkT">اطلب زيارتك الآن</h2>')
    form = form.replace('<!-- Booking request (sent to the dashboard) -->', '<!-- Booking request (sent to the dashboard), shown inside the page -->')
    hero = f'''<section class="hero pg-hero bk-hero" id="top">
  <div class="pat pat-10" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="bk-grid">
      <div class="pg-hero-in">
        <nav class="crumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">›</span><span aria-current="page">احجز موعدك</span></nav>
        <h1 class="display">نرعاكُم كأهلُنا .. ونصلكم بضغطة زر</h1>
        <p class="lead">احجز زيارتك الآن ودعنا نكون جزءاً من طمأنينتك.</p>
        <div class="tags">
          <span class="tag-oc"><span>متوسط الرد <em>دقيقة واحدة</em></span><img src="/assets/grad-tag1.svg" alt="" width="18" height="18"></span>
          <span class="tag-oc"><span>طواقم طبية مرخصة من وزارة الصحة</span><img src="/assets/ic-usercheck.svg" alt="" width="18" height="18"></span>
        </div>
        <div class="hero-acts">
          <a class="btn btn-white" href="#help" data-help><span>تواصل مباشر</span><img src="/assets/ic-whatsapp-btn.svg" alt="" width="32" height="32"></a>
        </div>
        <div class="stores">
          <a class="store" data-as href="/#download" aria-label="Download on the App Store"><img class="st-ic ap" src="/assets/apple-logo.svg" alt=""><span class="st-tx as"><small>Download on the</small><b>App Store</b></span></a>
          <a class="store" data-gp href="/#download" aria-label="Get it on Google Play"><img class="st-ic gp" src="/assets/gplay-logo.svg" alt=""><span class="st-tx"><small>GET IT ON</small><b>Google Play</b></span></a>
        </div>
      </div>
      <div class="bk-form">
{form}
      </div>
    </div>
  </div>
</section>'''
    body = f'''<section class="tst">
  <div class="wrap stack32">
    <div class="sec-head">
      <p class="eyebrow">سُمعتنا</p>
      <h2 class="h2">أصوات من عملائنا بجدة</h2>
    </div>
  </div>
  <div class="tst-track" id="tst" tabindex="0" aria-label="آراء العملاء">
{reviews}  </div>
  <div class="pager">
    <button type="button" class="pg" data-dir="next" aria-label="التالي"><img src="/assets/ic-next.svg" alt="" width="24" height="24" loading="lazy" decoding="async"></button>
    <span class="dots" id="dots" aria-hidden="true"></span>
    <button type="button" class="pg" data-dir="prev" aria-label="السابق"><img src="/assets/ic-prev.svg" alt="" width="24" height="24" loading="lazy" decoding="async"></button>
  </div>
</section>

<section class="faq" id="faq-sec">
  <div class="faq-in">
    <div class="faq-text">
      <h2 class="h2">أسئلة تراودكم .. وإجابات نعتز بها</h2>
      <p class="p16">نحن هنا لنزيل عنكم أي تساؤل، ولنضع بين أيديكم كل ما يمنحكم الراحة.</p>
      <div class="faq-btns"><a class="btn btn-primary" href="#top" data-book><span>احجز موعدك</span></a><a class="btn btn-neutral" href="#help" data-help>تحتاج لمساعدة؟</a></div>
    </div>
    <div class="faq-list" id="faq">
{qa}    </div>
  </div>
</section>
'''
    tail = '''<section class="tint" id="contact">
  <div class="pat pat-02" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="rt-cta">
      <div><h2 class="h2">لا تزال لديك أسئلة؟ تواصل مع فريقنا مباشرة</h2><p class="p16">متوسط وقت الرد دقيقة واحدة.</p></div>
      <a class="btn btn-primary" href="#help" data-help><span>تواصل مباشر</span></a>
    </div>
  </div>
</section>'''
    return policy_page("book", "احجز موعدك", "احجز زيارة منزلية في جدة | مدى كير",
                       "احجز زيارة طبيب أو تمريض أو تحاليل منزلية أو فيتامينات وريدية أو علاج طبيعي في جدة مع مدى كير. اترك اسمك ورقمك ونتواصل معك خلال دقائق.",
                       "", body, hero=hero, tail=tail, book="")


os.makedirs("book", exist_ok=True)
open("book/index.html", "w", encoding="utf-8").write(book_page())
print("wrote book")

POSTS = [
    {"slug": "home-doctor-visit", "svc": "doctor", "page": "/home-doctor/", "page_name": "زيارة طبيب منزلية", "icon": "svc-ic4.svg", "bg": "#eff8ff", "cat": "زيارة الطبيب",
     "title": "زيارة الطبيب المنزلي: راحة وأمان ورعاية صحية أفضل داخل منزلك",
     "desc": "لماذا يفضل الكثير زيارة الطبيب في المنزل؟ تعرّف على فوائد زيارة الطبيب المنزلي في جدة لكبار السن والمرضى، وكيف تحجزها مع مدى كير.",
     "intro": ["أصبحت خدمة زيارة الطبيب المنزلي من أكثر الخدمات الصحية طلباً في السعودية، خاصةً لكبار السن والمرضى الذين يحتاجون رعاية مستمرة دون عناء الذهاب للمستشفى.",
               "في مدى كير نوفر خدمة طبيب منزلي في جدة بأعلى معايير الجودة والخصوصية، مع سرعة استجابة وفريق طبي محترف."],
     "h2": "لماذا يفضل الكثير زيارة الطبيب في المنزل؟",
     "list": ["تقليل خطر العدوى داخل المستشفيات.", "راحة أكبر للمريض وأسرته.", "متابعة صحية دقيقة داخل بيئة المريض.", "توفير الوقت والجهد، خاصة لكبار السن."],
     "outro": "إذا كنت تبحث عن كشف طبي منزلي أو زيارة طبيب للمنزل في جدة، فمدى كير توفر لك الرعاية الصحية أينما كنت."},
    {"slug": "wound-dressing-at-home", "svc": "nursing", "page": "/home-nursing/", "page_name": "التمريض المنزلي", "icon": "svc-ic3.svg", "bg": "#f8edff", "cat": "التمريض المنزلي",
     "title": "تغيير الجروح والضمادات في المنزل بطريقة صحيحة لتجنب المضاعفات",
     "desc": "متى تحتاج إلى ممرض منزلي لتغيير الجروح والضمادات؟ تعرّف على أهمية العناية الصحيحة بالجروح بعد العمليات ولمرضى السكري، وخدمة التمريض المنزلي في جدة.",
     "intro": ["يُعد تغيير الجروح في المنزل من أهم الخدمات التمريضية التي تحتاج إلى عناية دقيقة لمنع الالتهابات وتسريع الشفاء.",
               "عدم تنظيف الجرح أو تغيير الضماد بشكل صحيح قد يؤدي إلى مضاعفات خطيرة وتأخر التئام الجروح."],
     "h2": "متى تحتاج إلى ممرض منزلي لتغيير الجروح؟",
     "list": ["بعد العمليات الجراحية.", "مرضى السكري وتقرحات القدم.", "الجروح العميقة أو المزمنة.", "الحروق والإصابات الجلدية."],
     "outro": "في مدى كير نقدم خدمة تمريض منزلي في جدة وتغيير ضمادات منزلية بواسطة طاقم تمريضي مؤهل يضمن لك الراحة والأمان داخل منزلك."},
    {"slug": "full-checkup-every-6-months", "svc": "blood", "page": "/home-lab/", "page_name": "المختبر المنزلي", "icon": "svc-ic1.svg", "bg": "#fffaeb", "cat": "التحاليل المنزلية",
     "title": "أهمية الفحص الشامل كل 6 أشهر للحفاظ على صحتك",
     "desc": "الفحص الشامل الدوري يساعد على اكتشاف الأمراض مبكراً. تعرّف لماذا تحتاج فحصاً شاملاً كل 6 أشهر، وكيف تسوي تحاليلك في البيت مع مختبر مدى كير المنزلي في جدة.",
     "intro": ["القيام بالفحص الشامل الدوري يساعد على اكتشاف الكثير من الأمراض مبكراً قبل ظهور الأعراض، مما يزيد فرص العلاج ويحافظ على جودة الحياة."],
     "h2": "لماذا تحتاج إلى فحص شامل؟",
     "list": ["الكشف المبكر عن السكري والضغط.", "متابعة صحة القلب والكوليسترول.", "الاطمئنان على وظائف الجسم والفيتامينات.", "الوقاية من الأمراض المزمنة."],
     "outro": "توفر مدى كير خدمة مختبر منزلي في جدة وتحاليل منزلية بكل سهولة وخصوصية، حيث يصل فريقنا إلى منزلك لسحب العينات دون الحاجة لزيارة المختبر."},
    {"slug": "iv-vitamins-benefits", "svc": "iv", "page": "/iv-therapy/", "page_name": "الفيتامينات الوريدية", "icon": "svc-ic2.svg", "bg": "#fef3f2", "cat": "الفيتامينات الوريدية",
     "title": "فوائد الفيتامينات الوريدية لتعزيز الطاقة والمناعة",
     "desc": "ما فوائد الفيتامينات الوريدية IV Therapy؟ تعرّف على دورها في دعم النشاط والترطيب والمناعة، وجلسات الفيتامينات الوريدية في منزلك بجدة مع مدى كير.",
     "intro": ["أصبحت جلسات الفيتامينات الوريدية IV Therapy من أكثر الخدمات الصحية انتشاراً لما لها من دور في دعم النشاط والترطيب وتعزيز المناعة."],
     "h2": "ما فوائد الفيتامينات الوريدية؟",
     "list": ["زيادة الطاقة وتقليل الإرهاق.", "دعم المناعة وتحسين التركيز.", "تعويض نقص الفيتامينات بسرعة.", "تحسين الترطيب وصحة البشرة."],
     "outro": "في مدى كير نقدم خدمة فيتامينات وريدية منزلية داخل منزلك بأمان تام وعلى يد مختصين، لتستمتع بتجربة صحية مريحة واحترافية."},
]
POST_DATE = "2026-11-21"
POST_DATE_AR = "21 نوفمبر 2026"


def read_min(p):
    words = sum(len(x.split()) for x in p["intro"] + p["list"] + [p["outro"], p["h2"]])
    n = max(1, round(words / 180))
    return {1: "دقيقة واحدة", 2: "دقيقتان"}.get(n, f"{n} دقائق")


def post_cover(p, big=False):
    return f'<div class="post-cover{" post-cover-lg" if big else ""}" style="--pc:{p["bg"]}" aria-hidden="true"><span class="vi"><img src="/assets/{p["icon"]}" alt="" width="40" height="40"></span></div>'


def post_card(p):
    return f'''      <article class="post-card">
        <a class="post-card-a" href="/blog/{p["slug"]}/">{post_cover(p)}</a>
        <div class="post-card-b">
          <p class="post-meta"><span class="post-cat">{p["cat"]}</span><span>قراءة {read_min(p)}</span></p>
          <h3><a href="/blog/{p["slug"]}/">{p["title"]}</a></h3>
          <p>{p["desc"]}</p>
          <a class="post-more" href="/blog/{p["slug"]}/">اقرأ المقال<img src="/assets/ic-arrow-left.svg" alt="" width="18" height="18" loading="lazy" decoding="async"></a>
        </div>
      </article>'''


def blog_hero(crumbs, h1, lead, meta=""):
    return f'''<section class="hero pg-hero" id="top">
  <div class="pat pat-10" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="pg-hero-in">
      <nav class="crumbs" aria-label="مسار الصفحة">{crumbs}</nav>
      <h1 class="display">{h1}</h1>
      <p class="lead">{lead}</p>{meta}
    </div>
  </div>
</section>'''


BLOG_TAIL = '''<section class="tint" id="contact">
  <div class="pat pat-02" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="rt-cta">
      <div><h2 class="h2">تحتاج رعاية في بيتك؟</h2><p class="p16">فريق مدى كير يوصلك داخل جدة، ومتوسط وقت الرد دقيقة واحدة.</p></div>
      <a class="btn btn-primary" href="#book" data-book><span>احجز موعدك الآن</span></a>
    </div>
  </div>
</section>'''


def blog_index():
    cards = "\n".join(post_card(p) for p in POSTS)
    hero = blog_hero('<a href="/">الرئيسية</a><span aria-hidden="true">›</span><span aria-current="page">المدونة</span>',
                     "مدونة مدى كير", "نصائح ومعلومات صحية موثوقة تساعدك تهتم بنفسك وبأهلك في البيت، من فريق مدى كير للرعاية الصحية المنزلية.")
    body = f'''<section class="svc" id="posts">
  <div class="wrap stack32">
    <div class="post-grid">
{cards}
    </div>
  </div>
</section>
'''
    ld_blog = {"@context": "https://schema.org", "@type": "Blog", "@id": SITE + "/blog/#blog", "name": "مدونة مدى كير", "url": SITE + "/blog/", "inLanguage": "ar",
               "publisher": {"@id": SITE + "/#org"},
               "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/blog/{p['slug']}/", "datePublished": POST_DATE} for p in POSTS]}
    html = policy_page("blog", "المدونة", "مدونة مدى كير | نصائح صحية للرعاية المنزلية في جدة",
                       "مقالات ونصائح صحية من مدى كير: زيارة الطبيب المنزلي، التمريض والعناية بالجروح، الفحص الشامل والتحاليل المنزلية، والفيتامينات الوريدية.",
                       "", body, hero=hero, tail=BLOG_TAIL)
    return html.replace("</script>\n</head>", "</script>\n<script type=\"application/ld+json\">\n" + json.dumps(ld_blog, ensure_ascii=False, indent=1) + "\n</script>\n</head>", 1)


def blog_post(p):
    url = f"{SITE}/blog/{p['slug']}/"
    meta = f'''
      <p class="post-meta post-meta-h"><span class="post-cat">{p["cat"]}</span><span>فريق مدى كير</span><time datetime="{POST_DATE}">{POST_DATE_AR}</time><span>قراءة {read_min(p)}</span></p>'''
    hero = blog_hero(f'<a href="/">الرئيسية</a><span aria-hidden="true">›</span><a href="/blog/">المدونة</a><span aria-hidden="true">›</span><span aria-current="page">{p["cat"]}</span>',
                     p["title"], p["intro"][0], meta)
    intro = "".join(f"<p>{x}</p>" for x in p["intro"][1:])
    items = "".join(f"<li>{x}</li>" for x in p["list"])
    others = [o for o in POSTS if o is not p][:3]
    rel = "\n".join(post_card(o) for o in others)
    body = f'''<section class="svc" id="article">
  <div class="wrap">
    <article class="post">
      {post_cover(p, True)}
      {intro}
      <h2>{p["h2"]}</h2>
      <ul>{items}</ul>
      <p>{p["outro"]}</p>
      <aside class="post-cta">
        <div><b>{p["page_name"]} في جدة</b><p>اعرف تفاصيل الخدمة وكيف تحجزها من صفحتها.</p></div>
        <div class="post-cta-acts"><a class="btn btn-primary" href="#book" data-book data-svc="{p["svc"]}"><span>احجز موعدك الآن</span></a><a class="btn btn-neutral" href="{p["page"]}">صفحة الخدمة</a></div>
      </aside>
      <p class="post-note">هذا المحتوى للتوعية الصحية العامة، ولا يغني عن استشارة الطبيب المختص لحالتك.</p>
    </article>
  </div>
</section>

<section class="tint" id="more">
  <div class="pat pat-02" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap stack32">
    <div class="sec-head"><p class="eyebrow">اقرأ أيضاً</p><h2 class="h2">مقالات أخرى</h2></div>
    <div class="post-grid">
{rel}
    </div>
  </div>
</section>
'''
    ld_post = {"@context": "https://schema.org", "@type": "BlogPosting", "@id": url + "#post", "mainEntityOfPage": url, "headline": p["title"], "description": p["desc"],
               "inLanguage": "ar", "datePublished": POST_DATE, "dateModified": POST_DATE, "image": SITE + "/assets/og-image.jpg",
               "author": {"@type": "Organization", "name": "فريق مدى كير", "url": SITE + "/"}, "publisher": {"@id": SITE + "/#org"},
               "about": {"@type": "MedicalBusiness", "@id": SITE + "/#org"}}
    html = policy_page(f"blog/{p['slug']}", p["title"], f"{p['title']} | مدونة مدى كير", p["desc"], "", body, hero=hero, tail="",
                       crumbs=[("المدونة", SITE + "/blog/"), (p["title"], url)])
    html = html.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">', 1)
    return html.replace("</script>\n</head>", "</script>\n<script type=\"application/ld+json\">\n" + json.dumps(ld_post, ensure_ascii=False, indent=1) + "\n</script>\n</head>", 1)


os.makedirs("blog", exist_ok=True)
open("blog/index.html", "w", encoding="utf-8").write(blog_index())
for p in POSTS:
    os.makedirs(f"blog/{p['slug']}", exist_ok=True)
    open(f"blog/{p['slug']}/index.html", "w", encoding="utf-8").write(blog_post(p))
print("wrote blog +", len(POSTS), "posts")


def contact_page():
    hero = """<section class="hero pg-hero" id="top">
  <div class="pat pat-10" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="pg-hero-in">
      <nav class="crumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">›</span><span aria-current="page">اتصل بنا</span></nav>
      <h1 class="display">نسعد بتواصلك معنا 💚</h1>
      <p class="lead">نحن هنا للإجابة عن استفساراتك ومساعدتك في الوصول إلى الخدمة المناسبة.</p>
    </div>
  </div>
</section>"""
    body = """<section class="ct-sec">
  <div class="wrap">
    <div class="ct-grid">
      <article class="ct-card">
        <span class="ct-ic ct-ic-wa"><img src="/assets/ic-whatsapp-btn.svg" alt="" width="28" height="28"></span>
        <h2>تواصل عبر واتساب</h2>
        <p>راسل فريق مدى كير وسنساعدك.</p>
        <a class="help-btn help-wa" data-wa-link href="#book"><span>ابدأ المحادثة</span></a>
      </article>
      <article class="ct-card">
        <span class="ct-ic"><img src="/assets/ic-phone-dark.svg" alt="" width="26" height="26"></span>
        <h2>اتصل بنا</h2>
        <p>تحدث مباشرة مع فريق خدمة العملاء.</p>
        <a class="help-btn help-call" data-tel-link href="#book"><span>اتصل الآن</span></a>
      </article>
      <article class="ct-card">
        <span class="ct-ic"><img src="/assets/ic-location.svg" alt="" width="26" height="26"></span>
        <h2>موقعنا</h2>
        <p>جدة، المملكة العربية السعودية.</p>
      </article>
    </div>
    <p class="ct-foot">مدى كير – نرعاكم كأهلنا 💚</p>
  </div>
</section>"""
    return policy_page("contact", "اتصل بنا", "اتصل بنا | مدى كير للرعاية الصحية المنزلية",
                       "تواصل مع مدى كير للرعاية الصحية المنزلية في جدة عبر واتساب أو الاتصال المباشر، فريقنا هنا لمساعدتك.",
                       "", body, hero=hero, tail="")


def about_page():
    hero = """<section class="hero pg-hero ab-hero" id="top">
  <div class="pat pat-10" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="pg-hero-in">
      <nav class="crumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">›</span><span aria-current="page">من نحن</span></nav>
      <h1 class="display">من نحن</h1>
      <p class="lead">في مدى كير لم نؤسس شركة تقدم خدمات طبية فقط ،<br>بل أسسنا مفهومًا جديدًا للرعاية المنزلية يعتمد على:</p>
    </div>
  </div>
</section>"""
    body = """<section class="ab-sec">
  <div class="wrap">
    <div class="ab-pillars">
      <div class="ab-pill"><span class="ab-emo" aria-hidden="true">🩺</span><b>الاحتراف الطبي</b></div>
      <div class="ab-pill"><span class="ab-emo" aria-hidden="true">⚡</span><b>سرعة الاستجابة</b></div>
      <div class="ab-pill"><span class="ab-emo" aria-hidden="true">🔒</span><b>الخصوصية التامة</b></div>
      <div class="ab-pill"><span class="ab-emo" aria-hidden="true">🤝</span><b>والتعامل الإنساني قبل أي شيء</b></div>
    </div>
  </div>
</section>
<section class="ab-sec ab-tint">
  <div class="wrap">
    <div class="ab-team">
      <span class="ab-big" aria-hidden="true">👩‍⚕️</span>
      <p class="ab-quote">لهذا حرصنا على اختيار فريق طبي مؤهل لا يتميز بالكفاءة فقط…<br><em>بل بالرحمة والاهتمام أيضًا.</em></p>
    </div>
  </div>
</section>
<section class="ab-sec">
  <div class="wrap">
    <div class="ab-mem">
      <h2 class="h2">لأننا نؤمن أن المريض يتذكر دائمًا:</h2>
      <ol class="ab-steps">
        <li><span class="ab-emo" aria-hidden="true">💬</span><b>كيف تم التعامل معه،</b></li>
        <li><span class="ab-emo" aria-hidden="true">💚</span><b>وكيف شعر أثناء الرعاية،</b></li>
        <li><span class="ab-emo" aria-hidden="true">✨</span><b>قبل أن يتذكر أي شيء آخر.</b></li>
      </ol>
    </div>
  </div>
</section>
<section class="ab-sec ab-tint">
  <div class="wrap">
    <div class="ab-see">
      <p class="ab-not">لذلك نحن لا نرى المرضى كأرقام أو مواعيد…</p>
      <div class="ab-chips" aria-hidden="true"><s>#1024</s><s>10:30</s></div>
      <div class="ab-fam" aria-hidden="true"><span>👩</span><span>👨</span><span>🧒</span></div>
      <p class="ab-yes">نحن نراهم أمهات وآباء وأبناء يستحقون الرعاية باحترام وطمأنينة.</p>
    </div>
  </div>
</section>
<section class="ab-motto">
  <div class="wrap">
    <div class="ab-motto-card">
      <p class="ab-motto-k">ولهذا اخترنا شعارنا بعناية:</p>
      <p class="ab-motto-t">نرعَــــاكُم كأهلُنـــا 💚</p>
      <a class="btn btn-white" href="#book" data-book><span>احجز موعدك الآن</span></a>
    </div>
  </div>
</section>"""
    return policy_page("about", "من نحن", "من نحن | مدى كير للرعاية الصحية المنزلية",
                       "مدى كير: مفهوم جديد للرعاية المنزلية يعتمد على الاحتراف الطبي وسرعة الاستجابة والخصوصية التامة والتعامل الإنساني. نرعاكم كأهلنا.",
                       "", body, hero=hero, tail="")


SVC_LOOK = {  # icon, soft background, accent colour, emoji for each service on /services/
    "home-doctor": ("svc-ic4.svg", "#eff8ff", "#1570ef", "🩺"),
    "home-nursing": ("svc-ic3.svg", "#f8edff", "#80519f", "💉"),
    "home-lab": ("svc-ic1.svg", "#fffaeb", "#dc6803", "🧪"),
    "iv-therapy": ("svc-ic2.svg", "#fef3f2", "#d92d20", "💧"),
    "home-physiotherapy": ("ic-bone.svg", "#ecfdf3", "#079455", "🦵"),
}


def services_page():
    chips = "".join(f'<a class="sx-chip" href="#{sv["slug"]}" style="--ac:{SVC_LOOK[sv["slug"]][2]}"><span aria-hidden="true">{SVC_LOOK[sv["slug"]][3]}</span>{sv["short"]}</a>' for sv in SERVICES)
    hero = f'''<section class="hero pg-hero sx-hero" id="top">
  <div class="pat pat-10" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="pg-hero-in">
      <nav class="crumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">›</span><span aria-current="page">خدماتنا</span></nav>
      <h1 class="display">خدماتنا الطبية المنزلية</h1>
      <p class="lead">رعاية طبية منزلية في جدة بطواقم طبية مرخصة من وزارة الصحة، تصلكم إلى باب البيت. اختر الخدمة اللي تحتاجها واحجز بخطوات بسيطة.</p>
    </div>
  </div>
</section>
<nav class="sx-bar" aria-label="خدماتنا"><div class="sx-bar-in">{chips}</div></nav>'''
    rows = []
    for n, sv in enumerate(SERVICES, 1):
        ic, bg, ac, emo = SVC_LOOK[sv["slug"]]
        inc = "".join(f'<li><span class="sx-ck" aria-hidden="true">✓</span><div><b>{t}</b><small>{d}</small></div></li>' for t, d in sv["inc"])
        floats = "".join(f'<span class="sx-float f{i}"><i>✓</i>{t}</span>' for i, (t, _) in enumerate(sv["inc"], 1))
        rows.append(f'''<section class="sx-row{' sx-rev' if n % 2 == 0 else ''}" id="{sv["slug"]}" style="--bg:{bg};--ac:{ac}">
  <div class="wrap sx-in">
    <div class="sx-vis" aria-hidden="true">
      <span class="sx-num">0{n}</span>
      <span class="sx-blob b1"></span><span class="sx-blob b2"></span>
      <span class="sx-ic"><img src="/assets/{ic}" alt="" width="64" height="64" loading="lazy" decoding="async"></span>
      <span class="sx-emo">{emo}</span>
      {floats}
    </div>
    <div class="sx-txt">
      <h2 class="h2">{sv["short"]}</h2>
      <p class="p16">{sv["lead"]}</p>
      <ul class="sx-inc">{inc}</ul>
      <div class="sx-acts"><a class="btn btn-primary" href="#book" data-book data-svc="{sv["svc"]}"><span>{sv["cta"]}</span></a><a class="btn btn-neutral" href="/{sv["slug"]}/">صفحة الخدمة</a></div>
    </div>
  </div>
</section>''')
    app = fix(between('<section class="appcta"', "</section>")).replace('srcset="assets/', 'srcset="/assets/').replace(", assets/", ", /assets/")
    body = "\n".join(rows) + "\n" + app
    html = policy_page("services", "خدماتنا", "خدماتنا | الرعاية الصحية المنزلية في جدة من مدى كير",
                       "خدمات مدى كير للرعاية الصحية المنزلية في جدة: زيارة طبيب منزلية، تمريض منزلي، مختبر منزلي، فيتامينات وريدية وعلاج طبيعي في بيتك.",
                       "", body, hero=hero, tail="")
    return html.replace('<a href="/services/">خدماتنا</a>', '<a href="/services/" aria-current="page">خدماتنا</a>', 1)



os.makedirs("services", exist_ok=True)
open("services/index.html", "w", encoding="utf-8").write(services_page())
print("wrote services")
os.makedirs("contact", exist_ok=True)
os.makedirs("about", exist_ok=True)
open("about/index.html", "w", encoding="utf-8").write(about_page())
print("wrote about")
open("contact/index.html", "w", encoding="utf-8").write(contact_page())
print("wrote contact")
os.makedirs("privacy-policy", exist_ok=True)
open("privacy-policy/index.html", "w", encoding="utf-8").write(privacy_page())
print("wrote privacy-policy")
os.makedirs("patient-rights", exist_ok=True)
open("patient-rights/index.html", "w", encoding="utf-8").write(rights_page())
print("wrote patient-rights")
os.makedirs("cancellation-policy", exist_ok=True)
open("cancellation-policy/index.html", "w", encoding="utf-8").write(cancel_page())
print("wrote cancellation-policy")

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for path in [""] + [s["slug"] + "/" for s in SERVICES] + ["patient-rights/", "cancellation-policy/", "privacy-policy/", "book/", "blog/", "contact/", "about/", "services/"] + [f"blog/{p['slug']}/" for p in POSTS]:
    sm += f"  <url>\n    <loc>{SITE}/{path}</loc>\n    <lastmod>2026-11-19</lastmod>\n  </url>\n"
open("sitemap.xml", "w").write(sm + "</urlset>\n")
