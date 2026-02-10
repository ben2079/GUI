# JsonTreeWidget Speicherlogik - Dokumentation

## Übersicht

Die JsonTreeWidget Speicherlogik wurde vollständig überarbeitet, um mit der Multi-Root-Struktur (PROJECTS, DATABASES, HISTORY) zu funktionieren.

## Implementierung

### Datenstruktur

```python
self._data: dict[str, dict[str, Any]] = {
    "PROJECTS": {},
    "DATABASES": {},
    "HISTORY": {}
}
```

### Tracking Dictionaries

```python
self._item_to_section: dict[QTreeWidgetItem, str] = {}  # Item -> Section Name
self._item_to_key: dict[QTreeWidgetItem, str] = {}      # Item -> Key in Section
```

### Speicherort

Daten werden gespeichert in: `AppData/tree_data.json` (relativ zum Projektstammverzeichnis)

## Funktionen

### 1. `add_to_section(section_name, key, value)`
- Fügt Daten zu einer Section hinzu
- Speichert in `_data[section_name][key] = value`
- Registriert das Item in den Tracking-Dictionaries
- Speichert automatisch nach dem Hinzufügen

### 2. `remove_from_section(section_name, item_name)`
- Entfernt ein Item aus einer Section
- Löscht aus `_data` und Tracking-Dictionaries
- Speichert automatisch nach dem Löschen

### 3. `_on_item_changed(item, column)`
- Wird bei Bearbeitung eines Items aufgerufen
- Findet die zugehörige Section durch Tracking oder Tree-Walking
- Extrahiert den Pfad vom Item zur Section-Root
- Aktualisiert `_data[section_name]` mit dem neuen Wert
- Speichert automatisch nach erfolgreicher Änderung

### 4. `_save_data()`
- Speichert `_data` als JSON nach `AppData/tree_data.json`
- Verwendet `ensure_ascii=False` für UTF-8 Zeichen
- Verwendet `indent=2` für lesbare Formatierung

### 5. `_load_data()`
- Wird beim Initialisieren aufgerufen
- Lädt `tree_data.json` wenn vorhanden
- Stellt alle Sections und Items wieder her
- Registriert Items in den Tracking-Dictionaries

## Automatisches Speichern

Die Daten werden automatisch gespeichert bei:
- Hinzufügen eines Items (`add_to_section`)
- Löschen eines Items (`remove_from_section`)
- Bearbeiten eines Items (`_on_item_changed`)

## Bearbeitung von Items

Items können direkt im Tree bearbeitet werden durch:
1. Doppelklick auf das Item
2. Neue Werte im Format `key: value` eingeben
3. Enter drücken

Die Änderungen werden automatisch:
- In die `_data` Struktur geschrieben
- Auf die Festplatte gespeichert
- Im Tree formatiert angezeigt

## Pfad-Auflösung

Die `_on_item_changed` Methode baut den Pfad vom bearbeiteten Item zur Section-Root auf:

```
PROJECTS (Section Root)
  └── TestProject1 (key="TestProject1")
      └── settings {...}
          └── version: "1.0"  ← Edit hier
```

Pfad: `["TestProject1", "settings", "version"]`

Lookup: `_data["PROJECTS"]["TestProject1"]["settings"]["version"] = "1.0"`

## Fehlerbehandlung

- Recursion Protection: `blockSignals()` verhindert Endlosschleifen
- Section-Validierung: Prüft ob Section in `_data` existiert
- Pfad-Validierung: Fängt KeyError/IndexError bei ungültigen Pfaden ab
- Disk I/O: Gibt Warnings bei Speicher-/Ladefehlern aus

## Beispiel

```python
# Widget erstellen
widget = JsonTreeWidgetWithToolbar()

# Daten hinzufügen
widget.add_to_section("PROJECTS", "MyProject", {
    "name": "My Project",
    "path": "/home/user/myproject",
    "files": ["main.py"]
})

# Automatisch gespeichert nach AppData/tree_data.json

# Beim nächsten Start werden die Daten automatisch geladen
```

## Tests

Siehe `test_jstree_save.py` für einen vollständigen Test der Speicherfunktionalität.

## Status

✅ Speichern funktioniert
✅ Laden funktioniert
✅ Bearbeiten funktioniert
✅ Löschen funktioniert
✅ Multi-Root Struktur wird unterstützt
✅ Automatisches Speichern nach jeder Änderung
