// Mada Care website behavior. Settings are in site-config.js.
(() => {
  const C = (typeof MADA_SITE !== "undefined" && MADA_SITE) || {}, $ = id => document.getElementById(id), $$ = s => [...document.querySelectorAll(s)];
  const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  const TZ = "Asia/Riyadh";
  const parts = (d, o) => Object.fromEntries(new Intl.DateTimeFormat("ar-SA-u-ca-gregory-nu-latn", { timeZone: TZ, ...o }).formatToParts(d).map(p => [p.type, p.value]));

  // Second nav: only the accessibility buttons (weather, date, time and city were removed at the client's request).

  // Last modified, in Saudi time.
  const lm = new Date(document.lastModified);
  if (!isNaN(lm) && $("lastMod")) {
    const d = parts(lm, { day: "2-digit", month: "2-digit", year: "numeric" }), t = parts(lm, { hour: "numeric", minute: "2-digit", hour12: true });
    $("lastMod").textContent = `تاريخ آخر تعديل: ${d.day}/${d.month}/${d.year} - ${t.hour}:${t.minute} ${/م|PM/i.test(t.dayPeriod || "") ? "م" : "ص"} بتوقيت السعودية`;
  }

  // Accessibility: text size, high contrast, read aloud.
  let zoom = parseFloat(store.get("mada-site-zoom")) || 1;
  const setZoom = z => { zoom = Math.min(1.3, Math.max(.9, Math.round(z * 10) / 10)); document.documentElement.style.setProperty("--zoom", zoom); store.set("mada-site-zoom", zoom); };
  setZoom(zoom);
  $("a11yZoomIn").addEventListener("click", () => setZoom(zoom + .1));
  $("a11yZoomOut").addEventListener("click", () => setZoom(zoom - .1));
  const hc = on => { document.documentElement.classList.toggle("hc", on); $("a11yView").setAttribute("aria-pressed", on); store.set("mada-site-hc", on ? "1" : ""); };
  hc(store.get("mada-site-hc") === "1");
  $("a11yView").addEventListener("click", () => hc(!document.documentElement.classList.contains("hc")));
  const rd = $("a11yRead");
  if (!("speechSynthesis" in window)) rd.hidden = true;
  else rd.addEventListener("click", () => {
    if (speechSynthesis.speaking) { speechSynthesis.cancel(); rd.setAttribute("aria-pressed", "false"); return; }
    const u = new SpeechSynthesisUtterance($("main").innerText.replace(/\s+/g, " ").slice(0, 6000));
    u.lang = "ar-SA"; u.onend = u.onerror = () => rd.setAttribute("aria-pressed", "false");
    rd.setAttribute("aria-pressed", "true"); speechSynthesis.speak(u);
  });

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
  cards.forEach((c, i) => { const b = document.createElement("button"); b.type = "button"; b.setAttribute("aria-label", `رأي ${i + 1}`); b.addEventListener("click", () => go(i)); dots.appendChild(b); });
  dots.removeAttribute("aria-hidden");
  let cur = 0;
  function go(i) {
    cur = Math.max(0, Math.min(cards.length - 1, i));
    const tr = track.getBoundingClientRect(), cr = cards[cur].getBoundingClientRect(), pad = parseFloat(getComputedStyle(track).paddingRight) || 0;
    track.scrollBy({ left: cr.right - (tr.right - pad), behavior: "smooth" });
    mark();
  }
  function mark() { [...dots.children].forEach((d, i) => d.setAttribute("aria-current", i === cur)); }
  let tmr;
  track.addEventListener("scroll", () => { clearTimeout(tmr); tmr = setTimeout(() => {
    const tr = track.getBoundingClientRect(), pad = parseFloat(getComputedStyle(track).paddingRight) || 0;
    let best = 0, bd = Infinity; cards.forEach((c, i) => { const dd = Math.abs(c.getBoundingClientRect().right - (tr.right - pad)); if (dd < bd) { bd = dd; best = i; } });
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
    if (url) ext(a, url); else a.addEventListener("click", e => { e.preventDefault(); toast("تطبيق مدى كير قريباً على المتاجر"); });
  });
  [["[data-gp]", C.googlePlay], ["[data-as]", C.appStore]].forEach(([s, url]) => $$(s).forEach(a => {
    if (url) ext(a, url); else a.addEventListener("click", e => { e.preventDefault(); toast("تطبيق مدى كير قريباً على المتاجر"); });
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
    const bookBtn = `<button type="button" class="help-btn help-wa" data-help-book><span>احجز موعدك وسنتواصل معك</span></button>`;
    let title, sub, acts, foot;
    if (kind === "ask") {
      title = "هل لديك استفسار آخر؟ 💚"; sub = "فريق مدى كير هنا لمساعدتك والإجابة عن جميع استفساراتك."; foot = "نرعاكم كأهلنا 💚";
      acts = wa ? waBtn("تواصل مع فريق مدى كير") : telNo ? callBtn("تواصل مع فريق مدى كير", "help-wa") : bookBtn;
    } else {
      title = "تحتاج مساعدة؟ 💚"; sub = "يسعدنا مساعدتك، تواصل معنا بالطريقة المناسبة لك."; foot = "فريقنا دائماً في خدمتك 💚";
      acts = (wa ? waBtn("تواصل عبر واتساب") : "") + (telNo ? callBtn("اتصل بنا", "help-call") : "") || bookBtn;
    }
    helpOv.innerHTML = `<div class="dlg help-dlg" role="dialog" aria-modal="true" aria-labelledby="helpT">
        <button type="button" class="dlg-x" data-hclose aria-label="إغلاق">×</button>
        <h2 id="helpT">${title}</h2>
        <p class="dlg-sub">${sub}</p>
        <div class="help-acts">${acts}</div>
        <p class="help-foot">${foot}</p>
      </div>`;
    helpOv.hidden = false; document.body.style.overflow = "hidden";
    setTimeout(() => { const f = helpOv.querySelector(".help-btn"); if (f) f.focus(); }, 30);
  }
  $$("[data-help]").forEach(a => a.addEventListener("click", e => { e.preventDefault(); openHelp(a.dataset.help); }));
  // Contact page buttons: WhatsApp / call when the numbers are set, otherwise the booking form.
  $$("[data-wa-link]").forEach(a => { if (wa) ext(a, wa); else a.addEventListener("click", e => { e.preventDefault(); openBook(); }); });
  $$("[data-tel-link]").forEach(a => { if (telNo) a.href = "tel:" + telNo; else a.addEventListener("click", e => { e.preventDefault(); openBook(); }); });
  const wf = $("waFloat");
  if (wa) ext(wf, wa); else wf.addEventListener("click", e => { e.preventDefault(); openBook(); });
  const tel = telNo;
  // Call button: opens a WhatsApp chat when a WhatsApp number is set, otherwise a phone call.
  // Call button: WhatsApp chat when a WhatsApp number is set, else a phone call; with neither it opens the booking form (data-book).
  $$("[data-call]").forEach(a => { const go = u => { delete a.dataset.book; a.href = u; a.hidden = false; }; if (wa) { go(wa); a.target = "_blank"; a.rel = "noopener"; } else if (tel) go("tel:" + tel); });
  $$("[data-phone]").forEach(a => { if (tel) { a.href = "tel:" + tel; a.textContent = C.phone; a.closest("[data-phone-row]").hidden = false; } });
  if (C.crNumber) ["crNo", "crNo2"].forEach(k => { if ($(k)) $(k).textContent = C.crNumber; });
  $$("[data-soon]").forEach(a => a.addEventListener("click", e => { e.preventDefault(); toast("هذه الصفحة قيد البناء في الورشة"); }));
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
    if ($("bkName").value.trim().length < 2) return bad($("bkName"), "اكتب الاسم.");
    if (!/^05\d{8}$/.test($("bkMobile").value)) return bad($("bkMobile"), "اكتب رقم جوال صحيح يبدأ بـ 05 ومكوّن من 10 أرقام.");
    if (!$("bkSvc").value) return bad($("bkSvc"), "اختر الخدمة.");
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
    if (!cloud.url || !cloud.key) { err.textContent = "الحجز من الموقع غير متاح حالياً، تواصل معنا عبر واتساب."; err.hidden = false; return; }
    const btn = $("bkSend"); btn.disabled = true;
    const now = new Date().toISOString(), id = "WEB-" + Date.now().toString(36).toUpperCase().slice(-5) + Math.random().toString(36).slice(2, 5).toUpperCase();
    const ref = attribution(), name = $("bkName").value.trim(), mobile = $("bkMobile").value, service = $("bkSvc").value, note = $("bkNote").value.trim();
    const order = {
      id, createdAt: now, updatedAt: now, service, mobile, medical: "non", patient: { en: name, ar: name }, mrn: null, staff: null, staffId: null,
      source: "website", status: "on_hold", decision: "pending", payment: null, web: { name, note: note || null, at: now, ref },
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
      err.textContent = "تعذّر إرسال الطلب، حاول مرة أخرى."; err.hidden = false;
    } finally { btn.disabled = false; }
  });

  // Subscribe: the email is saved to the shared database (mada_data, k "mada-newsletter"), one row per email.
  $("subForm").addEventListener("submit", async e => {
    e.preventDefault();
    const m = $("subMsg"), v = $("subEmail").value.trim().toLowerCase(), btn = $("subBtn");
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { m.textContent = "اكتب بريداً إلكترونياً صحيحاً."; m.hidden = false; return; }
    m.hidden = true;
    const cloud = C.cloud || {};
    btn.disabled = true;
    try {
      if (!cloud.url || !cloud.key) throw new Error("no cloud");
      const now = new Date().toISOString();
      const res = await fetch(cloud.url.replace(/\/$/, "") + "/rest/v1/mada_data", {
        method: "POST",
        headers: { apikey: cloud.key, "Content-Type": "application/json", Prefer: "return=minimal", ...(String(cloud.key).split(".").length === 3 ? { Authorization: "Bearer " + cloud.key } : {}) },
        body: JSON.stringify({ k: "mada-newsletter", rid: "NL-" + Date.now().toString(36).toUpperCase() + Math.random().toString(36).slice(2, 5).toUpperCase(), v: JSON.stringify({ email: v, at: now, page: location.pathname, ref: attribution() }), pos: Math.floor(Date.now() / 1000) })
      });
      if (!res.ok) throw new Error(res.status);
      gtmEvent("newsletter_submit");
      $("subBody").hidden = true; $("subDone").hidden = false;
    } catch (x) {
      m.textContent = "تعذّر الاشتراك الآن، حاول مرة أخرى."; m.hidden = false;
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
