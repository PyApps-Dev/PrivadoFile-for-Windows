#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#############################################################################
#               PROJECT   :   PrivadoFile                                   #
#               GROUP     :   Quantum Software                              #
#               VERSION   :   1.0.0                                         #
#               LICENSE   :   GNU GPL v3                                    #
#               AUTHOR    :   Youssef B.                                    #
#               YEAR      :   2026                                          #
#               COPYRIGHT :   © 2026 Quantum Software. All rights reserved. #
#############################################################################

# Quantum Software™
# PrivadoFile™
# CryptoFile™
# DestroFile™
# MetaFile™
# SafeFile™

import os
from tkinter import messagebox
import customtkinter as ctk
from lib.colors import *
from lib.cryptofile import *
from lib.destrofile import *
from lib.metafile import *
from lib.safefile import *
import webview
import threading

#logo_path = os.path.join("asset", "privadofile_icon.ico")

main_window = ctk.CTk()
main_window.title("PrivadoFile v1.0.0")
main_window.resizable(False, False)
main_window.configure(fg_color = color_main_window)
main_window.attributes("-fullscreen", False)
#main_window.iconbitmap(logo_path)

width = 1200
height = 750
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
x = (screen_width - width) // 2
y = (screen_height - height) // 2
main_window.geometry(f"{width}x{height}+{x}+{y}")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def quit():
    main_window.destroy()

def minimize():
    main_window.iconify()

def center_main_window():
  width = 1200
  height = 750
  screen_width = main_window.winfo_screenwidth()
  screen_height = main_window.winfo_screenheight()
  x = (screen_width - width) // 2
  y = (screen_height - height) // 2
  main_window.geometry(f"{width}x{height}+{x}+{y}")

def full_screen():
  full_screen_on = main_window.attributes("-fullscreen")

  if full_screen_on:
    main_window.attributes("-fullscreen", False)
    main_window.after(50, center_main_window)
    minimize_menu_button.configure(state = "normal")
  else:
    main_window.attributes("-fullscreen", True)
    minimize_menu_button.configure(state = "disabled")

def about():

    about_window_instance = None
    
    if about_window_instance is not None:
        try:
            if about_window_instance.winfo_exists():
                about_window_instance.focus_force()
                return
        except:
            pass

    about_window = ctk.CTkToplevel(main_window)
    about_window.title("About PrivadoFile")
    about_window.resizable(False, False)
    about_window.configure(fg_color = color_dark_1)
    about_window.transient(main_window)
    about_window.grab_set()             # Modal (bloque les clics ailleurs)
    about_window.focus_force()


    width = 300
    height = 325

    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    about_window.geometry(f"{width}x{height}+{x}+{y}")

    def learn_more():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path_about = os.path.join("file:///", base_dir, "doc", "about_privadofile.html")

        if os.path.exists(path_about):
            URL = path_about
            webview.create_window("PrivadoFile | About", URL)
            webview.start()
        else:
            messagebox.showerror("Error", "about_privadofile.html doesn't exists")
        about_window.destroy()

 
    learn_more_privadofile = ctk.CTkLabel(about_window, text = "PrivadoFile", font = ("Arial", 25, "bold"), text_color = color_white)
    learn_more_group = ctk.CTkLabel(about_window, text = "Group: Quantum Software", font = ("Arial", 15), text_color = description_text)
    learn_more_version = ctk.CTkLabel(about_window, text = "Version: 1.0.0", font = ("Arial", 15), text_color = description_text)
    learn_more_license = ctk.CTkLabel(about_window, text = "License: GNU GPL v3", font = ("Arial", 15), text_color = description_text)
    learn_more_devloper = ctk.CTkLabel(about_window, text = "Developer: Youssef B.", font = ("Arial", 15), text_color = description_text)
    learn_more_date = ctk.CTkLabel(about_window, text = "Date: 2026", font = ("Arial", 15), text_color = description_text)

    learn_more_privadofile.pack(pady = (20, 5))
    learn_more_group.pack(pady = 2)
    learn_more_version.pack(pady = 2)
    learn_more_license.pack(pady = 2)
    learn_more_devloper.pack(pady = 8)
    learn_more_date.pack(pady = 5)

    learn_more_button = ctk.CTkButton(about_window, text = "Learn more", width = 120, command = learn_more, fg_color = color_dark_2, hover_color = color_dark_3)
    learn_more_button.pack(pady = 15)

