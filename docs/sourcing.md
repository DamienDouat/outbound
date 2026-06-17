# Sourcing — adaptateurs pluggables

Le sourcing (trouver les sociétés cibles) est **séparé** du moteur de campagnes. Un adaptateur
produit un fichier de candidats ; le reste du pipeline (push Notion, routage, campagnes) est
provider-agnostique.

## Adaptateur fourni : France (INSEE)

`scripts/sourcing/source_companies_fr.py` — API `recherche-entreprises.api.gouv.fr` (gratuit,
sans clé, **France uniquement**). Config dans `config.sourcing` :

```json
"sourcing": {
  "provider": "france_insee",
  "naf_codes": ["47.71Z"],          // activités cibles (codes NAF)
  "departments": [],                 // [] = toute la France, ou ["75","69",...]
  "employee_tranches_min": "21",     // 21 = 50-99 salariés
  "employee_tranches_max": "42",     // 42 = 1000-1999 salariés
  "page_limit": 5
}
```

```bash
python3 scripts/sourcing/source_companies_fr.py          # dry -> data/companies_candidates.json
python3 scripts/sourcing/source_companies_fr.py --push   # crée les Companies (Prospect) dans Notion (gaté)
```

Tranches effectif INSEE : 21=50-99 · 22=100-199 · 31=200-249 · 32=250-499 · 41=500-999 · 42=1000-1999.

## Brancher un autre pays / une autre source

Écris un nouvel adaptateur (`source_companies_<x>.py`) qui produit le **même**
`data/companies_candidates.json` :

```json
[{ "siren": "ou tout id local", "name": "Nom société", "naf": "...", "tranche": "...", "dept": "..." }]
```

Le `--push` (création Notion) peut être réutilisé tel quel : il mappe `name` -> titre Company +
statut `Prospect`, dédoublonne par titre. À toi d'ajouter les colonnes propres à ton CRM
(SIREN, secteur, taille) en étendant `push_notion()`.

## Découverte des décideurs (contacts) — phase suivante

Cet adaptateur source les **sociétés**. La découverte des **décideurs** (qui contacter) +
l'enrichissement (email/tel) dépendent d'outils tiers (ex. un MCP d'enrichissement) et se font
côté agent, gatés. Le moteur de campagnes suppose les Contacts déjà dans Notion (avec Famille,
LinkedIn, Note contextuelle).
