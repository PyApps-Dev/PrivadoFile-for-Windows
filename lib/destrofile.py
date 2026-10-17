#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#############################################################################
#               PROJECT   :   DestroFile                                    #
#               GROUP     :   Quantum Software                              #
#               VERSION   :   1.0.0                                         #
#               LICENSE   :   GNU GPL v3                                    #
#               AUTHOR    :   Youssef B.                                    #
#               YEAR      :   2026                                          #
#               COPYRIGHT :   © 2026 Quantum Software. All rights reserved. #
#############################################################################

# DestroFile™

import os
import random
import threading
import customtkinter as ctk
from tkinter import filedialog

def destrofile():

  destrofile_window = ctk.CTk()
  destrofile_window.title("DestroFile")
  destrofile_window.resizable(False, False)

  width = 520
  height = 620
  screen_width = destrofile_window.winfo_screenwidth()
  screen_height = destrofile_window.winfo_screenheight()
  x = (screen_width - width) // 2
  y = (screen_height - height) // 2
  destrofile_window.geometry(f"{width}x{height}+{x}+{y}")

  ctk.set_appearance_mode("System")
  ctk.set_default_color_theme("blue")

  def ecraser_donnees(chemin, taille, progress_callback=None):
    """Méthode DoD 5220.22-M à 7 passes avec mise à jour de la progression."""
    motifs = [
        b"\x00",
        b"\xFF",
        b"\x00",
        lambda t: bytes(random.getrandbits(8) for _ in range(t)),
        lambda t: bytes(random.getrandbits(8) for _ in range(t)),
        b"\x00",
        lambda t: bytes(random.getrandbits(8) for _ in range(t)),
    ]

    with open(chemin, "r+b") as f:
      for i, motif in enumerate(motifs):
        f.seek(0)
        if callable(motif):
          f.write(motif(taille))
        else:
          f.write(motif * taille)
        f.flush()
        os.fsync(f.fileno())

        if progress_callback:
          progress_callback((i + 1) / 7)

  def detruire_element(chemin, progress_callback=None):
    """Pulvérisation définitive d'un fichier ou d'un dossier."""
    if os.path.isfile(chemin):
      try:
        taille = os.path.getsize(chemin)
        if taille > 0:
          ecraser_donnees(chemin, taille, progress_callback)
        os.remove(chemin)
        return True
      except Exception:
        return False

    elif os.path.isdir(chemin):
      fichiers_a_traiter = []
      for racine, dirs, fichiers in os.walk(chemin):
        for nom in fichiers:
          fichiers_a_traiter.destrofile_windowend(os.path.join(racine, nom))

      total_fichiers = len(fichiers_a_traiter)
      if total_fichiers == 0:
        for racine, dirs, fichiers in os.walk(chemin, topdown=False):
          for nom in dirs:
            try:
              os.rmdir(os.path.join(racine, nom))
            except Exception:
              pass
        try:
          os.rmdir(chemin)
          return True
        except Exception:
          return False

      traites = [0]

      for fp in fichiers_a_traiter:
        try:
          taille = os.path.getsize(fp)

          def sub_callback(pass_ratio):
            global_progress = (
                traites[0] + pass_ratio
            ) / total_fichiers
            if progress_callback:
              progress_callback(global_progress)

          if taille > 0:
            ecraser_donnees(fp, taille, sub_callback)
          os.remove(fp)
        except Exception:
          pass
        traites[0] += 1

      for racine, dirs, fichiers in os.walk(chemin, topdown=False):
        for nom in dirs:
          try:
            os.rmdir(os.path.join(racine, nom))
          except Exception:
            pass
      try:
        os.rmdir(chemin)
        return True
      except Exception:
        return False
    return False

  titre_label = ctk.CTkLabel(
      destrofile_window,
      text="Destrofile (DoD 7 Passes)",
      font=ctk.CTkFont(size=22, weight="bold"),
  )
  titre_label.pack(pady=(20, 5))

  info_label = ctk.CTkLabel(
      destrofile_window,
      text="Choisis un fichier ou un dossier à pulvériser numériquement.",
      font=ctk.CTkFont(size=13),
      text_color="gray",
  )
  info_label.pack(pady=5)

  def choisir_fichier():
    chemin = filedialog.askopenfilename(parent=destrofile_window)
    if chemin:
      chemin_label.configure(text=chemin, text_color="#FFFFFF")
      statut_label.configure(text="", text_color="gray")

  def choisir_dossier():
    chemin = filedialog.askdirectory(parent=destrofile_window)
    if chemin:
      chemin_label.configure(text=chemin, text_color="#FFFFFF")
      statut_label.configure(text="", text_color="gray")

  # Boutons de sélection
  btn_fichier = ctk.CTkButton(
      destrofile_window,
      text="📄 Choisir un Fichier",
      command=choisir_fichier,
      font=ctk.CTkFont(size=12, weight="bold"),
      width=220,
      height=35,
  )
  btn_fichier.pack(pady=(10, 5))

  btn_dossier = ctk.CTkButton(
      destrofile_window,
      text="📁 Choisir un Dossier",
      command=choisir_dossier,
      font=ctk.CTkFont(size=12, weight="bold"),
      width=220,
      height=35,
  )
  btn_dossier.pack(pady=(0, 10))

  chemin_label = ctk.CTkLabel(
      destrofile_window,
      text="Aucun fichier ou dossier sélectionné",
      font=ctk.CTkFont(size=11),
      wraplength=450,
      text_color="#A0A0A0",
  )
  chemin_label.pack(pady=5)

  cadre_barre = ctk.CTkFrame(destrofile_window, fg_color="transparent", height=25)
  cadre_barre.pack(pady=5, fill="x")
  cadre_barre.pack_propagate(False)

  progress_bar = ctk.CTkProgressBar(cadre_barre, width=350, height=15)
  progress_bar.set(0)

  # Label de statut dynamique CTK
  statut_label = ctk.CTkLabel(
      destrofile_window, text="", font=ctk.CTkFont(size=12, weight="bold")
  )
  statut_label.pack(pady=10)

  def lancer_destruction():
    chemin = chemin_label.cget("text")
    if not chemin or chemin == "Aucun fichier ou dossier sélectionné":
      statut_label.configure(
          text="⚠️ Choisis d'abord une cible à anéantir !", text_color="orange"
      )
      return

    btn_fichier.configure(state="disabled")
    btn_dossier.configure(state="disabled")
    btn_detruire.configure(state="disabled")

    progress_bar.pack(expand=True)
    progress_bar.set(0)

    statut_label.configure(
        text="⏳ Destruction DoD en cours... 🛌", text_color="lightblue"
    )

    def travail_en_arriere_plan():
      derniere_valeur = [-1.0]

      def update_progress(valeur):

        if abs(valeur - derniere_valeur[0]) >= 0.01 or valeur >= 1.0:
          derniere_valeur[0] = valeur
          try:
            destrofile_window.after(0, lambda v=valeur: progress_bar.set(v))
          except Exception:
            pass

      succes = detruire_element(chemin, progress_callback=update_progress)

      def fin_destruction():
        try:
          progress_bar.set(1.0)
          progress_bar.pack_forget()

          if succes:
            statut_label.configure(
                text="✨ Cible pulvérisée avec succès ! Irrécupérable (100%).",
                text_color="green",
            )
            chemin_label.configure(
                text="Aucun fichier ou dossier sélectionné", text_color="#A0A0A0"
            )
          else:
            statut_label.configure(
                text="❌ Erreur lors de la destruction de l'élément.",
                text_color="red",
            )

          btn_fichier.configure(state="normal")
          btn_dossier.configure(state="normal")
          btn_detruire.configure(state="normal")
        except Exception:
          pass

      destrofile_window.after(0, fin_destruction)

    threading.Thread(target=travail_en_arriere_plan, daemon=True).start()

  btn_detruire = ctk.CTkButton(
      destrofile_window,
      text="💥 Exécuter la destruction DoD",
      fg_color="#D32F2F",
      hover_color="#B71C1C",
      command=lancer_destruction,
      font=ctk.CTkFont(size=14, weight="bold"),
      width=260,
      height=40,
  )
  btn_detruire.pack(pady=15)

  destrofile_window.mainloop()