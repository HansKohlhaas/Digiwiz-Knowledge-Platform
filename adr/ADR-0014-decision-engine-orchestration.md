# ADR-0014: Decision Engine — Orchestrierung ohne Fachlogik im Code

## Status

Akzeptiert (2026-07-09)

## Metadaten

| Feld | Wert |
|------|------|
| Datum | 2026-07-09 |
| Scope | Stufe E4, DAR Pipeline |
| Artefakte | `contracts/decision-engine/`, `docs/14_decision_engine.md` |
| Verwandt | ADR-0003, ADR-0007, ADR-0010, ADR-0011, ADR-0012, ADR-0013 |

## Kontext

DAR orchestriert mehrere Schichten: Intent, Source Resolution, Context Assembly, Context Builder. Ohne explizite **Entscheidungsschicht** drohen:

- Quellenwahl ad hoc im App-Code statt aus KP-Contracts
- Widersprüchliche Interpretation von SQL-first, Graph und RAG
- Keine nachvollziehbare Begründung, warum eine Quelle aktiviert oder übersprungen wurde
- Vermischung von **Routing-Entscheidungen** mit **Antwortgenerierung**

ADR-0013 definiert **welche Quellen in welcher Reihenfolge** existieren. ADR-0011 definiert **wie** Context Assembly Felder sammelt. Es fehlt ein verbindlicher Schritt dazwischen: **welche Schritte und Quellen für diese konkrete Anfrage nötig sind**.

## Entscheidung

**Digiwiz führt eine Decision Engine als KP-Contract-Schicht ein (Stufe E4).**

Die Decision Engine:

1. **Entscheidet** über Quellenbedarf und Verarbeitungsschritte
2. **Erzeugt keine Antworten** und **führt keine Retrieval-Abfragen** aus
3. Enthält **keine fest codierten Fachregeln** — alle Entscheidungen werden aus KP-Artefakten **abgeleitet**
4. Liefert ein **maschinenlesbares Decision-Output** und **Decision-Trace** für Audit und Debugging

### Abgrenzung

| Komponente | Rolle | Antworten? | Fachregeln im Code? |
|------------|-------|------------|---------------------|
| **Intent Recognition** | Signale extrahieren (Domänen, Entitäten, Fragetyp) | ❌ | ❌ |
| **Decision Engine** | Quellen + Schritte + Gates ableiten | ❌ | ❌ |
| **Source Resolution** | Quellen gemäß Plan abfragen | ❌ | ❌ |
| **Context Assembly** | Context-Array füllen | ❌ | ❌ |
| **Context Builder** | Provider-Kontext bauen | ❌ | ❌ |
| **Provider** | Text generieren | ✅ | — |

### Regelquellen (SSOT)

| Quelle | Entscheidet über |
|--------|------------------|
| **Playbooks** | Task-spezifische Hinweise, Pflichtfelder, Freigabe, Domänen-Signale |
| **Contracts** | Sequenzen, Schemas, Schwellen, Reason-Codes |
| **ADRs** | Architekturgrenzen, Verbotene Pfade, SSOT-Hierarchie |
| **Source-Resolution-Policy** | SQL-first, kanonische Sequenz |
| **Context-Assembly-Contract** | Feldlogik, `ready_for_generation` |

### Pipeline-Position

```
Intent Recognition
        │
        ▼
Decision Engine          ← ADR-0014 (Stufe E4)
        │
        ▼
Source Resolution        ← ADR-0013
        │
        ▼
Context Assembly         ← ADR-0011
        │
        ▼
DAR Context Builder      ← ADR-0010/0011
        │
        ▼
Provider → Validator → Regisseur-Inbox
```

### Contracts (KP)

| Artefakt | Pfad |
|----------|------|
| Decision Policy | `contracts/decision-engine/decision_policy.yaml` |
| Input | `contracts/decision-engine/decision_input.schema.json` |
| Output | `contracts/decision-engine/decision_output.schema.json` |
| Trace | `contracts/decision-engine/decision_trace.schema.json` |
| Context (an Builder) | `contracts/decision-engine/decision_context.schema.json` |
| Doku | `docs/14_decision_engine.md` |
| Beispiele | `examples/decision-engine/` |

**Status:** contract_active · App-Implementierung app_planned (nach D4/D5 Contracts)

## Begründung

- Trennt **Entscheidung** von **Ausführung** und **Generierung**
- Alle Regeln bleiben in KP versionierbar und testbar (ADR-0007, ADR-0012)
- Decision Trace ermöglicht Audit ohne Log-Archäologie im Python-Code
- Erweiterbar für Stufe F (Policy-Contracts) ohne neue Runtime

## Konsequenzen

- Roadmap Stufe E: Meilenstein **E4 Decision Engine** (Contract ✅, App ⏳)
- `context_builder_input.schema.json` erhält optionales `decision_context_ref` — **kein Breaking Change**
- Implementierung in App als `decision_engine` Modul **nach** Contract-Tests
- Keine Auto-Veröffentlichung, keine Umgehung Regisseur-Inbox (ADR-0002, ADR-0004)

## Nicht-Ziele

- Keine LLM-Antworten in der Decision Engine
- Keine SQL-/Graph-/Chroma-Abfragen
- Keine Duplizierung der Source-Resolution-Sequenz — nur **Interpretation** und **Plan**
- Keine neue Runtime neben DAR (ADR-0010)

## Verwandte ADRs

- ADR-0010 — DAR einzige Runtime
- ADR-0011 — Context Assembly nach Entscheidung
- ADR-0013 — Source Resolution nach Entscheidung
- ADR-0012 — Contracts vor App-Automation

## Historie

| Version | Datum | Änderung |
|---------|-------|----------|
| 1 | 2026-07-09 | Decision Engine als KP-Contract, Stufe E4 |
