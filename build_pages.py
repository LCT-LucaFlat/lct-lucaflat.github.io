#!/usr/bin/env python3
"""Erzeugt ALLE Seiten der Website aus einer gemeinsamen Vorlage,
damit Kopf, Navigation und Fuß überall identisch sind.
Aufruf: python3 build_pages.py"""
from pathlib import Path

import html as _html
import json

import legal_texts
import site_config as cfg

ROOT = Path(__file__).parent

# Play-Store-Link und Status-Hinweis: erst aktiv, wenn Paketname gesetzt UND APP_PUBLISHED = True
PUBLISHED = bool(getattr(cfg, "APP_PUBLISHED", False) and getattr(cfg, "PLAY_PACKAGE", ""))
PLAY_URL = f"https://play.google.com/store/apps/details?id={cfg.PLAY_PACKAGE}" if PUBLISHED else ""
STATUS_BADGE = ('<span class="status status--live">Im Play Store</span>' if PUBLISHED
                else '<span class="status status--wip">Bald im Play Store</span>')

# Video der Streaming-Suche: wird nur eingebaut, wenn die Datei existiert (liegt auf der Website, kein YouTube)
VIDEO_FILE = ROOT / "assets" / "video" / "streaming-suche.mp4"

BRAND_SVG = ('<svg viewBox="0 0 280 100" aria-hidden="true"><path class="lct-mini-g" pathLength="1" '
             'd="M10 10V78Q10 90 22 90H160H102Q90 90 90 78V22Q90 10 102 10H270H227Q215 10 215 22V90"/></svg>')

AVATAR_SVG = '''<svg class="avatar__mark" viewBox="0 0 280 100" aria-hidden="true" style="width:70%; height:auto; display:block; margin:auto;">
              <defs><linearGradient id="lctGradStatic" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="100">
                <stop offset="0" stop-color="#c4f2ff"/><stop offset="1" stop-color="#4f8fff"/>
              </linearGradient></defs>
              <path class="avatar__mark-path" pathLength="1" fill="none" stroke="url(#lctGradStatic)" stroke-width="8" stroke-linecap="butt" stroke-linejoin="round"
                d="M10 10V78Q10 90 22 90H160H102Q90 90 90 78V22Q90 10 102 10H270H227Q215 10 215 22V90"/>
            </svg>'''

NAV = [("apps", "apps.html", "Apps"), ("ueber-mich", "ueber-mich.html", "Über mich"),
       ("fragen", "fragen.html", "Fragen"), ("kontakt", "kontakt.html", "Kontakt")]

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}" class="no-js{html_class}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{doc_title}</title>
  <meta name="description" content="{desc}">
  <meta name="color-scheme" content="light dark">
  <meta name="theme-color" content="#f5efe3" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#1a1612" media="(prefers-color-scheme: dark)">
  <link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="{up}assets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{up}assets/fonts/space-grotesk-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{up}css/style.css">
{head_extra}</head>
<body>
  <a class="skip-link" href="#main">{t_skip}</a>
  <div class="progress" aria-hidden="true"></div>
  <header class="nav">
    <div class="container nav__inner">
      <a class="brand" href="{base}index.html" aria-label="{t_home}"><span class="brand__mark">{brand}</span>Luca Flat</a>
      <nav class="nav__tools" aria-label="{t_mainnav}">
        <ul class="nav__links" id="navLinks">
{nav}
        </ul>
        <button class="icon-btn nav__toggle" id="navToggle" type="button" aria-label="{t_menu}" aria-expanded="false" aria-controls="navLinks">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        </button>
      </nav>
    </div>
  </header>

  <main id="main">
{main}
  </main>

  <footer class="footer{footer_class}">
    <div class="container">
{footer_grid}      <div class="footer__bottom"><span>© <span data-year>2026</span> Luca Flat</span>{footer_legal}</div>
    </div>
  </footer>

  <button class="icon-btn to-top" type="button" aria-label="{t_top}">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
  </button>
  <script src="{up}js/main.js"></script>
