from models import Vehicule, Client, Gestionnaire, Location, Maintenance
from datetime import datetime

class Flotte:
    def __init__(self):
        self.vehicules = []
        self.utilisateurs = {}
        self.locations = {}  # clé = client_id, valeur = liste de Location
        self.maintenances = []

    # --- Véhicules ---
    def ajouter_vehicule(self, vehicule):
        self.vehicules.append(vehicule)

    def modifier_vehicule(self, vehicule_id, **kwargs):
        v = self.rechercher_vehicule_par_id(vehicule_id)
        if not v:
            return False
        for k, val in kwargs.items():
            if hasattr(v, k):
                setattr(v, k, val)
        return True

    def supprimer_vehicule(self, vehicule_id):
        self.vehicules = [v for v in self.vehicules if v.id != vehicule_id]

    def rechercher_vehicule_par_id(self, vehicule_id):
        for v in self.vehicules:
            if v.id == vehicule_id:
                return v
        return None

    def rechercher_vehicule(self, marque=None, modele=None, autonomie=None, statut=None):
        result = self.vehicules
        if marque: result = [v for v in result if v.marque.lower() == marque.lower()]
        if modele: result = [v for v in result if v.modele.lower() == modele.lower()]
        if autonomie: result = [v for v in result if v.autonomie >= autonomie]
        if statut: result = [v for v in result if v.statut.lower() == statut.lower()]
        return result

    def afficher_vehicules(self):
        for v in self.vehicules:
            print(v.afficher_resume())

    # --- Utilisateurs ---
    def ajouter_utilisateur(self, utilisateur):
        self.utilisateurs[utilisateur.id] = utilisateur

    def rechercher_utilisateur_par_id(self, user_id):
        return self.utilisateurs.get(user_id, None)

    def afficher_utilisateurs(self):
        for u in self.utilisateurs.values():
            print(u.afficher_resume())

    # --- Locations ---
    def demarrer_location(self, client_id, vehicule_id):
        vehicule = self.rechercher_vehicule_par_id(vehicule_id)
        if not vehicule:
            print("Véhicule introuvable.")
            return
        if vehicule.statut != "disponible":
            print("Véhicule non disponible.")
            return
        vehicule.statut = "loué"
        loc = Location(client_id, vehicule_id)
        self.locations.setdefault(client_id, []).append(loc)
        print(f"Location démarrée : {vehicule.afficher_resume()}")

    def terminer_location(self, client_id, vehicule_id, km_parcourus, niveau_charge):
        locs = self.locations.get(client_id, [])
        for loc in locs:
            if loc.vehicule_id == vehicule_id and loc.date_fin is None:
                loc.terminer()
                vehicule = self.rechercher_vehicule_par_id(vehicule_id)
                vehicule.kilometrage += km_parcourus
                vehicule.niveau_charge = niveau_charge
                vehicule.statut = "disponible"
                print(f"Location terminée : {vehicule.afficher_resume()}")
                return
        print("Location non trouvée ou déjà terminée.")

    # --- Maintenances ---
    def ajouter_maintenance(self, maintenance):
        self.maintenances.append(maintenance)
        vehicule = self.rechercher_vehicule_par_id(maintenance.vehicule_id)
        if vehicule:
            vehicule.statut = "maintenance"
        print(f"Maintenance ajoutée pour {vehicule.afficher_resume()}")

    def valider_maintenance(self, vehicule_id):
        for m in self.maintenances:
            if m.vehicule_id == vehicule_id and not m.terminee:
                m.valider()
                vehicule = self.rechercher_vehicule_par_id(vehicule_id)
                if vehicule:
                    vehicule.statut = "disponible"
                print(f"Maintenance validée pour {vehicule.afficher_resume()}")

