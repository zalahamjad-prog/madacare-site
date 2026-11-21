#!/usr/bin/env python3
"""Build the English pages (/en/ and /en/contact/) from the Arabic ones.

Run after tools/build_service_pages.py:  python3 tools/build_en.py
Each Arabic text (between tags, or in alt/aria-label/placeholder/content/title)
is swapped for its English line in T below. Any Arabic text without a line
is printed as MISSING so nothing is left untranslated by accident.
"""
import os, re, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AR = re.compile("[؀-ۿ]")

T = {
    # Head
    "مدى كير | الرعاية الصحية المنزلية": "Mada Care | Home Healthcare in Jeddah",
    "مدى كير للرعاية الصحية المنزلية: زيارة طبيب، تمريض منزلي، مختبر منزلي، فيتامينات وريدية وعلاج طبيعي في منزلك.":
        "Mada Care Home Healthcare: doctor visits, home nursing, home lab, IV vitamins and physiotherapy at your home.",
    "زيارة طبيب، تمريض منزلي، مختبر منزلي، فيتامينات وريدية وعلاج طبيعي في منزلك.":
        "Doctor visits, home nursing, home lab, IV vitamins and physiotherapy at your home.",
    "مدى كير: رعاية طبية تمنحك شعور الأمان والراحة": "Mada Care: medical care that gives you safety and comfort",
    # Header and accessibility bar
    "تخطي إلى المحتوى": "Skip to content",
    "الرئيسية": "Home", "من نحن": "About us", "خدماتنا": "Services", "المدونة": "Blog",
    "احجز موعدك": "Book now", "تحميل التطبيق": "Get the app",
    "تباين عالٍ": "High contrast", "تكبير الخط": "Larger text", "تصغير الخط": "Smaller text",
    "قراءة الصفحة بصوت": "Read the page aloud", "مدى كير": "Mada Care", "القائمة الرئيسية": "Main menu",
    "اللغة": "العربية", "القائمة": "Menu", "إغلاق": "Close", "التالي": "Next", "السابق": "Previous",
    "مسار الصفحة": "Breadcrumb",
    # Hero
    "مدى كير للرعاية الصحية المنزلية": "Mada Care Home Healthcare",
    "طواقم طبية مرخصة": "Medical teams licensed", "من وزارة الصحة": "by the Ministry of Health",
    "رعاية طبية منزلية تمنحك الأمان ، الراحة ، والطمأنينة": "Home medical care that gives you safety, comfort and peace of mind",
    "الأمان…": "Safety…", "عندما يصل الطبيب إلى باب المنزل.": "when the doctor comes to your door.",
    "الراحة…": "Comfort…", "عندما يجد المريض الرعاية دون عناء الانتظار.": "when the patient gets care without the hassle of waiting.",
    "الطمأنينة…": "Peace of mind…", "عندما تشعر العائلة أن من يرعى أحبّتهم يعاملهم كأهله.": "when the family feels their loved ones are cared for like family.",
    "اتصل بنا الآن": "Call us now", "احجز موعدك الآن": "Book a visit",
    "متوسط وقت الرد": "Average reply time", "دقيقة واحدة": "1 minute",
    # Feature cards
    "لأن المريض يحتاج أكثر من علاج": "Because a patient needs more than treatment",
    "في مدى كير نؤمن أن الرعاية الحقيقية لا تبدأ بالأدوية فقط ، بل تبدأ بالاهتمام بكل التفاصيل":
        "At Mada Care we believe real care doesn't start with medicine alone. It starts with caring about every detail.",
    "أسلوب تعامل الفريق الطبي": "How our medical team treats you",
    "كوادرنا الطبية مدربة على أعلى مستويات الكفاءة والتعاطف الإنساني، ليتلقى أحباؤكم الرعاية الطبية بكثير من الود والمسؤولية.":
        "Our medical staff are trained to the highest levels of skill and compassion, so your loved ones receive care with warmth and responsibility.",
    "راحة المريض النفسية": "The patient's peace of mind",
    "نؤمن أن الشفاء يبدأ من الطمأنينة، لذلك نوفر بيئة علاجية مريحة تحافظ على خصوصية المريض وتعفيه من عناء المستشفيات.":
        "We believe healing starts with reassurance, so we provide a comfortable setting that protects the patient's privacy and spares them the strain of hospitals.",
    "سرعة الاستجابة": "Fast response",
    "الوقت يصنع الفارق في الرعاية الصحية؛ فريقنا مستعد دائماً لتلبية طلباتكم والوصول إلى باب منزلكم بأسرع وقت ممكن.":
        "Time makes the difference in healthcare. Our team is always ready to answer your request and reach your door as quickly as possible.",
    "متابعة الحالة بعد الزيارة": "Follow-up after the visit",
    "رعايتنا لا تنتهي بمغادرة المنزل؛ نلتزم بالتواصل المستمر معكم لمتابعة تطورات الحالة الصحية وضمان استقرارها تماماً.":
        "Our care doesn't end when we leave your home. We stay in touch to follow the patient's progress and make sure their condition is stable.",
    "نحن لا نقدم خدمة فقط ،،، بل نقدم شعوراً": "We don't just offer a service... we offer a feeling", "بالأمان": "of safety",
    "تحتاج لمساعدة؟": "Need help?",
    # Numbers
    "أرقام نفتخر بها": "Numbers we're proud of", "زيارة منزلية": "Home visits", "رضا العملاء": "Customer satisfaction",
    "فريق طبي محترف ومعتمد من وزارة الصحة": "A professional medical team licensed by the Ministry of Health",
    "استجابة سريعة جداً داخل جدة": "Very fast response across Jeddah",
    "أرقام تبني الثقة": "Numbers that build trust",
    # Services
    "خدماتنا الطبية المنزلية": "Our home medical services",
    "اطلب زيارة طبيب": "Request a doctor visit", "زيارة طبيب منزلية": "Home doctor visit",
    "رعاية طبية احترافية داخل منزلكم لتقييم الحالة وتشخيصها ومتابعتها.": "Professional medical care at home to assess, diagnose and follow up on the patient's condition.",
    "كشف منزلي": "Home check-up", "أطباء متخصصون": "Specialist doctors", "استجابة سريعة": "Fast response",
    "اطلب زيارة ممرض": "Request a nurse visit", "خدمات التمريض المنزلي": "Home nursing",
    "رعاية تمريضية متكاملة تشمل إعطاء الأدوية ، تغيير الجروح ، متابعة العلامات الحيوية ، والرعاية اليومية.":
        "Complete nursing care, including giving medication, changing wound dressings, checking vital signs and daily care.",
    "غيار جروح": "Wound dressing", "ممرضون مرخصون": "Licensed nurses", "رعاية يومية": "Daily care",
    "اطلب زيارة": "Request a visit", "الفيتامينات الوريدية (IV Therapy)": "IV vitamin therapy",
    "جلسات فيتامينات وريدية لتعزيز النشاط والطاقة ودعم الصحة العامة.": "IV vitamin sessions to boost your energy and support your overall health.",
    "تقوية المناعة": "Immune support", "جلسات آمنة": "Safe sessions", "تعزيز الطاقة": "Energy boost",
    "المختبر المنزلي": "Home lab",
    "سحب العينات والتحاليل المخبرية داخل المنزل بكل سهولة وخصوصية واستلام النتائج اون لاين.":
        "Sample collection and lab tests at home, easily and privately, with your results online.",
    "نتائج أونلاين": "Online results", "سحب عينات": "Sample collection", "دقة عالية": "High accuracy",
    "علاج طبيعي": "Physiotherapy",
    # Response banner
    "سرعة الاستجابة هي أولويتنا": "Fast response is our priority",
    "ندرك أن في الرعاية الصحية، كل ثانية تفرق ، لذلك فريقنا التقني والطبي يعمل بتناغم لضمان رد فوري واستجابة طبية لا تضاهى . جميع طواقمنا الطبية مرخصة ومعتمدة من وزارة الصحة مما يضمن أعلى مستويات الطمأنينة والأمان لكل أسرة من أهالينا.":
        "We know that in healthcare every second counts, so our technical and medical teams work together to make sure you get an instant reply and an unmatched medical response. All our medical teams are licensed and accredited by the Ministry of Health, for the highest level of reassurance and safety for every family.",
    # Testimonials
    "أصوات من أهلُنا بـ جدة": "Voices from our families in Jeddah", "آراء العملاء": "Customer reviews",
    "ريم القحطاني": "Reem Al-Qahtani",
    "أكثر شيء أعجبني إنهم يهتمون براحة المريض نفسيًا قبل أي شيء. الخدمة إنسانية جدًا وتحس فعلًا إنهم يهتمون.":
        "What I liked most is that they care about the patient's peace of mind before anything else. The service is truly human and you can feel they care.",
    "أبو عبدالله – جدة": "Abu Abdullah, Jeddah",
    "بدل تعب المشاوير والانتظار بالمستشفى، الطبيب زارنا في البيت بكل احترافية. الخدمة مريحة جدًا خصوصًا لكبار السن. شكرًا مدى كير.":
        "Instead of the tiring trips and waiting at the hospital, the doctor visited us at home and was very professional. The service is so convenient, especially for the elderly. Thank you, Mada Care.",
    "أم خالد – جدة": "Umm Khalid, Jeddah",
    "صراحة التجربة فاقت توقعاتي، الممرضة كانت راقية جدًا بالتعامل وحسّتنا فعلًا إن الوالدة بين أيدٍ أمينة. أكثر شيء ريّحنا سرعة الاستجابة والاهتمام بالتفاصيل.":
        "Honestly, the experience exceeded my expectations. The nurse was very kind and made us feel my mother was in safe hands. What reassured us most was the fast response and the attention to detail.",
    "أحمد – جدة": "Ahmed, Jeddah",
    "الخدمة ممتازة والتنظيم احترافي جدًا، المختبر وصل للبيت بموعده والنتائج وصلت بسرعة. وفروا علينا وقت ومجهود كبير.":
        "Excellent service and very well organised. The lab came to our home on time and the results arrived quickly. They saved us a lot of time and effort.",
    "سارة الحربي": "Sarah Al-Harbi",
    "جربت خدمة الفيتامينات الوريدية وكانت تجربة ممتازة جدًا، الفريق محترف والتعامل راقٍ والمواعيد دقيقة. أكيد مو آخر مرة.":
        "I tried the IV vitamin service and it was an excellent experience. The team is professional, kind and on time. Definitely not my last time.",
    "محمد – جدة": "Mohammed, Jeddah",
    "تعامل محترم جدًا واهتمام حقيقي بالمريض، خصوصًا المتابعة بعد الزيارة. هذا الشيء نادر اليوم.":
        "Very respectful, with real care for the patient, especially the follow-up after the visit. That's rare these days.",
    "نوف العتيبي": "Nouf Al-Otaibi",
    "كنت متخوفة بالبداية بالتعامل مع شركات رعاية منزلية مرة ثانية، لكن بعد أول زيارة عرفت الفرق فعلًا. مستوى الخدمة ممتاز ويستحق الثقة.":
        "At first I was worried about using a home care company again, but after the first visit I really saw the difference. The service is excellent and worth your trust.",
    # Why us
    "لماذا يختارُنا أهل جدة؟": "Why do Jeddah families choose us?",
    "الثقة المطلقة": "Complete trust", "طاقم طبي مرخص ومعتمد وفق أعلى المعايير الصحية المحلية والعالمية": "A licensed, accredited medical team that meets the highest local and international health standards",
    "السرعة الذكية": "Smart speed", "نظام استجابة سريع يضمن وصول الفريق الطبي في وقت قياسي إلى منزلك": "A fast response system that gets the medical team to your home in record time",
    "الخصوصية التامة": "Full privacy", "نحترم خصوصية المنزل ونقدم خدماتنا في بيئة آمنة وهادئة للمريض": "We respect the privacy of your home and care for the patient in a safe, calm setting",
    "التعامل الإنساني": "Human care", 'شعارنا "نرعاكم كأهلُنا" ليس مجرد كلمات، بل منهج عمل يومي': 'Our motto "We care for you like family" isn\'t just words. It\'s how we work every day.',
    # Steps
    "تجربة حجز أسهل من طلب قهوة": "Booking that's easier than ordering a coffee",
    "التسجيل برقم الجوال فقط": "Sign up with just your mobile number",
    "طلب الخدمة": "Book a service", "تحديد نوع الرعاية المطلوب": "Choose the type of care you need",
    "الدفع الذكي": "Smart payment", "كاش باك فوري في محفظتك": "Instant cashback in your wallet",
    "تتبع مباشر": "Live tracking", "متابعة الفريق على الخريطة": "Follow the team on the map",
    "الرعاية المستمرة": "Ongoing care", "إشعارات الأدوية والمتابعة": "Medication and follow-up reminders",
    # FAQ
    "أسئلة تراودكم .. وإجابات نعتز بها": "Your questions.. and answers we're proud of",
    "نحن هنا لنزيل عنكم أي تساؤل ، ولنضع بين أيديكم كل ما يمنحكم الراحة.": "We're here to answer every question and give you everything you need to feel at ease.",
    "كيف أضمن كفاءة الفريق الطبي القادم لمنزلي؟": "How can I be sure the medical team coming to my home is qualified?",
    "في مدى كير، لا نختار إلا الأفضل. جميع كوادرنا الطبية (أطباء، ممرضين، وفنيين) مرخصين ومعتمدين من الهيئة السعودية للتخصصات الصحية، ويخضعون لتدريب مستمر ليس فقط على الجانب الطبي، بل على «فن التعامل الإنساني» لضمان أن تكون الزيارة تجربة مريحة وآمنة لأحبتكم.":
        "At Mada Care, we only choose the best. All our medical staff (doctors, nurses and technicians) are licensed and accredited by the Saudi Commission for Health Specialties, and receive ongoing training not only in medicine but in “the art of human care”, so every visit is comfortable and safe for your loved ones.",
    "ما هي سرعة الاستجابة عند طلب الخدمة؟": "How fast do you respond when I request a service?",
    "نحن ندرك أن الوقت هو أغلى ما نملكه في ظروف المرض. لذلك، صممنا نظام استجابة ذكي يجعل متوسط وقت الرد لدينا لا يتجاوز دقيقة واحدة. بمجرد تأكيد طلبك، ستحصل على إشعار بتفاصيل الفريق وتوقيت وصوله المتوقع إلى باب منزلك.":
        "We know time is the most precious thing when someone is unwell. That's why we built a smart response system that keeps our average reply time to no more than one minute. Once your request is confirmed, you'll get a notification with the team's details and their expected arrival time at your door.",
    "هل تتوفر لديكم خدمات طارئة؟": "Do you offer emergency services?",
    "مدى كير تقدم رعاية منزلية تخصصية ومجدولة مع وجود إمكانية لاستقبال الحالات الطارئة، وإذا كانت الحالة تستدعي تدخلاً طارئاً وفورياً (مثل صعوبات التنفس الحادة أو الحوادث) يمكننا نقل الحالة بسيارة إسعاف إلى أقرب مستشفى أو الهلال الأحمر.":
        "Mada Care provides specialised, scheduled home care and can also take urgent cases. If a case needs immediate emergency help (such as severe breathing difficulty or an accident), we can transfer the patient by ambulance to the nearest hospital or the Red Crescent.",
    "هل يمكنني متابعة موقع الطبيب وهو في طريقه إليّ؟": "Can I track the doctor while they're on the way to me?",
    "بالتأكيد! هذا هو جوهر التزامنا بالشفافية والراحة. من خلال تطبيق «مدى كير»، يمكنك تتبع مسار الفريق الطبي مباشرة على الخريطة ومعرفة الوقت المتبقي لوصولهم بدقة، تماماً كما تتابع رحلتك المفضلة، وأيضاً يمكنك التحدث مباشرة من خلال شات مخصص مع الفريق الطبي أثناء قدومه لمنزلك.":
        "Absolutely! This is at the heart of our commitment to transparency and comfort. In the Mada Care app, you can follow the medical team live on the map and see exactly how long until they arrive, just like tracking a ride. You can also chat with the medical team directly in a dedicated chat while they're on their way to you.",
    "ماذا لو احتجت إلى متابعة حالتي بعد مغادرة الفريق الطبي؟": "What if I need follow-up after the medical team leaves?",
    "علاقتنا لا تنتهي بمغادرة باب المنزل. نحن نقدم خدمة «المتابعة بعد الزيارة»، حيث يظل فريقنا على تواصل للاطمئنان على استقرار الحالة، ويمكنك الوصول لسجلك الطبي الكامل، نتائج تحاليلك، وخططك العلاجية في أي وقت ومن أي مكان عبر التطبيق.":
        "Our relationship doesn't end at your door. We offer “follow-up after the visit”: our team stays in touch to make sure the condition is stable, and you can see your full medical record, test results and treatment plans anytime, anywhere in the app.",
    "هل خدماتكم تشمل جميع أحياء مدينة جدة؟": "Do you cover every neighbourhood in Jeddah?",
    "نعم، نحن نغطي كافة أنحاء مدينة جدة، ونسعى دائماً لتوسيع نطاق تغطيتنا لضمان وصول «مدى كير» لكل منزل يحتاج إلى رعاية إنسانية واحترافية.":
        "Yes, we cover all of Jeddah, and we're always working to expand our coverage so Mada Care can reach every home that needs caring, professional care.",
    "كيف يمكنني استلام نتائج الفحوصات المخبرية؟": "How do I get my lab test results?",
    "كل شيء رقمي وسهل، ستصلك نتائج تحاليلك المخبرية مباشرة عبر التطبيق فور صدورها، مع شرح مبسط للنتائج لضمان أن تكون الصورة واضحة أمامكم دائماً.":
        "Everything is digital and easy. Your lab results arrive in the app as soon as they're ready, with a simple explanation so you always have a clear picture.",
    "لا تزال لديك أسئلة؟": "Still have questions?", "تواصل مع فريقنا مباشرة": "Talk to our team directly",
    # App section
    "نرعاكُم كأهلُنا .. ونصلكم بضغطة زر": "We care for you like family.. and we're one tap away",
    "حمِّل التطبيق الآن...": "Download the app now...",
    "الرعاية الطبية صارت أقرب لك، احجز زيارة منزلية بدقايق وخلّ الطبيب أو الممرض يوصلك وين ما كنت.":
        "Medical care is now closer to you. Book a home visit in minutes and the doctor or nurse will come to you wherever you are.",
    "تقدر تتابع ملف مريضك وتقاريره، وتبقى على تواصل مع فريق الرعاية في أي وقت، من غير زحمة ولا انتظار. الراحة والأمان صاروا بين يدينك.":
        "Follow your patient's file and reports and stay in touch with the care team anytime, with no traffic and no waiting. Comfort and safety, right in your hands.",
    # Footer
    "نجمع بين أمان الرعاية العائلية وسرعة الخدمات الرقمية، لننقل أفضل الخدمات الطبية إلى باب منزلك بكل سهولة وراحة.":
        "We bring together the safety of family care and the speed of digital services, to bring the best medical care to your door with ease and comfort.",
    "بيانات الشركة": "Company details", "شركة المستقبل الذكية للخدمات الطبية": "Future Smart Medical Services Company",
    "السجل التجاري:": "CR No.:", "الرقم الضريبي:": "VAT No.:", "جدة، المملكة العربية السعودية": "Jeddah, Saudi Arabia",
    "روابط سريعة": "Quick links", "اتصل بنا": "Contact us", "روابط مهمة": "Important links",
    "سياسة الخصوصية": "Privacy policy", "حقوق المرضى": "Patient rights",
    "سياسة الإلغاء وإعادة الجدولة وعدم التواجد في المنزل": "Cancellation, rescheduling and no-show policy",
    "ابقَ على اطلاع 💚": "Stay in the loop 💚",
    "انضم إلى مجتمع مدى كير، وكن أول من يعرف جديد خدماتنا ومبادراتنا الصحية.": "Join the Mada Care community and be the first to hear about our new services and health initiatives.",
    "اشترك الآن": "Subscribe", "أدخل بريدك الإلكتروني": "Enter your email",
    "نحترم خصوصيتك، ولن نشارك بريدك الإلكتروني مع الآخرين.": "We respect your privacy and won't share your email with anyone.",
    "شكرًا لانضمامك إلينا 💚": "Thanks for joining us 💚",
    "يسعدنا وجودك في مجتمع مدى كير. سنبقيك على اطلاع بكل جديد يهم صحتك وصحة عائلتك.": "We're glad to have you in the Mada Care community. We'll keep you posted on everything that matters for your health and your family's.",
    "جميع الحقوق محفوظة مدى كير للرعاية الصحية المنزلية @ 2026": "© 2026 Mada Care Home Healthcare. All rights reserved.",
    "واتساب": "WhatsApp", "البريد الإلكتروني": "Email", "تواصل معنا على واتساب": "Chat with us on WhatsApp",
    # Booking form
    "اترك بياناتك، وسيتواصل معك فريقنا لتأكيد الموعد.": "Leave your details and our team will contact you to confirm the appointment.",
    "الاسم": "Name", "رقم الجوال": "Mobile number", "الخدمة": "Service", "اختر الخدمة": "Choose a service",
    "ملاحظات (اختياري)": "Notes (optional)", "إرسال الطلب": "Send request",
    "بإرسال الطلب، أنت توافق على": "By sending this request, you agree to our", "و": "and our ", "سياسة الإلغاء": "cancellation policy",
    "وصلنا طلبك": "We got your request", "رقم طلبك": "Your request number",
    ". سيتواصل معك فريقنا قريباً لتأكيد الموعد.": ". Our team will contact you soon to confirm the appointment.", "تم": "Done",
    "السعودية": "Saudi Arabia", "الهند": "India", "مصر": "Egypt", "الفلبين": "Philippines", "السودان": "Sudan", "باكستان": "Pakistan",
    # Contact page
    "اتصل بنا | مدى كير للرعاية الصحية المنزلية": "Contact us | Mada Care Home Healthcare",
    "تواصل مع مدى كير للرعاية الصحية المنزلية في جدة عبر واتساب أو الاتصال المباشر، فريقنا هنا لمساعدتك.":
        "Contact Mada Care Home Healthcare in Jeddah on WhatsApp or by phone. Our team is here to help.",
    "نسعد بتواصلك معنا 💚": "We'd love to hear from you 💚",
    "نحن هنا للإجابة عن استفساراتك ومساعدتك في الوصول إلى الخدمة المناسبة.": "We're here to answer your questions and help you find the right service.",
    "تواصل عبر واتساب": "Chat on WhatsApp", "راسل فريق مدى كير وسنساعدك.": "Message the Mada Care team and we'll help you.",
    "ابدأ المحادثة": "Start a chat", "تحدث مباشرة مع فريق خدمة العملاء.": "Talk directly to our customer care team.",
    "اتصل الآن": "Call now", "موقعنا": "Our location", "جدة، المملكة العربية السعودية.": "Jeddah, Saudi Arabia.",
    "6895 طاهر العمراني، حي أبحر الجنوبية، جدة 23734": "6895 Taher Al-Omrani, Abhur Al-Janubiyah, Jeddah 23734",
    "مدى كير – نرعاكم كأهلنا 💚": "Mada Care – We care for you like family 💚",
}

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from en_pages import T2
T.update(T2)

