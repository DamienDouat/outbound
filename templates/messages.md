# Templates de messages — les 3 tiers

Copy paramétrable. Placeholders : `{firstName}` `{companyName}` (remplis par l'outil d'envoi),
`{icebreaker}` (généré par lead, tier ICE), et les valeurs de marque depuis la config :
`{value_prop}` `{claim}` `{signature}` `{founder_background}` `{persona_angle}`.

> Règle d'or : `{claim}` = un **objectif** (ce que tu vises), jamais un résultat client présenté
> comme acquis. Pas de signal inventé. Ton sobre, pas de tirets en ponctuation.

---

## Structure commune (warm + standard)

Séquence LinkedIn-first + conditionnelle :

```
J0  visite profil
J0  invitation (note courte)
+6j condition : invitation acceptée ?
    OUI -> A1 message  ->  A2 note vocale  ->  A3 message  ->  A4 email  ->  A5 email  ->  A6 email
    NON -> B1 email     ->  B2 email        ->  B3 email
```

Les étapes **A2 à A6 et B2/B3 sont fixes** (mêmes pour tous, par persona). Seules les
**1res touches portent la perso** : invitation, A1, B1.

---

## Tier WARM — 1res touches = arc sur-mesure (par lead)

- **invitation** = `{noteInvite}` (variable d'arc)
- **A1 / B1** = `{t1BodyLi}` / `{t1Subject}` + `{t1BodyMail}` (variables d'arc)

L'arc complet est rédigé par lead (voir `templates/arc-prompt.md`) et stocké dans `data/arcs.json`.

## Tier ICEBREAKER — 1res touches = template + `{icebreaker}`

**Invitation** (≤200 car) :
> Bonjour {firstName}, {founder_background}. J'échange avec des décideurs de votre secteur sur {persona_angle}. Preneur de votre regard.

**A1 — 1er message LinkedIn** :
> Bonjour {firstName},
>
> {icebreaker}
>
> Je vous écris simplement. {value_prop}. {persona_angle}.
>
> Au plaisir d'échanger.
> {signature}

**B1 — 1er email** (objet court, minuscules) :
> Bonjour {firstName},
>
> {icebreaker}
>
> Je vous écris simplement. {value_prop}. {persona_angle}. Juste laisser une porte d'entrée si nos sujets se croisent.
>
> {signature}

## Tier STANDARD — générique (sans ligne perso)

Mêmes templates que ICE, **sans la ligne `{icebreaker}}`** : l'invitation et A1/B1 portent
directement la valeur (pas d'accroche perso). À réserver aux contacts sans note exploitable.

---

## Relances fixes (A3..A6, B2/B3) — partagées

- **A3 (LinkedIn, porte ouverte)** : « Je vous laisse tranquille, sans insister. Un mot ici suffit le jour où le sujet vous intéresse. »
- **A4 (email, ré-intro)** : présentation claire de `{value_prop}` + `{claim}` + signature.
- **A5 / B2 (email, cadeau)** : une ressource ou un diagnostic offert, sans contrepartie.
- **A6 / B3 (email, breakup)** : « Le timing n'est probablement pas le bon, et c'est normal. Ma porte reste ouverte, et si ce n'est pas vous, je suis preneur d'un nom. »

Chaque relance = **un angle neuf**, jamais répéter la 1re touche.
