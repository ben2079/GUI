# JsonTreeWidget - Multi-Root Explorer (VS Code Style)

## Übersicht

Der `JsonTreeWidget` wurde erweitert, um mehrere parallele Baumstrukturen zu unterstützen, ähnlich dem VS Code Explorer. Dies ermöglicht die Organisation verschiedener Datentypen in separaten, unabhängigen Wurzelsektionen.

## Neue Features

### 1. **Multi-Root Struktur**
Der Tree unterstützt jetzt mehrere Wurzelelemente:
- **PROJECTS** - Projektverwaltung
- **DATABASES** - Datenbankverbindungen
- **HISTORY** - Chat-Historie und andere Verlaufsdaten

### 2. **Neue Buttons in der Toolbar**

```
[📂] [⬇] [➕] [🗄️]
```

- **📂 Load History** - Lädt Chat-Historie in HISTORY Sektion
- **⬇ Collapse All** - Klappt alle Einträge zu
- **➕ Add Project** - Fügt neues Projekt zur PROJECTS Sektion hinzu
- **🗄️ Add Database** - Fügt neue Datenbankverbindung hinzu

### 3. **Neue Methoden**

#### `_initialize_root_sections()`
Initialisiert die Standard-Wurzelsektionen beim Start.

#### `_add_root_section(name: str, collapsed: bool = False) -> QTreeWidgetItem`
Fügt eine neue Wurzelsektion hinzu.

```python
tree._add_root_section("CUSTOM", collapsed=False)
```

#### `add_to_section(section_name: str, key: str, value: Any) -> None`
Fügt Daten zu einer bestimmten Sektion hinzu.

```python
tree.add_to_section("PROJECTS", "My App", {
    "path": "/home/user/app",
    "files": ["main.py"]
})
```

#### `remove_from_section(section_name: str, item_name: str) -> bool`
Entfernt ein Element aus einer Sektion.

```python
tree.remove_from_section("PROJECTS", "My App")
```

## Verwendungsbeispiele

### Beispiel 1: Projekt hinzufügen

```python
from jstree_widget import JsonTreeWidgetWithToolbar

tree = JsonTreeWidgetWithToolbar()

# Projekt hinzufügen
project_data = {
    "name": "AI IDE",
    "path": "/home/user/ai_ide",
    "files": ["main.py", "config.json"],
    "settings": {
        "python_version": "3.11",
        "venv": ".venv"
    }
}

tree.add_to_section("PROJECTS", "AI IDE", project_data)
```

### Beispiel 2: Datenbankverbindung hinzufügen

```python
db_connection = {
    "type": "PostgreSQL",
    "host": "localhost",
    "port": 5432,
    "database": "myapp_db",
    "username": "admin",
    "ssl": True
}

tree.add_to_section("DATABASES", "Production DB", db_connection)
```

### Beispiel 3: Eigene Sektion erstellen

```python
# Neue Sektion für API-Endpoints
tree._add_root_section("APIs", collapsed=False)

api_config = {
    "base_url": "https://api.example.com",
    "endpoints": [
        "/users",
        "/posts",
        "/comments"
    ],
    "auth": {
        "type": "Bearer",
        "token": "xxx"
    }
}

tree.add_to_section("APIs", "Main API", api_config)
```

### Beispiel 4: Dynamisch mehrere Projekte laden

```python
projects = [
    {"name": "Project A", "path": "/home/user/project-a"},
    {"name": "Project B", "path": "/home/user/project-b"},
    {"name": "Project C", "path": "/home/user/project-c"},
]

for proj in projects:
    tree.add_to_section("PROJECTS", proj["name"], proj)
```

## Styling

Die Wurzelsektionen haben ein spezielles Styling:
- **Fettgedruckt** für bessere Sichtbarkeit
- **Hellere Farbe** (#cccccc) zur Unterscheidung von Einträgen
- **Größere Schrift** (10pt) für Hierarchie

## Integration in die Hauptanwendung

```python
from PySide6.QtWidgets import QMainWindow, QDockWidget
from PySide6.QtCore import Qt
from jstree_widget import JsonTreeWidgetWithToolbar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Explorer Dock erstellen
        self.explorer = JsonTreeWidgetWithToolbar()
        
        dock = QDockWidget("Explorer", self)
        dock.setWidget(self.explorer)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        
        # Beispieldaten laden
        self._load_workspace()
    
    def _load_workspace(self):
        # Projekte laden
        for project in self.get_projects():
            self.explorer.add_to_section("PROJECTS", 
                                        project["name"], 
                                        project)
        
        # Datenbankverbindungen laden
        for db in self.get_databases():
            self.explorer.add_to_section("DATABASES", 
                                        db["name"], 
                                        db)
```

## Vergleich mit VS Code Explorer

| Feature | VS Code | JsonTreeWidget |
|---------|---------|----------------|
| Multiple Root Folders | ✅ | ✅ |
| Collapsible Sections | ✅ | ✅ |
| Add/Remove Roots | ✅ | ✅ |
| Inline Editing | ✅ | ✅ |
| Custom Sections | ❌ | ✅ |
| Hierarchical Data | ✅ | ✅ |

## Bekannte Einschränkungen

1. **Persistenz**: Änderungen werden aktuell nicht automatisch gespeichert
2. **Icons**: Standard-Icons werden verwendet (können angepasst werden)
3. **Drag & Drop**: Noch nicht implementiert

## Zukünftige Erweiterungen

- [ ] Drag & Drop zwischen Sektionen
- [ ] Kontextmenü für Sektionen
- [ ] Automatisches Speichern von Änderungen
- [ ] Import/Export von Konfigurationen
- [ ] Suche über alle Sektionen
- [ ] Custom Icons pro Sektion
- [ ] Verschachtelte Sektionen

## Test

Führe die Test-Datei aus, um die Funktionalität zu demonstrieren:

```bash
python test_jstree_multi_root.py
```

## Lizenz

Teil des AI_IDE_v1756 Projekts
