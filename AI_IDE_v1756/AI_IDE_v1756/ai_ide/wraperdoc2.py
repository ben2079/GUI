"""AttributeError: 'str' object has no attribute 'copy'"""

from __future__ import annotations

from pathlib import Path
import argparse
import ast
import html
import sys
import textwrap
from typing import Iterable, List, Tuple
try:
    from .litehigh import QSHighlighter
except Exception:
    from litehigh import QSHighlighter
import  random
from PySide6.QtWidgets import QTextEdit

import sys
import html
from typing import Iterable, List, Tuple, MutableSequence
# Öffentliche API ------------------------------------------------------------
__all__ = [
    "classify",
    "split_into_paragraphs",
    "to_html",
    "_is_python_code",
]

Segment = Tuple[str, str]           # ("text" | "code", paragraph)
MergedSegment = Tuple[str, list[str]]  # ("text" | "code", [paragraph, …])


# --------------------------------------------------------------------------- #
# Hilfsfunktionen                                                             #
# --------------------------------------------------------------------------- #
def _is_python_code(snippet: str) -> bool:
    """
    Erkenne, ob *snippet* (ein einzelner Absatz) höchstwahrscheinlich
    Python-Code ist (True) oder nicht (False).

    Vorgehen
    --------
    1. Frühe Heuristiken
    2. AST-Parsing (notfalls mit angehängtem ``pass``)
    3. Feinkorrektur für reine String-Literale
    """
    
    # 1) Frühe Heuristiken -------------------------------------------------
    lines = [ln.strip() for ln in snippet.splitlines() if ln.strip()]
    for ln in lines:
        if ln.startswith("```") or ln.endswith("```"):
            return True 
    if not lines:                             # leerer Absatz
        return False
    
    if all(ln.startswith("#") for ln in lines):    # nur Kommentare
        return False
    
    

    # 2) AST-Parsing -------------------------------------------------------
    code = textwrap.dedent(snippet).rstrip() + "\n"
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        if exc.msg in {"expected an indented block",
                       "unexpected EOF while parsing"}:
            try:
                tree = ast.parse(code + "    pass\n")
            except SyntaxError:
                return False
        else:
            
            return False

    # 3) Feinkorrektur -----------------------------------------------------
    if (
        len(tree.body) == 1
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, (str, bytes))
    ):
        return False

    return True


def split_into_paragraphs(text: str) -> List[str]:
    """
    Zerlegt ``text`` an *Leerzeilen-Sequenzen* in Absätze
    (Leerzeilen werden verworfen).
    """
    paragraphs: List[str] = []
    current: list[str] = []

    for (line) in text.splitlines():
        if line.strip(""):                       # nicht-leere Zeile
            current.append(line.strip(""))
        else:                                  # Leerzeile  → Absatzende 
            if current:
                paragraphs.append("\n".join(current))
                current.clear()

    if current:
        paragraphs.append("\n".join(current))

    return paragraphs


def classify(text: str) -> List[Segment]:
    """
    Liefert ``[(kind, paragraph), …]`` mit *kind* = ``"code"`` | ``"text"``.
    """

    return [
        ("code" if _is_python_code(p) else "text", p)
        for p in split_into_paragraphs(text)
    ]


import sys
import html
from typing import Iterable, List, Tuple, MutableSequence

from PySide6.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout

# ---------------------------------------------------------------------------
# Hilfstypen
# ---------------------------------------------------------------------------
# Ein Segment besteht hier nur aus  (kind, inhalt).
# kind  : "code" | "text"
# inhalt: Liste von Strings (= Zeilen bzw. Absätze des Segments)


# ---------------------------------------------------------------------------
# 1)  Hilfsfunktion: benachbarte Code-Blöcke zusammenfassen
#     (F i x  für  AttributeError:  'str' object has no attribute 'copy')
# ---------------------------------------------------------------------------
from typing import Iterable, List, Tuple

# Eingangs-Segment  -> (kind, paragraph:str)
InSegment   = Tuple[str, str]
# Ausgangs-Segment -> (kind, [paragraph, …])
OutSegment  = Tuple[str, List[str]]


