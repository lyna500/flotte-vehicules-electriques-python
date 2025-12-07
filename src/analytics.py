import pandas as pd
import matplotlib.pyplot as plt
import os

def stats_vehicules(vehicules):
    """
    Affiche les statistiques des véhicules et génère un graphique :
    - nombre de véhicules par marque
    - kilométrage total par modèle
    """
    if not vehicules:
        print("Aucun véhicule pour les statistiques.")
        return

    os.makedirs("outputs/graphe", exist_ok=True)

    data = [{"marque": v.marque, "modele": v.modele, "kilometrage": v.kilometrage} for v in vehicules]
    df = pd.DataFrame(data)

    print("\nNombre de véhicules par marque :")
    print(df.groupby("marque").size())

    print("\nKilométrage total par modèle :")
    print(df.groupby("modele")["kilometrage"].sum())

    # Graphique
    df.groupby("marque").size().plot(kind="bar", title="Véhicules par marque")
    plt.xlabel("Marques")
    plt.ylabel("Nombre de véhicules")
    plt.xticks(rotation=45)
    plt.tight_layout()
    chemin_graph = "outputs/graphe/vehicules_par_marque.png"
    plt.savefig(chemin_graph)
    plt.close()
    print(f"\nGraphique généré : {chemin_graph}\n")


def stats_locations(locations_dict, utilisateurs):
    """
    Affiche les statistiques sur les locations :
    - nombre de locations par client
    - durée moyenne des locations
    """
    if not locations_dict:
        print("Aucune location à analyser.")
        return

    rows = []
    for client_id, locs in locations_dict.items():
        for loc in locs:
            duree_jours = (loc.date_fin - loc.date_debut).days if loc.date_fin else None
            rows.append({
                "client_id": client_id,
                "vehicule_id": loc.vehicule_id,
                "duree_jours": duree_jours
            })

    df = pd.DataFrame(rows)
    if df.empty:
        print("Aucune location terminée à analyser.")
        return

    df_clients = df.groupby("client_id").size().reset_index(name="nombre_locations")
    print("\nNombre de locations par client :")
    for _, row in df_clients.iterrows():
        client = utilisateurs.get(row.client_id)
        nom = client.nom if client else f"Client {row.client_id}"
        print(f"{nom} : {row.nombre_locations}")

    df_valid = df[df.duree_jours.notnull()]
    if not df_valid.empty:
        duree_moyenne = df_valid["duree_jours"].mean()
        print(f"\nDurée moyenne des locations : {duree_moyenne:.2f} jours")
    else:
        print("\nAucune location terminée pour calculer la durée moyenne.")

