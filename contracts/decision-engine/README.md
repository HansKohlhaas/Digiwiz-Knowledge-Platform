# Decision Engine (Stufe E4)

Orchestrierungsentscheidungen **ohne Antwortgenerierung** und **ohne Retrieval**.

**Status:** **contract_active** · **app_planned** (Modul `decision_engine` in DAR)

**Verbindlich:** [ADR-0014](../../adr/ADR-0014-decision-engine-orchestration.md) · [docs/14_decision_engine.md](../../docs/14_decision_engine.md)

## Artefakte

| Datei | Rolle |
|-------|--------|
| [decision_policy.yaml](decision_policy.yaml) | Pipeline-Schritte, Reason-Codes, Gate-Logik |
| [decision_input.schema.json](decision_input.schema.json) | Input nach Intent Recognition |
| [decision_output.schema.json](decision_output.schema.json) | Quellenbedarf, Gates, Orchestration Plan |
| [decision_trace.schema.json](decision_trace.schema.json) | Audit-Log pro Entscheidungsschritt |
| [decision_context.schema.json](decision_context.schema.json) | Weitergabe an Source Resolution / Assembly / Context Builder |

## Pipeline-Position

```
Intent Recognition → Decision Engine → Source Resolution → Context Assembly → Context Builder
```

## Regelquellen (keine Fachlogik im Code)

| Quelle | Inhalt |
|--------|--------|
| Playbooks | `decision_hints` (optional) |
| Contracts | `decision_policy.yaml`, `source_resolution_policy.yaml`, Assembly/Merge |
| ADRs | Architekturgrenzen (ADR-0010, 0011, 0013, 0014) |

## Beispiele

`../../examples/decision-engine/`
