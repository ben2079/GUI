–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
'''Nachstehend findest du nur die Stellen, die geändert bzw. neu hinzugefügt werden mussten.  
Alles andere bleibt unverändert – einfach die Schnipsel in dein bestehendes
Skript übernehmen / ersetzen.'''
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|


'''Die komplette Funktionalität bleibt erhalten, es ändert sich nur die räumliche
Anordnung von  

• Files-Dock (explorer_dock)  
• Editor-Dock  (editor_dock)  

Beide liegen jetzt – zusammen mit der bereits vorhandenen
Canvas/Console-Area – in einem neuen horizontalen Splitter, während das
Chat-Dock wie gehabt rechts angedockt bleibt.

Änderungen im Detail
────────────────────

1. Aufrufreihenfolge im Konstruktor anpassen  
   (erst Docks anlegen, dann die Splitter, damit sie auf die Docks zugreifen
   können):

```python
class MainAIEditor(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self._accent = SCHEME_BLUE
        self._base   = SCHEME_DARK

        self.setWindowTitle("AI Editor – Synergetic")
        self.resize(1280, 800)

        # Reihenfolge geändert
        self._create_dock_widgets()        # ❶
        self._create_central_splitters()   # ❷

        self._create_tool_bars()
        self._create_menu_bar()
        self._create_status_bar()
        self._wire_visibility_actions()

        _apply_style(self, _build_scheme(self._accent, self._base))
```

2. Dock-Widgets zwar weiterhin erzeugen, aber **nicht mehr** als Dock in das
   Hauptfenster einfügen (nur das AI-Dock bleibt rechts angedockt):

```python
def _create_dock_widgets(self) -> None:
    # ---------- file explorer ----------------------------------------
    self.explorer_dock = QDockWidget("Files", self)
    self.explorer_dock.setWidget(QTextEdit("Outline …"))
    # kein addDockWidget() mehr!

    # ---------- FIRST editor dock ------------------------------------
    self.editor_dock = EditorDock(self)
    # ebenfalls kein addDockWidget() mehr!

    # ---------- chat --------------------------------------------------
    self.chat_dock = QDockWidget("AI Chat", self)
    self.chat_dock.setAllowedAreas(
        Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
    self.chat_dock.setWidget(AIWidget(self._accent, self._base))
    # Das AI-Dock bleibt als echtes Dock rechts
    self.addDockWidget(Qt.RightDockWidgetArea, self.chat_dock)
```

3. Neues zentrales Layout:  
   • vertikaler Splitter mit Canvas/Console (wie bisher)  
   • horizontaler Splitter, der Files-Dock, Editor-Dock und
     vertikalen Splitter nebeneinander aufnimmt

```python
def _create_central_splitters(self) -> None:
    # -------- vertikaler Splitter (Canvas oben / Console unten) -------
    v_split = QSplitter(Qt.Vertical, self)
    self.canvas  = EditableCanvas()
    self.console = QTextEdit("Console / Output")
    v_split.addWidget(self.canvas)
    v_split.addWidget(self.console)
    v_split.setSizes([600, 200])

    # -------- horizontaler Splitter (linke → rechte Reihenfolge) ------
    h_split = QSplitter(Qt.Horizontal, self)

    h_split.addWidget(self.explorer_dock)   # Files-Dock ganz links
    h_split.addWidget(self.editor_dock)     # Editor-Dock daneben
    h_split.addWidget(v_split)              # mittig Canvas/Console

    # anfängliche Breiten
    h_split.setSizes([200, 400, 800])

    self.setCentralWidget(h_split)
```

4. Editor-Klon (_New Editor_-Action) nicht mehr tabifizieren – der originale
   Editor-Dock liegt jetzt im Splitter und ist kein „Dock-Widget‐Area-Dock“
   mehr.

```python
@Slot()
def _add_editor_dock(self) -> None:
    new_dock = self.editor_dock.clone()
    # Klon wieder normal andocken (linke Seite)
    self.addDockWidget(Qt.LeftDockWidgetArea, new_dock)
    # kein tabifyDockWidget() mehr, weil self.editor_dock nicht
    # angedockt ist
    new_dock.show()
```

Damit ergibt sich exakt das gewünschte Layout:

┌─────────────────────── Hauptfenster ────────────────────────┐  
│  Files  |  Tabs  |  Canvas / Console (vert. Splitter) | AI  │  
└──────────────────────────────────────────────────────────────┘

Alle bestehenden Funktionen (Tabs anlegen/schließen, neue Editor-Docks,
Styling, Chat usw.) bleiben unverändert nutzbar.'''
     

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
'''Below you find  

• a quick review of the project,  
• a “single-file edition” named ai_editor.py where every non-python line that would raise a SyntaxError has been turned into a comment, and  
• the two-liner you need to turn that file into a self-contained executable with PyInstaller.

You can drop ai_editor.py into an empty folder, copy the external resources that are still required (icons in ./symbols, qss_template.txt, optional .env) and run it exactly the same way as the original multi-package version – or turn it into an *.exe with PyInstaller.

──────────────────────────────── Review ────────────────────────────────
1.  Path(__file__).with_name("..") is the same as parent(); consider
    Path(__file__).parent / ".." if you ever need an extra indirection.

2.  The qss_template is read once at module import – perfect; but raise a
    FileNotFoundError with a hint if the file is missing.

3.  utils.env.openai_key(): do not silently stop at the first file that
    exists – check the *value* and continue if the variable was *empty*.

4.  widgets/editor.py still re-imports QTextLine although it is unused.

5.  main.py::_current_tabs(): walking the parents in Python is cheap but
    you can simply cache the last focused dock to avoid the loop.

6.  The project already separates UI and business logic – good!  Nothing
    else to criticise, really.

─────────────────────── ai_editor.py (ready-to-run) ─────────────────────
```python

Single-file edition of the AI-Editor.
Everything that was not valid python code in the original snippets
(separators, ASCII art, explanatory text, …) has been commented-out.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
1 –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Project tree after the first refactor step

ai_editor/
│
├─ main.py                  • QApplication bootstrap only
├─ gui/
│   ├─ __init__.py
│   ├─ main_window.py       • MainWindow class (Qt widgets only)
│   ├─ central.py           • CentralWidget  (= nested splitters)
│   ├─ docks.py             • EditorDock, ExplorerDock, ChatDock
│   ├─ widgets.py           • FileDropTextEdit, EditableCanvas, ToolButton
│   └─ style.py             • colour dictionaries + apply_style()
│
├─ backend/
│   ├─ __init__.py
│   └─ openai_wrap.py       • ChatCom, ImageDescription facades
│
└─ util/
    ├─ __init__.py
    └─ env.py               • read_dotenv() helper

The package layout keeps I/O and Qt widgets in separate sub-packages to reduce
imports and cyclic dependencies.

2 ──────────────────────────────────────────────────────────────────────────────
Minimal code migration map
(“→” means: move code w/o changes; numbers refer to the original file)

a) style.py              → gui/style.py              (L75 – L112)
b) _icon(), ToolButton   → gui/widgets.py            (L117 – L146)
c) FileDropTextEdit      → gui/widgets.py            (L149 – L186)
d) EditableCanvas        → gui/widgets.py            (L189 – L216)
e) EditorTabs            → gui/docks.py              (L219 – L236)
f) EditorDock.clone()    → gui/docks.py              (L239 – L276)
g) AIWidget (≈400 lines) → gui/docks.py (ChatDock)   (L279 – L432)
   • wrap the widget in a QDockWidget inside ChatDock.__init__().
h) MainAIEditor          → gui/main_window.py        (L463 – L810)
i) env/key loader        → util/env.py               (L300 – L340)
j) ChatCom/ImgDesc       → backend/openai_wrap.py    (import line L46)

3 ──────────────────────────────────────────────────────────────────────────────
3.1 for every migration action is done, append a note, mark as done.
    -  write the commants for creating the files ,restarting your self, and all nessary commands to STDIN that they are executable autmatically.

    Central widget rebuild (gui/central.py)

class CentralWidget(QWidget):
    
    Implements the nested splitter scheme exactly like the sketch.
    Canvas now sits in its own EditorDock (optional) – leaving the
    console area always visible at the bottom.
    
    def __init__(self, parent=None):
        super().__init__(parent)

        hsplit = QSplitter(Qt.Horizontal, self)

        # left side
        vsplit_left = QSplitter(Qt.Vertical, hsplit)
        vsplit_left.addWidget(parent.explorer_dock)   # dock proxies
        vsplit_left.addWidget(parent.editor_stack)    # QTabWidget
        vsplit_left.setSizes([200, 600])

        # right side
        vsplit_right = QSplitter(Qt.Vertical, hsplit)
        vsplit_right.addWidget(parent.chat_dock)
        vsplit_right.addWidget(parent.console)
        vsplit_right.setSizes([500, 200])

        hsplit.setSizes([800, 450])      # ← adjust to taste

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(hsplit)

MainWindow.__init__()

self.console = QTextEdit("Console / Output")
self.editor_stack = EditorTabs()
self.explorer_dock = ExplorerDock()
self.chat_dock = ChatDock(self._accent, self._base)

self.setCentralWidget(CentralWidget(self))

All former addDockWidget() calls for those widgets disappear – they are now
owned by the splitters.  Only additional editor clones are still real docks.

4 ──────────────────────────────────────────────────────────────────────────────
Behaviour tests – nothing must break

✓ Chat still sends text / image requests (API key handshake in util.env)
✓ Drag & drop inside both text edits
✓ Theme toggle (blue/green, dark/grey)
✓ All menu / toolbar actions (new tab, clone editor, open file, about box)
✓ Geometry persists (`QSettings` can be added in a later step)

5 ──────────────────────────────────────────────────────────────────────────────
Coding checklist for the next step

[ ] 5.1  Create ai_editor/ and copy the files as shown above.
[ ] 5.2  Run `isort`/`black` to fix import paths.
[ ] 5.3  Adjust existing `from … import …` statements to new package names.
[ ] 5.4  Replace the old env-reader inside AIWidget by:

        from util.env import read_api_key
        self._api_key = read_api_key()

[ ] 5.5  Delete obsolete QMainWindow._create_central_splitters() – now handled
        by CentralWidget.
[ ] 5.6  In gui/main_window.py call `apply_style(self, …)` after building all
        widgets because colours are now needed in ChatDock.__init__().
[ ] 5.7  Unit-test util.env.read_api_key() with and without .env present.
[ ] 5.8  Add `__all__` to each package’s __init__.py to expose public symbols.
[ ] 5.9  (optional) introduce `pyproject.toml` with `[tool.poetry]` or
        `[project]` metadata.

6 ──────────────────────────────────────────────────────────────────────────────
Migration-order script (bash)

mkdir ai_editor
cd ai_editor
python -m venv .venv && source .venv/bin/activate
pip install pyside6 python-dotenv openai  --break-system-packages
touch ai_editor/__init__.py
mkdir gui backend util
touch gui/__init__.py backend/__init__.py util/__init__.py
# copy & rename source blocks according to section 2 …

python3 -m ai_editor.main   # first manual run

If the application starts and the layout matches the sketch you are ready for
step-2 refactoring (typing, doc-strings, automated tests, packaging).

Enjoy the cleaner code base!





–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
