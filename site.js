// Mada Care website behavior. Settings are in site-config.js.
(() => {
  const C = (typeof MADA_SITE !== "undefined" && MADA_SITE) || {}, $ = id => document.getElementById(id), $$ = s => [...document.querySelectorAll(s)];
  const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  const TZ = "Asia/Riyadh";
  // English pages (/en/) use lang="en"; L(ar, en) picks the text for the page language.
  const EN = document.documentElement.lang === "en", L = (ar, en) => EN ? en : ar;
  const parts = (d, o) => Object.fromEntries(new Intl.DateTimeFormat("ar-SA-u-ca-gregory-nu-latn", { timeZone: TZ, ...o }).formatToParts(d).map(p => [p.type, p.value]));

  // Mobile menu.
  const menu = $("menu"), burger = $("burger");
  burger.addEventListener("click", () => { const o = menu.classList.toggle("open"); burger.setAttribute("aria-expanded", o); });
  menu.addEventListener("click", e => { if (e.target.closest("a")) { menu.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); } });

  // FAQ accordion.
  $$(".qa-h").forEach(b => b.addEventListener("click", () => {
    const qa = b.parentElement, o = !qa.classList.contains("open");
    $$(".qa.open").forEach(x => { x.classList.remove("open"); x.querySelector(".qa-h").setAttribute("aria-expanded", "false"); });
    qa.classList.toggle("open", o); b.setAttribute("aria-expanded", o);
  }));

  // Testimonials carousel.
  const track = $("tst");
  if (track) {
  const cards = [...track.children], dots = $("dots");
  cards.forEach((c, i) => { const b = document.createElement("button"); b.type = "button"; b.setAttribute("aria-label", L(`رأي ${i + 1}`, `Review ${i + 1}`)); b.addEventListener("click", () => go(i)); dots.appendChild(b); });
  dots.removeAttribute("aria-hidden");
  let cur = 0;
  function go(i) {
    cur = Math.max(0, Math.min(cards.length - 1, i));
    const tr = track.getBoundingClientRect(), cr = cards[cur].getBoundingClientRect(), cs = getComputedStyle(track);
    // Arabic lines cards up on the right edge, English on the left.
    track.scrollBy({ left: EN ? cr.left - (tr.left + (parseFloat(cs.paddingLeft) || 0)) : cr.right - (tr.right - (parseFloat(cs.paddingRight) || 0)), behavior: "smooth" });
    mark();
  }
  function mark() { [...dots.children].forEach((d, i) => d.setAttribute("aria-current", i === cur)); }
  let tmr;
  track.addEventListener("scroll", () => { clearTimeout(tmr); tmr = setTimeout(() => {
    const tr = track.getBoundingClientRect(), cs = getComputedStyle(track), padR = parseFloat(cs.paddingRight) || 0, padL = parseFloat(cs.paddingLeft) || 0;
    let best = 0, bd = Infinity; cards.forEach((c, i) => { const r = c.getBoundingClientRect(), dd = EN ? Math.abs(r.left - (tr.left + padL)) : Math.abs(r.right - (tr.right - padR)); if (dd < bd) { bd = dd; best = i; } });
    cur = best; mark();
  }, 80); });
  $$(".pg").forEach(b => b.addEventListener("click", () => go(cur + (b.dataset.dir === "next" ? 1 : -1))));
  mark();
  }

  // Links from the settings. Empty settings keep the design's buttons and say the link is coming.
  const toast = msg => {
    let t = $("siteToast");
    if (!t) { t = document.createElement("div"); t.id = "siteToast"; t.setAttribute("role", "status"); t.style.cssText = "position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:120;background:#194136;color:#fff;padding:12px 18px;border-radius:8px;font-size:14px;box-shadow:0 12px 24px -8px rgba(0,0,0,.3)"; document.body.appendChild(t); }
    t.textContent = msg; t.hidden = false; clearTimeout(t._h); t._h = setTimeout(() => { t.hidden = true; }, 3200);
  };
  const wa = C.whatsapp ? "https://wa.me/" + String(C.whatsapp).replace(/\D/g, "") : "";
  const ext = (a, url) => { a.href = url; if (/^https?:/.test(url)) { a.target = "_blank"; a.rel = "noopener"; } };
  const isApple = /iPhone|iPad|iPod|Macintosh/.test(navigator.userAgent);
  $$("[data-app]").forEach(a => {
    const url = isApple ? (C.appStore || C.googlePlay) : (C.googlePlay || C.appStore);
    if (url) ext(a, url); else a.addEventListener("click", e => { e.preventDefault(); toast(L("تطبيق مدى كير قريباً على المتاجر", "The Mada Care app is coming soon to the stores")); });
  });
  [["[data-gp]", C.googlePlay], ["[data-as]", C.appStore]].forEach(([s, url]) => $$(s).forEach(a => {
    if (url) ext(a, url); else a.addEventListener("click", e => { e.preventDefault(); toast(L("تطبيق مدى كير قريباً على المتاجر", "The Mada Care app is coming soon to the stores")); });
  }));
  const so = C.social || {};
  $$("[data-so]").forEach(a => {
    const k = a.dataset.so, url = k === "whatsapp" ? wa : k === "email" ? (so.email ? "mailto:" + so.email : "") : so[k];
    if (url) ext(a, url); else { a.setAttribute("aria-disabled", "true"); a.addEventListener("click", e => e.preventDefault()); }
  });
  // "Need help?" buttons open a small dialog: WhatsApp, call, or (with neither number set) the booking form.
  // data-help="ask" (FAQ "تواصل مع فريقنا مباشرة") shows the "another question?" version with one button.
  let helpOv = null;
  const telNo = String(C.phone || "").replace(/[^\d+]/g, "");
  function openHelp(kind) {
    if (!helpOv) {
      helpOv = document.createElement("div");
      helpOv.className = "ov help-ov"; helpOv.hidden = true;
      document.body.appendChild(helpOv);
      const close = () => { helpOv.hidden = true; document.body.style.overflow = ""; };
      helpOv.addEventListener("click", e => {
        if (e.target === helpOv || e.target.closest("[data-hclose]")) close();
        else if (e.target.closest("[data-help-book]")) { close(); openBook(); }
        else if (e.target.closest("[data-help-wa]")) { gtmEvent("whatsapp_click", { area: "help_dialog" }); close(); }
        else if (e.target.closest("[data-help-call]")) { gtmEvent("call_click", { area: "help_dialog" }); close(); }
      });
      document.addEventListener("keydown", e => { if (e.key === "Escape" && !helpOv.hidden) close(); });
    }
    const waBtn = label => `<a class="help-btn help-wa" data-help-wa href="${wa}" target="_blank" rel="noopener"><img src="/assets/ic-whatsapp-btn.svg" alt="" width="24" height="24"><span>${label}</span></a>`;
    const callBtn = (label, cls) => `<a class="help-btn ${cls}" data-help-call href="tel:${telNo}"><img src="/assets/ic-phone${cls === "help-wa" ? "" : "-dark"}.svg" alt="" width="20" height="20"><span>${label}</span></a>`;
    const bookBtn = `<button type="button" class="help-btn help-wa" data-help-book><span>${L("احجز موعدك وسنتواصل معك", "Book now and we'll contact you")}</span></button>`;
    let title, sub, acts, foot;
    if (kind === "ask") {
      title = L("هل لديك استفسار آخر؟ 💚", "Have another question? 💚"); sub = L("فريق مدى كير هنا لمساعدتك والإجابة عن جميع استفساراتك.", "The Mada Care team is here to help and answer all your questions."); foot = L("نرعاكم كأهلنا 💚", "We care for you like family 💚");
      const team = L("تواصل مع فريق مدى كير", "Contact the Mada Care team");
      acts = wa ? waBtn(team) : telNo ? callBtn(team, "help-wa") : bookBtn;
    } else {
      title = L("تحتاج مساعدة؟ 💚", "Need help? 💚"); sub = L("يسعدنا مساعدتك، تواصل معنا بالطريقة المناسبة لك.", "We're happy to help. Reach us whichever way suits you."); foot = L("فريقنا دائماً في خدمتك 💚", "Our team is always here for you 💚");
      acts = (wa ? waBtn(L("تواصل عبر واتساب", "Chat on WhatsApp")) : "") + (telNo ? callBtn(L("اتصل بنا", "Call us"), "help-call") : "") || bookBtn;
    }
    helpOv.innerHTML = `<div class="dlg help-dlg" role="dialog" aria-modal="true" aria-labelledby="helpT">
        <button type="button" class="dlg-x" data-hclose aria-label="${L("إغلاق", "Close")}">×</button>
        <h2 id="helpT">${title}</h2>
        <p class="dlg-sub">${sub}</p>
        <div class="help-acts">${acts}</div>
        <p class="help-foot">${foot}</p>
      </div>`;
    helpOv.hidden = false; document.body.style.overflow = "hidden";
    setTimeout(() => { const f = helpOv.querySelector(".help-btn"); if (f) f.focus(); }, 30);
  }
  // Language button (globe): opens "choose language"; picking the other language opens the same page in it (/en/... <-> /...).
  let langOv = null;
  function openLang() {
    const p = location.pathname, other = (EN ? (p.replace(/^\/en(\/|$)/, "/") || "/") : "/en" + p) + location.hash;
    if (!langOv) {
      langOv = document.createElement("div");
      langOv.className = "ov lang-ov"; langOv.hidden = true;
      langOv.innerHTML = `<div class="dlg lang-dlg" role="dialog" aria-modal="true" aria-labelledby="langT">
          <button type="button" class="dlg-x" data-lclose aria-label="${L("إغلاق", "Close")}">×</button>
          <h2 id="langT">${L("اختر اللغة", "Choose language")}</h2>
          <div class="lang-opts">
            <a class="lang-opt${EN ? " on" : ""}" lang="en" hreflang="en" href="${EN ? "#" : other}"${EN ? ' aria-current="true" data-lclose' : ""}>English</a>
            <a class="lang-opt${EN ? "" : " on"}" lang="ar" hreflang="ar" href="${EN ? other : "#"}"${EN ? "" : ' aria-current="true" data-lclose'}>العربية</a>
          </div>
        </div>`;
      document.body.appendChild(langOv);
      const close = () => { langOv.hidden = true; document.body.style.overflow = ""; };
      langOv.addEventListener("click", e => { const x = e.target.closest("[data-lclose]"); if (e.target === langOv || x) { if (x) e.preventDefault(); close(); } });
      document.addEventListener("keydown", e => { if (e.key === "Escape" && !langOv.hidden) close(); });
    }
    langOv.hidden = false; document.body.style.overflow = "hidden";
    setTimeout(() => { const f = langOv.querySelector(".lang-opt:not(.on)"); if (f) f.focus(); }, 30);
  }
  $$(".globe").forEach(b => b.addEventListener("click", openLang));
  $$("[data-help]").forEach(a => a.addEventListener("click", e => { e.preventDefault(); openHelp(a.dataset.help); }));
  // Contact page buttons: WhatsApp / call when the numbers are set, otherwise the booking form.
  $$("[data-wa-link]").forEach(a => { if (wa) ext(a, wa); else a.addEventListener("click", e => { e.preventDefault(); openBook(); }); });
  $$("[data-tel-link]").forEach(a => { if (telNo) a.href = "tel:" + telNo; else a.addEventListener("click", e => { e.preventDefault(); openBook(); }); });
  const wf = $("waFloat");
  if (wa) ext(wf, wa); else wf.addEventListener("click", e => { e.preventDefault(); openBook(); });
  // "Need help?" bubble next to the WhatsApp button: once per visitor, 5s after arriving, hides after 6s or on tap.
  if (wf && !store.get("mada-wa-bubble")) setTimeout(() => {
    store.set("mada-wa-bubble", "1");
    const bb = document.createElement("button");
    bb.type = "button"; bb.className = "wa-bubble"; bb.textContent = L("تحتاج مساعدة؟ 💚", "Need help? 💚");
    document.body.appendChild(bb);
    requestAnimationFrame(() => bb.classList.add("in"));
    const hide = () => { bb.classList.remove("in"); setTimeout(() => bb.remove(), 300); };
    bb.addEventListener("click", () => { hide(); wf.click(); });
    wf.addEventListener("click", hide, { once: true });
    setTimeout(hide, 6000);
  }, 5000);
  const tel = telNo;
  // Call button: opens a WhatsApp chat when a WhatsApp number is set, otherwise a phone call.
  // Call button: WhatsApp chat when a WhatsApp number is set, else a phone call; with neither it opens the booking form (data-book).
  $$("[data-call]").forEach(a => { const go = u => { delete a.dataset.book; a.href = u; a.hidden = false; }; if (wa) { go(wa); a.target = "_blank"; a.rel = "noopener"; } else if (tel) go("tel:" + tel); });
  $$("[data-phone]").forEach(a => { if (tel) { a.href = "tel:" + tel; a.textContent = C.phone; a.closest("[data-phone-row]").hidden = false; } });
  if (C.crNumber) ["crNo", "crNo2"].forEach(k => { if ($(k)) $(k).textContent = C.crNumber; });
  $$("[data-soon]").forEach(a => a.addEventListener("click", e => { e.preventDefault(); toast(L("هذه الصفحة قيد البناء في الورشة", "This page is coming soon")); }));
  if (C.vatNumber && $("vatNo")) $("vatNo").textContent = C.vatNumber;
  if ($("vatRow") && !/[1-9]/.test(C.vatNumber || "")) $("vatRow").hidden = true;  // placeholder VAT stays hidden until the real number is set

  // Where the visitor came from (ad campaign, search, another site). Kept 30 days; a plain direct visit does not overwrite an ad visit.
  const ATTR_KEY = "mada_attr", ATTR_DAYS = 30;
  (() => {
    const q = new URLSearchParams(location.search), utm = {};
    ["source", "medium", "campaign", "term", "content"].forEach(k => { const v = q.get("utm_" + k); if (v) utm[k] = v.slice(0, 120); });
    const ids = {};
    ["gclid", "gbraid", "wbraid", "fbclid", "ttclid", "ScCid", "twclid", "msclkid"].forEach(k => { const v = q.get(k); if (v) ids[k] = v.slice(0, 200); });
    let ref = "";
    try { const r = document.referrer && new URL(document.referrer); if (r && r.hostname !== location.hostname) ref = r.hostname; } catch (e) {}
    const guess = ids.gclid || ids.gbraid || ids.wbraid ? ["google", "cpc"] : ids.fbclid ? ["meta", "paid_social"] : ids.ttclid ? ["tiktok", "paid_social"]
      : ids.ScCid ? ["snapchat", "paid_social"] : ids.twclid ? ["x", "paid_social"] : ids.msclkid ? ["bing", "cpc"]
      : /google\./.test(ref) ? ["google", "organic"] : /bing\./.test(ref) ? ["bing", "organic"] : ref ? [ref, "referral"] : null;
    if (!utm.source && !guess) return;  // direct visit: keep what we had
    const a = { source: utm.source || guess[0], medium: utm.medium || guess[1], campaign: utm.campaign || null, term: utm.term || null, content: utm.content || null,
      ids: Object.keys(ids).length ? ids : null, referrer: ref || null, landing: location.pathname, at: new Date().toISOString() };
    store.set(ATTR_KEY, JSON.stringify(a));
  })();
  const attribution = () => {
    try {
      const a = JSON.parse(store.get(ATTR_KEY) || "null");
      if (a && Date.now() - Date.parse(a.at) < ATTR_DAYS * 864e5) return a;
    } catch (e) {}
    return { source: "direct", medium: null, campaign: null };
  };

  // Booking request: one new row in the dashboard's requests (Requests page, source "website", on hold until the call center calls).
  const ov = $("bookOv"), form = $("bookForm"), err = $("bkErr");
  let lastFocus = null;
  const inline = ov.classList.contains("ov-inline"); // booking page: the form sits in the page instead of a popup
  function openBook(svc) {
    if (inline) {
      $("bkForm").hidden = false; $("bkDone").hidden = true;
      if (svc) $("bkSvc").value = svc;
      ov.scrollIntoView({ behavior: "smooth", block: "center" }); setTimeout(() => $("bkName").focus({ preventScroll: true }), 300);
      return;
    }
    lastFocus = document.activeElement;
    $("bkForm").hidden = false; $("bkDone").hidden = true; err.hidden = true;
    form.querySelectorAll("[aria-invalid]").forEach(x => x.removeAttribute("aria-invalid"));
    if (svc) $("bkSvc").value = svc;
    ov.hidden = false; document.body.style.overflow = "hidden";
    setTimeout(() => $("bkName").focus(), 30);
  }
  function closeBook() { if (inline) { $("bkForm").hidden = false; $("bkDone").hidden = true; return; } ov.hidden = true; document.body.style.overflow = ""; if (lastFocus) lastFocus.focus(); }
  $$("[data-book]").forEach(el => {
    const fire = e => { e.preventDefault(); openBook(el.dataset.svc); };
    el.addEventListener("click", fire);
    if (el.tagName !== "A") el.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") fire(e); });
  });
  ov.addEventListener("click", e => { if ((e.target === ov && !inline) || e.target.closest("[data-close]")) closeBook(); });
  document.addEventListener("keydown", e => {
    if (ov.hidden || inline) return;
    if (e.key === "Escape") closeBook();
    if (e.key === "Tab") {
      const f = [...ov.querySelectorAll("button, input, select, textarea, a[href]")].filter(x => x.offsetParent);
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });
  const latin = v => v.replace(/[٠-٩]/g, d => "٠١٢٣٤٥٦٧٨٩".indexOf(d)).replace(/[۰-۹]/g, d => "۰۱۲۳۴۵۶۷۸۹".indexOf(d));
  $("bkMobile").addEventListener("input", e => { e.target.value = latin(e.target.value).replace(/\D/g, "").slice(0, 10); });
  const bad = (el, msg) => { el.setAttribute("aria-invalid", "true"); err.textContent = msg; err.hidden = false; el.focus(); return false; };
  function valid() {
    form.querySelectorAll("[aria-invalid]").forEach(x => x.removeAttribute("aria-invalid")); err.hidden = true;
    if ($("bkName").value.trim().length < 2) return bad($("bkName"), L("اكتب الاسم.", "Please enter your name."));
    if (!/^05\d{8}$/.test($("bkMobile").value)) return bad($("bkMobile"), L("اكتب رقم جوال صحيح يبدأ بـ 05 ومكوّن من 10 أرقام.", "Enter a valid 10-digit mobile number starting with 05."));
    if (!$("bkSvc").value) return bad($("bkSvc"), L("اختر الخدمة.", "Please choose a service."));
    return true;
  }
  // Home page lead form (name, mobile, service): fills the booking form and sends it, so errors and the confirmation show in the same popup.
  const lead = $("leadForm");
  if (lead) lead.addEventListener("submit", e => {
    e.preventDefault();
    $("bkName").value = $("ldName").value; $("bkMobile").value = $("ldMobile").value.replace(/\D/g, "");
    openBook($("ldSvc").value);
    form.requestSubmit();
  });
  form.addEventListener("submit", async e => {
    e.preventDefault();
    if (!valid()) return;
    const cloud = C.cloud || {};
    if (!cloud.url || !cloud.key) { err.textContent = L("الحجز من الموقع غير متاح حالياً، تواصل معنا عبر واتساب.", "Online booking isn't available right now. Please contact us on WhatsApp."); err.hidden = false; return; }
    const btn = $("bkSend"); btn.disabled = true;
    const now = new Date().toISOString(), id = "WEB-" + Date.now().toString(36).toUpperCase().slice(-5) + Math.random().toString(36).slice(2, 5).toUpperCase();
    const ref = attribution(), name = $("bkName").value.trim(), mobile = $("bkMobile").value, service = $("bkSvc").value, note = $("bkNote").value.trim();
    const order = {
      id, createdAt: now, updatedAt: now, service, mobile, medical: "non", patient: { en: name, ar: name }, mrn: null, staff: null, staffId: null,
      source: "website", status: "on_hold", decision: "pending", payment: null, web: { name, note: note || null, at: now, ref, lang: EN ? "en" : "ar" },
      hold: { reason: "web", note: note || null, at: now, by: null, byId: null, view: "step1", snap: { mobile, source: "website", view: "step1", savedAt: now }, dueAt: now, action: "call", warned: null }
    };
    try {
      const res = await fetch(cloud.url.replace(/\/$/, "") + "/rest/v1/mada_data", {
        method: "POST",
        headers: { apikey: cloud.key, "Content-Type": "application/json", Prefer: "return=minimal", ...(String(cloud.key).split(".").length === 3 ? { Authorization: "Bearer " + cloud.key } : {}) },
        body: JSON.stringify({ k: "mada-orders", rid: id, v: JSON.stringify(order), pos: Math.floor(Date.now() / 1000) })
      });
      if (!res.ok) throw new Error(res.status);
      gtmEvent("booking_submit", { service, booking_source: ref.source, booking_medium: ref.medium, booking_campaign: ref.campaign });
      $("bkRef").textContent = id; $("bkForm").hidden = true; $("bkDone").hidden = false; form.reset();
      $("bkDone").querySelector("button").focus();
    } catch (x) {
      err.textContent = L("تعذّر إرسال الطلب، حاول مرة أخرى.", "We couldn't send your request. Please try again."); err.hidden = false;
    } finally { btn.disabled = false; }
  });

  // Subscribe: the email is saved to the shared database (mada_data, k "mada-newsletter"), one row per email.
  $("subForm").addEventListener("submit", async e => {
    e.preventDefault();
    const m = $("subMsg"), v = $("subEmail").value.trim().toLowerCase(), btn = $("subBtn");
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { m.textContent = L("اكتب بريداً إلكترونياً صحيحاً.", "Please enter a valid email."); m.hidden = false; return; }
    m.hidden = true;
    const cloud = C.cloud || {};
    btn.disabled = true;
    try {
      if (!cloud.url || !cloud.key) throw new Error("no cloud");
      const now = new Date().toISOString();
      const res = await fetch(cloud.url.replace(/\/$/, "") + "/rest/v1/mada_data", {
        method: "POST",
        headers: { apikey: cloud.key, "Content-Type": "application/json", Prefer: "return=minimal", ...(String(cloud.key).split(".").length === 3 ? { Authorization: "Bearer " + cloud.key } : {}) },
        body: JSON.stringify({ k: "mada-newsletter", rid: "NL-" + Date.now().toString(36).toUpperCase() + Math.random().toString(36).slice(2, 5).toUpperCase(), v: JSON.stringify({ email: v, at: now, page: location.pathname, lang: EN ? "en" : "ar", ref: attribution() }), pos: Math.floor(Date.now() / 1000) })
      });
      if (!res.ok) throw new Error(res.status);
      gtmEvent("newsletter_submit");
      $("subBody").hidden = true; $("subDone").hidden = false;
    } catch (x) {
      m.textContent = L("تعذّر الاشتراك الآن، حاول مرة أخرى.", "We couldn't subscribe you right now. Please try again."); m.hidden = false;
    } finally { btn.disabled = false; }
  });
})();

