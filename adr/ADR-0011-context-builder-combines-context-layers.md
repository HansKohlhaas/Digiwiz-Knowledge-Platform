# ADR-0011: Context Assembly before Answer Generation

## Status

Akzeptiert (2026-07-09, erweitert 2026-07-09)

## Metadaten

| Feld | Wert |
|------|------|
| Datum | 2026-07-09 |
| Scope | Stufe D/E, DAR Context Builder |
| Artefakte | `contracts/source-resolution/context_assembly.schema.json`, `schemas/context_builder_*.schema.json`, `docs/12_context_assembly_pipeline.md` |
| Verwandt | ADR-0002, ADR-0003, ADR-0004, ADR-0007, ADR-0009, ADR-0010, ADR-0013 |

## Kontext

DAR benötigt Kontext aus mehreren Quellen. Zwei Risiken ohne verbindliches Modell:

1. **Erster-Treffer-Antworten** — RAG oder SQL liefern ein Snippet, Provider halluziniert den Rest
2. **Quellenkonkurrenz** — Playbooks, SQL, Graph und Chroma ohne Feldlogik und Priorität

ADR-0013 definiert **welche Quelle wann** (Source Resolution). ADR-0011 definiert **wie** DAR Informationen **vor** der Antwortgenerierung sammelt: die **Context Assembly Pipeline**.

## Entscheidung

**Digiwiz erzeugt Antworten nicht direkt aus dem ersten Treffer.** DAR führt zuerst eine **Context Assembly Pipeline** aus:

```
Anfrage analysieren
    → Antwortziel + Antwortstruktur
    → required_fields ableiten
    → context_array aufbauen
    → Quellen sequenziell, feldgesteuert abfragen
    → fehlende/unsichere Felder → nächste Quellenstufe
    → Konflikte markieren
    → Validierung (Pflichtfelder)
    → erst dann Antwortgenerierung
```

### Context Builder Rolle

**`context_builder.py` (DAR)** bleibt die **einzige Kombinationsschicht** (ADR-0010). Sie wird um **`context_assembly_pipeline`** (App, geplant) erweitert:

| Phase | Modul (geplant) | Output |
|-------|-----------------|--------|
| Assembly | `context_assembly_pipeline` | `context_assembly.schema.json` |
| Provider-Kontext | `context_builder` | Provider-Messages aus gefülltem Array |
| Validierung | `response_validator` | Brandvoice, Regeln (Stufe B) |

**Keine neue Runtime.**

### Quellenreihenfolge (feldgesteuert, ADR-0013 aligned)

Pro Informationsfeld — nicht pauschal alle Quellen:

1. **SQL / CRM** — Unternehmensdaten, Stammdaten (System of Record)
2. **Knowledge Platform** — Regeln, Prozesse, Strukturen (SSOT)
3. **Knowledge Graph** — Beziehungen, Provenienz (Stufe E)
4. **Chroma / RAG** — semantischer, **abgeleiteter** Kontext
5. **Web / extern** — nur ergänzend, nie Ersatz für interne Wahrheit

**Nächste Stufe nur** für Felder mit Status `missing` oder `uncertain`.

### Pflichtregeln

- Pflichtfelder mit Status `missing` → `ready_for_generation: false` oder transparente Ausweisung — **kein Raten**
- Konflikte in `conflicts[]` dokumentieren; Winner gemäß ADR-0013 / `source_resolution_policy.yaml`
- **Kein** `published_url`, **kein** Auto-Publish (ADR-0004)
- Regisseur-Inbox unverändert (ADR-0002)

### Contract

Maschinenlesbar: `contracts/source-resolution/context_assembly.schema.json`

Pflichtfelder u. a.: `query`, `answer_goal`, `answer_structure`, `required_fields`, `context_array`, `missing_mandatory_fields`, `ready_for_generation`.

Beispiel: `examples/source-resolution/context_assembly.example.json`

### Output Context Builder (bestehend)

`context_builder_output.schema.json` bleibt gültig; Assembly-Output kann als **Vorgänger** oder eingebettete Phase an Provider-Kontext übergeben werden (Implementierungsdetail App, nicht breaking).

## Begründung

- Trennt **Informationssammlung** von **Textgenerierung** — reduziert Halluzinationen
- Feldgesteuerte Quellenabfrage vermeidet unnötiges RAG bei CRM-Fragen
- Transparente `missing_mandatory_fields` statt stiller Lücken
- Erweiterbar für Graph (E) ohne neue Runtime

## Konsequenzen

- Doku: [docs/12_context_assembly_pipeline.md](../docs/12_context_assembly_pipeline.md)
- Roadmap Stufe D: Meilenstein **D5 Context Assembly** (Contract ✅, App ⏳)
- ADR-0013 bleibt gültig für Quellen-Priorität; ADR-0011 definiert Assembly-Ablauf
- Implementierung in App inkrementell nach ADR-0012
- Keine Breaking Changes an Stufe A–D API

## Verwandte ADRs

- ADR-0002, ADR-0004 — Inbox, kein Auto-Publish
- ADR-0003 — Playbooks SSOT
- ADR-0009 — Chroma abgeleitet
- ADR-0010 — DAR einzige Runtime
- ADR-0012 — Contracts vor Automation
- ADR-0013 — Source Resolution, SQL-first

## Historie

| Version | Datum | Änderung |
|---------|-------|----------|
| 1 | 2026-07-09 | Context Builder kombiniert Schichten (Graph/RAG) |
| 2 | 2026-07-09 | Context Assembly Pipeline vor Antwortgenerierung; Contract `context_assembly.schema.json` |
