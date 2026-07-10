# ADR-0015: Provider Data Boundary

## Status

Akzeptiert (2026-07-10)

## Metadaten

| Feld | Wert |
|------|------|
| Datum | 2026-07-10 |
| Scope | Stufe D/E, DAR KP-Pipeline Phase 7E |
| Artefakte | `contracts/provider/provider_data_policy.yaml`, `docs/16_provider_data_boundary.md` |
| Verwandt | ADR-0011, ADR-0013, ADR-0014, ADR-0004, ADR-0007 |

## Kontext

Die DAR KP-Pipeline (Context Assembly → Provider Gate → Context Builder → externer LLM-Provider) kann operative CRM-/SQL-Daten, Governance-Regeln, RAG-Snippets und Graph-Provenienz zusammenführen.

Ohne verbindliche **Provider Data Boundary** drohen:

- Übertragung von Kundennummern, CRM-Status und personenbezogenen Daten an externe Cloud-LLMs
- Leckage interner Notizen oder unklassifizierter Felder in Provider-Prompts
- Unnachvollziehbare Freigaben sensibler Kontextteile
- Widerspruch zwischen Field Source Policy (Quellenauflösung) und Provider-Übertragung

Phase 7D hat gezeigt: E2E-Tests mit echtem Provider sind möglich — aber nur mit synthetischen Daten und ohne TLS-Umgehung. Phase 7E bereitet kontrollierte Tests mit echter read-only SQL vor, ohne CRM-Rohwerte an Provider zu senden.

## Entscheidung

**Vor jedem externen Provider-Aufruf sanitisiert DAR den Kontext gemäß `provider_data_policy.yaml`.**

### Verbindliche Regeln

1. **Standard:** Sensible SQL-/CRM-Felder werden **nicht** an externe Provider übertragen (maskiert oder blockiert).
2. **Unbekannte Felder** werden blockiert (Default: `unknown_field_action: block`).
3. **Governance- und öffentliche Playbook-Regeln** dürfen übertragen werden.
4. **Kundennummern, interne Notizen, Ansprechpartner-/Personendaten** bleiben lokal.
5. **Freigabeentscheidungen** (allow / mask / block / pseudonymize) werden protokolliert (`audit` in Policy).
6. **Das ursprüngliche Context Assembly** wird nicht verändert — Sanitierung erzeugt eine separate Provider-Message-Kopie.
7. **TLS-Umgehung (`verify=False`)** ist verboten; Zertifikatsfehler führen zu kontrolliertem Abbruch.

### Local-only SQL Test Mode

Mit `DAR_KP_SQL_LOCAL_ONLY=1`:

- Read-only SQL darf lokal ausgeführt werden (Context Assembly validiert Ergebnisse).
- SQL-Werte werden **nicht** an den Provider übergeben.
- Provider erhält nur neutrale Struktur (`[LOCAL_VALIDATED:field_present]`) oder wird nicht aufgerufen.
- Telemetrie, Memory und Inbox enthalten keine sensiblen Rohdaten.

### Maschinenlesbarer Contract

`contracts/provider/provider_data_policy.yaml` definiert je Feldklasse und `field_id`:

| Dimension | Beschreibung |
|-----------|--------------|
| `external_provider_transfer` | Darf an externen Provider |
| `local_processing_only` | Nur lokale Verarbeitung |
| `action` | allow / mask / block / local_only_neutral |
| `pseudonymize` | Stabile Pseudonym-Referenz statt Rohwert |
| `max_data_depth` | none / summary / full |
| `allowed_purpose` | content_generation, governance_hint, local_validation |
| `allowed_provider_classes` | external_llm, mock, local_only |
| `require_explicit_approval` | Explizite Freigabe erforderlich |

### Runtime (Digiwiz App)

| Modul | Funktion |
|-------|----------|
| `provider_context_sanitizer.py` | `sanitize_context_for_provider()` |
| `provider_tls.py` | TLS-Guard, kein `verify=False` |
| `contracts/provider_data_policy.py` | Policy-Loader |
| `kp_pipeline.py` | Sanitizer vor Provider-Aufruf |

## Konsequenzen

### Positiv

- Kontrollierter Übergang zu echter SQL-DB mit unkritischer Testfirma (Phase 7E → 7F)
- Nachvollziehbare Audit-Spur in `provider_sanitization` Meta
- Klare Trennung: Assembly (vollständig lokal) vs. Provider-Kontext (gefiltert)

### Negativ / Aufwand

- Provider-Antworten enthalten keine operativen CRM-Fakten — Generierung basiert auf Governance + neutraler Struktur
- Zusätzlicher Pipeline-Schritt (`provider_sanitizer`) vor Provider-Aufruf
- Policy-Pflege synchron zu `field_source_policy.yaml`

## Nicht-Ziele

- Keine produktive Aktivierung der KP-Pipeline (weiterhin Feature-Flags)
- Keine Ersetzung der Field Source Policy bei Quellenauflösung
- Keine Auto-Veröffentlichung (ADR-0004 bleibt gültig)