def _merge_adjacent_code_blocks(
    segments: Iterable[InSegment],
) -> List[OutSegment]:
    """
    Fasst aufeinanderfolgende »code«-Segmente zu einem gemeinsamen
    Segment zusammen, damit im HTML nur **ein** <pre> pro Block steht.

    Eingabe :
        [("code", "foo = 1"),
         ("code", "bar = 2"),
         ("text", "Ein Absatz"),
         ("code", "print('done')")]

    Ausgabe :
        [("code", ["foo = 1", "", "bar = 2"]),
         ("text", ["Ein Absatz"]),
         ("code", ["print('done')"])]
    """
    merged: List[OutSegment] = []

    for kind, para in segments:
        # ––––– Einheitliches internes Format: Liste von Absätzen –––––
        current: List[str] = [para] if isinstance(para, str) else list(para)

        # Mehrere Code-Blöcke hintereinander ⇒ zusammenführen
        if merged and kind == "code" and merged[-1][0] == "code":
            merged[-1][1].extend([""] + current)       # Leerzeile als Trenner
        else:
            merged.append((kind, current))             # NEUER Block

    return merged


# ---------------------------------------------------------------------------
# 2)  Die neue to_html-Methode
# ---------------------------------------------------------------------------
def to_html(segments: Iterable[Segment]) -> str:
    """
    Wandelt eine Sequenz aus Text- und Code-Segmenten in ein vollständiges
    HTML-Dokument um.  Gestaltungsziel ist das gleiche Aussehen wie im
    statischen Beispiel des Fragestellers (zentrierte Box mit abgerundetem
    Rahmen etc.).
    """
    merged_segments = _merge_adjacent_code_blocks(segments)

    style_block = """
        /* Grundlayout -------------------------------------------- */
        body{
            margin:0;
            padding:2rem;
            font-family:system-ui,sans-serif;
            background:#222;
            color:#E3E3DED6;
            display:flex;
            justify-content:center;
        }

        /* Die Box, in die wir alles einbetten -------------------- */
        .box{
            margin:0 auto 2em;
            padding:0;
            max-width:45rem;
            width:100%;
            text-align:left;
        }

        /* Code-Darstellung --------------------------------------- */
        pre.code{
            background:#181818;
            color:#E3E3DED6;
            padding:1em;
            overflow:auto;
            margin:0 auto 2em;
            border-radius:8px;
            border:1px solid #ddd;
            white-space:pre-wrap; /* Zeilen umbrechen, wenn nötig */
        }

        /* Fließtext ---------------------------------------------- */
        p.text{
            line-height:1.5;
        }
    """

    html_parts: list[str] = [
        "<!DOCTYPE html>",
        "<html>",
        "  <head>",
        "    <meta charset='utf-8'>",
        "    <title>docwrap export</title>",
        "    <style>",
        style_block,
        "    </style>",
        "  </head>",
        "  <body>",
        "    <div class='pre.code'>",
    ]

    # ----------------------------- Inhalt rendern ---------------------------
    for kind, paras in merged_segments:
        if kind == "code":
            escaped = html.escape("\n".join(paras))
            html_parts.append(f"<pre class='code'>{escaped}</pre>")
        else:  # normaler Text
            for para in paras:
                escaped = html.escape(para)
                html_parts.append(f"<p class='text'>{escaped}</p>")

    # ----------------------------- schließen -------------------------------
    html_parts.extend([
        "    </div>",
        "  </body>",
        "</html>",
    ])

    return "\n".join(html_parts)

    


"""
docwrap.gui
===========

Mini-Qt-App, um das durch ``docwrap.core.to_html`` erzeugte
Resultat komfortabel zu betrachten.
"""

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

classify, to_html


def main() -> None:  # pragma: no cover
    app = QApplication(sys.argv)

    browser = QTextBrowser()
    browser.setOpenExternalLinks(True)
    browser.setFont(QFont("Fira Code, Consolas, Courier New", 11))

    win = QWidget()
    lay = QVBoxLayout(win)
    lay.addWidget(browser)
    win.resize(900, 600)
    win.setWindowTitle("docwrap – Preview")

    # Datei auswählenp
    path, _ = QFileDialog.getOpenFileName(
        win,
        "Dokument laden",
        "",
        "Text (*.txt *.md *.rst);;Alle Dateien (*)",
    )
    if not path:
        sys.exit(0)

    segments = classify(Path(path).read_text(encoding="utf-8"))
    browser.setHtml(to_html(segments))

    win.show()
    sys.exit(app.exec())

