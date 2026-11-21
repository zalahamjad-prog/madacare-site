// Mada Care for Business page behaviour. Settings are in b2b-config.js.
(() => {
  const C = (typeof MADA_B2B !== "undefined" && MADA_B2B) || {}, $ = id => document.getElementById(id), $$ = s => [...document.querySelectorAll(s)];
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;

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

  if (C.email) $$("[data-mail]").forEach(a => { a.href = "mailto:" + C.email; });

  // Sections and cards rise into view; cards in a group follow one another.
  if (!still && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { io.unobserve(x.target); x.target.classList.add("in"); } }), { threshold: .15, rootMargin: "0px 0px -6% 0px" });
    $$(".rv-up").forEach(el => { el.classList.add("rv"); io.observe(el); });
    [[".bx-card", 3], [".bx-tiles li", 3], [".sc.why", 4], [".bx-step", 4]].forEach(([sel, n]) => $$(sel).forEach((el, i) => {
      el.classList.add("rv"); el.style.setProperty("--d", (i % n) * .12 + "s"); io.observe(el);
    }));
  }

  // How we work: the line fills and the steps light up as the section scrolls past.
  const steps = $("steps");
  if (steps) {
    const items = $$(".bx-step");
    const update = () => {
      const r = steps.getBoundingClientRect(), mid = innerHeight * .62;
      const p = still ? 1 : Math.min(1, Math.max(0, (mid - r.top) / r.height));
      steps.style.setProperty("--p", p.toFixed(3));
      items.forEach((s, i) => s.classList.toggle("on", p >= .98 || p >= i / items.length + .02));
    };
    let raf = 0;
    addEventListener("scroll", () => { if (!raf) raf = requestAnimationFrame(() => { raf = 0; update(); }); }, { passive: true });
    addEventListener("resize", update); update();
  }

  // WhatsApp button (bottom corner) with a "Need help?" bubble. Without a number in b2b-config.js it goes to the quote form.
  const wf = $("waFloat"), waNo = String(C.whatsapp || "").replace(/\D/g, "");
  if (wf) {
    const msg = encodeURIComponent("السلام عليكم، أبغى أعرف أكثر عن خدمات مدى كير للشركات");
    if (waNo) { wf.href = "https://wa.me/" + waNo + "?text=" + msg; wf.target = "_blank"; wf.rel = "noopener"; }
    wf.addEventListener("click", () => (window.dataLayer = window.dataLayer || []).push({ event: "whatsapp_click", area: "b2b_float" }));
    setTimeout(() => {
      const bb = document.createElement("button");
      bb.type = "button"; bb.className = "wa-bubble"; bb.textContent = "تحتاج مساعدة؟ 💚";
      document.body.appendChild(bb);
      requestAnimationFrame(() => bb.classList.add("in"));
      const hide = () => { bb.classList.remove("in"); setTimeout(() => bb.remove(), 300); };
      bb.addEventListener("click", () => { hide(); wf.click(); });
      wf.addEventListener("click", hide, { once: true });
      setTimeout(hide, 8000);
    }, 4000);
  }

  // Quote request: one row in the shared database (mada_data, k "mada-b2b-leads").
  const form = $("quoteForm"), err = $("qErr"), mail = C.email || "digital@madacare.sa";
  const latin = v => v.replace(/[٠-٩]/g, d => "٠١٢٣٤٥٦٧٨٩".indexOf(d)).replace(/[۰-۹]/g, d => "۰۱۲۳۴۵۶۷۸۹".indexOf(d));
  $("qMobile").addEventListener("input", e => { e.target.value = latin(e.target.value).replace(/\D/g, "").slice(0, 10); });
  const bad = (el, msg) => { el.setAttribute("aria-invalid", "true"); err.textContent = msg; err.hidden = false; el.focus(); return false; };
  const valid = () => {
    form.querySelectorAll("[aria-invalid]").forEach(x => x.removeAttribute("aria-invalid")); err.hidden = true;
    if ($("qCompany").value.trim().length < 2) return bad($("qCompany"), "اكتب اسم الشركة.");
    if (!/^05\d{8}$/.test($("qMobile").value)) return bad($("qMobile"), "اكتب رقم جوال صحيح يبدأ بـ 05 ومكوّن من 10 أرقام.");
    const em = $("qEmail").value.trim();
    if (em && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)) return bad($("qEmail"), "اكتب بريدًا إلكترونيًا صحيحًا.");
    return true;
  };
  const utm = () => {
    const q = new URLSearchParams(location.search), o = {};
    ["source", "medium", "campaign"].forEach(k => { const v = q.get("utm_" + k); if (v) o[k] = v.slice(0, 120); });
    if (!o.source && document.referrer) o.referrer = document.referrer.slice(0, 200);
    return o;
  };
  form.addEventListener("submit", async e => {
    e.preventDefault();
    if (!valid()) return;
    if (C.preview) { $("qRef").textContent = "B2B-PREVIEW"; $("qPv").hidden = false; form.hidden = true; $("qDone").hidden = false; form.reset(); return; }
    const cloud = C.cloud || {};
    if (!cloud.url || !cloud.key) { err.textContent = "الإرسال غير متاح حالياً، راسلنا على " + mail; err.hidden = false; return; }
    const btn = $("qSend"); btn.disabled = true;
    const now = new Date().toISOString(), id = "B2B-" + Date.now().toString(36).toUpperCase().slice(-5) + Math.random().toString(36).slice(2, 5).toUpperCase();
    const sz = form.querySelector("input[name=qSize]:checked"), svc = $("qService");
    const lead = {
      id, createdAt: now, status: "new", source: "b2b-website",
      company: $("qCompany").value.trim(), contact: $("qName").value.trim() || null, mobile: $("qMobile").value, email: $("qEmail").value.trim().toLowerCase() || null,
      employees: sz ? sz.value : null, service: svc.value || null, serviceLabel: svc.value ? svc.options[svc.selectedIndex].text : null,
      note: $("qNote").value.trim() || null, ref: utm()
    };
    try {
      const res = await fetch(cloud.url.replace(/\/$/, "") + "/rest/v1/mada_data", {
        method: "POST",
        headers: { apikey: cloud.key, "Content-Type": "application/json", Prefer: "return=minimal", ...(String(cloud.key).split(".").length === 3 ? { Authorization: "Bearer " + cloud.key } : {}) },
        body: JSON.stringify({ k: "mada-b2b-leads", rid: id, v: JSON.stringify(lead), pos: Math.floor(Date.now() / 1000) })
      });
      if (!res.ok) throw new Error(res.status);
      (window.dataLayer = window.dataLayer || []).push({ event: "b2b_quote_submit", employees: lead.employees, service: lead.service });
      $("qRef").textContent = id; form.hidden = true; $("qDone").hidden = false; form.reset();
    } catch (x) {
      err.textContent = "تعذّر إرسال الطلب، حاول مرة ثانية أو راسلنا على " + mail; err.hidden = false;
    } finally { btn.disabled = false; }
  });
})();
