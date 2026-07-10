# Decision Engine — Architektur (Stufe E4)

**Stand:** 10.07.2026  
**Verbindlich:** [ADR-0014](../adr/ADR-0014-decision-engine-orchestration.md)  
**Contracts:** [contracts/decision-engine/](../contracts/decision-engine/)

## Kernaussage

Die **Decision Engine** entscheidet, **welche Wissensquellen und Verarbeitungsschritte** für eine Anfrage benötigt werden. Sie erzeugt **keine Antworten**, führt **keine Retrieval-Abfragen** aus und enthält **keine fest codierten Fachregeln**.

Alle Entscheidungen werden aus der Knowledge Platform abgeleitet:

- Playbooks
- Contracts
- ADRs
- Source-Resolution-Regeln
- Context-Assembly-Regeln

---

## 1. Decision Pipeline

Die Engine durchläuft **intern** diese Schritte (Orchestrierungsentscheidung, keine Datenabfrage):

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. validate_input          Decision Input Contract prüfen       │
│ 2. resolve_task_routing    task → playbooks (runtime/routing)   │
│ 3. load_rule_stack         decision_policy + source_resolution  │
│ 4. load_playbook_hints     governance, rules, decision_hints    │
│ 5. consume_intent_signals  Intent Recognition Ergebnis nutzen   │
│ 6. derive_source_requirements  SQL/Graph/Chroma/Web/KP        │
│ 7. derive_required_fields  aus Playbook + Query + Intent        │
│ 8. evaluate_governance_gates Freigabe, Klärung, Block           │
│ 9. build_orchestration_plan  geordnete Schritte für Downstream  │
│10. assess_readiness        answer / clarification / approval    │
│11. emit_output             decision_output + trace + context     │
└─────────────────────────────────────────────────────────────────┘
```

**Ausgabe:** Plan für Source Resolution und Context Assembly — **kein** Provider-Kontext, **kein** generierter Text.

---

## 2. Decision Contract

### Input (`decision_input.schema.json`)

| Feld | Pflicht | Beschreibung |
|------|---------|--------------|
| `query` | ✅ | Original-User-Anfrage |
| `task` | ✅ | DAR-Task (z. B. `presseschau`) |
| `intent_classification` | ✅ | Signale aus Intent Recognition |
| `routing_ref` | ✅ | Verweis auf `runtime/routing.json` |
| `decision_policy_ref` | ✅ | `contracts/decision-engine/decision_policy.yaml` |
| `resolution_policy_ref` | ✅ | `contracts/source-resolution/source_resolution_policy.yaml` |
| `playbook_refs` | ✅ | Aus Routing abgeleitete Playbooks |
| `session_id` | ❌ | Session-Kontext |
| `user_context` | ❌ | Rolle, Mandant, CRM-Kontext (ohne Rohdaten-SSOT) |

**Intent Classification (Input-Signale, keine Entscheidung):**

```json
{
  "sql_first_signals": ["kundennummer", "crm_status"],
  "domain_matches": ["apothekenbezug"],
  "query_type": "operational_lookup",
  "entity_refs": [{ "type": "kundennummer", "value": "12345" }],
  "confidence": 0.92
}
```

### Output (`decision_output.schema.json`)

| Feld | Beschreibung |
|------|--------------|
| `decision_id` | Eindeutige Entscheidungs-ID |
| `source_requirements` | Pro Quelle: `required` \| `optional` \| `skipped` + `reason_code` |
| `decisions` | Aggregierte Booleans (siehe Abschnitt 5) |
| `orchestration_plan` | Geordnete Downstream-Schritte |
| `required_fields` | An Context Assembly weitergegeben |
| `governance` | `approval_required`, `clarification_required`, … |
| `readiness` | `answer_generation_allowed`, `ready_for_source_resolution` |
| `decision_confidence` | Gesamt + pro Quelle |
| `decision_trace_id` | Verweis auf Trace |

---

## 3. Decision Context (an DAR Context Builder / Downstream)

`decision_context.schema.json` ist die **schlanke Weitergabe** an Source Resolution, Context Assembly und Context Builder:

| Feld | Zweck |
|------|--------|
| `decision_id` | Korrelation |
| `task`, `query` | Kontext |
| `sql_first` | ADR-0013 Klassifikation (aus Decision abgeleitet) |
| `source_requirements` | Welche Quellen aktiv |
| `orchestration_plan` | Schrittfolge |
| `required_fields` | Feldgesteuerte Assembly |
| `governance` | Gates vor Generierung |
| `policy_refs` | Nachvollziehbarkeit |
| `next_stage` | `source_resolution` \| `clarification` \| `approval_gate` \| `block` |

**Integration Context Builder:** optionales Feld `decision_context_ref` in `context_builder_input.schema.json` (kein Breaking Change).

---

## 4. Decision Rules — Aufteilung

### In Playbooks (task-spezifisch)

Optionaler Block `decision_hints` (YAML, `additionalProperties` erlaubt):

```yaml
decision_hints:
  default_query_type: content_preparation
  sql_first_when_entities: [kundennummer, apotheken_id]
  preferred_sources: [knowledge_platform, chroma_rag]
  required_field_templates:
    - field_id: presseschau_no_auto_publish
      mandatory: true
      preferred_sources: [knowledge_platform]
  clarification_triggers:
    - missing_entity: kundennummer
      when_query_type: operational_lookup
