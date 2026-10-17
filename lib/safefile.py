#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#############################################################################
#               PROJECT   :   SafeFile                                      #
#               GROUP     :   Quantum Software                              #
#               VERSION   :   1.0.0                                         #
#               LICENSE   :   GNU GPL v3                                    #
#               AUTHOR    :   Youssef B.                                    #
#               YEAR      :   2026                                          #
#               COPYRIGHT :   © 2026 Quantum Software. All rights reserved. #
#############################################################################

# SafeFile™

import os
import hashlib
import threading
import customtkinter as ctk
from tkinter import filedialog

def safefile():

  safefile_window = ctk.CTk()
  safefile_window.title("SafeFile")
  safefile_window.resizable(False, False)

  width = 520
  height = 620
  screen_width = safefile_window.winfo_screenwidth()
  screen_height = safefile_window.winfo_screenheight()
  x = (screen_width - width) // 2
  y = (screen_height - height) // 2
  safefile_window.geometry(f"{width}x{height}+{x}+{y}")

  ctk.set_appearance_mode("System")
  ctk.set_default_color_theme("blue")

  # Titre stylé
  titre_label = ctk.CTkLabel(
      safefile_window,
      text="SafeFile (Coffre-Fort Local)",
      font=ctk.CTkFont(size=20, weight="bold"),
  )
  titre_label.pack(pady=(15, 5))

  info_label = ctk.CTkLabel(
      safefile_window,
      text="Protège tes fichiers secrets dans un coffre crypté par mot de passe.",
      font=ctk.CTkFont(size=11),
      text_color="gray",
  )
  info_label.pack(pady=2)

  contexte = {"fichier": "", "coffre": ""}

  def choisir_fichier():
    chemin = filedialog.askopenfilename(
        parent=safefile_window,
        title="Sélectionner le fichier à enfermer"
    )
    if chemin:
      contexte["fichier"] = chemin
      label_fic.configure(text=os.path.basename(chemin), text_color="#FFFFFF")
      statut_label.configure(text="📄 Fichier cible sélectionné !", text_color="green")

  btn_fic = ctk.CTkButton(
      safefile_window,
      text="📁 1. Choisir un fichier à cacher",
      command=choisir_fichier,
      font=ctk.CTkFont(size=12, weight="bold"),
      width=300,
      height=35,
  )
  btn_fic.pack(pady=(12, 2))

  label_fic = ctk.CTkLabel(
      safefile_window,
      text="Aucun fichier choisi",
      font=ctk.CTkFont(size=11),
      wraplength=450,
      text_color="#A0A0A0",
  )
  label_fic.pack(pady=2)

  # --- SECTION 2 : MOT DE PASSE MAÎTRE ---
  cadre_mdp = ctk.CTkFrame(safefile_window, fg_color="transparent")
  cadre_mdp.pack(pady=10, fill="x", padx=60)

  ctk.CTkLabel(
      cadre_mdp,
      text="🔑 Mot de passe maître du coffre :",
      font=ctk.CTkFont(size=11, weight="bold"),
  ).pack(anchor="w", pady=(2, 2))

  entree_mdp = ctk.CTkEntry(
      cadre_mdp,
      width=400,
      height=32,
      show="*",
      placeholder_text="Entre ton mot de passe secret...",
  )
  entree_mdp.pack(pady=(0, 5))

  # Barre de progression
  cadre_barre = ctk.CTkFrame(safefile_window, fg_color="transparent", height=20)
  cadre_barre.pack(pady=5, fill="x")
  cadre_barre.pack_propagate(False)

  progress_bar = ctk.CTkProgressBar(cadre_barre, width=350, height=12)
  progress_bar.set(0)

  statut_label = ctk.CTkLabel(
      safefile_window, text="", font=ctk.CTkFont(size=12, weight="bold")
  )
  statut_label.pack(pady=2)

  # --- LOGIQUE DE CHIFFREMENT / DÉCHIFFREMENT LÉGÈRE (SANS DÉPENDANCE) ---
  def deriver_cle(password: str) -> bytes:
    """Génère une clé robuste de 32 octets à partir du mot de passe."""
    return hashlib.sha256(password.encode("utf-8")).digest()

  def chiffrer_donnees(donnees: bytes, cle: bytes) -> bytes:
    """Chiffrement symétrique par XOR dynamique avec la clé hashée."""
    cle_etendue = (
        cle * (len(donnees) // len(cle) + 1)
    )[:len(donnees)]
    return bytes(a ^ b for a, b in zip(donnees, cle_etendue))

  # --- ACTIONS DU COFFRE ---
  def creer_coffre():
    fic = contexte["fichier"]
    mdp = entree_mdp.get()

    if not fic or not os.path.exists(fic):
      statut_label.configure(
          text="⚠️ Choisis un fichier valide à enfermer !", text_color="orange"
      )
      return
    if not mdp:
      statut_label.configure(
          text="⚠️ Entre un mot de passe maître !", text_color="orange"
      )
      return

    # Demander où enregistrer le fichier .vault
    coffre_path = filedialog.asksaveasfilename(
        parent=safefile_window,
        defaultextension=".vault",
        filetypes=[("Coffre SafeFile", "*.vault")],
        title="Enregistrer le coffre-fort",
    )
    if not coffre_path:
      return

    progress_bar.pack(expand=True)
    progress_bar.set(0.5)
    statut_label.configure(
        text="🔒 Création du coffre-fort local...", text_color="lightblue"
    )

    def tache():
      try:
        # Lire le fichier original et garder son nom d'origine dans l'en-tête
        nom_original = os.path.basename(fic).encode("utf-8")
        with open(fic, "rb") as f:
          contenu = f.read()

        # Format : [Taille du nom (2 octets)] + [Nom original] + [Contenu]
        paquet = (
            len(nom_original).to_bytes(2, "big") + nom_original + contenu
        )

        cle = deriver_cle(mdp)
        donnees_chiffrees = chiffrer_donnees(paquet, cle)

        with open(coffre_path, "wb") as f_out:
          f_out.write(donnees_chiffrees)

        def succes():
          progress_bar.set(1.0)
          progress_bar.pack_forget()
          statut_label.configure(
              text="✨ Coffre créé et verrouillé avec succès !",
              text_color="green",
          )

        safefile_window.after(0, succes)
      except Exception:
        def erreur():
          progress_bar.set(0)
          progress_bar.pack_forget()
          statut_label.configure(
              text="❌ Erreur lors de la création du coffre.", text_color="red"
          )
        safefile_window.after(0, erreur)

    threading.Thread(target=tache, daemon=True).start()

  def ouvrir_coffre():
    mdp = entree_mdp.get()
    if not mdp:
      statut_label.configure(
          text="⚠️ Entre le mot de passe pour ouvrir le coffre !",
          text_color="orange",
      )
      return

    coffre_path = filedialog.askopenfilename(
        parent=safefile_window,
        filetypes=[("Coffre SafeFile", "*.vault")],
        title="Sélectionner le coffre .vault à ouvrir",
    )
    if not coffre_path:
      return

    progress_bar.pack(expand=True)
    progress_bar.set(0.5)
    statut_label.configure(
        text="🔓 Ouverture et déchiffrement du coffre...", text_color="lightblue"
    )

    def tache_ouv():
      try:
        with open(coffre_path, "rb") as f_in:
          donnees_chiffrees = f_in.read()

        cle = deriver_cle(mdp)
        paquet = chiffrer_donnees(donnees_chiffrees, cle)

        # Extraire le nom d'origine et le contenu
        taille_nom = int.from_bytes(paquet[:2], "big")
        nom_original = paquet[2 : 2 + taille_nom].decode("utf-8")
        contenu = paquet[2 + taille_nom :]

        # Sauvegarder le fichier restauré là où l'utilisateur le souhaite
        dossier_sortie = filedialog.askdirectory(
            parent=safefile_window,
            title="Où extraire le fichier déchiffré ?"
        )
        if not dossier_sortie:
          progress_bar.set(0)
          progress_bar.pack_forget()
          statut_label.configure(text="❌ Extraction annulée.", text_color="orange")
          return

        chemin_final = os.path.join(dossier_sortie, nom_original)
        with open(chemin_final, "wb") as f_out:
          f_out.write(contenu)

        def succes_ouv():
          progress_bar.set(1.0)
          progress_bar.pack_forget()
          statut_label.configure(
              text=f"✨ Extrait : {nom_original} !", text_color="green"
          )

        safefile_window.after(0, succes_ouv)
      except Exception:
        def erreur_ouv():
          progress_bar.set(0)
          progress_bar.pack_forget()
          statut_label.configure(
              text="❌ Mot de passe incorrect ou coffre corrompu !",
              text_color="red",
          )
        safefile_window.after(0, erreur_ouv)

    threading.Thread(target=tache_ouv, daemon=True).start()

  # Boutons d'action du coffre
  cadre_boutons = ctk.CTkFrame(safefile_window, fg_color="transparent")
  cadre_boutons.pack(pady=15)

  btn_creer = ctk.CTkButton(
      cadre_boutons,
      text="🔒 Verrouiller en .vault",
      command=creer_coffre,
      fg_color="#C62828",
      hover_color="#8E0000",
      font=ctk.CTkFont(size=12, weight="bold"),
      width=150,
      height=38,
  )
  btn_creer.pack(side="left", padx=10)

  btn_ouvrir = ctk.CTkButton(
      cadre_boutons,
      text="🔓 Ouvrir le .vault",
      command=ouvrir_coffre,
      fg_color="#2E7D32",
      hover_color="#1B5E20",
      font=ctk.CTkFont(size=12, weight="bold"),
      width=150,
      height=38,
  )
  btn_ouvrir.pack(side="left", padx=10)

  safefile_window.mainloop()