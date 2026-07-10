# Changelog

Format basiert auf [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added

- DAR App Phase 0 (Monorepo): `knowledge_paths` Contract-Pfade, `kp_loader`, `schema_validator`, `policy_refs`, Tests T0–T2 — siehe `docs/15_dar_app_integration_plan.md`
- DAR App Phase 1 (Monorepo): Intent Recognition Dry-Run (`intent_recognition`, `intent_adapter`), Tests T3 — noch nicht in Pipeline
- DAR App Phase 2 (Monorepo): Decision Engine Dry-Run (`decision_engine`), Tests T4 — keine Retrieval-Ausführung
- DAR App Phase 3 (Monorepo): Source Resolution Dry-Run (KP + SQL/CRM), Tests T5 — Feature-Flag `DAR_KP_SOURCE_RESOLUTION`
- DAR App Phase 4 (Monorepo): Context Assembly Dry-Run + Provider-Gate (`context_assembly_pipeline`, `darf_provider_aufgerufen_werden`), Tests T6/T7 — Feature-Flag `DAR_KP_CONTEXT_ASSEMBLY`; SQL-Adapter `ist_readonly_select()` Guard
- DAR App Phase 5 (Monorepo): Chroma/RAG-Adapter + Merge (`chroma_rag_adapter`, `rag_merge`), Router-Eskalation — Feature-Flag `DAR_KP_CHROMA_RAG`
- DAR App Phase 6 (Monorepo): Knowledge Graph Stub-Adapter (`graph_query_adapter`, `InMemoryGraphStore`), Tests — Feature-Flag `DAR_KP_KNOWLEDGE_GRAPH`
- DAR App Phase 7B (Monorepo): End-to-End KP-Pipeline hinter `DAR_KP_PIPELINE` — `kp_pipeline.py`, zentrales `provider_gate`, optionale Runtime-Response-Felder; baut auf Phase-7A-Guards auf
- DAR App P0 (Monorepo): Policy-Redaction, KP-Stufen-Exception-Handling, Graph-Testmodus-Gate, vereinheitlichtes Provider-Gate
- DAR App Phase 7C (Monorepo): kontrollierter manueller Schaltertest — `scripts/run_phase_7c_manual_test.py`, Bericht `reviews/manual_test_dar_kp_phase_7c.md`
- DAR App Phase 7D (Monorepo): E2E mit echtem Provider (OpenAI), synthetische Mock-SQL — `scripts/run_phase_7d_real_provider_test.py`, Bericht `reviews/manual_test_dar_kp_phase_7d_real_provider.md`
- DAR App Phase 7E (Monorepo): Provider Data Boundary — `contracts/provider/provider_data_policy.yaml`, `provider_context_sanitizer.py`, TLS-Härtung, `DAR_KP_SQL_LOCAL_ONLY`

## [1.5.3] - 2026-07-10

### Added

- `contracts/provider/provider_data_policy.yaml` — maschinenlesbare Provider Data Boundary je Feldklasse (übertragbar, lokal, maskiert, pseudonymisiert, Freigabe, Datentiefe, Zweck, Provider-Klasse).
- DAR App Phase 7E: `sanitize_context_for_provider()`, TLS-Guard (`verify=False` verboten), Local-only-SQL-Modus `DAR_KP_SQL_LOCAL_ONLY=1`.

### Changed

- Phase-7D-SSL-Bypass entfernt; TLS nur mit gültiger Zertifikatskette.
- KP-Pipeline sanitisiert Provider-Kontext vor externem Aufruf; CRM-/SQL-Werte standardmäßig nicht an externe Provider.

## [1.5.2] - 2026-07-10

### Added

- `contracts/source-resolution/field_source_policy.yaml` — kanonische Field-Source-Policy je `field_id` mit kanonischer Quelle, erlaubten Ergänzungsquellen, verbotenen Ersatzquellen, Eskalationsbedingungen, Konfliktregel, Provenienzpflicht, Mindest-Confidence und Redaction-Metadaten.
- DAR App Phase 7A Verweise: globaler Schalter `DAR_KP_PIPELINE`, zentrales Provider-Gate, Field-Source-Contract-Konsum und Privacy-Minimum — keine produktive KP-Pipeline-Aktivierung.

### Changed

- `meta/manifest.yaml`, ADR-0011, ADR-0013, Source-Resolution-Doku und Integrationsplan verweisen auf den Field-Source-Contract.
- `chroma_index_manifest.example.json` auf KP-Version `1.5.2` aktualisiert.

## [1.5.1] - 2026-07-10

### Added

- `decision_shared.schema.json` — gemeinsame Teilstrukturen (`source_requirements`, `required_fields`, `reason_code` enum)
- Decision-Beispiele: `clarification`, `block`, `approval_gate`
- `context_assembly` — `decision_id`, `decision_context_ref`, `source_requirements_planned`
- `decision_policy.yaml` — `playbook_hints_fallback`, `optional_source_escalation`, fehlende Reason-Codes

### Changed

- `decision_output` — `provider_call_allowed: false` Pflicht; `downstream_answer_possible` statt irreführendem `answer_generation_allowed`
- `readiness.answer_generation_allowed_after_context_assembly` — klare Semantik
- `reason_code` validiert gegen Policy-Katalog (enum in `decision_shared`)
- `decision_context.policy_refs` — `decision_output_ref`, `decision_trace_ref`
- `playbook.schema.json` — `decision_hints` enger typisiert
- Tests — Reason-Code-Katalog, Output/Context-Sync, Negativbeispiele, Assembly-Verknüpfung

## [1.5.0] - 2026-07-10

### Added

- **ADR-0014:** Decision Engine — Orchestrierung ohne Fachlogik im Code (Stufe E4)
- `contracts/decision-engine/` — Policy, Input/Output/Trace/Context Schemas
- `examples/decision-engine/` — Presseschau SQL-first Beispiel (Input, Output, Trace, Context)
- `docs/14_decision_engine.md` — Architektur (Pipeline, Contracts, Integration)
- `playbooks/presseschau.yaml` — optionales `decision_hints` (ADR-0014)
- `schemas/playbook.schema.json` — `decision_hints` (optional, nicht breaking)
- `schemas/context_builder_input.schema.json` — optionales `decision_context_ref`

### Changed

- Roadmap Stufe E — Meilenstein **E4 Decision Engine** (Contract ✅, App ⏳)
- `meta/manifest.yaml` — Contract-Typ `decision_engine`
- `adr/README.md` — ADR-0014 Index

## [1.4.1] - 2026-07-09

### Added

- Statusmodell **contract_active / app_planned / app_active** in `meta/manifest.yaml`, `contracts/README.md`, `docs/10_contracts.md`
- `context_assembly.schema.json` — `canonical_sequence_ref`, `classification.steps_completed` (Pflicht: `classify_intent`, `kp_governance`)
- `context_builder_output.schema.json` — ADR-0013-Felder Pflicht; Profil `dar_context_builder_output_v1_4`

### Changed

- Roadmap Übersicht — Stufe-D-Zeile Spalten korrigiert; Contract vs. App Status getrennt
- `contracts/README.md` — v1.4.0, Graph/Merge als contract_active
- ADR-0008 — Graph Query Contract statt „Format TBD“
- ADR-0009 — Merge Policy v1 aktiv, nicht mehr „geplant“
- `chroma_index_manifest.example.json` — `knowledge_platform_version: 1.4.1`
- `contracts/graph/README.md`, `contracts/retrieval/README.md` — Contract/App-Status

## [1.4.0] - 2026-07-09

### Added

- Kanonische Source-Resolution-Sequenz (`classify` → `kp_governance` → feldgesteuert SQL/Graph/RAG/Web) in ADR-0011, ADR-0013, Policy, Docs
- `context_builder_input.schema.json` — `sql_first`, `required_fields`, `resolution_policy_ref`, `context_assembly_ref`
- `examples/runtime/context_builder_input.example.json`
- `contracts/graph/graph_query.schema.json` + `examples/graph/` (Node, Edge, Query)
- `examples/retrieval/chroma_rebuild_report.example.json`
- `contracts/retrieval/merge_policy.yaml` v1 (Token-Limits, Provenienz, Konflikte)

### Changed

- `context_builder_output.example.json` — ADR-0013-Felder (`sql_first`, `resolution_path`, `sql_snippets`)
- Roadmap Stufe D — Basis (D1–D3) vs. D4/D5 geplant
- ADR-0009 — Verweis auf Merge-Policy v1
- Tests — Sequenz-Konsistenz, Input-Contract, Merge-Policy, Graph-Query, Chroma-Rebuild

## [1.3.0] - 2026-07-09

### Added

- **ADR-0011 v2:** Context Assembly Pipeline — Antwort erst nach internem Context-Array
- `docs/12_context_assembly_pipeline.md` — 10-Schritte-Pipeline, feldgesteuerte Quellenabfrage
- `contracts/source-resolution/context_assembly.schema.json` — Contract für Assembly-Output
- `examples/source-resolution/context_assembly.example.json`

### Changed

- ADR-0011 — Titel und Inhalt: *Context Assembly before Answer Generation*
- `meta/manifest.yaml` — Contract-Typ `context_assembly`
- Roadmap Stufe D — Meilenstein **D5 Context Assembly**

## [1.2.0] - 2026-07-09

### Added

- **ADR-0013:** Source Resolution and SQL-first Policy
- `docs/13_source_resolution.md` — verbindliche Auflösungssequenz, Entscheidungsregeln, Konflikte, DAR-Integration (geplant)
- `contracts/source-resolution/source_resolution_policy.yaml` — maschinenlesbare SQL-first-Domänen und Konfliktregeln
- `examples/source-resolution/` — Beispiele SQL-first, Chroma/RAG, Knowledge Graph
- `context_builder_output.schema.json` — optionale Felder `sql_first`, `resolution_path`, `sql_snippets`, `conflicts`

### Changed

- ADR-0011 — Erweiterung um SQL-first-Schicht (Verweis ADR-0013)
- `adr/README.md` — ADR-0013, erweiterte Leitplanke SQL vs. Chroma
- `docs/12_architecture_layers.md`, `docs/04_ai_runtime.md`, Roadmap — Source Resolution Querschnitt
- `contracts/retrieval/README.md` — Abgrenzung zu `source-resolution/`

## [1.1.0] - 2026-07-09

### Added

- ADR-0010: DAR als einzige AI Runtime
- ADR-0011: Context Builder kombiniert kanonisch + Graph + RAG
- ADR-0012: Contracts vor E/F-Automation
- `docs/12_architecture_layers.md` — Schichtenmodell KP / DAR / Graph / Chroma
- Contract-Schemas: Runtime-Output, API-Fehler, Knowledge Graph Node/Edge, Context Builder, Chroma Manifest/Rebuild, Playbook-Governance, LinkedIn
- Beispiele: `examples/linkedin/`, `examples/retrieval/`, `examples/runtime/`
- Einheitliche `governance`-Metadaten in allen Playbooks
- `tests/test_governance.py` — Schema-, YAML- und Governance-Validierung
- `cursor/CURSOR_TASK_STAGE_E.md`, `cursor/CURSOR_TASK_STAGE_F.md`
- Operative Matrix in `docs/11_roadmap_stufen_a_f.md`

### Changed

- `docs/04_ai_runtime.md` — explizite DAR-Definition und Abgrenzung
- `docs/10_contracts.md` — Runtime- und Context-Contract-Katalog

## [1.0.0] - 2026-07-09

### Added

- Initiales Knowledge-Platform-Repo im Digiwiz-Monorepo (`knowledge-platform/`)
- Playbooks: presseschau, linkedin, brandvoice, sources, image, wordpress, seo
- Content: `linkedin-presseschau.md` (kanonisch)
- Schema: `agent-lieferung.v3.json`
- Runtime: `routing.json` (aus Stufe D)
- ADR-0001 bis ADR-0005
- ADR-0006: Kein Git-Submodule bis nach Stufe E — lose Kopplung über `DIGIWIZ_KNOWLEDGE_ROOT`
- ADR-0007: Verträge (Contracts) als verbindliche Artefakte
- ADR-0008: Knowledge Graph als KP-Erweiterung, keine neue Runtime (Stufe E)
- ADR-0009: Knowledge Graph + Chroma/RAG — Rollen, DAR Context Builder kombiniert beides
- `adr/README.md` — ADR-Index
- `contracts/retrieval/` — Retrieval-Policy-Platzhalter (keine Chroma-Implementierung)
- `docs/11_roadmap_stufen_a_f.md` — Roadmap A–F inkl. Dual-Repo-Synchronisation
- Manifest `meta/manifest.yaml`, VERSION 1.0.0
- Verfahrensdoku migriert aus `docs/wiki/verfahren/`
- Digiwiz App: `knowledge_paths.py` + `knowledge_lock.json` (Fallback-kompatibel)

### Notes

- Keine Breaking Changes — Legacy-Pfade in `firmenapp/config/` bleiben als Fallback
- Stufe E (Knowledge Graph) bewusst nicht enthalten
