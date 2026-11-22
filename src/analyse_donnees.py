
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def charger_donnees():

    df = pd.read_csv(
        "data/household_power_consumption.csv",
        sep=";",
        quoting=3,
        na_values=["?"],
        low_memory=False
    )

    # Nettoyage du fichier CSV
    df.columns = df.columns.str.strip('"')
    df["Date"] = df["Date"].str.strip('"')
    df["Time"] = df["Time"].str.strip('"')

    df["Global_active_power"] = pd.to_numeric(
        df["Global_active_power"].astype(str).str.strip('"'),
        errors="coerce"
    )

    df["datetime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],
        format="%d/%m/%Y %H:%M:%S"
    )

    # Semaine étudiée : 8 au 14 janvier 2007
    debut = pd.Timestamp("2007-01-08")
    fin = pd.Timestamp("2007-01-15")

    semaine = df[
        (df["datetime"] >= debut)
        & (df["datetime"] < fin)
    ].copy()

    assert len(semaine) == 10080

    # Interpolation des mesures manquantes
    semaine["Global_active_power"] = (
        semaine["Global_active_power"].interpolate(method="linear")
    )

    assert semaine["Global_active_power"].notna().all()

    semaine = semaine.set_index("datetime")

    # Conversion de la puissance (kW) en énergie (kWh)
    semaine["energie_minute"] = semaine["Global_active_power"] / 60

    consommation_horaire = (
        semaine["energie_minute"].resample("1h").sum()
    )

    assert len(consommation_horaire) == 168
    assert consommation_horaire.notna().all()
    assert (consommation_horaire >= 0).all()

    # Tarification heures pleines / heures creuses (simulation)
    prix_creuses = 0.1589
    prix_pleines = 0.2142

    def tarif(heure):
        if heure >= 22 or heure < 6:
            return prix_creuses
        return prix_pleines

    prix_horaire = consommation_horaire.index.hour.map(tarif)

    assert len(prix_horaire) == len(consommation_horaire)
    assert np.isfinite(np.asarray(prix_horaire, dtype=float)).all()

    return consommation_horaire, prix_horaire


if __name__ == "__main__":

    consommation_horaire, prix_horaire = charger_donnees()

    cout_reference = (
        consommation_horaire.to_numpy()
        * np.asarray(prix_horaire, dtype=float)
    ).sum()

    print(f"Coût sans batterie : {cout_reference:.2f} €")

    # Consommation horaire sur la semaine
    plt.figure(figsize=(12, 5))

    plt.plot(
        consommation_horaire.index,
        consommation_horaire.values
    )

    plt.xlabel("Date et heure")
    plt.ylabel("Énergie consommée (kWh)")
    plt.title("Consommation électrique horaire du logement")
    plt.grid(True)
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)

    plt.savefig(
        "figures/consommation_horaire.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
