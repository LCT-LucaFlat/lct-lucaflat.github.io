"""Zusätzliche Seiten der Website: App-Seite, Hilfe, Presse (Deutsch und Englisch) sowie die
englische Fassung der Standardseiten. Wird von build_pages.py eingebunden.
Texte stehen hier gebündelt, damit sie an einer Stelle gepflegt werden können."""
import html as _html
import zipfile
from pathlib import Path

APP = "universalfernbedienung"
SCREENS = [  # Datei, Höhe, (Titel, Beschreibung, Alt-Text) je Sprache
    ("fernbedienung", 1078,
     ("Fernbedienung", "Alle wichtigen Tasten auf einem Bildschirm.", "Hauptbildschirm mit Richtungstasten, Lautstärke, Kanälen und Tasten für Streaming-Apps"),
     ("Remote", "All important keys on one screen.", "Main screen with D-pad, volume, channels and streaming apps")),
    ("streaming-suche", 1102,
     ("Streaming-Suche", "Titel eingeben und an die App senden.", "Streaming-Suche mit Tastatur zur Eingabe von Titeln"),
     ("Streaming search", "Enter a title and send it to the app.", "Streaming search with keyboard for entering titles")),
    ("einstellungen", 1104,
     ("Einstellungen", "Alles an einem Ort, übersichtlich sortiert.", "Einstellungen mit Fernseher, Darstellung, Bedienung, Sprachbefehlen, Makros, Fehlerprotokoll, Lieblingssendern, Sprache und Rundgang"),
     ("Settings", "Everything in one place, neatly sorted.", "Settings with TV, appearance, controls, voice commands, macros, error log, favourite channels, language and tour")),
    ("darstellung", 1103,
     ("Darstellung", "Vier Designs mit eigenen Farbschemen, Gesten oder Kompakt.", "Darstellung mit der Auswahl der Designs Original, Rechenwerk, Stellwerk und Programmheft sowie Farbschema und Ansicht"),
     ("Appearance", "Four designs with their own colour schemes, gestures or compact.", "Appearance with the choice of the designs Original, Calculator, Signal box and TV guide as well as colour scheme and view")),
    ("beruehrungsschutz", 1100,
     ("Berührungsschutz", "Schützt vor versehentlichen Eingaben.", "Berührungsschutz: zum Entsperren nach oben ziehen"),
     ("Touch lock", "Protects against accidental input.", "Touch lock: swipe up to unlock")),
]
WIDGETS = [  # Datei, Breite, Höhe, Klasse, (Titel, Text, Alt) je Sprache
    ("widget-fernbedienung", 746, 504, "w-wide",
     ("Fernbedienung", "4×2: Name, Ein/Aus, Lautstärke, Sender, Zurück, Home, Eingang.",
      "Widget Fernbedienung mit Ein/Aus, Stumm, Lautstärke, Sender, Zurück, Home, Eingang und App öffnen"),
     ("Remote", "4×2: name, on/off, volume, channels, back, home, input.",
      "Remote widget with on/off, mute, volume, channels, back, home, input and open app")),
    ("widget-mini", 746, 227, "w-wide",
     ("Fernbedienung Mini", "4×1: Ein/Aus, Lautstärke und Stumm.", "Widget Fernbedienung Mini mit Ein/Aus, Lautstärke und Stumm"),
     ("Remote Mini", "4×1: on/off, volume and mute.", "Remote Mini widget with on/off, volume and mute")),
    ("widget-steuerkreuz", 547, 781, "w-dpad",
     ("Steuerkreuz", "3×3: Pfeile, OK, Zurück, Home und Lautstärke.", "Widget Steuerkreuz mit Pfeilen, OK, Zurück, Home und Lautstärke"),
     ("D-pad", "3×3: arrows, OK, back, home and volume.", "D-pad widget with arrows, OK, back, home and volume")),
]

