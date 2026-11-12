"""Datenschutzerklärungen: Website (selbst geschrieben) und App (aus dem Text der App übernommen)."""
import re
import html as _html
from datetime import date
from pathlib import Path

import site_config as cfg

ROOT = Path(__file__).parent
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
GITHUB_STMT = "https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement"
GITHUB_PAGES = "https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages"
GITHUB_DPA = "https://docs.github.com/en/site-policy/privacy-policies/github-data-protection-addendum"
GOOGLE_PRIVACY = "https://policies.google.com/privacy"


def print_btn():
    """Knopf zum Drucken oder Speichern als PDF; bleibt ohne JavaScript verborgen."""
    return '<p class="legal-actions"><button type="button" class="btn btn--ghost btn--sm" data-print hidden>Drucken oder als PDF speichern</button></p>'


def stand():
    d = date.today()
    return f'<p class="note">Stand: {MONATE[d.month - 1]} {d.year}</p>'


def ph(value, label):
    """Wert einsetzen oder sichtbaren Platzhalter zeigen."""
    return _html.escape(value) if value else f'<span class="ph">[{label}]</span>'


def missing_fields():
    out = []
    for val, label in [(cfg.OWNER_NAME, "Name"), (cfg.OWNER_STREET, "Straße und Hausnummer"),
                       (cfg.OWNER_CITY, "PLZ und Ort"), (cfg.OWNER_EMAIL, "E-Mail-Adresse"),
                       (getattr(cfg, "DEVELOPER_NAME", ""), "Name des Entwicklers"),
                       (cfg.SITE_URL, "öffentliche Adresse der Website")]:
        if not val:
            out.append(label)
    return out


def todo_box():
    miss = missing_fields()
    if not miss:
        return ""
    return ('<div class="placeholder-box"><strong>Noch auszufüllen:</strong> ' + ", ".join(miss) +
            '. Trage die Angaben in <code>site_config.py</code> ein und führe <code>python3 build_pages.py</code> aus. '
            'Dieser Hinweis verschwindet dann von selbst.</div>')


def developer_same():
    d = getattr(cfg, "DEVELOPER_NAME", "")
    return bool(d) and d.strip() == cfg.OWNER_NAME.strip()


def developer_line():
    """Entwickler-Hinweis; entfällt, wenn Entwickler und Anbieter dieselbe Person sind."""
    if developer_same():
        return ""
    return "<p>Entwickelt von " + ph(getattr(cfg, "DEVELOPER_NAME", ""), "Vor- und Nachname des Entwicklers") + ".</p>"


def controller_block():
    mail = (f'<a href="mailto:{_html.escape(cfg.OWNER_EMAIL)}">{_html.escape(cfg.OWNER_EMAIL)}</a>'
            if cfg.OWNER_EMAIL else ph("", "E-Mail-Adresse"))
    return ('<p>' + ph(cfg.OWNER_NAME, "Vor- und Nachname") + "<br>" + ph(cfg.OWNER_STREET, "Straße und Hausnummer") +
            "<br>" + ph(cfg.OWNER_CITY, "PLZ und Ort") + "<br>E-Mail: " + mail + "</p>" + developer_line())


def url_of(path):
    return f"{cfg.SITE_URL.rstrip('/')}/{path}" if cfg.SITE_URL else None


def toc(items):
    lis = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)
    return f'<nav class="toc" aria-label="Inhalt dieser Erklärung"><p class="toc__title">Inhalt</p><ul>{lis}</ul></nav>'


