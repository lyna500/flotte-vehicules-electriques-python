import pandas as pd
import matplotlib.pyplot as plt

def stats_vehicules(vehicules):
    data = [{"marque": v.marque, "modele": v.modele, "kilometrage": v.kilometrage} for v in vehicules]
    df = pd.DataFrame(data)
    print("Nombre de véhicules par marque :")
    print(df.groupby("marque").size())
    print("Kilométrage total par modèle :")
    print(df.groupby("modele")["kilometrage"].sum())

    # Graphique simple
    df.groupby("marque").size().plot(kind="bar", title="Véhicules par marque")
    plt.ylabel("Nombre de véhicules")
    plt.savefig("graphs/vehicules_par_marque.png")
    plt.close()




