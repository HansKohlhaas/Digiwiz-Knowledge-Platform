# Deployment

## Knowledge Platform

- **Eigenständiges Repository** — kanonische Entwicklung in `Digiwiz-Knowledge-Platform`
- Versionierung über `VERSION` + `CHANGELOG.md`
- App pinnt kompatible Version via `digiwiki/knowledge_lock.json`
- **Kein Git-Submodule** bis nach Stufe E — siehe [ADR-0006](../adr/ADR-0006-no-git-submodule-until-stage-e.md)

### Abgleich Monorepo

Die Kopie `knowledge-platform/` im Digiwiz-Monorepo ist **kein eigenständiger Kanon** — sie folgt dem KP-Repo (siehe [11_roadmap_stufen_a_f.md](11_roadmap_stufen_a_f.md#dual-repo-synchronisation-entwicklungsplan)).

Bei jedem KP-Release: KP-Repo pushen → Monorepo-Kopie nachziehen → `knowledge_lock.json` anpassen.

### App-Anbindung (Produktiv)

1. KP-Repo klonen: `git clone https://github.com/HansKohlhaas/Digiwiz-Knowledge-Platform.git`
2. In Digiwiz `.env`: `DIGIWIZ_KNOWLEDGE_ROOT=<absoluter Pfad zum Klon>`
3. `digiwiki/knowledge_lock.json` auf KP-`VERSION` abstimmen

## Digiwiz App (Render / lokal)

- Runtime-Code unverändert in `digiwiki/`
- Env: `DIGIWIZ_KNOWLEDGE_ROOT` wenn KP außerhalb des Monorepos
- `data/` bleibt lokal/ephemeral

Siehe Render-Regeln: Port `0.0.0.0:$PORT`, ephemeral filesystem.