# Pages that have an English copy: Arabic path -> English path.
PAGES = {"/": "/en/"}
for _loc in re.findall(r"<loc>https://madacare\.sa(/[^<]*)</loc>", open("sitemap.xml", encoding="utf-8").read()):
    if _loc != "/" and not _loc.startswith("/en/"):
        PAGES[_loc] = "/en" + _loc
# Longer paths first, so "/blog/x/" is rewritten before "/blog/".
PAGES = dict(sorted(PAGES.items(), key=lambda kv: -len(kv[0])))
missing = []


def tr(t):
    k = t.strip()
    if not AR.search(k):
        return t
    if k not in T:
        missing.append(k)
        return t
    lead, tail = t[: len(t) - len(t.lstrip())], t[len(t.rstrip()):]
    return lead + T[k] + tail


def esc(v):
    return v.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def translate(s, ar_path, en_path):
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", s, flags=re.S)
    s = s.replace('<html lang="ar" dir="rtl">', '<html lang="en" dir="ltr">', 1)
    s = s.replace('content="ar_SA"', 'content="en_US"')
    canon = f'<link rel="canonical" href="https://madacare.sa{ar_path}">'
    assert canon in s, ar_path
    s = s.replace(canon, f'<link rel="canonical" href="https://madacare.sa{en_path}">\n' + alt_links(ar_path, en_path))
    s = s.replace(f'content="https://madacare.sa{ar_path}"', f'content="https://madacare.sa{en_path}"')
    # Relative paths become absolute so they work from /en/.
    for a in ("assets/", "fonts/", "site.css", "site.js", "site-config.js"):
        s = re.sub(rf'(src|href)="{re.escape(a)}', rf'\1="/{a}', s)
    s = re.sub(r'(srcset)="assets/', r'\1="/assets/', s).replace(", assets/", ", /assets/")
    s = s.replace('href="#top"', f'href="{en_path}"')
    if ar_path == "/":
        for k in ("about", "services", "blog", "download"):
            s = s.replace(f'href="#{k}"', f'href="/en/#{k}"')
    for a, e in PAGES.items():
        s = s.replace(f'href="{a}#', f'href="{e}#').replace(f'href="{a}"', f'href="{e}"')
    # Text between tags (skip scripts and styles), then attributes.
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", s, flags=re.S)
    for i in range(0, len(parts), 2):
        p = re.sub(r">([^<]+)<", lambda m: ">" + tr(m.group(1)) + "<", parts[i])
        parts[i] = re.sub(r'\b(alt|aria-label|placeholder|content|title)="([^"]*)"',
                          lambda m: f'{m.group(1)}="{esc(tr(m.group(2)))}"' if AR.search(m.group(2)) else m.group(0), p)
    s = "".join(parts)
    # The language button points back to Arabic.
    s = s.replace('<button type="button" class="globe" aria-label="العربية">', '<button type="button" class="globe" aria-label="العربية" lang="ar">')
    return s