def help():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_learn_more = os.path.join("file:///", base_dir, "doc", "help.html")

    def run_web ():
        if os.path.exists(path_learn_more):
            URL = path_learn_more
            webview.create_window("PrivadoFile | Help", URL)
            webview.start()
        else:
            messagebox.showerror("Error", "help.html doesn't exists")

    run_web()

main_frame = ctk.CTkFrame(main_window, fg_color = color_main_window)
main_frame.pack(side = "bottom", fill = "both", expand = True, pady = 15, padx = 15)
main_frame.pack_propagate(False)

window_frame = ctk.CTkFrame(main_frame, fg_color = color_dark_1)
window_frame.pack(fill="both", expand=True)

menu_bar_frame = ctk.CTkFrame(main_window, width=1200, height=30, fg_color=color_dark_1)
quit_menu_button = ctk.CTkButton(menu_bar_frame, text = "Quit", width = 100, height = 15, fg_color = color_dark_2, hover_color = color_dark_3, command = quit)
minimize_menu_button = ctk.CTkButton(menu_bar_frame, text = "Minimize", width = 100, height = 15, fg_color = color_dark_2, hover_color = color_dark_3, command = minimize)
full_screen_menu_button = ctk.CTkButton(menu_bar_frame, text = "Full screen", width = 100, height = 15, fg_color = color_dark_2, hover_color = color_dark_3, command = full_screen)
about_menu_button = ctk.CTkButton(menu_bar_frame, text = "About", width = 100, height = 15, fg_color = color_dark_2, hover_color = color_dark_3, command = about)
help_menu_button = ctk.CTkButton(menu_bar_frame, text = "Help", width = 100, height = 15, fg_color = color_dark_2, hover_color = color_dark_3, command = help)

menu_bar_frame.pack(side = "top", fill = "x", pady = (15, 0), padx = 15)

quit_menu_button.pack(side = "left", pady = 5, padx = 5)
minimize_menu_button.pack(side = "left", pady = 5, padx = 5)
full_screen_menu_button.pack(side = "left", pady = 5, padx = 5)
about_menu_button.pack(side = "left", pady = 5, padx = 5)
help_menu_button.pack(side = "left", pady = 5, padx = 5)

menu_bar_frame.pack_propagate(False)
quit_menu_button.pack_propagate(False)
minimize_menu_button.pack_propagate(False)
full_screen_menu_button.pack_propagate(False)
about_menu_button.pack_propagate(False)
help_menu_button.pack_propagate(False)


welcome_label = ctk.CTkLabel(window_frame, text = "PrivadoFile", font = ("Arial", 45, "bold"), text_color = color_white)
welcome_label.pack(pady=(20, 5))

welcome_description_label = ctk.CTkLabel(window_frame, text = "Select a utility to start", font = ("Arial", 18), text_color = description_text)
welcome_description_label.pack(pady=(0, 20))

utility_main_frame = ctk.CTkFrame(window_frame, fg_color = "transparent")
utility_main_frame.pack(fill = "x", padx = 20, pady = 10)

copyright_label = ctk.CTkLabel(window_frame, text = "© 2026 PrivadoFile™ Quantum Softwares™. All rights reserved.", font = ("Arial", 10, "italic"), text_color = description_text,)
copyright_label.pack(side = "bottom")


cryptofile_frame = ctk.CTkFrame(utility_main_frame, width = 265, height = 350, fg_color = color_dark_2)
cryptofile_frame.pack(side = "left", expand = True, padx = 10)
cryptofile_frame.pack_propagate(False)

