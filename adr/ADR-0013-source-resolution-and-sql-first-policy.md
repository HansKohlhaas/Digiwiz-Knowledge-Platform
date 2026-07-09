# ADR-0013: Source Resolution and SQL-first Policy

## Status

Akzeptiert (2026-07-09)

## Metadaten

| Feld | Wert |
|------|------|
| Datum | 2026-07-09 |
| Scope | Stufe D/E, Wiki, DAR Context Builder |
| Artefakte | `contracts/source-resolution/`, `docs/13_source_resolution.md`, `schemas/context_builder_output.schema.json` (Erweiterung geplant) |
| Verwandt | ADR-0003, ADR-0007, ADR-0009, ADR-0010, ADR-0011 |

> **Hinweis:** ADR-0010 ist bereits „DAR als einzige AI Runtime“. Source Resolution ist **ADR-0013**.

## Kontext

Digiwiz vereint mehrere Wissensquellen: **SQL/CRM-Stammdaten**, Knowledge Platform (Playbooks/Contracts), Knowledge Graph, Chroma/RAG und externe Web-Quellen.

Ohne verbindliche **Source-Resolution-Sequenz** drohen:

- RAG/Chroma-Antworten statt verbindlicher CRM-Fakten (falsche Kundennummern, Status, Umsatzklassen)
- Halluzinationen bei firmenspezifischen Stammdaten
- Widersprüchliche Antworten zwischen Wiki-Index und operativer Datenbank
- Context Builder ohne klare Priorität bei Konflikten

## Entscheidung

**Bei jeder Wissensabfrage prüft DAR (bzw. ein vorgelagerter Source-Resolution-Schritt) zuerst, ob die Anfrage eine direkte SQL-/CRM-/Unternehmensdaten-Abfrage ist.**

### Verbindliche Auflösungssequenz (kanonisch)

```
0. classify_intent          → SQL-first ja/nein (Pflicht)
1. kp_governance            → Playbooks + ADRs + Contracts (Pflicht für DAR-Tasks)
2. sql_crm_stammdaten       → bei SQL-first / Firmendaten-Feldern
3. knowledge_graph          → Beziehungen, Provenienz (Stufe E)
4. chroma_rag               → semantisch, abgeleitet
5. web_external             → nur ergänzend
```

**Klarstellung KP vs. SQL:**

| Aspekt | KP (Schritt 1) | SQL (Schritt 2) |
|--------|----------------|-----------------|
| Rolle | **Governance-Prüfung immer** — Regeln, Freigabe, Prozesse | **Operative Fakten** — Stammdaten, CRM |
| SSOT für | Playbooks, ADRs, Contracts | Firmendaten |
| Nicht | SQL-Fakten ersetzen | KP-Regeln ersetzen |

**Feldgesteuert (Context Assembly, ADR-0011):** Pro `required_field` bestimmt `preferred_sources[]` die **erste** Datenquelle — konsistent mit obiger Sequenz, aber nicht jede Stufe für jedes Feld.

Maschinenlesbar: `canonical_sequence` und `field_first_source` in `source_resolution_policy.yaml`.

### SQL-first-Pflichtdomänen

Die **eigene SQL-Datenbank hat Vorrang**, wenn die Anfrage sich bezieht auf:

- Hersteller, Vertreiber, Apothekenbezug
- Ansprechpartner, CRM-Status, Kundennummern
- Segmentierung, Umsatzklassen, Vertriebskanäle, Nielsengebiete
- MSV3-Status, Sortiments-/Produktbezug
- Historien, Freigaben, interne Bewertungen
- firmenspezifische Notizen, operative Stammdaten

Maschinenlesbar: `contracts/source-resolution/source_resolution_policy.yaml`

### Konfliktregeln (Kurzform)

| Konflikt | Führend |
|----------|---------|
| SQL vs. Chroma/RAG (Firmendaten) | **SQL** |
| SQL vs. Web (Firmendaten) | **SQL** |
| KP-Contract vs. Chroma/RAG | **KP** (ADR-0009) |
| Graph vs. SQL (Attribut/Fakt) | **SQL** |
| Graph vs. Chroma (Beziehung vs. Textähnlichkeit) | **Graph** für Struktur, **Chroma** für Passagen — merge per Policy |
| Regeln/Freigabe vs. beliebige Quelle | **Playbooks/ADRs** (KP) |

### DAR Context Builder (geplant)

ADR-0011 wird durch ADR-0013 **erweitert**, nicht ersetzt:

1. **`source_resolution_router`** (App, geplant) — Klassifikation + Routing
2. **`context_builder`** — Merge gemäß Sequenz; Output dokumentiert `resolution_path[]`, `sql_snippets[]`, `uncertainties[]`
3. Kein Auto-Publish; Regisseur-Inbox unverändert (ADR-0002, ADR-0004)

Details: [docs/13_source_resolution.md](../docs/13_source_resolution.md)

### Was nicht entschieden wird

- Keine SQL-Implementierung oder Schema-Migration in dieser ADR
- Kein Ersatz des bestehenden `ask_wiki.py`-Pfads — Einordnung folgt separater Klärung (Audit P1)
- Keine Web-Scraping-Pipeline in KP

## Begründung

- Operative Wahrheit für Vertrieb/CRM liegt in SQL — RAG über Wiki/MD ist dafür unzuverlässig
- KP bleibt SSOT für **Regeln**; SQL bleibt SSOT für **Stammdaten**
- Chroma und Graph bleiben Kontextlieferanten, keine Entscheidungssysteme
- Einheitliche Sequenz verhindert konkurrierende Wissensquellen

## Konsequenzen

- Neuer Contract-Ordner `contracts/source-resolution/`
- `contracts/retrieval/` verweist auf Source Resolution (Merge nach Schritt 2–4)
- Roadmap Stufe D: Unterpunkt „Source Resolution (D4)“ geplant
- `context_builder_output.schema.json` — optionale Felder `resolution_path`, `sql_snippets` (Contract-Erweiterung v1.2.0, Implementierung später)
- Keine Breaking Changes an Stufe A–D API-Pfaden

## Verwandte ADRs

- ADR-0003 — Playbooks SSOT (Regeln)
- ADR-0009 — Chroma abgeleitet, KP bei Konflikt
- ADR-0010 — DAR einzige AI Runtime
- ADR-0011 — Context Builder (wird um SQL-first erweitert)
- ADR-0012 — Contracts vor Automation