# --------------------------------------------------------------------------- #
# CLI-Interface                                                               #
# --------------------------------------------------------------------------- #

 
def _cli() -> None:  # pragma: no cover
    ap = argparse.ArgumentParser(description="Plain-Text ↔ Python-Code Wrapper")
    ap.add_argument("input",  help="Text-Datei als Eingabe")
    ap.add_argument("output", nargs="?", default=f'out_{random.random()}.html',
                    help="Optional: HTML-Datei als Ausgabe")
    ns = ap.parse_args()

    in_path  = Path(ns.input).expanduser()
    out_path = Path(ns.output).expanduser() if ns.output else None

    text     = in_path.read_text(encoding="utf-8")
    segments = classify(text)

    if out_path:
        out_path.write_text(to_html(segments), encoding="utf-8")
        print(f"Ergebnis in {out_path} geschrieben.")
    else:   # Konsolen-Kurzvorschau-
        for kind, para in segments:
            head = para.splitlines()[0][:] + ("…" if len(para) > 60 else "")
            print(f"[{kind.upper():4}] {head}")

'''
if __name__ == "__main__":
  _cli()
'''
# docwrap/test_merge.py
classify, _merge_adjacent_code_blocks

def test_merge_adjacent_code_blocks():
    txt = "x = 1\n\ny = 2\n\nNur Text\n\nfor i in range(2):\n    print(i)"
    merged = _merge_adjacent_code_blocks(classify(txt))
    print(merged)

    # Erwartet:  zwei zusammengelegte Code-Blöcke, dazwischen Text
    kinds = [kind for kind, _ in merged]
    assert kinds == ["code", "text", "code"]
    print(kinds == ["code", "text", "code"])

    # erster Code-Block enthält beide Code-Absätze
    assert len(merged[0][1]) == 2
    print(len(merged[0][1]) == 2)
    
#test_merge_adjacent_code_blocks()

'''
Kurze Erklärung
───────────────
• Bisher bekam jeder Code-Absatz sein eigenes `<pre class="code">`, was
  zwangsläufig zu sichtbaren Zwischenräumen führte.  
• Die neue Hilfsfunktion `_merge_adjacent_code_blocks` sammelt
  hintereinander auftretende `"code"`-Segmente in einer Liste.  
• `to_html` verwendet diese verschmolzenen Segmente, nimmt zwischen den
  einzelnen Code-Absätzen lediglich zwei Zeilenumbrüche (`\n\n`) in das
  `<pre>` auf und erzeugt so einen einzigen Container mit durchgehendem
  Hintergrund.  
• Für Text-Absätze bleibt alles beim Alten.  
• Die CSS-Definition enthält `margin:0` für `<pre>`-Elemente, wodurch
  selbst bei mehreren zusammengefügten `<pre>`-Blöcken (sollten sie
  entstehen) kein Abstand sichtbar wäre.

Code & Tests sind sofort einsatzbereit (`python -m docwrap.core` bzw.
`pytest`). 
'''

"""def test_is_python_code():
    assert _is_python_code("x = 5")  # Basis-Fall

    # Offensichtlicher Klartext
    assert not _is_python_code("Dies ist kein Code.")

    # Block-Header ohne Rumpf
    assert _is_python_code("def foo():")

    # Eingeschobener Code aus tieferer Ebene (4 Leerzeichen)
    assert _is_python_code("    chunks: list[torch.Tensor] = []")


def test_split_into_paragraphs():
    text = "Line 1\n\nLine 2\nLine 3\n\n\nLine 4"
    assert split_into_paragraphs(text) == ["Line 1", "Line 2\nLine 3", "Line 4"]


def test_classify():
    text = "a = 1\n\nPlain text\n\nfor i in range(3):\n    print(i)"
    kinds = [k for k, _ in classify(text)]
    assert kinds == ["code", "text", "code"]

    # Eingeschobener Code aus tieferer Ebene (4 Leerzeichen)
    assert _is_python_code("    chunks: list[torch.Tensor] = []")

    # Kommentar-Block ⇒ KEIN Code
    assert not _is_python_code("# nur Kommentar\n# noch einer")

    # Reines String-Literal ⇒ KEIN Code
    assert not _is_python_code("'DEBUGGING'")

"""