// Service cards on phones: dots follow the swipe
(() => {
  const row = document.querySelector(".svc-cards"), dots = document.querySelectorAll("#svcDots i");
  if (!row || !dots.length) return;
  const cards = [...row.children];
  const mark = () => {
    const r = row.getBoundingClientRect();
    let best = 0, bestD = Infinity;
    cards.forEach((c, i) => { const b = c.getBoundingClientRect(); const d = Math.abs(b.right - r.right); if (d < bestD) { bestD = d; best = i; } });
    dots.forEach((d, i) => d.classList.toggle("on", i === best));
  };
  row.addEventListener("scroll", () => requestAnimationFrame(mark), { passive: true });
  window.addEventListener("resize", mark);
  mark();
})();

// Marketing events for Google Tag Manager (GTM-THZZPBRT): each push carries the event name and where on the page the click came from.
function gtmEvent(event, extra) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push(Object.assign({ event }, extra || {}));
}
(() => {
  const where = el => {
    if (el.id === "waFloat") return "floating";
    const box = el.closest("header, footer, section, #bookOv");
    if (!box) return "page";
    if (box.tagName === "HEADER") return "header";
    if (box.tagName === "FOOTER") return "footer";
    if (box.id === "bookOv") return "booking_form";
    const names = { top: "hero", services: "services", help: "faq", download: "app_banner", about: "features" };
    return names[box.id] || box.id || box.className.split(" ")[0] || "page";
  };
  const rules = [
    ["[data-book]", "book_click"],
    ["[data-so=whatsapp], #waFloat", "whatsapp_click"],
    ["[data-as]", "app_store_click"],
    ["[data-gp]", "google_play_click"],
    ["[data-help]", "help_click"],
    ["[data-call], [data-tel-link]", "call_click"],
    ["[data-wa-link]", "whatsapp_click"]
  ];
  document.addEventListener("click", e => {
    for (const [sel, ev] of rules) {
      const el = e.target.closest(sel);
      if (el) {
        const extra = { click_location: where(el) };
        if (el.dataset.svc) extra.service = el.dataset.svc;
        gtmEvent(ev, extra);
        return;
      }
    }
  }, true);
})();

