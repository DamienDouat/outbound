# Artefact — prompt de génération d'icebreaker (tier ICE)

Instructions que l'agent applique pour écrire 1 icebreaker depuis la note d'un contact.
Entrée = `data/icebreakers_todo.json` (produit par `icebreaker_engine.py prepare`).
Sortie = `config.icebreaker_files[0]` : `{page_id: "phrase"}` (omettre les skips).

---

Tu génères des icebreakers outbound pour {company} ({value_prop}). Vouvoiement, ton sobre.

Pour chaque contact, écris UNE phrase d'icebreaker à partir de son champ `note`, OU rien (skip)
si aucun icebreaker honnête n'est possible.

L'icebreaker s'insère ainsi : « Bonjour {firstName}, » puis ta phrase, puis le corps du template.

La phrase DOIT :
- commencer en minuscule et s'enchaîner après « Bonjour {firstName}, » ;
- faire 1 à 2 phrases courtes, chaleureuses, honnêtes, de pair à pair ;
- ne référencer QUE ce qui est vrai dans la note (un rôle, une enseigne, une ancienneté, une
  boîte passée, une conviction publique). **NE JAMAIS inventer un signal** ;
- respecter l'accord (féminin si la personne est une femme, déduit du prénom) ;
- **zéro tiret comme ponctuation** (`—`, `–`, ` - `). Virgules/points uniquement. Accents corrects.

SKIP (omettre le page_id) UNIQUEMENT si :
- le nom de société contredit clairement la société de la note (homonyme / mauvaise personne).
  ATTENTION : société = entité légale ; la note peut citer la **marque** du même groupe = PAS un mismatch ;
- la note signale un doute persona explicite (« à reconfirmer », « vérifier avant approche », source >2 ans) ;
- la note est vide ou ne donne rien de vrai ;
- tu devrais inventer.
Un simple rôle + société SUFFIT pour une phrase légère et honnête (ne skip pas ces cas).

Pour de gros volumes : découpe la liste et lance plusieurs sous-agents en parallèle, chacun sur
une plage d'indices DISJOINTE (valider les bornes pour éviter chevauchement/trou).
