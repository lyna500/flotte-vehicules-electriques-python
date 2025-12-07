from datetime import datetime

# ------------------ Véhicule ------------------
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
        return f"{self.id} - {self.marque} {self.modele} | Statut: {self.statut} | Km: {self.kilometrage} | Charge: {self.niveau_charge}%"

    @property
    def niveau_charge(self):
        return self._niveau_charge

    @niveau_charge.setter
    def niveau_charge(self, value):
        if 0 <= value <= 100:
            self._niveau_charge = value
        else:
            raise ValueError("Niveau de charge doit être entre 0 et 100")

    def to_dict(self):
        return {
            "id": self.id,
            "marque": self.marque,
            "modele": self.modele,
            "batterie": self.batterie,
            "autonomie": self.autonomie,
            "niveau_charge": self._niveau_charge,
            "kilometrage": self.kilometrage,
            "statut": self.statut
        }

    @classmethod
    def from_dict(cls, data):
        v = cls(data["marque"], data["modele"], data["batterie"], data["autonomie"])
        v.id = data["id"]
        v._niveau_charge = data.get("niveau_charge", 100)
        v.kilometrage = data.get("kilometrage", 0)
        v.statut = data.get("statut", "disponible")
        return v

# ------------------ Utilisateur ------------------
class Utilisateur:
    _id_counter = 1

    def __init__(self, nom, email):
        self.id = Utilisateur._id_counter
        Utilisateur._id_counter += 1
        self.nom = nom
        self.email = email

    def afficher_resume(self):
        return f"{self.id} - {self.nom} ({self.email})"

    def to_dict(self):
        return {"id": self.id, "nom": self.nom, "email": self.email}

    @classmethod
    def from_dict(cls, data):
        u = cls(data["nom"], data["email"])
        u.id = data["id"]
        return u

class Client(Utilisateur):
    def __init__(self, nom, email, permis):
        super().__init__(nom, email)
        self.permis = permis

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "client"
        data["permis"] = self.permis
        return data

    @classmethod
    def from_dict(cls, data):
        u = cls(data["nom"], data["email"], data["permis"])
        u.id = data["id"]
        return u

class Gestionnaire(Utilisateur):
    def __init__(self, nom, email):
        super().__init__(nom, email)

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "gestionnaire"
        return data

    @classmethod
    def from_dict(cls, data):
        u = cls(data["nom"], data["email"])
        u.id = data["id"]
        return u

# ------------------ Location ------------------
class Location:
    def __init__(self, client_id, vehicule_id, date_debut=None):
        self.client_id = client_id
        self.vehicule_id = vehicule_id
        self.date_debut = date_debut or datetime.now()
        self.date_fin = None
        self.estimation_km = None
        self.estimation_charge = None

    def terminer(self):
        self.date_fin = datetime.now()

    def to_dict(self):
        return {
            "client_id": self.client_id,
            "vehicule_id": self.vehicule_id,
            "date_debut": self.date_debut.isoformat(),
            "date_fin": self.date_fin.isoformat() if self.date_fin else None,
            "estimation_km": self.estimation_km,
            "estimation_charge": self.estimation_charge
        }

    @classmethod
    def from_dict(cls, data):
        loc = cls(data["client_id"], data["vehicule_id"], datetime.fromisoformat(data["date_debut"]))
        loc.date_fin = datetime.fromisoformat(data["date_fin"]) if data["date_fin"] else None
        loc.estimation_km = data.get("estimation_km")
        loc.estimation_charge = data.get("estimation_charge")
        return loc

# ------------------ Maintenance ------------------
class Maintenance:
    def __init__(self, vehicule_id, type_op, cout, date=None):
        self.vehicule_id = vehicule_id
        self.type_op = type_op
        self.cout = cout
        self.date = date or datetime.now()
        self.terminee = False

    def valider(self):
        self.terminee = True

    def to_dict(self):
        return {
            "vehicule_id": self.vehicule_id,
            "type_op": self.type_op,
            "cout": self.cout,
            "date": self.date.isoformat(),
            "terminee": self.terminee
        }

    @classmethod
    def from_dict(cls, data):
        m = cls(data["vehicule_id"], data["type_op"], data["cout"], datetime.fromisoformat(data["date"]))
        m.terminee = data.get("terminee", False)
        return m
