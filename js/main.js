/* ==========================================================================
   Luca Flat – Website-Skript
   Reines JavaScript, keine Bibliotheken, keine externen Anfragen.
   ========================================================================== */
(function () {
  "use strict";

  var doc = document.documentElement;
  doc.classList.remove("no-js");

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Hilfsfunktionen ---------- */
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }


  /* ---------- Navigation ---------- */
  var nav = $(".nav");
  var toggle = $("#navToggle");
  var links = $("#navLinks");

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    $$("a", links).forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
    /* Tippen neben das geöffnete Menü schließt es */
    document.addEventListener("click", function (e) {
      if (links.classList.contains("is-open") && !(e.target.closest && e.target.closest(".nav"))) {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* Untermenü: per Klick/Tipp auf den Pfeil öffnen, per Escape oder Klick daneben schließen */
  function closeSubs() {
    /* Fokus abgeben, sonst bleibt das Menü über :focus-within offen */
    var ae = document.activeElement;
    if (ae && ae.closest && ae.closest(".has-sub") && ae.blur) ae.blur();
    $$(".has-sub.is-open").forEach(function (li) {
      li.classList.remove("is-open");
      var b = $(".sub-toggle", li); if (b) b.setAttribute("aria-expanded", "false");
    });
  }
  $$(".has-sub").forEach(function (li) {
    var btn = $(".sub-toggle", li);
    if (!btn) return;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !li.classList.contains("is-open");
      closeSubs();
      if (open) { li.classList.add("is-open"); btn.setAttribute("aria-expanded", "true"); btn.focus(); }
    });
  });
  document.addEventListener("click", closeSubs);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeSubs(); });

  /* Scroll-Zustand: Navigationsleiste, Fortschrittsbalken, Nach-oben-Knopf */
  var progress = $(".progress");
  var toTop = $(".to-top");
  var ticking = false;

  function onScroll() {
    var y = window.scrollY || doc.scrollTop;
    var max = doc.scrollHeight - window.innerHeight;
    if (nav) nav.classList.toggle("is-scrolled", y > 12);
    if (progress) progress.style.transform = "scaleX(" + (max > 0 ? y / max : 0) + ")";
    if (toTop) toTop.classList.toggle("is-visible", y > 700);
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    });
  }

  /* Aktiven Menüpunkt beim Scrollen markieren (nur auf der Startseite mit Ankern) */
  var sectionLinks = $$('.nav__links a[href^="#"], .nav__links a[href^="index.html#"]');
  var sections = sectionLinks.map(function (a) {
    var id = a.getAttribute("href").split("#")[1];
    return id ? document.getElementById(id) : null;
  });
  if ("IntersectionObserver" in window && sections.some(Boolean)) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        sectionLinks.forEach(function (a) {
          a.classList.toggle("is-active", a.getAttribute("href").split("#")[1] === en.target.id);
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach(function (s) { if (s) spy.observe(s); });
  }

  /* Feste Reiter-Leiste: markiert den Abschnitt, in dem man sich gerade befindet */
  var tabBar = $(".subnav-bar .subnav");
  var tabLinks = tabBar ? $$('a[href^="#"]', tabBar) : [];
  if (tabLinks.length) {
    var tabSecs = tabLinks.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    var lastTab = -2, tabTick = false;
    var updateTabs = function () {
      tabTick = false;
      var line = 168; /* Linie knapp unter Menü und Reiter-Leiste */
      var idx = 0;
      tabSecs.forEach(function (sec, i) { if (sec && sec.getBoundingClientRect().top <= line) idx = i; });
      if (window.innerHeight + (window.scrollY || doc.scrollTop) >= doc.scrollHeight - 4) idx = tabSecs.length - 1;
      if (idx === lastTab) return;
      lastTab = idx;
      tabLinks.forEach(function (a, i) {
        if (i === idx) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
      });
      /* aktiven Reiter in der (auf dem Handy waagerecht scrollbaren) Leiste in die Mitte holen */
      var cur = tabLinks[idx];
      var target = cur.offsetLeft - (tabBar.clientWidth - cur.offsetWidth) / 2;
      if (tabBar.scrollWidth > tabBar.clientWidth) tabBar.scrollTo({ left: target, behavior: reduceMotion ? "auto" : "smooth" });
    };
    window.addEventListener("scroll", function () {
      if (!tabTick) { tabTick = true; requestAnimationFrame(updateTabs); }
    }, { passive: true });
    window.addEventListener("resize", updateTabs);
    updateTabs();
  }

  /* ---------- Scroll-Reveal ---------- */
  var revealEls = $$(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); obs.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Zähler ---------- */
  function animateCount(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var suffix = el.getAttribute("data-suffix") || "";
    if (isNaN(target)) return;
    if (reduceMotion) { el.textContent = target + suffix; return; }
    var dur = 1400, t0 = null;
    function step(ts) {
      if (t0 === null) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = $$("[data-count]");
  if ("IntersectionObserver" in window) {
    var co = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { animateCount(en.target); obs.unobserve(en.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { co.observe(c); });
  } else {
    counters.forEach(animateCount);
  }

  /* ---------- Fähigkeiten-Balken ---------- */
  var bars = $$(".skill__bar i");
  function fillBar(b) { b.style.width = b.getAttribute("data-v") + "%"; }
  if ("IntersectionObserver" in window) {
    var bo = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { fillBar(en.target); obs.unobserve(en.target); }
      });
    }, { threshold: 0.5 });
    bars.forEach(function (b) { bo.observe(b); });
  } else {
    bars.forEach(fillBar);
  }

  /* ---------- Tipp-Effekt im Hero ---------- */
  var typed = $("#typed");
  if (typed) {
    var phrases = (typed.getAttribute("data-phrases") || "").split("|").filter(Boolean);
    if (reduceMotion || !phrases.length) {
      typed.textContent = phrases[0] || "";
    } else {
      var pi = 0, ci = 0, deleting = false;
      (function tick() {
        var word = phrases[pi];
        typed.textContent = word.slice(0, ci);
        var delay = deleting ? 32 : 68;
        if (!deleting && ci === word.length) { deleting = true; delay = 1700; }
        else if (deleting && ci === 0) { deleting = false; pi = (pi + 1) % phrases.length; delay = 380; }
        ci += deleting ? -1 : 1;
        setTimeout(tick, delay);
      })();
    }
  }

  /* ---------- Karten: Lichtkegel folgt dem Mauszeiger ---------- */
  $$(".card").forEach(function (card) {
    card.addEventListener("pointermove", function (e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty("--mx", (e.clientX - r.left) + "px");
      card.style.setProperty("--my", (e.clientY - r.top) + "px");
    });
  });

  /* ---------- Filter der App-Karten ---------- */
  var chips = $$(".chip[data-filter]");
  var appCards = $$("[data-cat]");
  var emptyMsg = $("#filterEmpty");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var f = chip.getAttribute("data-filter");
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
      var visible = 0;
      appCards.forEach(function (card) {
        var show = f === "all" || card.getAttribute("data-cat").split(" ").indexOf(f) !== -1;
        card.classList.toggle("is-hidden", !show);
        if (show) visible++;
      });
      if (emptyMsg) emptyMsg.hidden = visible !== 0;
    });
  });


  /* ---------- Kontaktformular: rein lokale Vorprüfung, öffnet das E-Mail-Programm ---------- */
  var EN = doc.lang === "en";
  var M = EN ? {
    name: "Please enter your name.", mail: "Please enter a valid email address.",
    short: "Your message is too short. Please write at least 10 characters.",
    none: "The contact address has not been set yet. The form is not active yet.",
    subject: "Message from ", opened: "Your email app is opening. Send the message there."
  } : {
    name: "Bitte gib deinen Namen ein.", mail: "Bitte gib eine gültige E-Mail-Adresse ein.",
    short: "Deine Nachricht ist zu kurz. Bitte schreib mindestens 10 Zeichen.",
    none: "Die Kontaktadresse ist noch nicht hinterlegt. Das Formular ist noch nicht aktiv.",
    subject: "Nachricht von ", opened: "Dein E-Mail-Programm öffnet sich. Sende die Nachricht dort ab."
  };
  var form = $("#contactForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = form.elements.name.value.trim();
      var mail = form.elements.email.value.trim();
      var msg = form.elements.message.value.trim();
      var out = $("#formStatus");
      var okMail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail);

      if (name.length < 2) { out.textContent = M.name; return; }
      if (!okMail) { out.textContent = M.mail; return; }
      if (msg.length < 10) { out.textContent = M.short; return; }

      /* Die Adresse kommt aus site_config.py (OWNER_EMAIL) und wird von build_pages.py eingetragen */
      var to = form.getAttribute("data-mailto") || "";
      if (!to) {
        out.textContent = M.none;
        return;
      }
      var subject = encodeURIComponent(M.subject + name);
      var body = encodeURIComponent(msg + "\n\n" + name + " (" + mail + ")");
      window.location.href = "mailto:" + to + "?subject=" + subject + "&body=" + body;
      out.textContent = M.opened;
    });
  }

  /* ---------- Großes Marken-Logo: Zeichenanimation beim ersten Sichtbarwerden ---------- */
  var bigMark = $(".avatar");
  if (bigMark) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      bigMark.classList.add("is-drawn");
    } else {
      var mo = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { bigMark.classList.add("is-drawn"); obs.unobserve(en.target); }
        });
      }, { threshold: 0.4 });
      mo.observe(bigMark);
    }
  }

  /* ---------- Marken-Icon: Zeichenanimation nur beim Einstieg von außen ----------
     Ohne Cookies oder Browser-Speicher: Kommt der Besucher von einer Seite dieser Website,
     wird die Animation nicht wiederholt. */
  (function () {
    var marks = $$(".brand__mark");
    var internal = false;
    try { internal = !!document.referrer && new URL(document.referrer).origin === location.origin; } catch (e) { internal = false; }
    if (internal || reduceMotion || !marks.length) return;
    marks.forEach(function (m) { m.classList.add("lct-drawing"); });
    setTimeout(function () {
      marks.forEach(function (m) { m.classList.remove("lct-drawing"); });
    }, 1100);
  })();

  /* ---------- Bildergalerie: Screenshots und Widgets, Pfeile neben dem Bild, Wischen, endlos (nach dem letzten Bild folgt das erste) ---------- */
  (function () {
    var EN = doc.lang === "en";
    var L = EN ? { prev: "Previous image", next: "Next image", go: "Show image ", shots: "Screenshots", widgets: "Widgets", slide: "Image", of: " of " }
               : { prev: "Vorheriges Bild", next: "Nächstes Bild", go: "Bild anzeigen ", shots: "Screenshots", widgets: "Widgets", slide: "Bild", of: " von " };
    /* Breite Bildschirme zeigen alle Bilder nebeneinander – das Karussell lohnt sich nur am Handy */
    if (window.matchMedia && window.matchMedia("(min-width: 960px)").matches) return;
    $$(".shots, .widgets").forEach(function (track) {
      var slides = Array.prototype.slice.call(track.children).filter(function (el) { return el.tagName === "FIGURE"; });
      var n = slides.length;
      if (n < 2) return;
      var label = track.classList.contains("widgets") ? L.widgets : L.shots, slot = 1, settleTimer = null, ticking = false;
      var g = document.createElement("div");
      g.className = "gallery"; g.setAttribute("role", "group"); g.setAttribute("aria-roledescription", "carousel"); g.setAttribute("aria-label", label);
      track.parentNode.insertBefore(g, track); g.appendChild(track);
      track.classList.add("gallery__track"); track.tabIndex = 0; track.setAttribute("aria-label", label);
      slides.forEach(function (sl, i) {
        sl.setAttribute("role", "group"); sl.setAttribute("aria-roledescription", "slide");
        sl.setAttribute("aria-label", L.slide + " " + (i + 1) + L.of + n);
      });
      /* Kopien am Anfang (letztes Bild) und Ende (erstes Bild) ermöglichen das endlose Weiterwischen */
      function clone(src) {
        var c = src.cloneNode(true); c.setAttribute("aria-hidden", "true"); c.setAttribute("inert", ""); c.removeAttribute("role");
        c.removeAttribute("aria-label"); c.removeAttribute("aria-roledescription"); c.classList.add("is-clone");
        $$("img", c).forEach(function (im) { im.loading = "eager"; });
        return c;
      }
      track.insertBefore(clone(slides[n - 1]), track.firstChild);
      track.appendChild(clone(slides[0]));
      var all = Array.prototype.slice.call(track.children);

      var prev = document.createElement("button"), next = document.createElement("button");
      prev.type = next.type = "button"; prev.className = "gallery__btn gallery__prev"; next.className = "gallery__btn gallery__next";
      prev.setAttribute("aria-label", L.prev); next.setAttribute("aria-label", L.next); prev.textContent = "‹"; next.textContent = "›";
      g.appendChild(prev); g.appendChild(next);
      var dots = document.createElement("div"); dots.className = "gallery__dots"; g.appendChild(dots);
      var dotEls = slides.map(function (_, i) {
        var d = document.createElement("button"); d.type = "button"; d.className = "gallery__dot";
        d.setAttribute("aria-label", L.go + (i + 1)); d.addEventListener("click", function () { goSlot(i + 1); }); dots.appendChild(d); return d;
      });
      function real() { return (slot - 1 + n) % n; }
      function update() {
        var r = real();
        dotEls.forEach(function (d, i) { if (i === r) d.setAttribute("aria-current", "true"); else d.removeAttribute("aria-current"); });
        track.style.height = all[slot].offsetHeight + "px";  /* Höhe folgt dem aktuellen Bild */
        var im = $("img", all[slot]);
        if (im) {  /* Pfeile auf Höhe der Bildmitte */
          var t = im.getBoundingClientRect(), k = track.getBoundingClientRect();
          g.style.setProperty("--arrow-top", Math.round(t.top - k.top + t.height / 2) + "px");
        }
      }
      function jump(s) {  /* ohne Animation auf die echte Seite springen */
        slot = s; track.style.scrollBehavior = "auto"; track.scrollLeft = s * track.clientWidth; track.style.scrollBehavior = "";
      }
      function goSlot(s) {
        s = Math.max(0, Math.min(n + 1, s));
        track.scrollTo({ left: s * track.clientWidth, behavior: reduceMotion ? "auto" : "smooth" });
      }
      function settle() {
        var w = track.clientWidth; if (!w) return;
        slot = Math.round(track.scrollLeft / w);
        if (slot === 0) jump(n); else if (slot === n + 1) jump(1);
        update();
      }
      track.addEventListener("scroll", function () {
        if (!ticking) {
          ticking = true;
          requestAnimationFrame(function () {
            ticking = false; var w = track.clientWidth; if (!w) return;
            slot = Math.max(0, Math.min(n + 1, Math.round(track.scrollLeft / w))); update();
          });
        }
        clearTimeout(settleTimer); settleTimer = setTimeout(settle, 140);
      }, { passive: true });
      prev.addEventListener("click", function () { goSlot(slot - 1); });
      next.addEventListener("click", function () { goSlot(slot + 1); });
      track.addEventListener("keydown", function (e) {
        if (e.key === "ArrowLeft") { e.preventDefault(); goSlot(slot - 1); }
        else if (e.key === "ArrowRight") { e.preventDefault(); goSlot(slot + 1); }
        else if (e.key === "Home") { e.preventDefault(); goSlot(1); }
        else if (e.key === "End") { e.preventDefault(); goSlot(n); }
      });
      window.addEventListener("resize", function () { jump(slot); update(); });
      $$("img", track).forEach(function (im) { if (!im.complete) im.addEventListener("load", update); });
      jump(1); update();
    });
  })();

  /* ---------- Drucken / als PDF speichern (rechtliche Seiten) ---------- */
  $$("[data-print]").forEach(function (b) {
    b.hidden = false;
    b.addEventListener("click", function () { window.print(); });
  });

  /* ---------- FAQ: alle öffnen/schließen, Direktlink zu einer Frage ---------- */
  (function () {
    var faq = $(".faq");
    if (!faq) return;
    var EN = doc.lang === "en";
    var T = EN ? { open: "Open all", close: "Close all", copy: "Copy link to this question", copied: "Link copied" }
               : { open: "Alle öffnen", close: "Alle schließen", copy: "Link zu dieser Frage kopieren", copied: "Link kopiert" };
    var items = $$("details", faq);
    var tools = document.createElement("div"); tools.className = "faq-tools";
    var all = document.createElement("button"); all.type = "button"; all.className = "btn btn--ghost btn--sm"; all.textContent = T.open;
    tools.appendChild(all); faq.parentNode.insertBefore(tools, faq);
    function refresh() {
      var allOpen = items.every(function (d) { return d.open; });
      all.textContent = allOpen ? T.close : T.open;
    }
    all.addEventListener("click", function () {
      var openAll = !items.every(function (d) { return d.open; });
      items.forEach(function (d) { d.open = openAll; }); refresh();
    });
    items.forEach(function (d) {
      d.addEventListener("toggle", refresh);
      if (!d.id) return;
      var b = document.createElement("button"); b.type = "button"; b.className = "faq__copy"; b.textContent = T.copy;
      b.addEventListener("click", function () {
        var url = location.href.split("#")[0] + "#" + d.id;
        function done() { b.textContent = T.copied; setTimeout(function () { b.textContent = T.copy; }, 2000); }
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, function () { location.hash = d.id; });
        else location.hash = d.id;
      });
      var body = $(".faq__body", d); if (body) body.appendChild(b);
    });
    function openFromHash() {
      var id = decodeURIComponent((location.hash || "").slice(1)); if (!id) return;
      var d = document.getElementById(id);
      if (d && d.tagName === "DETAILS" && faq.contains(d)) { d.open = true; d.scrollIntoView({ block: "center" }); }
    }
    window.addEventListener("hashchange", openFromHash); openFromHash();
  })();

  /* ---------- Jahr im Footer ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
