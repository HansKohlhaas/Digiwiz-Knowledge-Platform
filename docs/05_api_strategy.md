# API Strategy

Digiwiz nutzt eine REST-first-Strategie. MCP wird vorbereitet, aber nicht als Voraussetzung fuer fruehe Integrationen behandelt.

## REST zuerst

REST-Endpunkte sind nachvollziehbar, testbar und fuer bestehende Systeme einfach integrierbar. Sie bilden die stabile Grundlage fuer CLI, UI und spaetere Agenten.

## Vorgeschlagene Ressourcen

- `GET /playbooks`
- `GET /playbooks/{id}`
- `POST /validate/playbook`
- `POST /drafts/presseschau`
- `POST /drafts/linkedin`
- `POST /reviews/content`

## API-Regeln

- Keine Breaking Changes ohne ADR.
- Versionierte Response-Formate.
- Validierung gegen Schemas.
- Keine Veroeffentlichungs-Endpunkte ohne manuelle Freigabestufe.