cryptofile_label = ctk.CTkLabel(cryptofile_frame, text = "CryptoFile", font = ("Arial", 22, "bold"), text_color = color_white)
cryptofile_label.pack(pady=(25, 15))

cryptofile_description_label = ctk.CTkLabel(cryptofile_frame, text = "Encrypt and decrypt your sensitive data using encryption keys.", font = ("Arial", 14), text_color = description_text, wraplength = 220, justify = "center")
cryptofile_description_label.pack(pady=(0, 20), padx=15, expand=True)

cryptofile_button = ctk.CTkButton(cryptofile_frame, text = "Start", width = 180, height = 40, fg_color = color_cryptofile, hover_color = color_hover_cryptofile, font = ("Arial", 15, "bold"), command = cryptofile)
cryptofile_button.pack(pady=(0, 25))


destrofile_frame = ctk.CTkFrame(utility_main_frame, width = 265, height = 350, fg_color = color_dark_2)
destrofile_frame.pack(side = "left", expand = True, padx = 10)
destrofile_frame.pack_propagate(False)

destrofile_label = ctk.CTkLabel(destrofile_frame, text = "DestroFile", font = ("Arial", 22, "bold"), text_color = color_white)
destrofile_label.pack(pady = (25, 15))

destrofile_description_label = ctk.CTkLabel(destrofile_frame, text = "Destroy your files with 7-pass DoD 5220.22-M method.", font = ("Arial", 14), text_color = description_text, wraplength = 220, justify = "center")
destrofile_description_label.pack(pady=(0, 20), padx=15, expand=True)

destrofile_button = ctk.CTkButton(destrofile_frame, text = "Start", width = 180, height = 40, fg_color = color_destrofile, hover_color = color_hover_destrofile, font = ("Arial", 15, "bold"), command = destrofile)
destrofile_button.pack(pady=(0, 25))


metafile_frame = ctk.CTkFrame(utility_main_frame, width = 265, height = 350, fg_color = color_dark_2)
metafile_frame.pack(side = "left", expand = True, padx = 10)
metafile_frame.pack_propagate(False)

metafile_label = ctk.CTkLabel(metafile_frame, text = "Metafile", font = ("Arial", 22, "bold"), text_color = color_white)
metafile_label.pack(pady=(25, 15))

metafile_description_label = ctk.CTkLabel(metafile_frame, text = "Modify metadata to wipe identifying traces.", font = ("Arial", 14), text_color = description_text, wraplength = 220, justify = "center")
metafile_description_label.pack(pady = (0, 20), padx = 15, expand = True)

metafile_button = ctk.CTkButton(metafile_frame, text = "Start", width = 180, height = 40, fg_color = color_metafile, hover_color = color_hover_metafile, font = ("Arial", 15, "bold"), command =  metafile)
metafile_button.pack(pady=(0, 25))


safefile_frame = ctk.CTkFrame(utility_main_frame, width = 265, height = 350, fg_color = color_dark_2)
safefile_frame.pack(side = "left", expand = True, padx = 10)
safefile_frame.pack_propagate(False)

safefile_label = ctk.CTkLabel(safefile_frame, text = "SafeFile", font = ("Arial", 22, "bold"), text_color = color_white)
safefile_label.pack(pady=(25, 15))

safefile_description_label = ctk.CTkLabel(safefile_frame, text = "Manage your secure local vault for sensitive files.", font = ("Arial", 14), text_color = description_text, wraplength = 220, justify = "center")
safefile_description_label.pack(pady = (0, 20), padx = 15, expand = True)

safefile_button = ctk.CTkButton(safefile_frame, text = "Start", width = 180, height = 40, fg_color = color_safefile, hover_color = color_hover_safefile, font = ("Arial", 15, "bold"), command = safefile)
safefile_button.pack(pady=(0, 25))


main_window.mainloop()