# ADR-0007: Verträge (Contracts) als verbindliche Artefakte

## Status

Akzeptiert (2026-07-09)

## Kontext

Die Knowledge Platform wurde zunächst als Dokumentations- und Regel-Repository aufgebaut. Langfristig soll sie jedoch **nicht nur Dokumente**, sondern **maschinenlesbare Verträge** bereitstellen — die verbindliche Quelle für Regeln und Schnittstellen zwischen Knowledge Platform und Digiwiz App (sowie externen Agenten).

Bisherige SSOT-Fokussierung (ADR-0003) betonte Playbooks. Das reicht als Leitbild nicht aus.

## Entscheidung

Die Knowledge Platform ist die **kanonische Contract-Quelle** für:

| Vertragstyp | Zweck | Ort (kanonisch) | Status v1.0 |
|-------------|-------|-----------------|---------------|
| **Playbooks** | Inhalts- und Qualitätsregeln (YAML + Markdown) | `playbooks/`, `content/playbooks/` | ✅ |
| **JSON-Schemas** | Datenlieferungen, Validierung (z. B. Agenten-Lieferung v3) | `schemas/` | ✅ teilweise |
| **Prompt-Schemas** | Struktur von KI-Prompts / Kontext-Bausteinen | `schemas/prompts/` | ⏳ geplant |
| **API-Verträge** | REST/MCP-Schnittstellen (Request/Response, Fehlercodes) | `contracts/api/` | ⏳ geplant |
| **Runtime-Konfiguration** | Routing, Task→Agent→Modell (keine Ausführung) | `runtime/` | ✅ |
| **ADRs** | Architektur- und Prozessentscheidungen | `adr/` | ✅ |

**Prinzip:** Was die App oder externe Systeme **erwarten oder liefern müssen**, wird in der Knowledge Platform als versioniertes, prüfbares Artefakt definiert — nicht nur in Fließtext-Doku.

### Abgrenzung

| In Knowledge Platform | In Digiwiz App |
|----------------------|----------------|
| Verträge, Schemas, Beispiele | Implementierung, Validierungscode, UI |
| `examples/` als Referenz-Instanzen | Laufzeit unter `data/` |
| API-Vertrag (Spezifikation) | FastAPI-Routen, `agent_lieferung_service.py` |

### Validierung

- **Contract-Tests** in `tests/` prüfen Vollständigkeit und Konsistenz der Artefakte (kein App-Code).
- **Integrations-Tests** in `digiwiki/tests/` prüfen, dass die App die Verträge korrekt lädt und anwendet.
- `VERSION` + `digiwiki/knowledge_lock.json` pinnen kompatible Contract-Versionen.

## Konsequenzen

- README und Manifest sprechen von **Contracts**, nicht nur von „Dokumentation“.
- Neue Schnittstellen (Stufe C/D/E) werden zuerst als Vertrag in KP spezifiziert, dann in der App implementiert.
- Prompt-Schemas und API-Verträge (z. B. OpenAPI) folgen inkrementell — ohne Breaking Changes an bestehenden Pfaden.
- Stufe E (Knowledge Graph) erweitert die Contract-Familie um Graph-Schema und Abfrage-Verträge; Chroma/RAG bleibt abgeleiteter Index in der App (ADR-0009).

## Verwandte ADRs

- ADR-0003 — Playbooks als SSOT (Teilmenge dieses Modells)
- ADR-0005 — Knowledge getrennt von Runtime
- ADR-0006 — Kein Git-Submodule bis nach Stufe E
