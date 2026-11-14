# LCT – Website

Statische Website ohne externe Dienste, ohne Cookies und ohne Tracking. Schriften liegen lokal.

## Struktur
- `build_pages.py` erzeugt ALLE Seiten aus einer Vorlage. Nach jeder Änderung: `python3 build_pages.py`
- `site_config.py` enthält deine Angaben (Name, Anschrift, E-Mail, Website-Adresse, Paketname, Veröffentlichungsstatus)
- `legal_texts.py` enthält Datenschutzerklärung der Website und Impressum, `content/app-datenschutz-quelle.html` den Text der App-Datenschutzerklärung
- **App-Datenschutz immer gleich wie in der App:** Nach jeder Änderung des Datenschutztextes in der App `python3 sync_app_datenschutz.py <Pfad zur index.html der App>` und danach `python3 build_pages.py` ausführen. Der Text wird 1:1 übernommen; nur die Platzhalter (Verantwortlicher, Aufsichtsbehörde, Adresse) füllt die Website aus `site_config.py`. Aufbau wie in der App: Stand – Inhalt – Abschnitte.
- `css/`, `js/`, `assets/` – Design, Skript, Bilder, Schriften, Video

## Noch auszufüllen (site_config.py)
1. `OWNER_NAME`, `OWNER_STREET`, `OWNER_CITY`, `OWNER_EMAIL` – erscheinen in Impressum, beiden Datenschutzerklärungen und im Kontaktformular. Solange etwas fehlt, zeigen die Seiten einen sichtbaren Platzhalter.
2. `SITE_URL` – die spätere öffentliche Adresse, z. B. `https://benutzername.github.io/lucaflat` (ohne Schrägstrich am Ende).
3. `PLAY_PACKAGE` – Paketname der App. Er lässt sich nach der Veröffentlichung nie mehr ändern.
4. `APP_PUBLISHED = True` – erst setzen, wenn die App im Play Store wirklich online ist. Dann erscheint der Link „Bei Google Play ansehen“.

## Video der Streaming-Suche
Datei als `assets/video/streaming-suche.mp4` ablegen und `python3 build_pages.py` ausführen. Das Video erscheint dann im Abschnitt „Screenshots“. Es liegt auf der Website selbst und wird erst nach einem Klick auf Play geladen. Ohne Datei erscheint kein Abschnitt.

Verkleinern (ffmpeg, Ziel unter 10 MB, ohne Ton, läuft in jedem Browser):

    ffmpeg -i aufnahme.mp4 -vf "scale=-2:960" -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -an -movflags +faststart streaming-suche.mp4

## Lokal testen
Im Ordner `python3 -m http.server 8080` starten und `http://localhost:8080` öffnen.

## Auf der Synology (Web Station)
1. Paketzentrum: **Web Station** installieren.
2. Den Ordner `lucaflat-site` in den freigegebenen Ordner `web` kopieren.
3. Aufrufen unter `http://<NAS-IP>/lucaflat-site/`.

## Auf GitHub Pages
1. Neues Repository anlegen (bei einem kostenlosen Konto muss es öffentlich sein) und den Inhalt dieses Ordners hochladen, einschließlich der Datei `.nojekyll`.
2. Einstellungen → Pages → Branch `main`, Ordner `/ (root)`.
3. Die Seite erscheint unter `https://<benutzername>.github.io/<repository>/`. Diese Adresse in `SITE_URL` eintragen und neu bauen.
4. In den Pages-Einstellungen „Enforce HTTPS“ aktivieren.
5. Für den Play Store: Die Adresse `<SITE_URL>/legal/datenschutz-app.html` in der Play Console als Datenschutzerklärung der App eintragen.

## Schriften
Inter und Space Grotesk liegen lokal unter `assets/fonts/` (SIL Open Font License, Lizenztexte liegen dabei). Es werden keine Schriften von Fremdservern geladen.

## Kontaktformular (nur GitHub, ohne Server)

GitHub Pages kann keine E-Mails versenden. Das Formular füllt deshalb eine E-Mail an `OWNER_EMAIL` komplett vor
(Thema, Name, Nachricht) und öffnet das E-Mail-Programm des Besuchers – er tippt nur noch auf „Senden“. Die Nachricht
kommt von seiner eigenen Adresse; du antwortest ganz normal. Kein Server, kein Fremddienst, keine Kosten, keine Cookies.
Ohne E-Mail-Programm (z. B. am PC) zeigt die Seite die Adresse mit einem Knopf zum Kopieren.