# ------------------------------------------------------------------ Website
def website_privacy_body():
    n = {}  # Nummern der Abschnitte, damit Verweise stimmen
    order = ["ueberblick", "verantwortlicher", "hosting", "speicher", "extern", "kontakt", "play", "grundlagen",
             "dauer", "sicherheit", "kinder", "rechte", "auto", "aenderung"]
    for k, key in enumerate(order, 1):
        n[key] = k
    S = []

    def sec(key, title, body):
        S.append((f"w{n[key]}", f"{n[key]}. {title}", body))

    sec("ueberblick", "Überblick", f"""
<p>Kurz gesagt: Diese Website setzt <strong>keine Cookies</strong>, speichert <strong>nichts in deinem Browser</strong>, lädt <strong>keine Inhalte von Fremdservern</strong> nach (keine Schriften, Skripte, Videos, Karten oder Bilder Dritter), nutzt <strong>keine Analyse- oder Tracking-Dienste</strong>, zeigt <strong>keine Werbung</strong> und hat <strong>keine Benutzerkonten</strong>.</p>
<p>Verarbeitet werden nur die Daten, die beim Aufruf der Seiten technisch anfallen (Punkt {n['hosting']}), und die Angaben, die du mir freiwillig per E-Mail schickst (Punkt {n['kontakt']}).</p>
<p>Diese Erklärung gilt für diese Website. Für die App „Universalfernbedienung“ gilt die eigene <a href="datenschutz-app.html">Datenschutzerklärung der App</a>.</p>""")

    sec("verantwortlicher", "Verantwortlicher", f"""
<p>Verantwortlich im Sinne der Datenschutz-Grundverordnung (DSGVO) ist:</p>
{controller_block()}
<p>Ein Datenschutzbeauftragter ist nicht benannt, da hierzu keine gesetzliche Pflicht besteht. Anfragen zum Datenschutz kannst du an die oben genannte E-Mail-Adresse richten.</p>""")

    sec("hosting", "Hosting und Server-Logfiles", f"""
<p>Diese Website wird über <strong>GitHub Pages</strong> bereitgestellt. Anbieter ist GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA.</p>
<p>Beim Aufruf einer Seite verarbeitet GitHub technisch notwendige Verbindungsdaten. Dazu gehören üblicherweise deine <strong>IP-Adresse</strong>, Datum und Uhrzeit des Zugriffs, die aufgerufene Seite oder Datei, die übertragene Datenmenge, der Statuscode der Anfrage, Angaben zu deinem Browser und Betriebssystem sowie gegebenenfalls die zuvor besuchte Seite. Nach Angaben von GitHub wird die IP-Adresse beim Besuch einer GitHub-Pages-Website aus Sicherheitsgründen protokolliert und gespeichert, unabhängig davon, ob du bei GitHub angemeldet bist (<a href="{GITHUB_PAGES}" rel="noopener">Dokumentation von GitHub</a>).</p>
<p><strong>Zweck:</strong> Auslieferung der Website, Stabilität und Sicherheit des Betriebs. <strong>Rechtsgrundlage:</strong> berechtigtes Interesse an einem sicheren und zuverlässigen Betrieb (Art. 6 Abs. 1 lit. f DSGVO). Die Bereitstellung dieser Daten ist technisch erforderlich; ohne sie kann die Website nicht angezeigt werden.</p>
<p>Ich selbst betreibe keinen eigenen Server für diese Website, führe keine eigenen Zugriffsprotokolle, werte keine Zugriffe aus und erhalte keine Besucherstatistik. Auf die bei GitHub gespeicherten Daten habe ich keinen Zugriff.</p>
<p><strong>Übermittlung in die USA:</strong> GitHub hat seinen Sitz in den USA, dort können Daten verarbeitet werden. Nach eigenen Angaben sichert GitHub Übermittlungen aus der EU durch geeignete Garantien ab, unter anderem durch Standardvertragsklauseln (<a href="{GITHUB_DPA}" rel="noopener">Datenschutzzusatz von GitHub</a>). Weitere Informationen findest du in der <a href="{GITHUB_STMT}" rel="noopener">Datenschutzerklärung von GitHub</a>.</p>
<p><strong>Speicherdauer:</strong> Sie richtet sich nach den Vorgaben von GitHub; darauf habe ich keinen Einfluss.</p>""")

    sec("speicher", "Keine Cookies, keine Speicherung im Browser", """
<p>Diese Website setzt <strong>keine Cookies</strong> und verwendet weder Local Storage, Session Storage noch IndexedDB oder vergleichbare Techniken, um Informationen auf deinem Gerät abzulegen oder auszulesen. Deshalb ist auch kein Einwilligungsbanner nötig.</p>
<p>Die Seite merkt sich nicht, welche Seiten du besucht hast oder welche Einstellungen du gewählt hast. Kleine Animationen (zum Beispiel das gezeichnete Logo) laufen rein im Browser ab und übertragen nichts.</p>""")

    sec("extern", "Keine externen Dienste und Inhalte", """
<p>Alle Bestandteile dieser Website werden von der Website selbst ausgeliefert:</p>
<ul>
<li><strong>Schriften:</strong> „Inter“ und „Space Grotesk“ liegen lokal auf dem Server (SIL Open Font License). Es werden keine Schriften von Google Fonts oder anderen Anbietern geladen.</li>
<li><strong>Skripte und Bibliotheken:</strong> Es werden keine Programme aus Content-Delivery-Netzwerken (CDN) oder von anderen Servern nachgeladen.</li>
<li><strong>Analyse und Werbung:</strong> Es gibt keine Statistik- oder Analysedienste, keine Werbenetzwerke und keinen Tag-Manager.</li>
<li><strong>Einbindungen Dritter:</strong> Es gibt keine Social-Media-Plugins, keine Karten und keine eingebetteten Videos von Plattformen wie YouTube. Sollten auf der Website Videos gezeigt werden, liegen diese auf der Website selbst.</li>
<li><strong>Bilder:</strong> Screenshots, Icons und Grafiken liegen auf der Website selbst.</li>
</ul>
<p>Die Website enthält <strong>Links zu externen Seiten</strong>, zum Beispiel zu Google Play. Erst wenn du einen solchen Link anklickst, verlässt du diese Website; für die fremde Seite gelten deren Datenschutzbestimmungen.</p>""")

    sec("kontakt", "Kontaktaufnahme", f"""
<p>Wenn du mir eine E-Mail schreibst, verarbeite ich deine Angaben (E-Mail-Adresse, Name falls angegeben, Inhalt der Nachricht), um deine Anfrage zu bearbeiten. <strong>Rechtsgrundlage</strong> ist Art. 6 Abs. 1 lit. b DSGVO, soweit die Anfrage mit einem Vertrag zusammenhängt, ansonsten das berechtigte Interesse an der Beantwortung (Art. 6 Abs. 1 lit. f DSGVO). Die Daten werden gelöscht, sobald die Anfrage erledigt ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p>
<p>Das Kontaktformular auf dieser Website sendet <strong>selbst nichts an einen Server</strong>. Es bereitet nur eine E-Mail vor und öffnet dein E-Mail-Programm. Erst wenn du die Nachricht dort abschickst, erhalte ich sie. Deine Eingaben im Formular verlassen deinen Browser also nicht, bevor du sie selbst versendest.</p>
<p>Hinweis: Eine E-Mail ohne zusätzliche Verschlüsselung ist nicht so vertraulich wie ein Brief. Sende deshalb keine sensiblen Angaben per E-Mail. Die Verarbeitung durch deinen E-Mail-Anbieter richtet sich nach dessen Datenschutzbestimmungen.</p>""")

    sec("play", "Verweis auf Google Play", f"""
<p>Die Website verweist auf die App im Google Play Store (sobald sie dort veröffentlicht ist). Wenn du einen solchen Link anklickst, wird Google Play geöffnet. Dort verarbeitet Google Daten in eigener Verantwortung nach seinen Datenschutzbestimmungen (<a href="{GOOGLE_PRIVACY}" rel="noopener">policies.google.com/privacy</a>). Darauf habe ich keinen Einfluss. Google kann Daten auch in den USA verarbeiten.</p>""")

    sec("grundlagen", "Rechtsgrundlagen im Überblick", """
<ul>
<li>Bereitstellung und Sicherheit der Website, Server-Logfiles bei GitHub: berechtigtes Interesse, Art. 6 Abs. 1 lit. f DSGVO</li>
<li>Beantwortung von Anfragen: Art. 6 Abs. 1 lit. b oder lit. f DSGVO</li>
<li>Ein Zugriff auf dein Endgerät (§ 25 TDDDG) findet nicht statt, weil keine Cookies oder vergleichbaren Techniken eingesetzt werden.</li>
</ul>""")

    sec("dauer", "Speicherdauer und Löschung", """
<p>Eigene Daten über Besucher dieser Website speichere ich nicht. E-Mails bewahre ich nur so lange auf, wie es zur Bearbeitung der Anfrage nötig ist. Danach lösche ich sie, sofern keine gesetzlichen Aufbewahrungspflichten bestehen. Für Daten, die GitHub verarbeitet, gilt Punkt """ + str(n["hosting"]) + """.</p>""")

    sec("sicherheit", "Datensicherheit", """
<p>Die Website wird über eine verschlüsselte Verbindung (HTTPS) ausgeliefert. Du erkennst das am Schloss-Symbol in der Adresszeile deines Browsers. Dadurch können Dritte im Netzwerk nicht mitlesen, welche Seiten du aufrufst.</p>""")

    sec("kinder", "Kinder", """
<p>Die Website richtet sich nicht gezielt an Kinder unter 16 Jahren. Ich erhebe wissentlich keine Daten über Kinder.</p>""")

    sec("rechte", "Deine Rechte", f"""
<p>Du hast gegenüber dem Verantwortlichen folgende Rechte:</p>
<ul>
<li>Auskunft über die zu deiner Person verarbeiteten Daten (Art. 15 DSGVO)</li>
<li>Berichtigung unrichtiger Daten (Art. 16 DSGVO)</li>
<li>Löschung (Art. 17 DSGVO)</li>
<li>Einschränkung der Verarbeitung (Art. 18 DSGVO)</li>
<li>Datenübertragbarkeit (Art. 20 DSGVO)</li>
<li>Widerspruch gegen Verarbeitungen auf Grundlage berechtigter Interessen (Art. 21 DSGVO)</li>
<li>Widerruf einer erteilten Einwilligung mit Wirkung für die Zukunft (Art. 7 Abs. 3 DSGVO)</li>
</ul>
<p>Da ich selbst keine Daten über Besucher dieser Website speichere, liegen bei mir in der Regel keine personenbezogenen Daten über dich vor, außer deinen E-Mails. Auskunfts- und Löschwünsche zu den Daten, die GitHub verarbeitet, richtest du an GitHub.</p>
<p><strong>Beschwerderecht:</strong> Du kannst dich bei einer Datenschutz-Aufsichtsbehörde beschweren (Art. 77 DSGVO), insbesondere in dem Mitgliedstaat deines Aufenthaltsorts. Für den Verantwortlichen zuständig ist: {_html.escape(cfg.SUPERVISORY_AUTHORITY)}.</p>""")

    sec("auto", "Keine automatisierte Entscheidungsfindung", """
<p>Es findet keine automatisierte Entscheidungsfindung einschließlich Profiling im Sinne von Art. 22 DSGVO statt.</p>""")

    page_url = url_of("legal/datenschutz.html")
    sec("aenderung", "Änderungen dieser Erklärung", f"""
<p>Ändern sich die Website oder rechtliche Anforderungen, passe ich diese Erklärung an. Die jeweils aktuelle Fassung findest du unter {('<a href="' + page_url + '">' + _html.escape(page_url) + '</a>') if page_url else ph("", "öffentliche Adresse dieser Seite")}.</p>""")

    body = "".join(f'<section class="legal-sec"><h2 id="{i}">{t}</h2>{b}</section>' for i, t, b in S)
    return f'<div class="legal-doc">{todo_box()}{stand()}{print_btn()}{toc([(i, t) for i, t, _ in S])}{body}</div>'


