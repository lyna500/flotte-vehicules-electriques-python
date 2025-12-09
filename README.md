Lyna SIDANE 
Bilal GHERRAS
LAMOUREUX Laura

# Projet Python – Gestion d'une flotte de véhicules électriques

Gestion d'une Flotte de Véhicules Électriques – Projet Python


Ce projet est une application Python complète permettant de gérer une flotte de véhicules électriques pour une entreprise de location courte durée.

Elle inclut :

-Programmation orientée objet (POO)

-Gestion des véhicules, utilisateurs, locations et maintenances

-Sauvegarde et chargement JSON/CSV

-Analyses statistiques (pandas)

-Graphiques (matplotlib)

-Interface en ligne de commande (CLI)

-Bonus : début d’intégration Tkinter (GUI)

1.  Fonctionnalités
Gestion des véhicules

Ajouter, modifier, supprimer un véhicule

Afficher la liste complète

Rechercher par :

ID

marque / modèle

autonomie

statut (disponible / loué / maintenance)

Attributs gérés :

ID auto-incrémenté

marque, modèle

capacité batterie (kWh)

autonomie estimée (km)

niveau de charge (%)

kilométrage

statut

Gestion des utilisateurs

Deux types :

Client

Gestionnaire

Chaque utilisateur possède :

ID unique

nom

email

type

(optionnel) permis / mode de paiement

Architecture POO :

Utilisateur
 ├── Client
 └── Gestionnaire

Gestion des locations

Un client peut louer un véhicule s’il est disponible.
Le système enregistre :

Au début :

statut → loué

date/heure de départ

estimation charge/km (optionnel)

Au retour :

date/heure de fin

kilomètres parcourus

niveau de charge mis à jour

pénalité si > 7 jours

Stockage :

{ id_client : [locations] }

Gestion de la maintenance

Le système enregistre :

date

type (batterie, freins, etc.)

coût

validation du gestionnaire

Maintenance automatique si :

kilométrage trop élevé

niveau de charge anormal

contrôle sécurité requis


2.  Structure du projet
flotte-vehicules/
│
├── src/
│   ├── models.py               # Classes POO (Vehicule, Utilisateur, Location, Maintenance)
│   ├── flotte.py               # Classe centrale Flotte
│   ├── persistance.py          # Sauvegarde & chargement JSON/CSV
│   ├── analytics.py            # Statistiques & graphiques pandas/matplotlib
│   ├── cli.py                  # Interface en ligne de commande (menu)
│   ├── charger_donnees_test.py # Données de test automatiques
│
├── data/                       # Données enregistrées
│   ├── vehicules.json
│   ├── utilisateurs.json
│   ├── locations.json
│   ├── maintenances.json
│
├── README.md
└── requirements.txt

3.  Concepts POO utilisés
-Encapsulation

Gestion protégée du niveau de charge via @property.

- Héritage

Utilisateur → Client, Gestionnaire.

- Polymorphisme

Méthodes comme afficher_resume() selon le type d’objet.

- Sérialisation

Méthodes to_dict() et from_dict() pour sauvegarde JSON/CSV.

- Gestion d’ID

Remise à jour des compteurs d’ID après rechargement (_id_counter).

4.  Sauvegarde & Chargement

Dans persistance.py :

Sauvegarde JSON
sauvegarder_json(objets, fichier)

Chargement JSON
charger_json(cls, fichier)

Sauvegarde CSV
sauvegarder_csv(objets, fichier)


Utilisation de __dict__ pour convertir objets → dictionnaires.

5.  Statistiques & Graphiques

Dans analytics.py :

nombre de véhicules par marque

kilométrage total par mois

locations par client

durée moyenne des locations

coût des maintenances

Les données sont analysées via :

pandas.read_csv()


Graphiques générés avec matplotlib.

6. Exécution (CLI)

Lancer l’application depuis la racine du projet :

python src/cli.py


Sous Windows :

py src/cli.py

Menu principal :
1. Gérer les véhicules
2. Gérer les utilisateurs
3. Gérer les locations
4. Gérer la maintenance
5. Sauvegarder / Charger les données
6. Statistiques & Visualisations
7. Quitter

7.  Données de test

Le fichier :

src/charger_donnees_test.py


Ajoute automatiquement :

3 véhicules

2 clients

1 gestionnaire

2 locations (dont une terminée)

Utile pour tester rapidement l’application.

8. Installation
Prérequis

Python 3.10 ou plus

pip installé

Installer les dépendances :
pip install pandas matplotlib


ou :

pip install -r requirements.txt

9.  Bibliothèques utilisées
Bibliothèque	Utilité
json:sauvegarde & chargement JSON
csv:export CSV
pandas:statistiques & tableaux
matplotlib:graphiques
datetime:gestion des dates
os	gestion:fichiers locaux
tkinter:(bonus)	interface graphique
unittest	tests

11.  Conclusion

Ce projet permet de :

gérer une flotte de véhicules électriques

appliquer pleinement la POO en Python

manipuler des données réelles (JSON/CSV)

produire des analyses et graphiques professionnels

proposer une architecture claire et évolutive

offrir une base solide pour une interface graphique (Tkinter)

Ce README constitue la documentation complète du projet.
