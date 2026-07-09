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

## Quellenreihenfolge (kanonisch — ADR-0013)

Identisch in ADR-0011, ADR-0013, `source_resolution_policy.yaml` und [13_source_resolution.md](13_source_resolution.md).

### Global (Pipeline-Schritte)

| Schritt | ID | Rolle |
|---------|-----|--------|
| 0 | `classify_intent` | SQL-first ja/nein — **immer zuerst** |
| 1 | `kp_governance` | Playbooks/ADRs/Contracts — **immer für DAR** (Regeln, nicht SQL-Fakten) |
| 2 | `sql_crm_stammdaten` | Operative Firmendaten bei SQL-first / Firmendaten-Feldern |
| 3 | `knowledge_graph` | Beziehungen, Provenienz (Stufe E) |
| 4 | `chroma_rag` | Semantik — **abgeleitet** |
| 5 | `web_external` | Nur ergänzend |

### Feldgesteuert (erste Quelle pro Feldtyp)

| Feldtyp | Erste Quelle |
|---------|--------------|
| CRM-Status, Kundennummer, Umsatzklasse, MSV3, … | **SQL** |
| Freigabe, Auto-Publish, Governance, Prozesse | **Knowledge Platform** |
| Beziehung Entität A → B, Provenienz-Kette | **Knowledge Graph** |
| Verfahren, Wiki-Formulierung, semantische Ähnlichkeit | **KP** → ggf. **Chroma/RAG** |
| Branchennews extern | **Web** (nie über SQL/KP für Firmendaten) |

**Regel:** Nächste Pipeline-Stufe nur für Felder mit Status `missing` oder `uncertain`.

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