# ---------------------------------------------------------------------- App
def app_privacy_body():
    """Text 1:1 aus der App (content/app-datenschutz-quelle.html, aus index.html übernommen).
    Aufbau wie in der App: Stand – Inhalt – nummerierte Abschnitte. Ersetzt werden nur die Platzhalter
    (Verantwortlicher, Aufsichtsbehörde, öffentliche Adresse) durch die Angaben aus site_config.py."""
    src = (ROOT / "content" / "app-datenschutz-quelle.html").read_text(encoding="utf-8")
    h = src

    # Stand aus der App übernehmen (gleiches Datum wie in der App), interne Anbieter-Hinweise entfernen
    m = re.match(r'\s*(<p class="note">Stand: [^<]*</p>)', h)
    stand_html = m.group(1) if m else stand()
    if m: h = h[m.end():]
    h, n_hint = re.subn(r'<p class="note"><b>Hinweis für den Anbieter.*?</p>', "", h, flags=re.S)

    # Verantwortlicher, Aufsichtsbehörde, öffentliche Adresse
    h, n_ctrl = re.subn(r'<p><span class="ph">\[Name oder Firma\]</span>.*?\[E-Mail-Adresse\]</span></p>',
                        lambda m: controller_block(), h, flags=re.S)
    h = re.sub(r'<span class="ph">\[zuständige Aufsichtsbehörde[^<]*\]</span>', lambda m: _html.escape(cfg.SUPERVISORY_AUTHORITY), h)
    page_url = url_of("legal/datenschutz-app.html")
    h = re.sub(r'<span class="ph">\[öffentliche Adresse der Datenschutzerklärung\]</span>',
               lambda m: ('<a href="' + page_url + '">' + _html.escape(page_url) + '</a>') if page_url else ph("", "öffentliche Adresse dieser Seite"), h)

    # Überschriften → h2 mit denselben Sprungmarken wie in der App (#a1 … #a24)
    items = []
    def head(m):
        title = m.group(1)
        mm = re.match(r"(\d+[a-z]?)\.", title)
        i = "a" + (mm.group(1) if mm else str(len(items) + 1))
        items.append((i, title))
        return f'</section><section class="legal-sec"><h2 id="{i}">{title}</h2>'
    h = re.sub(r"<h3>(.*?)</h3>", head, h)
    h = "<section class=\"legal-sec\">" + h.lstrip() + "</section>"
    h = h.replace("<section class=\"legal-sec\"></section>", "", 1)
    h = h.replace("<b>", "<strong>").replace("</b>", "</strong>")

    print(f"App-Datenschutz: {len(items)} Abschnitte, Anbieter-Hinweis entfernt: {n_hint}, Verantwortlicher ersetzt: {n_ctrl}")
    return f'<div class="legal-doc">{todo_box()}{print_btn()}{stand_html}{toc(items)}{h}</div>'


