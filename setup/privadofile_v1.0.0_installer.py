#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##############################################################
#               PROJECT   :   PrivadoFile Installer          #
#               GROUP     :   Quantum Software               #
#               VERSION   :   1.0.0                          #
#               LICENSE   :   GNU GPL v3                     #
#               AUTHOR    :   Youssef B.                     #
#               YEAR      :   2026                           #
##############################################################

import io
import os
import sys
import time
import zipfile
import requests
import threading
import customtkinter as ctk

# Configuration de base de la fenêtre
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("PrivadoFile v1.0.0 Installer")
root.geometry("550x400")
root.resizable(False, False)

# --- CONFIGURATION ---
CURRENT_STEP = 1
GITHUB_ORGANIZATION = "TomSchimansky"
REPO_NAME = "CustomTkinter"
WEB_TARGET_URL = "https://github.com/QuantumSoftwareGroup" 
CHOSEN_PATH = ctk.StringVar(value=os.path.join(os.environ["USERPROFILE"], "Desktop", "CustomTkinter_Project"))
CREATE_SHORTCUT = ctk.BooleanVar(value=True)

screen_widgets = []


def clear_screen():
    global screen_widgets
    for widget in screen_widgets:
        widget.destroy()
    screen_widgets = []


def create_web_shortcut_on_desktop(site_url):
    """Crée un raccourci internet (.url) sur le Bureau."""
    try:
        desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        shortcut_file = os.path.join(desktop_path, "QuantumSoftwareGroup.url")
        
        with open(shortcut_file, "w", encoding="utf-8") as f:
            f.write("[InternetShortcut]\n")
            f.write(f"URL={site_url}\n")
        return True
    except Exception as e:
        print(f"Erreur raccourci Web : {e}")
        return False


def start_installation_thread(progress_label, stats_label, progress_bar):
    """Lance le téléchargement dans un thread séparé."""
    progress_bar.configure(mode="determinate")
    progress_bar.set(0)
    
    threading.Thread(
        target=download_and_extract_logic, 
        args=(progress_label, stats_label, progress_bar), 
        daemon=True
    ).start()


