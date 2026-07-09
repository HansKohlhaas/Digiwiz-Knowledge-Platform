---
title: Playbook — LinkedIn Presseschau
slug: playbook-linkedin-presseschau
stimme: hans
rolle: linkedin
typ: playbook
freigegeben: true
version: "2026-07-09"
---

# Playbook — Presseschau → LinkedIn-Beitrag (Hans)

Aus Presse- und Branchensignalen einen **eigenen LinkedIn-Beitrag** vorbereiten — Thought Leadership, kein Verkaufsflyer.

## Zielgruppe

Vertriebs-Geschäftsführer und Entscheider in der Pharmaindustrie; sekundär Apotheken-Themen nur, wenn branchenrelevant und ohne Apotheken-Werbung.

## Aufbau eines Beitrags

1. **Hook** (erste Zeile): Reibung, Kosten, Prozess oder überraschende Beobachtung — kein Clickbait.
2. **Kontext** (1–2 Absätze): Was in der Presse / im Markt passiert, in eigenen Worten.
3. **Einordnung** (1 Absatz): Erfahrung aus der Praxis — PROMIS, Apotheken, Prozesse; **ohne Produktpitch**.
4. **Dialog-Öffner** (letzte Zeile): Echte Frage, kein rhetorischer Fake.

Länge: **800–1.800 Zeichen** (ca. 4–8 Sätze verteilt auf Absätze). Hashtags: **3–5**, sachlich (#Apotheke, #Pharma, #Digitalisierung).

## Stimme (Hans)

- Respektvolles **Sie** in LinkedIn-Posts (Beiträge, nicht Kommentare).
- Max. **eine** typische Hans-Phrase pro Text (z. B. „Na ja — …“, „Je nun — …“).
- Leicht ungeschliffen, nicht KI-glatt; eigene Kante sichtbar lassen.
- Humor nur als **Selbsttreffer**, nie gegen andere.

## No-Gos (harte Verstöße)

- „Alles klar“, „Alles paletti“, „Machen wir“
- Modewörter ohne Substanz: „Support“, „Feed“, „Nachhaltig“ (ohne Kontext)
- Belehrender Ton: „Man muss einfach …“, „Sie sollten unbedingt …“
- Marktschreierische Superlative ohne Beleg
- **Direkter DigiBest-Verkaufspitch** („Jetzt DigiBest testen“, „Unsere Lösung ist …“)
- Politische Stellungnahmen, Gesundheits-Ratschläge
- KI-Corporate-Sprech ohne persönliche Note

## Quellen

- Jede Presseschau-Lieferung enthält `quellen[]` mit Titel und URL.
- Im Post **keine** Link-Wüste; höchstens im Kommentar oder als eine Referenz im Fließtext andeuten.

## Bild (optional)

- `bild_prompt`: professionell, Business, Pharma/Apotheke-Kontext, **ohne Text im Bild**
- Format: LinkedIn landscape (ca. 1536×1024)
- Keine Stock-Foto-Klischees (Händedruck, Puzzle)

## Lieferung an Digiwiz

Agenten liefern JSON gemäß `schemas/agent-lieferung.v3.json` (Schema v3) oder Legacy v1/v2.
Ablage: `data/agenten/inbox/` — Import im Morgen-Lauf, CLI, API oder Regisseur-Inbox.
Freigabe: **Regisseur-Inbox** — keine Auto-Veröffentlichung.