FEATURES = {
    "de": ["Zwei Bedienarten: Gesten mit großer Wischfläche oder kompakt mit allen Tasten, dazu wahlweise Pfeiltasten oder Touchpad",
           "Vier Designs: Original, Rechenwerk, Stellwerk und Programmheft, jeweils mit eigenen Farbschemen",
           "Sony Bravia und Android TV: Fernseher im Netzwerk finden und einrichten",
           "Sender, Apps und Makros: mehrere Schritte mit einem Tipp",
           "Sprachbefehle: per Tipp auf das Mikrofon, auch mit eigenen Sätzen",
           "Streaming-Suche: Titel eingeben und direkt an die Streaming-App senden",
           "Benachrichtigungsfeld (optional): Ein/Aus, Lautstärke, Sender, Steuerkreuz und OK, auch bei geschlossener App",
           "Drei Widgets: Mini (Ein/Aus, Lautstärke, Stumm), Fernbedienung (mit Sendern, Zurück, Home und Eingang) und Steuerkreuz",
           "Berührungsschutz: verhindert versehentliche Eingaben",
           "Fehlerprotokoll: Wenn eine Taste nicht funktioniert, zeigt die App Code und Lösungshinweis",
           "Mehrere Fernseher: speichern und mit einem Tipp auf den Namen oben links wechseln",
           "Neustart des Fernsehers: in der Ansicht „Kompakt“, zur Sicherheit erst nach zweimaligem Antippen (bei Android TV hält die App dafür Ein/Aus fünf Sekunden gedrückt)",
           "Eingänge: alle auf einen Blick (bei Android TV einmal anlernbar), dazu Zahlentasten und Lieblingssender als Schnellwahl",
           "Bei Sony Bravia zusätzlich: genaue Lautstärke, Anzeige des laufenden Programms, Bildmodus und Senderliste vom Fernseher",
           "10 Sprachen: darunter Deutsch, Englisch, Französisch und Spanisch"],
    "en": ["Two control styles: gestures with a large swipe area, or compact with all keys, plus either arrow keys or a touchpad",
           "Four designs: Original, Calculator, Signal box and TV guide, each with its own colour schemes",
           "Sony Bravia and Android TV: find and set up your TV on the network",
           "Channels, apps and macros: several steps with one tap",
           "Voice commands: tap the microphone, including your own phrases",
           "Streaming search: type a title and send it straight to the streaming app",
           "Notification panel (optional): on/off, volume, channels, D-pad and OK, even when the app is closed",
           "Three widgets: Mini (on/off, volume, mute), Remote (with channels, back, home and input) and D-pad",
           "Touch lock: prevents accidental input",
           "Error log: if a key does not work, the app shows a code and a hint for solving it",
           "Several TVs: save them and switch with one tap on the name at the top left",
           "TV restart: in the “Compact” view, only after tapping twice to be safe (on Android TV the app holds on/off for five seconds)",
           "Inputs: all at a glance (teachable once on Android TV), plus number keys and favourite channels for quick access",
           "On Sony Bravia also: exact volume, display of what is playing, picture mode and the TV’s channel list",
           "10 languages: including German, English, French and Spanish"],
}

T = {  # Oberflächentexte der App-Seite
    "de": dict(title="Universalfernbedienung", lead="Dein Handy als Fernbedienung für den Fernseher.",
               tabs=["Überblick", "Funktionen", "Screenshots", "Kompatibilität", "Download", "Hilfe"], tabs_label="Abschnitte dieser Seite",
               intro="Die Universalfernbedienung macht dein Handy zur Fernbedienung. Sie verbindet sich über dein WLAN direkt mit dem Fernseher, ohne Umweg über einen Server. Sie funktioniert mit Sony Bravia sowie mit Android TV und Google TV.",
               h_feat="Funktionen", h_shots="Screenshots", h_video="Streaming-Suche im Video", h_widgets="Widgets für den Startbildschirm",
               h_compat="Kompatibilität", h_dl="Download",
               compat="Funktioniert mit Sony-Bravia-Fernsehern (IP-Steuerung mit PSK) sowie mit Fernsehern und Zuspielern mit Android TV oder Google TV (Kopplung per Code). Handy und Fernseher müssen sich im selben WLAN befinden. Bei Sony Bravia stehen einige Funktionen mehr bereit, etwa genaue Lautstärke, Bildmodus und ein echter Neustart. Bei Android TV hängen Eingänge und Neustart vom Hersteller ab.",
               marks="Sony und Bravia sind Marken der Sony Group Corporation, Android TV und Google TV Marken von Google LLC. Diese App ist ein unabhängiges Projekt und steht in keiner Verbindung zu diesen Unternehmen.",
               soon="Der Link zum Play Store erscheint hier, sobald die App veröffentlicht ist.", play="Bei Google Play ansehen", badge_alt="Jetzt bei Google Play",
               gp="Google Play ist eine Marke von Google LLC.",
               privacy='Keine Werbung und kein Tracking. Details stehen in der <a href="{A}legal/datenschutz-app.html">Datenschutzerklärung der App</a>.',
               help='Probleme oder Fragen? Die <a href="hilfe.html">Hilfe zur App</a> erklärt Verbindung, Widgets und Fehlerprotokoll.',
               video_caption="Titel eingeben und direkt an die Streaming-App senden.",
               video_alt="Video: Streaming-Suche der Universalfernbedienung", video_fallback="Dein Browser kann dieses Video nicht abspielen.",
               desc="Universalfernbedienung: dein Handy als Fernbedienung für den Fernseher.", doc="Universalfernbedienung – Luca Flat"),
    "en": dict(title="Universal Remote", lead="Your phone as a remote control for your TV.",
               tabs=["Overview", "Features", "Screenshots", "Compatibility", "Download", "Help"], tabs_label="Sections of this page",
               intro="The Universal Remote turns your phone into a remote control. It connects to your TV directly over your Wi-Fi, without going through a server. It works with Sony Bravia as well as Android TV and Google TV.",
               h_feat="Features", h_shots="Screenshots", h_video="Streaming search in a video", h_widgets="Home-screen widgets",
               h_compat="Compatibility", h_dl="Download",
               compat="Works with Sony Bravia TVs (IP control with PSK) and with TVs and streaming devices running Android TV or Google TV (pairing by code). Your phone and TV must be on the same Wi-Fi network. Sony Bravia offers a few more functions, such as exact volume, picture mode and a true restart. On Android TV, inputs and restart depend on the manufacturer.",
               marks="Sony and Bravia are trademarks of Sony Group Corporation; Android TV and Google TV are trademarks of Google LLC. This app is an independent project and is not affiliated with these companies.",
               soon="The link to Google Play will appear here once the app is published.", play="View on Google Play", badge_alt="Get it on Google Play",
               gp="Google Play is a trademark of Google LLC.",
               privacy='No ads and no tracking. Details are in the <a href="{A}legal/datenschutz-app.html" hreflang="de" lang="de">app privacy policy</a> (in German).',
               help='Problems or questions? The <a href="help.html">app help</a> covers connecting, widgets and the error log.',
               video_caption="Type a title and send it straight to the streaming app.",
               video_alt="Video: streaming search of the Universal Remote", video_fallback="Your browser cannot play this video.",
               desc="Universal Remote: your phone as a remote control for your TV.", doc="Universal Remote – Luca Flat"),
}
# Pressebereich (Seite, Footer-Link, ZIP): auf True setzen und build_pages.py ausführen, sobald er gebraucht wird
PRESSE_AKTIV = False
LEGAL_NOTE_EN = '<span class="note">(in German)</span>'


