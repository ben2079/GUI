# JsonTreeWidget - Feature Documentation

## Übersicht
Das JsonTreeWidget ist ein VS Code-ähnlicher Explorer mit Multi-Root-Unterstützung, automatischer Datenpersistenz und umfangreichen Import/Export-Funktionen.

## Toolbar Buttons (von links nach rechts)

### 📂 Load History
- Lädt Chat-Historie aus ChatHistory._history_
- Fügt zur HISTORY Section hinzu

### ⬇ Collapse All
- Klappt alle Tree-Items ein
- Schneller Überblick über Workspace-Struktur

### ➕ Add Project
- Dialog zum Hinzufügen eines neuen Projekts
- Erstellt Projekt-Eintrag in PROJECTS Section
- Felder: name, path, files, settings

### 🗄 Add Database
- Dialog zum Hinzufügen einer Datenbankverbindung
- Erstellt DB-Eintrag in DATABASES Section
- Felder: type, host, port, database, username

### 📥 Import JSON
**Funktionalität:**
- Lädt beliebige JSON-Datei
- Dialog zur Auswahl der Ziel-Section (PROJECTS/DATABASES/HISTORY)
- Dialog zur Angabe eines Item-Namens
- Fügt importierte Daten zur gewählten Section hinzu

**Anwendungsfälle:**
- Import von Projekt-Konfigurationen
- Import von Datenbank-Verbindungen
- Import von Chat-Historie
- Migration von Daten aus anderen Tools

### 📤 Export JSON
**Funktionalität:**
- Selektiver Export einzelner oder mehrerer Sections
- Dialog mit Checkboxen zur Auswahl der Sections
- Zeigt Anzahl der Items pro Section
- Exportiert nur ausgewählte Sections

**Anwendungsfälle:**
- Backup einzelner Sections
- Teilen von Projekt-Konfigurationen
- Export von Datenbank-Verbindungen
- Partielle Workspace-Migration

### 📋 Load Template
**Funktionalität:**
- Listet Built-in Templates auf
- Lädt benutzerdefinierte Templates aus `AppData/templates/`
- Option zum Laden aus beliebiger Datei
- Merge- oder Replace-Modus beim Anwenden

**Built-in Templates:**
1. **Python Web Project**
   - Flask-Web-App mit PostgreSQL
   - Files: app.py, requirements.txt, config.py
   - Settings: Framework, Python-Version, Debug-Flag

2. **Data Science Project**
   - Jupyter Notebook Setup
   - Files: analysis.ipynb, data_processing.py
   - Libraries: pandas, numpy, matplotlib, scikit-learn

3. **Microservices Setup**
   - 3 Services: API-Gateway, Auth, Data
   - Redis Cache + MongoDB
   - Port-Konfiguration

4. **Empty Workspace**
   - Leert alle Sections
   - Neustart ohne alte Daten

**Benutzerdefinierte Templates:**
- Werden mit 📁-Symbol gekennzeichnet
- Aus `AppData/templates/*.json` geladen
- Automatisch in Liste eingebunden

### 💾 Save as Template
**Funktionalität:**
- Speichert aktuellen Workspace als wiederverwendbares Template
- Dialog zur Auswahl der zu inkludierenden Sections
- Speichert in `AppData/templates/`
- Automatisch verfügbar beim nächsten "Load Template"

**Workflow:**
1. Workspace aufbauen (Projekte, DBs, etc.)
2. 💾 Click → Template-Name eingeben
3. Sections auswählen (z.B. nur PROJECTS)
4. Speichern → Template ist verfügbar

**Anwendungsfälle:**
- Projekt-Boilerplates erstellen
- Standard-DB-Verbindungen speichern
- Team-Konfigurationen teilen
- Schnelles Setup für neue Projekte

---

## Datenpersistenz

### Automatisches Speichern
- **Trigger:** Jedes Add/Remove/Edit von Items
- **Speicherort:** `AppData/tree_data.json`
- **Format:** JSON mit Sections als Top-Level Keys
- **Kodierung:** UTF-8 mit ensure_ascii=False

### Automatisches Laden
- Beim Widget-Start wird `_load_data()` aufgerufen
- Stellt alle Sections und Items wieder her
- Tracking-Dictionaries werden aktualisiert

### Speicherstruktur
```json
{
  "PROJECTS": {
    "ProjectName": {
      "name": "...",
      "path": "...",
      "files": [],
      "settings": {}
    }
  },
  "DATABASES": {
    "ConnectionName": {
      "type": "PostgreSQL",
      "host": "localhost",
      ...
    }
  },
  "HISTORY": {}
}
```

---

## Editier-Funktionalität

### Item Editing
- Alle Items sind editierbar (Qt.ItemIsEditable)
- Doppelklick oder F2 zum Editieren
- Format: `key: value` (JSON-Value)

