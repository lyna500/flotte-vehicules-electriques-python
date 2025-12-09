import json
import csv

def to_dict(obj):
    """Convertit un objet ou dict en dictionnaire exploitable."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "__dict__"):
        return dict(obj.__dict__)
    return {}  # Sécurité si cas particulier



def sauvegarder_json(objets, fichier):
    try:
        data = [to_dict(o) for o in objets]

        with open(fichier, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str)

        print(f"Sauvegarde JSON réussie : {fichier}")

    except Exception as e:
        print("Erreur sauvegarde JSON :", e)



def charger_json(cls, fichier):
    try:
        with open(fichier, 'r', encoding="utf-8") as f:
            data = json.load(f)

        objets = []

        for d in data:
            if isinstance(d, dict):
                try:
                    # tentative de reconstruction propre
                    objets.append(cls(**d))
                except TypeError:
                    # si certains attributs ne correspondent plus → garder dict
                    objets.append(d)
            else:
                objets.append(d)

        return objets

    except Exception as e:
        print("Erreur chargement JSON :", e)
        return []



def sauvegarder_csv(objets, fichier):
    try:
        if not objets:
            print("Aucun objet à sauvegarder en CSV.")
            return

        # conversion du premier élément pour déterminer les colonnes
        first = to_dict(objets[0])
        fieldnames = list(first.keys())

        with open(fichier, 'w', newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for o in objets:
                writer.writerow(to_dict(o))

        print(f"CSV sauvegardé avec succès : {fichier}")

    except Exception as e:
        print("Erreur CSV :", e)



def charger_csv(cls, fichier):
    try:
        with open(fichier, 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            objets = []

            for row in reader:
                # convertir valeurs numériques ou bool si besoin
                d = {k: convertir_valeur(v) for k, v in row.items()}
                
                try:
                    objets.append(cls(**d))
                except TypeError:
                    objets.append(d)

        return objets

    except Exception as e:
        print("Erreur CSV :", e)
        return []


# Utilitaire : conversion automatique des champs CSV
def convertir_valeur(val):
    """Convertit automatiquement int, float, bool, sinon laisse string."""
    if val.isdigit():
        return int(val)
    try:
        return float(val)
    except ValueError:
        pass
    if val.lower() in ("true", "false"):
        return val.lower() == "true"
    return val