def alt_links(ar_path, en_path):
    return (f'<link rel="alternate" hreflang="ar" href="https://madacare.sa{ar_path}">\n'
            f'<link rel="alternate" hreflang="en" href="https://madacare.sa{en_path}">\n'
            f'<link rel="alternate" hreflang="x-default" href="https://madacare.sa{ar_path}">')


for ar_path, en_path in PAGES.items():
    src = "index.html" if ar_path == "/" else ar_path.strip("/") + "/index.html"
    s = open(src, encoding="utf-8").read()
    # Arabic page: add hreflang links once.
    canon = f'<link rel="canonical" href="https://madacare.sa{ar_path}">'
    if 'hreflang="en"' not in s:
        s = s.replace(canon, canon + "\n" + alt_links(ar_path, en_path), 1)
        open(src, "w", encoding="utf-8").write(s)
    out = en_path.strip("/") + "/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(translate(s, ar_path, en_path))

# Sitemap: add the English pages.
sm = open("sitemap.xml", encoding="utf-8").read()
for en_path in PAGES.values():
    loc = f"<loc>https://madacare.sa{en_path}</loc>"
    if loc not in sm:
        sm = sm.replace("</urlset>", f"  <url>{loc}</url>\n</urlset>")
open("sitemap.xml", "w", encoding="utf-8").write(sm)

if missing:
    print("MISSING translations:", len(dict.fromkeys(missing)))
    open("/tmp/en_missing.txt", "w", encoding="utf-8").write("\n".join(dict.fromkeys(missing)))
    sys.exit(1)
print("ok:", ", ".join(PAGES.values()))