### Sync-Mechanismus
- `_on_item_changed()` wird bei jeder Änderung getriggert
- Baut Pfad vom Item zur Section-Root auf
- Aktualisiert `_data` Dictionary
- Ruft `_save_data()` auf

### Rekursionsschutz
- `blockSignals()` verhindert Endlos-Loops
- Canonical Text wird nur gesetzt wenn nötig

---

## Architektur

### Klassen-Hierarchie
```
JsonTreeWidgetWithToolbar (QWidget)
├── QFrame (Toolbar, 28px height)
│   └── 8x QToolButton (26x26px)
└── JsonTreeWidget (QTreeWidget)
    ├── _data: dict[str, dict[str, Any]]
    ├── _root_sections: dict[str, QTreeWidgetItem]
    ├── _item_to_section: dict[QTreeWidgetItem, str]
    └── _item_to_key: dict[QTreeWidgetItem, str]
```

### Datenfluss
1. **Add:** `add_to_section()` → Update `_data` → Update Tracking → `_save_data()`
2. **Edit:** User edit → `_on_item_changed()` → Parse path → Update `_data` → `_save_data()`
3. **Remove:** `remove_from_section()` → Update `_data` → Update Tracking → `_save_data()`
4. **Import:** File → Parse JSON → `add_to_section()` → (siehe Add)
5. **Export:** Select sections → Filter `_data` → Write file
6. **Template:** Load → Parse → `_apply_template()` → Batch `add_to_section()`

---

## API für Integration

### Öffentliche Methoden

```python
# Section Management
add_to_section(section_name: str, key: str, value: Any) -> None
remove_from_section(section_name: str, item_name: str) -> bool

# Legacy (für Kompatibilität)
set_json(data: Any) -> None
```

### Verwendung in ai_ide_v1756.py

```python
from jstree_widget import JsonTreeWidgetWithToolbar

# Widget erstellen
explorer = JsonTreeWidgetWithToolbar()

# Projekt hinzufügen
explorer.add_to_section("PROJECTS", "MyProject", {
    "name": "My Project",
    "path": "/path/to/project"
})

# In Dock integrieren
dock = QDockWidget("Explorer")
dock.setWidget(explorer)
self.addDockWidget(Qt.LeftDockWidgetArea, dock)
```

---

## Verzeichnisstruktur

```
AppData/
├── tree_data.json           # Automatische Persistenz
└── templates/               # Benutzerdefinierte Templates
    ├── My_Custom_Setup.json
    └── Team_Config.json
```

---

## Keyboard Shortcuts (geplant/möglich)

- `Ctrl+I` - Import JSON
- `Ctrl+E` - Export JSON
- `Ctrl+T` - Load Template
- `Ctrl+Shift+T` - Save as Template
- `F2` - Rename Item
- `Delete` - Remove Item

---

## Best Practices

### Template-Erstellung
1. Build einmal manuell den gewünschten Workspace auf
2. Teste alle Einstellungen
3. Save as Template mit aussagekräftigem Namen
4. Optional: Teile Template-Datei mit Team (Git, E-Mail, etc.)

### Import/Export
- Nutze Export für Backups vor größeren Änderungen
- Exportiere einzelne Sections statt Alles
- Import mit Merge wenn du bestehende Daten behalten willst

### Section-Naming
- PROJECTS: Für Code-Projekte, Repos
- DATABASES: Für DB-Verbindungen, APIs
- HISTORY: Für Chat-Historie, Logs
- Eigene Sections möglich durch Anpassung von `_initialize_root_sections()`

---

## Troubleshooting

### Template lädt nicht
- Check `AppData/templates/` Verzeichnis existiert
- JSON-Syntax valide? (validate mit `jq` oder online tool)
- Prüfe Console-Output für Fehlermeldungen

### Items werden nicht gespeichert
- `_save_data()` wird bei jedem Edit aufgerufen
- Check `AppData/tree_data.json` Schreibrechte
- Console zeigt "[INFO] Tree data saved to ..." bei Erfolg

### Import schlägt fehl
- JSON muss valides Format haben
- Kann beliebige Struktur sein (wird als Value gespeichert)
- Section muss existieren oder wird automatisch erstellt

---

## Erweiterungsmöglichkeiten

### Geplant
- Context-Menu für Items (Right-Click)
- Drag & Drop zwischen Sections
- Search/Filter Funktionalität
- Undo/Redo für Edits
- Export als YAML, TOML

### Entwickler-Hooks
```python
# Eigene Section hinzufügen
def _initialize_root_sections(self):
    super()._initialize_root_sections()
    self._add_root_section("CUSTOM_SECTION")
    self._data["CUSTOM_SECTION"] = {}

# Custom Template Provider
def _get_builtin_templates(self):
    templates = super()._get_builtin_templates()
    templates["My Company Template"] = {...}
    return templates
```

---

## Lizenz & Maintenance
- Teil von ai_ide_v1756 Projekt
- Maintainer: ben2079
- Stand: November 2025