```

| Regeltyp | Beispiel |
|----------|----------|
| Domänen-Signale | `sql_first_when_entities` |
| Quellenpräferenz | `preferred_sources` |
| Pflichtfelder | `required_field_templates` |
| Klärungsbedarf | `clarification_triggers` |
| Freigabe | `governance.approval_required` (bestehend) |

### In Contracts (maschinenlesbar)

| Contract | Regeln |
|----------|--------|
| `decision_policy.yaml` | Pipeline-Schritte, Reason-Codes, Gate-Logik |
| `source_resolution_policy.yaml` | Kanonische Sequenz, SQL-first-Domänen |
| `context_assembly.schema.json` | Feldstatus, `ready_for_generation` |
| `merge_policy.yaml` | Graph↔RAG nach Resolution |
| Schemas | Pflichtfelder, Enums, Validierung |

### In ADRs (Architekturgrenzen)

| ADR | Regel |
|-----|-------|
| ADR-0010 | Keine zweite Runtime; Decision Engine ist Planungsschicht in DAR |
| ADR-0013 | SQL-first für Firmendaten; KP-Governance immer |
| ADR-0011 | Keine Antwort ohne Assembly |
| ADR-0004 | Kein Auto-Publish aus Entscheidung |
| ADR-0009 | Chroma nie SSOT; Graph für Struktur |
| ADR-0014 | Keine Fachlogik im Code |

---

## 5. Decision Output — mögliche Entscheidungen

Aggregiert im Objekt `decisions`:

| Entscheidung | Bedeutung |
|--------------|-----------|
| `sql_required` | SQL/CRM-Abfrage im Plan |
| `sql_not_required` | Kein SQL-first (explizit dokumentiert) |
| `kp_governance_required` | Immer `true` für DAR-Tasks |
| `knowledge_graph_required` | Graph-Abfrage im Plan |
| `chroma_required` | RAG-Abfrage im Plan |
| `web_required` | Web-Ergänzung im Plan |
| `answer_generation_allowed` | Downstream darf Provider aufrufen |
| `clarification_required` | Rückfrage an User vor Fortsetzung |
| `approval_required` | Regisseur-Freigabe vor externer Wirkung |
| `block_execution` | Pipeline stoppen (Governance-Verstoß) |

**Hinweis:** `sql_required` und `sql_not_required` schließen sich gegenseitig aus; beide müssen im Trace begründet sein.

---

## 6. Decision Trace

Maschinenlesbar: `decision_trace.schema.json`

```json
{
  "trace_id": "tr-dec-presseschau-001",
  "decision_id": "dec-presseschau-001",
  "engine_version": "contract_v1",
  "entries": [
    {
      "step_id": "derive_source_requirements",
      "timestamp": "2026-07-09T21:00:00Z",
      "rule_ref": "contracts/source-resolution/source_resolution_policy.yaml#sql_first_domains",
      "rule_type": "contract",
      "input_signals": { "domain_matches": ["kundennummer"] },
      "outcome": "sql_required",
      "confidence": 0.95,
      "rationale": "Domänen-Match kundennummer → SQL-first Pflicht",
      "source_effect": { "sql_crm_stammdaten": "required" }
    }
  ]
}
```

Jeder Trace-Eintrag **muss** `rule_ref`, `rule_type`, `outcome` und `rationale` enthalten.

---

## 7. Decision Confidence

Struktur in `decision_output.decision_confidence`:

```json
{
  "overall": 0.88,
  "sources": [
    {
      "source_id": "sql_crm_stammdaten",
      "decision": "required",
      "confidence": 0.95,
      "reason_code": "domain_match_kundennummer",
      "evidence_refs": [
        "contracts/source-resolution/source_resolution_policy.yaml#sql_first_domains",
        "intent_classification.entity_refs"
      ],
      "rejected_alternatives": [
        {
          "source_id": "chroma_rag",
          "reason_code": "sql_first_overrides_rag_for_operational_facts",
          "adr": "ADR-0013"
        }
      ]
    }
  ]
}
```

**Reason-Codes** sind in `decision_policy.yaml` definiert — nicht im App-Code hardcodiert.

---

## 8. Integration in DAR

```
┌──────────────────┐
│ User Query       │
└────────┬─────────┘
         ▼
