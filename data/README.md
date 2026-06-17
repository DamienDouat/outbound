# data/ — fichiers runtime (gitignored)

Ces fichiers contiennent tes données CRM : **jamais committés** (voir `.gitignore`).

| Fichier | Produit par | Contenu |
|---|---|---|
| `icebreakers_todo.json` | `icebreaker_engine.py prepare` | contacts à icebreaker (page_id, prénom, société, persona, note) |
| `icebreakers.json` | l'agent (rédaction) | `{page_id: "phrase d'icebreaker"}` (tier ICE) |
| `arcs.json` | ton process de rédaction d'arcs | `[{page_id, t1_invite_note, t1_subject, t1_body, t2_body}]` (tier WARM) |
| `route/<tier>_<persona>.json` | `route_all.py` | leads prêts à pousser (page_id + variables) |

Le chemin de `arcs.json` et `icebreakers.json` est configurable (`config.arc_dataset`,
`config.icebreaker_files`).
