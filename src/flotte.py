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
        if marque:
            result = [v for v in result if v.marque.lower() == marque.lower()]
        if modele:
            result = [v for v in result if v.modele.lower() == modele.lower()]
        if autonomie:
            result = [v for v in result if v.autonomie >= autonomie]
        if statut:
            result = [v for v in result if v.statut.lower() == statut.lower()]
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
    def demarrer_location(self, client_id, vehicule_id, estimation_km=None, estimation_charge=None):
        vehicule = self.rechercher_vehicule_par_id(vehicule_id)
        if not vehicule:
            print("Véhicule introuvable.")
            return
        if vehicule.statut != "disponible":
            print("Véhicule non disponible.")
            return

        vehicule.statut = "loué"
        loc = Location(client_id, vehicule_id)
        loc.estimation_km = estimation_km
        loc.estimation_charge = estimation_charge
        self.locations.setdefault(client_id, []).append(loc)

        print("Location démarrée :")
        print(f"- Véhicule : {vehicule.marque} {vehicule.modele} (ID {vehicule.id})")
        print(f"- Statut : {vehicule.statut}")
        print(f"- Date/heure départ : {loc.date_debut}")
        if estimation_km:
            print(f"- Estimation km : {estimation_km}")
        if estimation_charge:
            print(f"- Estimation charge : {estimation_charge}%")

    def terminer_location(self, client_id, vehicule_id, km_parcourus, niveau_charge, jours_max=7, penalite_par_jour=100):
        locs = self.locations.get(client_id, [])
        for loc in locs:
            if loc.vehicule_id == vehicule_id and loc.date_fin is None:
                loc.terminer()
                vehicule = self.rechercher_vehicule_par_id(vehicule_id)
                vehicule.kilometrage += km_parcourus
                vehicule.niveau_charge = max(0, min(100, niveau_charge))
                vehicule.statut = "disponible"

                duree_jours = (loc.date_fin - loc.date_debut).days
                loc.penalite = 0
                if duree_jours > jours_max:
                    loc.penalite = (duree_jours - jours_max) * penalite_par_jour

                print("Location terminée :")
                print(f"- Véhicule : {vehicule.marque} {vehicule.modele} (ID {vehicule.id})")
                print(f"- Statut : {vehicule.statut}")
                print(f"- Km parcourus : {km_parcourus}")
                print(f"- Niveau de charge : {vehicule.niveau_charge}%")
                print(f"- Date/heure retour : {loc.date_fin}")
                if loc.penalite > 0:
                    print(f"- Attention : dépassement {jours_max} jours. Pénalité = {loc.penalite} €")
                return
        print("Location non trouvée ou déjà terminée.")

    # --- Maintenance ---
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

    # --- Vérification maintenance automatique ---
    def verifier_maintenance(self, km_seuil=10000, charge_min=20):
        for v in self.vehicules:
            if v.statut == "disponible":
                besoin = False
                raison = []
                if v.kilometrage > km_seuil:
                    besoin = True
                    raison.append("kilométrage élevé")
                if v.niveau_charge < charge_min:
                    besoin = True
                    raison.append("niveau de charge faible")
                if besoin:
                    m = Maintenance(v.id, type_op="contrôle automatique", cout=0)
                    self.ajouter_maintenance(m)
                    print(f"Véhicule {v.id} envoyé en maintenance ({', '.join(raison)})")


    def afficher_vehicules_en_maintenance(self):
        for v in self.vehicules:
            if v.statut == "maintenance":
                print(v.afficher_resume())

    def afficher_logs_maintenance(self):
        for m in self.maintenances:
            etat = "terminée" if m.terminee else "en cours"
            print(f"Véhicule {m.vehicule_id} | {m.type_op} | Coût {m.cout} | {m.date} | {etat}")

