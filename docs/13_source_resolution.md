# Source Resolution — SQL-first Policy

**Stand:** 09.07.2026  
**Verbindlich:** [ADR-0013](../adr/ADR-0013-source-resolution-and-sql-first-policy.md)  
**Contract:** [contracts/source-resolution/source_resolution_policy.yaml](../contracts/source-resolution/source_resolution_policy.yaml)

## Kernaussage

Bei **jeder Wissensabfrage** muss **zuerst** geprüft werden, ob es sich um eine **direkte SQL-/CRM-/Unternehmensdaten-Abfrage** handelt. Trifft das zu — oder liegen Schlüsselwörter/Entitäten aus den SQL-first-Domänen vor — hat die **eigene SQL-Datenbank Vorrang** vor Graph, Chroma/RAG und Web.

---

## 1. Reihenfolge der Wissensquellen

| Stufe | Quelle | Rolle | SSOT für |
|-------|--------|-------|----------|
| **0** | **Intent-Klassifikation** | Pflicht vor jeder Abfrage | Routing-Entscheid |
| **1** | **Knowledge Platform** | Playbooks, ADRs, Contracts | Regeln, Freigabe, Schnittstellen |
| **2** | **SQL / CRM / Stammdaten** | Operative Firmendaten (Access/CRM-DB) | Hersteller, Apotheken, Kunden, Status, Historien |
| **3** | **Knowledge Graph** | Struktur, Beziehungen, Provenienz (Stufe E) | Kanten, Entitätsbezüge — nicht Attribut-Fakten |
| **4** | **Chroma / RAG** | Semantischer, abgeleiteter Index | Wiki-Passagen, Verfahren, ähnliche Texte |
| **5** | **Web / extern** | Ergänzung, Branchennews | Öffentliche Quellen — **nicht** über SQL bei Firmendaten |

```
Anfrage
   │
   ▼
[0] SQL-first? ──ja──► [2] SQL abfragen ──► Ergebnis mit Provenienz
   │                           │
   nein                         │
   ▼                             │
[1] Playbooks/Contracts (immer für DAR-Tasks)
   │
   ▼
[3] Graph (wenn strukturelle Frage, Stufe E)
   │
   ▼
[4] Chroma/RAG (wenn semantische/Wiki-Frage)
   │
   ▼
[5] Web (optional, niedrigste Priorität)
   │
   ▼
Context Builder Output → Provider → Validator → ggf. Inbox
```

---

## 2. Entscheidungsregeln — wann SQL zuerst

### Pflicht SQL-first (mindestens eine Bedingung)

1. **Explizite Entität:** Kundennummer, Apotheken-ID, Hersteller-ID, Vertreiber-ID im Query oder Kontext
2. **Domänen-Match:** Anfrage enthält Begriffe aus `sql_first_domains` (siehe Policy-YAML)
3. **Fragetyp operational:** Status, Historie, Freigabe, Segment, Umsatzklasse, MSV3, Sortiment, Ansprechpartner
4. **Task-Routing:** DAR-Task oder Agent mit CRM-/Vertriebs-Kontext (`routing.json` Erweiterung geplant)

### SQL-first optional ergänzend

- Nach SQL: Graph für **Beziehungen** (z. B. „Welche Produkte hängen an Apotheke X?“ — Fakten aus SQL, Kanten aus Graph)
- Chroma **danach** nur für Verfahren/Wiki-Einordnung, nicht für Stammdaten-Ersatz

### Kein SQL-first

- Reine Verfahrensfragen („Wie funktioniert Presseschau-Import?“)
- Brandvoice / Playbook-Regeln
- Allgemeine Brancheneinordnung ohne Firmenbezug
- LinkedIn-Stil / Thought Leadership ohne Kundenbezug

---

## 3. Beispiele SQL-first-Fragen

| Frage | Warum SQL-first |
|-------|-----------------|
| „Welchen CRM-Status hat Apotheke 12345?“ | Kundennummer + CRM-Status |
| „Wer ist Ansprechpartner bei Hersteller XY für Nielsengebiet Nord?“ | Ansprechpartner + Hersteller + Nielsengebiet |
| „In welcher Umsatzklasse ist Vertreiber Müller GmbH?“ | Vertreiber + Umsatzklasse |
| „MSV3-Status für Sortiment ABC beim Kunden 98765?“ | MSV3 + Sortiment + Kundennummer |
| „Letzte interne Bewertung zu Apotheke Schmidt?“ | interne Bewertung + Apothekenbezug |
| „Welche Freigaben liegen für Produkt P-2024 vor?“ | Freigaben + Produktbezug |
| „Historie der Kontakte mit Kunde 55555?“ | Historie + Kundennummer |
| „Segmentierung aller Apotheken in Kanal E-Commerce?“ | Segmentierung + Vertriebskanal + Apotheken |

Weitere Beispiele: [examples/source-resolution/sql_first_questions.yaml](../examples/source-resolution/sql_first_questions.yaml)

---

## 4. Beispiele Chroma/RAG-Fragen