# ------------------------------------------------------------------ Impressum
def impressum_body():
    phone = getattr(cfg, "OWNER_PHONE", "")
    tel = f"<br>Telefon: {_html.escape(phone)}" if phone else ""
    return (f'<div class="legal-doc">{todo_box()}{print_btn()}'
            '<section class="legal-sec"><h2 id="anbieter">Angaben gemäß § 5 DDG</h2>'
            '<p>' + ph(cfg.OWNER_NAME, "Vor- und Nachname") + "<br>" + ph(cfg.OWNER_STREET, "Straße und Hausnummer") +
            "<br>" + ph(cfg.OWNER_CITY, "PLZ und Ort") + "</p></section>"
            + ("" if developer_same() else '<section class="legal-sec"><h2 id="entwickler">Entwickler der Apps</h2>' + developer_line() + '</section>') +
            '<section class="legal-sec"><h2 id="kontakt">Kontakt</h2>'
            "<p>E-Mail: " + (f'<a href="mailto:{_html.escape(cfg.OWNER_EMAIL)}">{_html.escape(cfg.OWNER_EMAIL)}</a>'
                             if cfg.OWNER_EMAIL else ph("", "E-Mail-Adresse")) + tel + "</p>"
            '<p>Du kannst mir auch über die <a href="../kontakt.html">Kontaktseite</a> schreiben.</p></section>'
            '</div>')