// Achievement numbers count up from 0 when they scroll into view.
(() => {
  const els = [...document.querySelectorAll(".num-big")];
  if (!els.length || !("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const parse = el => { const m = el.textContent.trim().match(/^(\D*)(\d+)(\D*)$/); return m && { pre: m[1], n: +m[2], post: m[3], text: el.textContent }; };
  const run = el => {
    const p = el._p, t0 = performance.now(), dur = 1600;
    const step = now => {
      const k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = p.pre + Math.round(p.n * e) + p.post;
      if (k < 1) requestAnimationFrame(step); else el.textContent = p.text;
    };
    requestAnimationFrame(step);
  };
  const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { io.unobserve(x.target); run(x.target); } }), { threshold: .6 });
  els.forEach(el => { const p = parse(el); if (!p) return; el._p = p; el.setAttribute("aria-label", p.text); el.textContent = p.pre + "0" + p.post; io.observe(el); });
})();

// Cards appear one after another and grow as they scroll into view.
(() => {
  if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const io = new IntersectionObserver(es => es.forEach(x => {
    if (!x.isIntersecting) return;
    io.unobserve(x.target); x.target.classList.add("in");
    setTimeout(() => x.target.style.removeProperty("--d"), 1400);
  }), { threshold: .2, rootMargin: "0px 0px -8% 0px" });
  [".feat-grid .fc", ".sc.why", ".ach .sc"].forEach(sel => document.querySelectorAll(sel).forEach((el, i) => {
    el.classList.add("rv"); el.style.setProperty("--d", (i % 4) * .12 + "s"); io.observe(el);
  }));
})();

