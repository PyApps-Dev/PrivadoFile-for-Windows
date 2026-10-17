#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#############################################################################
#               PROJECT   :   CryptoFile                                    #
#               GROUP     :   Quantum Software                              #
#               VERSION   :   1.0.0                                         #
#               LICENSE   :   GNU GPL v3                                    #
#               AUTHOR    :   Youssef B.                                    #
#               YEAR      :   2026                                          #
#               COPYRIGHT :   © 2026 Quantum Software. All rights reserved. #
#############################################################################

# CryptoFile™

import os
import threading
import customtkinter as ctk
from cryptography.fernet import Fernet
from tkinter import filedialog, messagebox

def cryptofile():

  cryptofile_window = ctk.CTk()
  cryptofile_window.title("CryptoFile")
  cryptofile_window.resizable(False, False)

  width = 520
  height = 620
  screen_width = cryptofile_window.winfo_screenwidth()
  screen_height = cryptofile_window.winfo_screenheight()
  x = (screen_width - width) // 2
  y = (screen_height - height) // 2
  cryptofile_window.geometry(f"{width}x{height}+{x}+{y}")

  ctk.set_appearance_mode("System")
  ctk.set_default_color_theme("blue")

  welcome_label = ctk.CTkLabel(cryptofile_window, text = "CryptoFile", font = ("Arial", 40, "bold"), text_color = "#E0E0E0")
  welcome_label.pack(pady = (15, 5))

  welcome_description_label = ctk.CTkLabel(cryptofile_window, text = "Encrypt and decrypt your sensitive data using encryption keys", font = ("Arial", 15), text_color = "#949494")
  welcome_description_label.pack(pady = 2)

  chemin_fichier_val = {"path": ""}
  chemin_cle_val = {"path": ""}

  def choisir_fichier():
    chemin = filedialog.askopenfilename(parent=cryptofile_window, title="Choisir le fichier à chiffrer/déchiffrer")
    if chemin:
      chemin_fichier_val["path"] = chemin
      label_fichier_path.configure(
          text=os.path.basename(chemin), text_color="#FFFFFF")
      statut_label.configure(text="📁 Fichier sélectionné !", text_color="green")

  btn_fichier = ctk.CTkButton(
      cryptofile_window,
      text="📄 1. Choisir le Fichier Cible",
      command=choisir_fichier,
      font=ctk.CTkFont(size=12, weight="bold"),
      width=300,
      height=35,
  )
  btn_fichier.pack(pady=(15, 2))

  label_fichier_path = ctk.CTkLabel(
      cryptofile_window,
      text="Aucun fichier choisi",
      font=ctk.CTkFont(size=11),
      wraplength=450,
      text_color="#A0A0A0",
  )
  label_fichier_path.pack(pady=2)

  def generer_cle():
    cle = Fernet.generate_key()
    chemin_sauvegarde = filedialog.asksaveasfilename(
        parent=cryptofile_window,
        defaultextension=".key",
        filetypes=[("Fichiers Clé", "*.pfkey")],
        title="Enregistrer la nouvelle clé secrète",
      )
    if chemin_sauvegarde:
      with open(chemin_sauvegarde, "wb") as f_cle:
        f_cle.write(cle)
      chemin_cle_val["path"] = chemin_sauvegarde
      label_cle_path.configure(
          text=os.path.basename(chemin_sauvegarde), text_color="#4CAF50"
      )
      statut_label.configure(
          text="🔑 Nouvelle clé générée et enregistrée !", text_color="green"
      )

  def charger_cle():
    chemin = filedialog.askopenfilename(
        parent=cryptofile_window, filetypes=[("Fichiers Clé", "*.pfkey")], title="Sélectionner une clé .key"
    )
    if chemin:
      chemin_cle_val["path"] = chemin
      label_cle_path.configure(
          text=os.path.basename(chemin), text_color="#FFFFFF"
      )
      statut_label.configure(text="🔑 Clé .pfkey chargée avec succès !", text_color="green")

  cadre_cles = ctk.CTkFrame(cryptofile_window, fg_color="transparent")
  cadre_cles.pack(pady=10)

  btn_generer_cle = ctk.CTkButton(
      cadre_cles,
      text="✨ Générer une clé .key",
      command=generer_cle,
      fg_color="#2E7D32",
      hover_color="#1B5E20",
      font=ctk.CTkFont(size=11, weight="bold"),
      width=140,
      height=30,
  )
  btn_generer_cle.pack(side="left", padx=5)

  btn_charger_cle = ctk.CTkButton(
      cadre_cles,
      text="📂 Charger une clé .key",
      command=charger_cle,
      fg_color="#1565C0",
      hover_color="#0D47A1",
      font=ctk.CTkFont(size=11, weight="bold"),
      width=140,
      height=30,
  )
  btn_charger_cle.pack(side="left", padx=5)

  label_cle_path = ctk.CTkLabel(
      cryptofile_window,
      text="Aucune clé .key sélectionnée",
      font=ctk.CTkFont(size=11),
      wraplength=450,
      text_color="#A0A0A0",
  )
  label_cle_path.pack(pady=2)

  # Barre de progression
  cadre_barre = ctk.CTkFrame(cryptofile_window, fg_color="transparent", height=20)
  cadre_barre.pack(pady=5, fill="x")
  cadre_barre.pack_propagate(False)

  progress_bar = ctk.CTkProgressBar(cadre_barre, width=350, height=12)
  progress_bar.set(0)

  statut_label = ctk.CTkLabel(
      cryptofile_window, text="", font=ctk.CTkFont(size=12, weight="bold")
  )
  statut_label.pack(pady=2)

  def executer_action(mode):
    f_path = chemin_fichier_val["path"]
    k_path = chemin_cle_val["path"]

    if not f_path or not os.path.exists(f_path):
      statut_label.configure(text="⚠️ Sélectionne un fichier valide !", text_color="orange")
      return
    if not k_path or not os.path.exists(k_path):
      statut_label.configure(text="⚠️ Sélectionne ou génère une clé .key !", text_color="orange")
      return

    progress_bar.pack(expand=True)
    progress_bar.set(0.5)
    statut_label.configure(text=f"⚙️ Opération en cours ({mode})...", text_color="lightblue")

    def tache():
      try:
        with open(k_path, "rb") as f_k:
          cle = f_k.read()
        f = Fernet(cle)

        with open(f_path, "rb") as f_f:
          donnees = f_f.read()

        if mode == "chiffrer":
          donnees_traitees = f.encrypt(donnees)
          nouveau_chemin = f_path + ".locked"
        else:
          donnees_traitees = f.decrypt(donnees)
          if f_path.endswith(".locked"):
            nouveau_chemin = f_path[:-7]
          else:
            nouveau_chemin = f_path + ".unlocked"

        with open(nouveau_chemin, "wb") as f_out:
          f_out.write(donnees_traitees)

        def succes_ui():
          progress_bar.set(1.0)
          progress_bar.pack_forget()
          statut_label.configure(
              text=f"✨ Succès ! Fichier enregistré : {os.path.basename(nouveau_chemin)}",
              text_color="green",
          )

        cryptofile_window.after(0, succes_ui)

      except Exception as e:
        def erreur_ui():
          progress_bar.set(0)
          progress_bar.pack_forget()
          statut_label.configure(text="❌ Erreur : Clé incorrecte ou fichier corrompu", text_color="red")
        cryptofile_window.after(0, erreur_ui)

    threading.Thread(target=tache, daemon=True).start()

  # Boutons de commande
  cadre_boutons = ctk.CTkFrame(cryptofile_window, fg_color="transparent")
  cadre_boutons.pack(pady=15)

  btn_chiffrer = ctk.CTkButton(
      cadre_boutons,
      text="🔒 Chiffrer",
      command=lambda: executer_action("chiffrer"),
      fg_color="#C62828",
      hover_color="#8E0000",
      font=ctk.CTkFont(size=13, weight="bold"),
      width=130,
      height=38,
  )
  btn_chiffrer.pack(side="left", padx=10)

  btn_dechiffrer = ctk.CTkButton(
      cadre_boutons,
      text="🔓 Déchiffrer",
      command=lambda: executer_action("dechiffrer"),
      fg_color="#2E7D32",
      hover_color="#1B5E20",
      font=ctk.CTkFont(size=13, weight="bold"),
      width=130,
      height=38,
  )
  btn_dechiffrer.pack(side="left", padx=10)

  cryptofile_window.mainloop()