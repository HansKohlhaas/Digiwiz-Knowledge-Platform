# API-Strategie

## Stufe C — Agenten-API

- CLI: `digiwiz-agent`
- REST: `/api/v1/agenten/*`, `/api/v1/playbooks/*`
- Auth: `X-DIGIWIZ-API-KEY`

Details: `docs/verfahren/digiwiz_agent_api.md`

## Stufe D — Runtime-API

- REST: `/api/v1/runtime/*`
- Gleicher Server (`11_wiki_api.py`)

## Prinzipien

1. REST zuerst (ADR-0001)
2. Keine offenen Schreib-Endpunkte
3. Responses liefern `inbox_id`, nicht Publish-URLs (ADR-0004)