// Booking steps: the section stays in place while scrolling moves from one step to the next, then the page carries on.
(() => {
  const sec = document.querySelector("section.steps");
  if (!sec || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const wrap = sec.querySelector(".wrap"), box = sec.querySelector(".st-scroll"), board = sec.querySelector(".st-board"), bar = sec.querySelector(".st-bar");
  const steps = [...sec.querySelectorAll(".st")];
  if (!wrap || !box || !board || !bar || steps.length < 2) return;
  const fill = document.createElement("i"); fill.className = "st-fill"; bar.prepend(fill);
  const ltr = document.documentElement.dir === "ltr";
  let on = false, top = 0, len = 0, W = 0, C = 0, sc = 1, d = [];
  const update = () => {
    if (!on) return;
    const p = Math.min(1, Math.max(0, (top - sec.getBoundingClientRect().top) / len));
    const k = Math.min(steps.length - 1, p / .85 * (steps.length - 1)), i = Math.floor(k), g = Math.min(1, Math.max(0, (k - i - .3) / .4)), f = g * g * (3 - 2 * g);
    const cur = d[i] + ((d[i + 1] ?? d[i]) - d[i]) * f;
    steps.forEach((s, j) => { s.classList.toggle("on", j <= i + f + .05); s.classList.toggle("cur", j === Math.round(i + f)); });
    fill.style.width = cur + "px";
    if (sc < 1) board.style.transform = `scale(${sc})`;
    else if (W > C) {
      const shift = Math.min(W - C, Math.max(0, cur - C / 2));
      board.style.transform = `translateX(${ltr ? -shift : -(W - C - shift)}px)`;
    }
  };
  const layout = () => {
    on = false; sec.style.height = ""; wrap.style.top = ""; board.style.transform = ""; box.style.height = "";
    sec.classList.add("pin");
    W = board.offsetWidth; C = box.clientWidth;
    // A board a little wider than the screen (laptops) is scaled down to fit; on phones it slides sideways instead.
    sc = W > C && C >= 700 ? C / W : 1;
    if (sc < 1) { board.style.transformOrigin = "0 0"; box.style.height = board.offsetHeight * sc + "px"; }
    const navH = (document.querySelector(".nav") || {}).offsetHeight || 0, h = wrap.offsetHeight;
    if (h + navH > innerHeight) { sec.classList.remove("pin"); board.style.transform = ""; box.style.height = ""; fill.style.width = "100%"; return; }
    top = Math.max(navH, navH + (innerHeight - navH - h) / 2);
    wrap.style.top = top + "px";
    len = steps.length * Math.min(260, innerHeight * .4);
    sec.style.height = h + len + "px";
    d = steps.map(s => ltr ? s.offsetLeft + s.offsetWidth / 2 : W - s.offsetLeft - s.offsetWidth / 2);
    on = true; update();
  };
  let raf = 0;
  addEventListener("scroll", () => { if (!raf) raf = requestAnimationFrame(() => { raf = 0; update(); }); }, { passive: true });
  // Phones fire resize when the address bar shows or hides; only lay out again for a real size change.
  let lw = innerWidth, lh = innerHeight;
  addEventListener("resize", () => { if (innerWidth !== lw || Math.abs(innerHeight - lh) > 150) { lw = innerWidth; lh = innerHeight; layout(); } });
  addEventListener("load", layout);
  layout();
})();

// Services page: rows slide in from their side, and the chip of the service on screen lights up.
(() => {
  const rows = [...document.querySelectorAll(".sx-row")], chips = [...document.querySelectorAll(".sx-chip")];
  if (!rows.length || !("IntersectionObserver" in window)) return;
  if (!matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { io.unobserve(x.target); x.target.classList.add("in"); } }), { threshold: .15 });
    rows.forEach(r => { r.classList.add("sx-js"); io.observe(r); });
  }
  const bar = document.querySelector(".sx-bar-in");
  const nav = document.querySelector(".nav"), sticky = document.querySelector(".sx-bar");
  const fitTop = () => { if (nav && sticky) sticky.style.top = nav.offsetHeight + "px"; };
  fitTop(); addEventListener("resize", fitTop);
  const mark = id => chips.forEach(c => {
    const on = c.getAttribute("href") === "#" + id;
    c.classList.toggle("on", on);
    if (on && bar) bar.scrollTo({ left: c.offsetLeft - (bar.clientWidth - c.offsetWidth) / 2, behavior: "smooth" });
  });
  const spy = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) mark(x.target.id); }), { rootMargin: "-45% 0px -50% 0px" });
  rows.forEach(r => spy.observe(r));
})();

// "بل نقدم شعوراً …": the last word cycles through the three things we focus on.
(() => {
  const w = document.querySelector(".ft-w[data-words]");
  if (!w) return;
  const words = w.dataset.words.split("|");
  const en = { "بالأمان": "of safety", "بالراحة": "of comfort", "بالطمأنينة": "of peace of mind" };
  const list = document.documentElement.lang === "en" ? words.map(x => en[x] || x) : words;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  let n = 0;
  setInterval(() => {
    w.classList.add("out");
    setTimeout(() => { n = (n + 1) % list.length; w.textContent = list[n]; w.classList.remove("out"); }, 350);
  }, 2200);
})();
