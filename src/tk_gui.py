import tkinter as tk
from tkinter import ttk, messagebox
from flotte import Flotte
from models import Vehicule, Client, Gestionnaire, Location, Maintenance
import persistence
import analytics
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion flotte véhicules électriques")
        self.root.geometry("900x600")
        self.flotte = Flotte()

        # --- Menu principal ---
        frame_menu = tk.Frame(root)
        frame_menu.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        tk.Label(frame_menu, text="Menu Principal", font=("Arial", 14, "bold")).pack(pady=5)

        tk.Button(frame_menu, text="1. Gérer les véhicules", width=25, command=self.menu_vehicules).pack(pady=2)
        tk.Button(frame_menu, text="2. Gérer les utilisateurs", width=25, command=self.menu_utilisateurs).pack(pady=2)
        tk.Button(frame_menu, text="3. Gérer les locations", width=25, command=self.menu_locations).pack(pady=2)
        tk.Button(frame_menu, text="4. Gérer la maintenance", width=25, command=self.menu_maintenance).pack(pady=2)
        tk.Button(frame_menu, text="5. Sauvegarde / Chargement", width=25, command=self.menu_sauvegarde).pack(pady=2)
        tk.Button(frame_menu, text="6. Statistiques & Visualisations", width=25, command=self.menu_stats).pack(pady=2)
        tk.Button(frame_menu, text="7. Quitter", width=25, command=root.destroy).pack(pady=2)

        # --- Frame central ---
        self.frame_central = tk.Frame(root)
        self.frame_central.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # ------------------------- Véhicules -------------------------
    def menu_vehicules(self):
        self.clear_frame()
        frame = self.frame_central
        tk.Label(frame, text="Gestion des véhicules", font=("Arial", 14, "bold")).pack(pady=5)

        # Treeview
        self.tree_vehicules = ttk.Treeview(frame, columns=("ID", "Marque", "Modèle", "Batterie", "Autonomie", "Charge", "Km", "Statut"), show="headings")
        for col in self.tree_vehicules["columns"]:
            self.tree_vehicules.heading(col, text=col)
        self.tree_vehicules.pack(fill=tk.BOTH, expand=True, pady=5)
        self.refresh_tree_vehicules()

        # Formulaire ajout
        form = tk.Frame(frame)
        form.pack(pady=5)
        tk.Label(form, text="Marque").grid(row=0, column=0)
        self.entry_marque = tk.Entry(form)
        self.entry_marque.grid(row=0, column=1)
        tk.Label(form, text="Modèle").grid(row=0, column=2)
        self.entry_modele = tk.Entry(form)
        self.entry_modele.grid(row=0, column=3)
        tk.Label(form, text="Batterie").grid(row=1, column=0)
        self.entry_batterie = tk.Entry(form)
        self.entry_batterie.grid(row=1, column=1)
        tk.Label(form, text="Autonomie").grid(row=1, column=2)
        self.entry_autonomie = tk.Entry(form)
        self.entry_autonomie.grid(row=1, column=3)

        tk.Button(frame, text="Ajouter véhicule", command=self.ajouter_vehicule).pack(pady=2)
        tk.Button(frame, text="Modifier véhicule sélectionné", command=self.modifier_vehicule).pack(pady=2)
        tk.Button(frame, text="Supprimer véhicule sélectionné", command=self.supprimer_vehicule).pack(pady=2)
        tk.Button(frame, text="Recharger Treeview", command=self.refresh_tree_vehicules).pack(pady=2)

    def ajouter_vehicule(self):
        try:
            marque = self.entry_marque.get()
            modele = self.entry_modele.get()
            batterie = int(self.entry_batterie.get())
            autonomie = int(self.entry_autonomie.get())
            v = Vehicule(marque, modele, batterie, autonomie)
            self.flotte.ajouter_vehicule(v)
            messagebox.showinfo("Succès", f"Véhicule ajouté ! ID {v.id}")
            self.refresh_tree_vehicules()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs correctement")

    def modifier_vehicule(self):
        selected = self.tree_vehicules.selection()
        if not selected:
            messagebox.showerror("Erreur", "Sélectionnez un véhicule")
            return
        vid = int(self.tree_vehicules.item(selected[0])["values"][0])
        marque = self.entry_marque.get() or None
        modele = self.entry_modele.get() or None
        batterie = self.entry_batterie.get()
        autonomie = self.entry_autonomie.get()
        kwargs = {}
        if marque: kwargs['marque'] = marque
        if modele: kwargs['modele'] = modele
        if batterie: kwargs['batterie'] = int(batterie)
        if autonomie: kwargs['autonomie'] = int(autonomie)
        self.flotte.modifier_vehicule(vid, **kwargs)
        messagebox.showinfo("Succès", "Véhicule modifié")
        self.refresh_tree_vehicules()

    def supprimer_vehicule(self):
        selected = self.tree_vehicules.selection()
        if not selected:
            messagebox.showerror("Erreur", "Sélectionnez un véhicule")
            return
        vid = int(self.tree_vehicules.item(selected[0])["values"][0])
        self.flotte.supprimer_vehicule(vid)
        messagebox.showinfo("Succès", "Véhicule supprimé")
        self.refresh_tree_vehicules()

    def refresh_tree_vehicules(self):
        for i in self.tree_vehicules.get_children():
            self.tree_vehicules.delete(i)
        for v in self.flotte.vehicules:
            self.tree_vehicules.insert("", "end", values=(v.id, v.marque, v.modele, v.batterie, v.autonomie, v.niveau_charge, v.kilometrage, v.statut))

    # ------------------------- Utilisateurs -------------------------
    def menu_utilisateurs(self):
        self.clear_frame()
        frame = self.frame_central
        tk.Label(frame, text="Gestion des utilisateurs", font=("Arial", 14, "bold")).pack(pady=5)

        self.tree_utilisateurs = ttk.Treeview(frame, columns=("ID","Nom","Email","Type"), show="headings")
        for col in self.tree_utilisateurs["columns"]:
            self.tree_utilisateurs.heading(col, text=col)
        self.tree_utilisateurs.pack(fill=tk.BOTH, expand=True, pady=5)
        self.refresh_tree_utilisateurs()

        form = tk.Frame(frame)
        form.pack(pady=5)
        tk.Label(form, text="Nom").grid(row=0,column=0)
        self.entry_nom = tk.Entry(form)
        self.entry_nom.grid(row=0,column=1)
        tk.Label(form, text="Email").grid(row=0,column=2)
        self.entry_email = tk.Entry(form)
        self.entry_email.grid(row=0,column=3)
        tk.Label(form, text="Type").grid(row=1,column=0)
        self.combo_type = ttk.Combobox(form, values=["client","gestionnaire"])
        self.combo_type.grid(row=1,column=1)
        tk.Label(form, text="Permis (si client)").grid(row=1,column=2)
        self.entry_permis = tk.Entry(form)
        self.entry_permis.grid(row=1,column=3)
        tk.Button(frame, text="Ajouter utilisateur", command=self.ajouter_utilisateur).pack(pady=2)
        tk.Button(frame, text="Recharger Treeview", command=self.refresh_tree_utilisateurs).pack(pady=2)

    def ajouter_utilisateur(self):
        nom = self.entry_nom.get()
        email = self.entry_email.get()
        type_user = self.combo_type.get()
        if type_user=="client":
            permis = self.entry_permis.get()
            u = Client(nom,email,permis)
        else:
            u = Gestionnaire(nom,email)
        self.flotte.ajouter_utilisateur(u)
        messagebox.showinfo("Succès", f"Utilisateur ajouté ! ID {u.id}")
        self.refresh_tree_utilisateurs()

    def refresh_tree_utilisateurs(self):
        for i in self.tree_utilisateurs.get_children():
            self.tree_utilisateurs.delete(i)
        for u in self.flotte.utilisateurs.values():
            type_u = "client" if isinstance(u, Client) else "gestionnaire"
            self.tree_utilisateurs.insert("", "end", values=(u.id,u.nom,u.email,type_u))

    # ------------------------- Locations -------------------------
    def menu_locations(self):
        self.clear_frame()
        frame = self.frame_central
        tk.Label(frame, text="Gestion des locations", font=("Arial", 14, "bold")).pack(pady=5)

        # Formulaire
        form = tk.Frame(frame)
        form.pack(pady=5)
        tk.Label(form, text="ID Client").grid(row=0,column=0)
        self.entry_loc_client = tk.Entry(form)
        self.entry_loc_client.grid(row=0,column=1)
        tk.Label(form, text="ID Véhicule").grid(row=0,column=2)
        self.entry_loc_vehicule = tk.Entry(form)
        self.entry_loc_vehicule.grid(row=0,column=3)
        tk.Label(form, text="Km parcourus").grid(row=1,column=0)
        self.entry_loc_km = tk.Entry(form)
        self.entry_loc_km.grid(row=1,column=1)
        tk.Label(form, text="Niveau charge (%)").grid(row=1,column=2)
        self.entry_loc_charge = tk.Entry(form)
        self.entry_loc_charge.grid(row=1,column=3)

        tk.Button(frame, text="Démarrer location", command=self.demarrer_location).pack(pady=2)
        tk.Button(frame, text="Terminer location", command=self.terminer_location).pack(pady=2)
        tk.Button(frame, text="Afficher historique client", command=self.historique_location).pack(pady=2)

    def demarrer_location(self):
        try:
            cid = int(self.entry_loc_client.get())
            vid = int(self.entry_loc_vehicule.get())
            self.flotte.demarrer_location(cid,vid)
            messagebox.showinfo("Succès","Location démarrée")
        except:
            messagebox.showerror("Erreur","Vérifiez les IDs")

    def terminer_location(self):
        try:
            cid = int(self.entry_loc_client.get())
            vid = int(self.entry_loc_vehicule.get())
            km = int(self.entry_loc_km.get())
            charge = int(self.entry_loc_charge.get())
            self.flotte.terminer_location(cid,vid,km,charge)
            messagebox.showinfo("Succès","Location terminée")
        except:
            messagebox.showerror("Erreur","Vérifiez les champs")

    def historique_location(self):
        try:
            cid = int(self.entry_loc_client.get())
            locs = self.flotte.locations.get(cid,[])
            if not locs:
                messagebox.showinfo("Info","Aucune location pour ce client")
                return
            hist = "\n".join([f"Véhicule {l.vehicule_id} | Début {l.date_debut} | Fin {l.date_fin}" for l in locs])
            messagebox.showinfo("Historique Locations", hist)
        except:
            messagebox.showerror("Erreur","Vérifiez ID client")

    # ------------------------- Maintenance -------------------------
    def menu_maintenance(self):
        self.clear_frame()
        frame = self.frame_central
        tk.Label(frame, text="Gestion maintenance", font=("Arial",14,"bold")).pack(pady=5)

        form = tk.Frame(frame)
        form.pack(pady=5)
        tk.Label(form,text="ID Véhicule").grid(row=0,column=0)
        self.entry_maint_veh = tk.Entry(form)
        self.entry_maint_veh.grid(row=0,column=1)
        tk.Label(form,text="Type opération").grid(row=0,column=2)
        self.entry_maint_type = tk.Entry(form)
        self.entry_maint_type.grid(row=0,column=3)
        tk.Label(form,text="Coût").grid(row=1,column=0)
        self.entry_maint_cout = tk.Entry(form)
        self.entry_maint_cout.grid(row=1,column=1)

        tk.Button(frame,text="Ajouter maintenance",command=self.ajouter_maintenance).pack(pady=2)
        tk.Button(frame,text="Valider maintenance",command=self.valider_maintenance).pack(pady=2)
        tk.Button(frame,text="Maintenance automatique",command=self.maintenance_auto).pack(pady=2)
        tk.Button(frame,text="Historique maintenance",command=self.historique_maintenance).pack(pady=2)

    def ajouter_maintenance(self):
        try:
            vid = int(self.entry_maint_veh.get())
            type_op = self.entry_maint_type.get()
            cout = float(self.entry_maint_cout.get())
            m = Maintenance(vid,type_op,cout)
            self.flotte.ajouter_maintenance(m)
            messagebox.showinfo("Succès","Maintenance ajoutée")
        except:
            messagebox.showerror("Erreur","Vérifiez les champs")

    def valider_maintenance(self):
        try:
            vid = int(self.entry_maint_veh.get())
            self.flotte.valider_maintenance(vid)
            messagebox.showinfo("Succès","Maintenance validée")
        except:
            messagebox.showerror("Erreur","Vérifiez ID véhicule")

    def maintenance_auto(self):
        self.flotte.verifier_maintenance()
        messagebox.showinfo("Succès","Maintenance automatique effectuée")

    def historique_maintenance(self):
        hist = "\n".join([f"Véhicule {m.vehicule_id} | {m.type_op} | Coût {m.cout} | Terminé: {m.terminee} | Date: {m.date}" for m in self.flotte.maintenances])
        messagebox.showinfo("Historique Maintenance", hist)

    # ------------------------- Sauvegarde / Chargement -------------------------
    def menu_sauvegarde(self):
        self.clear_frame()
        frame = self.frame_central
        tk.Label(frame,text="Sauvegarde / Chargement", font=("Arial",14,"bold")).pack(pady=5)
        tk.Button(frame,text="Sauvegarder JSON",command=self.sauvegarder_json).pack(pady=2)
        tk.Button(frame,text="Charger JSON",command=self.charger_json).pack(pady=2)
        tk.Button(frame,text="Sauvegarder CSV",command=self.sauvegarder_csv).pack(pady=2)
        tk.Button(frame,text="Charger CSV",command=self.charger_csv).pack(pady=2)

    def sauvegarder_json(self):
        os.makedirs("data",exist_ok=True)
        persistence.sauvegarder_json(self.flotte.vehicules,"data/vehicules.json")
        persistence.sauvegarder_json(list(self.flotte.utilisateurs.values()),"data/utilisateurs.json")
        all_locs=[]
        for locs in self.flotte.locations.values():
            all_locs.extend([loc.to_dict() for loc in locs])
        persistence.sauvegarder_json(all_locs,"data/locations.json")
        persistence.sauvegarder_json(self.flotte.maintenances,"data/maintenances.json")
        messagebox.showinfo("Succès","Données sauvegardées JSON")

    def charger_json(self):
        self.flotte.vehicules = persistence.charger_json(Vehicule,"data/vehicules.json")
        utilisateurs = persistence.charger_json(list,"data/utilisateurs.json")
        self.flotte.utilisateurs={}
        for u in utilisateurs:
            type_user = u.get("type")
            if type_user=="client":
                self.flotte.utilisateurs[u["id"]]=Client.from_dict(u)
            else:
                self.flotte.utilisateurs[u["id"]]=Gestionnaire.from_dict(u)
        locs_data = persistence.charger_json(list,"data/locations.json")
        self.flotte.locations={}
        for loc_dict in locs_data:
            loc = Location.from_dict(loc_dict)
            self.flotte.locations.setdefault(loc.client_id,[]).append(loc)
        m_data = persistence.charger_json(list,"data/maintenances.json")
        self.flotte.maintenances = [Maintenance.from_dict(m) for m in m_data]
        messagebox.showinfo("Succès","Données chargées JSON")
        self.refresh_tree_vehicules()
        self.refresh_tree_utilisateurs()

    def sauvegarder_csv(self):
        os.makedirs("data",exist_ok=True)
        persistence.sauvegarder_csv(self.flotte.vehicules,"data/vehicules.csv")
        persistence.sauvegarder_csv(list(self.flotte.utilisateurs.values()),"data/utilisateurs.csv")
        messagebox.showinfo("Succès","Données sauvegardées CSV")

    def charger_csv(self):
        self.flotte.vehicules = persistence.charger_csv(Vehicule,"data/vehicules.csv")
        utilisateurs = persistence.charger_csv(list,"data/utilisateurs.csv")
        self.flotte.utilisateurs={}
        for u in utilisateurs:
            type_user = u.get("type")
            if type_user=="client":
                self.flotte.utilisateurs[u["id"]]=Client.from_dict(u)
            else:
                self.flotte.utilisateurs[u["id"]]=Gestionnaire.from_dict(u)
        messagebox.showinfo("Succès","Données chargées CSV")
        self.refresh_tree_vehicules()
        self.refresh_tree_utilisateurs()

    # ------------------------- Statistiques -------------------------
    def menu_stats(self):
        self.clear_frame()
        frame=self.frame_central
        tk.Label(frame,text="Statistiques",font=("Arial",14,"bold")).pack(pady=5)
        fig = analytics.stats_vehicules(self.flotte.vehicules, gui=True)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ------------------------- Utilitaires -------------------------
    def clear_frame(self):
        for widget in self.frame_central.winfo_children():
            widget.destroy()

if __name__=="__main__":
    os.makedirs("data",exist_ok=True)
    root = tk.Tk()
    app = TkGUI(root)
    root.mainloop()
