# Doctrine — le système 3 tiers

Le but : **ne bloquer aucun prospect** tout en réservant l'effort de personnalisation aux
contacts qui le méritent. Chaque contact tombe dans **un seul** tier.

## Les 3 tiers

1. **warm** — message **sur-mesure de bout en bout**. Réservé aux contacts à fort signal
   (un « arc » complet a été rédigé et validé : note d'invitation + 1er message + relances).
   Coûteux à produire (recherche par personne), réservé aux comptes prioritaires.

2. **icebreaker** — **template + 1 phrase perso**. Le corps du message est fixe (par persona),
   seule la 1re ligne (`icebreaker`) est générée depuis la note CRM du contact. Bon compromis
   perso/volume. Règle dure : **pas de signal exploitable dans la note = pas d'icebreaker** →
   le contact bascule en standard (jamais de signal inventé).

3. **standard** — **message générique honnête**, sans ligne perso. Pour tout le reste
   (Prospect avec un canal mais sans arc ni note exploitable). Évite de bloquer la prospection.

## Routage (1 contact = 1 tier)

```
arc validé ?              -> warm
sinon icebreaker généré ? -> icebreaker
sinon (Prospect + canal)  -> standard
```

À tier égal, si une enseigne a plusieurs contacts éligibles, on garde **un seul** contact :
le persona le plus prioritaire (ordre configurable, ex. décideur d'abord).

## Garde-fous

- **1 entrée par enseigne** : on ne contacte jamais 2 personnes de la même société en même temps.
- **Déjà-en-séquence** : si un contact d'une enseigne est déjà `En séquence`, l'enseigne est verrouillée.
- **Canal propre** : LinkedIn-only par défaut (les emails douteux/homonymes restent en hold).
- **Humain dans la boucle** : le moteur prépare et charge les leads ; le lancement reste un acte humain.

## Mapping vers les campagnes

`config.campaigns[tier][persona]` -> identifiant de campagne dans ton outil d'envoi.
Soit 3 tiers × N personas campagnes à créer (chacune avec son angle + son copy).
