"""Übernimmt die Datenschutzerklärung 1:1 aus der App.

Aufruf:  python3 sync_app_datenschutz.py <Pfad zur index.html der App>
Danach:  python3 build_pages.py

Liest das Array LEGAL_PRIVACY aus der index.html der App und schreibt es nach
content/app-datenschutz-quelle.html. So stehen in App und Website immer
derselbe Text und dieselbe Gliederung (Stand – Inhalt – Abschnitte 1 bis n)."""
import re, sys
from pathlib import Path

src = Path(sys.argv[1] if len(sys.argv) > 1 else "../app/src/main/assets/index.html").read_text(encoding="utf-8")
a = src.index("const LEGAL_PRIVACY = [")
b = src.index("].join('');", a)
parts = re.findall(r"'((?:[^'\\\\]|\\\\.)*)'", src[a:b])
text = "".join(p.replace("\\\\'", "'").replace("\\\\\\\\", "\\\\") for p in parts)
out = Path(__file__).parent / "content" / "app-datenschutz-quelle.html"
out.write_text(text, encoding="utf-8")
print(f"übernommen: {len(parts)} Teile, {len(text)} Zeichen → {out}")
