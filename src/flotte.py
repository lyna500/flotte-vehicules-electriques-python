from models import Vehicule, Client, Gestionnaire, Location, Maintenance

class Flotte:
    def __init__(self):
        self.vehicules = []
        self.utilisateurs = {}
        self.locations = {}  # clé = client_id, valeur = liste de Location
        self.maintenances = []

    # --- Véhicules ---
    def ajouter_vehicule(self, vehicule):
        self.vehicules.append(vehicule)

    def supprimer_vehicule(self, vehicule_id):
        self.vehicules = [v for v in self.vehicules if v.id != vehicule_id]

    def rechercher_vehicule_par_id(self, vehicule_id):
        for v in self.vehicules:
            if v.id == vehicule_id:
                return v
        return None

    def afficher_vehicules(self):
        for v in self.vehicules:
            print(v.afficher_resume())

    # --- Utilisateurs ---
    def ajouter_utilisateur(self, utilisateur):
        self.utilisateurs[utilisateur.id] = utilisateur

    def rechercher_utilisateur_par_id(self, user_id):
        return self.utilisateurs.get(user_id, None)

    # --- Locations ---
    def demarrer_location(self, client_id, vehicule_id):
        vehicule = self.rechercher_vehicule_par_id(vehicule_id)
        if vehicule and vehicule.statut == "disponible":
            vehicule.statut = "loué"
            loc = Location(client_id, vehicule_id)
            self.locations.setdefault(client_id, []).append(loc)
            print(f"Location démarrée : {vehicule.afficher_resume()}")
        else:
            print("Véhicule non disponible")

    def terminer_location(self, client_id, vehicule_id, km_parcourus, niveau_charge):
        locs = self.locations.get(client_id, [])
        for loc in locs:
            if loc.vehicule_id == vehicule_id and loc.date_fin is None:
                loc.date_fin = datetime.now()
                vehicule = self.rechercher_vehicule_par_id(vehicule_id)
                vehicule.kilometrage += km_parcourus
                vehicule.niveau_charge = niveau_charge
                vehicule.statut = "disponible"
                print(f"Location terminée : {vehicule.afficher_resume()}")
                return
        print("Location non trouvée ou déjà terminée")

    # --- Maintenances ---
    def ajouter_maintenance(self, maintenance):
        self.maintenances.append(maintenance)

    def valider_maintenance(self, vehicule_id):
        for m in self.maintenances:
            if m.vehicule_id == vehicule_id and not m.terminee:
                m.terminee = True
                vehicule = self.rechercher_vehicule_par_id(vehicule_id)
                vehicule.statut = "disponible"
                print(f"Maintenance validée pour {vehicule.afficher_resume()}")

