# Context Assembly Pipeline

**Stand:** 09.07.2026  
**Verbindlich:** [ADR-0011](../adr/ADR-0011-context-builder-combines-context-layers.md)  
**Contract:** [context_assembly.schema.json](../contracts/source-resolution/context_assembly.schema.json)  
**Quellenreihenfolge:** [13_source_resolution.md](13_source_resolution.md) (ADR-0013)

## Kernaussage

Digiwiz erzeugt **keine Antwort direkt aus dem ersten Treffer**. Stattdessen durchläuft DAR eine **Context Assembly Pipeline**: Anfrage analysieren → Antwortziel und -struktur bestimmen → benötigte Informationsfelder ableiten → internes **Context-Array** aufbauen → Quellen **sequenziell und feldgesteuert** abfragen → erst danach Antwort generieren.

Fehlende **Pflichtinformationen** werden transparent ausgewiesen — **nicht geraten**.

---

## Pipeline (10 Schritte)

```
1.  Anfrage analysieren
2.  Antwortziel bestimmen
3.  Antwortstruktur bestimmen
4.  Benötigte Informationsfelder ableiten (required_fields)
5.  Internes Context-Array initialisieren (leer / missing)
6.  Quellen sequenziell abfragen (nur für offene Felder)
7.  Gefundene Informationen je Feld eintragen (context_array)
8.  Fehlende / unsichere Felder erkennen
9.  Nur für fehlende/unsichere Felder nächste Quellenstufe anzapfen
10. Konflikte markieren → Validierung → ggf. Antwortgenerierung
```

**Antwortgenerierung startet erst nach Schritt 10**, und nur wenn `ready_for_generation: true` oder fehlende Pflichtfelder explizit in der Antwort genannt werden.

---

## Quellenreihenfolge (feldgesteuert)

Die Pipeline nutzt **nicht alle Quellen blind**, sondern pro Feld die passende Stufe — in dieser **Priorität**:

| Stufe | Quelle | Wann | SSOT für |
|-------|--------|------|----------|
| 1 | **SQL / CRM / operative Daten** | Unternehmensdaten, Stammdaten | Strukturierte Firmendaten |
| 2 | **Knowledge Platform** | Regeln, Prozesse, Strukturen | Playbooks, ADRs, Contracts |
| 3 | **Knowledge Graph** | Beziehungen, Provenienz, Abhängigkeiten | Kanten (Stufe E) |
| 4 | **Chroma / RAG** | Ähnliche Inhalte, Formulierungen, semantischer Kontext | — (abgeleitet) |
| 5 | **Web / extern** | Nur bei Bedarf, ergänzend | — (niedrigste Priorität) |

**Regel:** Nächste Stufe nur für Felder mit Status `missing` oder `uncertain` — nicht für bereits `filled` Felder mit ausreichender Confidence.

---

## Entscheidungslogik je Feld

| Feldtyp | Erste Quelle | Nächste Stufe wenn |
|---------|--------------|-------------------|
| CRM-Status, Kundennummer, Umsatzklasse | SQL | SQL leer → `missing`, kein RAG-Raten |
| Freigabe, Auto-Publish, Governance | KP | — (Pflicht aus Playbook/ADR) |
| Beziehung Entität A → B | Graph (E) | Graph leer → optional RAG, nie SQL raten |
| Verfahren, Wiki-Formulierung | KP → RAG | RAG nur ergänzend |
| Branchennews extern | Web | Nie über SQL/KP für Firmendaten |

---

## Context-Array — Feldstatus

| Status | Bedeutung | Antwortgenerierung |
|--------|-----------|-------------------|
| `filled` | Wert aus autoritativer Quelle | Darf verwendet werden |
| `missing` | Keine Quelle lieferte Wert | Pflichtfeld → `ready_for_generation: false` |
| `uncertain` | Schwache/evidenzarme Evidenz | Ausweisen, nicht als Fakt |
| `conflict` | Widersprüchliche Quellen | Konflikt dokumentieren, Winner-Regel anwenden |

---

## Konflikte

Siehe [13_source_resolution.md](13_source_resolution.md) §6 und `source_resolution_policy.yaml`:

- **SQL > Chroma/Web** für Firmendaten
- **KP > Chroma** für Regeln
- **Graph** für Beziehungen, **SQL** für Attribute
- Konflikte in `conflicts[]` und ggf. `uncertainties[]` — nie stillschweigend mergen

---

## DAR Context Builder — geplante Integration

**Status:** Contract only — Implementierung später (ADR-0012).

```
User Query
    │
    ▼
context_assembly_pipeline     ← NEU (App, geplant)
    ├── analyze_query
    ├── derive required_fields + answer_structure
    ├── build context_array
    ├── source_resolution_router (ADR-0013)
    └── field-driven source queries (SQL → KP → Graph → RAG → Web)
    │
    ▼
context_assembly (Contract)   ← context_assembly.schema.json
    │
    ▼
context_builder                 ← Provider-Messages aus gefülltem Array
    │
    ▼
Provider → Validator → Inbox (optional)
```

**Keine neue Runtime** — Erweiterung von DAR `context_builder` / Pipeline (ADR-0010).

### Leitplanken (unverändert)

- ADR-0002: Regisseur-Inbox bleibt Freigabe-Hub
- ADR-0004: Keine Auto-Veröffentlichung
- ADR-0003: Playbooks SSOT für Regeln
- ADR-0009: Chroma abgeleitet, nicht kanonisch

---

## Contract-Artefakte

| Artefakt | Pfad |
|----------|------|
| Schema | `contracts/source-resolution/context_assembly.schema.json` |
| Beispiel | `examples/source-resolution/context_assembly.example.json` |
| Source Resolution | `contracts/source-resolution/source_resolution_policy.yaml` |

---

## Beispiel-Ablauf (kurz)

**Frage:** „CRM-Status Apotheke 12345 und Presseschau-Regeln?“

1. Felder: `crm_status` (mandatory, SQL), `presseschau_rules` (mandatory, KP)
2. SQL liefert Status → `crm_status: filled`
3. Playbook liefert No-Auto-Publish → `presseschau_rules: filled`
4. `ready_for_generation: true` → Provider erzeugt Antwort mit beiden Abschnitten

**Frage:** „CRM-Status Apotheke 99999?“ (nicht in DB)

1. SQL leer → `crm_status: missing`
2. Kein RAG-Ersatz für CRM-Fakt
3. `ready_for_generation: false`, `missing_mandatory_fields: ["crm_status"]`
4. Antwort: transparent „Kein CRM-Eintrag für 99999“ — **kein Raten**

---

## Verwandte Dokumente

- [12_architecture_layers.md](12_architecture_layers.md)
- [13_source_resolution.md](13_source_resolution.md)
- [04_ai_runtime.md](04_ai_runtime.md)
- [11_roadmap_stufen_a_f.md](11_roadmap_stufen_a_f.md)
