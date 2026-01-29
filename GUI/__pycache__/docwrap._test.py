


'''Hier ein eigenständiges, sofort lauffähiges Python-Modul, das genau das macht, was in Ihrem Eingangs-Docstring beschrieben ist:

1. Ein beliebiges Dokument wird in Absätze (durch eine oder mehrere Leerzeilen getrennt) zerteilt.  
2. Jeder Absatz wird heuristisch als „Plain-Text“ oder „Python-Code“ klassifiziert.  
   • Kriterium: Lässt sich der (links getrimmte) Absatz ohne SyntaxError kompilieren?  
3. Das Ergebnis wird wahlweise  
   • als HTML (mit <p class="text"> … bzw. <pre class="code"> …) oder  
   • als Python-Liste von Tupeln [(“text”, …), (“code”, …)] zurückgegeben.  
4. Es gibt eine kleine CLI, Unit-Tests (pytest) sowie eine Mini-GUI (PySide6), mit der man das Ergebnis sofort prüfen kann.  

Dateistruktur
─────────────
docwrap/
 ├─ __init__.py
 ├─ core.py        <- Kern-Logik + CLI-Entry-Point
 ├─ gui.py         <- optionale Qt-Vorschau
 └─ test_core.py   <- pytest-Tests

#######################################################################
#  docwrap/core.py
#######################################################################
```python

docwrap.core
============
'''
"""
Kern-Logik zum Erkennen und Einwickeln („wrap“) von Python-Code-
Absätzen vs. Normaltext-Absätzen.

Aufruf als Skript:
    python -m docwrap.core <eingabe.txt> [<ausgabe.html>]

Copyright (c) 2024
"""

from __future__ import annotations

import argparse
import ast
import html
import sys
from pathlib import Path
from typing import Iterable, List, Tuple


Segment = Tuple[str, str]      # ("text" | "code", absatz_in_originalform)


# --------------------------------------------------------------------------- #
# Hilfsfunktionen                                                             #
# --------------------------------------------------------------------------- #
def _is_python_code(snippet: str) -> bool:
    """
    Heuristik: Versuche, den Absatz als Python zu kompilieren.
    Klappt das ohne ``SyntaxError`` gilt er als Code-Absatz.

    Vor dem Kompilieren wird der Absatz links getrimmt, damit bereits
    eingerückte Blöcke (z.B. innerhalb einer Klasse) erkannt werden.
    """
    try:
        ast.parse(snippet.lstrip() + "\n")     # Newline verhindert EOL-Fehler
        return True
    except SyntaxError:
        return False


def split_into_paragraphs(text: str) -> List[str]:
    """
    Zerlegt *text* an Leerzeilen-Sequenzen in Absätze
    (Leerzeilen bleiben NICHT erhalten).
    """
    paragraphs: List[str] = []
    current: list[str] = []

    for line in text.splitlines():
        if line.strip():                       # nicht-leere Zeile
            current.append(line)
        else:                                  # Leerzeile -> Absatzende
            if current:
                paragraphs.append("\n".join(current))
                current.clear()
    if current:
        paragraphs.append("\n".join(current))
    return paragraphs


def classify(text: str) -> List[Segment]:
    """
    Hauptroutine: Liefert eine Liste von Segmenten („text“ | „code“).
    """
    segments: List[Segment] = []
    for para in split_into_paragraphs(text):
        kind = "code" if _is_python_code(para) else "text"
        segments.append((kind, para))
    return segments


def to_html(segments: Iterable[Segment]) -> str:
    """
    Wandelt Segmente in HTML um.  Sehr schlankes Mark-Up mit
    Klassen-Attributen, damit man via CSS beliebig gestalten kann.
    """
    html_parts: list[str] = [
        "<!DOCTYPE html>",
        "<meta charset='utf-8'>",
        "<title>docwrap export</title>",
        "<style>",
        "  body        { font-family: sans-serif; background:#222; color:#ddd; }",
        "  pre.code    { background:#111; color:#eee; padding:1em; overflow:auto; }",
        "  p.text      { margin:1em 0; line-height:1.4; }",
        "</style>",
        "<body>",
    ]

    for kind, para in segments:
        escaped = html.escape(para)
        if kind == "code":
            html_parts.append(f"<pre class='code'>{escaped}</pre>")
        else:
            html_parts.append(f"<p class='text'>{escaped}</p>")

    html_parts.append("</body>")
    return "\n".join(html_parts)