def download_and_extract_logic(progress_label, stats_label, progress_bar):
    """Télécharge le fichier et calcule la vitesse, le temps écoulé et le temps restant."""
    target_dir = CHOSEN_PATH.get()
    
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
    except Exception:
        root.after(0, lambda: progress_label.configure(text="Error: Could not create destination folder. ❌", text_color="red"))
        root.after(0, lambda: btn_back.configure(state="normal"))
        return

    zip_url = f"https://github.com/{GITHUB_ORGANIZATION}/{REPO_NAME}/archive/refs/heads/master.zip"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        root.after(0, lambda: progress_label.configure(text="Connecting to GitHub... 🌐", text_color="white"))
        
        response = requests.get(zip_url, headers=headers, stream=True)
        
        if response.status_code != 200:
            zip_url = f"https://github.com/{GITHUB_ORGANIZATION}/{REPO_NAME}/archive/refs/heads/main.zip"
            response = requests.get(zip_url, headers=headers, stream=True)
            
        if response.status_code != 200:
            root.after(0, lambda: progress_label.configure(text=f"GitHub Error (Code {response.status_code}) ❌", text_color="red"))
            root.after(0, lambda: btn_back.configure(state="normal"))
            return

        total_size = response.headers.get('content-length')
        file_data = io.BytesIO()
        
        if total_size is None:
            root.after(0, lambda: progress_label.configure(text="Downloading... 📥 (Dynamic Size)"))
            file_data.write(response.content)
        else:
            total_size = int(total_size)
            downloaded = 0
            
            spinner = ["▖", "▘", "▝", "▗"]
            spinner_index = 0
            
            # --- TOP CHRONO ---
            start_time = time.time()
            
            for chunk in response.iter_content(chunk_size=8192): # Bloc de 8 Ko pour plus de stabilité
                if chunk:
                    file_data.write(chunk)
                    downloaded += len(chunk)
                    
                    # 1. Calcul du pourcentage
                    percent = downloaded / total_size
                    percent_text = int(percent * 100)
                    
                    # 2. Temps écoulé (Elapsed Time)
                    elapsed_time = time.time() - start_time
                    
                    # 3. Calcul de la vitesse (Speed) en MB/s
                    # Vitesse = Octets téléchargés / temps écoulé / (1024 * 1024)
                    if elapsed_time > 0:
                        speed_mbs = (downloaded / elapsed_time) / (1024 * 1024)
                    else:
                        speed_mbs = 0
                        
                    # 4. Calcul du temps restant (Time Remaining)
                    if speed_mbs > 0:
                        remaining_bytes = total_size - downloaded
                        remaining_time = (remaining_bytes / (1024 * 1024)) / speed_mbs
                    else:
                        remaining_time = 0
                        
                    # Petit spinner d'animation
                    char = spinner[spinner_index % len(spinner)]
                    spinner_index += 1
                    
                    # --- Formatage des textes en US ---
                    status_text = f"Downloading:  {char}  {percent_text}%"
                    
                    # Affichage : Speed (MB/s) | Elapsed | Remaining
                    stats_text = (
                        f"Speed: {speed_mbs:.2f} MB/s   |   "
                        f"Elapsed: {int(elapsed_time)}s   |   "
                        f"Remaining: {int(remaining_time)}s"
                    )
                    
                    # Envoi des valeurs sur l'IHM
                    root.after(0, lambda p=percent, t=status_text, s=stats_text: [
                        progress_bar.set(p), 
                        progress_label.configure(text=t),
                        stats_label.configure(text=s)
                    ])

        # Extraction des fichiers
        root.after(0, lambda: progress_label.configure(text="Extracting files to Desktop... 📂"))
        root.after(0, lambda: stats_label.configure(text="Please wait... finalizing setup."))
        
        with zipfile.ZipFile(file_data) as zip_file:
            zip_file.extractall(target_dir)
            
        if CREATE_SHORTCUT.get():
            root.after(0, lambda: progress_label.configure(text="Creating Web Shortcut... 🌐"))
            create_web_shortcut_on_desktop(WEB_TARGET_URL)

        root.after(0, go_to_finish_screen)

    except Exception as e:
        root.after(0, lambda: progress_label.configure(text=f"Critical Error: {str(e)} ❌", text_color="red"))
        root.after(0, lambda: stats_label.configure(text=""))
        root.after(0, lambda: btn_back.configure(state="normal"))


def go_to_finish_screen():
    global CURRENT_STEP
    CURRENT_STEP = 4
    show_screen()


def select_folder():
    folder = ctk.filedialog.askdirectory(initialdir=CHOSEN_PATH.get())
    if folder:
        CHOSEN_PATH.set(folder)


