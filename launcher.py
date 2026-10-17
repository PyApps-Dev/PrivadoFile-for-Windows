import os
import subprocess
import sys

dossier_base = os.path.dirname(os.path.abspath(__file__))

script_main = os.path.join(dossier_base, "main_window.py")

subprocess.Popen([sys.executable, script_main])