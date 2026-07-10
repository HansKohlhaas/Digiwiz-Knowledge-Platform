# Provider Data Boundary

Maschinenlesbarer Contract fuer die Uebertragung von Kontextfeldern an externe LLM-Provider.

## Contract

| Datei | Beschreibung |
|-------|--------------|
| `provider_data_policy.yaml` | Feldklassen, Feldregeln, Local-only-SQL-Modus, Audit |

## Standardregeln

- Sensible SQL-/CRM-Felder werden **nicht** an externe Provider gesendet (maskiert oder blockiert).
- Unbekannte Felder werden **blockiert**.
- Governance- und oeffentliche Playbook-Regeln duerfen uebertragen werden.
- Kundennummern, interne Notizen und personenbezogene Daten bleiben **lokal**.
- Freigabeentscheidungen werden protokolliert.

## Runtime

Konsumiert durch `digiwiki/ai_runtime/provider_context_sanitizer.py` (`sanitize_context_for_provider`).

Feature-Flag Local-only SQL: `DAR_KP_SQL_LOCAL_ONLY=1`

## Status

**contract_active / app_planned** (Phase 7E)
