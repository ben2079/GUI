# Apply Agent – Ausführungsleitfaden

## Ziel
Bewerbungen automatisiert erstellen, deduplizieren, validieren und mit Metadaten im Vektor-Store ablegen.

## Pflicht-Ressourcen
- Profilquelle: AGENTS.md (per Retrieval/Tool-Aufruf relevante Passagen ziehen).
- Anhänge: /lebenslauf.pdf, /zeugnisse.pdf, /portfolio.pdf.
- Vorlagen: Muster-Anschreiben je Job-Typ (z.B. Anwendungsentwickler).

## Workflow (Checkliste)
1. **Kontext laden**
   - RAG/Tool: relevante Passagen aus AGENTS.md abfragen.
   - Stellenanzeige parsen (Titel, Firma, Ansprechpartner, E-Mail, Anforderungen).
2. **Deduplizieren**
   - Vektor-Store prüfen auf gleiche Firma + Jobtitel (+ optional Datum ≤30 Tage).
3. **Analyse der Anzeige**
   - Muss-/Kann-Kriterien, Tech-Stack, Kernanforderungen extrahieren.
4. **Anschreiben generieren**
   - Vorlage nach Job-Typ wählen.
   - Platzhalter füllen: {Firma}, {JobTitel}, {Ansprechpartner}, {Datum}, {USP}, {Beispiele}, {CallToAction}.
5. **Validieren**
   - Sprache/Format prüfen (Deutsch, höflich), Kontakte korrekt, Anhänge referenziert.
6. **Persistieren**
   - Anschreiben + Metadaten im Vektor-Store ablegen (Schema unten).
   - Bewerbung als erledigt markieren (für spätere Deduplikation).
7. **Anhänge referenzieren**
   - Pfade der Anhänge im Datensatz hinterlegen.

## Ablauf – Sequenzdiagramm (Mermaid)
```mermaid
sequenceDiagram
    actor User as User / Stellenposting
    participant Agent as Apply-Agent
    participant Profile as Profil-Lader
    participant Dedup as Duplikat-Check
    participant Retrieval as Retrieval / Kontext
    participant Drafter as Anschreiben-Generator
    participant Validator as Validator
    participant Store as Persistenz
    participant Delivery as Versand / Skip

    User->>Agent: Neue Stellenanzeige (Rolle, Firma, Kontakt)
    Agent->>Profile: Profil-Kontext laden (AGENTS.md)
    Agent->>Dedup: Prüfe vorhandene Bewerbungen (Firma+Job)
    Dedup-->>Agent: Status (neu / bereits vorhanden)
    Agent->>Retrieval: RAG-Kontext + Anforderungen extrahieren
    Retrieval-->>Agent: Kontext (USP, Beispiele, Stack)
    Agent->>Drafter: Anschreiben mit Vorlage erzeugen
    Drafter-->>Agent: Entwurf
    Agent->>Validator: Format/Contact/Anhänge prüfen
    Validator-->>Agent: OK oder Fehler + Hinweise
    Agent->>Store: Anschreiben + Metadaten speichern
    Store-->>Agent: Persistenz bestätigt
    Agent->>Delivery: Senden oder überspringen (wenn Duplikat)
```

## Zustände – State/Flow (Mermaid)
```mermaid
stateDiagram-v2
    [*] --> Profil_laden
    Profil_laden --> Anzeige_parsen
    Anzeige_parsen --> Deduplizieren
    Deduplizieren --> Kontext_retrieval
    Deduplizieren --> Skip_bestehend: bereits vorhanden
    Kontext_retrieval --> Entwurf_erstellen
    Entwurf_erstellen --> Validieren
    Validieren --> Persistieren: valid
    Validieren --> Entwurf_erstellen: retry bei Fehler
    Persistieren --> Versenden
    Persistieren --> Skip_bestehend: optional
    Versenden --> [*]
    Skip_bestehend --> [*]

    state Validieren {
        [*] --> Format_check
        Format_check --> Kontakt_check
        Kontakt_check --> Anhang_check
        Anhang_check --> [*]
    }
```