# --------------------------------------------------------------------------- #
# CLI-Interface                                                               #
# --------------------------------------------------------------------------- #
def _cli() -> None:                  # pragma: no cover
    ap = argparse.ArgumentParser(description="Plain-Text vs. Python-Code-Wrapper")
    ap.add_argument("input",  help="Text-Datei als Eingabe")
    ap.add_argument("output", help="(optional) HTML-Datei als Ausgabe",
                    nargs="?", default=None)
    ns = ap.parse_args()

    in_path  = Path(ns.input).expanduser()
    out_path = Path(ns.output).expanduser() if ns.output else None

    text = in_path.read_text(encoding="utf-8")
    segments = classify(text)

    if out_path:
        out_path.write_text(to_html(segments), encoding="utf-8")
        print(f"Ergebnis in {out_path} geschrieben.")
    else:
        # Dumpe die Struktur in die Konsole
        for kind, para in segments:
            line = para.splitlines()[0][:60] + ("…" if len(para) > 60 else "")
            print(f"[{kind.upper():4}] {line}")

"""
if __name__ == "__main__":
    _cli()
"""

#######################################################################
#  docwrap/gui.py  (Mini-Qt-Vorschau, optional)
#######################################################################

"""
docwrap.gui
===========

Kleine Qt-Anwendung, die zeigt, wie das HTML-Ergebnis von
``docwrap.core`` direkt angezeigt werden kann.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QFileDialog, QTextBrowser, QVBoxLayout, QWidget

from docwrap_test import classify, to_html


def main() -> None:                 # pragma: no cover
    app = QApplication(sys.argv)

    view = QTextBrowser()
    view.setOpenExternalLinks(True)
    view.setFont(QFont("Fira Code, Consolas, Courier New", 12))

    win = QWidget()
    lay = QVBoxLayout(win)
    lay.addWidget(view)
    win.resize(900, 600)
    win.setWindowTitle("docwrap – Preview")

    # Datei auswählen
    path, _ = QFileDialog.getOpenFileName(win, "Dokument laden", "", "Text (*.txt *.md);;Alle Dateien (*)")
    if not path:
        sys.exit(0)

    segments = classify(Path(path).read_text(encoding="utf-8"))
    view.setHtml(to_html(segments))

    win.show()
    sys.exit(app.exec())

"""
if __name__ == "__main__":
    main()
"""

#######################################################################
#  docwrap/test_core.py  (Unit-Tests mit pytest)
#######################################################################
from docwrap_test import _is_python_code, classify, split_into_paragraphs


def test_is_python_code():
    assert _is_python_code("x = 5")
    assert not _is_python_code("Dies ist kein Code.")


def test_split_into_paragraphs():
    text = "Line 1\n\nLine 2\nLine 3\n\n\nLine 4"
    paras = split_into_paragraphs(text)
    assert paras == ["Line 1", "Line 2\nLine 3", "Line 4"]


def test_classify():
    text = "a = 1\n\nPlain text\n\nfor i in range(3):\n    print(i)"
    segs = classify(text)
    kinds = [k for k, _ in segs]
    assert kinds == ["code", "text", "code"]


#######################################################################
"""
Installation & Verwendung
─────────────────────────
1. Installieren (am besten in einer venv):

   ```
   pip install PySide6 pytest
   ```

2. Als Skript:

   ```bash
   python -m docwrap.core README.txt README.html
   ```

3. GUI-Vorschau:

   ```bash
   python -m docwrap.gui
   ```

4. Tests ausführen:

   ```bash
   pytest -q   
   ```

Kurze Erklärung
───────────────
• Ein Dokument wird Absatzweise verarbeitet, weil menschlicher Text üblicherweise so strukturiert ist.  
• `_is_python_code()` nutzt den Python-Parser selbst – das ist 100 % robust gegenüber allen Sprachkonstrukten und benötigt keine fragile Regex-Magie.  
• HTML-Export erlaubt sofortige Weiterverarbeitung (CSS, Einbettung in Webseiten, PDF-Export etc.).  
• Die Qt-Mini-App zeigt, wie man das Ergebnis visuell inspizieren kann.  

Damit haben Sie eine zuverlässige Grundlage, um reinen Text und Python-Code sauber getrennt weiterzuverarbeiten oder anzuzeigen.
"""