
import numpy as np
from analyse_donnees import charger_donnees
from scipy.optimize import linprog
import matplotlib.pyplot as plt
from pathlib import Path


# Récupérer les données
consommation_horaire, prix_horaire = charger_donnees()

N = len(consommation_horaire)
p = np.asarray(prix_horaire, dtype=float)

# Variables : charge, décharge et stock
coefficients = np.concatenate([
    p,
    -p,
    np.zeros(N + 1)
])

assert N == 168
assert len(coefficients) == 3 * N + 1
assert np.allclose(coefficients[:N], p)


# Paramètres de la batterie
capacite = 5.0
puissance_max = 2.0
eta_charge = 0.95
eta_decharge = 0.95

# Bornes des variables
bornes = (
    [(0, puissance_max)] * N
    + [(0, puissance_max)] * N
    + [(0, capacite)] * (N + 1)
)

assert len(bornes) == 3 * N + 1


# Contraintes d'évolution du stock
A_eq = np.zeros((N + 2, 3 * N + 1))
b_eq = np.zeros(N + 2)

for t in range(N):
    A_eq[t, t] = -eta_charge
    A_eq[t, N + t] = 1 / eta_decharge
    A_eq[t, 2 * N + t] = -1
    A_eq[t, 2 * N + t + 1] = 1

# Batterie vide au début et à la fin
A_eq[N, 2 * N] = 1
A_eq[N + 1, 3 * N] = 1

assert A_eq.shape == (N + 2, 3 * N + 1)
assert b_eq.shape == (N + 2,)


# Consommations horaires
D = consommation_horaire.to_numpy()

# Contraintes : -c_t + d_t <= D_t
A_ub = np.zeros((N, 3 * N + 1))
b_ub = D.copy()

for t in range(N):
    A_ub[t, t] = -1
    A_ub[t, N + t] = 1

assert A_ub.shape == (N, 3 * N + 1)
assert b_ub.shape == (N,)


# Résolution du problème d'optimisation
resultat = linprog(
    c=coefficients,
    A_ub=A_ub,
    b_ub=b_ub,
    A_eq=A_eq,
    b_eq=b_eq,
    bounds=bornes,
    method="highs"
)

if not resultat.success:
    raise RuntimeError(f"Optimisation échouée : {resultat.message}")

x = resultat.x

charge = x[:N]
decharge = x[N:2*N]
stock = x[2*N:]


# Énergie achetée au réseau
energie_reseau = D + charge - decharge

# Calcul des coûts
cout_reference = np.sum(p * D)
cout_optimise = np.sum(p * energie_reseau)

economie = cout_reference - cout_optimise
economie_pct = 100 * economie / cout_reference

print(f"Coût sans batterie : {cout_reference:.2f} €")
print(f"Coût avec batterie : {cout_optimise:.2f} €")
print(f"Économie : {economie:.2f} €")
print(f"Économie relative : {economie_pct:.2f} %")


# Vérification des contraintes physiques
tol = 1e-6

assert np.all(stock >= -tol)
assert np.all(stock <= capacite + tol)
assert np.all(energie_reseau >= -tol)

assert np.isclose(stock[0], 0, atol=tol)
assert np.isclose(stock[-1], 0, atol=tol)

assert np.allclose(
    stock[1:],
    stock[:-1] + eta_charge * charge - decharge / eta_decharge,
    atol=tol
)

simultane = np.sum(
    (charge > tol) & (decharge > tol)
)

print("Nombre d'heures avec charge et décharge simultanées :", simultane)


# Stratégie de charge et de décharge sur 24 heures
heures = np.arange(24)

plt.figure(figsize=(12, 5))

plt.plot(
    heures,
    charge[:24],
    label="Charge",
    marker="o"
)

plt.plot(
    heures,
    decharge[:24],
    label="Décharge",
    marker="o"
)

plt.xlabel("Heure de la journée")
plt.ylabel("Énergie (kWh)")
plt.title("Stratégie optimale de charge et de décharge")
plt.xticks(heures)
plt.legend()
plt.grid(True)
plt.tight_layout()

Path("figures").mkdir(parents=True, exist_ok=True)

plt.savefig(
    "figures/strategie_batterie.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Évolution du stock sur la première journée
heures_stock = np.arange(25)

plt.figure(figsize=(12, 5))

plt.step(
    heures_stock,
    stock[:25],
    where="post",
    marker="o",
    label="Énergie stockée"
)

plt.axhline(
    y=capacite,
    linestyle="--",
    label="Capacité maximale"
)

plt.xlabel("Heure")
plt.ylabel("Énergie stockée (kWh)")
plt.title("Évolution du stock de la batterie — 8 janvier 2007")
plt.xticks(heures_stock)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    "figures/evolution_stock.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
