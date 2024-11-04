import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import json
import threading

# Speicherdatei für die Auswahl der Parameter im Benutzerordner
config_file = os.path.join(os.path.expanduser("~"), "lost_ark_config.json")

# Verfügbare Startparameter
start_parameters = [
    "-useallavailablecores",
    "-high",
    "-notexturestreaming",
    "-novsync",
    "-nomoviestartup",
    "-lanplay"
]

# App-ID für Lost Ark
app_id = "1599340"  # Lost Ark App-ID

# Sucht rekursiv nach steam.exe auf allen Laufwerken
def find_steam_exe():
    for drive in [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]:
        for root, _, files in os.walk(drive):
            if "steam.exe" in files:
                return os.path.join(root, "steam.exe")
    return None

# Lade die gespeicherten Parameter
def load_config():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return {}

# Speichert die aktuellen Parameter
def save_config(selected_params):
    with open(config_file, "w") as f:
        json.dump(selected_params, f)

# Startet Lost Ark mit den ausgewählten Parametern in einem Thread
def start_game():
    steam_path = find_steam_exe()
    if not steam_path:
        messagebox.showerror("Fehler", "Steam konnte nicht gefunden werden.")
        return

    selected_params = [param for param, var in param_vars.items() if var.get()]
    save_config(selected_params)  # Speichert die aktuelle Auswahl

    # Zeige Startmeldung
    status_label.config(text=f"Lost Ark wird gestartet... [Parameter: {' '.join(selected_params)}]")
    try:
        subprocess.Popen([steam_path, "-applaunch", app_id] + selected_params, creationflags=subprocess.CREATE_NO_WINDOW)
        print("Startbefehl gesendet.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Starten des Spiels: {e}")
        status_label.config(text="Fehler beim Starten von Lost Ark")

# Führt die Startfunktion in einem separaten Thread aus
def on_start_button_click():
    threading.Thread(target=start_game).start()

# Darkmode Farben
bg_color = "#2e2e2e"
fg_color = "#ffffff"
button_color = "#444444"
check_color = "#3b3b3b"

# GUI erstellen
root = tk.Tk()
root.title("Lost Ark Startparameter")
root.geometry("300x300")
root.config(bg=bg_color)

# Darkmode Style für Checkboxes und Buttons
config = load_config()
param_vars = {}

for param in start_parameters:
    var = tk.BooleanVar(value=(param in config))
    cb = tk.Checkbutton(root, text=param, variable=var, bg=bg_color, fg=fg_color, selectcolor=check_color, activebackground=bg_color)
    cb.pack(anchor="w", padx=10, pady=2)
    param_vars[param] = var

# Start-Button
start_button = tk.Button(root, text="Start", command=on_start_button_click, bg=button_color, fg=fg_color, activebackground=fg_color, activeforeground=bg_color)
start_button.pack(pady=10)

# Status-Label für Startmeldung
status_label = tk.Label(root, text="", bg=bg_color, fg=fg_color)
status_label.pack(pady=10)

root.mainloop()
