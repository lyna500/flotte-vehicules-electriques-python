from models import Vehicule, Client, Gestionnaire, Location, Maintenance
from datetime import datetime

def charger_donnees_test(flotte):

    v1 = Vehicule("Tesla", "Model Y", 78, 505)
    v1.kilometrage = 12000
    v1.niveau_charge = 85

    v2 = Vehicule("Kia", "EV6", 77, 480)
    v2.kilometrage = 31000
    v2.niveau_charge = 62

    v3 = Vehicule("Volkswagen", "ID.3", 58, 420)
    v3.kilometrage = 54000
    v3.niveau_charge = 40

    flotte.ajouter_vehicule(v1)
    flotte.ajouter_vehicule(v2)
    flotte.ajouter_vehicule(v3)

    c1 = Client("Emma Leroy", "emma@example.com", "PERMIS-AZ12")
    c2 = Client("Louis Morel", "louis@example.com", "PERMIS-BX34")
    g1 = Gestionnaire("Admin Système", "admin@example.com")

    flotte.ajouter_utilisateur(c1)
    flotte.ajouter_utilisateur(c2)
    flotte.ajouter_utilisateur(g1)

    loc1 = Location(c1.id, v1.id, datetime(2025, 1, 3, 9, 0))
    loc1.date_fin = datetime(2025, 1, 8, 10, 30)
    loc1.estimation_km = 300
    loc1.estimation_charge = 70
    v1.kilometrage += 320
    flotte.locations.setdefault(c1.id, []).append(loc1)

    loc2 = Location(c2.id, v2.id, datetime(2025, 2, 12, 14, 0))
    loc2.estimation_km = 150
    loc2.estimation_charge = 60
    v2.statut = "loué"
    flotte.locations.setdefault(c2.id, []).append(loc2)