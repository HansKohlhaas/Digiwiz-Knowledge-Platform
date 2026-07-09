# ADR-0009: Knowledge Graph und Chroma/RAG — Rollen und Zusammenspiel

## Status

Akzeptiert (2026-07-09)

## Kontext

Digiwiz nutzt heute **ChromaDB** als semantischen Vektor-Index über Wiki-Inhalte (`digiwiki/Chroma_DB/`, Wiki-Wächter). Stufe E führt einen **Knowledge Graph** ein (ADR-0008): strukturierte Entitäten, Beziehungen, Provenienz.

Offene Frage: Ersetzt der Graph Chroma/RAG? Wird Chroma SSOT? Entsteht eine dritte Runtime?

Risiken bei falscher Einordnung:

- Chroma-Index als „Wahrheit“ — Playbooks/ADRs/Contracts verlieren Führungsrolle
- Graph ersetzt RAG voreilig — semantische Suche geht verloren
- Doppel-Runtime oder parallele Kontext-Pipelines neben DAR
- Auto-Publish durch „intelligenten“ RAG-Kontext ohne Regisseur-Freigabe

## Entscheidung

**Knowledge Graph und Chroma/RAG erfüllen unterschiedliche Rollen und werden im DAR Context Builder kombiniert — ohne neue Runtime, ohne Chroma-Implementierung in der Knowledge Platform.**

### Rollenmodell

| Schicht | Rolle | SSOT? | Ort |
|---------|--------|-------|-----|
| **Playbooks, ADRs, Contracts** | Regeln, Schnittstellen, Architektur | ✅ **führend** | Knowledge Platform |
| **Knowledge Graph** | Strukturierte Beziehungen, Provenienz, explizite Kanten | ✅ Schema/Contracts in KP | KP + App-Store |
| **Chroma / RAG** | Abgeleiteter **semantischer Retrieval-Index** | ❌ **nicht** SSOT | Digiwiz App (bestehend) |

### Kanonische Wahrheit

1. **Knowledge Platform** definiert, was gilt: Playbooks, JSON-Schemas, Graph-Schema, Retrieval-**Regeln** (nicht der Index).
2. **Chroma** ist ein **Rebuild-fähiger Index** aus kanonischen Quellen (Wiki, Playbooks, freigegebene Inhalte) — vergleichbar mit einem Cache, nicht mit einem Contract.
3. **Knowledge Graph** liefert **strukturierten Kontext** (wer-hängt-mit-wem, Provenienz, explizite Beziehungen).
4. **Chroma/RAG** liefert **semantisch ähnlichen Fließtext** (passage retrieval, embedding-basiert).

Beide ergänzen sich; keiner ersetzt Playbooks oder ADRs als Leitplanke.

### DAR Context Builder (Stufe D/E — geplant)

```
Task + Playbooks (KP, Pflicht)
    │
    ├──► Graph-Kontext (strukturiert, Provenienz)     ← Stufe E
    │
    └──► RAG-Kontext (Chroma, semantisch)              ← bestehend, abgeleitet
              │
              ▼
        context_builder.py  →  Provider  →  Validator  →  Regisseur-Inbox
```

- **Eine Runtime:** Stufe D (`ai_runtime/`) — ADR-0008 bleibt gültig
- Context Builder **mergt** Graph- und RAG-Snippets nach definierten Prioritäten (Contract unter `contracts/retrieval/`, geplant)
- **Keine** direkte Veröffentlichung aus RAG- oder Graph-Ergebnissen

### Was nicht entschieden wird (bewusst ausgeklammert)

- **Keine Implementierung** der Chroma-DB in dieser ADR oder in der Knowledge Platform
- Kein Ersatz des Wiki-Wächters oder Chroma-Pflege in Stufe E
- Kein verbindliches Embedding-Modell — bleibt App-Konfiguration

### Retrieval-Contracts (KP, geplant)

Regeln für Kontext-Zusammenführung — nicht der Vektor-Index:

- `contracts/retrieval/` — Prioritäten, Limits, Provenienz-Anzeige, No-Gos
- Graph-Abfragen bleiben in `contracts/graph/` (ADR-0008)

## Begründung

- SSOT-Klarheit: Contracts und Playbooks steuern Verhalten; Chroma ist abgeleitetes Artefakt
- Graph + RAG adressieren verschiedene Fragestellungen (Beziehung vs. Ähnlichkeit)
- DAR bleibt einzige Orchestrierung — kein `rag_runtime/`, kein `graph_runtime/`
- Regisseur-Modell unverändert: Kontext beeinflusst Vorschläge, nicht Freigabe (ADR-0002, ADR-0004)

## Konsequenzen

- Stufe E **ersetzt Chroma nicht** — Graph-Contracts und Retrieval-Contracts parallel pflegen
- KP enthält **keine** Chroma-Konfiguration, Collections oder Embeddings — nur Retrieval-**Policy**-Contracts
- App: Chroma bleibt wo sie ist; Graph-Loader und Context Builder werden erweitert (Integrations-Tests, kein KP-Code)
- `meta/manifest.yaml` erhält Contract-Typ `retrieval`
- Roadmap E3: „Context Builder kombiniert Graph + RAG“
- Rebuild-Policy: Bei Widerspruch zwischen Index und KP-Contract gilt **KP**

## Nicht-Ziele

- Chroma-DB in Knowledge Platform implementieren oder versionieren
- RAG-Antworten auto-freigeben oder an LinkedIn/WordPress senden
- Graph als einzige Wissensquelle für DAR
- Breaking Changes an bestehenden Chroma-Pfaden oder Wiki-Wächter

## Verwandte ADRs

- ADR-0002 — Regisseur-Inbox bleibt Freigabe-Hub
- ADR-0003 — Playbooks als SSOT
- ADR-0004 — Keine Auto-Veröffentlichung
- ADR-0005 — Knowledge getrennt von Runtime
- ADR-0007 — Contracts als SSOT
- ADR-0008 — Knowledge Graph als KP-Erweiterung, keine neue Runtime
