from flotte import Flotte
from models import Vehicule, Client, Gestionnaire, Location, Maintenance
from test_data import charger_donnees_test
import persistence
import analytics
import os

def menu_principal():
    flotte = Flotte()

    charger_donnees_test(flotte)

    while True:
        print("""
1. Gérer les véhicules
2. Gérer les utilisateurs
3. Gérer les locations
4. Gérer la maintenance
5. Sauvegarder / Charger
6. Statistiques & Visualisations
7. Quitter
        """)
        choix = input("Votre choix : ").strip() 

        # --- VÉHICULES ---
        if choix == "1":
            print("1: Ajouter | 2: Modifier | 3: Supprimer | 4: Afficher | 5: Rechercher")
            sub = input("Choix : ").strip()

            if sub == "1":
                marque = input("Marque : ").strip()
                modele = input("Modèle : ").strip()
                while True:
                    try:
                        batterie = int(input("Batterie (kWh) : "))
                        if 10 <= batterie <= 150:
                            break
                        print("Erreur : batterie 10-150 kWh")
                    except ValueError:
                        print("Erreur : nombre entier")
                while True:
                    try:
                        autonomie = int(input("Autonomie (km) : "))
                        if autonomie > 0:
                            break
                        print("Erreur : autonomie positive")
                    except ValueError:
                        print("Erreur : nombre entier")
                v = Vehicule(marque, modele, batterie, autonomie)
                flotte.ajouter_vehicule(v)
                print(f"Véhicule ajouté ! ID {v.id}")

            elif sub == "2":
                try:
                    vid = int(input("ID du véhicule à modifier : "))
                    v = flotte.rechercher_vehicule_par_id(vid)
                    if not v:
                        print("Véhicule introuvable")
                        continue
                    marque = input(f"Nouvelle marque ({v.marque}) : ") or v.marque
                    modele = input(f"Nouveau modèle ({v.modele}) : ") or v.modele
                    batterie = input(f"Nouvelle batterie ({v.batterie}) : ")
                    autonomie = input(f"Nouvelle autonomie ({v.autonomie}) : ")
                    kwargs = {}
                    kwargs['marque'] = marque
                    kwargs['modele'] = modele
                    if batterie: kwargs['batterie'] = int(batterie)
                    if autonomie: kwargs['autonomie'] = int(autonomie)
                    flotte.modifier_vehicule(vid, **kwargs)
                    print("Véhicule modifié.")
                except ValueError:
                    print("Erreur de saisie.")

            elif sub == "3":
                try:
                    vid = int(input("ID du véhicule à supprimer : "))
                    flotte.supprimer_vehicule(vid)
                    print("Véhicule supprimé.")
                except ValueError:
                    print("Erreur de saisie.")

            elif sub == "4":
                flotte.afficher_vehicules()

            elif sub == "5":
                marque = input("Filtrer par marque (laisser vide = tous) : ").strip() or None
                modele = input("Filtrer par modèle (laisser vide = tous) : ").strip() or None
                statut = input("Filtrer par statut (disponible/loué/maintenance) : ").strip() or None
                try:
                    autonomie = int(input("Autonomie minimale (km, laisser vide = 0) : ") or 0)
                except ValueError:
                    autonomie = 0
                result = flotte.rechercher_vehicule(marque, modele, autonomie, statut)
                for v in result:
                    print(v.afficher_resume())

        # --- UTILISATEURS ---
        elif choix == "2":
            print("1: Ajouter utilisateur | 2: Afficher utilisateurs")
            sub = input("Choix : ").strip()
            if sub == "1":
                nom = input("Nom : ").strip()
                email = input("Email : ").strip()
                type_user = input("Type (client/gestionnaire) : ").lower().strip()
                if type_user == "client":
                    permis = input("Permis : ").strip()
                    u = Client(nom, email, permis)
                else:
                    u = Gestionnaire(nom, email)
                flotte.ajouter_utilisateur(u)
                print(f"Utilisateur ajouté ! ID {u.id}")
            elif sub == "2":
                flotte.afficher_utilisateurs()

        # --- LOCATIONS ---
        elif choix == "3":
            print("1: Démarrer location | 2: Terminer location | 3: Historique locations client")
            sub = input("Choix : ").strip()
            if sub == "1":
                try:
                    cid = int(input("ID client : "))
                    vid = int(input("ID véhicule : "))
                    flotte.demarrer_location(cid, vid)
                except ValueError:
                    print("Erreur de saisie.")
            elif sub == "2":
                try:
                    cid = int(input("ID client : "))
                    vid = int(input("ID véhicule : "))
                    km = int(input("Km parcourus : "))
                    while True:
                        try:
                            charge = int(input("Niveau de charge (%) : "))
                            if 0 <= charge <= 100:
                                break
                            print("Charge 0-100%")
                        except ValueError:
                            print("Nombre entier")
                    flotte.terminer_location(cid, vid, km, charge)
                except ValueError:
                    print("Erreur de saisie.")
            elif sub == "3":
                try:
                    cid = int(input("ID client : "))
                    locs = flotte.locations.get(cid, [])
                    if not locs:
                        print("Aucune location pour ce client.")
                        continue
                    for loc in locs:
                        penalite_str = f" | Pénalité : {loc.penalite} €" if getattr(loc, "penalite", 0) > 0 else ""
                        print(f"Véhicule {loc.vehicule_id} | Début: {loc.date_debut} | Fin: {loc.date_fin}{penalite_str}")
                except ValueError:
                    print("Erreur de saisie.")


        # --- MAINTENANCE ---
        elif choix == "4":
            print("1: Ajouter maintenance | 2: Valider maintenance | 3: Maintenance automatique | 4: Véhicules en maintenance | 5: Logs maintenance")
            sub = input("Choix : ").strip()
            if sub == "1":
                try:
                    vid = int(input("ID véhicule : "))
                    type_op = input("Type maintenance : ").strip()
                    cout = float(input("Coût : "))
                    m = Maintenance(vid, type_op, cout)
                    flotte.ajouter_maintenance(m)
                except ValueError:
                    print("Erreur de saisie.")
            elif sub == "2":
                try:
                    vid = int(input("ID véhicule : "))
                    flotte.valider_maintenance(vid)
                except ValueError:
                    print("Erreur de saisie.")
            elif sub == "3":
                flotte.verifier_maintenance()
            elif sub == "4":
                    flotte.afficher_vehicules_en_maintenance()
            elif sub == "5":
                flotte.afficher_logs_maintenance()


        # --- SAUVEGARDE / CHARGEMENT ---
        elif choix == "5":
            print("1: Sauvegarder JSON | 2: Charger JSON | 3: Sauvegarder CSV | 4: Charger CSV")
            sub = input("Choix : ").strip()
            if sub == "1":
                # Véhicules / utilisateurs
                persistence.sauvegarder_json(flotte.vehicules, "data/vehicules.json")
                persistence.sauvegarder_json(list(flotte.utilisateurs.values()), "data/utilisateurs.json")
                # Locations
                all_locs = []
                for locs in flotte.locations.values():
                    all_locs.extend([loc.to_dict() for loc in locs])
                persistence.sauvegarder_json(all_locs, "data/locations.json")
                # Maintenances
                persistence.sauvegarder_json(flotte.maintenances, "data/maintenances.json")
                print("JSON sauvegardé pour véhicules, utilisateurs, locations et maintenances.")
            elif sub == "2":
                flotte.vehicules = persistence.charger_json(Vehicule, "data/vehicules.json")
                utilisateurs = persistence.charger_json(list, "data/utilisateurs.json")
                flotte.utilisateurs = {}
                for u in utilisateurs:
                    type_user = u.get("type")
                    if type_user == "client":
                        flotte.utilisateurs[u["id"]] = Client.from_dict(u)
                    elif type_user == "gestionnaire":
                        flotte.utilisateurs[u["id"]] = Gestionnaire.from_dict(u)
                # Locations
                locs_data = persistence.charger_json(list, "data/locations.json")
                flotte.locations = {}
                for loc_dict in locs_data:
                    loc = Location.from_dict(loc_dict)
                    flotte.locations.setdefault(loc.client_id, []).append(loc)
                # Maintenances
                m_data = persistence.charger_json(list, "data/maintenances.json")
                flotte.maintenances = [Maintenance.from_dict(m) for m in m_data]
                print("JSON chargé pour véhicules, utilisateurs, locations et maintenances.")
            elif sub == "3":
                persistence.sauvegarder_csv(flotte.vehicules, "data/vehicules.csv")
                persistence.sauvegarder_csv(list(flotte.utilisateurs.values()), "data/utilisateurs.csv")
                print("CSV sauvegardé pour véhicules et utilisateurs.")
            elif sub == "4":
                flotte.vehicules = persistence.charger_csv(Vehicule, "data/vehicules.csv")
                utilisateurs = persistence.charger_csv(list, "data/utilisateurs.csv")
                flotte.utilisateurs = {}
                for u in utilisateurs:
                    type_user = u.get("type")
                    if type_user == "client":
                        flotte.utilisateurs[u["id"]] = Client.from_dict(u)
                    elif type_user == "gestionnaire":
                        flotte.utilisateurs[u["id"]] = Gestionnaire.from_dict(u)
                print("CSV chargé pour véhicules et utilisateurs.")

        # --- STATISTIQUES ---
        elif choix == "6":
            analytics.stats_vehicules(flotte.vehicules)

        # --- QUITTER ---
        elif choix == "7":
            break

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    os.makedirs("outputs/graphe", exist_ok=True)
    menu_principal()
