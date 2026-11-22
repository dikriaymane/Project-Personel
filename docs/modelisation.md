Projet personnel — Hypothèses et modélisation mathématique

## 1. Description du système

Nous considérons un logement alimenté par le réseau électrique et équipé d'une batterie de stockage.

À chaque heure, le logement possède une demande énergétique qui doit être satisfaite.

La batterie peut être chargée à partir du réseau électrique et déchargée pour alimenter le logement.

L'objectif est de déterminer une stratégie optimale de gestion de la batterie afin de minimiser le coût total de l'électricité achetée au réseau.

## 2. Hypothèses simplificatrices

Pour la première version du modèle, nous adoptons les hypothèses suivantes :

1. La consommation électrique du logement est connue à l'avance.
2. Les tarifs électriques sont connus et fixés sur l'horizon étudié.
3. La simulation porte initialement sur 24 heures, avec un pas de temps d'une heure.
4. La capacité de stockage de la batterie est constante.
5. Les rendements de charge et de décharge sont constants.
6. Le vieillissement et les coûts d'usure de la batterie sont négligés.
7. La revente d'électricité au réseau est interdite.
8. La batterie est initialement vide et doit être vide à la fin de l'horizon.
9. La demande énergétique du logement doit toujours être satisfaite.
10. Aucune production locale d'électricité n'est considérée.

Ces hypothèses permettent de construire un premier problème d'optimisation linéaire.

## 3. Paramètres du système

| Paramètre | Symbole | Valeur | Unité |
|---|---|---|---|
| Capacité maximale de la batterie | C_max | 5 | kWh |
| Puissance maximale de charge | P_c,max | 2 | kW |
| Puissance maximale de décharge | P_d,max | 2 | kW |
| Rendement de charge | η_c | 0,95 | — |
| Rendement de décharge | η_d | 0,95 | — |
| Énergie initiale | S_0 | 0 | kWh |
| Énergie finale | S_24 | 0 | kWh |
| Pas de temps | Δt | 1 | heure |
| Horizon d'optimisation | T | 24 | heures |

Ces paramètres constituent des hypothèses initiales. Ils pourront être modifiés lors de l'analyse de sensibilité.

## 4. Variables du modèle

### 4.1 Données connues

Pour chaque heure t :

- D_t : demande énergétique du logement (kWh).
- p_t : prix de l'électricité (€/kWh).

### 4.2 Variables de décision

- c_t : énergie prélevée sur le réseau pour charger la batterie (kWh).
- d_t : énergie fournie par la batterie au logement (kWh).

### 4.3 Variables d'état et variables calculées

- S_t : énergie stockée dans la batterie au début de l'heure t (kWh).
- G_t : énergie achetée au réseau pendant l'heure t (kWh).

## 5. Équations du système

### 5.1 Bilan énergétique

L'énergie achetée au réseau est donnée par :

$$
G_t=D_t+c_t-d_t
$$

Cette équation exprime le bilan énergétique entre le réseau, la batterie et le logement.

### 5.2 Dynamique de la batterie

L'évolution de l'énergie stockée est donnée par :

$$
S_{t+1}=S_t+\eta_c c_t-\frac{d_t}{\eta_d}
$$

Le rendement de charge réduit la quantité d'énergie effectivement stockée.

Le rendement de décharge implique qu'une quantité d'énergie supérieure à celle fournie au logement doit être retirée de la batterie.

## 6. Fonction objectif

Nous cherchons à minimiser le coût total de l'électricité achetée au réseau :

$$
\min \sum_{t=0}^{23}p_tG_t
$$

En remplaçant G_t :

$$
\min \sum_{t=0}^{23}p_t(D_t+c_t-d_t)
$$

## 7. Contraintes

### 7.1 Capacité de stockage

$$
0\leq S_t\leq C_{\max}
$$

### 7.2 Limites de charge et de décharge

$$
0\leq c_t\leq P_{c,\max}\Delta t
$$

$$
0\leq d_t\leq P_{d,\max}\Delta t
$$

### 7.3 Absence de revente au réseau

$$
G_t=D_t+c_t-d_t\geq0
$$

### 7.4 Conditions initiale et finale

$$
S_0=0
$$

$$
S_{24}=0
$$

### 7.5 Charge et décharge simultanées

La première formulation linéaire n'interdit pas explicitement la charge et la décharge simultanées.

Nous vérifierons dans quelles conditions une solution optimale sans fonctionnement simultané existe. Si nécessaire, une contrainte supplémentaire sera introduite.

## 8. Scénario de référence

Afin de mesurer les gains obtenus, nous considérons un scénario sans batterie.

Dans ce cas :

$$
c_t=d_t=0
$$

Donc :

$$
G_t=D_t
$$

Le coût de référence est :

$$
C_{\text{référence}}=\sum_{t=0}^{23}p_tD_t
$$

Les économies réalisées sont :

$$
\text{Économies}=C_{\text{référence}}-C_{\text{optimisé}}
$$

Le taux d'économie est :

$$
\text{Taux d'économie}=
\frac{C_{\text{référence}}-C_{\text{optimisé}}}
{C_{\text{référence}}}\times100
$$

## 9. Données utilisées

Le projet s'appuie sur des données historiques de consommation électrique, agrégées à un pas horaire.

Les données seront vérifiées avant leur utilisation : continuité temporelle, valeurs manquantes, cohérence des unités et qualité des mesures.

Les tarifs électriques seront définis séparément comme hypothèses de simulation, sauf si des tarifs historiques correspondant à la période de consommation sont disponibles.

## 10. Limites du modèle

Cette première version ne prend pas en compte :

- Le coût d'achat et d'installation de la batterie.
- Le vieillissement de la batterie.
- Les coûts de maintenance.
- L'incertitude sur les consommations futures.
- Les contraintes détaillées du réseau électrique.
- Les variations éventuelles des rendements avec la puissance et l'état de charge.

Ces limites seront prises en compte lors de l'interprétation des résultats et pourront faire l'objet d'améliorations ultérieures.
