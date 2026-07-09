# ADR-0008: Knowledge Graph als Erweiterung der Knowledge Platform

## Status

Akzeptiert (2026-07-09)

## Kontext

Stufe E führt einen **Knowledge Graph** ein: Entitäten, Beziehungen und Provenienz über Playbooks, Wiki-Inhalte und Agenten-Lieferungen hinweg.

Offene Architekturfrage: Wird der Graph ein **eigenes Runtime-System** (neuer Service, eigene Pipeline, parallele Schicht zu DAR) — oder eine **Erweiterung der Knowledge Platform** als Contract-Artefakt, den die bestehende App-Runtime konsumiert?

Risiko bei „neuer Runtime“:

- Duplikat zu Stufe D (`ai_runtime/`) — zweite Orchestrierung, zweite Konfiguration
- Schwächere SSOT — Graph-Logik verteilt zwischen KP und App
- Höhere Kopplung und Wartungskosten ohne Mehrwert für das Regisseur-Modell

## Entscheidung

**Der Knowledge Graph ist eine Erweiterung der Knowledge Platform — keine neue Runtime.**

| Schicht | Stufe E — Zuständigkeit |
|---------|-------------------------|
| **Knowledge Platform** | Graph-Schema, Knoten-/Kantentypen, Abfrage-Verträge, Beispiel-Graph, Provenienz-Regeln, ADRs |
| **Digiwiz App** | **Konsument:** Graph laden, Abfragen ausführen, Ergebnisse in DAR Context Builder / RAG einbinden |
| **Nicht** | Kein `graph_runtime/`, kein paralleler AI-Director, kein eigener HTTP-Server für den Graph |

### Konkret

1. Graph-Artefakte leben unter KP-Contracts (ADR-0007):
   - `schemas/graph/` — Datenmodell (Knoten, Kanten, Typen)
   - `contracts/graph/` — Abfrage-Verträge (Format TBD, z. B. deklarative JSON-Queries)
   - `examples/graph/` — Referenz-Instanzen
2. **Stufe D (DAR)** bleibt die einzige AI-Runtime; Stufe E **erweitert den Kontext**, den DAR über Playbooks hinaus nutzt.
3. Optionaler **persistenter Graph-Store** (Datei, DB) ist **Infrastruktur der App**, nicht Bestandteil der KP — das **Schema und die Semantik** bleiben in KP.
4. Import aus Wiki/Playbooks (E2) produziert Graph-**Daten** in der App; die **Regeln des Imports** sind Contracts in KP.

## Begründung

- Konsistent mit ADR-0005 (Wissen getrennt von Runtime) und ADR-0007 (Contracts als SSOT)
- Kein Breaking Change an `ai_runtime/` — nur Erweiterung von `context_builder` / Graph-Loader
- Versionierung und Review des Graph-Modells im KP-Repo, nicht versteckt im Python-Code
- Regisseur-Inbox und ADR-0004 bleiben unberührt — der Graph liefert **Kontext**, keine Auto-Veröffentlichung

## Konsequenzen

- Stufe E-Implementierung **startet in KP** (Schema, Beispiele, Contract-Tests), dann App-Integration
- Kein neues Stufen-Label „Stufe E Runtime“ — E ist **Knowledge Layer++**
- `meta/manifest.yaml` erhält Contract-Typ `knowledge_graph`
- Roadmap-Meilensteine E1–E5 bleiben; E3 heißt explizit: DAR Context Builder, nicht neuer Director
- Stufe F (Autonome Agenten) nutzt den Graph als **Provenienz- und Policy-Kontext**, nicht als autonome Schicht

## Nicht-Ziele (Stufe E)

- Eigener MCP-/REST-Server nur für den Graph
- Ersetzen von Chroma/RAG — Graph **ergänzt**; Rollen klärt ADR-0009
- Auto-Publish oder Umgehung der Regisseur-Inbox

## Verwandte ADRs

- ADR-0005 — Knowledge getrennt von Runtime
- ADR-0006 — Kein Submodule bis nach E (Re-Evaluation inkl. Graph-Deployment)
- ADR-0007 — Contracts als SSOT
- ADR-0009 — Knowledge Graph und Chroma/RAG — Rollen und Zusammenspiel
