from datetime import datetime

class Vehicule:
    _id_counter = 1

    def __init__(self, marque, modele, batterie, autonomie):
        self.id = Vehicule._id_counter
        Vehicule._id_counter += 1
        self.marque = marque
        self.modele = modele
        self.batterie = batterie
        self.autonomie = autonomie
        self._niveau_charge = 100
        self.kilometrage = 0
        self.statut = "disponible"

    def afficher_resume(self):
        return f"{self.id} - {self.marque} {self.modele} | Statut: {self.statut} | Km: {self.kilometrage} | Charge: {self._niveau_charge}%"

    @property
    def niveau_charge(self):
        return self._niveau_charge

    @niveau_charge.setter
    def niveau_charge(self, value):
        if 0 <= value <= 100:
            self._niveau_charge = value
        else:
            raise ValueError("Niveau de charge doit être entre 0 et 100")

class Utilisateur:
    _id_counter = 1

    def __init__(self, nom, email):
        self.id = Utilisateur._id_counter
        Utilisateur._id_counter += 1
        self.nom = nom
        self.email = email

    def afficher_resume(self):
        return f"{self.id} - {self.nom} ({self.email})"

class Client(Utilisateur):
    def __init__(self, nom, email, permis):
        super().__init__(nom, email)
        self.permis = permis

class Gestionnaire(Utilisateur):
    def __init__(self, nom, email):
        super().__init__(nom, email)

class Location:
    def __init__(self, client_id, vehicule_id, date_debut=None):
        self.client_id = client_id
        self.vehicule_id = vehicule_id
        self.date_debut = date_debut or datetime.now()
        self.date_fin = None

    def terminer(self):
        self.date_fin = datetime.now()

class Maintenance:
    def __init__(self, vehicule_id, type_op, cout, date=None):
        self.vehicule_id = vehicule_id
        self.type_op = type_op
        self.cout = cout
        self.date = date or datetime.now()
        self.terminee = False

    def valider(self):
        self.terminee = True
