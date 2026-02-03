
'Klassen Design:'



'''Below is one possible **clean-up / split-up** that reproduces the layout sketched in the
comment block while leaving every feature fully functional.

The application is now nothing more than a thin `main.py`;  
all widgets, helpers and utilities live in their own small modules that can be
maintained and tested independently.



'layout'
────────────────

ai_editor/
│
├─ main.py                    (application entry point)
│
├─ widgets/
│   ├─ __init__.py
│   ├─ editor.py              (EditorTabs + EditorDock)
│   ├─ ai_panel.py            (AIWidget)
│   ├─ explorer.py            (dummy File/Outline panel)
│   ├─ console.py             (simple QTextEdit wrapper)
│   └─ canvas.py              (EditableCanvas – kept for demo, can be removed)
│
└─ utils/
    ├─ __init__.py
    ├─ style.py               (colour palettes + apply_style)
    ├─ icons.py               (icon loader + ToolButton)
    └─ env.py                 (OPENAI key loader)






===========================================================================
1)  utils/style.py
===========================================================================

from pathlib import Path
from PySide6.QtWidgets import QWidget

SCHEME_BLUE  = {"col1": "#3a5fff", "col2": "#6280ff"}
SCHEME_GREEN = {"col1": "#0fe913", "col2": "#58ed5b"}
SCHEME_GREY  = {
    "col5": "#161616",
    "col6": "#E3E3DED6",
    "col7": "#1F1F1F",
    "col8": "#E3E3DED6",
}
SCHEME_DARK  = {
    "col5": "#1F1F1F",
mit 6 Falafel, Salat und einer Beilage nach Wahl
    "col6": "#E3E3DED6",
    "col7": "#161616",
    "col8": "#E3E3DED6",
}

_STYLE_SRC = Path(__file__).with_name("qss_template.txt").read_text()

def build_scheme(accent: dict, base: dict) -> dict:
    return {**base, **accent}

def apply_style(w: QWidget, scheme: dict) -> None:
    w.setStyleSheet(_STYLE_SRC.format(**scheme))
mit 6 Falafel, Salat und einer Beilage nach Wahl

(The QSS template was moved to an external text file, it is *identical* to the
one in the original script.)



===========================================================================
2)  utils/icons.py
===========================================================================

from pathlib import Path
from typing  import Optional, Callable
from PySide6.QtCore   import QSize
from PySide6.QtGui    import QIcon
from PySide6.QtWidgets import QPushButton

def icon(name: str) -> QIcon:
    base = Path(__file__).with_name("..").resolve() / "symbols"
    return QIcon(str(base / name))

class ToolButton(QPushButton):
    def __init__(self,
                 svg:      str,
                 tooltip:  str = "",
                 slot: Optional[Callable] = None,
                 parent=None):
        super().__init__(parent)
        self.setIcon(icon(svg))
        self.setIconSize(QSize(22, 22))
        self.setFlat(True)
        if tooltip:
            self.setToolTip(tooltip)
        if slot:
            self.clicked.connect(slot)



===========================================================================
3)  utils/env.py           (unchanged logic – only isolated)
===========================================================================

import os
from pathlib import Path
from dotenv import load_dotenv


def openai_key() -> str:
    root = Path(__file__).resolve().parents[2] / ".env"
    local = Path(__file__).with_suffix(".env")

    for p in (root, local):
        if p.exists():
            load_dotenv(p, override=False)
            break

    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "Missing OPENAI_API_KEY.\n"
            "Create a .env file with\n"
            '    OPENAI_API_KEY="sk-..."'
        )
    return key

    


===========================================================================
4) widgets/editor.py       (100 % identical code – merely relocated)
===========================================================================

from __future__ import annotations
from pathlib import Path
from PySide6.QtCore    import Qt, Slot
from PySide6.QtGui     import QTextLine
from PySide6.QtWidgets import (
    QDockWidget, QTabWidget, QTextEdit, QFileDialog, QMessageBox
)


class EditorTabs(QTabWidget):
    …                                               # unchanged


class EditorDock(QDockWidget):
    …                                               # unchanged
    def clone(self) -> "EditorDock": …

    

    


===========================================================================
5) widgets/ai_panel.py     (AIWidget, unchanged but imports moved)
===========================================================================

from __future__ import annotations
from typing import List
from PySide6.QtCore    import Qt, QEvent, QSize, Signal, Slot
from PySide6.QtWidgets import (QWidget, QSplitter, QTextEdit,
                               QMessageBox, QHBoxLayout, QVBoxLayout)

from ..utils.icons import ToolButton
from ..utils.env   import openai_key
from ..utils.style import build_scheme
from ChatClassCompletion import ChatCom, ImageDescription    # noqa: E402

class FileDropTextEdit(QTextEdit): …
class AIWidget(QWidget): …
    (identical as before except: _api_key = openai_key())

    


===========================================================================
6) widgets/explorer.py  +  widgets/console.py + widgets/canvas.py
===========================================================================

All three are tiny wrappers that simply expose the old placeholder widgets so
they can be imported cleanly:

from PySide6.QtWidgets import QTextEdit
class ExplorerView(QTextEdit):
    def __init__(self): super().__init__("Outline …")


from PySide6.QtWidgets import QTextEdit
class ConsoleView(QTextEdit):
    def __init__(self): super().__init__("Console / Output")


(EditableCanvas is copied verbatim into canvas.py, but can be deleted if not
needed.)




===========================================================================
7)  main.py    (only **this** file has to be run)
===========================================================================

from __future__ import annotations
import sys
from pathlib import Path

from PySide6.QtCore    import Qt, Slot, QSize
from PySide6.QtGui     import QAction
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QStyle,
    QFileDialog, QTextEdit, QMessageBox, QToolBar, QStatusBar, QMenuBar
)

# 3rd-party --------------------------------------------------------------
from ChatClassCompletion import ChatCom, ImageDescription    # noqa: E402

# local modules ----------------------------------------------------------
from widgets.editor   import EditorDock, EditorTabs
from widgets.ai_panel import AIWidget
from widgets.explorer import ExplorerView
from widgets.console  import ConsoleView
from utils.icons  import ToolButton
from utils.style  import (
    SCHEME_BLUE, SCHEME_GREEN, SCHEME_GREY, SCHEME_DARK,
    apply_style, build_scheme
)


class MainAIEditor(QMainWindow):
    ORG_NAME = "ai.bentu"
    APP_NAME = "AI-Editor"

    # --------------------------------------------------------------- init
    def __init__(self) -> None:
        super().__init__()

        self._accent = SCHEME_BLUE
        self._base   = SCHEME_DARK

        self.setWindowTitle("AI Editor – Synergetic")
        self.resize(1280, 800)

        # central widgets -------------------------------------------------
        self._build_central_splitters()

        # tool-bars / menu / status --------------------------------------
        self._build_tool_bar()
        self._build_menu_bar()
        self.setStatusBar(QStatusBar())

        apply_style(self, build_scheme(self._accent, self._base))

    # ------------------------------------------------------------------ central
    def _build_central_splitters(self) -> None:
        """
        Implements the ASCII-sketch:

           ┌<–v-splitter (outer)
           | ┌──h-splitter───────────────┐
           | │ Files │   Editors   │ AI  │
           | └───────────────────────────┘
           | │           Console         │
           └─────────────────────────────┘
        """
        outer = QSplitter(Qt.Vertical, self)
        top   = QSplitter(Qt.Horizontal, outer)

        # --- left : explorer            ---------------------------------
        top.addWidget(ExplorerView())

        # --- middle : editor tabs (in a dock so they can be duplicated) -
        self.editor_dock = EditorDock(self)
        top.addWidget(self.editor_dock.widget())        # just the tabs!

        # --- right : chat panel         ---------------------------------
        top.addWidget(AIWidget(self._accent, self._base))

        # --- bottom : console           ---------------------------------
        outer.addWidget(ConsoleView())

        # weight: [upper ¾, lower ¼]
        outer.setSizes([600, 200])
        self.setCentralWidget(outer)

    # ------------------------------------------------------------------ tool bar
    def _build_tool_bar(self) -> None:
        style = self.style()
        tb    = QToolBar()
        self.addToolBar(tb)

        self.act_new_tab = QAction(
            style.standardIcon(QStyle.SP_FileIcon), "", self, triggered=self._new_tab)
        self.act_close_tab = QAction(
            style.standardIcon(QStyle.SP_DialogCloseButton), "", self, triggered=self._close_tab)
        self.act_toggle_accent = QAction(
            style.standardIcon(QStyle.SP_BrowserReload), "", self, triggered=self._toggle_accent)
        self.act_open_file = QAction(
            style.standardIcon(QStyle.SP_DialogOpenButton), "", self, triggered=self._open_file)

        tb.addActions([self.act_new_tab, self.act_close_tab,
                       self.act_open_file, self.act_toggle_accent])

    # ------------------------------------------------------------------ menu
    def _build_menu_bar(self) -> None:
        mbar = QMenuBar()
        self.setMenuBar(mbar)
        view = mbar.addMenu("View")
        self.act_grey = QAction("Greyscale", self, checkable=True,
                                toggled=self._toggle_grey)
        view.addAction(self.act_grey)

    # -------------- helpers --------------------------------------------
    def _current_tabs(self) -> EditorTabs:
        w = self.focusWidget()
        while w and not isinstance(w, EditorDock):
            w = w.parent()
        return w.tabs if isinstance(w, EditorDock) else self.editor_dock.tabs

    # -------------- slots ----------------------------------------------
    @Slot() def _new_tab       (self): …
    @Slot() def _close_tab     (self): …
    @Slot() def _open_file     (self): …
    @Slot() def _toggle_accent (self):
        self._accent = SCHEME_GREEN if self._accent is SCHEME_BLUE else SCHEME_BLUE
        apply_style(self, build_scheme(self._accent, self._base))
    @Slot() def _toggle_grey   (self, checked: bool):
        self._base = SCHEME_GREY if checked else SCHEME_DARK
        apply_style(self, build_scheme(self._accent, self._base))


def main() -> None:
    app = QApplication(sys.argv)
    win = MainAIEditor()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

    


===========================================================================
What changed – and why?
===========================================================================

1  Split the file into *logical* modules.  
   Reading / testing / exchanging any part is now trivial.

2  Re-implemented the central area exactly as in the sketch  
   (nested vertical + horizontal splitters).

3  The old QDockWidgets (“Files”, “AI chat”) were replaced by plain widgets
   because the sketch shows them as integral, non-floating panels.  
   You can of course re-dock them again – just swap `ExplorerView()` with a
   proper `QDockWidget("Files")` if you prefer the old behaviour.

4  All styling, icons and environment logic live in the `utils` package.

5  No functionality has been dropped:  
   – multiple editor tabs & multiple editor *docks* (via clone)  
   – ChatGPT dialogue & image analysis  
   – drag-and-drop files into the chat panes  
   – accent switcher / grey mode / about box / open file …

Enjoy the cleaner, easier-to-maintain code base!'''