## UML (PlantUML) – Sequenz & Zustände
### Sequenz (PlantUML)
```plantuml
@startuml
actor User as "User / Stellenposting"
participant Agent as "Apply-Agent"
participant Profile as "Profil-Lader"
participant Dedup as "Duplikat-Check"
participant Retrieval as "Retrieval / Kontext"
participant Drafter as "Anschreiben-Generator"
participant Validator as "Validator"
participant Store as "Persistenz"
participant Delivery as "Versand / Skip"

User -> Agent: Neue Stellenanzeige (Rolle, Firma, Kontakt)
Agent -> Profile: Profil-Kontext laden (AGENTS.md)
Agent -> Dedup: Prüfe vorhandene Bewerbungen (Firma+Job)
Dedup --> Agent: Status (neu / vorhanden)
Agent -> Retrieval: RAG-Kontext + Anforderungen
Retrieval --> Agent: Kontext (USP, Beispiele, Stack)
Agent -> Drafter: Anschreiben erzeugen (Vorlage)
Drafter --> Agent: Entwurf
Agent -> Validator: Format/Kontakt/Anhänge prüfen
Validator --> Agent: OK oder Fehlerhinweise
Agent -> Store: Anschreiben + Metadaten speichern
Store --> Agent: Persistenz bestätigt
Agent -> Delivery: Senden oder überspringen
@enduml
```

### Zustände (PlantUML)
```plantuml
@startuml
[*] --> Profil_laden
Profil_laden --> Anzeige_parsen
Anzeige_parsen --> Deduplizieren
Deduplizieren --> Kontext_retrieval
Deduplizieren --> Skip_bestehend : Duplikat
Kontext_retrieval --> Entwurf_erstellen
Entwurf_erstellen --> Validieren
Validieren --> Persistieren : valid
Validieren --> Entwurf_erstellen : retry bei Fehler
Persistieren --> Versenden
Persistieren --> Skip_bestehend : optional
Versenden --> [*]
Skip_bestehend --> [*]

state Validieren {
   [*] --> Format_check
   Format_check --> Kontakt_check
   Kontakt_check --> Anhang_check
   Anhang_check --> [*]
}
@enduml
```

## Persistenz-Schema (Beispiel, JSON)
```json
{
  "firma": "Example GmbH",
  "job_titel": "Anwendungsentwickler",
  "email": "hr@example.com",
  "ansprechpartner": "Frau Muster",
  "source_url": "https://example.com/jobs/123",
  "generiert_am": "2025-04-21T10:00:00Z",
  "sprache": "de",
  "anschreiben": "Sehr geehrte ...",
  "quellen": ["AGENTS.md", "Stellenanzeige_123.pdf"],
  "anhaenge": ["/lebenslauf.pdf", "/zeugnisse.pdf", "/portfolio.pdf"],
  "vector_ref": "AppData/index.faiss#example-gmbh-anwendungsentwickler",
  "status": "gesendet",
  "hash_key": "example-gmbh|anwendungsentwickler|2025-04",
  "notizen": "Kontakt bestätigt, Versand per E-Mail"
}
```

## Auto-Generated Graphs (LangGraph-Style Platzhalter)
- Aktuelles Export-Asset hier einbinden: `ai_ide/Dokumente/job_agent_graph.svg` (oder `.png`).
- Zum Aktualisieren einfach die Datei ersetzen; Einbindung bleibt konstant.
- Beispiel-Einbettung:

![Job Agent Graph](job_agent_graph.svg)

## Preview/Update Hinweise
- Mermaid rendert nativ in GitHub und in VS Code (Markdown Preview, Mermaid-Erweiterung optional).
- Bei neuem Graph-Export nur die Datei unter `ai_ide/Dokumente/job_agent_graph.svg` ersetzen.
- Für andere Formate (png) den Dateinamen in der Einbettung anpassen.