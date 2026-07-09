# Deployment

## Knowledge Platform

- Versionierung über `VERSION` + `CHANGELOG.md`
- Kann als Git-Submodule oder separates Repo ausgekoppelt werden
- App pinnt Version via `digiwiki/knowledge_lock.json`

## Digiwiz App (Render / lokal)

- Runtime-Code unverändert in `digiwiki/`
- Env: `DIGIWIZ_KNOWLEDGE_ROOT` wenn KP außerhalb des Monorepos
- `data/` bleibt lokal/ephemeral

Siehe Render-Regeln: Port `0.0.0.0:$PORT`, ephemeral filesystem.