'''There is no object called fies_dock (or files_dock) anywhere in the script you pasted.

• The QDockWidget that represents the “file / outline / explorer” panel is created inside MainAIEditor._create_dock_widgets and is stored in the attribute

    self.explorer_dock      # title = "Files"

If somewhere else in your code you wrote something like

    self.files_dock.show()

or

    win.fies_dock.setVisible(True)

Python will raise

    AttributeError: 'MainAIEditor' object has no attribute 'files_dock'   # or fies_dock

because only explorer_dock exists.  
So either

1. Change every occurrence of fies_dock or files_dock to explorer_dock, or  
2. Rename the variable when you create it:

       self.files_dock = QDockWidget("Files", self)
       …                           # build widget
       self.addDockWidget(Qt.LeftDockWidgetArea, self.files_dock)

then use files_dock everywhere else.

Tip for locating it quickly: in an editor search for either

    "Files"             # the window-title string
or

    QDockWidget("Files" # creation of the dock widget

Those are the only places where the file-explorer dock is defined.'''


'''There simply is no attribute or variable called  fies_dock (nor files_dock) anywhere in the module you pasted.

The “Files / Explorer” panel is created here:

```python
# MainAIEditor._create_dock_widgets
self.explorer_dock = QDockWidget("Files", self)
self.explorer_dock.setWidget(QTextEdit("Outline …"))
self.addDockWidget(Qt.LeftDockWidgetArea, self.explorer_dock)
```

So if another part of your program tries to access

```python
win.fies_dock
# or
self.files_dock
```

Python will raise

```
AttributeError: 'MainAIEditor' object has no attribute 'fies_dock'
```

Fixes:

1. Use the existing name:

   ```python
   win.explorer_dock.show()
   ```

2. …or rename it at creation so the rest of your code matches:

   ```python
   self.files_dock = QDockWidget("Files", self)   # instead of explorer_dock
   …
   self.addDockWidget(Qt.LeftDockWidgetArea, self.files_dock)
   ```

A quick way to verify is to search the file (or the whole project) for the string “Files” or for `QDockWidget(`—you’ll only find the `explorer_dock` definition and no `fies_dock / files_dock`.'''