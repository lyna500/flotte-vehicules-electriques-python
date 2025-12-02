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

        if choix == "1":
            marque = input("Marque : ")
            modele = input("Modèle : ")
            batterie = int(input("Capacité batterie (kWh) : "))
            autonomie = int(input("Autonomie (km) : "))
            v = Vehicule(marque, modele, batterie, autonomie)
            flotte.ajouter_vehicule(v)
            print("Véhicule ajouté !")
        elif choix == "2":
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
        elif choix == "6":
            analytics.stats_vehicules(flotte.vehicules)
        elif choix == "7":
            break

if __name__ == "__main__":
    menu_principal()

