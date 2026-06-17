# outbound — moteur de campagnes 3 tiers (agentic)

Un moteur d'**outbound piloté par un agent** (Claude Code) : il assigne chaque contact de
ton CRM à la bonne campagne sur **3 vitesses** (warm / icebreaker / standard), applique les
garde-fous (1 entrée par enseigne, déjà-en-séquence exclu, LinkedIn-only), et charge les leads
dans tes campagnes. **Tu déclenches, l'agent fait le répétitif, tu valides. Rien ne part tout seul.**

> Config-driven : aucune valeur (IDs, colonnes, branding) n'est en dur. Tout vit dans
> `config/outbound.config.json`. Branche ton propre CRM Notion et tes propres campagnes.

---

## Le système 3 tiers

Chaque contact tombe dans **un seul** tier, pour ne bloquer aucun prospect :

| Tier | Pour qui | Message |
|---|---|---|
| **warm** | contacts à fort signal (arc validé) | message sur-mesure de bout en bout |
| **icebreaker** | contacts avec une note exploitable | template + 1 phrase perso générée |
| **standard** | le reste (Prospect + canal) | message générique honnête, sans ligne perso |

Routage (priorité **warm > icebreaker > standard** ; à tier égal, priorité persona configurable).
Détail : `docs/3-tier.md`.

## Prérequis

- **Claude Code** (CLI) — c'est l'agent qui orchestre.
- **Connecteurs MCP** : ton outil d'envoi (ex. lemlist) pour charger les leads, et **Notion** (CRM).
- **CRM Notion** : 2 bases (Companies, Contacts) partagées avec une intégration Notion.
- **Python 3.8+** (lib standard uniquement, zéro dépendance).

## Installation

```bash
git clone https://github.com/DamienDouat/outbound
cd outbound
cp config/outbound.config.example.json config/outbound.config.json
# édite config/outbound.config.json (IDs Notion, mapping colonnes, IDs campagnes, branding)
export NOTION_TOKEN="secret_xxx"     # ou un .env à la racine : NOTION_TOKEN=...
```

### Schéma CRM attendu (paramétrable)

Les noms de colonnes sont **mappés dans la config** (`notion.columns`), adapte-les à ton CRM :

- **Companies** : titre (`company_title`), statut (`company_status`, valeur "Prospect" = `prospect_value`).
- **Contacts** : titre, `Famille` (persona), `Arc statut` (valeur "Validé" = arc prêt), `Canal status`
  (valeur "En séquence" = déjà poussé), `LinkedIn URL`, `Email`, `Note contextuelle`, relation vers Companies.

## Workflow

```bash
# 1. (tier ICE) préparer la feuille d'icebreakers à rédiger
python3 scripts/icebreaker_engine.py prepare
#    -> l'agent lit data/icebreakers_todo.json, rédige 1 phrase honnête par contact,
#       les écrit dans data/icebreakers.json  (zéro signal inventé)

# 2. router tous les contacts vers les 9 campagnes (PLAN, n'écrit rien côté envoi)
python3 scripts/route_all.py
#    -> data/route/<tier>_<persona>.json  (leads + page_id + variables)

# 3. l'agent pousse chaque lot dans la campagne correspondante (gate humain),
#    puis met le Canal status à "En séquence". Tu lances la campagne toi-même.
```

Les **arcs** (tier warm) sont fournis dans `data/arcs.json` (page_id -> {t1_invite_note,
t1_subject, t1_body, t2_body}) ; tu les génères avec ton propre process de rédaction.

## Garde-fous (toujours actifs)

- **1 entrée par enseigne** (1 contact par Company, le meilleur tier).
- **Déjà-en-séquence exclu** (un contact `En séquence` verrouille son enseigne).
- **LinkedIn-only** par défaut (canal propre ; l'email se branche quand tu veux).
- **Aucun envoi automatique** : le moteur prépare, l'humain lance.

## Statut

MVP = le **moteur de campagnes 3 tiers** (route + icebreaker). Le **sourcing** (découverte +
enrichissement des contacts) et la génération de **copy/voix** sont une phase suivante :
ce repo suppose que tes contacts sont déjà dans Notion.

## Licence

Tous droits réservés. Code public en lecture, pas de réutilisation sans accord.