def show_screen():
    global CURRENT_STEP
    clear_screen()

    # --- ÉCRAN 1 : BIENVENUE ---
    if CURRENT_STEP == 1:
        title = ctk.CTkLabel(center_frame, text="Welcome to the Pro Installer!", font=("Arial", 20, "bold"))
        title.pack(pady=20)
        screen_widgets.append(title)

        desc = ctk.CTkLabel(center_frame, text="This tool downloads the project directly from GitHub\nand creates a useful Web Shortcut on your Desktop. ⚡", font=("Arial", 14), justify="center")
        desc.pack(pady=10)
        screen_widgets.append(desc)

        btn_back.configure(state="disabled")
        btn_next.configure(text="Next >", state="normal")

    # --- ÉCRAN 2 : OPTIONS & CHEMIN ---
    elif CURRENT_STEP == 2:
        title = ctk.CTkLabel(center_frame, text="Installation Settings ⚙️", font=("Arial", 18, "bold"))
        title.pack(pady=10)
        screen_widgets.append(title)

        path_label = ctk.CTkLabel(center_frame, text="Destination Folder:", font=("Arial", 12))
        path_label.pack(pady=5)
        screen_widgets.append(path_label)

        path_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        path_frame.pack(pady=5, fill="x", padx=20)
        screen_widgets.append(path_frame)

        entry_path = ctk.CTkEntry(path_frame, textvariable=CHOSEN_PATH, width=320)
        entry_path.pack(side="left", padx=5)
        
        btn_browse = ctk.CTkButton(path_frame, text="Browse...", width=80, command=select_folder)
        btn_browse.pack(side="left", padx=5)

        chk_shortcut = ctk.CTkCheckBox(center_frame, text="Create GitHub Shortcut on Desktop 🌐", variable=CREATE_SHORTCUT)
        chk_shortcut.pack(pady=20)
        screen_widgets.append(chk_shortcut)

        btn_back.configure(state="normal")
        btn_next.configure(text="Install", state="normal")

    # --- ÉCRAN 3 : CHARGEMENT AVEC STATS COMPLETES ---
    elif CURRENT_STEP == 3:
        title = ctk.CTkLabel(center_frame, text="Installing Files... ⏳", font=("Arial", 18, "bold"))
        title.pack(pady=15)
        screen_widgets.append(title)

        progress_label = ctk.CTkLabel(center_frame, text="Preparing...", font=("Arial", 14, "bold"))
        progress_label.pack(pady=5)
        screen_widgets.append(progress_label)

        progress_bar = ctk.CTkProgressBar(center_frame, width=400)
        progress_bar.set(0)
        progress_bar.pack(pady=10)
        screen_widgets.append(progress_bar)

        # Nouveau label pour afficher la vitesse (MB/s) et le temps restant ! 📊
        stats_label = ctk.CTkLabel(center_frame, text="Speed: 0.00 MB/s  |  Elapsed: 0s  |  Remaining: 0s", font=("Courier New", 12, "bold"), text_color="#3a7ebf")
        stats_label.pack(pady=10)
        screen_widgets.append(stats_label)

        btn_back.configure(state="disabled")
        btn_next.configure(state="disabled")
        
        start_installation_thread(progress_label, stats_label, progress_bar)

    # --- ÉCRAN 4 : FINISH ---
    elif CURRENT_STEP == 4:
        title = ctk.CTkLabel(center_frame, text="Installation Completed! 🎉", font=("Arial", 22, "bold"), text_color="green")
        title.pack(pady=20)
        screen_widgets.append(title)

        success_text = f"The project has been successfully installed.\nA shortcut to our GitHub has been placed on your Desktop! 🌐💻"
        desc = ctk.CTkLabel(center_frame, text=success_text, font=("Arial", 13), justify="center")
        desc.pack(pady=10)
        screen_widgets.append(desc)

        btn_back.configure(state="disabled")
        btn_next.configure(text="Finish", state="normal")


def navigate_next():
    global CURRENT_STEP
    if CURRENT_STEP < 4:
        CURRENT_STEP += 1
        show_screen()
    else:
        root.quit()


def navigate_back():
    global CURRENT_STEP
    if CURRENT_STEP > 1:
        CURRENT_STEP -= 1
        show_screen()


# --- LAYOUT ---
center_frame = ctk.CTkFrame(root, width=510, height=300, fg_color="transparent")
center_frame.pack(pady=10, fill="both", expand=True)

separator = ctk.CTkFrame(root, height=2, fg_color="gray")
separator.pack(fill="x", padx=10, pady=5)

nav_frame = ctk.CTkFrame(root, fg_color="transparent")
nav_frame.pack(fill="x", padx=20, pady=10)

btn_back = ctk.CTkButton(nav_frame, text="< Back", width=100, command=navigate_back)
btn_back.pack(side="left")

btn_next = ctk.CTkButton(nav_frame, text="Next >", width=100, command=navigate_next)
btn_next.pack(side="right")

show_screen()
root.mainloop()