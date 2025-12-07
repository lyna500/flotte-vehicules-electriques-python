import json, csv

# --- JSON ---
def sauvegarder_json(objets, fichier):
    try:
        with open(fichier, 'w') as f:
            json.dump([o.__dict__ for o in objets], f, default=str)
        print(f"Sauvegarde JSON réussie : {fichier}")
    except Exception as e:
        print("Erreur sauvegarde JSON :", e)

def charger_json(cls, fichier):
    try:
        with open(fichier, 'r') as f:
            data = json.load(f)
            return [cls(**d) for d in data]
    except Exception as e:
        print("Erreur chargement JSON :", e)
        return []

# --- CSV ---
def sauvegarder_csv(objets, fichier):
    try:
        if not objets:
            return
        with open(fichier, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(objets[0].__dict__.keys()))
            writer.writeheader()
            for o in objets:
                writer.writerow(o.__dict__)
        print(f"CSV sauvegardé avec succès : {fichier}")
    except Exception as e:
        print("Erreur CSV :", e)
