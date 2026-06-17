# Artefact — prompt de génération d'arc (tier WARM)

Instructions que l'agent applique pour écrire un **arc relationnel chaleureux** par contact
prioritaire. Sortie = `data/arcs.json` : liste d'objets
`{page_id, t1_invite_note, t1_subject, t1_body, t2_body}`.

Réservé aux comptes à **fort signal** (recherche réelle par personne). Sans hook personnel
crédible -> on ne rédige pas (le contact reste en ICE ou STD).

---

## Le moteur (par personne, PAS un template)

Pour chaque contact prioritaire, cherche un **hook PERSONNEL** (intervention, post, interview,
prise de poste, prix, conviction publique) via recherche web + sources fiables. Puis écris un
copy sur-mesure. **Sans hook crédible -> watchlist, on n'écrit pas** (jamais générique en warm).

## Les 4 morceaux à produire

- **t1_invite_note** (≤200 car) : ouverture sincère sur le hook, zéro pitch, zéro CTA.
- **t1_subject** : 2 mots minuscules sur le hook.
- **t1_body** (le 1er message) : 1) accroche sincère sur le hook (on parle de LUI, pas de sa
  boîte) ; 2) « je vous écris simplement, sans rien vous vendre dans ce message » + une phrase de
  légitimité (`{founder_background}`, `{site}`) ; 3) porte ouverte douce. Signé `{signature}`.
- **t2_body** (la relance « cadeau ») : on relie au métier par curiosité, on offre une ressource
  ou un diagnostic **sans rien attendre en retour**.

## Règles dures

- **Jamais de mensonge.** « sans rien vous vendre dans ce message » est OK (vrai pour ce message).
- Aucun CTA / aucune offre en t1. Le cadeau vient en t2.
- **Zéro tiret comme ponctuation.** Accents corrects. Accord féminin si la personne est une femme.
- **Varier** les formules entre prospects (ne pas répéter la même clôture partout).
- `{value_prop}` au plus une fois, jamais en feature-dump.

Côté envoi : `t1_body` sert en LinkedIn (sauts `\n`) ET en email (sauts `<br>`). Le routeur
(`route_all.py`) produit ces deux variantes automatiquement.
