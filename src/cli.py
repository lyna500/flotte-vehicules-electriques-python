from flotte import Flotte
from models import Vehicule, Client, Gestionnaire
import persistence
import analytics

def menu_principal():
    flotte = Flotte()
    while True:
        print("""
1. Gérer les véhicules
2. Gérer les utilisateurs
3. Gérer les locations
4. Gérer la maintenance
5. Sauvegarder / Charger
6. Statistiques
7. Quitter
        """)
        choix = input("Votre choix : ")

        # --- Véhicules ---
        if choix == "1":
            print("1: Ajouter véhicule | 2: Afficher véhicules")
            sub = input("Choix : ")
            if sub == "1":
                marque = input("Marque : ")
                modele = input("Modèle : ")
                batterie = int(input("Batterie (kWh) : "))
                autonomie = int(input("Autonomie (km) : "))
                v = Vehicule(marque, modele, batterie, autonomie)
                flotte.ajouter_vehicule(v)
                print("Véhicule ajouté !")
            elif sub == "2":
                flotte.afficher_vehicules()

        # --- Utilisateurs ---
        elif choix == "2":
            print("1: Ajouter utilisateur | 2: Afficher utilisateurs")
            sub = input("Choix : ")
            if sub == "1":
                nom = input("Nom : ")
                email = input("Email : ")
                type_user = input("Type (client/gestionnaire) : ").lower()
                if type_user == "client":
                    permis = input("Permis : ")
                    u = Client(nom, email, permis)
                else:
                    u = Gestionnaire(nom, email)
                flotte.ajouter_utilisateur(u)
                print("Utilisateur ajouté !")
            elif sub == "2":
                flotte.afficher_utilisateurs()

        # --- Locations ---
        elif choix == "3":
            print("1: Démarrer location | 2: Terminer location")
            sub = input("Choix : ")
            if sub == "1":
                client_id = int(input("ID client : "))
                vehicule_id = int(input("ID véhicule : "))
                flotte.demarrer_location(client_id, vehicule_id)
            elif sub == "2":
                client_id = int(input("ID client : "))
                vehicule_id = int(input("ID véhicule : "))
                km = int(input("Km parcourus : "))
                charge = int(input("Niveau de charge (%) : "))
                flotte.terminer_location(client_id, vehicule_id, km, charge)

        # --- Maintenance ---
        elif choix == "4":
            print("1: Ajouter maintenance | 2: Valider maintenance")
            sub = input("Choix : ")
            if sub == "1":
                vehicule_id = int(input("ID véhicule : "))
                type_op = input("Type maintenance : ")
                cout = float(input("Coût : "))
                from models import Maintenance
                m = Maintenance(vehicule_id, type_op, cout)
                flotte.ajouter_maintenance(m)
            elif sub == "2":
                vehicule_id = int(input("ID véhicule : "))
                flotte.valider_maintenance(vehicule_id)

        # --- Sauvegarde / Chargement ---
        elif choix == "5":
            print("1: Sauvegarder JSON | 2: Charger JSON")
            sub = input("Choix : ")
            if sub == "1":
                persistence.sauvegarder_json(flotte.vehicules, "data/vehicules.json")
                persistence.sauvegarder_json(list(flotte.utilisateurs.values()), "data/utilisateurs.json")

            elif sub == "2":
                flotte.vehicules = persistence.charger_json(Vehicule, "data/vehicules.json") 
                utilisateurs = persistence.charger_json(dict, "data/utilisateurs.json")
                flotte.utilisateurs = {u["id"]: u for u in utilisateurs}


        # --- Statistiques ---
        elif choix == "6":
            analytics.stats_vehicules(flotte.vehicules)

        elif choix == "7":
            break

if __name__ == "__main__":
    menu_principal()