┌──────────────────┐     Signale: Entitäten, Domänen, query_type
│ Intent           │     (keine Quellenentscheidung)
│ Recognition      │
└────────┬─────────┘
         │ intent_classification
         ▼
┌──────────────────┐     Liest: Playbooks, Policies, ADRs
│ Decision Engine  │──── Output: decision_output, decision_trace
│ (E4 Contract)    │     Context: decision_context
└────────┬─────────┘
         │ orchestration_plan + source_requirements
         ▼
┌──────────────────┐     Führt Abfragen aus (ADR-0013)
│ Source           │
│ Resolution       │
└────────┬─────────┘
         │ Snippets, resolution_path
         ▼
┌──────────────────┐     Baut context_array (ADR-0011)
│ Context          │
│ Assembly         │
└────────┬─────────┘
         │ context_assembly + required_fields filled
         ▼
┌──────────────────┐     Provider-Messages (ADR-0010/0011)
│ DAR Context      │
│ Builder          │
└────────┬─────────┘
         ▼
    Provider → Validator → Inbox
```

| Übergabe | Von → Nach | Artefakt |
|----------|------------|----------|
| Signale | Intent → Decision | `intent_classification` in Input |
| Plan | Decision → Source Resolution | `decision_context.orchestration_plan` |
| Felder | Decision → Context Assembly | `decision_context.required_fields` |
| Kontext | Decision → Context Builder | `decision_context_ref` (optional) |
| Audit | Decision → Telemetry | `decision_trace` |

---

## Status

| Aspekt | Status |
|--------|--------|
| ADR-0014 | ✅ |
| Contracts + Beispiele | ✅ KP v1.5.0 |
| App-Modul `decision_engine` | ⏳ geplant |
| Integration D4/D5/E3 | ⏳ nach Contract-Tests |

Siehe auch: [13_source_resolution.md](13_source_resolution.md) · [12_context_assembly_pipeline.md](12_context_assembly_pipeline.md) · [11_roadmap_stufen_a_f.md](11_roadmap_stufen_a_f.md)