def build(ctx):
    """Liefert alle zusätzlichen Seiten als (rel, active, doc_title, desc, main)."""
    page_head, prose, ROOT, cfg = ctx["page_head"], ctx["prose"], ctx["ROOT"], ctx["cfg"]
    PUBLISHED, PLAY_URL = ctx["PUBLISHED"], ctx["PLAY_URL"]
    esc = _html.escape
    pages = []

    def badge(lang):
        return ('<span class="status status--live">%s</span>' % ("Im Play Store" if lang == "de" else "On Google Play")) if PUBLISHED else \
               ('<span class="status status--wip">%s</span>' % ("Bald im Play Store" if lang == "de" else "Coming soon to Google Play"))

    def dirs(lang, depth):
        """R: Weg zur Sprachwurzel (Seiten), A: Weg zur Website-Wurzel (Dateien)."""
        R = "../" * depth
        return R, (R if lang == "de" else R + "../")

    # ------------------------------------------------------------- App-Seite
    def app_page(lang):
        t = T[lang]; i = 0 if lang == "de" else 1
        R, A = dirs(lang, 2)
        base = "" if lang == "de" else "en/"
        shots = "\n".join(
            f'          <figure><div class="phone"><img src="{A}assets/screens/{n}.webp" width="540" height="{h}" alt="{esc(s[i][2])}" loading="lazy" decoding="async"></div>'
            f'<figcaption><strong>{esc(s[i][0])}</strong>{esc(s[i][1])}</figcaption></figure>' for n, h, *s in [(x[0], x[1], x[2], x[3]) for x in SCREENS if x[0] != "fernbedienung"])
        video = ""
        if ctx["VIDEO_FILE"].exists():
            video = (f'          <h3 class="shots-sub">{t["h_video"]}</h3>\n          <figure class="video">\n'
                     f'            <video controls preload="none" playsinline poster="{A}assets/screens/streaming-suche.webp" aria-label="{t["video_alt"]}">\n'
                     f'              <source src="{A}assets/video/streaming-suche.mp4" type="video/mp4">\n              {t["video_fallback"]}\n            </video>\n'
                     f'            <figcaption><strong>{SCREENS[1][2 + i][0]}</strong>{t["video_caption"]}</figcaption>\n          </figure>\n')
        widgets = "\n".join(
            f'            <figure class="{c}"><img src="{A}assets/screens/{n}.webp" width="{w}" height="{h}" alt="{esc(x[i][2])}" loading="lazy" decoding="async">'
            f'<figcaption><strong>{esc(x[i][0])}</strong>{esc(x[i][1])}</figcaption></figure>' for n, w, h, c, *x in WIDGETS_ROWS)
        if PUBLISHED:
            bf = next((p for p in ("google-play-badge.svg", "google-play-badge.png") if (ROOT / "assets" / p).exists()), None)
            btn = (f'<a href="{PLAY_URL}" rel="noopener"><img src="{A}assets/{bf}" height="60" alt="{t["badge_alt"]}"></a>' if bf
                   else f'<a class="btn" href="{PLAY_URL}" rel="noopener">{t["play"]}</a>')
            dl = f'<p>{btn}</p>\n            <p class="note">{t["gp"]}</p>'
        else:
            dl = f'<p>{t["soon"]}</p>'
        anchors = ["ueberblick", "funktionen", "screenshots", "kompatibilitaet", "download"]
        bar = ('    <div class="subnav-bar"><div class="container"><nav class="subnav" aria-label="%s">' % t["tabs_label"]
               + "".join(f'<a href="#{a}">{n}</a>' for a, n in zip(anchors, t["tabs"][:5]))
               + f'<a href="{"hilfe" if lang == "de" else "help"}.html">{t["tabs"][5]}</a></nav></div></div>')
        def feat(x):
            head, sep, rest = x.partition(": ")
            return f"<strong>{esc(head)}:</strong> {esc(rest)}" if sep and len(head) < 60 else esc(x)
        feats = "\n".join(f"            <li>{feat(x)}</li>" for x in FEATURES[lang])
        icon = (f'<span class="title-with-icon"><img class="app-icon" src="{A}assets/app-icon-192.png" width="76" height="76" alt=""><span>{t["title"]}</span></span>')
        main = (page_head(R, [], icon, t["lead"], "") + "\n" + bar + f"""
    <section class="section" style="padding-top:1rem;">
      <div class="container">
        <div class="about" id="ueberblick">
          <div>
            <p>{t["intro"]}</p>
            <p>{badge(lang)}</p>
          </div>
          <figure class="phone phone--single"><img src="{A}assets/screens/fernbedienung.webp" width="540" height="{SCREENS[0][1]}" alt="{esc(SCREENS[0][2 + i][2])}" decoding="async"></figure>
        </div>

        <section class="app-sec" id="funktionen">
          <h2>{t["h_feat"]}</h2>
          <div class="app-text"><ul>
{feats}
          </ul></div>
        </section>

        <section class="app-sec" id="screenshots">
          <h2>{t["h_shots"]}</h2>
          <div class="shots">
{shots}
          </div>
{video}          <h3 class="shots-sub">{t["h_widgets"]}</h3>
          <div class="widgets">
{widgets}
          </div>
        </section>

        <section class="app-sec" id="kompatibilitaet">
          <h2>{t["h_compat"]}</h2>
          <div class="app-text">
            <p>{t["compat"]}</p>
            <p class="note">{t["marks"]}</p>
          </div>
        </section>

        <section class="app-sec" id="download">
          <h2>{t["h_dl"]}</h2>
          <div class="app-text">
            {dl}
            <p>{t["privacy"].format(A=A)}</p>
            <p>{t["help"]}</p>
          </div>
        </section>
      </div>
    </section>""")
        rel = f"{base}apps/{APP}/index.html"
        pages.append((rel, "apps", t["doc"], t["desc"], main, A))

    WIDGETS_ROWS = WIDGETS
    app_page("de"); app_page("en")

    # ------------------------------------------------------------- Hilfe
    HELP = {
        "de": dict(doc="Hilfe zur Universalfernbedienung – Luca Flat", desc="Hilfe zur Universalfernbedienung: Verbindung, Widgets, Berührungsschutz und Fehlerprotokoll.",
                   title="Hilfe", lead="Verbindung herstellen, Probleme lösen und Funktionen finden.", back="Zurück zur App",
                   sections=[
                       ("Erste Schritte", """<ol>
<li>Handy und Fernseher müssen im selben WLAN sein.</li>
<li>Öffne die App und richte deinen Fernseher ein. Bei <b>Sony Bravia</b> schaltest du am Fernseher die IP-Steuerung ein, legst einen Schlüssel (PSK) fest und trägst ihn in der App ein. Bei <b>Android TV und Google TV</b> zeigt der Fernseher beim ersten Verbinden einen Code, den du in der App eingibst (Kopplung).</li>
<li>Wähle in den Einstellungen unter „Darstellung“ dein Design mit Farbschema und die Bedienart: Gesten mit großer Wischfläche oder kompakt mit allen Tasten, dazu Pfeiltasten oder Touchpad.</li>
<li>Ein Rundgang in den Einstellungen zeigt dir die wichtigsten Funktionen noch einmal.</li>
</ol>"""),
                       ("Fernseher wird nicht gefunden oder eine Taste reagiert nicht", """<ul>
<li>Der Fernseher muss eingeschaltet oder im Netzwerk-Standby sein, und Handy und Fernseher müssen im selben WLAN hängen.</li>
<li>Manche Router trennen Geräte voneinander (zum Beispiel Gast-WLAN oder „Client-Isolation“). Dann sieht das Handy den Fernseher nicht.</li>
<li>Ein aktives VPN auf dem Handy kann die Verbindung im Heimnetz stören. Schalte es zum Test aus.</li>
<li>Bei Sony Bravia müssen die IP-Steuerung am Fernseher eingeschaltet und der PSK in der App richtig eingetragen sein. Das Fehlerprotokoll nennt dazu zum Beispiel „IP-Steuerung am Sony aus“ oder „PSK falsch“.</li>
<li>Bei Android TV und Google TV hilft es oft, den Fernseher neu zu koppeln, wenn die Kopplung abgelehnt wurde oder fehlgeschlagen ist. Manche Fernseher lassen nur ein Handy gleichzeitig als Fernbedienung zu.</li>
<li>Ab Android 17 braucht die App die Erlaubnis „Geräte in der Nähe“, um Fernseher im Heimnetz zu erreichen. Fehlt sie, zeigt die App den Code G305 und einen Knopf zum Erlauben.</li>
<li>Lässt sich der Fernseher nach dem Ausschalten nicht wieder einschalten, schalte am Fernseher „Fern-Start“ (Sony) bzw. „Netzwerk-Standby“ oder „Über WLAN einschalten“ ein.</li>
<li>Öffne in den Einstellungen das Fehlerprotokoll. Es zeigt Fehlercodes mit Erklärung und Lösungshinweis. Mit „Leeren“ löschst du es wieder.</li>
</ul>"""),
                       ("Mehrere Fernseher, Neustart und Eingänge", """<ul>
<li>Tippe oben links auf den Namen, um zwischen deinen gespeicherten Fernsehern zu wechseln oder einen neuen hinzuzufügen.</li>
<li>In der Ansicht „Kompakt“ musst du „Neustart“ zur Sicherheit zweimal antippen. Android TV kennt keinen eigenen Neustart-Befehl, deshalb hält die App Ein/Aus fünf Sekunden gedrückt. Je nach Hersteller erscheint dann ein Menü mit „Neustart“, oder der Fernseher schaltet nur aus. Am zuverlässigsten ist eine Bravia, die zusätzlich als Sony eingerichtet ist.</li>
<li>Unter „Eingänge“ siehst du die Eingänge deines Fernsehers. Antippen wechselt direkt dorthin. Android TV hat dafür keinen einheitlichen Befehl: Klappt das Umschalten nicht, tippe auf „Eingang anlernen“ und zeig der App einmal den Weg durchs Eingangsmenü. Danach genügt ein Tipp.</li>
</ul>"""),
                       ("Berührungsschutz", "<p>Der Berührungsschutz verhindert versehentliche Eingaben. Zum Entsperren ziehst du auf dem Bildschirm nach oben.</p>"),
                       ("Widgets und Benachrichtigungsfeld", """<ul>
<li>Es gibt drei Widgets: Mini (Ein/Aus, Lautstärke, Stumm), Fernbedienung (mit Sendern, Zurück, Home und Eingang) und Steuerkreuz.</li>
<li>Widgets fügst du wie bei jeder Android-App hinzu: Auf dem Startbildschirm lange auf eine freie Stelle tippen, „Widgets“ wählen und die Universalfernbedienung suchen.</li>
<li>Die Fernbedienung im Benachrichtigungsfeld ist optional und lässt sich in den Einstellungen einschalten.</li>
</ul>"""),
                       ("Sprachbefehle, Makros und Streaming-Suche", """<ul>
<li>Sprachbefehle startest du mit einem Tipp auf das Mikrofon. Eigene Sätze kannst du in den Einstellungen anlegen.</li>
<li>Makros führen mehrere Schritte mit einem Tipp aus.</li>
<li>Die Streaming-Suche sendet einen eingegebenen Titel direkt an die Streaming-App.</li>
</ul>"""),
                       ("Weiter Hilfe nötig?", '<p>Schreib mir über die <a href="{R}kontakt.html">Kontaktseite</a>. Hilfreich sind das Modell deines Fernsehers, die Art der Verbindung und der Code aus dem Fehlerprotokoll.</p>'),
                   ]),
        "en": dict(doc="Help for the Universal Remote – Luca Flat", desc="Help for the Universal Remote: connecting, widgets, touch lock and the error log.",
                   title="Help", lead="Connect, solve problems and find features.", back="Back to the app",
                   sections=[
                       ("Getting started", """<ol>
<li>Your phone and TV must be on the same Wi-Fi network.</li>
<li>Open the app and set up your TV. On a <b>Sony Bravia</b> you switch on IP control on the TV, set a key (PSK) and enter it in the app. On <b>Android TV and Google TV</b> the TV shows a code the first time you connect, and you enter it in the app (pairing).</li>
<li>In the settings under “Appearance”, choose your design with its colour scheme and control style: gestures with a large swipe area, or compact with all keys, plus arrow keys or a touchpad.</li>
<li>A tour in the settings shows you the most important features again.</li>
</ol>"""),
                       ("TV is not found or a key does not respond", """<ul>
<li>The TV must be on or in network standby, and phone and TV must be on the same Wi-Fi network.</li>
<li>Some routers separate devices from each other (for example guest Wi-Fi or “client isolation”). Then the phone cannot see the TV.</li>
<li>An active VPN on the phone can interfere with the home network. Turn it off to test.</li>
<li>On a Sony Bravia, IP control must be switched on at the TV and the PSK entered correctly in the app. The error log names this, for example as “IP control off on Sony” or “wrong PSK”.</li>
<li>On Android TV and Google TV it often helps to pair the TV again if pairing was rejected or failed. Some TVs only allow one phone at a time as a remote.</li>
<li>From Android 17 the app needs the “Nearby devices” permission to reach TVs on your home network. If it is missing, the app shows code G305 and a button to allow it.</li>
<li>If the TV cannot be switched back on after turning it off, enable “Remote start” (Sony) or “Network standby” / “Wake on Wi-Fi” on the TV.</li>
<li>Open the error log in the settings. It shows error codes with an explanation and a hint for solving them. “Clear” deletes it again.</li>
</ul>"""),
                       ("Several TVs, restart and inputs", """<ul>
<li>Tap the name at the top left to switch between your saved TVs or add a new one.</li>
<li>In the “Compact” view you must tap “Restart” twice for safety. Android TV has no restart command of its own, so the app holds on/off for five seconds. Depending on the manufacturer, a menu with “Restart” appears, or the TV only switches off. A Bravia that is also set up as a Sony is the most reliable.</li>
<li>Under “Inputs” you see your TV’s inputs. Tapping one switches straight to it. Android TV has no common command for this: if switching does not work, tap “Teach input” and show the app the way through the input menu once. After that, one tap is enough.</li>
</ul>"""),
                       ("Touch lock", "<p>The touch lock prevents accidental input. To unlock, swipe up on the screen.</p>"),
                       ("Widgets and notification panel", """<ul>
<li>There are three widgets: Mini (on/off, volume, mute), Remote (with channels, back, home and input) and D-pad.</li>
<li>Add widgets as with any Android app: long-press an empty spot on the home screen, choose “Widgets” and look for the Universal Remote.</li>
<li>The remote in the notification panel is optional and can be switched on in the settings.</li>
</ul>"""),
                       ("Voice commands, macros and streaming search", """<ul>
<li>Start voice commands by tapping the microphone. You can add your own phrases in the settings.</li>
<li>Macros run several steps with one tap.</li>
<li>Streaming search sends a title you type straight to the streaming app.</li>
</ul>"""),
                       ("Still need help?", '<p>Write to me via the <a href="{R}contact.html">contact page</a>. It helps to include your TV model, how you connect and the code from the error log.</p>'),
                   ]),
    }
    for lang in ("de", "en"):
        h = HELP[lang]; R, A = dirs(lang, 2)
        body = "\n".join(f'<h2 id="h{n}">{esc(s[0])}</h2>\n{s[1].replace("{R}", R)}' for n, s in enumerate(HELP[lang]["sections"], 1))
        tt = "Inhalt" if lang == "de" else "Contents"
        toc = f'<nav class="toc" aria-label="{tt}"><p class="toc__title">{tt}</p><ul>' + "".join(
            f'<li><a href="#h{n}">{esc(sec[0])}</a></li>' for n, sec in enumerate(h["sections"], 1)) + "</ul></nav>\n"
        body = toc + body
        body += f'\n<p><a class="btn btn--ghost" href="index.html">{h["back"]}</a></p>'
        rel = ("" if lang == "de" else "en/") + f"apps/{APP}/" + ("hilfe.html" if lang == "de" else "help.html")
        pages.append((rel, "apps", h["doc"], h["desc"], page_head(R, [], h["title"], h["lead"], "") + "\n" + prose(body), A))

    # ------------------------------------------------------------- Presse
    if PRESSE_AKTIV:
        PRESS_FILES = [("app-icon-192.png", "assets/app-icon-192.png")] + \
                      [(f"{s[0]}.jpg", f"assets/screens/{s[0]}.jpg") for s in SCREENS] + \
                      [(f"{w[0]}.png", f"assets/screens/{w[0]}.png") for w in WIDGETS]
        SHORT = {"de": "Universalfernbedienung: Dein Handy als Fernbedienung für den Fernseher. Die Android-App verbindet sich über das WLAN direkt mit dem Fernseher, ohne Umweg über einen Server, und funktioniert mit Sony Bravia sowie mit Android TV und Google TV. Keine Werbung, kein Tracking.",
                 "en": "Universal Remote: your phone as a remote control for your TV. The Android app connects to the TV directly over Wi-Fi, without going through a server, and works with Sony Bravia as well as Android TV and Google TV. No ads, no tracking."}
        zdir = ROOT / "assets" / "presse"; zdir.mkdir(parents=True, exist_ok=True)
        zpath = zdir / "universalfernbedienung-presse.zip"
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:  # feste Zeitstempel, damit die Datei reproduzierbar bleibt
            for name, src in PRESS_FILES:
                zi = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(zi, (ROOT / src).read_bytes())
            zi = zipfile.ZipInfo("kurzbeschreibung.txt", (2026, 1, 1, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, (SHORT["de"] + "\n\n" + SHORT["en"] + "\n").encode("utf-8"))
        PRESS = {
            "de": dict(rel="presse.html", doc="Presse – Luca Flat", desc="Pressematerial zu Luca Flat und der Universalfernbedienung.", title="Presse",
                       lead="Material zu Luca Flat und der Universalfernbedienung.", h1="Kurzbeschreibung", h2="Downloads", zip="Alles als ZIP-Datei",
                       icon="App-Icon", shots="Screenshots", widgets="Widgets", contact='Fragen oder weiteres Material? Schreib mir über die <a href="kontakt.html">Kontaktseite</a>.',
                       marks="Sony und Bravia sind Marken der Sony Group Corporation, Android TV und Google TV Marken von Google LLC. Die App ist ein unabhängiges Projekt."),
            "en": dict(rel="en/press.html", doc="Press – Luca Flat", desc="Press material about Luca Flat and the Universal Remote.", title="Press",
                       lead="Material about Luca Flat and the Universal Remote.", h1="Short description", h2="Downloads", zip="Everything as a ZIP file",
                       icon="App icon", shots="Screenshots", widgets="Widgets", contact='Questions or more material? Write to me via the <a href="contact.html">contact page</a>.',
                       marks="Sony and Bravia are trademarks of Sony Group Corporation; Android TV and Google TV are trademarks of Google LLC. The app is an independent project."),
        }
        for lang, p in PRESS.items():
            A = "" if lang == "de" else "../"; i = 0 if lang == "de" else 1
            li = lambda f, label: f'<li><a href="{A}assets/{f}" download>{esc(label)}</a></li>'
            shots = "".join(li(f"screens/{s[0]}.jpg", s[2 + i][0]) for s in SCREENS)
            widgets = "".join(li(f"screens/{w[0]}.png", w[4 + i][0] if False else w[4 + i][0]) for w in WIDGETS)
            body = (f'<h2>{p["h1"]}</h2>\n<p>{esc(SHORT[lang])}</p>\n<h2>{p["h2"]}</h2>\n'
                    f'<p><a class="btn" href="{A}assets/presse/universalfernbedienung-presse.zip" download>{p["zip"]}</a></p>\n'
                    f'<h3>{p["icon"]}</h3>\n<ul>{li("app-icon-192.png", p["icon"] + " (192 × 192)")}</ul>\n'
                    f'<h3>{p["shots"]}</h3>\n<ul>{shots}</ul>\n<h3>{p["widgets"]}</h3>\n<ul>{widgets}</ul>\n'
                    f'<p class="note">{p["marks"]}</p>\n<p>{p["contact"]}</p>')
            pages.append((p["rel"], "", p["doc"], p["desc"], page_head("", [], p["title"], p["lead"], "") + "\n" + prose(body), A))


    # ------------------------------------------------------------- Englische Standardseiten
    en_status = badge("en")
    pages.append(("en/index.html", "", "Luca Flat – Android apps", "Luca Flat develops Android apps for everyday life.",
                  f"""    <section class="hero" aria-labelledby="hero-title">
      <div class="container hero__content">
        <div class="hero__text">
          <a class="hero__badge intro" href="apps/{APP}/index.html"><span class="dot" aria-hidden="true"></span>New: Universal Remote →</a>
          <h1 id="hero-title" class="intro"><span class="grad">Luca Flat</span></h1>
          <p class="lead intro">Android apps for everyday life.</p>
          <div class="hero__cta intro">
            <a class="btn" href="apps.html">See my apps</a>
            <a class="btn btn--ghost" href="about.html">About me</a>
          </div>
        </div>
        <a class="hero__shot" href="apps/{APP}/index.html" aria-label="View the Universal Remote"><figure class="phone"><img src="../assets/screens/fernbedienung.webp" width="540" height="1078" alt="Universal Remote: main screen with D-pad, volume and channels" decoding="async"></figure></a>
      </div>
    </section>""", "../"))
    pages.append(("en/apps.html", "apps", "Apps – Luca Flat", "All apps by Luca Flat.",
                  page_head("", [], "Apps", "My apps are released as standalone Android apps on Google Play.") + f"""
    <section class="section" style="padding-top:1rem;">
      <div class="container">
        <div class="grid grid--3">
          <article class="card card--app reveal">
            <div class="card__head">
              <img class="card__appicon" src="../assets/app-icon-192.png" width="56" height="56" alt="" loading="lazy" decoding="async">
              <div><h3>Universal Remote</h3>{en_status}</div>
            </div>
            <p>Your phone as a remote control for your TV.</p>
            <a class="btn btn--ghost card__btn" href="apps/{APP}/index.html">View details</a>
          </article>
          <article class="card card--soon reveal" data-delay="1">
            <div class="card__icon card__icon--muted" aria-hidden="true"></div>
            <h3>More apps to come</h3>
            <p>New projects will appear here as soon as they are ready.</p>
          </article>
        </div>
      </div>
    </section>""", "../"))
    pages.append(("en/about.html", "ueber-mich", "About me – Luca Flat", "About Luca Flat and his apps.",
                  page_head("", [], "About me", "") + f"""
    <section class="section" style="padding-top:1rem;">
      <div class="container about">
        <div class="reveal">
          <div class="avatar" role="img" aria-label="LCT – monogram of Luca Flat">
            <div class="avatar__ring"></div>
            {ctx["AVATAR_SVG"]}
          </div>
        </div>
        <div>
          <h2 class="reveal">Hi, my name is Luca</h2>
          <p class="reveal">In my free time I enjoy building apps that make everyday life easier. It makes me happy to see how a simple idea turns into a fully working Android app.</p>
          <p class="reveal">I care a lot about simple operation and software that makes life more practical.</p>
          <p class="reveal">On this website I present my first app and all future projects.</p>
          <p class="reveal"><a class="btn" href="apps.html">See my apps</a></p>
        </div>
      </div>
    </section>""", "../"))
    pages.append(("en/faq.html", "fragen", "FAQ – Luca Flat", "Frequently asked questions about the apps by Luca Flat.",
                  page_head("", [], "Frequently asked questions", "") + """
    <section class="section" style="padding-top:1rem;">
      <div class="container prose">
        <div class="faq">
          <details id="kosten"><summary>Do the apps cost anything?</summary><div class="faq__body">No. All apps are free and contain no ads.</div></details>
          <details id="daten"><summary>Do you collect my data?</summary><div class="faq__body">What exactly is stored is explained in the privacy policies of the <a href="../legal/datenschutz-app.html" hreflang="de" lang="de">app</a> and the <a href="../legal/datenschutz.html" hreflang="de" lang="de">website</a> (both in German).</div></details>
          <details id="fehler"><summary>How do I report a bug or ask for a feature?</summary><div class="faq__body">Write to me via the <a href="contact.html">contact page</a>.</div></details>
          <details id="geraete"><summary>Which devices do the apps run on?</summary><div class="faq__body">On Android phones and tablets running Android 8 or later. The apps are released on Google Play. For the Universal Remote you also need a TV on the same Wi-Fi: a Sony Bravia or a device with Android TV or Google TV.</div></details>
          <details id="hilfe"><summary>Where can I find help for the app?</summary><div class="faq__body">The <a href="apps/universalfernbedienung/help.html">app help</a> covers connecting to your TV, widgets, touch lock and the error log.</div></details>
        </div>
      </div>
    </section>""", "../"))
    pages.append(("en/contact.html", "kontakt", "Contact – Luca Flat", "Contact Luca Flat.",
                  page_head("", [], "Contact", "Questions, feedback or an idea for the next app? I would be happy to hear from you.") + f"""
    <section class="section" style="padding-top:1rem;">
      <div class="container prose">
        <form class="form" id="contactForm" data-mailto="{esc(cfg.OWNER_EMAIL)}" novalidate>
          <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-mail">Email</label><input id="f-mail" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" required></textarea></div>
          <div><button class="btn" type="submit">Prepare message</button></div>
          <p class="note" id="formStatus" role="status" aria-live="polite">The form does not send anything to a server. It opens your email app.</p>
        </form>
      </div>
    </section>""", "../"))
    return pages
