import pandas as pd
import matplotlib.pyplot as plt
import os

def stats_vehicules(vehicules):
    """
    Affiche les statistiques des véhicules et génère un graphique :
    - nombre de véhicules par marque
    - kilométrage total par modèle
    - sauvegarde d'un graphique dans outputs/graphe
    """

    if not vehicules:
        print("Aucun véhicule pour les statistiques.")
        return

    # Création du dossier si inexistant
    os.makedirs("outputs/graphe", exist_ok=True)

    # Extraction des données
    data = [{
        "marque": v.marque,
        "modele": v.modele,
        "kilometrage": v.kilometrage
    } for v in vehicules]

    df = pd.DataFrame(data)

    # Statistiques console
    print("\nNombre de véhicules par marque :")
    print(df.groupby("marque").size())

    print("\nKilométrage total par modèle :")
    print(df.groupby("modele")["kilometrage"].sum())

    # Graphique
    fig = df.groupby("marque").size().plot(kind="bar", title="Véhicules par marque")

    plt.xlabel("Marques")
    plt.ylabel("Nombre de véhicules")
    plt.xticks(rotation=45)

    # Enregistrement
    chemin_graph = "outputs/graphe/vehicules_par_marque.png"
    plt.tight_layout()
    plt.savefig(chemin_graph)
    plt.close()

    print(f"\nGraphique généré : {chemin_graph}\n")