</body>
</html>
"""

PLACEHOLDER = """        <div class="placeholder-box">
          <strong>Inhalt folgt.</strong> Dieser Text wird später mit deinen Angaben ergänzt. Bis dahin dient die Seite als Platzhalter, damit alle Links funktionieren.
        </div>"""


def page_head(up, crumbs, title, lead, subnav=""):
    """Seitenkopf mit Überschrift. Der Pfad „Start / Apps / …“ wird bewusst nicht mehr angezeigt."""
    lead_html = f'\n        <p class="lead">{lead}</p>' if lead else ""
    return f"""    <section class="page-head">
      <div class="container">
        <h1 style="font-size:clamp(1.5rem,6.4vw,3.2rem);">{title}</h1>{lead_html}
{subnav}
      </div>
    </section>"""


def wide_section(body):
    return f"""    <section class="section" style="padding-top:1rem;">
      <div class="container">
{body}
      </div>
    </section>"""


def prose(body):
    return f"""    <section class="section" style="padding-top:1rem;">
      <div class="container prose">
{body}
      </div>
    </section>"""


# ---------------------------------------------------------------- Inhalte
APP_DIR = "apps/universalfernbedienung/"


PAGES = []

# --- Startseite: schlankes Tor. Marke, ein Satz zur Art der Apps, Hinweis auf die neueste App
APP_URL = "apps/universalfernbedienung/index.html"
PAGES.append(("index.html", "", "Luca Flat – Android-Apps",
              "Luca Flat entwickelt Android-Apps für den Alltag.",
              f"""    <section class="hero" aria-labelledby="hero-title">
      <div class="container hero__content">
        <div class="hero__text">
          <a class="hero__badge intro" href="{APP_URL}"><span class="dot" aria-hidden="true"></span>Neu: Universalfernbedienung →</a>
          <h1 id="hero-title" class="intro"><span class="grad">Luca Flat</span></h1>
          <p class="lead intro">Android-Apps für den Alltag.</p>
          <div class="hero__cta intro">
            <a class="btn" href="apps.html">Meine Apps ansehen</a>
            <a class="btn btn--ghost" href="ueber-mich.html">Über mich</a>
          </div>
        </div>
      </div>
    </section>""", ""))

# --- Apps
PAGES.append(("apps.html", "apps", "Apps – Luca Flat", "Alle Apps von Luca Flat.",
              page_head("", [("Apps", None)], "Apps", "Meine Apps erscheinen als eigenständige Android-Apps im Play Store.") + f"""
    <section class="section" style="padding-top:1rem;">
      <div class="container">
        <div class="grid grid--3">
          <article class="card card--app reveal">
            <div class="card__head">
              <img class="card__appicon" src="assets/app-icon-192.png" width="56" height="56" alt="" loading="lazy" decoding="async">
              <div><h3>Universalfernbedienung</h3>{STATUS_BADGE}</div>
            </div>
            <p>Dein Handy als Fernbedienung für den Fernseher.</p>
            <a class="btn btn--ghost card__btn" href="apps/universalfernbedienung/index.html">Details ansehen</a>
          </article>
          <article class="card card--soon reveal" data-delay="1">
            <div class="card__icon card__icon--muted" aria-hidden="true"></div>
            <h3>Weitere Apps folgen</h3>
            <p>Neue Projekte erscheinen hier, sobald sie fertig sind.</p>
          </article>
        </div>
      </div>
    </section>""", ""))

# --- Über mich
PAGES.append(("ueber-mich.html", "ueber-mich", "Über mich – Luca Flat", "Über Luca Flat und seine Apps.",
              page_head("", [("Über mich", None)], "Über mich", "") + f"""
    <section class="section" style="padding-top:1rem;">
      <div class="container about">
        <div class="reveal">
          <div class="avatar" role="img" aria-label="LCT – Monogramm von Luca Flat">
            <div class="avatar__ring"></div>
            {AVATAR_SVG}
          </div>
        </div>
        <div>
          <h2 class="reveal">Hallo, mein Name ist Luca</h2>
          <p class="reveal">In meiner Freizeit entwickle ich gerne Apps, die den Alltag einfacher machen. Es macht mir Freude zu sehen, wie aus einer einfachen Idee eine voll funktionsfähige Android-App wird.</p>
          <p class="reveal">Ich lege viel Wert auf eine einfache Bedienung und Software, die das Leben praktisch erleichtert.</p>
          <p class="reveal">Auf dieser Website präsentiere ich meine erste App sowie alle zukünftigen Projekte.</p>
          <p class="reveal"><a class="btn" href="apps.html">Meine Apps ansehen</a></p>
        </div>
      </div>
    </section>""", ""))

# --- Fragen
PAGES.append(("fragen.html", "fragen", "Fragen – Luca Flat", "Häufige Fragen zu den Apps von Luca Flat.",
              page_head("", [("Fragen", None)], "Häufige Fragen", "") + """
    <section class="section" style="padding-top:1rem;">
      <div class="container prose">
        <div class="faq">
          <details id="kosten"><summary>Kosten die Apps etwas?</summary><div class="faq__body">Nein. Alle Apps sind kostenlos und enthalten keine Werbung.</div></details>
          <details id="daten"><summary>Sammelt ihr meine Daten?</summary><div class="faq__body">Was genau gespeichert wird, steht in den Datenschutzerklärungen der <a href="legal/datenschutz-app.html">App</a> und der <a href="legal/datenschutz.html">Website</a>. Die App speichert alles nur auf deinem Gerät.</div></details>
          <details id="fehler"><summary>Wie melde ich einen Fehler oder wünsche mir eine Funktion?</summary><div class="faq__body">Schreib mir über die <a href="kontakt.html">Kontaktseite</a>.</div></details>
          <details id="geraete"><summary>Auf welchen Geräten laufen die Apps?</summary><div class="faq__body">Auf Android-Geräten. Die Apps erscheinen über den Play Store.</div></details>
          <details id="hilfe"><summary>Wo finde ich Hilfe zur App?</summary><div class="faq__body">Die <a href="apps/universalfernbedienung/hilfe.html">Hilfe zur App</a> erklärt die Verbindung zum Fernseher, Widgets, Berührungsschutz und das Fehlerprotokoll.</div></details>
        </div>
      </div>
    </section>""", ""))

# --- Kontakt
PAGES.append(("kontakt.html", "kontakt", "Kontakt – Luca Flat", "Kontakt zu Luca Flat.",
              page_head("", [("Kontakt", None)], "Kontakt", "Fragen, Feedback oder eine Idee für die nächste App? Ich freue mich über jede Nachricht.") + f"""
    <section class="section" style="padding-top:1rem;">
      <div class="container prose">
        <form class="form" id="contactForm" data-mailto="{_html.escape(cfg.OWNER_EMAIL)}" novalidate>
          <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-mail">E-Mail</label><input id="f-mail" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="f-msg">Nachricht</label><textarea id="f-msg" name="message" required></textarea></div>
          <div><button class="btn" type="submit">Nachricht vorbereiten</button></div>
          <p class="note" id="formStatus" role="status" aria-live="polite">Das Formular sendet nichts an einen Server. Es öffnet dein E-Mail-Programm.</p>
        </form>
      </div>
    </section>""", ""))

# --- Rechtliches (Platzhalter)
PAGES.append(("legal/datenschutz.html", "", "Datenschutzerklärung der Website – Luca Flat",
              "Datenschutzerklärung der Website von Luca Flat.",
              page_head("../", [("Datenschutz", None)], "Datenschutzerklärung der Website",
                        "Welche Daten diese Website verarbeitet und welche nicht.") + "\n" + prose(legal_texts.website_privacy_body()), "../"))
PAGES.append(("legal/datenschutz-app.html", "", "Datenschutzerklärung der App – Luca Flat",
              "Datenschutzerklärung der App Universalfernbedienung.",
              page_head("../", [("Datenschutz App", None)], "Datenschutzerklärung der App",
                        "Universalfernbedienung: Welche Daten die App verarbeitet.") + "\n" + prose(legal_texts.app_privacy_body()), "../"))
PAGES.append(("legal/impressum.html", "", "Impressum – Luca Flat", "Impressum von Luca Flat.",
              page_head("../", [("Impressum", None)], "Impressum", "Angaben zum Betreiber dieser Website.") + "\n" + prose(legal_texts.impressum_body()), "../"))

# --- Zusätzliche Seiten (App-Seite, Hilfe, Presse, englische Fassung) stehen in inhalt.py
import inhalt
PAGES += inhalt.build(dict(page_head=page_head, prose=prose, ROOT=ROOT, cfg=cfg, PUBLISHED=PUBLISHED, PLAY_URL=PLAY_URL,
                           VIDEO_FILE=VIDEO_FILE, AVATAR_SVG=AVATAR_SVG))

# --- Fehlerseite (404): Adressen beginnen mit dem Pfad der Website, weil sie unter jeder beliebigen Adresse angezeigt wird
NOTFOUND_MAIN = '''    <section class="section">
      <div class="container notfound">
        <p class="notfound__code" aria-hidden="true">404</p>
        <h1>Seite nicht gefunden</h1>
        <p class="lead">Diese Seite gibt es nicht oder sie wurde verschoben.<br><span lang="en">Page not found.</span></p>
        <p><a class="btn" href="@@BASE@@index.html">Zur Startseite</a> <a class="btn btn--ghost" href="@@BASE@@apps.html">Apps</a></p>
      </div>
    </section>'''
PAGES.append(("404.html", "", "Seite nicht gefunden – Luca Flat", "Diese Seite gibt es nicht.", NOTFOUND_MAIN))

CHEVRON = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'


FOOTER_GRID = '''      <div class="footer__grid">
        <div>
          <a class="brand" href="{base}index.html"><span class="brand__mark">{brand}</span>Luca Flat</a>
        </div>
        <div>
          <h4>{t_pages}</h4>
          <ul>
{foot_nav}
          </ul>
        </div>
        <div>
          <h4>{t_legal}</h4>
          <ul>
{legal_html}
          </ul>
        </div>
      </div>
'''

NAV_EN = [("apps", "apps.html", "Apps"), ("ueber-mich", "about.html", "About"),
          ("fragen", "faq.html", "FAQ"), ("kontakt", "contact.html", "Contact")]
UI = {
    "de": dict(skip="Zum Inhalt springen", home="Luca Flat – Startseite", mainnav="Hauptnavigation", menu="Menü öffnen",
               pages="Seiten", legal="Rechtliches", top="Nach oben", sub="Untermenü Apps", app="Universalfernbedienung",
               extra=[("presse", "presse.html", "Presse")] if inhalt.PRESSE_AKTIV else []),
    "en": dict(skip="Skip to content", home="Luca Flat – Home", mainnav="Main navigation", menu="Open menu",
               pages="Pages", legal="Legal", top="Back to top", sub="Apps submenu", app="Universal Remote",
               extra=[("press", "press.html", "Press")] if inhalt.PRESSE_AKTIV else []),
}
LEGAL_DE = (("datenschutz", "Datenschutz Website"), ("datenschutz-app", "Datenschutz App"), ("impressum", "Impressum"))
LEGAL_EN = (("datenschutz", "Privacy – website (German)"), ("datenschutz-app", "Privacy – app (German)"), ("impressum", "Legal notice (German)"))

# Gegenstück jeder Seite in der anderen Sprache (für den Sprachwechsel)
ALT = {"index.html": "en/index.html", "apps.html": "en/apps.html", "ueber-mich.html": "en/about.html", "fragen.html": "en/faq.html",
       "kontakt.html": "en/contact.html", "presse.html": "en/press.html",
       "apps/universalfernbedienung/index.html": "en/apps/universalfernbedienung/index.html",
       "apps/universalfernbedienung/hilfe.html": "en/apps/universalfernbedienung/help.html"}
ALT.update({v: k for k, v in list(ALT.items())})
ASSET_VERSION = ""


def nav_html(base, active, indent, lang, sub=False, extra=()):
    """Menüeinträge. Mit sub=True bekommt „Apps“ ein Untermenü (nur im Kopfbereich)."""
    ui = UI[lang]
    out = []
    for k, h, t in (NAV if lang == "de" else NAV_EN) + list(extra):
        cur = ' class="is-active" aria-current="page"' if k == active else ""
        link = f'<a href="{base}{h}" data-nav="{k}"{cur}>{t}</a>'
        if sub and k == "apps":
            out.append(f'''{indent}<li class="has-sub">{link}<button class="sub-toggle" type="button" aria-label="{ui["sub"]}" aria-expanded="false" aria-controls="subApps">{CHEVRON}</button>
{indent}  <ul class="nav__sub" id="subApps"><li><a href="{base}apps/universalfernbedienung/index.html">{ui["app"]}</a></li></ul>
{indent}</li>''')
        else:
            out.append(f"{indent}<li>{link}</li>")
    return "\n".join(out)


def head_extra(rel, lang, up, title, desc):
    """Icons, Link-Vorschau (Open Graph), Sprachverweise und App-Daten für Suchmaschinen."""
    e = lambda x: _html.escape(x, quote=True)
    site = cfg.SITE_URL.rstrip("/")
    h = [f'  <link rel="icon" href="{up}assets/favicon-32.png" sizes="32x32" type="image/png">',
         f'  <link rel="icon" href="{up}assets/favicon-48.png" sizes="48x48" type="image/png">',
         f'  <link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">',
         f'  <meta property="og:type" content="website">', f'  <meta property="og:site_name" content="Luca Flat">',
         f'  <meta property="og:title" content="{e(title)}">', f'  <meta property="og:description" content="{e(desc)}">',
         f'  <meta property="og:locale" content="{"de_DE" if lang == "de" else "en_US"}">']
    if rel == "404.html":
        h.append('  <meta name="robots" content="noindex">')
    elif site:  # absolute Adressen gibt es erst, wenn SITE_URL in site_config.py gesetzt ist
        h += [f'  <link rel="canonical" href="{site}/{rel}">', f'  <meta property="og:url" content="{site}/{rel}">',
              f'  <meta property="og:image" content="{site}/assets/og-image.png">', '  <meta property="og:image:width" content="1200">',
              '  <meta property="og:image:height" content="630">', '  <meta name="twitter:card" content="summary_large_image">']
        if rel in ALT:
            h += [f'  <link rel="alternate" hreflang="{"de" if lang == "de" else "en"}" href="{site}/{rel}">',
                  f'  <link rel="alternate" hreflang="{"en" if lang == "de" else "de"}" href="{site}/{ALT[rel]}">']
    if rel.endswith("universalfernbedienung/index.html"):
        data = {"@context": "https://schema.org", "@type": "MobileApplication", "name": UI[lang]["app"], "operatingSystem": "Android",
                "applicationCategory": "UtilitiesApplication", "description": desc, "inLanguage": lang,
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "author": {"@type": "Organization", "name": "Luca Flat"}}
        if site: data["url"] = f"{site}/{rel}"
        if PUBLISHED: data["installUrl"] = PLAY_URL
        h.append('  <script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    return "\n".join(h) + "\n"


if not inhalt.PRESSE_AKTIV:
    import shutil
    for old in ("presse.html", "en/press.html"):
        (ROOT / old).unlink(missing_ok=True)
    shutil.rmtree(ROOT / "assets" / "presse", ignore_errors=True)

for rel, active, doc_title, desc, main, *rest in PAGES:
    lang = "en" if rel.startswith("en/") else "de"
    ui = UI[lang]
    up = "../" * rel.count("/")
    base = up + ("en/" if lang == "en" else "")
    if rel == "404.html":
        from urllib.parse import urlparse
        up = base = (urlparse(cfg.SITE_URL).path.rstrip("/") + "/") if cfg.SITE_URL else "/"
        main = main.replace("@@BASE@@", base)
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    # Sprachwechsel: Gegenstück der Seite, sonst die Startseite der anderen Sprache
    alt = ALT.get(rel, "en/index.html" if lang == "de" else "index.html")
    other = "en" if lang == "de" else "de"
    switch = (f'\n          <li class="lang-switch"><a href="{up}{alt}" hreflang="{other}" lang="{other}" '
              f'aria-label="{"English version" if lang == "de" else "Deutsche Version"}">{other.upper()}</a></li>')
    de_attr = ' hreflang="de" lang="de"' if lang == "en" else ""
    legal = "\n".join(f'            <li><a href="{up}legal/{k}.html"{de_attr}>{t}</a></li>'
                      for k, t in (LEGAL_DE if lang == "de" else LEGAL_EN))
    # Großer Footer nur auf der Startseite; Unterseiten bekommen nur eine schmale Zeile mit den rechtlichen Links
    home = rel in ("index.html", "en/index.html")
    foot_nav = nav_html(base, None, " " * 12, lang, extra=ui["extra"]).replace(" data-nav", " data-x")
    footer_grid = FOOTER_GRID.format(base=base, brand=BRAND_SVG, t_pages=ui["pages"], foot_nav=foot_nav, t_legal=ui["legal"], legal_html=legal) if home else ""
    footer_legal = "" if home else (f'<nav class="footer__legal" aria-label="{ui["legal"]}">'
        + " ".join(f'<a href="{up}legal/{k}.html"{de_attr}>{t}</a>' for k, t in (LEGAL_DE if lang == "de" else LEGAL_EN)) + "</nav>")
    path.write_text(TEMPLATE.format(
        footer_grid=footer_grid, footer_legal=footer_legal, footer_class="" if home else " footer--slim",
        doc_title=doc_title, desc=desc, up=up, base=base, lang=lang, brand=BRAND_SVG, main=main,
        html_class=(" has-tabs" if "subnav-bar" in main else ""),
        nav=nav_html(base, active, " " * 10, lang, sub=True) + switch,
        foot_nav=nav_html(base, None, " " * 12, lang, extra=ui["extra"]).replace(" data-nav", " data-x"),
        head_extra=head_extra(rel, lang, up, doc_title, desc), legal_html=legal,
        t_skip=ui["skip"], t_home=ui["home"], t_mainnav=ui["mainnav"], t_menu=ui["menu"], t_pages=ui["pages"],
        t_legal=ui["legal"], t_top=ui["top"]),
        encoding="utf-8")
    print("erzeugt:", rel)

# ---- Sitemap und robots.txt (nur mit öffentlicher Adresse, sonst gibt es keine gültigen Adressen)
site = cfg.SITE_URL.rstrip("/")
if site:
    from datetime import date
    urls = "\n".join(f"  <url><loc>{site}/{rel}</loc><lastmod>{date.today().isoformat()}</lastmod></url>" for rel, *_ in PAGES if rel != "404.html")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + urls + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {site}/sitemap.xml\n", encoding="utf-8")
else:
    (ROOT / "sitemap.xml").unlink(missing_ok=True)
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    print("Hinweis: SITE_URL in site_config.py ist leer, daher gibt es noch keine sitemap.xml, canonical- und Vorschaubild-Angaben.")