| Frage | Warum RAG (nach Klassifikation, ohne SQL-first) |
|-------|--------------------------------------------------|
| „Wie exportiere ich markierte Chat-Antworten aus dem DigiWiki?“ | Bedienung/Verfahren im Wiki |
| „Was steht in der Brandvoice zu Superlativen?“ | Playbook/Wiki-Text, semantisch |
| „Welche Schritte hat die Presseschau-Qualitätssicherung?“ | Verfahrensdoku |
| „DigiBest Positionierung USPs — Zusammenfassung“ | Unternehmens-Wiki, kein CRM-Fakt |
| „Ähnliche Wiki-Artikel zu Oracle-Integration?“ | Semantische Ähnlichkeit |
| „Was bedeutet Regisseur-Inbox im Workflow?“ | Architektur/Verfahren |

**Regel:** Auch bei RAG-Fragen **Schritt 0** ausführen — enthält die Frage versteckt eine Kundennummer, ist SQL-first.

Beispiele: [examples/source-resolution/chroma_rag_questions.yaml](../examples/source-resolution/chroma_rag_questions.yaml)

---

## 5. Beispiele Knowledge-Graph-Fragen

| Frage | Warum Graph (Stufe E, nach SQL wenn nötig) |
|-------|---------------------------------------------|
| „Welche Playbooks referenzieren die Quellen-Regeln?“ | Struktur: Playbook → Regel-Kante |
| „Welche ADRs hängen an Stufe E?“ | ADR-Beziehungsgraph |
| „Welche Entitäten teilen dieselbe Provenienz-Quelle?“ | Graph-Provenienz |
| „Welche Agenten-Lieferungen bezogen sich auf Hersteller X?“ | Kanten Lieferung→Entität (Fakten zu X aus SQL) |
| „Konflikt zwischen zwei Regeln — welche ADR-Kette gilt?“ | Strukturierte Policy-Kette |

**Regel:** Attributwerte (Status, Umsatz, MSV3) **immer aus SQL**; Graph liefert **Beziehungen und Provenienz**, nicht operative Fakten.

Beispiele: [examples/source-resolution/knowledge_graph_questions.yaml](../examples/source-resolution/knowledge_graph_questions.yaml)

---

## 6. Konfliktregeln

| Situation | Auflösung | Dokumentieren in Output |
|-----------|-----------|-------------------------|
| SQL sagt Status „aktiv“, Chroma-Text sagt „inaktiv“ | **SQL gewinnt** | `uncertainties[]` + SQL-Provenienz |
| SQL leer, Chroma liefert firmenspezifische „Fakten“ | **Nicht als Fakt verwenden** — Unsicherheit ausweisen | `uncertainties[]`: „Kein SQL-Treffer“ |
| KP-Playbook vs. Chroma-Snippet (Regeln) | **KP gewinnt** (ADR-0009) | `applied_playbooks[]` |
| Graph-Kante vs. SQL-Fakt zum selben Attribut | **SQL gewinnt** für Attribut; Graph für Beziehungskontext | getrennte Snippet-Typen |
| Web vs. SQL (Kundennummer, Status) | **SQL gewinnt** | Web nur als `supplementary` markieren |
| Mehrere SQL-Zeilen widersprüchlich | **Kein Merge raten** — an Regisseur/Inbox oder `uncertainties[]` | harte Unsicherheit |
| RAG vs. Web (allgemeine Branche) | Neueres Playbook/Verfahren > alter Index; Web niedrigste Priorität | Quellenliste vollständig |

**Leitplanke:** Bei Konflikt zwischen **abgeleitetem Index** (Chroma) und **KP-Contract** gilt die Knowledge Platform. Bei Konflikt zwischen **Chroma und SQL** für **Firmendaten** gilt **SQL**.

---

## 7. Geplante Integration — DAR Context Builder

**Status:** Contract + ADR — **Implementierung in App später** (ADR-0012).

### Geplante Pipeline-Erweiterung

```
routing_engine
      │
      ▼
source_resolution_router     ← NEU (App): Klassifikation Schritt 0
      │
      ├── sql_first → crm/sql_query_adapter (App, read-only)
      │
      ▼
context_builder              ← ADR-0011 + ADR-0013
      │
      ├── [1] playbooks + contracts (Pflicht)
      ├── [2] sql_snippets (wenn sql_first)
      ├── [3] graph_snippets (Stufe E)
      └── [4] rag_snippets (abgeleitet)
      │
      ▼
context_builder_output       ← resolution_path, sources, uncertainties
```

### Geplante Output-Felder (Contract-Erweiterung)

Zusätzlich zu ADR-0011:

- `resolution_path[]` — z. B. `["classify", "sql", "playbooks", "rag"]`
- `sql_first: boolean`
- `sql_snippets[]` — `{ "text", "query_ref", "provenance" }`
- `conflicts[]` — `{ "sources", "resolution", "winner" }`

Schema: `schemas/context_builder_output.schema.json` (Erweiterung v1.2.0, optional bis Implementierung).

### Bestehender Code (Ist)

`digiwiki/ai_runtime/context_builder.py` — nur Playbooks + Memory. **Kein** SQL/Graph/RAG — dokumentiert als D2; Source Resolution = **D4** (Roadmap).

---

## Verwandte Dokumente

- [12_architecture_layers.md](12_architecture_layers.md)
- [04_ai_runtime.md](04_ai_runtime.md)
- [11_roadmap_stufen_a_f.md](11_roadmap_stufen_a_f.md)
- [contracts/retrieval/README.md](../contracts/retrieval/README.md)
