# Copy & voix — adapter les messages

Le copy vit dans `templates/` et se paramètre par la config (`branding`, `persona_angles`).
Aucun texte produit n'est en dur dans le code : les variables par lead (`{icebreaker}`, arcs)
sont générées, le reste est du template que tu édites.

## Les placeholders

| Placeholder | Source | Quand |
|---|---|---|
| `{firstName}` `{companyName}` | l'outil d'envoi (champs lead) | à l'envoi |
| `{icebreaker}` | généré par lead (tier ICE) | au routage |
| `{value_prop}` `{claim}` `{signature}` `{founder_background}` | `config.branding` | dans les templates |
| `{persona_angle}` | `config.persona_angles[persona]` | dans les templates, par persona |

## Les 3 niveaux de personnalisation

- **warm** : arc complet par personne -> `templates/arc-prompt.md` (l'agent rédige, sort `data/arcs.json`).
- **icebreaker** : template + 1 phrase -> `templates/icebreaker-prompt.md` (l'agent rédige `data/icebreakers.json`).
- **standard** : template seul, zéro perso (le reste).

## Règles de voix (garde-fous)

- `{claim}` = un **objectif** (ce que tu vises), jamais un résultat client présenté comme acquis.
- **Zéro signal inventé** : pas de matière vraie -> on baisse d'un tier, on ne brode pas.
- **Zéro tiret comme ponctuation** (tell d'IA). Virgules/points.
- **Chaque relance = un angle neuf**, jamais répéter la 1re touche.
- Accord correct (féminin/masculin), accents corrects.

## Où ça se branche

`route_all.py` produit, par lead, les variables que tes campagnes attendent
(`noteInvite`, `t1BodyLi`, `t1BodyMail`, `t2BodyMail` pour warm ; `icebreaker` pour ice ; rien
pour std). Crée tes 3 tiers × N personas campagnes dans ton outil d'envoi, colle les templates
ci-dessus, et mappe leurs identifiants dans `config.campaigns`.
