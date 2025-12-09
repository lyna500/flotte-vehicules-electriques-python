
# Projet Python – Gestion d'une flotte de véhicules électriques



Ce projet est une application complète en Python permettant de gérer une flotte de véhicules électriques pour une entreprise de location courte durée.
L’application utilise :

Programmation orientée objet (POO)

Sauvegarde/Chargement JSON & CSV

Analyse et visualisation via pandas & matplotlib

Menu CLI interactif

(Bonus) Interface graphique Tkinter

 1. Fonctionnalités principales
 
 🔹Gestion des véhicules:
 
 Ajouter, modifier, supprimer un véhicule.
Afficher tous les véhicules.
Rechercher un véhicule par :ID ,modèle,autonomie,statut (disponible / loué / maintenance)

Caractéristiques gérées :ID unique auto-incrémenté,marque, modèle,capacité batterie et autonomie estimée,niveau de charge (%),kilométrage,statut du véhicule

🔹 Gestion des utilisateurs

Deux types d’utilisateurs :

Client (locataire)

Gestionnaire

Chaque utilisateur possède :

un identifiant unique

nom complet

email

type (Client ou Gestionnaire)

données optionnelles : permis, mode de paiement

Architecture avec héritage :

Utilisateur
 ├── Client
 └── Gestionnaire

🔹 Gestion des locations

Un client peut louer un véhicule disponible.

Au début :

le véhicule passe en statut loué,

date/heure de départ enregistrées.

Au retour :

date/heure de fin enregistrées

kilomètres ajoutés

niveau de charge mis à jour

pénalité si durée > 7 jours

Les locations sont stockées sous forme de dictionnaire :

{ id_client : [liste des locations] }

🔹 Gestion de la maintenance

Enregistrer des opérations : date, type, coût.

Déclenchement automatique si :

kilométrage trop élevé

sécurité insuffisante

niveau de charge anormal

Les gestionnaires valident et clôturent les maintenances.

Remarque importante à dire en soutenance :

La maintenance automatique fonctionne mais peut créer plusieurs maintenances identiques si appelée plusieurs fois. Amélioration prévue : vérifier si une maintenance similaire existe déjà.

 2. Structure du projet
flotte-vehicules/
│
├── src/
│   ├── models.py          # Classes POO : Vehicule, Utilisateur, Client, Gestionnaire, Location, Maintenance
│   ├── flotte.py          # Classe Flotte centrale
│   ├── persistance.py     # Sauvegarde / Chargement JSON & CSV
│   ├── analytics.py       # Analyse de données & Graphiques (pandas/matplotlib)
│   ├── cli.py             # Menu interactif (interface en ligne de commande)
│   ├── charger_donnees_test.py   # Données de test
│
├── data/
│   ├── vehicules.json
│   ├── utilisateurs.json
│   ├── locations.json
│   ├── maintenances.json
│
├── README.md
└── requirements.txt




 3. Points techniques clés (POO)
 Encapsulation & @property

Le niveau de charge est protégé :

@property
def niveau_charge(self):
    return self._niveau_charge

@niveau_charge.setter
def niveau_charge(self, val):
    self._niveau_charge = max(0, min(100, val))




Sérialisation : to_dict() et from_dict()

Les objets sont convertis en dictionnaires pour être enregistrés.

def to_dict(self):
    return {
        "id": self.id,
        "marque": self.marque,
        ...
    }


Et reconstruits avec :

@classmethod
def from_dict(cls, data):
    return cls(**data)


Ce que ça permet :

sauvegarder facilement en JSON/CSV

charger les objets complets dans la flotte


Lorsque from_dict() recharge un objet avec un ID déjà défini, il faut ensuite mettre :

Vehicule._id_counter = max(id existants) + 1


Pour éviter les collisions d’ID quand on ajoute de nouveaux objets.

 4. Sauvegarde & Chargement

Fonctions dans persistance.py :

JSON
sauvegarder_json(objets, fichier)
charger_json(cls, fichier)

CSV
sauvegarder_csv(objets, fichier)


Technique utilisée :
o.__dict__ ou o.to_dict() pour transformer objets → dictionnaires.

5. Statistiques & Visualisation (pandas & matplotlib)

Dans analytics.py, plusieurs analyses sont proposées :

nombre de véhicules par marque

kilométrage total par mois

locations par client

durée moyenne des locations

coûts de maintenance par type

Graphiques produits :

histogrammes

camemberts

barres verticales

Les données sont chargées avec :

df = pd.read_csv("data/vehicules.csv")

 6. Interface en ligne de commande (CLI)

L’application se lance avec :

python src/cli.py


Menu principal :

1. Gérer les véhicules
2. Gérer les utilisateurs
3. Gérer les locations
4. Gérer la maintenance
5. Sauvegarder / Charger
6. Statistiques & Visualisations
7. Quitter

 

 8. Installation & Exécution

Python 3.10+

pip (installé par défaut avec Python)

✔ Cloner ou télécharger le projet
git clone https://github.com/<votre_repo>/flotte-vehicules-electriques-python.git
cd flotte-vehicules-electriques-python


Si vous avez téléchargé un ZIP, extraire puis entrer dans le dossier :

cd flotte-vehicules-electriques-python-main

. Installation des dépendances

Le projet utilise ces modules externes :

Module	Utilité
pandas	Manipulation et export de données
matplotlib	Graphiques & statistiques
csv	Gestion de fichiers CSV
json	Sauvegarde et chargement JSON

Installer les dépendances :

pip install pandas matplotlib


Ou via un fichier requirements.txt (si fourni) :

pip install -r requirements.txt

. Exécution de l’application

Depuis la racine du projet, lancer :

python src/cli.py


Sur Windows PowerShell :

py src/cli.py


 11. Conclusion

Ce projet met en pratique :

Programmation orientée objet complète

Gestion réelle de données (JSON/CSV)

Analyses et visualisations professionnelles

Menu CLI solide

Modularité du code

Possibilité d’extension en GUI (Tkinter)

L’application fournit une solution fonctionnelle et évolutive pour gérer une flotte de véhicules électriques.

Bibliothèque	
json:Sauvegarde et chargement des données en JSON (véhicules, utilisateurs, locations…)
csv:Sauvegarde et chargement des données en CSV pour les tableaux ou exports Excel
matplotlib.pyplot:Création de graphiques (barres, camemberts, lignes) pour visualiser les statistiques
pandas (optionnel):Manipulation rapide et facile des tableaux de données pour filtrer, trier ou calculer des statistiques
datetime:Gestion des dates et heures (début et fin des locations, calcul de pénalités)
os (parfois):Gestion des chemins de fichiers, vérification si un fichier existe
unittest (pour test.py):Pour tester automatiquement que les classes et fonctions fonctionnent correctement
math (optionnel):Calculs mathématiques, par exemple pour l’autonomie ou les pourcentages

