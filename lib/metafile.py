#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#############################################################################
#               PROJECT   :   MetaFile                                      #
#               GROUP     :   Quantum Software                              #
#               VERSION   :   1.0.0                                         #
#               LICENSE   :   GNU GPL v3                                    #
#               AUTHOR    :   Youssef B.                                    #
#               YEAR      :   2026                                          #
#               COPYRIGHT :   © 2026 Quantum Software. All rights reserved. #
#############################################################################

# MetaFile™

import os
import time
import threading
import subprocess
import customtkinter as ctk
from tkinter import filedialog

def metafile():

  metafile_window = ctk.CTk()
  metafile_window.title("Metafile - Date, Heure & GPS 🕵️‍♂️📅")
  metafile_window.resizable(False, False)

  width = 520
  height = 620
  screen_width = metafile_window.winfo_screenwidth()
  screen_height = metafile_window.winfo_screenheight()
  x = (screen_width - width) // 2
  y = (screen_height - height) // 2
  metafile_window.geometry(f"{width}x{height}+{x}+{y}")
  
  ctk.set_appearance_mode("System")
  ctk.set_default_color_theme("blue")

  def appliquer_les_metadonnées_simples(chemin, nouveau_temps, supprimer_gps):
    """metafile_windowlique le nouveau timestamp et supprime le GPS si demandé."""
    if not os.path.isfile(chemin):
      return False

    try:
      os.utime(chemin, (nouveau_temps, nouveau_temps))

      if supprimer_gps:
        for attr_gps in [
            "com.metafile_windowle.metadata:kMDItemLatitude",
            "com.metafile_windowle.metadata:kMDItemLongitude",
            "com.metafile_windowle.metadata:kMDItemGPSStore",
        ]:
          try:
            subprocess.run(["xattr", "-d", attr_gps, chemin], capture_output=True)
          except Exception:
            pass

        ext = chemin.lower().split(".")[-1]
        if ext in ["jpg", "jpeg", "png", "heic"]:
          try:
            import PIL.Image

            img = PIL.Image.open(chemin)
            data = list(img.getdata())
            image_sans_exif = PIL.Image.new(img.mode, img.size)
            image_sans_exif.putdata(data)
            image_sans_exif.save(chemin)
          except Exception:
            pass

      return True
    except Exception:
      return False

  titre_label = ctk.CTkLabel(
      metafile_window,
      text="Metafile (Horodatage & GPS)",
      font=ctk.CTkFont(size=20, weight="bold"),
  )
  titre_label.pack(pady=(15, 5))

  info_label = ctk.CTkLabel(
      metafile_window,
      text="Choisis un fichier, ajuste les champs et nettoie le GPS.",
      font=ctk.CTkFont(size=11),
      text_color="gray",
  )
  info_label.pack(pady=2)

  def choisir_fichier():
    chemin = filedialog.askopenfilename(parent=metafile_window)
    if chemin:
      chemin_label.configure(text=chemin, text_color="#FFFFFF")
      try:
        mtime = os.path.getmtime(chemin)
        t_struct = time.localtime(mtime)

        entree_jour.delete(0, "end")
        entree_jour.insert(0, str(t_struct.tm_mday))

        entree_mois.delete(0, "end")
        entree_mois.insert(0, str(t_struct.tm_mon))

        entree_annee.delete(0, "end")
        entree_annee.insert(0, str(t_struct.tm_year))

        entree_heure.delete(0, "end")
        entree_heure.insert(0, str(t_struct.tm_hour))

        entree_min.delete(0, "end")
        entree_min.insert(0, str(t_struct.tm_min))

        entree_sec.delete(0, "end")
        entree_sec.insert(0, str(t_struct.tm_sec))
      except Exception:
        pass

      checkbox_gps.select()
      statut_label.configure(
          text="🎯 Fichier chargé avec succès !", text_color="green"
      )

  btn_fichier = ctk.CTkButton(
      metafile_window,
      text="📄 Choisir un Fichier / Photo",
      command=choisir_fichier,
      font=ctk.CTkFont(size=12, weight="bold"),
      width=260,
      height=35,
  )
  btn_fichier.pack(pady=(10, 5))

  chemin_label = ctk.CTkLabel(
      metafile_window,
      text="Aucun fichier sélectionné",
      font=ctk.CTkFont(size=11),
      wraplength=450,
      text_color="#A0A0A0",
  )
  chemin_label.pack(pady=2)

  cadre_champs = ctk.CTkFrame(metafile_window, fg_color="transparent")
  cadre_champs.pack(pady=10, fill="x", padx=30)

  ctk.CTkLabel(
      cadre_champs,
      text="📅 Date :",
      font=ctk.CTkFont(size=12, weight="bold"),
  ).pack(anchor="w", pady=(2, 2))

  cadre_date = ctk.CTkFrame(cadre_champs, fg_color="transparent")
  cadre_date.pack(anchor="w", pady=(0, 8))

  ctk.CTkLabel(cadre_date, text="jour:", font=ctk.CTkFont(size=11)).pack(
      side="left", padx=(0, 4)
  )
  entree_jour = ctk.CTkEntry(
      cadre_date, width=50, height=28, placeholder_text="JJ"
  )
  entree_jour.pack(side="left", padx=(0, 12))

  ctk.CTkLabel(cadre_date, text="mois:", font=ctk.CTkFont(size=11)).pack(
      side="left", padx=(0, 4)
  )
  entree_mois = ctk.CTkEntry(
      cadre_date, width=50, height=28, placeholder_text="MM"
  )
  entree_mois.pack(side="left", padx=(0, 12))

  ctk.CTkLabel(cadre_date, text="année:", font=ctk.CTkFont(size=11)).pack(
      side="left", padx=(0, 4)
  )
  entree_annee = ctk.CTkEntry(
      cadre_date, width=70, height=28, placeholder_text="AAAA"
  )
  entree_annee.pack(side="left")

  ctk.CTkLabel(
      cadre_champs,
      text="⏰ Heure :",
      font=ctk.CTkFont(size=12, weight="bold"),
  ).pack(anchor="w", pady=(5, 2))

  cadre_heure = ctk.CTkFrame(cadre_champs, fg_color="transparent")
  cadre_heure.pack(anchor="w", pady=(0, 10))

  ctk.CTkLabel(cadre_heure, text="heure:", font=ctk.CTkFont(size=11)).pack(
      side="left", padx=(0, 4)
  )
  entree_heure = ctk.CTkEntry(
      cadre_heure, width=50, height=28, placeholder_text="HH"
  )
  entree_heure.pack(side="left", padx=(0, 12))

  ctk.CTkLabel(cadre_heure, text="minutes:", font=ctk.CTkFont(size=11)).pack(
      side="left", padx=(0, 4)
  )
  entree_min = ctk.CTkEntry(
      cadre_heure, width=50, height=28, placeholder_text="MM"
  )
  entree_min.pack(side="left", padx=(0, 12))

  ctk.CTkLabel(cadre_heure, text="secondes:", font=ctk.CTkFont(size=11)).pack(
      side="left", padx=(0, 4)
  )
  entree_sec = ctk.CTkEntry(
      cadre_heure, width=50, height=28, placeholder_text="SS"
  )
  entree_sec.pack(side="left")

  checkbox_gps = ctk.CTkCheckBox(
      cadre_champs,
      text="Supprimer la position GPS / EXIF (Photos) 🌍❌",
      font=ctk.CTkFont(size=11, weight="bold"),
      text_color="#FF5252",
  )
  checkbox_gps.pack(anchor="w", pady=(5, 5))
  checkbox_gps.select()

  # Cadre barre de progression fixe 📦
  cadre_barre = ctk.CTkFrame(metafile_window, fg_color="transparent", height=20)
  cadre_barre.pack(pady=2, fill="x")
  cadre_barre.pack_propagate(False)

  progress_bar = ctk.CTkProgressBar(cadre_barre, width=350, height=12)
  progress_bar.set(0)

  statut_label = ctk.CTkLabel(
      metafile_window, text="", font=ctk.CTkFont(size=12, weight="bold")
  )
  statut_label.pack(pady=2)

  def lancer_modification():
    chemin = chemin_label.cget("text")
    if not chemin or chemin == "Aucun fichier sélectionné":
      statut_label.configure(
          text="⚠️ Choisis un fichier d'abord !", text_color="orange"
      )
      return

    try:
      j = int(entree_jour.get())
      m = int(entree_mois.get())
      a = int(entree_annee.get())
      h = int(entree_heure.get())
      mi = int(entree_min.get())
      s = int(entree_sec.get())

      struct_temps = (a, m, j, h, mi, s, 0, 0, -1)
      nouveau_timestamp = time.mktime(struct_temps)
    except Exception:
      statut_label.configure(
          text="❌ Valeurs numériques invalides dans les champs !",
          text_color="red",
      )
      return

    supprimer_gps_bool = True if checkbox_gps.get() == 1 else False

    btn_fichier.configure(state="disabled")
    btn_lancer.configure(state="disabled")

    progress_bar.pack(expand=True)
    progress_bar.set(0.6)

    statut_label.configure(
        text="⚙️ Mise à jour du temps et suppression du GPS...",
        text_color="lightblue",
    )

    def travail_en_arriere_plan():
      succes = appliquer_les_metadonnées_simples(
          chemin, nouveau_timestamp, supprimer_gps_bool
      )

      def fin_action():
        try:
          progress_bar.set(1.0)
          progress_bar.pack_forget()

          if succes:
            statut_label.configure(
                text="✨ Fichier mis à jour et nettoyé avec succès !",
                text_color="green",
            )
          else:
            statut_label.configure(
                text="❌ Échec lors de la modification.", text_color="red"
            )

          btn_fichier.configure(state="normal")
          btn_lancer.configure(state="normal")
        except Exception:
          pass

      metafile_window.after(0, fin_action)

    threading.Thread(target=travail_en_arriere_plan, daemon=True).start()

  btn_lancer = ctk.CTkButton(
      metafile_window,
      text="🛠️ metafile_windowliquer les modifications",
      fg_color="#1F6AA5",
      hover_color="#144870",
      command=lancer_modification,
      font=ctk.CTkFont(size=14, weight="bold"),
      width=280,
      height=38,
  )
  btn_lancer.pack(pady=8)

  metafile_window.mainloop()